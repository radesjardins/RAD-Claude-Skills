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
argument-hint: "[project description or existing codebase path]"
user-invocable: true
allowed-tools: Read Glob Grep WebSearch WebFetch Agent Write
---

# Plan Project — Structured Implementation Planning

You are orchestrating a complete project planning workflow. Your goal is to produce a zero-context-ready implementation plan that prevents the "vibe coding doom loop" — where AI agents write code without a plan, encounter conflicts, and spiral into endless correction loops.

**CRITICAL: You are in PLANNING MODE. Do NOT write implementation code. Do NOT create source files. You produce planning artifacts ONLY.**

## Workflow

### Phase 1: Strategic Discovery

**If the user provided a project description:**
1. Summarize your understanding of the project
2. Ask 3-5 high-information strategic questions (NOT implementation details):
   - "What's the most important thing this system must get right?"
   - "What's the biggest technical risk you see?"
   - "Who are the target users and what's their primary workflow?"
   - "What existing systems does this need to integrate with?"
   - "What are the hard constraints? (timeline, team, infrastructure)"
3. Wait for answers before proceeding

**If in an existing codebase:**
1. Explore the codebase structure: read CLAUDE.md, README, package.json, key config files
2. Map the directory structure and understand current architecture
3. Identify patterns, conventions, and integration points
4. Present findings to the user and ask clarifying questions

### Phase 2: Stack Evaluation

Use the Agent tool to delegate to the `stack-advisor` agent:
- For new projects: provide the project context and request a full stack recommendation
- For existing projects: provide the codebase details and ask whether the current stack supports the planned work
- The stack-advisor will verify current versions via web search and Context7

If Context7 MCP is available, use it to fetch current documentation for the recommended frameworks. If not, use WebSearch to verify framework versions and features.

Present the stack recommendation to the user. Incorporate their feedback.

### Phase 3: Build the Plan

Load `references/plan-template.md` for the required structure.

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

Load `references/task-format.md` for task state syntax and dependency rules.
Load `references/anti-patterns.md` and verify no task triggers a known anti-pattern.

### Phase 4: Risk Assessment

Use the Agent tool to delegate to the `risk-assessor` agent with the draft plan:
- Anti-pattern scan (14 constraints)
- Failure state coverage check
- Dependency graph integrity
- TDD compliance
- Context management assessment

Incorporate findings. Fix critical and high issues before presenting to the user.

### Phase 5: Plan Review & Approval

Present to the user:
1. **Executive summary** — milestones, task count, complexity distribution, estimated risk level
2. **Architecture overview** — component diagram, key decisions
3. **Full task list** — with dependencies, validation, and rollback for each
4. **Risk report** — any remaining concerns and mitigations
5. **Context management plan** — when to checkpoint and clear

**Ask the user explicitly: "Does this plan look correct? Should I adjust anything before we lock it in?"**

The plan is NOT approved until the user says so.

### Phase 6: Plan Export

Once approved:
1. Write the plan to `implementation_plan.md` (or user's preferred path)
2. Write the task list to `tasks.md` in machine-readable format
3. Recommend the user run `/rad-planner:generate-project-config` to create CLAUDE.md
4. Advise: "Start a fresh session for execution. Load implementation_plan.md and tasks.md. Work through tasks in dependency order, one milestone at a time."

## Key References

These files contain the detailed templates and constraints. Load them as needed during planning:
- `references/plan-template.md` — Master plan structure (7 sections)
- `references/task-format.md` — Task states, dependency rules, complexity scoring
- `references/golden-path-matrix.md` — Tech stack evaluation criteria
- `references/anti-patterns.md` — 14 "Do Not Do" constraints
- `references/failure-state-template.md` — Triple-component validation
- `references/tdd-constraints.md` — Testing requirements per task
- `references/context-management.md` — Document & Clear protocol
- `references/claude-md-template.md` — Project config generation guide
