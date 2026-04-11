---
name: startup
description: >
  Start-of-session skill that reads HANDOFF.md, session log, and CLAUDE.md to
  orient a new session with full context from prior work. Read-only — never
  modifies files. Trigger when the user says "/startup", "start session",
  "orient me", "what's the state", "session briefing", "where did we leave off",
  "catch me up", "what was I working on".
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Session Startup

Orient a new session by reading the handoff state left by `/wrapup`, detecting the project type, and presenting a concise briefing.

**This skill is read-only. It never creates, modifies, or deletes files.**

---

## Phase 1: Discover Project State

Read handoff files in order. All are optional — skip silently if missing.

### 1.1 Read CLAUDE.md

Read `CLAUDE.md` at the project root. Note:
- Project name and type
- Tech stack
- Key conventions and rules
- Any referenced external files (e.g., `@path/to/import` patterns)

### 1.2 Read HANDOFF.md

Read `HANDOFF.md` at the project root. This is the primary handoff from the last session. Extract:
- Status line
- Where work was left off
- Key decisions from last session
- "What NOT To Do" traps
- Open work items
- Modified files
- Key insights

### 1.3 Read Session Log

Read `.claude/session-log.md` if it exists. Focus on the most recent 3-5 entries for:
- Patterns across sessions (recurring traps, ongoing work threads)
- Context that the latest HANDOFF.md alone might not capture
- How long the current work has been in progress

### 1.4 Assess Handoff Freshness

Check the date in HANDOFF.md against today's date:
- **Same day or yesterday:** Handoff is fresh — trust it fully
- **2-7 days old:** Handoff is recent — trust it but note the gap
- **7+ days old:** Handoff is stale — warn that project state may have changed outside of Claude Code sessions. Suggest running `/wrapup` first if significant manual work happened in the gap.
- **No HANDOFF.md:** Note this is either a brand-new project or one that hasn't used `/wrapup` yet

---

## Phase 2: Detect Project Type

Quick scan to classify the project and gather live state.

### 2.1 Project Type Detection

Use Glob to check for:

**Coding project indicators** (any of these):
```
package.json
Cargo.toml
pyproject.toml
go.mod
Makefile
*.sln
.git/
```

**Non-coding project:** No build system detected. Note this — it changes the briefing format (no git info).

### 2.2 Live State (Coding Projects Only)

Run these Bash commands:

```bash
git status --short 2>/dev/null
git log --oneline -5 2>/dev/null
git rev-parse --abbrev-ref HEAD 2>/dev/null
git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null
```

Capture:
- Current branch name
- Uncommitted changes (if any)
- Recent commits since last session
- Ahead/behind status relative to remote

### 2.3 Detect Changes Since Last Session

If HANDOFF.md exists and has a date, check if any commits were made between that date and now that were NOT part of the last Claude Code session (e.g., manual commits, other contributors):

```bash
git log --oneline --since="[handoff date]" 2>/dev/null
```

If new commits are found that aren't referenced in HANDOFF.md, flag them as "changes made outside the last session."

---

## Phase 2.5: Resource Discovery

Detect what project-specific resources are available so Claude doesn't have to be reminded every session. All steps are read-only and optional — skip silently when nothing is found.

### 2.5.1 MCP Servers

Read `.mcp.json` at the project root if it exists:

```bash
# Glob only — do not exec the servers
```

Parse the JSON and extract the keys under `mcpServers`. Example:

```json
{ "mcpServers": { "supabase": {...}, "coolify": {...} } }
```

→ `MCPs: supabase, coolify`

If `.claude/settings.json` exists, also read it and collect any names under `enabledMcpjsonServers` or plugin-scoped MCP entries. Merge without duplication.

If the JSON is malformed, skip silently — do not crash the briefing.

### 2.5.2 Stack CLIs (inferred from marker files)

Use Glob to check the project root for the following markers. Each implies a CLI the user likely uses on this project. **Do not exec any binary** — this is purely file-presence inference.

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

Collect into a deduplicated list.

### 2.5.3 Package Manager & Scripts

If `package.json` exists:

- Read `packageManager` field (e.g., `pnpm@9.0.0`) to know which PM to use. If absent, infer from lockfile: `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lockb` → bun, else npm.
- Extract the top 5–8 keys from the `scripts` object. Prefer common ones in this order if present: `dev`, `build`, `test`, `typecheck`, `lint`, `start`, `check`, `format`.

Output example: `Scripts (pnpm): dev, build, test, typecheck, lint`

Skip if no `package.json`. For non-Node projects, note the equivalent if obvious (e.g., `Makefile` → `make <target>` list from top-level `make help` targets if documented; otherwise omit).

### 2.5.4 Environment Template

If `.env.example` exists, read it and extract the **variable names only** (everything before `=` on each non-comment line). Never read `.env` or any file containing real values.

Output: `Env template: SUPABASE_URL, STRIPE_SECRET_KEY, ... (.env.example)`

### 2.5.5 CLAUDE.md Resources Section

If CLAUDE.md contains a heading matching any of these (case-insensitive), extract its contents verbatim:

- `## Resources`
- `## MCP` / `## MCPs`
- `## Tools` / `## CLI Tools`

Treat the extracted contents as the **documented** source of truth for this project.

### 2.5.6 Reconciliation

Compare documented (2.5.5) against detected (2.5.1–2.5.4):

- **Documented + detected** → show normally in the "Resources available" block.
- **Documented but not detected** → show with `⚠ documented but not found` — possible drift (config moved, tool uninstalled).
- **Detected but not documented** → show under a secondary line `Also detected (not in CLAUDE.md):` — signals the user may want to run `/add-resource` to register them.

If no CLAUDE.md Resources section exists, treat all detected items as primary with no drift warnings.

---

## Phase 3: Orient and Brief

Present a concise, scannable session briefing. Adapt the format based on what information is available.

### Full Briefing (HANDOFF.md exists + coding project)

```
Project: [name]
Type: [Coding (stack) | Non-coding]
Branch: [name] ([N ahead, M behind] or [up to date])
Last session: [date] — [status line from HANDOFF.md]

Where we left off:
  - [item from HANDOFF.md]
  - [item from HANDOFF.md]

Watch out for:
  - [trap from HANDOFF.md "What NOT To Do"]
  - [recurring trap from session log, if any]

Open work:
  - [item from HANDOFF.md]

[If any resources detected or documented:]
Resources available:
  MCPs: [list from .mcp.json + settings]
  Stack CLIs: [list inferred from marker files]
  Scripts ([pm]): [top scripts from package.json]
  Env template: [names from .env.example]
  [⚠ documented but not found: <items>]
  [Also detected (not in CLAUDE.md): <items>  →  run /add-resource to register]

[If uncommitted changes exist:]
Uncommitted changes from last session:
  - [file list from git status]

[If commits made outside last session:]
Changes since last session (not from Claude Code):
  - [commit list]

Ready to continue. What would you like to work on?
```

### Minimal Briefing (No HANDOFF.md)

```
Project: [name from directory or CLAUDE.md]
Type: [Coding (stack) | Non-coding]
[Branch: [name] — if git project]

No session handoff found — this is either a new project or one that hasn't used /wrapup yet.

[If CLAUDE.md exists:]
From CLAUDE.md: [brief summary of project rules/conventions]

[If any resources detected:]
Resources available:
  MCPs: [list]
  Stack CLIs: [list]
  Scripts ([pm]): [list]

[If git history exists:]
Recent activity:
  - [last 5 commits]

What would you like to work on?
```

### Non-Coding Briefing

```
Project: [name]
Type: Non-coding
Last session: [date] — [status from HANDOFF.md]

Where we left off:
  - [items]

Watch out for:
  - [traps]

[If any resources documented/detected:]
Resources available:
  MCPs: [list]
  Tools: [list]

Recently modified files:
  - [file list]

Ready to continue. What would you like to work on?
```

### Presentation Rules

- Keep the briefing under 35 lines — this is a quick orientation, not a report
- Use the exact wording from HANDOFF.md for traps and open work — don't paraphrase (the original wording was chosen carefully)
- End with "Ready to continue. What would you like to work on?" to hand control back to the user
- If the handoff is stale (7+ days), lead with the staleness warning before the briefing
- Omit the "Resources available" block entirely if every category (MCPs, CLIs, scripts, env) is empty — don't show an empty header
- Cap the Resources block at 6 lines; truncate with `...` if a category has more than 8 items
