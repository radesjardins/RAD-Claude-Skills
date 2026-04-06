# rad-session Plugin Design Spec

**Date:** 2026-04-05
**Status:** Draft
**Plugin:** rad-session
**Location:** `plugins/rad-session/` in rad-skills-repo

## Overview

A lightweight Claude Code plugin providing two complementary skills — `/wrapup` and `/startup` — that manage seamless session handoffs across any project type. The plugin maintains a consistent trio of files (CLAUDE.md, HANDOFF.md, `.claude/session-log.md`) that together give each new session full context without bloating CLAUDE.md.

### Problem

Claude Code sessions are stateless. Each new session loads CLAUDE.md and whatever the user provides. Without intentional handoffs, sessions lose: what was tried and failed, where work was left mid-flight, what decisions were made and why, and what the next session needs to know. The common workaround — dumping everything into CLAUDE.md — makes it bloated, which degrades Claude's instruction-following.

### Solution

Split session context into three tiers:

| Tier | File | Lifecycle | Purpose |
|------|------|-----------|---------|
| Permanent rules | `CLAUDE.md` | Long-lived, pruned regularly | Architecture, conventions, tech stack, build commands |
| Current state | `HANDOFF.md` | Overwritten each session | Where we left off, decisions, traps, modified files |
| History | `.claude/session-log.md` | Append-only, capped at 20 entries | Institutional memory — patterns, recurring traps |

## Plugin Structure

```
rad-session/
├── .claude-plugin/plugin.json
├── skills/
│   ├── wrapup/SKILL.md
│   └── startup/SKILL.md
├── references/
│   ├── handoff-template.md
│   ├── session-log-format.md
│   └── file-conventions.md
└── README.md
```

## Skill: `/wrapup`

### Trigger

User-invoked via `/wrapup` or phrases like "wrap up this session", "end of session", "session handoff", "save session state".

### Allowed Tools

Read, Write, Edit, Glob, Grep, Bash

### Phases

#### Phase 1: Gather State

No user interaction. Collects raw material:

- Read `CLAUDE.md` (if exists)
- Read `HANDOFF.md` (if exists — prior state for comparison)
- Read last 3-5 entries from `.claude/session-log.md` (if exists)
- **Coding projects:** Run `git status`, `git diff --stat`, `git log --oneline -10`
- **Non-coding projects:** Scan for recently modified files via filesystem timestamps
- Synthesize from the current conversation context (already in memory — no tool call needed):
  - Decisions made (with reasoning)
  - Problems encountered and failed approaches
  - Corrections/feedback from the user
  - Open/incomplete work
  - Non-obvious insights or discoveries

#### Phase 2: Write HANDOFF.md

Overwrite `HANDOFF.md` at project root with structured content following `references/handoff-template.md`. Sections:

| Section | Content |
|---------|---------|
| **Status** | One line — current project state |
| **Last Session Summary** | 2-4 sentences — what was accomplished |
| **Where I Left Off** | Specific files, features, or tasks in progress |
| **Key Decisions** | Choices made this session with brief reasoning |
| **What NOT To Do** | Failed approaches, dead ends — and why they failed |
| **Open Work** | Remaining items described as state, not instructions |
| **Modified Files** | Paths (with line ranges if relevant) |
| **Key Insights** | Non-obvious things the next session must know |

Every section is optional. If nothing failed, "What NOT To Do" is omitted (not filled with "N/A"). The skill adapts to what actually happened.

#### Phase 3: Append Session Log

Add a compact entry (15-25 lines) to `.claude/session-log.md`. Newest entries at top (reverse chronological) — read the existing file, prepend the new entry, and write the full file back. Format per `references/session-log-format.md`:

```markdown
## YYYY-MM-DD — [Title]
**Status:** [one-line]
**Changes:** [files or summary]
**Decisions:** [key choices, if any]
**Traps:** [what to avoid, if any]
---
```

If the log exceeds 20 entries:
- Scan oldest entries for recurring "Traps" (appeared 3+ times)
- Promote recurring traps to CLAUDE.md
- Trim oldest entries beyond 20
- Notify user: "Trimmed N oldest entries. Promoted recurring trap: [description]"

#### Phase 4: Prune CLAUDE.md

Read CLAUDE.md and evaluate each section against:

1. **Still accurate?** Does it match current project state?
2. **Duplicated?** Is this now captured in HANDOFF.md or session-log.md?
3. **Removal-safe?** Would removing this cause Claude to make mistakes next session?
4. **Ephemeral?** Is this session-specific state masquerading as a permanent rule?

Primary pruning heuristic: **ephemeral state migrates out of CLAUDE.md into HANDOFF.md.**

Edit CLAUDE.md directly, then show a summary diff:

```
CLAUDE.md changes:
  - Removed: "Currently working on auth middleware refactor" (captured in HANDOFF.md)
  - Removed: "Don't use lodash.merge" (merged 3 sessions ago, no longer relevant)
  - Updated: Tech stack section — added Zod v3.23
  - Kept: 24 lines unchanged
```

User can say "undo X" or "looks good" to proceed.

Rules:
- Does NOT restructure or reorganize existing CLAUDE.md headings
- Does NOT impose a format the user didn't choose
- Exception: if CLAUDE.md was just created by `/wrapup` on first run, uses the scaffold format

#### Phase 5: Memory Prompt

If the session surfaced anything worth remembering globally (new reference, user preference, feedback, cross-project learning), present candidates:

```
Global memory candidates:
  1. This project uses Coolify for deployment (reference)
  2. You prefer single bundled PRs for refactors (feedback)

Save any of these to global memory? (1, 2, both, none)
```

If confirmed, discover the active memory directory for the current project (typically `~/.claude/projects/<project-hash>/memory/`), write/update the relevant memory file, and update the `MEMORY.md` index. If declined, skip silently.

## Skill: `/startup`

### Trigger

User-invoked via `/startup` or phrases like "start session", "orient me", "what's the state", "session briefing".

### Allowed Tools

Read, Glob, Grep, Bash

### Phases

#### Phase 1: Discover Project State

Read handoff files in order (all optional):

1. `CLAUDE.md` — project rules and conventions
2. `HANDOFF.md` — where the last session left off
3. `.claude/session-log.md` — last 3-5 entries for broader context

If none exist, note this is a fresh project with no prior session history.

#### Phase 2: Detect Project Type

Quick scan:

- **Coding project:** Has `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `.git/`, Makefile, etc.
- **Non-coding project:** Documents, planning, content — no build system detected

For coding projects, also capture:
- `git status` — uncommitted work carried over
- `git log --oneline -5` — recent commits since last session
- Branch name and ahead/behind status

#### Phase 3: Orient and Brief

Present a concise session briefing:

```
Project: [name]
Type: [Coding (stack) | Non-coding]
Branch: [name] ([ahead/behind status])
Last session: [date] — [summary]

Where we left off:
  - [item 1]
  - [item 2]

Watch out for:
  - [trap 1]
  - [trap 2]

Uncommitted changes:
  - [file list, if any]

Ready to continue. What would you like to work on?
```

### Design Principle

`/startup` never modifies files. Read-only. It trusts `/wrapup` left things in good shape and surfaces them. If HANDOFF.md doesn't exist, it orients from what it can find (CLAUDE.md, git state, file structure).

## Reference Files

### `references/handoff-template.md`

Canonical HANDOFF.md structure. The `/wrapup` skill follows this template, adapting content but keeping sections consistent. See Phase 2 above for the full template.

### `references/session-log-format.md`

Defines the compact entry format. Rules:
- Newest entries at top (reverse chronological)
- Target 15-25 lines per entry
- No full file contents — paths only
- `---` separator between entries for parseability

### `references/file-conventions.md`

Shared rules both skills follow:

| Convention | Rule |
|------------|------|
| HANDOFF.md location | Always project root |
| session-log.md location | Always `.claude/session-log.md` |
| CLAUDE.md max target | ~150 lines — prune aggressively |
| Session log max entries | 20 — older entries trimmed on `/wrapup` |
| CLAUDE.md content | Permanent rules, conventions, tech stack, build commands |
| HANDOFF.md content | Session state, current work, decisions, traps, modified files |
| Session log content | Historical record — compact per-session entries |
| First-run behavior | Create CLAUDE.md scaffold, `.claude/` dir, HANDOFF.md, session-log.md as needed |

## Edge Cases

### First-run on a new project
- Creates `.claude/` directory if missing
- Creates `HANDOFF.md` from template
- Creates `.claude/session-log.md` with first entry
- If no `CLAUDE.md`, creates minimal scaffold (project name, tech stack TBD, conventions TBD)
- Does NOT over-generate CLAUDE.md

### Non-coding projects
- Skips all git commands — no errors
- Uses filesystem scan (recently modified files) instead of git diff
- All other phases work identically

### Nothing meaningful happened
- Produces lighter handoff: "Status: No changes — exploratory session"
- Session log still gets an entry
- CLAUDE.md pruning still runs

### CLAUDE.md has no clear structure
- Prunes within existing structure — does not reorganize
- Never imposes a format the user didn't choose

### Conflicting CLAUDE.md and HANDOFF.md
- HANDOFF.md wins for "what's happening now"
- CLAUDE.md wins for "how we do things here"
- Session-specific state in CLAUDE.md migrates to HANDOFF.md

### Multiple sessions in one day
- HANDOFF.md overwrites — always latest
- Session log appends second entry with same date — each stands alone

## Plugin Metadata

```json
{
  "name": "rad-session",
  "version": "1.0.0",
  "description": "Session handoff management — /wrapup captures state, prunes CLAUDE.md, logs history; /startup orients new sessions from handoff files.",
  "author": { "name": "RAD", "url": "https://github.com/radesjardins" },
  "license": "Apache-2.0",
  "keywords": ["session", "handoff", "wrapup", "startup", "CLAUDE.md", "context"]
}
```

## What This Plugin Does NOT Do

- Does not commit code or take destructive actions
- Does not restructure or reorganize CLAUDE.md formatting
- Does not push to remote repositories
- Does not run tests or linters (it reports their state if available)
- Does not replace `--continue`/`--resume` for same-task continuation
- Does not manage git branches or merges
