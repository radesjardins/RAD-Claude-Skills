# Entry Point Routing — /plan

**Status:** Draft (Phase 0 spec, 2026-05-14)
**References:** `doc-conventions.md`, `cross-plugin-contracts.md`, `status-md-schema.md`

How `/plan` determines what kind of planning conversation to run, what state to read, and what artifacts to produce. Four entry points, four explicit flags, one universal ambiguity fallback.

## The four entry points

The four entry points are user-facing categories with clear definitions and explicit flag support.

### 1. Full plan (greenfield)

**Definition:** Start from scratch. Walk through goal, scope, milestones, quality gates; recommend a doc set; produce complete planning artifacts.

**Use cases:**
- New projects with no existing planning documents
- Projects with loose/minimal initial structure that need a real foundation
- Existing projects where existing docs need a full rewrite (rare — usually pivot is the better fit)

**End state:** Complete planning artifacts in the project directory: operating manual Constitution sections, vision.md, architecture.md, planning/current.md, status.md scaffold, decisions/README.md, optionally roadmap.md.

**Flag:** `/plan --full`

### 2. Improvement

**Definition:** Take the existing plan and deepen it, fill in missing detail, or pick up where it left off. Existing plan and docs stay; we add or refine.

**Sub-branches** (always-ask, no automatic detection):
- **Continue:** "I've executed the plan up to some point and need help with what comes next." Picks up next acceptance criterion, surfaces blockers, structures next steps.
- **Deepen:** "I'm mid-milestone and want to add detail, scope, or specificity to what we're working on — without changing direction." Adds sub-tasks, clarifies criteria, surfaces decisions that need ADRs.

**Use cases:**
- Plan exists but lacks detail (deepen)
- User stuck on what to work on next (continue)
- Mid-milestone refinement
- Adding scope to current milestone (within bounds — see escalation handling)

**End state:** Updated planning/current.md, possibly new ADRs, possibly minor updates to roadmap.md. Strategic docs (vision, architecture) typically unchanged.

**Flag:** `/plan --improve`

### 3. Drift assessment

**Definition:** Compare what's been built against what was planned. Output is a report, not necessarily a new plan.

**Use cases:**
- User feels off-course but can't articulate why
- Periodic project health check
- Pre-pivot sanity check ("are we just drifting, or should we pivot?")

**End state:** A drift report at one of three severity tiers (no drift / some / significant), with specific findings and a three-option action menu (incorporate / sub-plan / handle yourself). May result in updates to planning/current.md, but does not unilaterally rewrite plans.

**Flag:** `/plan --drift`

### 4. Pivot

**Definition:** Substantial re-plan because direction has changed. Existing context preserved (archived, not deleted); strategic docs may be revised; current plan replaced.

**Use cases:**
- Audience or scope has fundamentally shifted
- User's vision for the project has taken a significant change
- Scope creep has gotten out of hand and requires re-foundation

**End state:** Disposition manifest covering every existing artifact; archived previous current.md; revised strategic docs as needed; new planning/current.md; superseded ADRs marked appropriately.

**Flag:** `/plan --pivot`

## Detection model

When `/plan` is invoked without a flag, the planner determines the entry point through a three-step detection process.

### Step 1: Read user invocation

Capture the natural-language text the user provided with the `/plan` invocation.

### Step 2: Inspect project state

Compute a feature vector mechanically from the project directory (no model reasoning):

- `has_git` — `.git/` exists with at least 1 commit
- `commit_count` — number of commits in current branch
- `source_file_count` — code files, excluding node_modules / build outputs / .venv / similar
- `has_operating_manual` — `AGENTS.md` or `CLAUDE.md` exists with non-trivial content (>500 bytes, not pure /init residue)
- `has_strategic_docs` — `docs/vision.md` OR `docs/architecture.md` exists
- `has_planning_current` — `docs/planning/current.md` exists with substantive content
- `has_status` — `docs/status.md` exists with populated fields
- `planning_current_progress` — none / partial / complete (acceptance-criteria checkbox state)
- `recent_activity_spread` — focused (matches current.md planned changes) / diffuse (broad)
- `status_freshness` — fresh / stale

### Step 3: Compute hypothesis

State produces a prior; utterance produces a prior; they combine.

#### State priors

- **Greenfield prior:** `has_git == false` OR (`commit_count < 3` AND `source_file_count < 10` AND `has_strategic_docs == false`)
- **Improvement prior:** `has_git == true` AND `has_planning_current == true` AND `planning_current_progress != complete` AND `status_freshness == fresh`
- **Drift-check prior (weak):** `has_planning_current == true` AND `recent_activity_spread == diffuse` AND `status_freshness == fresh`. Primarily utterance-driven.
- **Pivot prior (weak):** `has_planning_current == true` AND (`planning_current_progress == partial` OR `complete`) AND existing strategic docs present. Primarily utterance-driven.
- **Ambiguous-existing prior:** `has_git == true` AND `has_planning_current == false`. Existing code with no plan — could go any direction; planner asks.

State alone reliably distinguishes greenfield from "something exists." It can't reliably distinguish improvement vs drift-check vs pivot.

#### Utterance signal triggers (hybrid keyword + model)

**Tier 1 — keyword shortcut.** Quick literal matching against curated phrases:

| Entry | Trigger keywords |
|---|---|
| Full plan | "have an idea", "new project", "new app", "from scratch", "starting fresh", "no plan yet", "need a plan", "greenfield" |
| Improvement | "improve the plan", "deepen", "more detail", "flesh out", "next step", "what's next", "stuck", "not sure where to go" |
| Drift assessment | "off course", "off track", "drift", "drifting", "scope creep", "feels wrong", "are we sticking to", "audit", "check the plan" |
| Pivot | "pivot", "rescope", "redirect", "change direction", "not what I envisioned", "shift focus", "major change", "restart but keep" |

**Tier 2 — model classification.** If no clear keyword fires and the utterance has substance, the planner classifies the intent through reasoning.

**Tier 3 — no signal.** Utterance is empty or generic. State alone drives detection; if state is also ambiguous, menu fires.

### Step 4: Reconcile and confirm

**High confidence (state and utterance agree):**

> "Greenfield project — empty directory, planning from scratch. Sound right?"

One-line confirmation. Fast.

**Moderate confidence (one strong signal, other weak/absent):**

> "I see existing code and an active plan at `docs/planning/current.md` (milestone 2 of 4, last status update 3 days ago). Treating this as an improvement entry — confirming you want to deepen or continue the existing plan, not pivot or check for drift?"

Brief rationale plus explicit confirmation.

**Low confidence (signals disagree or are absent):**

Fall to the universal four-direction menu (see below).

**Hard contradiction (state says one thing, utterance another):**

Surface the contradiction explicitly:

> "You said 'new project' but I see existing code and docs in this directory. Possibilities — starting fresh in a different directory, pivoting on existing work, or treating this code as scaffolding. Which?"

## The four-direction menu

The universal ambiguity fallback. Fires when detection is low-confidence, or whenever the planner can't be sure.

```
Discovery summary:
- Working directory: [path]
- Git: [N commits / no git]
- Code: [N source files]
- Strategic docs: [list found / none]
- Current plan: [milestone X of Y, last updated N days ago / none]
- Status: [fresh / stale / none]
- Operating manual: [content / /init residue / none]

I'm not 100% clear which plan direction you want to take. Which matches?

1. Full plan — Start from scratch. Walk through goal, scope, milestones, quality
   gates; recommend a doc set; produce complete planning artifacts. Use for new
   projects or when existing docs need a full rewrite.

2. Drift assessment — Compare what's been built against what was planned.
   Output is a report, not a new plan. Use when you're not sure if the project
   has gone off course.

3. Improvement — Deepen the existing plan, fill in missing detail, or pick up
   where it left off. Existing docs stay; we add or refine. Use when the plan
   exists but needs more or you're stuck on next steps.

4. Pivot — Substantial re-plan because direction has changed. Existing context
   preserved (archived, not deleted); strategic docs may be revised; current
   plan replaced. Use when the project is shifting meaningfully.

(Run /plan --full, --drift, --improve, or --pivot to skip this question.)
```

**The menu fires when:**
- Detection low-confidence
- State + utterance conflict
- User invokes `/plan` with no message
- Ambiguous-existing case (code with no plan)
- User explicitly asks "what should I do here?"
- Empty-flag invocation (e.g., `/plan --improve` with no message) — surfaces menu to confirm entry

**The menu skips when:**
- Explicit flag used with utterance that confirms the flag — proceeds with one-line confirmation
- High-confidence detection — proceeds with one-line confirmation

## Explicit flags

`/plan --full` — full plan / greenfield entry
`/plan --improve` — improvement entry
`/plan --drift` — drift assessment entry
`/plan --pivot` — pivot entry
`/plan --validate` — utility; runs validators on existing plan artifacts without entering a conversation

Flags act as strong hints. When combined with a confirming utterance and matching state, they skip detection. When invoked alone (no utterance), they surface the four-direction menu to confirm.

## Discovery summary template

The planner generates a discovery summary by inspecting the project state. Used as the opening context for the four-direction menu and for high/moderate-confidence one-line confirmations.

Format:

```
Discovery summary:
- Working directory: <path>
- Git: <N commits / no git>
- Code: <N source files>
- Strategic docs: <list found / none>
- Current plan: <milestone X of Y, last updated N days ago / none>
- Status: <fresh / stale / none>
- Operating manual: <content / /init residue / none>
```

## Per-entry conversation shapes

### Full plan (greenfield)

The five-phase conversation:

1. **Constitution & Frame** — goal, why now, project-wide principles (style, naming, what's never allowed)
2. **Goal-Backward Scope** — what must be TRUE, EXIST, CRITICAL; what's deferred; hardest unknown; risks
3. **Sequence with Size Discipline** — how CRITICAL items sequence, what parallelizes, milestones fit 2–3-task / ~50%-context bar
4. **Quality Gates** — what "done" means per milestone, how we verify, when we stop
5. **Doc-Set Recommendation** — recommend doc set with project-specific rationale; complexity routing (lite / standard / full)

M6 executes the plan's M0: doc creation per the approved set.

### Improvement

Opens with sub-branch question (always-ask):

> "Quick check — are we picking up the next thing in the plan (continue from where you left off), or adding detail to what we're already working on (deepen the current milestone)?"

**Continue sub-branch — opening questions:**
1. State confirmation: "Looks like you're picking up where you left off. Status says current milestone is M[N], with acceptance criteria [list pending]. Sound right, or has anything shifted since last wrapup?"
2. What's completed since last status (verify against git evidence and plan-task checkboxes; flag if status is stale)
3. What's blocking the obvious next step
4. Anything relevant since last session that should factor in

Output: most likely a small update to current.md, a clear "do this next" handoff. Strategic docs usually untouched.

**Deepen sub-branch — opening questions:**
1. Which piece of the current milestone do you want more detail on
2. Is this adding scope or adding specificity
3. Does this change milestone exit criteria, or just how we get there
4. Any decisions surfacing that should be ADRs

Output: substantive update to current.md (new sub-tasks, expanded acceptance criteria, clarified planned changes). May add ADRs.

**When both apply:** Sequence deepen first (current work), then continue (next thing).

**Generic improvement utterance with no sub-branch signal:** Planner reads state to pick a default (complete acceptance criteria → continue; partial criteria + recent commits → deepen) but always confirms with the always-ask question.

### Drift assessment

Reads source material and compares against the plan. Five drift areas:

1. **Scope drift** — work happening outside what was planned
2. **Dependency drift** — new packages added without an ADR
3. **Architectural drift** — new patterns introduced that aren't documented
4. **Acceptance criteria drift** — criteria skipped, reordered, or reinterpreted (sequence-flexibility framing — see below)
5. **Non-goal drift** — recent work touching things vision.md explicitly says are out

#### Sources read

- `planning/current.md` for Objective, Non-goals, Current milestone, Acceptance criteria, Planned changes, Risks
- `docs/decisions/*.md` for ADR titles + decision statements
- `docs/architecture.md` for Canonical patterns, Core invariants
- `docs/vision.md` for Non-goals
- `docs/status.md` for previous baseline
- Git log + diff
- Package manifest (`package.json` / `Cargo.toml` / `pyproject.toml`)

#### Lookback boundary

The more recent of (status.md mtime, current milestone start date). Bounded at 30 days or 50 commits maximum.

#### Drift area computation

**Scope drift:**
- `changed_files = git diff --name-only <lookback>..HEAD`
- `planned_files = parsed from current.md "Planned changes" section`
- `unplanned = changed_files - planned_files`
- Edge: if Planned changes doesn't list files (just task descriptions), fall back to directory-level match

**Dependency drift:**
- `current_deps = parsed from package manifest`
- `baseline_deps = parsed from package manifest at <lookback> commit`
- `new_deps = current_deps - baseline_deps`
- `unrecorded_deps = new_deps - deps_mentioned_in_ADRs`

**Architectural drift:**
- v1 leans mechanical-only with model fallback for ambiguous cases
- Mechanical: search for known canonical-pattern keywords from architecture.md in recent diff; flag absences
- Soft: model reasoning on whether a new pattern appears in recent code that isn't in architecture.md's Canonical patterns
- AST analysis is out of scope for v1

**Acceptance criteria drift:**
- Parse acceptance criteria checkboxes from current.md
- Compare order completed against the order listed
- Flag: criteria skipped, criteria appearing complete by commit content but not checked off, criteria checked off without matching commit evidence

**Non-goal drift:**
- Parse non-goals from vision.md (project-level) and current.md (plan-level)
- For each recent commit, check if commit message or changed files match non-goal content
- Keyword matching with model fallback

#### Severity tiers

- **No drift:** Zero unplanned files (or all clearly serve planned tasks), zero unrecorded deps, zero new architectural patterns, acceptance criteria progressing in order, zero non-goal touches.
- **Some drift:** 1–2 unplanned files in scope-adjacent areas, OR 1 unrecorded dep, OR 1 skipped/delayed acceptance criterion, OR 1 minor non-goal touch.
- **Significant drift:** 3+ unplanned files, OR 2+ unrecorded deps, OR new architectural pattern not in architecture.md, OR systematically reordered/skipped acceptance criteria, OR substantial non-goal touch.

Multiple "some" findings across different areas can compound to "significant."

#### Sequence flexibility framing (acceptance criteria drift)

When the user is working on M3 features while M2 still has open criteria, default assumption is intentional, not drift. Planner surfaces it for confirmation:

> "I see acceptance criteria for M3 progressing while M2 still has 2 open items (criteria 4 and 6). Sequence flexibility — are you working in parallel and planning to come back to M2, or did M2 get deprioritized? If the latter, worth updating `current.md`."

#### Output format (three tiers)

**No drift detected:**

> "I compared recent work (last N commits, M files changed) against the current plan (milestone X of Y).
>
> No drift detected. Recent activity matches the planned scope, no new dependencies, acceptance criteria are progressing as expected, and the architectural patterns in use are documented in architecture.md.
>
> Is there anything specific you'd like me to consider further, or is the assessment sufficient?"

**Some drift detected:**

> "I compared recent work against the current plan. Some drift detected:
>
> - [Finding 1]
> - [Finding 2]
> - [Finding 3]
>
> Three options:
> 1. Incorporate these into the plan
> 2. Brainstorm a sub-plan to get back on course
> 3. Take care of it yourself"

**Significant drift detected:**

> "I compared recent work against the current plan. Significant drift detected:
>
> [Multiple findings across categories]
>
> The project has moved meaningfully beyond the original plan. Three options:
> 1. Incorporate these into the plan
> 2. Brainstorm a sub-plan to get back on course
> 3. Take care of it yourself
>
> Given the size of the drift, you might want to consider whether this is actually a pivot rather than course-correction. /plan --pivot would explicitly treat it as one."

#### Individual finding format

- Category (Scope / Dependency / Architectural / Acceptance / Non-goal)
- Specific evidence (file paths, dep names + versions, pattern descriptions)
- Severity (low / moderate / high)
- Suggested resolution (what doc to update if incorporating; what to roll back if course-correcting)

Example:

> **Scope (moderate):** `lib/cache.ts` and `lib/queue.ts` were created in the last 5 commits but aren't in current.md's Planned changes. Suggested resolution: if these are needed for M2, add them to Planned changes and write a brief ADR for the caching choice; if not, consider whether they should be deferred to a later milestone or removed.

#### Handling "I don't know" on ambiguous findings

When the user can't decide on a borderline finding, three escalation moves:

1. **Investigate further:** "Let me look at `lib/cache.ts` more closely — it's importing from the planned cache layer module, so it seems related. Does that match your memory of why you created it?"
2. **Note as open question:** Add to `planning/current.md`'s "Open questions" section. Surfaces on next drift-check.
3. **Suggest watching:** "OK, leaving this unflagged for now. If it turns out to matter, we'll catch it on the next drift-check or wrapup."

Respect for "I'm not sure" — never force a binary answer when the honest answer is uncertainty.

#### Token cost discipline

Drift-check should run under 2k tokens for typical projects, 3k absolute cap. Mechanical comparisons preferred over model reasoning.

#### No-plan case

If drift-check is invoked on a project without `planning/current.md`, the planner doesn't refuse — it says:

> "No plan to check against. The work in this directory can inform a planning session if you want one. Want to create a plan? I can use the existing code as context."

Routes to /plan --full or /plan --improve depending on what the user picks.

### Pivot

Opens with the seven-question opening conversation:

1. **Summary of the plan/roadmap as it exists.** Planner reads vision.md, current.md, archive/, decisions/ and surfaces the current state in plain language.
2. **Echo back the user's original concern.** "You said 'this isn't what I envisioned and we need to rescope.' Holding that."
3. **"What are you happy with right now?"** — surfaces what survives. Long list → drift-shaped; short list → pivot-shaped.
4. **"What specifically do you want to change, remove, or roll back?"** — surfaces what's being killed.
5. **"What hasn't changed about the project — what's still load-bearing in your head?"** — surfaces the scaffolding that carries forward (some load-bearing things may not have been on the "happy with" list — they're just assumed to continue).
6. **"What's your ultimate vision for this project now?"** — surfaces direction; compares against existing vision.md.
7. **"What would 'done' look like for this?"** — surfaces scope of the new plan.

After Q4 and Q5, the planner can already gauge lift size:
- Drift-shaped: Q3 yields long list, Q4 yields 1–2 items → planner offers to switch entries to drift assessment.
- Pivot-shaped: Q3 yields short list, Q4 yields substantial list → continue into the disposition step.

#### Pivot disposition manifest

After the seven questions, planner walks the existing artifacts with the user. For each file (vision.md, architecture.md, roadmap.md, current.md, each decisions/NNNN-*.md):

- **Carry forward** — survives unchanged, references update if needed
- **Revise** — content is partly relevant; edit in place
- **Archive** — move to `planning/archive/` or `.rad-archive/`; retain as historical record
- **Supersede** — for decisions; new entry written that supersedes the old with a reference; old entry marked superseded
- **Delete** — only for content with no historical value (rare; archive is usually safer)

For code: **Flag for human cleanup** — planner doesn't touch code. Lists code paths the user said are being discarded; user handles the actual deletion.

The manifest is shown as a markdown table:

| File | Current content | Disposition | Reason / notes |
|---|---|---|---|
| `docs/vision.md` | Solo-hunter trip planning | Revise | Audience expanding to families |
| `docs/architecture.md` | Stack, tier system | Carry forward | Scaffolding unchanged |
| `docs/decisions/0007-...` | Hunter-only features | Supersede | New ADR records family-mode also supported |
| ... | ... | ... | ... |

User reviews, edits dispositions, approves. Then planner executes:
- Moves planning/current.md to `planning/archive/YYYY-MM-DD-pre-pivot.md`
- Writes new ADRs that supersede the old ones with `Supersedes 0007` references
- Edits vision.md, roadmap.md, status.md per dispositions
- Drafts new current.md from the pivot conversation
- Saves the manifest as `planning/archive/YYYY-MM-DD-pivot-manifest.md` (the receipt of the pivot)

Code paths tagged for human cleanup are listed but not touched.

#### Scaling

For small projects (a dozen docs, handful of ADRs), the manifest is quick — maybe 15 rows. For large projects (50+ docs), show the full table and let the user scroll. Grouping by category is deferred to a future version only if real-world use shows it's needed.

#### After execution

The new plan proceeds through the five-phase conversation with the carry-forward content pre-loaded as context.

## Re-routing between entries

Entries are not strictly locked once detection completes. The conversation can re-route:

**Drift → Pivot.** Significant drift assessment surfaces that this is actually a pivot. Planner suggests at the end of the assessment.

**Pivot → Drift.** Pivot's seven-question opening reveals lift is smaller than expected. After Q4/Q5, planner offers: "Reading your answers, this is sounding more like course-correction than pivot — most of the existing plan survives. Want to switch to drift assessment, or proceed with pivot?"

**Improvement → Pivot.** Mid-improvement conversation reveals the additions amount to a significant direction change. Planner surfaces: "What you're describing is starting to look like a pivot rather than improvement. Continue as improvement, or switch entries?"

**Continue → milestone-complete shift.** If improvement-continue starts and the user describes work that completes the current milestone, planner notices and shifts: "Sounds like M2 is actually done — want me to mark it complete and start planning M3?"

The user always confirms re-routing.

## No-plan case handling

If `/plan --drift` is invoked on a project without `planning/current.md`:

> "No plan to check against — drift assessment needs a plan. Want to create one? Existing code can inform a planning session."

If `/plan --improve` is invoked without an existing plan:

> "No plan to improve — improvement needs a plan to start from. Want to create one?"

If `/plan --pivot` is invoked without an existing plan:

> "No plan to pivot from — pivot needs an existing direction to redirect. Want to create a fresh plan instead?"

All three route to the four-direction menu with full plan pre-highlighted.

## Edge cases

**Directory doesn't exist yet.** User said "create at this path" during pre-flight discovery. Auto-greenfield; no state to inspect.

**Existing repo with no plan docs at all.** Has git, has code, no `docs/planning/current.md`. Falls to four-direction menu: "I see existing code with no plan. Add planning to this project (improvement-flavored) or start fresh on the planning side (greenfield)?"

**Plan exists but is stale (months old).** Could be resumed project or forgotten one. Falls to menu: "Plan exists but hasn't been touched in 4 months. Are we resuming this plan or rescoping?"

**`/plan` invoked with no message.** No utterance signal at all. State-based detection runs; if state is unambiguous, confirms with one-line; if state is ambiguous, menu fires.

**Mid-conversation entry-point shift.** User says "actually, this feels more like a pivot." Planner allows graceful re-routing — archives current discovery, restarts at the new entry, doesn't lose collected context.

**Hard contradiction (state vs. utterance).** Surface explicitly. Don't try to resolve silently.
