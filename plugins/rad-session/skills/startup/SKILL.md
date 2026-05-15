---
name: startup
description: >
  Start-of-session skill for v5.0 — orient a new session by reading the operating
  manual (CLAUDE.md / AGENTS.md per .rad/profile agent_scope), docs/status.md
  (evidence-based reality from last /wrapup), docs/planning/current.md (active
  plan), and presenting a concise resume briefing. Read-only — never modifies
  files. Targets <5s wall clock via parallel reads and detect-resources caching.
  Trigger when the user says "/startup", "start session", "orient me", "what's
  the state", "session briefing", "where did we leave off", "catch me up", "what
  was I working on".
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Session Startup (v5.0)

Open the store: read the operating manual, read `docs/status.md` (where things actually are), read `docs/planning/current.md` (where things should go), surface the resume context concisely, and get out of the way. Read-only; never modifies files.

**Doorman model:** quick, deliberate, no ceremony. Target under 5 seconds wall clock. If you need 30 seconds to brief, the project state is the problem, not this skill.

> **Status:** rad-session 5.0 — released. plugin.json is at 5.0.0; the marketplace ships this workflow.

## What changed from v4.0

| v4.0 | v5.0 |
|---|---|
| `CLAUDE.md` (always) | Operating manual (CLAUDE.md and/or AGENTS.md) per `.rad/profile` agent_scope |
| `HANDOFF.md` | `docs/status.md` — evidence-based, project-scoped (not session-scoped) |
| `.claude/session-log.md` | retired — `docs/planning/archive/` serves the journal role |
| v3.0 strategic-doc gap-check (PRD/ARCHITECTURE/ASSUMPTIONS/DECISIONS/PLAN) | v4.0 canonical gap-check (`docs/vision.md`, `docs/architecture.md`, `docs/planning/current.md`, `docs/status.md`, `docs/decisions/`) |

The session-log retirement is the biggest behavioral shift: rad-session no longer maintains a chronological session journal. Instead, completed milestones live in `docs/planning/archive/` (moved by /wrapup when a milestone ships), and `docs/status.md` always reflects current evidence-based reality.

## Mode flags

- `--auto-pull` — Skip the Phase 0 prompt; fast-forward silently when behind. For autonomous loops or when you've already decided to always sync.
- `--no-pull` — Skip the sync check entirely; read local files as-is. Briefing leads with a stale warning if origin has unpulled commits. For offline work.
- Neither → prompt at Phase 0 when behind (default).

## Cross-model note

Output briefing format is identical across Opus 4.7, Sonnet 4.6, and Haiku 4.5. This skill runs in the **session model** — whatever tier you're already in. Resource discovery is delegated to `scripts/detect-resources.py` with caching (Phase 2.5.0), so the model rarely does scanning work itself.

---

## Execution: parallel-first

Phase 0 (sync from origin) **must run first** because it can update the very files the rest of the skill reads. After Phase 0 resolves (pulled, declined, skipped, or aborted), Phases 1, 2, and 2.5 have no inter-phase dependencies — every read and shell command can be issued as a single parallel batch. Opus 4.7 and Sonnet 4.6 should do exactly that.

**Batch to issue at the start of the skill (after Phase 0 resolves):**

- Read `.rad/profile` (Phase 1.1 — determines which operating manual files to read)
- Read `CLAUDE.md` and/or `AGENTS.md` per agent_scope (Phase 1.2)
- Read `docs/status.md` or `docs/status-<branch>.md` per multi_branch_status (Phase 1.3)
- Read `docs/planning/current.md` (Phase 1.4)
- Read `docs/vision.md`, `docs/architecture.md` (Phase 1.5 file-existence checks)
- Glob `docs/decisions/*.md` (Phase 1.5)
- Glob root for legacy v3.0 strategic docs: `PRD.md`, `ARCHITECTURE.md`, `ASSUMPTIONS.md`, `DECISIONS.md`, `PLAN.md` (Phase 1.5 legacy detection)
- Read `.mcp.json`, `.claude/settings.json`, `.env.example`, `package.json`, `pyproject.toml` (Phase 2.5)
- Glob for stack marker files (Phase 2.5.2)
- Bash: combined `git status --short && git log --oneline -5 && git rev-parse --abbrev-ref HEAD && git rev-list --left-right --count HEAD...@{upstream}` (Phase 2.2)

Missing files error silently — skip them in the briefing. Do not re-attempt serial reads after a parallel batch.

---

## Phase 0: Sync from origin

A handoff is only useful if you're reading the latest state. Phase 0 confirms local matches origin **before** any operating manual / status.md / planning/current.md read fires.

### 0.1 Skip silently if any hold

- Project is not a git repo (`git rev-parse --git-dir` fails).
- Current branch has no upstream (`git rev-parse --abbrev-ref --symbolic-full-name @{u}` fails).
- An in-progress merge / rebase / cherry-pick (`.git/MERGE_HEAD` or `.git/REBASE_HEAD` exists).

### 0.2 Fetch and compare

```bash
git fetch --quiet 2>/dev/null
git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null
```

Output is `<ahead>\t<behind>`. Also check tree cleanliness with `git status --porcelain` — used to decide whether a fast-forward is even possible.

### 0.3 Act on the result

A fast-forward is possible when the tree is clean AND ahead = 0. Otherwise it's blocked (dirty tree or diverged).

| State | `--auto-pull` | `--no-pull` | Default (no flag) |
|---|---|---|---|
| Behind = 0 | continue silently | continue silently | continue silently |
| Behind > 0, FF possible | `git pull --ff-only` silently | stale-warn + read local | show incoming commits + prompt; on Y → pull, on N → stale-warn + read local |
| Behind > 0, FF blocked | block-warn + read local | block-warn + read local | block-warn + ask "Read local anyway? (Y/n)" — Y reads local, N aborts the briefing |

**Stale warning** (placed at the top of the Phase 3 briefing, above the Project line):
```
⚠ Reading stale local state — origin has N unpulled commits. Re-run /startup without --no-pull to sync.
```

**Block warning** (placed at the top of the Phase 3 briefing):
```
⚠ Couldn't sync — <dirty working tree | local diverged from origin>. Resolve with: <git stash | git pull --rebase>.
```

When prompting in the default behind-FF-possible case, list the incoming commits first via `git log HEAD..@{u} --oneline -10` so the user sees what's about to land. Default the prompt to Y.

### 0.4 Cross-machine handoff signal

Fires whenever the most recent commit to `docs/status.md` was made on another machine — independent of whether this turn pulled.

```bash
git log -1 --format='%s' -- docs/status.md 2>/dev/null
```

Parse for the canonical session-commit format `session: YYYY-MM-DD on <hostname> — <status>` written by `/wrapup`.

- Hostname differs from `$HOSTNAME` / `$COMPUTERNAME` / `hostname` → stash this Phase 3 note:
  ```
  Continuing from <other-host> — last status update committed there.
  ```
- Hostname matches → no note (continuing on the same machine).
- Commit doesn't match the canonical session format (manual commit) → skip silently.

The cross-machine note appears at the top of the Phase 3 briefing, above the Project line and below any stale/block warning.

---

## Phase 1: Read project state

All reads in Phase 1 are issued as one parallel batch with Phases 2 and 2.5 (after Phase 0 resolves). The phase numbering is for human readability; execution is concurrent.

### 1.1 Read `.rad/profile`

Determine:

- `agent_scope` (`claude_only` / `codex_only` / `claude_and_codex`) — drives Phase 1.2
- `mode` (`mentor` / `dev`) — recorded but not used by /startup (used by /wrapup)
- `multi_branch_status` (`true` / `false`) — if true, Phase 1.3 reads `docs/status-<current-branch>.md` instead of `docs/status.md`

If `.rad/profile` doesn't exist, default: `agent_scope = claude_only`, `mode = mentor`, `multi_branch_status = false`. Surface in briefing: "No .rad/profile detected — run /init to set up project profile."

### 1.2 Read operating manual

Per `agent_scope`:

- `claude_only` → read `CLAUDE.md`
- `codex_only` → read `AGENTS.md`
- `claude_and_codex` → read `AGENTS.md` (canonical) + `CLAUDE.md` (shim)

**Non-standard naming detection (Phase 2 M4 adaptation):** if the expected file is missing, Glob root for any `*.md` containing the heading `# Agent Operating Manual` or an `@AGENTS.md` import line. If found, treat that file as the operating manual — roll with what's there. Surface in briefing: "Operating manual: detected at non-standard path `<filename>`."

Extract:

- Project name and one-sentence purpose
- Read order (which docs to consult before what kind of work)
- Hard boundaries
- Engineering rules
- Definition of done
- Escalate triggers
- Commands (install / dev / test / lint / build)

Resolve `@-imports` one level deep (per v4.0 logic). Missing import targets are reported silently with a "⚠ missing import: <path>" line in the briefing.

### 1.3 Read `docs/status.md` (the canonical handoff)

If `multi_branch_status == true`, read `docs/status-<current-branch>.md` instead.

Extract the 8 sections (per [`docs/status-md-schema.md`](../../../../docs/status-md-schema.md)):

1. **Current state** (branch, milestone, overall status: on track | blocked | validating | needs decision)
2. **Last completed**
3. **Files changed recently**
4. **Latest validation results**
5. **Decisions made during execution**
6. **Known issues or blockers**
7. **Next recommended step**
8. **If restarting from scratch** — load-bearing read order for the briefing

**If status.md doesn't exist** or all 8 sections show "No data yet — populated by rad-session /wrapup from evidence", fall through to Minimal Briefing in Phase 3.

### 1.4 Read `docs/planning/current.md` (the active plan)

Extract:

- Objective
- Current milestone
- Acceptance criteria (including checkbox state — count `[x]` vs `[ ]` for progress)
- Stop conditions
- Notes for the next session

If `current.md` doesn't exist, surface in briefing: "No active plan — recommend `/rad-planner:plan` to create one."

### 1.5 Strategic Doc Gap-Check (v4.0)

Soft gap-check for the v4.0 canonical strategic docs. The reads already happened in the parallel batch at the top of the skill — Phase 1.5 just inspects which Reads returned content vs. which silently errored.

| File | If missing |
|---|---|
| `docs/vision.md` | Add to "missing strategic docs" list |
| `docs/architecture.md` | Add to list |
| `docs/planning/current.md` | (already checked in 1.4) |
| `docs/status.md` | (already checked in 1.3) |
| `docs/decisions/` (directory with at least `README.md`) | Add to list |

**Output behavior:**

- **All present** → emit nothing. Strategic docs are in place.
- **Some missing** → single briefing line:
  ```
  ⚠ Missing strategic docs: <comma-separated list> — run /rad-planner:plan to create. (Soft warning; session continues.)
  ```

**Legacy v3.0 detection:** Glob root for `PRD.md`, `ARCHITECTURE.md`, `ASSUMPTIONS.md`, `DECISIONS.md`, `PLAN.md`. If any present, surface separately:

```
⚠ v3.0 strategic docs detected at project root (PRD.md / etc.). v4.0 canonical structure is at docs/. Run /rad-planner:plan --pivot to migrate, or rad-session 5.0 will read what's there in mixed-layout mode.
```

**Why soft.** Many sessions are pure execution against an existing plan; some are exploratory; some projects are too small for the full set. The warning informs without blocking — session continues regardless.

### 1.6 Status freshness check

Quick mtime check (or use `status-validator.py --mode freshness` if rad-planner is installed alongside):

```bash
python3 ${plugin_root}/../rad-planner/scripts/status-validator.py --mode freshness docs/status.md --json 2>/dev/null
```

If `status-validator.py` isn't available (rad-planner not installed or path doesn't resolve), inline check:

```bash
# status.md mtime vs HEAD commit date
git log -1 --format='%ct' -- docs/status.md 2>/dev/null  # status's last commit timestamp
git log -1 --format='%ct' HEAD 2>/dev/null              # HEAD timestamp
git rev-list "$(git log -1 --format=%H -- docs/status.md)..HEAD" --count 2>/dev/null
```

Compute:
- **fresh:** `(head_date - status_date) < 2 days` AND `commits_since_status < 5`
- **stale:** `(head_date - status_date) > 7 days` OR `commits_since_status > 20`
- **moderate:** in between

If stale, include warning in briefing:

```
⚠ docs/status.md is N days old (M commits since last update) — refresh at next /wrapup recommended.
```

If status.md doesn't exist at all, skip the freshness check.

---

## Phase 2: Detect Project Type

### 2.1 Project Type Detection

Use Glob to check for coding-project indicators (any of these):

```
package.json
Cargo.toml
pyproject.toml
go.mod
Makefile
*.sln
.git/
```

**Non-coding project:** none detected. Note this — the briefing drops git info.

### 2.2 Live State (Coding Projects Only)

Run as a single combined command:

```bash
git status --short 2>/dev/null && echo "---" && \
git log --oneline -5 2>/dev/null && echo "---" && \
git rev-parse --abbrev-ref HEAD 2>/dev/null && echo "---" && \
git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null
```

Capture: current branch, uncommitted changes, recent commits, ahead/behind vs. remote.

### 2.3 Detect Changes Since Last Status Update

If `docs/status.md` has been committed and the freshness check (1.6) returned non-fresh, spot-check for commits between the status's last-commit-date and HEAD. Flag in briefing as "changes since status last updated" — useful when work happened outside a rad-session session (e.g., a quick hand-edit between /startup and /wrapup).

---

## Phase 2.5: Resource Discovery

Detect project-specific resources so Claude doesn't need to be reminded every session. All steps are read-only and issued in the parallel batch. Skip silently when nothing is found.

### 2.5.0 Preferred path: deterministic script (mtime-cached)

If Python is available, prefer the deterministic scanner over LLM-based marker scanning. Always pass `--cache` so cache-hit startups skip re-scanning entirely:

```bash
python3 ${plugin_root}/scripts/detect-resources.py "$PWD" --json --cache --include-env-names
```

The `--cache` flag writes results to `.claude/cache/resources.json`, keyed by mtimes of every input file. On cache hit, scanning is skipped — results return in milliseconds. The output adds a `"cache_status": "hit" | "miss"` field; surface under the briefing's resources block only if status is `miss` (e.g., `Resources: scanned fresh`); on `hit`, stay silent.

The script returns the same data structure as steps 2.5.1–2.5.6 below. Use JSON output verbatim. The LLM-based steps remain as fallback when Python is not available.

### 2.5.1 MCP Servers

Read `.mcp.json` at project root. Parse JSON and extract keys under `mcpServers`. Also read `.claude/settings.json` and collect names under `enabledMcpjsonServers` or plugin-scoped MCP entries. Merge without duplication. Malformed JSON → skip silently.

### 2.5.2 Stack CLIs (inferred from marker files)

Glob the project root for marker files. File-presence inference only — never exec any binary.

| Marker file(s) | Implied CLI |
|----------------|-------------|
| `supabase/config.toml` | `supabase` |
| `wrangler.toml`, `wrangler.jsonc` | `wrangler` |
| `netlify.toml` | `netlify` |
| `vercel.json` | `vercel` |
| `fly.toml` | `flyctl` |
| `firebase.json` | `firebase` |
| `.github/workflows/` (any *.yml) | `gh` |
| `Dockerfile`, `docker-compose.yml`, `compose.yaml` | `docker` |
| `coolify.json`, `.coolify/` | Coolify deploy target |
| `terraform/`, `*.tf` | `terraform` |
| `pulumi.yaml` | `pulumi` |
| `pyproject.toml` + `poetry.lock` | `poetry` |
| `Pipfile` | `pipenv` |
| `requirements.txt` (no poetry/pipenv) | `pip` |
| `Gemfile` | `bundle` |
| `deno.json`, `deno.jsonc` | `deno` |
| `bun.lockb`, `bunfig.toml` | `bun` |
| `Cargo.toml`, `rust-toolchain.toml` | `cargo` |
| `go.mod` | `go` |
| `mise.toml`, `.mise.toml` | `mise` |
| `.tool-versions` | `asdf` |
| `flake.nix`, `shell.nix` | `nix` |
| `devbox.json` | `devbox` |

Collect into a deduplicated list.

### 2.5.3 Package Manager & Scripts

If `package.json` exists:

- Read `packageManager` field. If absent, infer from lockfile.
- Extract top 5–8 keys from `scripts`. Prefer in order if present: `dev`, `build`, `test`, `typecheck`, `lint`, `start`, `check`, `format`.

Output example: `Scripts (pnpm): dev, build, test, typecheck, lint`

For Python: if `pyproject.toml` has a `[tool.poetry.scripts]` or `[project.scripts]` table, list up to 5 entries.

### 2.5.4 Environment Template

If `.env.example` exists, read it and extract variable names only (everything before `=` on each non-comment line). **Never read `.env`** or any file that may contain real values.

Output: `Env template: SUPABASE_URL, STRIPE_SECRET_KEY, ... (.env.example)`

### 2.5.5 Operating Manual Resources Section

If the operating manual (CLAUDE.md or AGENTS.md) contains a heading matching any of these (case-insensitive), extract its contents verbatim:

- `## Resources`
- `## MCP` / `## MCPs`
- `## Tools` / `## CLI Tools`

Treat as the **documented** source of truth for this project.

### 2.5.6 Reconciliation

Compare documented (2.5.5) against detected (2.5.1–2.5.4):

- **Documented + detected** → show normally in "Resources available."
- **Documented but not detected** → show with `⚠ documented but not found` — possible drift.
- **Detected but not documented** → show under `Also detected (not in operating manual):` — user may want to register via `/add-resource`.

If no Resources section exists in the operating manual, treat all detected items as primary with no drift warnings.

---

## Phase 3: Orient and Brief

Present a concise, scannable session briefing. Adapt the format based on what's available. Target **under 35 lines** and **under 5 seconds wall clock**.

### Briefing selection

| Condition | Template |
|---|---|
| status.md + planning/current.md both present + coding project | **Full Briefing** |
| status.md present, no planning/current.md | **Status-only Briefing** (recommend `/rad-planner:plan` to create the plan) |
| No status.md but operating manual exists | **Minimal Briefing** (no resume context to share; recommend `/wrapup` at end of next session to populate status) |
| No operating manual | **First-time Briefing** (recommend `/init`) |
| No build-system markers | **Non-Coding Briefing** |

### Full Briefing structure

```
[warnings — one line each, in order: block, stale, cross-machine, gap-check, freshness]

Project: {from operating manual Project line}
Branch: {current_branch} ({clean | <N> uncommitted})
Plan: {milestone X of Y from planning/current.md; AC progress N/M ({pct}%)}

Last completed:
- {top 3-5 from status.md Last completed}

Recently changed:
- {top 3-5 files from status.md Files changed recently}

Validation: {from status.md Latest validation results — one line, only if recent and not 'No data this session'}

Open issues:
- {top 3 from status.md Known issues or blockers, only if any}

Next: {from status.md Next recommended step — one paragraph; use exact wording}

Resources: {from Phase 2.5 — MCPs / CLIs / scripts; omit if all categories empty}

Ready to continue. What would you like to work on?
```

### Status-only Briefing structure

```
[warnings]

Project: {from operating manual}
Branch: {current_branch}
Plan: (none — recommend /rad-planner:plan to create one)

Last completed: {from status.md, only if any}
Next: {from status.md Next recommended step, only if any}

Resources: {from Phase 2.5}

Ready to continue. What would you like to work on?
```

### Minimal Briefing structure

```
[warnings, if any]

Project: {from operating manual}
Branch: {current_branch}

No status.md yet — first session, or /wrapup hasn't run yet on this project.
Run /wrapup at the end of this session to populate status.md from evidence.

Resources: {from Phase 2.5}

Ready to continue. What would you like to work on?
```

### First-time Briefing structure

```
No operating manual detected. This looks like a fresh project.

Recommend: /rad-session:init to set up the operating manual + status.md scaffold.
Then: /rad-planner:plan to create the plan and populate Constitution sections.

What would you like to work on?
```

### Non-Coding Briefing structure

```
[warnings]

Project: {from operating manual} (non-coding)

{status.md Next, if present, else "No status.md."}

Ready to continue.
```

### Presentation rules

- Keep the briefing **under 35 lines** — this is a quick orientation.
- Use the **exact wording from status.md** — don't paraphrase. The wrapup chose those words from evidence; paraphrasing loses load-bearing detail.
- End with `Ready to continue. What would you like to work on?` to hand control back.
- **Omit empty blocks** — don't show "Validation: (none)" or empty Resources headers.
- Cap each block at the line counts indicated; truncate with `...` if longer.
- If imports were resolved in Phase 1.2 and surfaced non-trivial content, add a single `Imports: <file1>, <file2>` line under Resources.
- If the "If restarting from scratch" section in status.md has a `Resume with:` line, prefer that verbatim as the Next-step content.

---

## What this skill does NOT do

- Does not modify any files (strict read-only)
- Does not write `docs/status.md` — that's `/wrapup`'s job at session end
- Does not update `docs/planning/current.md` — that's `/rad-planner:plan` or human edits
- Does not invoke `/rad-planner:plan` — recommends only when missing
- Does not derive resume context from chat history — only from evidence on disk (status.md, planning/current.md, git)
- Does not run anything beyond read-only Bash commands + `detect-resources.py`
- Does not read `.env` or any file that may contain secret values
- Does not maintain `.claude/session-log.md` (retired in v5.0)
- Does not maintain `HANDOFF.md` (retired in v5.0 — replaced by `docs/status.md`)

## Key references

**Canonical spec docs (top-level):**

- [`docs/doc-conventions.md`](../../../../docs/doc-conventions.md) — canonical file structure
- [`docs/cross-plugin-contracts.md`](../../../../docs/cross-plugin-contracts.md) — single-writer rule, sectioned-writer exception, .rad/profile protocol
- [`docs/status-md-schema.md`](../../../../docs/status-md-schema.md) — 8-section status schema with evidence sources

**Plugin internals:**

- `scripts/detect-resources.py` — MCP + CLI scanner with drift detection and mtime cache
- `references/briefing-examples.md` — concrete v5.0 briefing examples (5 templates: full / status-only / minimal / first-time / non-coding)
- `scripts/README.md` — full script documentation

## Mode flags (recap)

- `--auto-pull` — skip Phase 0 prompt, fast-forward silently when behind
- `--no-pull` — skip sync entirely; lead briefing with stale warning if behind
- Default → prompt at Phase 0 when behind
