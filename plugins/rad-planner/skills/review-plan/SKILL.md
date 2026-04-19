---
name: review-plan
description: >
  This skill should be used when the user says "review my plan", "audit this plan",
  "check my implementation plan", "is this plan complete", "what's missing from my plan",
  "validate my plan", "plan review", "check plan quality", "risk review", "check
  dependencies", "are there any risks in my plan", or has an existing implementation
  plan (plan.md, implementation_plan.md, tasks.md) that needs quality assessment
  before execution begins.
argument-hint: "[path to plan file] [--strict] [--non-interactive] [--resume <run-id>]"
user-invocable: true
allowed-tools: Read Glob Grep Agent Write
---

# Review Plan — Implementation Plan Quality Audit

Audit an existing implementation plan for completeness, anti-patterns, missing failure states, dependency integrity, and TDD compliance. This is the quality gate between planning and execution.

## Cross-model note

This skill works identically across Opus 4.7, Sonnet 4.6, and Haiku 4.5. Opus/Sonnet batch the plan-file reads and the risk-assessor reference loads in parallel. Haiku may follow the steps sequentially if parallel batching misbehaves. The risk-assessor JSON contract is identical regardless of model.

## Execution: parallel-first

- **Step 1 plan location** — if multiple candidate paths exist, Glob and Read them in a single parallel batch
- **Step 2 risk-assessor dispatch** — single agent call; the agent itself runs its audit passes with parallel reference loading
- **Step 3 additional checks** can run concurrently with interpreting the risk-assessor's JSON output, not sequentially

## Mode Flags

- `--strict` — Apply production-grade standards (see "Strict Mode" below)
- `--non-interactive` — Skip Step 5 fix-offer interaction. Emit verdict + unresolved issues as trailing JSON. Auto-proceed thresholds: `verdict: APPROVE` → exit clean; `verdict: REVISE` → emit issues without applying fixes; `verdict: RETHINK` → emit escalation routing.
- `--resume <run-id>` — Load `.planner/state/<run-id>.json` and continue from last saved step. Uses the shared checkpoint schema documented in `references/context-management.md`.

## Workflow

### 1. Locate the Plan

If a path was provided, read it directly. Otherwise, Glob for candidates in parallel:
- `implementation_plan.md`
- `PLAN.md`
- `plan.md`
- `tasks.md`
- `active-plan.md`
- Any `.md` file in `docs/plans/` or `plans/`

Read the plan file(s) completely. If multiple files exist (plan + tasks), read all of them in a single parallel batch.

Save Step 1 checkpoint to `.planner/state/<run-id>.json`.

### 2. Delegate to Risk Assessor

Use the Agent tool to delegate to the `risk-assessor` agent with the substituted template from `references/subagent-prompts/risk-assessment.md`. Pass the plan content, `iteration_number: 1`, and `max_iterations: 1` (this skill runs a single pass; the iterative loop is owned by `plan-project`).

Parse the returned JSON per the `risk-assessment.md` schema. Key fields:
- `verdict`: `APPROVE` | `REVISE` | `RETHINK`
- `blocking_issues[]`: CRITICAL/HIGH issues with fix suggestions
- `advisory_issues[]`: MEDIUM/LOW issues
- `escalation_required`: surfaced when the audit cannot produce a clean verdict

Save Step 2 checkpoint with the parsed JSON.

### 3. Additional Checks (Beyond Risk Assessment)

After parsing the risk assessor's report, also verify:

**Zero-Context Readiness:**
- Could a fresh AI session execute this plan with no prior conversation?
- Are all file paths explicit (not "the auth file" but `src/middleware/auth.ts`)?
- Are all commands runnable as-is (not "run the tests" but `npm test -- --grep auth`)?
- Are all external dependencies documented (environment variables, API keys, services)?

**Completeness:**
- Does every milestone have a checkpoint?
- Does every task have a Definition of Done?
- Are success criteria defined at the project level?
- Is the architecture documented (not just implied)?
- Are edge cases called out specifically?

**Formatting:**
- Are task states using valid syntax? (`[PENDING]`, `[IN PROGRESS]`, `[BLOCKED]`, `[DONE]`, `[VERIFIED]`)
- Are dependencies using task ID arrays? (`Dependencies: [S1, S2]`)
- Are complexity scores present for every task?
- Is the plan structured per the 7-section template?

### 4. Present Results

Output a structured review, merging the risk-assessor JSON with the additional checks:

```markdown
# Plan Review Report

**Plan:** [filename]
**Review mode:** [standard | strict]
**Overall Quality:** [score /10]
**Verdict:** APPROVE | REVISE | RETHINK

## Strengths
- [What the plan does well]

## Critical Issues (Block execution until fixed)
- [Issue with specific fix recommendation]

## Improvements (Recommended before execution)
- [Issue with fix]

## Optional Enhancements
- [Nice-to-have improvements]

## Completeness Checklist
- [x] Project summary and success criteria
- [x] Architecture documented
- [ ] Target files listed ← MISSING
- [x] Dependencies mapped
[...]

## Escalation
[Only present if verdict=RETHINK — recommend /rad-brainstormer:design-sprint]
```

### 5. Offer Fixes (interactive only)

If `verdict` is `REVISE` and not `--non-interactive`, offer to fix the identified issues directly in the plan file. For each fix:
- Explain what you're changing and why
- Show the before/after
- Only modify the plan document — never create implementation files

If `verdict` is `RETHINK`, do NOT offer fixes. Instead surface: "This plan has fundamental architectural issues that task-level fixes won't resolve. Re-enter via `/rad-brainstormer:design-sprint` to rework the architecture, then return here for re-review."

In `--non-interactive` mode, emit a trailing JSON block and exit:

```json
{
  "review_complete": true,
  "run_id": "string",
  "plan_path": "string",
  "verdict": "APPROVE | REVISE | RETHINK",
  "blocking_issue_count": 0,
  "advisory_issue_count": 0,
  "escalation_required": false,
  "escalation_route": "",
  "awaiting_user_review": ["string"]
}
```

## Strict Mode (`--strict`)

When `--strict` is specified, apply production-grade standards:
- Every task MUST have validation AND rollback (no exceptions)
- Coverage targets MUST be specified per task
- Security review checkpoints MUST exist for auth/payment/data tasks
- Context management plan MUST include specific clear points
- All external API integrations MUST have error handling in the task spec

In strict mode, the risk-assessor treats any MEDIUM issue in these categories as HIGH.
