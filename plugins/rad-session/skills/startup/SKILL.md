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

Recently modified files:
  - [file list]

Ready to continue. What would you like to work on?
```

### Presentation Rules

- Keep the briefing under 30 lines — this is a quick orientation, not a report
- Use the exact wording from HANDOFF.md for traps and open work — don't paraphrase (the original wording was chosen carefully)
- End with "Ready to continue. What would you like to work on?" to hand control back to the user
- If the handoff is stale (7+ days), lead with the staleness warning before the briefing
