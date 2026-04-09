---
name: review-plan
description: >
  This skill should be used when the user says "review my plan", "audit this plan",
  "check my implementation plan", "is this plan complete", "what's missing from my plan",
  "validate my plan", "plan review", "check plan quality", "risk review", "check
  dependencies", "are there any risks in my plan", or has an existing implementation
  plan (plan.md, implementation_plan.md, tasks.md) that needs quality assessment
  before execution begins.
argument-hint: "[path to plan file] [--strict for production-grade review]"
user-invocable: true
allowed-tools: Read Glob Grep Agent
---

# Review Plan — Implementation Plan Quality Audit

Audit an existing implementation plan for completeness, anti-patterns, missing failure states, dependency integrity, and TDD compliance. This is the quality gate between planning and execution.

## Workflow

### 1. Locate the Plan

If a path was provided, read it directly. Otherwise, search for:
- `implementation_plan.md`
- `PLAN.md`
- `plan.md`
- `tasks.md`
- `active-plan.md`
- Any `.md` file in a `docs/plans/` or `plans/` directory

Read the plan file completely. If multiple files exist (plan + tasks), read all of them.

### 2. Delegate to Risk Assessor

Use the Agent tool to delegate to the `risk-assessor` agent with the plan content. Request a full 6-pass assessment:
1. Anti-pattern scan (14 constraints from `references/anti-patterns.md`)
2. Failure state coverage check
3. Dependency graph integrity (DAG validation)
4. TDD compliance check
5. Context management assessment
6. Stack and architecture review

### 3. Additional Checks (Beyond Risk Assessment)

After receiving the risk assessor's report, also verify:

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

Output a structured review:

```markdown
# Plan Review Report

**Plan:** [filename]
**Review mode:** [standard | strict]
**Overall Quality:** [score /10]

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

## Verdict: APPROVE | REVISE | RETHINK
```

### 5. Offer Fixes

If the user wants, offer to fix the identified issues directly in the plan file. For each fix:
- Explain what you're changing and why
- Show the before/after
- Only modify the plan document — never create implementation files

## Strict Mode (--strict)

When `--strict` is specified, apply production-grade standards:
- Every task MUST have validation AND rollback (no exceptions)
- Coverage targets MUST be specified per task
- Security review checkpoints MUST exist for auth/payment/data tasks
- Context management plan MUST include specific clear points
- All external API integrations MUST have error handling in the task spec
