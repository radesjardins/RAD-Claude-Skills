---
name: wrapup
description: >
  End-of-session skill that captures session state to HANDOFF.md, appends to the
  session log, and prunes CLAUDE.md of stale/ephemeral content (the ## Resources
  section is protected from removal). Surfaces insights for Claude Code's native
  Auto Memory but does not write to the memory path itself. Use at the end of any
  work session for seamless handoffs. Trigger when the user says "/wrapup",
  "wrap up", "end of session", "session handoff", "save session state",
  "wrap this up", "let's wrap up", "close out this session".
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Session Wrapup

Capture the current session's state, decisions, traps, and insights into structured handoff files, then prune CLAUDE.md to keep it lean. The `## Resources` section is protected from deletion. Insights worth remembering are surfaced in the final summary for Claude Code's native Auto Memory to pick up on its own schedule.

**Cross-model note.** Works identically across Opus 4.7, Sonnet 4.6, and Haiku 4.5. Opus/Sonnet should issue Phase 1 reads + git state commands as a single parallel batch; Haiku may execute sequentially. The conversation-synthesis step in Phase 1.3 uses the explicit tag-and-summarize pattern so all three models produce comparable output.

**Announce at start:** "Wrapping up this session — gathering state, writing handoff, updating session log, pruning CLAUDE.md (Resources protected), and surfacing any insights..."

---

## Phase 1: Gather State

Collect all raw material silently — no user interaction in this phase. Phase 1.1 and 1.2 have no dependencies and can run in parallel.

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

**If coding project detected**, run as one combined command:
```bash
git status --short 2>/dev/null && echo "---" && \
git diff --stat 2>/dev/null && echo "---" && \
git log --oneline -10 2>/dev/null
```

Capture: branch name, uncommitted changes, recent commits.

**If non-coding project:**
- Use Glob for recently modified files: `**/*` sorted by modification time
- Note the most recently touched files as "Modified Files"

### 1.3 Synthesize Conversation Context

Walk the conversation already in your context — no tool call needed. To produce reliable, comparable output across models, use this explicit scan pattern instead of freeform reflection:

**Scan pass.** Starting from the earliest turn still visible and moving forward, tag each meaningful turn with one or more of these labels:

| Label | What qualifies |
|-------|----------------|
| `DECISION` | Architecture choice, tool selection, naming rule, approach taken — with a stated or inferable reason |
| `FAIL` | Something was tried and didn't work, **and** a root cause was identified |
| `CORRECTION` | User explicitly redirected, rejected an approach, or stated a preference |
| `INSIGHT` | Non-obvious fact about the codebase, environment, API, or user that a fresh session couldn't easily rediscover |
| `OPEN` | Task started but not finished, or a next step that was identified but not executed |

Skip turns that are pure tool output, navigation, or conversational filler. Do not re-tag the same content twice.

**Synthesis pass.** After tagging, collapse the labels into the HANDOFF.md sections:

- `DECISION` → Key Decisions (with the WHY preserved)
- `FAIL` → What NOT To Do (use TRIED / FAILED BECAUSE / CORRECT APPROACH format — see below)
- `CORRECTION` → Key Decisions (if it locks in a rule) or Key Insights (if it reveals a preference)
- `INSIGHT` → Key Insights
- `OPEN` → Open Work (stated as current state, not instructions)

If the conversation was truncated by compaction, note this explicitly in the Last Session Summary: "Context was compacted during this session — synthesis based on remaining visible turns only."

---

## Phase 2: Write HANDOFF.md

Overwrite `HANDOFF.md` at the project root. Follow the template in `references/handoff-template.md`.

### Content Rules

- **Every section is optional.** If nothing failed, omit "What NOT To Do" entirely — do not fill it with "N/A" or placeholders.
- **Be specific.** "Modified `src/auth.ts` lines 45-80 — added JWT validation" is useful. "Made changes to auth" is not.
- **Describe state, not instructions.** "Open Work" says "EBirdProvider started, API auth not wired" — not "Next, wire up the eBird API auth."
- **Keep it scannable.** Bullet points over paragraphs. One idea per bullet.
- **Target length:** 30-80 lines depending on session complexity.

### "What NOT To Do" — canonical trap format

Every entry under this section uses a structured three-part form. Small models (Haiku) and downstream parsers depend on it being literal. Opus/Sonnet can collapse to a single line when the third field is unknown; the two required prefixes remain.

**Full form (preferred):**
```
- TRIED: [specific approach that was attempted]
  FAILED BECAUSE: [root cause — not just "it didn't work"]
  CORRECT APPROACH: [what actually worked, or what should be tried instead — omit the line if unknown]
```

**Compact form (acceptable when the correct approach is unknown):**
```
- TRIED: [approach] — FAILED BECAUSE: [root cause]
```

Do not write unstructured trap prose. The prefix tokens are how `/startup` reliably extracts the trap into the next session's briefing.

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
- TRIED: [failed approach]
  FAILED BECAUSE: [root cause]
  CORRECT APPROACH: [what works, if known]

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
**Traps:** [compact trap form — "TRIED: X — FAILED BECAUSE: Y" — only include if something actually failed]
---
```

**Target:** 15-25 lines per entry. Be concise — this is a log, not a narrative.

### Log Maintenance

If the log now exceeds 20 entries after prepending:

1. Scan entries being trimmed for "Traps" that appear 3+ times across the full log (match on the FAILED BECAUSE clause, not the TRIED clause — same root cause with different surface attempts should still count)
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

### Auto-proceed threshold (autonomous-friendly)

The confirmation gate was added for safety on large or surprising prunes. For small, low-risk edits, blocking on a confirmation prompt breaks autonomous loops and background sessions. Evaluate this gate against the diff:

**Auto-proceed is allowed only if ALL of these are true:**

1. Total removals ≤ 3 lines/bullets (not including whitespace)
2. No removed line resides in `## Tech Stack`, `## Conventions`, `## Architecture`, or any heading that matches the regex `(?i)^##\s+(rules?|principles?|guardrails?|do\s*not)` — these encode permanent rules
3. No removed line comes from a protected Resources section
4. No removed line contains the word "must", "never", "always", "required", or "forbidden" (signals a permanent rule the user wrote)
5. The session is not the first run on this project (i.e., CLAUDE.md existed before this wrapup)

If all five hold: proceed without waiting, and the diff block above becomes the record of what happened. Continue to Phase 5.

Otherwise: wait for the user to respond. Acceptable responses:
- "looks good" / "fine" / "ok" / approval → proceed to Phase 5
- "undo [specific item]" → revert that change, show updated diff
- If no changes were needed, say: "CLAUDE.md looks clean — no changes needed." and proceed

---

## Phase 5: Surface Insights for Native Auto Memory

**What changed in 2.1:** rad-session no longer writes to `~/.claude/projects/<project>/memory/` — that path is owned by Claude Code's **native Auto Memory** (shipped in v2.1.59). Writing there would collide with the native system and confuse `/memory` and `MEMORY.md` consolidation.

Instead, Phase 5 **surfaces insights** by mentioning them in the final session summary. Claude Code's native Auto Memory will see them in the conversation context and save them on its own schedule — no duplicate write path, no collision.

### What Qualifies as an Insight to Surface

| Type | Example |
|------|---------|
| **reference** | "This project's API docs are at [URL]", "Bugs tracked in Linear project INGEST" |
| **feedback** | User correction that applies beyond this project: "Prefer single PRs for refactors" |
| **project** | Non-obvious project fact: "Auth rewrite driven by compliance, not tech debt" |
| **user** | New info about the user's role/expertise: "First time working with GraphQL" |

### What Does NOT Qualify

- Anything already captured in HANDOFF.md or session-log.md — duplication wastes tokens
- Code patterns, file paths, or architecture (derivable from the codebase)
- Session-specific debugging details
- Resource entries — those belong in CLAUDE.md's `## Resources` section via `/add-resource`, not memory

### Presentation

If insights exist, include them in the final summary block under a "Worth remembering" sub-section:

```
Worth remembering (for native Auto Memory):
  - [insight 1] ([type])
  - [insight 2] ([type])
```

Do **not** prompt the user to pick which ones to save — Claude Code's native Auto Memory decides on its own schedule. Your job is to surface the candidate; the harness persists it.

**Do not** write to `~/.claude/projects/<project>/memory/` directly. **Do not** create or edit `MEMORY.md`. If you detect that a prior rad-session version wrote memory files there, leave them alone — do not migrate or delete, and note it once in the final summary:

```
Note: detected legacy rad-session memory files at ~/.claude/projects/<project>/memory/.
These are no longer written to by /wrapup. Native Auto Memory manages that path.
```

### Session Complete

End with a brief confirmation:

```
Session wrapped up:
  - HANDOFF.md written ([N] lines)
  - Session log updated ([N] total entries)
  - CLAUDE.md [pruned: N changes (auto-proceeded | confirmed) | unchanged | created]
  [- Worth remembering: N insights surfaced for native Auto Memory]
```
