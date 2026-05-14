# status.md Schema

**Status:** Draft (Phase 0 spec, 2026-05-14)
**References:** `doc-conventions.md`, `cross-plugin-contracts.md`

Field-by-field specification for `docs/status.md` — the project's evidence-based handoff and audit log.

## Purpose

status.md captures **project reality from evidence**. It is the answer to "where are things right now?" — not "where do we want them to be" (that's planning/current.md).

The intent/reality split is foundational. When planned-intent and observed-reality live in the same document, agents confuse aspiration with fact. status.md is the reality side.

**Audience:** /startup (next session reads this first), any agent loading project context, humans glancing at the file, code reviewers.

**Owner:** rad-session (writes at /wrapup from evidence). rad-planner scaffolds at /plan M6 with placeholders.

## Inference policy labels

Each field below is tagged with how it gets populated:

- **DIRECT** — read from file/git/etc., no inference involved. Strongest evidence.
- **HEURISTIC** — rule-based inference from data. Predictable, deterministic.
- **SYNTHESIZED** — model reasoning, bounded by source material.
- **USER-STATED** — only from explicit user input in the session.

The labels matter because the research's evidence-not-narrative principle requires clarity about which fields are evidence-bound vs. interpretation-bound. Stricter labels indicate the field cannot be invented.

## The eight sections

Section ordering is preserved as in the research template — it's the right reading order for /startup.

### Section 1: Current state

**Purpose:** One-glance snapshot of where the project is right now.

**Fields:**
- Branch / worktree
- Current milestone
- Overall status (enum: `on track` | `blocked` | `validating` | `needs decision`)

**Evidence sources:**
- Branch: `git rev-parse --abbrev-ref HEAD` — **DIRECT**
- Current milestone: read planning/current.md "Current milestone" section — **DIRECT**
- Overall status: see heuristic below — **HEURISTIC**

**Status heuristic:**

- `on_track`: acceptance criteria in current.md are progressing AND recent commits match planned-changes AND no blockers listed
- `blocked`: explicit blocker noted last update, OR most recent validation failed and hasn't been re-attempted
- `validating`: recent commits exist AND acceptance criteria still pending AND no failure detected (validation likely in progress; no assumption that untested code works)
- `needs_decision`: open question listed in current.md AND no commits in the last working session

Default to `on_track` only if no negative signal. Planner can override based on conversation ("I'm stuck on Y" → blocked even if commits look fine).

**Update cadence:** Every `/wrapup`.

**Update behavior:** Overwrite. This section is always "right now."

### Section 2: Last completed

**Purpose:** What concretely shipped this session (and possibly the last few).

**Evidence sources:**
- Commits since last status.md mtime — **DIRECT**
- Plan-task checkboxes that flipped from `[ ]` to `[x]` in current.md — **DIRECT**
- Commit messages parsed for completion signals — **HEURISTIC**

**Format:** Bullet list, most recent first. Each bullet: concrete completion, not narrative.

- Good: "Implemented weather firing rules for Tier 1 access (`lib/weather/tier1.ts`)"
- Bad: "Worked on weather stuff and made some progress"

**Inference policy:** HEURISTIC consolidation allowed. Multiple "WIP weather" commits → one "Weather firing rules for Tier 1 complete" — but the consolidation must be backed by actual completion evidence (test passed, milestone box checked, file created). Planner cannot invent completions.

**Update cadence:** Every `/wrapup`.

**Update behavior:** Rewrite. Keep last 5–10 items. Older items implicitly archived via git history of status.md itself.

### Section 3: Files changed recently

**Purpose:** Where work happened — so the next session knows where to look.

**Evidence sources:**
- `git diff --name-only <since-last-status>..HEAD` — **DIRECT**
- Uncommitted changes via `git status --porcelain` — **DIRECT**

**Format:** Path + one-line annotation per file (what was done to it). 10 entries max.

**If more than 10 files changed:** Prepend a header line: "Recent activity touched N files; showing 10 most-recently-modified:"

**Inference policy:** DIRECT for the file list. Annotation is HEURISTIC — derived from commit messages or diff content. If the annotation can't be confidently inferred, omit it (just the path).

**Update cadence:** Every `/wrapup`.

**Update behavior:** Rewrite. Cap at 10. If more, group ("`lib/weather/*` (5 files)") within the 10-item limit.

### Section 4: Latest validation results

**Purpose:** What's actually been tested, what passed, what failed.

**Evidence sources:**
- Test runner output captured during session (if available) — **DIRECT**
- Lint / typecheck / build results — **DIRECT**
- User-reported test status during conversation — **USER-STATED**

**Format:** Command + result per item. Result: `pass | fail | partial | not-run`.

**Inference policy:** STRICT. Only commands that actually ran in this session get listed with their actual results. Planner cannot infer "tests probably pass." If validation wasn't run, section says explicitly: "No validation run this session — last run YYYY-MM-DD with results: [...]".

This is the most evidence-strict section. The whole point of separating plan and status collapses if status fabricates validation results.

**Update cadence:** Every `/wrapup`, but only updates if validation actually ran. Otherwise marked stale with last-run date preserved.

**Update behavior:** Replace with most recent. If a command failed and was re-run, keep latest result.

**Length cap:** None — all commands run get listed.

### Section 5: Decisions made during execution

**Purpose:** Decisions that happened mid-session — durable enough to surface, but not always promoted to a full ADR yet.

**Evidence sources:**
- Candidate-decision detection at /wrapup (mechanical triggers + soft model reasoning) — **HEURISTIC**
- User-confirmed decisions during the session — **USER-STATED**
- Existing ADR pointers when user wrote one mid-session — **DIRECT**

**Format:** Each entry:
- Decision: short statement
- Why: brief reason
- Recorded in ADR? `yes (decisions/0007-...)` | `no` | `pending`

**Inference policy:** Candidate detection is HEURISTIC. Recording happens only with user confirmation (mentor mode: draft + accept/edit/skip; dev mode: quick approve list).

**Update cadence:** Every `/wrapup` when candidates surface.

**Update behavior:** Items marked `yes (recorded in ADR)` are **dropped at next wrapup** — the ADR is the durable record. Items marked `no` or `pending` stay until user revisits, or age past N sessions and get re-surfaced.

**Length cap:** Most projects have 0–3 per session; no formal cap.

### Section 6: Known issues or blockers

**Purpose:** What's actually getting in the way.

**Evidence sources:**
- Failed validation that wasn't fixed in the same session — **DIRECT**
- User-stated blockers during the session — **USER-STATED**
- Open questions in current.md that have aged past N days — **HEURISTIC**

**Format:** Bullet list, one line per blocker. Include first-noted date if blocker has been around more than a session.

**Inference policy:** Mix. Validation failure is hard evidence; user-stated is direct; aged-open-questions are softer (an old open question might just be inactive, not blocking).

**Update cadence:** Every `/wrapup`. Resolved items removed; new items added.

**Update behavior:** Rewrite. Planner can compare against last status to identify resolved-since items and surface them as completion signals for section 2.

**Length cap:** Soft cap 10 blockers. More than that is a project-level signal worth flagging.

### Section 7: Next recommended step

**Purpose:** First concrete thing the next session should do. Load-bearing for /startup.

**Evidence sources:**
- Pending acceptance criteria in current.md's current milestone — **DIRECT**
- "Notes for the next session" in current.md — **DIRECT**
- Blockers from section 6 (if blocking is the priority) — **DIRECT**

**Format:** One short paragraph. Three parts:
- Most likely next action
- First file to read
- First question to ask the user (if applicable)

**Inference policy:** SYNTHESIZED. Planner reads plan state + session context and proposes the next step. Bounded by what's in current.md; cannot invent goals.

**Update cadence:** Every `/wrapup`.

**Update behavior:** Overwrite.

**Length cap:** 3–5 lines.

### Section 8: If restarting from scratch

**Purpose:** Read-order for an agent waking up cold with no chat history. The /startup skill literally reads this section to know what to load.

**Evidence sources:**
- Operating manual location (CLAUDE.md or AGENTS.md per detected scope) — **DIRECT**
- Always include: planning/current.md, architecture.md — **DIRECT**
- Conditional: vision.md if user-facing work is in scope — **HEURISTIC**
- Resume question synthesized from section 7 — **SYNTHESIZED**

**Format:** Ordered list of files + one resume question or action.

```
- Read AGENTS.md
- Read docs/planning/current.md
- Read docs/architecture.md
- Resume with: "Pick up where we left off on M2 acceptance criterion 3 (weather firing rules for Tier 1) — failing test in lib/weather/tier1.test.ts"
```

**Inference policy:** Mostly DIRECT. File list is mechanical. Resume question is SYNTHESIZED from section 7.

**Update cadence:** Every `/wrapup`, but often stable across sessions (read-order doesn't change unless project structure does).

**Update behavior:** Update when read-order changes or when the resume action shifts.

**Length cap:** 3–6 files + 1 resume line.

## Cross-cutting principles

### Empty sections are explicit, not silent

If no validation ran this session, section 4 says "No validation run this session — last run YYYY-MM-DD with results: [...]". If no candidates surfaced, section 5 says "No decisions captured this session." An empty section without context is ambiguous; explicit "nothing here this time" is informative.

### Lookback bounds

Some fields look back since-last-status-mtime. If status hasn't been updated in a long time, that span could be weeks. Cap at: 50 commits OR 30 days, whichever is shorter. Beyond that, the planner notes "lookback truncated at X commits, see git log for full history."

### Branch handling (active hybrid)

**Default behavior:** Single `docs/status.md`, current branch only. New projects start here; most solo-dev workflows stay here.

**Detection trigger:** rad-session notices when:
- More than one local branch has had commits in the last 30 days, OR
- More than one git worktree is registered (`git worktree list` shows > 1)

When detected at /wrapup (or /startup), the plugin prompts:

> "I see multiple active branches/worktrees: [list]. Want me to start tracking status per-branch instead of a single file?"

**Migration to per-branch:** Existing `docs/status.md` becomes `docs/status-<current-branch>.md` (or `docs/status-main.md` if on main). Other branches get scaffold files at next /wrapup or /startup on those branches.

**Empty-state handling on a per-branch file:** When rad-session encounters a per-branch status that's blank or missing:

> "Status file for branch `feature-y` is blank. Three options: (1) document what this branch is for and what's next; (2) mark it for cleanup — branch should be removed or merged; (3) leave it blank, you'll come back to it. Which?"

**Merged-branch cleanup:** At /wrapup, rad-session checks `git branch --merged <default-branch>`. For each merged branch with a status file:

> "Branch `feature-x` was merged 2 days ago. Remove `docs/status-feature-x.md`? (Y/n/never-ask)"

Git history preserves the file regardless. "never-ask" sets `.rad/profile` to auto-clean future merged-branch statuses silently.

**Cooldown on re-prompts:** Once user picks single-file mode, don't re-prompt for at least 30 days or some commit threshold.

### Length caps per section

Soft caps:
- Section 1: < 5 lines
- Section 2: 5–10 bullets
- Section 3: 10 paths (or grouped within 10 entries)
- Section 4: All commands run + their results (no cap — strict evidence)
- Section 5: All candidates (no cap)
- Section 6: < 10 blockers
- Section 7: 3–5 lines
- Section 8: 3–6 files + 1 resume line

If a section exceeds its soft cap repeatedly, that's a signal worth flagging to the user.

### Section ordering preserved

The template's order (current state → last completed → files → validation → decisions → blockers → next → restart) is the right reading order for /startup. Don't reorder.

## The "If restarting from scratch" pointer's special role

Section 8 is load-bearing for /startup. It's the answer to "what do I read to pick up cold?" — designed so an agent with zero chat context can load the right files and start working.

Format:

```markdown
## If restarting from scratch
- Read AGENTS.md
- Read docs/planning/current.md
- Read docs/architecture.md
- Resume with this question: "[next exact question or next exact action]"
```

The resume question is the most synthesized field in the file. It compresses section 7's three-part synthesis into a single actionable sentence.

## No-work-detected behavior

When /wrapup is invoked but no work is detected since the last status update (no commits, no changed files, no plan-task changes), rad-session refuses to run:

> "No work detected since last wrapup. Nothing to wrap up — exit, or run anyway to refresh timestamps?"

Per Phase 0 lock, the default is to exit. Forcing a noise update would erode status.md's evidence quality.
