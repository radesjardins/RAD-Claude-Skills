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

**Announce at start:** "Wrapping up this session — gathering state, writing handoff, updating session log, pruning CLAUDE.md (Resources protected), surfacing insights, and syncing session files to git..."

## Mode flags

- `--push` — Skip the Phase 6.4 push prompt and push the session commit immediately. For autonomous loops or when the user has already decided.
- `--no-push` — Skip the push entirely; commit locally only. Useful for "I'm not done with this slice yet, don't share it."
- Neither push flag → prompt at Phase 6.4 (default).

- `--quick` — Fast wrapup for short sessions. Bounds Phase 1.3 tagging to the last 15 turns, skips Phase 4 (CLAUDE.md prune) unconditionally, skips recurring-trap promotion in Phase 3 maintenance. Use when "I just sat down for an hour, save state and go." For thorough wrapups (end of phase, end of week), run without `--quick`.

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

Walk the conversation already in your context — no tool call needed. To produce reliable, comparable output across models, use this explicit scan pattern instead of freeform reflection.

**Recency window (bounds cost on long sessions).** Do not tag the entire visible conversation by default. Tagging is bounded to the most recent meaningful work. Determine the window like this:

1. Scan backward through the conversation looking for any of these signals (the most recent one wins):
   - A user message containing `/wrapup`, `/checkpoint`, "wrap up", or "checkpoint"
   - A PreCompact systemMessage from rad-session (indicates context boundary)
   - A prior `/startup` briefing (turns before this are last session, already captured)

2. The window is everything from that signal forward to the current turn.

3. If no signal is found, the window is the **last 40 turns** (default cap).

4. In `--quick` mode (see Mode flags), the cap drops to the **last 15 turns** regardless of signals.

Only the turns inside the window are tagged. This bounds wrapup cost regardless of total session length — long sessions don't make wrapup proportionally slower. The PreCompact hook already covers the "context about to be lost" case separately, so safety isn't compromised.

**Scan pass.** Within the window, starting from the earliest turn and moving forward, tag each meaningful turn with one or more of these labels:

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

**Derive, don't re-synthesize.** Phase 2 already wrote a structured HANDOFF.md from the conversation tagging in Phase 1.3. The session-log entry is a mechanical compression of that same handoff — do **not** re-walk the conversation or re-tag turns. The fields map directly:

| Log entry field | Sourced from HANDOFF.md |
|---|---|
| Title | The HANDOFF.md `**Status:**` line, summarized to ≤8 words |
| `**Status:**` | The HANDOFF.md `**Status:**` line verbatim |
| `**Changes:**` | The HANDOFF.md `## Modified Files` section, compressed to a comma-separated list (drop per-file descriptions) |
| `**Decisions:**` | The HANDOFF.md `## Key Decisions` section, compressed to one-line-per-decision (keep the WHY, drop bullets) |
| `**Traps:**` | The HANDOFF.md `## What NOT To Do` section, in compact form `TRIED: X — FAILED BECAUSE: Y` (one line per trap, omit CORRECT APPROACH for the log) |

If a HANDOFF.md section is empty or omitted, the corresponding log field is omitted too — never write `N/A` or placeholders.

### Mechanism

1. Read `.claude/session-log.md` if it exists (may be empty or missing)
2. Build the new entry by mechanically compressing the HANDOFF.md you just wrote (no LLM synthesis needed)
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

1. **Skip in `--quick` mode** — trim oldest entries past the cap and stop. No trap-promotion scan, no CLAUDE.md edits. The next non-quick wrapup will catch up on promotions.
2. (Non-quick) Scan entries being trimmed for "Traps" that appear 3+ times across the full log (match on the FAILED BECAUSE clause, not the TRIED clause — same root cause with different surface attempts should still count)
3. If recurring traps found, promote them to CLAUDE.md as permanent rules (add under an appropriate existing section, or create a "Known Gotchas" section if none fits)
4. Remove entries beyond the 20-entry cap (trim from the bottom — oldest entries)
5. Notify the user:
   ```
   Session log maintenance: Trimmed [N] oldest entries.
   [If traps promoted]: Promoted recurring trap to CLAUDE.md: "[description]"
   ```

---

## Phase 4: Prune CLAUDE.md

Read CLAUDE.md and evaluate it for staleness, duplication, and ephemeral state.

### 4.0 Skip when CLAUDE.md is unchanged this session

The prune evaluation is the slowest non-synthesis phase of wrapup. Most sessions don't touch CLAUDE.md at all — re-evaluating an unchanged file every wrapup is wasted work.

**Skip Phase 4 entirely if all of these hold:**

1. CLAUDE.md exists (skipping the prune of a non-existent file is handled below).
2. Project is a git repo.
3. CLAUDE.md has no uncommitted changes: `git diff --quiet HEAD -- CLAUDE.md` returns 0.
4. The last commit that modified CLAUDE.md is older than the last session-log entry's date (i.e., CLAUDE.md hasn't been changed since the last wrapup):
   ```bash
   last_claude_commit=$(git log -1 --format=%cI -- CLAUDE.md 2>/dev/null)
   last_log_date=$(head -20 .claude/session-log.md | grep -m1 '^## ' | sed 's/^## \([0-9-]*\).*/\1/')
   # Skip Phase 4 if last_claude_commit < last_log_date
   ```

If skipped, log: `CLAUDE.md unchanged since last wrapup — prune skipped.` Continue to Phase 5.

In `--quick` mode, skip Phase 4 unconditionally (with the same one-line note).

If CLAUDE.md does not exist, run the "If No CLAUDE.md Exists" sub-step below; otherwise proceed to 4.1.

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

---

## Phase 6: Cross-Machine Sync (auto-commit + prompted push)

This phase keeps `HANDOFF.md` and `.claude/session-log.md` in sync across machines via git. Without it, the laptop never sees what the PC did, and vice versa.

**Behavior:**

- **Commit:** always, silently. Local commits are cheap and recoverable; not committing risks losing session state if the working tree is later discarded.
- **Push:** prompted by default. Yes → push; No → keep the commit local for next time. Stacking multiple unpushed session commits is fine and expected (e.g., several sessions on the same machine before switching).

### 6.1 Skip conditions

Skip Phase 6 entirely (and say nothing) if any of these hold:

- Project is not a git repo (`git rev-parse --git-dir` fails).
- All three target files are unchanged (no HANDOFF.md, session-log.md, or CLAUDE.md modifications this wrapup).
- An in-progress merge, rebase, or cherry-pick is detected (`git status --porcelain=v2 --branch` shows merge/rebase state, or `.git/MERGE_HEAD` / `.git/REBASE_HEAD` exists).

### 6.2 Stage only session files

**Critical: never `git add -A` or `git add .`** The user's other working-tree changes are theirs to manage.

Stage only the files this wrapup may have touched:

```bash
git add HANDOFF.md .claude/session-log.md
# Add CLAUDE.md only if Phase 4 modified it (created/pruned)
[ "$claude_md_modified" = "true" ] && git add CLAUDE.md
```

If none of the staged files actually has changes after staging (`git diff --cached --quiet`), skip the rest of Phase 6 silently — there is nothing to commit.

### 6.3 Auto-commit

Build the commit message from the HANDOFF.md status line and the current hostname:

```bash
HOSTNAME="${HOSTNAME:-${COMPUTERNAME:-$(hostname 2>/dev/null || echo unknown)}}"
DATE=$(date +%Y-%m-%d)
# STATUS comes from the HANDOFF.md **Status:** line written in Phase 2
git commit -m "session: ${DATE} on ${HOSTNAME} — ${STATUS}"
```

Commit must succeed before Phase 6 continues. If a commit hook fails, stop the phase and report the failure — do not retry with `--no-verify`. The local commit is the durable record; pushing is secondary.

### 6.4 Push decision

Determine push behavior in this priority order:

1. **`--push` flag passed to `/wrapup`** → push without prompting.
2. **`--no-push` flag passed to `/wrapup`** → skip push, end Phase 6.
3. **Non-interactive context** (autonomous loop, PreCompact-triggered wrapup, headless mode) → skip push silently. The local commit is sufficient; the next interactive wrapup can push.
4. **Otherwise** → prompt:

   ```
   Push session files to origin? (y/N)
   ```

   Default (empty / N / no) → skip push. Y → push.

### 6.5 Push

Only attempt push if the current branch has an upstream (`git rev-parse --abbrev-ref --symbolic-full-name @{u}` succeeds). If no upstream:

```
⚠ No upstream configured for this branch — session committed locally. Set an upstream with: git push -u origin <branch>
```

Then end Phase 6.

If upstream exists:

```bash
git push
```

On success: continue. On rejection (non-fast-forward, diverged): do not force, do not retry. Report:

```
⚠ Push rejected (likely diverged from origin). The session commit is safe locally. Resolve with: git pull --rebase  then  git push
```

### 6.6 Sync summary line

Append one line to the Phase 5 final summary so the user knows what happened:

- Committed + pushed: `Sync: committed + pushed (<short-sha>)`
- Committed, push declined: `Sync: committed locally (<short-sha>) — N unpushed session commits`
- Committed, push failed: `Sync: committed locally (<short-sha>) — push rejected, resolve manually`
- Skipped: omit the line.

### Session Complete

End with a brief confirmation:

```
Session wrapped up:
  - HANDOFF.md written ([N] lines)
  - Session log updated ([N] total entries)
  - CLAUDE.md [pruned: N changes (auto-proceeded | confirmed) | unchanged | created]
  [- Worth remembering: N insights surfaced for native Auto Memory]
  [- Sync: <one of the lines from 6.6>]
```
