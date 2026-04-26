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
argument-hint: "[project description or existing codebase path] [--lite] [--non-interactive] [--resume <run-id>]"
user-invocable: true
allowed-tools: Read Glob Grep WebSearch WebFetch Agent Write Bash
---

# Plan Project — Structured Implementation Planning

You are orchestrating a project planning workflow. The goal is an implementation plan a fresh AI session can pick up and execute without the original conversation context. Whether the plan actually achieves that depends on the quality of the planning session — this skill provides scaffolding and mechanical checks, not guarantees.

**CRITICAL: You are in PLANNING MODE. Do NOT write implementation code. Do NOT create source files. Produce planning artifacts ONLY.**

## What this skill does — honestly

- Walks you through a 6-phase workflow (Discovery → Stack → Plan → Risk → Review → Export).
- Dispatches subagents for stack evaluation and risk assessment with JSON output contracts.
- Runs `scripts/plan-lint.py` to mechanically check the generated tasks.md for cycles, phantom dependencies, missing required fields, vague validation language, and complexity-7+ tasks without subtasks. **This is real validation, not a model self-check.**
- Runs `scripts/validate-json.py` against the subagent JSON contracts before consuming them; re-prompts the agent once on schema failure.
- Saves run state to `.planner/state/<run-id>.json` so a long planning session can be resumed.

## What this skill does NOT do

- Does not execute the resulting plan.
- Does not test that the plan is actually "zero-context ready" — that label is the goal of the templates, not a verified property.
- Does not detect every anti-pattern; the mechanical checks cover field presence, DAG integrity, and vague language. The risk-assessor agent handles judgment-required anti-patterns and architectural concerns.
- Does not stop you skipping phases. The phase order is enforced by instructions to the model, not by code.

## Cross-model note

This skill works across Opus 4.7, Sonnet 4.6, and Haiku 4.5. Opus/Sonnet handle parallel batching reliably; Haiku may follow phase order sequentially. The plan output, JSON contracts, and validator scripts are identical regardless of model.

## Execution: parallel-first

- **Phase 1 codebase exploration** has no inter-file dependencies when the project exists. Issue parallel Reads for `CLAUDE.md`, `README.md`, `package.json`, `tsconfig.json` (or language-equivalent config), plus a Glob of the top-level directory structure.
- **Phase 3 reference loading** (`plan-template.md`, `task-format.md`, `anti-patterns.md`, `failure-state-template.md`, `tdd-constraints.md`, `context-management.md`) has no inter-file dependencies — single parallel batch.
- **Phase 2 and Phase 4 subagent dispatches** are independent of each other only when Phase 2 is complete before Phase 3 begins.
- **Always serialize:** user-approval gates and the discovery → stack → plan → risk → review phase order.

## Mode Flags

- `--lite` — Skip Phase 2 (stack eval) and the iterative risk-assessor loop. For small, single-milestone work (bug fixes, single-feature additions touching ≤3 files). Produces a 5-10 task plan with the same per-task fields, but no architecture diagram or full risk audit. Auto-detected if the project description is short and clearly bounded; explicit flag overrides.
- `--non-interactive` — Skip all user-approval gates. Best-effort plan, commit artifacts, emit a trailing JSON block listing `awaiting_user_review` items. Auto-proceed thresholds: stack-advisor `verification_verified: true` with `confidence: high|medium` → proceed; risk-assessor `verdict: APPROVE` → proceed; any `RETHINK` verdict → halt regardless of mode and escalate.
- `--resume <run-id>` — Load checkpoint state from `.planner/state/<run-id>.json` and continue from the last saved phase.

## Checkpoint & Resume

Long planning runs are compaction-prone. Save state to `.planner/state/<run-id>.json` at these transitions:

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

The model has to remember to write the checkpoint at each transition — there is no hook that does it automatically. On `--resume <run-id>`, load the file, announce the phase you're resuming from, and continue.

## Workflow

### Phase 1: Strategic Discovery

**Pre-discovery scope check.** If the user's project idea is clearly fuzzy (still debating what to build, which approach, or whether the problem is the right one), recommend `/rad-brainstormer:brainstorm-session` or `/rad-brainstormer:design-sprint` and return here once the direction is locked. `plan-project` plans the *how/order*; it assumes the *what* is decided.

**Lite-mode auto-detect.** If the project description fits all of:
- Single feature or bug fix, ≤3 files affected
- No new dependencies / framework choices
- One milestone of work, estimated <1 day

…suggest `--lite` mode unless the user explicitly wants the full workflow.

**If the user provided a project description:**
1. Summarize your understanding.
2. Ask 3-5 high-information strategic questions (NOT implementation details):
   - "What's the most important thing this system must get right?"
   - "What's the biggest technical risk you see?"
   - "Who are the target users and what's their primary workflow?"
   - "What existing systems does this need to integrate with?"
   - "What are the hard constraints? (timeline, team, infrastructure)"
3. Wait for answers (skip in `--non-interactive` — record unanswered questions in `awaiting_user_review`).

**If in an existing codebase:**
1. Issue parallel Reads for `CLAUDE.md`, `README.md`, `package.json`, `tsconfig.json` (or language equivalents), plus a Glob of the top-level structure.
2. Identify patterns, conventions, integration points.
3. Present findings and ask clarifying questions (skip in `--non-interactive`).

Save Phase 1 checkpoint.

### Phase 2: Stack Evaluation (skip in `--lite`)

Use the Agent tool to delegate to the `stack-advisor` agent using the substituted template from `references/subagent-prompts/stack-eval.md`. Pass `mode` (`new_project` | `evaluate_existing` | `compare_frameworks`) and `project_context`.

**After receiving the agent's output, validate the JSON contract:**

```bash
# Pipe the agent's output through the schema validator
echo "$AGENT_OUTPUT" | python3 ${plugin_root}/scripts/validate-json.py \
  ${plugin_root}/references/subagent-prompts/stack-eval.schema.json - --extract-from-markdown
```

If validation fails, re-prompt the agent once with: "Your last output failed JSON Schema validation: [errors]. Re-emit the JSON block matching `references/subagent-prompts/stack-eval.schema.json`." If the second attempt also fails, fall back to markdown parsing per the legacy structure in `agents/stack-advisor.md`.

Parse the validated JSON per the schema:
- `evaluation_complete: true` + `confidence: high|medium` → present recommendation to user (or auto-proceed in `--non-interactive`)
- `confidence: low` → surface risks to user before proceeding
- `escalation_required: true` → stop. Surface `escalation_reason` and recommend rethinking scope via brainstormer

Save Phase 2 checkpoint.

### Phase 3: Build the Plan

Load references in a single parallel batch: `plan-template.md`, `task-format.md`, `anti-patterns.md`, `failure-state-template.md`, `tdd-constraints.md`, `context-management.md`.

1. **Define milestones** — logical phases of work (3-6 milestones typical; 1-2 in `--lite`).
2. **Break into tasks** — each milestone becomes 3-8 specific tasks (lite: 5-10 tasks total, no milestone hierarchy required).
3. **Map dependencies** — explicit `Dependencies: [S1, S2]` for every task.
4. **Score complexity** — 1-10 per task; expand any task > 7 into subtasks.
5. **Define validation** — every task gets a runnable validation check.
6. **Define rollbacks** — every task gets a revert procedure.
7. **Set test strategy** — per `references/tdd-constraints.md`.
8. **Insert checkpoints** — after every milestone, per `references/failure-state-template.md`.
9. **Plan context management** — identify where to checkpoint/clear sessions per `references/context-management.md`.

**Mechanical validation (this is the part that's actually enforced):**

```bash
python3 ${plugin_root}/scripts/plan-lint.py --mode all <path-to-tasks.md> --json
```

The script returns issues for: cycles, phantom dependencies, complexity > 7 without subtasks, missing required fields (Validation, Rollback, Dependencies, Complexity), and vague validation language ("verify it works", "looks right", "tbd", etc.).

**If `plan-lint` reports CRITICAL or HIGH issues, fix them before proceeding to Phase 4.** Re-run until clean. The risk-assessor agent should not have to re-do work the script already covered.

Save Phase 3 checkpoint.

### Phase 4: Risk Assessment (skip in `--lite`)

Use the Agent tool to delegate to the `risk-assessor` agent using the substituted template from `references/subagent-prompts/risk-assessment.md`. The agent will also run `plan-lint.py` itself but should focus its judgment on the passes scripts can't cover (anti-patterns 1, 11, 13; architectural concerns; TDD strategy quality).

Pass the draft plan, current `iteration_number`, and `max_iterations` (default 3).

**Validate the agent's JSON output before consuming:**

```bash
echo "$AGENT_OUTPUT" | python3 ${plugin_root}/scripts/validate-json.py \
  ${plugin_root}/references/subagent-prompts/risk-assessment.schema.json - --extract-from-markdown
```

Re-prompt once on validation failure, then fall back to markdown parsing.

Parse the validated JSON per the schema:
- `verdict: APPROVE` → proceed to Phase 5
- `verdict: REVISE` and `iteration < max_iterations` → fix `blocking_issues`, increment iteration, re-dispatch. Save per-iteration checkpoint.
- `verdict: REVISE` and `iteration >= max_iterations` with issues remaining → stop looping. Surface `unresolved_issues` to user: "Risk assessment hit iteration cap. Decide: (a) accept these as known gaps, (b) drop back to Phase 3 and restructure the affected tasks yourself, or (c) re-enter via `/rad-brainstormer:design-sprint` if the architecture itself is the problem." In `--non-interactive`, add unresolved issues to `awaiting_user_review`.
- `verdict: RETHINK` → stop immediately regardless of iteration. Surface to user: "Risk assessment returned RETHINK. The architecture has fundamental issues that task-level patches won't fix. Re-enter via `/rad-brainstormer:design-sprint`." Set `escalation.required: true` and `escalation.route_to: "/rad-brainstormer:design-sprint"` in the checkpoint.

### Phase 5: Plan Review & Approval

Present to the user:
1. **Executive summary** — milestones, task count, complexity distribution, plan-lint result, estimated risk level.
2. **Architecture overview** — component diagram, key decisions (omitted in `--lite`).
3. **Full task list** — with dependencies, validation, and rollback for each.
4. **Risk report** — any remaining concerns and mitigations (omitted in `--lite`).
5. **Context management plan** — when to checkpoint and clear.

**Ask explicitly: "Does this plan look correct? Should I adjust anything before we lock it in?"**

The plan is NOT approved until the user says so. (In `--non-interactive`, skip approval and add "plan not reviewed by user" to `awaiting_user_review`.)

Save Phase 5 checkpoint.

### Phase 6: Plan Export

Once approved:
1. Write the plan to `implementation_plan.md` (or user's preferred path).
2. Write the task list to `tasks.md` in machine-readable format per `references/task-format.md`.
3. **Generate `EXECUTION-PROMPT.md`** — a copy-pasteable kickoff for the next session containing:
   - The first eligible task ID + its full spec
   - Validation command for that task
   - Rollback procedure
   - Pointer to the plan file for the rest
   - One-line instruction: "Start with [task ID]. Run validation when done. Mark `[VERIFIED]` and pick up the next eligible task via `/rad-planner:status`."
4. **Run `plan-lint.py --mode all`** one final time on the exported tasks.md. If clean, report it. If issues, surface them — the user has the choice to fix or accept.
5. Recommend the user run `/rad-planner:generate-project-config` to create CLAUDE.md.
6. Save Phase 6 checkpoint (terminal).

In `--non-interactive` mode, emit a trailing JSON block:
```json
{
  "plan_complete": true,
  "run_id": "string",
  "plan_path": "implementation_plan.md",
  "tasks_path": "tasks.md",
  "execution_prompt_path": "EXECUTION-PROMPT.md",
  "milestones": 0,
  "task_count": 0,
  "plan_lint_clean": true,
  "risk_verdict": "APPROVE | REVISE | not-run-in-lite",
  "escalation_required": false,
  "awaiting_user_review": ["string"]
}
```

## Lite Mode Workflow

For small, single-milestone work, the workflow collapses:

1. **Discovery** — 1-2 questions, not 5
2. **Skip Phase 2** (stack eval) — assume the existing stack
3. **Phase 3 plan** — 5-10 tasks, single milestone, no architecture diagram needed
4. **Skip Phase 4** (risk assessor) — but still run `plan-lint.py` for the mechanical checks
5. **Phase 5 review** — present and approve
6. **Phase 6 export** — same artifacts (plan, tasks, EXECUTION-PROMPT)

Lite mode trades the architectural review for speed. Use it when you'd otherwise be tempted to skip planning entirely. Don't use it when the work is novel, cross-cutting, or touches anything security/auth/payment.

## Key References

These contain the detailed templates and contracts. Load them as needed:
- `references/plan-template.md` — Master plan structure (7 sections)
- `references/task-format.md` — Task states, dependency rules, complexity scoring
- `references/golden-path-matrix.md` — Tech stack evaluation criteria
- `references/anti-patterns.md` — 14 documented anti-patterns
- `references/failure-state-template.md` — Triple-component validation
- `references/tdd-constraints.md` — Testing requirements per task
- `references/context-management.md` — Document & Clear protocol + checkpoint schema
- `references/claude-md-template.md` — Project config generation guide
- `references/subagent-prompts/stack-eval.md` — Stack-advisor dispatch template
- `references/subagent-prompts/risk-assessment.md` — Risk-assessor dispatch template
- `examples/example-plan.md` + `examples/example-tasks.md` — A real, validator-clean output
- `scripts/README.md` — Validator script documentation
