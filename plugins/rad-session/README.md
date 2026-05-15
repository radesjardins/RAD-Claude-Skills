# rad-session — agent session lifecycle: init, startup, wrapup, with cross-machine continuity for Claude + Codex.

**What it is.** A four-skill plugin that gives agent-driven projects a structured session lifecycle: bootstrap a project once, orient each session at the start, capture each session at the end, register tools as you discover them. Works for a single agent on a single machine — and **transparently keeps PC ↔ GitHub ↔ Laptop in sync across Claude Code and Codex sessions** when a git remote exists.

**What it solves.** The default Claude / Codex experience loses session state at compaction, can't tell you what tools the project has, lets the operating manual grow forever, and forgets everything when you switch machines or agents. rad-session keeps `docs/status.md` (evidence-based reality), pairs it with `docs/planning/current.md` (intent — owned by rad-planner), archives shipped milestones, and pulls/commits/pushes the relevant files via git so your laptop sees what your PC did, and your Codex session sees what your Claude session did.

**What it isn't.** It is **not** an automation layer over your code: it never runs builds, never touches non-session files in commits, and never force-pushes. It does not write your strategic docs — that's rad-planner's job. It does not invent state — `/wrapup` writes from **evidence** (git diff, test output, plan-task state), not chat synthesis.

## The canonical doc structure (v5.0)

rad-session 5.0 is built around the canonical structure aligned with published OpenAI / Anthropic project-structure research. The structure is shared with rad-planner 4.0 via the **single-writer rule** (each file has exactly one automated writer) with a **sectioned-writer exception** for the operating manual.

```
<project-root>/
├── CLAUDE.md or AGENTS.md       # operating manual — conditional on agent scope
├── docs/
│   ├── vision.md                # rad-planner
│   ├── architecture.md          # rad-planner
│   ├── status.md                # rad-session — EVIDENCE-BASED reality
│   ├── planning/
│   │   ├── current.md           # rad-planner — INTENT for the active milestone
│   │   └── archive/             # rad-session — one file per shipped milestone
│   ├── decisions/               # rad-planner (creation); rad-session prompts at wrapup
│   │   ├── README.md
│   │   └── NNNN-*.md            # ADRs, sequence-numbered
│   └── roadmap.md               # optional
├── .rad/profile                 # mode (mentor/dev) + agent_scope + multi_branch_status
├── .claude/settings.json        # if Claude in scope
└── .codex/config.toml           # if Codex in scope
```

→ Canonical specs: [`docs/doc-conventions.md`](../../docs/doc-conventions.md), [`docs/cross-plugin-contracts.md`](../../docs/cross-plugin-contracts.md), [`docs/status-md-schema.md`](../../docs/status-md-schema.md)

## Intent vs. reality split (the v5.0 insight)

v4.0 conflated "what we're trying to do" with "what's actually true." v5.0 separates them:

| File | What it captures | Written by |
|---|---|---|
| `docs/planning/current.md` | **Intent** for the active milestone — objective, acceptance criteria, validation commands, planned changes, stop conditions | rad-planner `/plan` |
| `docs/status.md` | **Reality** — branch state, last completed work, files changed recently, latest validation results, decisions made during execution, blockers, next recommended step | rad-session `/wrapup` |

`/wrapup` writes `docs/status.md` from **evidence** (git log, git diff, test output, plan-task checkbox state) — not from what the LLM remembers about the conversation. This is the structural shift that makes the new artifact reliable across compaction, machine switches, and agent switches.

## Sectioned-writer rule (the operating manual)

The operating manual is the **one file with two automated writers**. The single-writer rule is preserved at the section level:

| Section | Owner |
|---|---|
| Project, Read order, Hard boundaries, Engineering rules, Definition of done, Escalate triggers | rad-planner `/plan` M6 (Constitution) |
| Commands, Compact Instructions (CLAUDE.md only), Claude-specific behavior (CLAUDE.md only), `@AGENTS.md` import line (CLAUDE.md shim case) | rad-session `/init` (Operational) |
| Any other section | User-owned. Plugins preserve as-is and surface in output. |

`/wrapup` Phase 5 (prune) operates on **Operational sections only**. Constitution sections are never touched by rad-session. User-added sections are never touched by either plugin.

## Agent scope routing

`/init` asks once whether the project will be worked by Claude, Codex, or both — and routes operating-manual writes accordingly:

| `agent_scope` | Files scaffolded |
|---|---|
| `claude_only` | `CLAUDE.md` (canonical) |
| `codex_only` | `AGENTS.md` (canonical) |
| `claude_and_codex` | `AGENTS.md` (canonical) + `CLAUDE.md` (`@AGENTS.md` shim with Claude-specific Operational sections) |

The choice is persisted to `.rad/profile`. `/startup` and `/wrapup` read the profile and behave per scope.

## The four skills

| Skill | When | What it does |
|---|---|---|
| **`/init`** | Once per project | Detects stack via Python scripts (`detect-stack.py`, `detect-resources.py`, `audit-plugin-bloat.py`), asks the agent-scope question, scaffolds the operating manual's **Operational sections only** (sectioned-writer rule), scaffolds `docs/status.md`, creates `.rad/profile`, creates `.claude/settings.json` / `.codex/config.toml` per scope, runs the plugin-bloat audit, gap-checks strategic docs and recommends `/rad-planner:plan` if any are missing. |
| **`/startup`** | Every session | **Doorman model — under 5 seconds wall clock.** Fetches origin and prompts to pull when behind. Reads `.rad/profile`, the operating manual per scope (including non-canonical filenames via header heuristic), `docs/status.md`, `docs/planning/current.md`. Surfaces a concise briefing (<35 lines). Read-only — never writes. |
| **`/wrapup`** | Every session | **9-phase workflow.** Refuses if no work changed since the last status (Phase 0). Writes `docs/status.md` from **evidence** (Phase 2). Detects candidate decisions mechanically (dep adds, schema changes, env additions, new top-level dirs) plus soft triggers (Phase 3). Mode-aware: mentor mode teaches and drafts an ADR; dev mode shows a quick list. Runs cross-doc validators from rad-planner (`doc-redundancy.py` + `doc-contradiction.py`) (Phase 4). Prunes the operating manual's Operational sections only (Phase 5). Detects milestone-shipped state (all ACs checked) and proposes archiving `current.md` to `planning/archive/YYYY-MM-DD-MN-slug.md` (Phase 6). Commits + prompts to push (Phase 7). Anomaly-gated final output (silent on success) (Phase 8). |
| **`/add-resource`** | Any time | Register a new MCP server, CLI tool, script, or note in the operating manual's Resources section so `/startup` picks it up next session. |

## Slash command flags

| Skill | Triggers | Flags |
|---|---|---|
| **`/init`** | "/init", "set up rad-session", "bootstrap this project" | `--non-interactive` skip prompts · `--dry-run` preview without writing · `--agents <scope>` set agent scope without prompting (`claude_only` / `codex_only` / `claude_and_codex`) |
| **`/startup`** | "/startup", "where did we leave off", "catch me up", "what's the state" | `--auto-pull` skip Phase 0 prompt, fast-forward silently · `--no-pull` skip sync entirely · `--quiet` even more terse briefing |
| **`/wrapup`** | "/wrapup", "wrap up", "end of session", "save state" | `--push` skip Phase 7 prompt, push immediately · `--no-push` commit locally only · `--quick` skip Phase 3 deep scan + Phase 4 validators + Phase 5 prune · `--non-interactive` suppress all prompts · `--force` override Phase 0 no-work check |
| **`/add-resource`** | "add this MCP", "remember the supabase CLI", "register this resource" | (none) |

Combine flags freely — e.g. `/wrapup --push --quick` (autonomous-loop wrapup), `/startup --no-pull` (offline work).

Plus one hook:

| Hook | Event | What it does |
|---|---|---|
| `precompact` | `PreCompact` | Fires automatically when context compaction begins. Injects a systemMessage telling the agent to run `/wrapup` before the compacted context loses session state. |

## Mode-aware behavior (mentor vs. dev)

`.rad/profile` carries a `mode` field that gates teaching depth in `/wrapup`:

| Mode | `/wrapup` Phase 3 behavior |
|---|---|
| `mentor` (default) | When a candidate decision is detected, surface a teaching block explaining why this is decision-worthy, then draft an ADR for the user to review. |
| `dev` | Surface candidate decisions as a quick list. No teaching block, no draft. User picks Y/N. |

Mode is project-level; user can flip it any time by editing `.rad/profile`.

## Cross-machine + cross-agent continuity

If your project has a git remote, rad-session keeps the canonical docs in sync — across machines AND across agents (Claude ↔ Codex):

| Phase | What it does |
|---|---|
| `/init` | Ensures `docs/status.md`, `docs/planning/`, `docs/decisions/`, and the operating manual aren't gitignored. |
| `/wrapup` Phase 7 | Auto-commits `docs/status.md` + any `planning/archive/` entries + any new `decisions/NNNN-*.md` ADRs + operating-manual changes. Prompts: `Push session files to origin? (Y/n)`. Commit message: `session: YYYY-MM-DD on <hostname> — <status>`. |
| `/startup` Phase 0 | Fetches origin and prompts to pull when behind. Lists incoming commits before approval. On approval, fast-forwards. On decline, briefing leads with `⚠ Reading stale local state`. If the most recent session commit was made on a different host, briefing also leads with `Continuing from <other-host>`. |

**Auto-commit, prompted push.** Local commits are cheap so they always happen. Push is a deliberate "I'm about to switch machines" decision. Stack multiple unpushed session commits on the same machine; push when ready to hand off.

**Multi-branch active hybrid.** When `multi_branch_status = true` in `.rad/profile`, `/wrapup` writes per-branch status (e.g. `docs/status.feat-invoice-pdf.md` alongside the main `docs/status.md`). Opt-in for projects that maintain several active branches simultaneously.

**Safety:** wrapup never force-pushes, never touches non-session files, and bails cleanly on diverged history. Startup never merges, never rebases, never discards local work — it only attempts a fast-forward pull and warns if it can't.

## Working with rad-planner

rad-session 5.0 and rad-planner 4.0 are **soft-coupled** — each is independently useful, and they share contracts via the canonical doc structure:

1. **Operating manual (sectioned-writer).** rad-planner writes Constitution sections during `/plan` M6; rad-session writes Operational sections during `/init`. Each parses headers and modifies only its owned list.
2. **`docs/status.md` (single-writer, rad-session).** Written by `/wrapup` from evidence. Read by `/plan` to ground the conversation in current reality.
3. **`docs/planning/current.md` (single-writer, rad-planner).** Written by `/plan` from intent. Read by `/wrapup` to detect milestone-shipped state.
4. **`docs/decisions/` (creation by rad-planner; prompts by both).** rad-planner creates the directory + README at `/plan` M6 and seeds initial ADRs. rad-session prompts to add new ADRs when candidate decisions surface at `/wrapup`. The user's `y` is what authorizes the write.
5. **Cross-doc validators.** rad-planner ships four Python validators at `plugins/rad-planner/scripts/`: `plan-lint.py`, `status-validator.py`, `doc-redundancy.py`, `doc-contradiction.py`. rad-session's `/wrapup` Phase 4 invokes `doc-redundancy.py` and `doc-contradiction.py` against the project; if rad-planner is not installed, Phase 4 silently no-ops.

**rad-session works standalone** — `/init` notes when strategic docs are missing; `/wrapup` skips cross-doc validators gracefully. **rad-planner works standalone** — `/plan` produces strategic docs whether rad-session is installed or not.

## What `/init` does (one-time bootstrap)

1. **Verify Python availability** — falls back to LLM-based detection if missing.
2. **Run `detect-stack.py`** — scans languages, frameworks, package manager, scripts, deploy targets, infrastructure.
3. **Run `detect-resources.py --check-clis`** — scans `.mcp.json`, `.claude/settings.json`, marker files. Flags CLIs the project assumes but aren't installed.
4. **Ask agent-scope** — Claude only / Codex only / both. Persists to `.rad/profile`.
5. **Run `audit-plugin-bloat.py`** — proposes per-project `enabledPlugins` disables to cut token cost on projects that don't use a given plugin's stack.
6. **Scaffold operating manual Operational sections** per scope (sectioned-writer rule).
7. **Scaffold `docs/status.md`** with the 8-section schema, all sections marked "No data yet — populated by /wrapup from evidence."
8. **Scaffold `.claude/settings.json` and/or `.codex/config.toml`** per scope.
9. **Write `.rad/profile`** with mode + agent_scope + multi_branch_status.
10. **Final report** — what was created/modified, what to do next (typically: `/rad-planner:plan` to populate strategic docs and Constitution sections).

Safe to re-run: merges, never overwrites. Has `--non-interactive`, `--dry-run`, `--agents` flags for autonomous setup runs.

## Example `/startup` briefing

```
Project: wayfinder
Type: Coding (Next.js + Supabase + Drizzle)
Branch: main (up to date)
Mode: mentor    Scope: claude_only

Current milestone: M2 — Activity-constraint engine
Status: on track

Where we left off (status.md):
  - Constraint evaluator implemented at lib/constraints/evaluator.ts (24/24 tests passing)
  - Constraint type definitions locked at lib/constraints/types.ts

Open acceptance criteria (current.md):
  - [ ] Failure reasons surfaced (which constraint failed, by how much)
  - [ ] UI handles 1+ constraint sets per user
  - [ ] Visual Crossing rate-limit handling

Latest validation:
  - bun test lib/constraints/ → pass (24/24)
  - bun run typecheck → pass

Next recommended step:
  Start the Drizzle CRUD layer in lib/constraints/queries.ts. First decide: per-user vs per-account scope.

Ready to continue. What would you like to work on?
```

See `references/briefing-examples.md` for the full template set (5 shapes).

## Upgrading from 3.x / 4.x

Run the bundled migration helper **before** installing rad-session 5.0:

```bash
# Preview the changes (writes nothing)
python3 ${rad-claude-skills}/plugins/rad-session/scripts/migrate-to-v5.py /path/to/your/project --dry-run

# Apply (interactive — confirms each transformation)
python3 ${rad-claude-skills}/plugins/rad-session/scripts/migrate-to-v5.py /path/to/your/project

# Or apply non-interactively (safe transforms only)
python3 ${rad-claude-skills}/plugins/rad-session/scripts/migrate-to-v5.py /path/to/your/project --non-interactive
```

**What gets transformed:**

| v3.x / v4.x artifact | v5.0 outcome |
|---|---|
| `HANDOFF.md` at project root | Archived; `docs/status.md` replaces it. User prompted to seed status.md from archived content. |
| `.claude/session-log.md` | Archived; `docs/planning/archive/` replaces it (per-milestone, not per-session). |
| v4.0 8-doc files at project root (`PRD.md`, `ARCHITECTURE.md`, `PLAN.md`, `DECISIONS.md`, `ASSUMPTIONS.md`) | Moved to `docs/` per canonical structure. DECISIONS.md splits into sequence-numbered ADRs. |
| `CLAUDE-FRAGMENT.md` (v4.0 transient) | Archived. Role replaced by rad-planner `/plan` M6 writing Constitution sections directly. |
| Existing operating manual | Preserved. User opts in to adding Operational scaffold (`## Commands`, etc.). |

All originals archive to `.rad-archive/<UTC-timestamp>/` (gitignored). The archive's `manifest.json` records every action.

**Re-run safety:** the migration script is a no-op on projects already on the v5.0 layout.

> See `scripts/README.md` for the full `migrate-to-v5.py` contract.

## How this compares to alternatives

|  | **rad-session 5.0** | claude-plugins-official/remember | claude-mem | thepushkarp/handoff |
|---|---|---|---|---|
| Project bootstrap (`/init`) with deterministic stack detection | ✅ | ❌ | ❌ | ❌ |
| Multi-agent (Claude + Codex) support | ✅ **unique** | ❌ | ❌ | ❌ |
| Intent-vs-reality split (status.md from evidence) | ✅ **unique** | ❌ | ❌ | ❌ |
| Sectioned-writer operating manual | ✅ **unique** | ❌ | ❌ | ❌ |
| Cross-machine sync via git (auto-commit + prompted push) | ✅ | ❌ | ❌ | ❌ |
| Active operating-manual prune | ✅ | compression | ❌ | ❌ |
| Cross-doc validators (redundancy + contradiction) | ✅ | ❌ | ❌ | ❌ |
| PreCompact safety net | ✅ | ✅ | ✅ | ✅ |
| Zero dependencies for skills (Python optional for scripts) | ✅ | ❌ (Haiku) | ❌ (Chroma) | ✅ |

**When to use rad-session:** you want a structured workflow lifecycle for an agent-driven project across Claude and/or Codex — bootstrap once, orient each session, capture each session from evidence.

## Quick Start

```bash
/plugin marketplace update rad-claude-skills
/plugin install rad-session@rad-claude-skills
```

**First time in a project:**
```
/init                                # interactive bootstrap
/init --non-interactive              # accept proposed scaffold without prompting
/init --dry-run                      # preview detection + scaffold
/init --agents claude_and_codex      # pre-set agent scope without prompting
```

**Start of every session:**
```
/startup                # fetches origin, prompts to pull if behind, then reads canonical docs
/startup --auto-pull    # fast-forward silently when behind
/startup --no-pull      # skip sync entirely
```

**Register resources as you discover them:**
```
remember we have the coolify MCP available for this project
```

**End of every session:**
```
/wrapup                 # auto-commits, prompts to push
/wrapup --push          # commit + push without prompting
/wrapup --no-push       # commit locally only
/wrapup --quick         # skip Phase 3/4/5 (terse wrapup)
```

**Switching machines or agents.** Run `/wrapup --push` on the PC (Claude). On the laptop (Codex), the user's Codex session reads the same `docs/status.md` directly — or via `/wrapup` Codex equivalents if the agent has its own session lifecycle. No manual git work, no copy-paste.

## What's NOT in scope

- **Does not write strategic docs** — that's rad-planner's `/plan`. `/init` notes missing strategic docs and recommends `/rad-planner:plan`.
- **Does not install rad-* plugins for you** — `/init` recommends; you decide.
- **Does not configure MCP servers** — detects what's already there.
- **Does not run tests, builds, or any side-effect commands** beyond detection scripts and `mkdir`.
- **Does not exec stack binaries** without `--check-clis` opt-in.
- **Does not read `.env`** — only `.env.example`, and only variable names.
- **Does not orchestrate code reviews** — use the specialist reviewers directly (rad-code-review for general, rad-supabase / rad-coolify-orchestrator / rad-a11y / rad-chrome-extension for their domains).

## Version

**5.0.0** — **Canonical doc structure + intent-vs-reality split + multi-agent support.** Aligned with published OpenAI/Anthropic project-structure research.
- **`docs/status.md` replaces `HANDOFF.md`** — project-scoped, evidence-based, written from git + test output, not chat synthesis.
- **`docs/planning/current.md` (rad-planner-owned)** carries intent. `docs/status.md` (rad-session-owned) carries reality. The split makes each artifact reliable independently.
- **`docs/planning/archive/`** replaces `.claude/session-log.md` — one file per shipped milestone, not per session.
- **Sectioned-writer rule for the operating manual** — rad-planner writes Constitution; rad-session writes Operational. Each parses headers, modifies only owned sections, preserves user-added sections.
- **Agent scope routing** — `/init` asks once (Claude / Codex / both); persists to `.rad/profile`; all skills read the profile and write to the correct file(s).
- **Mode-aware `/wrapup` Phase 3** — `mentor` mode teaches and drafts ADRs; `dev` mode shows quick lists.
- **Cross-doc validators integrated** — `/wrapup` Phase 4 calls `doc-redundancy.py` and `doc-contradiction.py` from rad-planner.
- **Milestone-shipped archive** — `/wrapup` Phase 6 detects all ACs checked in `current.md` and prompts to archive.
- **Multi-branch active hybrid** — opt-in per-branch status via `multi_branch_status` in `.rad/profile`.
- **Anomaly-gated final output** preserved from 3.5.2 — silent on success.
- **PreCompact hook** preserved.

**4.0.0** — **8-doc standardization (soft-coupled with rad-planner 3.0).** Introduced `CLAUDE-FRAGMENT.md` handoff, strategic-doc gap-check in `/startup` Phase 1.5, `DECISIONS.md` prompt in `/wrapup` Phase 3.5. Single-writer rule: rad-session owned CLAUDE.md / HANDOFF.md / session-log; rad-planner owned PRD / ARCH / ASSUMPTIONS / DECISIONS / PLAN / tasks.md / FRAGMENT. **Retired in v5.0 in favor of the canonical doc structure.**

**3.7.0** — Removed Haiku model pin (context-window regression fix).

**3.6.0** — Per-project plugin-bloat audit in `/init` (Step 5.5). `audit-plugin-bloat.py` detects 10 stack signals and writes `enabledPlugins` disables to `.claude/settings.local.json`. ~1–3K tokens cut from baseline per turn on typical projects.

**3.5.2** — Anomaly-gated final output for `/wrapup` (silent on success).

**3.5.1** — Removed Phase 5 "surface insights" (empirically dead — zero downstream pickup across 12+ wrapups).

**3.5.0** — Haiku-pinned skills (reverted in 3.7), cached resource scan, low-activity auto-quick.

**3.4.0** — Maintenance mandatory + per-bullet caps. Closed the silent-skip-of-maintenance defect.

**3.3.0** — Verify-before-read sync on `/startup`. Fetches first, prompts to pull when behind, lists incoming commits.

**3.2.0** — Slim wrapup. Recency-bounded tagging, mechanical session-log derivation, auto-skip prune when unchanged.

**3.1.0** — Cross-machine continuity via auto-commit + prompted push.

**3.0.0** — Lifecycle expansion. Added `/init`, two Python detection scripts. Absorbed retired rad-stack-guide.

**2.x** — Original Resource Discovery and CLAUDE.md prune protection.

**1.0.0** — Initial release: `/wrapup` and `/startup` skills.

## License
Apache-2.0
