---
name: wrapup
description: >
  End-of-session skill that captures session state to HANDOFF.md, appends to the
  session log, prunes CLAUDE.md of stale/ephemeral content, and optionally updates
  global memory. Use at the end of any work session for seamless handoffs.
  Trigger when the user says "/wrapup", "wrap up", "end of session",
  "session handoff", "save session state", "wrap this up",
  "let's wrap up", "close out this session".
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Session Wrapup

Capture the current session's state, decisions, traps, and insights into structured handoff files, then prune CLAUDE.md to keep it lean for the next session.

**Announce at start:** "Wrapping up this session — gathering state, writing handoff, updating session log, and pruning CLAUDE.md..."

---

## Phase 1: Gather State

Collect all raw material silently — no user interaction in this phase.

### 1.1 Read Existing Files

Read these files if they exist (skip silently if missing):

1. `CLAUDE.md` at project root
2. `HANDOFF.md` at project root (prior session's state — useful for comparison)
3. `.claude/session-log.md` — last 3-5 entries for continuity context

### 1.2 Detect Project Type

Use Glob to check for project markers:

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

**If coding project detected**, run these Bash commands:
```bash
git status --short 2>/dev/null
git diff --stat 2>/dev/null
git log --oneline -10 2>/dev/null
```

Capture: branch name, uncommitted changes, recent commits.

**If non-coding project** (none of the above found):
- Use Glob for recently modified files: `**/*` sorted by modification time
- Note the most recently touched files as "Modified Files"

### 1.3 Synthesize Conversation Context

From the current conversation already in your context (no tool call needed), extract:

- **Decisions made** — architectural choices, tool selections, approach decisions, with their reasoning
- **Failed approaches** — things that were tried and didn't work, and specifically why they failed
- **User corrections** — feedback or preferences the user expressed that adjusted your approach
- **Open/incomplete work** — tasks started but not finished, next steps identified
- **Non-obvious insights** — discoveries about the codebase, API quirks, environment issues, anything a fresh session would need to know but couldn't easily rediscover

---

## Phase 2: Write HANDOFF.md

Overwrite `HANDOFF.md` at the project root. Follow the template in `references/handoff-template.md`.

### Content Rules

- **Every section is optional.** If nothing failed, omit "What NOT To Do" entirely — do not fill it with "N/A" or placeholders.
- **Be specific.** "Modified `src/auth.ts` lines 45-80 — added JWT validation" is useful. "Made changes to auth" is not.
- **Describe state, not instructions.** "Open Work" says "EBirdProvider started, API auth not wired" — not "Next, wire up the eBird API auth."
- **Keep it scannable.** Bullet points over paragraphs. One idea per bullet.
- **Target length:** 30-80 lines depending on session complexity.

### File Structure

```markdown
# Session Handoff

**Date:** [today's date]
**Status:** [One-line project state — e.g., "Phase 2 implementation in progress, auth complete, data layer next"]

## Last Session Summary
[2-4 sentences — what was accomplished. Focus on outcomes, not play-by-play.]

## Where I Left Off
- [Specific file, feature, or task that is mid-flight]
- [Include file paths and line numbers when relevant]

## Key Decisions
- [Decision]: [Brief reasoning — WHY, not just WHAT]

## What NOT To Do
- [Failed approach]: [Why it failed — prevents the next session from retrying]

## Open Work
- [Item]: [Current state as a description, not an instruction]

## Modified Files
- `path/to/file` — [what changed, briefly]

## Key Insights
[Non-obvious things: API quirks, environment gotchas, architectural constraints not in CLAUDE.md, 
user preferences discovered during this session]
```

---

## Phase 3: Append Session Log

Update `.claude/session-log.md` with a compact entry for this session. Follow `references/session-log-format.md`.

### Mechanism

1. Read `.claude/session-log.md` if it exists (may be empty or missing)
2. Create the new entry (see format below)
3. Prepend the new entry to the existing content (newest first)
4. Write the full file back

If `.claude/` directory doesn't exist, create it first.

### Entry Format

```markdown
## YYYY-MM-DD — [Brief title of what was done]
**Status:** [one-line project state]
**Changes:** [file list or high-level summary]
**Decisions:** [key choices made, if any]
**Traps:** [what to avoid — only include if something actually failed or a gotcha was discovered]
---
```

**Target:** 15-25 lines per entry. Be concise — this is a log, not a narrative.

### Log Maintenance

If the log now exceeds 20 entries after prepending:

1. Scan entries being trimmed for "Traps" that appear 3+ times across the full log
2. If recurring traps found, promote them to CLAUDE.md as permanent rules (add under an appropriate existing section, or create a "Known Gotchas" section if none fits)
3. Remove entries beyond the 20-entry cap (trim from the bottom — oldest entries)
4. Notify the user:
   ```
   Session log maintenance: Trimmed [N] oldest entries.
   [If traps promoted]: Promoted recurring trap to CLAUDE.md: "[description]"
   ```

---

## Phase 4: Prune CLAUDE.md

Read CLAUDE.md and evaluate it for staleness, duplication, and ephemeral state.

### If No CLAUDE.md Exists

Create a minimal scaffold:

```markdown
# [Project Name — from directory name, package.json, or ask]

## Tech Stack
[Auto-detected if coding project, otherwise "TBD"]

## Conventions
[To be established]
```

Then skip the rest of Phase 4 — there's nothing to prune.

### Pruning Heuristics

For each identifiable section or statement in CLAUDE.md, evaluate:

| Question | If YES |
|----------|--------|
| Is this about current work in progress? (e.g., "Currently refactoring auth") | Move to HANDOFF.md, remove from CLAUDE.md |
| Is this a task or TODO? (e.g., "Need to add error handling to API routes") | Move to HANDOFF.md "Open Work" section |
| Was this a temporary constraint that's been resolved? (e.g., "Don't touch billing — migration pending" when migration is done) | Remove |
| Is this duplicating what HANDOFF.md now captures? | Remove |
| Does this reference files, functions, or patterns that no longer exist? | Remove |
| Would removing this cause Claude to make mistakes? | Keep |
| Is this a permanent convention, rule, or architectural decision? | Keep |
| Is this inside a protected Resources section (`## Resources`, `## MCP`, `## Tools`, `## CLI Tools`)? | Keep — see "Protected Sections" below |

**Primary heuristic:** Ephemeral state migrates out of CLAUDE.md into HANDOFF.md. CLAUDE.md is for permanent rules and registered resources.

### Respecting Structure

- Do NOT reorganize, reformat, or restructure the existing CLAUDE.md
- Do NOT change heading levels or naming conventions the user chose
- Do NOT add sections, comments, or formatting the user didn't ask for
- Only prune within the existing structure
- Exception: if CLAUDE.md was just created by this skill in this run, the scaffold format is used

### Protected Sections

The following sections are **protected** from removal. Never delete the section itself. Individual entries inside them may only be removed if they reference a file path, binary, or URL that clearly no longer exists — and even then, show the specific item in the diff and wait for explicit approval before removing.

- `## Resources` (canonical)
- `## MCP` / `## MCPs`
- `## Tools` / `## CLI Tools`

**Why:** these sections are the user's registered resources for the project — MCPs, CLIs, scripts, environment tools — and the `/startup` skill (Phase 2.5) reads them as the authoritative source when orienting a new session. Pruning them would force the user to re-explain available resources every session, defeating the purpose of the handoff system. Entries are typically added via the `/add-resource` skill or manually by the user.

If a Resources-section entry appears stale, **flag it in the diff but keep it** unless the user explicitly says "remove it." When in doubt, keep.

### Show the Diff

After editing, present a summary of changes:

```
CLAUDE.md changes:
  - Removed: "[quoted text or description]" ([reason])
  - Removed: "[quoted text or description]" ([reason])
  - Updated: [section] — [what changed]
  - Kept: [N] lines unchanged
```

Wait for the user to respond. Acceptable responses:
- "looks good" / "fine" / "ok" / approval → proceed to Phase 5
- "undo [specific item]" → revert that change, show updated diff
- If no changes were needed, say: "CLAUDE.md looks clean — no changes needed." and proceed

---

## Phase 5: Memory Prompt

Review the session for insights worth preserving in global memory (the `~/.claude/projects/` memory system).

### What Qualifies as a Memory Candidate

| Type | Example |
|------|---------|
| **reference** | "This project's API docs are at [URL]", "Bugs tracked in Linear project INGEST" |
| **feedback** | User correction that applies beyond this project: "Prefer single PRs for refactors" |
| **project** | Non-obvious project fact: "Auth rewrite driven by compliance, not tech debt" |
| **user** | New info about the user's role/expertise: "First time working with GraphQL" |

### What Does NOT Qualify

- Anything already captured in HANDOFF.md or session-log.md
- Code patterns, file paths, or architecture (derivable from the codebase)
- Session-specific debugging details
- Anything already in existing memory files

### Presentation

If candidates exist, present them:

```
Global memory candidates:
  1. [Description] ([type])
  2. [Description] ([type])

Save any of these to global memory? (1, 2, both, none)
```

If the user confirms:
1. Discover the active memory directory for the current project working directory
2. Write or update the relevant memory file using the standard frontmatter format:
   ```markdown
   ---
   name: [Human-readable name]
   description: [One-line — used for relevance matching in future sessions]
   type: [user | feedback | project | reference]
   ---

   [Content — for feedback/project types: rule/fact, then **Why:** and **How to apply:** lines]
   ```
3. Update the `MEMORY.md` index with a one-line pointer

If no candidates or user declines, skip silently.

### Session Complete

End with a brief confirmation:

```
Session wrapped up:
  - HANDOFF.md written ([N] lines)
  - Session log updated ([N] total entries)
  - CLAUDE.md [pruned: N changes | unchanged | created]
  [- Global memory updated (if applicable)]
```
