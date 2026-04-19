---
name: plan-project
description: >
  This skill should be used when the user says "plan my project", "create an implementation
  plan", "plan this app", "I need a plan before coding", "help me architect this", "let's
  plan before we build", "create a project plan", "implementation plan", "plan this feature",
  "map out the work", "break this down into tasks", "create a roadmap", "project breakdown",
  or wants to create a structured, dependency-aware implementation plan before writing any
  code. Also trigger proactively when a user describes a non-trivial project idea and
  appears ready to start coding without a plan.
argument-hint: "[project description or existing codebase path] [--non-interactive] [--resume <run-id>]"
user-invocable: true
allowed-tools: Read Glob Grep WebSearch WebFetch Agent Write
---

# Plan Project — Structured Implementation Planning

You are orchestrating a complete project planning workflow. Your goal is to produce a zero-context-ready implementation plan that prevents the "vibe coding doom loop" — where AI agents write code without a plan, encounter conflicts, and spiral into endless correction loops.

**CRITICAL: You are in PLANNING MODE. Do NOT write implementation code. Do NOT create source files. You produce planning artifacts ONLY.**

## Cross-model note

This skill works identically across Opus 4.7, Sonnet 4.6, and Haiku 4.5. Opus/Sonnet should batch reference file reads, codebase exploration reads, and independent subagent dispatches into parallel tool-call bursts (see "Execution: parallel-first" below). Haiku may follow phase order sequentially if parallel batching misbehaves. The plan output and subagent JSON contracts are identical regardless of model.

## Execution: parallel-first

This skill chains multiple phases with heavy sub-agent dispatch and reference loading. To keep wall-clock time and context usage sane:

- **Phase 1 codebase exploration** has no inter-file dependencies when the project exists. Issue parallel Reads for `CLAUDE.md`, `README.md`, `package.json`, `tsconfig.json` (or language-equivalent config), plus a Glob of the top-level directory structure. Only serialize when a specific route/module identified in the batch needs targeted reading.
- **Phase 3 reference loading** (`plan-template.md`, `task-format.md`, `anti-patterns.md`, `failure-state-template.md`, `tdd-constraints.md`, `context-management.md`) has no inter-file dependencies — single parallel batch.
- **Phase 2 and Phase 4 subagent dispatches** are independent of each other only when Phase 2 is complete before Phase 3 begins. Within Phase 4's risk-assessor iteration loop, each iteration is sequential (the next iteration needs the prior iteration's findings), but any file reads within an iteration should be parallel.
- **What to serialize, always:** user-approval gates (Phase 5 explicit approval), and the discovery → stack → plan → risk → review phase order.

## Mode Flags

This skill honors two mode flags when passed in the invocation (`/rad-planner:plan-project --non-interactive`, etc.):

- `--non-interactive` — Skip all user-approval gates. Produce a best-effort plan, commit the artifacts, and emit a trailing JSON block listing `awaiting_user_review` items (e.g., unconfirmed scope, unvalidated stack choices, unresolved risk-assessor findings). Auto-proceed thresholds: stack-advisor `verification_verified: true` with `confidence: high|medium` → proceed; risk-assessor `verdict: APPROVE` → proceed; any `RETHINK` verdict → halt regardless of mode and escalate. For agent/CI callers that deadlock on interactive menus.
- `--resume <run-id>` — Load checkpoint state from `.planner/state/<run-id>.json` and continue from the last saved phase. See "Checkpoint & Resume" below.

If neither flag is present, run interactively as documented.

## Checkpoint & Resume

Long planning runs (codebase exploration + stack eval + full DAG construction + risk audit + plan review) are compaction-prone. Save state to `.planner/state/<run-id>.json` at these transitions:

1. After Phase 1 (discovery complete, codebase explored if applicable)
2. After Phase 2 (stack recommendation received and accepted)
3. End of Phase 3 (plan DAG drafted)
4. After each Phase 4 risk-assessor iteration
5. After Phase 5 (user approval)
6. After Phase 6 (artifacts written)

Checkpoint schema (shared with `review-plan` and `evaluate-stack`):
```json
{
  "run_id": "string",
  "skill": "plan-project | review-plan | evaluate-stack",
  "phase": "1 | 2 | 3 | 4-iter-N | 5 | 6",
  "started_at": "ISO-8601",
  "last_saved": "ISO-8601",
  "model": "opus | sonnet | haiku",
  "project_summary": "string",
  "codebase_context": {
    "root": "string",
    "claude_md_present": false,
    "stack_detected": ["string"]
  },
  "stack_recommendation": "JSON from stack-advisor or null",
  "plan_path": "string or null",
  "tasks_path": "string or null",
  "risk_history": [{"iteration": 1, "verdict": "REVISE", "issue_count": 0}],
  "escalation": {"required": false, "reason": "", "route_to": ""},
  "awaiting_user_review": ["string"]
}
```

On `--resume <run-id>`, load the file, announce the phase you're resuming from, and continue. Do not re-run completed phases.

## Workflow

### Phase 1: Strategic Discovery

**Pre-discovery scope check.** If the user's project idea is clearly fuzzy (they're still debating what to build, which approach to take, or whether the problem is even the right one to solve), recommend they run `/rad-brainstormer:brainstorm-session` or `/rad-brainstormer:design-sprint` first and return here once the direction is locked. `plan-project` produces an implementation plan — it assumes the *what* is decided and plans the *how/order*. Proceed only once the user confirms they have a direction.

**If the user provided a project description:**
1. Summarize your understanding of the project
2. Ask 3-5 high-information strategic questions (NOT implementation details):
   - "What's the most important thing this system must get right?"
   - "What's the biggest technical risk you see?"
   - "Who are the target users and what's their primary workflow?"
   - "What existing systems does this need to integrate with?"
   - "What are the hard constraints? (timeline, team, infrastructure)"
3. Wait for answers before proceeding (skip in `--non-interactive` — record unanswered questions in `awaiting_user_review`)

**If in an existing codebase:**
1. Issue parallel Reads for `CLAUDE.md`, `README.md`, `package.json`, `tsconfig.json` (or language equivalents), plus a Glob of the top-level structure
2. After the batch, identify patterns, conventions, and integration points
3. Present findings to the user and ask clarifying questions (skip interactive Qs in `--non-interactive`)

Save Phase 1 checkpoint.

### Phase 2: Stack Evaluation

Use the Agent tool to delegate to the `stack-advisor` agent using the substituted template from `references/subagent-prompts/stack-eval.md`. Pass `mode` (`new_project` | `evaluate_existing` | `compare_frameworks`) and `project_context`.

Parse the returned JSON per the `stack-eval.md` schema:
- `evaluation_complete: true` + `confidence: high|medium` → present recommendation to user (or auto-proceed in `--non-interactive`)
- `confidence: low` → surface risks to user before proceeding
- `escalation_required: true` → stop. Surface `escalation_reason` to user and recommend rethinking scope via brainstormer

If Context7 MCP is available, the stack-advisor uses it to fetch current documentation. If not, it uses WebSearch. Either way, the JSON's `verification_sources` documents what was checked.

Save Phase 2 checkpoint.

### Phase 3: Build the Plan

Load references in a single parallel batch: `plan-template.md`, `task-format.md`, `anti-patterns.md`, `failure-state-template.md`, `tdd-constraints.md`, `context-management.md`.

1. **Define milestones** — logical phases of work (3-6 milestones typical)
2. **Break into tasks** — each milestone becomes 3-8 specific tasks
3. **Map dependencies** — explicit `Dependencies: [S1, S2]` for every task
4. **Score complexity** — 1-10 per task; expand any task > 7 into subtasks
5. **Verify DAG** — check for circular dependencies (A->B->C->A = forbidden)
6. **Define validation** — every task gets a runnable validation check
7. **Define rollbacks** — every task gets a revert procedure
8. **Set test strategy** — per TDD constraints in `references/tdd-constraints.md`
9. **Insert checkpoints** — after every milestone, per `references/failure-state-template.md`
10. **Plan context management** — identify where to checkpoint/clear sessions per `references/context-management.md`

Save Phase 3 checkpoint.

### Phase 4: Risk Assessment

Use the Agent tool to delegate to the `risk-assessor` agent using the substituted template from `references/subagent-prompts/risk-assessment.md`. Pass the draft plan, current `iteration_number`, and `max_iterations` (default 3).

Parse the returned JSON per the `risk-assessment.md` schema:

- `verdict: APPROVE` → proceed to Phase 5
- `verdict: REVISE` and `iteration < max_iterations` → fix `blocking_issues`, increment iteration, re-dispatch. Save per-iteration checkpoint.
- `verdict: REVISE` and `iteration >= max_iterations` with issues remaining → stop looping. Surface `unresolved_issues` to user: "Risk assessment hit iteration cap. Decide: (a) accept these as known gaps, (b) drop back to Phase 3 and restructure the affected tasks yourself, or (c) re-enter via `/rad-brainstormer:design-sprint` if the architecture itself is the problem." In `--non-interactive`, add unresolved issues to `awaiting_user_review`.
- `verdict: RETHINK` → stop immediately regardless of iteration. Surface to user: "Risk assessment returned RETHINK. The architecture has fundamental issues that task-level patches won't fix. Re-enter via `/rad-brainstormer:design-sprint` to rework the architecture, then return here for planning." Set `escalation.required: true` and `escalation.route_to: "/rad-brainstormer:design-sprint"` in the checkpoint. Do not proceed.

### Phase 5: Plan Review & Approval

Present to the user:
1. **Executive summary** — milestones, task count, complexity distribution, estimated risk level
2. **Architecture overview** — component diagram, key decisions
3. **Full task list** — with dependencies, validation, and rollback for each
4. **Risk report** — any remaining concerns and mitigations
5. **Context management plan** — when to checkpoint and clear

**Ask the user explicitly: "Does this plan look correct? Should I adjust anything before we lock it in?"**

The plan is NOT approved until the user says so. (In `--non-interactive` mode, skip approval and add "plan not reviewed by user" to `awaiting_user_review`.)

Save Phase 5 checkpoint.

### Phase 6: Plan Export

Once approved:
1. Write the plan to `implementation_plan.md` (or user's preferred path)
2. Write the task list to `tasks.md` in machine-readable format
3. Recommend the user run `/rad-planner:generate-project-config` to create CLAUDE.md
4. Advise: "Start a fresh session for execution. Load implementation_plan.md and tasks.md. Work through tasks in dependency order, one milestone at a time."
5. Save Phase 6 checkpoint (terminal).

In `--non-interactive` mode, emit a trailing JSON block:
```json
{
  "plan_complete": true,
  "run_id": "string",
  "plan_path": "implementation_plan.md",
  "tasks_path": "tasks.md",
  "milestones": 0,
  "task_count": 0,
  "risk_verdict": "APPROVE | REVISE",
  "escalation_required": false,
  "awaiting_user_review": ["string"]
}
```

## Key References

These files contain the detailed templates and contracts. Load them as needed during planning:
- `references/plan-template.md` — Master plan structure (7 sections)
- `references/task-format.md` — Task states, dependency rules, complexity scoring
- `references/golden-path-matrix.md` — Tech stack evaluation criteria
- `references/anti-patterns.md` — 14 "Do Not Do" constraints
- `references/failure-state-template.md` — Triple-component validation
- `references/tdd-constraints.md` — Testing requirements per task
- `references/context-management.md` — Document & Clear protocol + checkpoint schema
- `references/claude-md-template.md` — Project config generation guide
- `references/subagent-prompts/stack-eval.md` — Stack-advisor dispatch template
- `references/subagent-prompts/risk-assessment.md` — Risk-assessor dispatch template
