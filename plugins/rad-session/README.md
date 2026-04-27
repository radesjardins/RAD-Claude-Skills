# rad-session — Claude Code workflow lifecycle: init, startup, wrapup.

> **v3.0 — Lifecycle expansion.** Adds `/init` for one-time project bootstrap, plus two Python scripts (`detect-stack.py`, `detect-resources.py`) that make stack and resource detection deterministic. **rad-session 3.0 absorbs the retired rad-stack-guide** — its stack-detection value is now in `/init`, in the same lifecycle as `/startup` and `/wrapup`.

Claude Code has built-in memory (CLAUDE.md + native Auto Memory since v2.1.59). **rad-session doesn't replace it — it owns the workflow lifecycle around it.**

## The three-phase lifecycle

| Phase | When | Skill | What it does |
|---|---|---|---|
| **Init** | Once, when you start work in a project | `/init` | Detects stack deterministically, finds MCPs and CLIs, scaffolds CLAUDE.md (or proposes additions), recommends which rad-* plugins fit your stack |
| **Startup** | Every session | `/startup` | Reads HANDOFF.md + session log, runs Phase 2.5 Resource Discovery, presents a concise briefing of where you left off and what's available |
| **Wrapup** | Every session | `/wrapup` | Writes structured HANDOFF.md with "what NOT to do" field, prunes CLAUDE.md with diff confirmation (Resources section protected), surfaces insights for native Auto Memory |

Plus `/add-resource` (any time, registers a new tool) and a PreCompact hook (auto-fires on context compaction).

## What's in the plugin

| Component | Triggers | What it does |
|---|---|---|
| **`/init`** *(new in 3.0)* | start of project work, "set up rad-session here", "bootstrap" | One-time project bootstrap. Runs the two detection scripts, scaffolds CLAUDE.md with detected stack/resources, recommends rad-* plugins for your stack, sets up `.claude/session-log.md`. Safe to re-run (merges, doesn't overwrite). |
| **`/startup`** | start of session, "/startup", "where did we leave off" | Reads HANDOFF.md + session log, detects git state, **runs Phase 2.5 Resource Discovery** (now uses `detect-resources.py` deterministically when Python is available), presents briefing |
| **`/wrapup`** | end of session, "/wrapup", "wrap up" | Writes HANDOFF.md with "What NOT to do" field, appends session log (20-entry cap), prunes CLAUDE.md with diff confirmation (**Resources section protected**), surfaces insights for native Auto Memory |
| **`/add-resource`** | "add this MCP", "remember the supabase CLI", "register this resource" | Appends an MCP/CLI/script/note to CLAUDE.md's `## Resources` section so `/startup` picks it up next session |

Plus one hook:

| Hook | Event | What it does |
|---|---|---|
| `precompact` | `PreCompact` | Fires automatically when context compaction begins. Injects a systemMessage telling Claude to run `/wrapup` before the compacted context loses session state. |

Plus two Python scripts (new in 3.0):

| Script | What it does |
|---|---|
| `scripts/detect-stack.py` | Scans project for languages, frameworks (via package.json deps + marker files), package manager, deploy targets, infrastructure, toolchain. Returns structured JSON. |
| `scripts/detect-resources.py` | Scans for MCP servers (`.mcp.json` + `.claude/settings.json`), stack CLIs (marker-file inference + optional PATH check), parses CLAUDE.md `## Resources` section, computes drift. Returns structured JSON. |

Both are pure stdlib Python 3.8+. No `pip install` required. Used by `/init` and optionally by `/startup` Phase 2.5.

## Files the plugin maintains

| File | Purpose | Who writes it |
|---|---|---|
| `CLAUDE.md` | Permanent project rules + **`## Resources` section** (MCPs, CLIs, scripts, notes) | `/init` (scaffold), `/add-resource` (additions); pruned by `/wrapup` (Resources protected) |
| `HANDOFF.md` | Current session state — status, decisions, what NOT to do, open work, insights | `/wrapup` (overwrites each session) |
| `.claude/session-log.md` | Session history, newest first, capped at 20 entries | `/init` (creates header), `/wrapup` (prepends one entry per session) |

Notably **not** managed: `~/.claude/projects/<project>/memory/` — that's owned by Claude Code's native Auto Memory (v2.1.59+). rad-session surfaces insights in the wrapup summary so native auto-memory can pick them up, but never writes to that path.

## What `/init` does (the headline of 3.0)

**Run once per project.** Bootstraps everything `/startup` and `/wrapup` need.

1. **Verify Python availability** — falls back to LLM-based detection if missing, with a warning that the bootstrap will be less reliable.
2. **Run `detect-stack.py`** — scans languages, frameworks, package manager, scripts, deploy targets, infrastructure. Replaces "ask the LLM to read package.json."
3. **Run `detect-resources.py --check-clis`** — scans `.mcp.json`, `.claude/settings.json`, marker files. Verifies CLIs in PATH. **Flags CLIs the project assumes but aren't installed.**
4. **Synthesize a stack summary** — scannable report of what's there.
5. **Recommend rad-* plugins** — based on detected stack, only currently-shipping plugins (no references to retired ones). Tells you what each adds, doesn't auto-install.
6. **Propose CLAUDE.md scaffold** (greenfield) or **propose additions** (existing). Shows diff. Waits for confirmation.
7. **Create `.claude/session-log.md`** with header line if missing.
8. **Final report** — what was created/modified, what to do next.

Safe to re-run: merges, never overwrites. Has `--non-interactive` and `--dry-run` flags for autonomous setup runs.

### Why `/init` exists

Stack detection used to live in two places:
- `rad-stack-guide` had a `/detect-stack` skill (ran once per project)
- `rad-session`'s `/startup` Phase 2.5 (ran every session)

The duplication was awkward, and rad-stack-guide's other value (orchestrating specialist reviewers) collapsed when the framework reviewers were archived. **3.0 absorbs the per-project setup into rad-session's lifecycle.** rad-stack-guide is retired.

If you previously used rad-stack-guide's `/detect-stack`, your existing CLAUDE.md content stays intact — it was just markdown. Run `/init` once to re-establish the `## Resources` section in the new format.

## Phase 2.5 Resource Discovery in `/startup` (refined in 3.0)

`/startup` runs a read-only resource-detection pass every session. **In 3.0 it prefers `detect-resources.py` when Python is available** — same data, deterministic. The LLM-based marker scanning remains as fallback.

Detection covers:

- **`.mcp.json`** and `.claude/settings.json` → MCP servers available to the project
- **Stack marker files** → implied CLIs (full table in `skills/startup/SKILL.md` Phase 2.5.2)
- **`package.json`** → `packageManager` field + top scripts (`dev`, `build`, `test`, `typecheck`, `lint`, ...)
- **`.env.example`** → variable **names** only (never values)
- **CLAUDE.md `## Resources` section** → documented source of truth, reconciled against what's actually detected

### Example briefing output

```
Project: my-app
Type: Coding (Next.js + Supabase)
Branch: main (up to date)
Last session: 2026-04-25 — Auth flow complete, billing next

Where we left off:
  - Stripe checkout endpoint wired, webhook handler still TODO
  - Supabase RLS policies applied for users table

Watch out for:
  - Do not mock the Stripe webhook in integration tests — signature verify must hit real code path

Resources available:
  MCPs: supabase, stripe, coolify
  Stack CLIs: supabase, gh, docker
  Scripts (pnpm): dev, build, test, typecheck, lint
  Env template: DATABASE_URL, STRIPE_SECRET_KEY, SUPABASE_ANON_KEY (.env.example)

Ready to continue. What would you like to work on?
```

## Disciplined `/wrapup`

`/wrapup` writes a **structured HANDOFF.md** with sections most handoff tools skip:

- **What NOT to do** — failed approaches in the canonical `TRIED: … FAILED BECAUSE: … CORRECT APPROACH: …` form. Prefix tokens are load-bearing — `/startup` extracts them literally.
- **Key Decisions** — the *why* behind architecture/approach choices, not just the what.
- **Open Work** — state-of-play as descriptions, never as instructions ("EBirdProvider started, API auth not wired" — not "Next, wire up the eBird API auth").
- **Key Insights** — API quirks, environment gotchas, architectural constraints not in CLAUDE.md.

Then it prunes CLAUDE.md with **diff confirmation** (you see what's about to be removed and can say "undo item X" before anything is saved), **protecting the `## Resources` section** from removal. An auto-proceed threshold lets small low-risk prunes (≤3 removals, no rules/architecture/Resources sections, no "must/never/always" markers) skip the gate — autonomous and loop-mode sessions don't hang.

Nothing else in the Claude Code ecosystem actively shrinks CLAUDE.md.

## PreCompact safety net

When Claude Code's context compaction fires, the `PreCompact` hook injects a systemMessage instructing Claude to run `/wrapup` before anything else. The injected message enumerates the six capture targets explicitly (decisions, failed approaches, user corrections, modified files, open work, insights) so even smaller models with thin post-compaction context can reconstruct usable state.

No config required; the hook ships with the plugin.

## Quick Start

```bash
/plugin marketplace update rad-claude-skills
/plugin install rad-session@rad-claude-skills
```

**First time in a project:**
```
/init
```

**Start of every session:**
```
/startup
```

**Register resources as you discover them:**
```
remember we have the coolify MCP available for this project
```

**End of every session:**
```
/wrapup
```

Works with coding projects (captures git state + stack resources) and non-coding projects (scans recently modified files; still surfaces documented resources).

## How this compares to alternatives

| | **rad-session 3.0** | Native CC Auto Memory | claude-plugins-official/remember | claude-mem | thepushkarp/handoff |
|---|---|---|---|---|---|
| Project bootstrap (`/init`) | ✅ **unique** (3.0) | ❌ | ❌ | ❌ | ❌ |
| Resource discovery (MCPs/CLIs/stack) | ✅ **unique** | ❌ | ❌ | ❌ | ❌ |
| Active CLAUDE.md prune w/ diff | ✅ **unique** | ❌ (grows) | compression | ❌ | ❌ |
| Deterministic stack detection (Python scripts) | ✅ (3.0) | ❌ | ❌ | ❌ | ❌ |
| "What NOT to do" field | ✅ | ❌ | ❌ | ❌ | partial |
| PreCompact safety net | ✅ | ✅ (built in) | ✅ | ✅ | ✅ |
| Zero dependencies for skills (Python optional for scripts) | ✅ | ✅ | ❌ (Haiku) | ❌ (Chroma) | ✅ |
| Setup cost | plugin install + `/init` | **zero — built in** | plugin install | plugin install | plugin install |

**When to use rad-session:** you want structured workflow lifecycle for a project — bootstrap once, orient each session, capture each session.

**When you don't need it:** simple single-language projects where CLAUDE.md + native Auto Memory is enough. Don't install what you won't use.

**Complementary:** rad-session pairs well with `basic-memory` MCP if you want semantic recall *across* projects — they're not competing.

## What's NOT in scope

- **Does not install rad-* plugins for you** — `/init` recommends; you decide.
- **Does not configure MCP servers** — detects what's already there. Adding new MCPs is a separate concern (`/configure-mcp` in rad-agentic-company-builder, or just edit `.mcp.json`).
- **Does not run tests, builds, or any side-effect commands** beyond two read-only Python scripts and `mkdir .claude/`.
- **Does not exec stack binaries** without `--check-clis` opt-in.
- **Does not read `.env`** — only `.env.example`, and only variable names.
- **Does not orchestrate code reviews** — that role belonged to retired rad-stack-guide. Use the specialist reviewers directly (rad-code-review for general, rad-supabase / rad-coolify-orchestrator / rad-a11y / rad-chrome-extension for their domains).

## Version

**3.0.0** — **Lifecycle expansion + rad-stack-guide consolidation.**
- New `/init` skill — one-time project bootstrap. Detects stack deterministically, scaffolds CLAUDE.md, recommends rad-* plugins for the detected stack.
- New `scripts/detect-stack.py` — pure-Python stack scanner. Languages, frameworks (via package.json deps + marker files), package manager, scripts, deploy targets, infrastructure.
- New `scripts/detect-resources.py` — pure-Python MCP + CLI scanner with PATH verification (`--check-clis`) and drift detection vs CLAUDE.md `## Resources`.
- `/startup` Phase 2.5 now prefers `detect-resources.py` when Python is available; LLM-based marker scanning remains as fallback.
- `rad-stack-guide` retired. Its stack-detection value is now in `/init`. Its review-orchestration value collapsed when the framework reviewers were archived; rad-code-review handles its multi-pass internally.
- README repositioned around the three-phase lifecycle (init → startup → wrapup).

**2.2.0** — Optimized for Opus 4.7. Parallel-batched `/startup` reads, explicit conversation-synthesis scan in `/wrapup`, auto-proceed threshold for low-risk CLAUDE.md prunes, stale-handoff auto-refresh from git log, canonical `TRIED / FAILED BECAUSE / CORRECT APPROACH` trap format, expanded stack marker table, PreCompact hook payload that enumerates capture targets explicitly.

**2.1.0** — PreCompact hook for silent-context-loss prevention; Phase 5 stops writing to native Auto Memory path; repositioned pitch around Resource Discovery and wrapup discipline.

**2.0.0** — Added `/add-resource` skill, `/startup` Phase 2.5 Resource Discovery, `/wrapup` prune protection for the Resources section.

**1.0.0** — Initial release: `/wrapup` and `/startup` skills.

## License
Apache-2.0
