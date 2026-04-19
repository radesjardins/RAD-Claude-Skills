# rad-planner

Structured coding project planner for Claude Code that enforces dependency-aware planning, risk assessment, and stack intelligence before any code is written.

## What It Does

rad-planner guides you through a structured Explore → Plan → Review → Approve workflow before any code is written. It produces dependency-aware implementation plans in Markdown and JSON that are designed to be picked up by a fresh AI session without needing the original conversation context.

The core problem it addresses: AI agents that start coding without a plan tend to encounter conflicts, lose architectural coherence as context windows fill, and spiral into correction loops. Planning first — with explicit dependencies, validation checks, and failure handling — reduces this risk substantially.

## Design Approach

Built from research across a curated AI Code Review knowledge base (15 structured queries) and analysis of existing planning tools (GSD, Deep Plan, Claude Spec, BMAD, Task Master, Blueprint, Kiro, and others). The design prioritizes:

- **Dependency-aware task graphs** — tasks mapped as a DAG with explicit `blockedBy` arrays, complexity scoring (1-10), and parallel execution waves. Tasks above complexity 7 must be broken into subtasks.
- **Failure state templates** — the plan template requires each task to define a validation check (runnable command), rollback procedure, and definition of done. Whether the generated plan actually achieves this depends on the quality of the planning session.
- **Stack evaluation with live verification** — a Golden Path matrix ranks frameworks by AI code generation accuracy across 4 tiers. The stack-advisor agent uses Context7 and web search to verify current versions rather than relying on training data alone.
- **14 documented anti-patterns** — extracted from the knowledge base covering specific failure modes (context rot, fallback traps, test editing, stale APIs, etc.), not generic advice like "write clean code."
- **Context management** — the checkpoint skill implements a Document & Clear protocol: dump session state to a handoff file, clear the context, and resume in a fresh session. This addresses the well-documented degradation of AI reasoning as context windows fill.
- **TDD integration** — each task in the plan template includes a test strategy field specifying what to test, what to mock, edge cases, and coverage targets.

## Skills

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `/rad-planner:plan-project` | "plan my project", "create implementation plan" | Full 5-phase planning workflow |
| `/rad-planner:evaluate-stack` | "what stack should I use", "recommend a stack" | AI-native tech stack evaluation |
| `/rad-planner:review-plan` | "review my plan", "audit this plan" | Quality audit of existing plans |
| `/rad-planner:generate-project-config` | "generate CLAUDE.md", "setup project files" | Generate CLAUDE.md + reference files |
| `/rad-planner:checkpoint` | "checkpoint", "save progress", "document and clear" | Preserve state for context reset |

## Agents

| Agent | Role | Triggers |
|-------|------|----------|
| **plan-architect** | Lead orchestrator — read-only exploration, strategic questions, plan drafting | Invoked by plan-project skill |
| **stack-advisor** | Tech stack evaluation using Golden Path matrix + live verification | Invoked by evaluate-stack skill or plan-architect |
| **risk-assessor** | Anti-pattern detection, failure state coverage, TDD compliance review | Invoked by review-plan skill or plan-architect |

## When to Use This vs rad-brainstormer

`rad-planner` and [`rad-brainstormer`](../rad-brainstormer/) are designed to chain, not compete. They own different phases of the idea → ship pipeline:

| Phase | Plugin | Owns | Output |
|-------|--------|------|--------|
| **Ideation** (divergent) | `rad-brainstormer` | Exploring the problem, generating options, stress-testing assumptions, converging on a direction | A decided idea + rough direction |
| **Design** (post-ideation) | `rad-brainstormer:design-sprint` | Architecture, components, data flow, API design, error handling, testing strategy | A reviewable design spec |
| **Planning** (pre-code) | `rad-planner:plan-project` | Dependency-aware task graph, complexity scoring, parallel waves, risk audit, failure states | An ordered implementation plan |
| **Code** | your tools of choice | Implementation | Working software |

**The boundary that matters:** `design-sprint` answers *"what are we building and how is it shaped?"* (spec). `plan-project` answers *"in what order do we build it, what could go wrong, and how do we know each step is done?"* (plan).

**If you come in with a clear idea**, start here with `/rad-planner:plan-project`. **If the idea is still fuzzy** or you haven't settled on an approach, start with `/rad-brainstormer:brainstorm-session` first — then hand off to this plugin once the direction is locked. For non-trivial projects, running both in sequence is usually worth it.

## Reference Files

The `references/` directory contains the knowledge base that agents and skills load on demand:

| Reference | Content |
|-----------|---------|
| `golden-path-matrix.md` | AI-native proficiency tiers + project-type stack recommendations |
| `anti-patterns.md` | 14 documented "Do Not Do" constraints |
| `plan-template.md` | Master Implementation Plan structure (7 sections) |
| `task-format.md` | DAG-based task syntax, states, dependency rules, complexity scoring |
| `failure-state-template.md` | Triple-component validation (Action → Validation → Rollback) |
| `tdd-constraints.md` | Red-Green-Refactor + mutation testing requirements |
| `claude-md-template.md` | WHY/WHAT/HOW template for CLAUDE.md generation |
| `context-management.md` | Document & Clear triggers, handoff protocol, shared checkpoint schema |
| `subagent-prompts/stack-eval.md` | JSON-first dispatch template for `stack-advisor` |
| `subagent-prompts/risk-assessment.md` | JSON-first dispatch template for `risk-assessor` |

## What's New in 2.0

Platform-level optimization pass for Opus 4.7 (Sonnet 4.6 and Haiku 4.5 fully supported):

- **Opus-default on all three agents.** `plan-architect`, `stack-advisor`, and `risk-assessor` all run on Opus 4.7 by default. Sonnet 4.6 is a first-class fallback per agent; Haiku 4.5 for narrow-scope use.
- **JSON-first subagent output contracts.** `stack-advisor` and `risk-assessor` emit structured JSON matching schemas at `references/subagent-prompts/{stack-eval,risk-assessment}.md`. Dispatching skills parse the JSON authoritatively; markdown fallback remains for model variance.
- **Externalized subagent prompt templates** at plugin-level `references/subagent-prompts/` (multi-skill-plugin pattern — shared across `plan-project`, `review-plan`, `evaluate-stack`).
- **`--non-interactive` mode** on `plan-project`, `review-plan`, `evaluate-stack`, and `generate-project-config` for agent/CI callers that deadlock on interactive menus. Auto-proceed thresholds documented per skill.
- **`--resume <run-id>` + shared checkpoint schema** at `.planner/state/<run-id>.json`. Long planning runs survive compaction; the `checkpoint` skill writes the same format that the three multi-phase skills read via `--resume`.
- **Parallel-first execution guidance** in every multi-phase skill — codebase exploration reads, reference file loads, and independent subagent dispatches batch into single tool-call bursts.
- **Escalation path to brainstormer.** When `risk-assessor` returns `RETHINK` or `stack-advisor` sets `escalation_required`, the dispatching skill surfaces `/rad-brainstormer:design-sprint` as the re-entry point rather than looping on patches that can't fix architectural problems.
- **Flattened agent layout** — `agents/<name>/AGENT.md` → `agents/<name>.md` to match every other plugin in the repo.
- **Honest claims audit** across references — unsourced specific statistics softened to honest language about direction and magnitude.

## Quick Start

1. Start a new Claude Code session
2. Run `/rad-planner:plan-project` with your project description
3. Answer the strategic discovery questions
4. Review the generated plan and approve
5. Start a fresh session for execution with the approved plan

## The Planning Workflow

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Discovery   │───▶│  Stack Eval  │───▶│  Planning   │
│ (Questions)  │    │ (Golden Path)│    │ (DAG Tasks) │
└─────────────┘    └──────────────┘    └─────────────┘
                                              │
┌─────────────┐    ┌──────────────┐           │
│   Export     │◀───│   Review     │◀──────────┘
│ (Plan Files) │    │ (Risk Audit) │
└─────────────┘    └──────────────┘
```

## What Gets Generated

After the planning workflow completes:

- `implementation_plan.md` — The master plan with 7 sections
- `tasks.md` — Machine-readable task list with dependency graph
- `CLAUDE.md` — Project configuration (via generate-project-config)
- `ARCHITECTURE.md` — Component diagram and design decisions
- `HANDOFF.md` — Session state for context management (via checkpoint)

## License

Apache-2.0
