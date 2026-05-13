# rad-planner

Structured implementation-planning scaffolding for Claude Code, with **mechanical validators** (Python scripts) backing the parts that templates alone can't enforce.

## What this actually is

A 6-skill plugin that walks you through Discovery → Stack Eval → Plan → Risk → Review → Export, dispatches subagents for stack and risk work, and runs Python validators on the generated artifacts. The plan output is markdown intended for a fresh AI session to pick up cold.

The skills are mostly structured prompts that ask the model to behave like a planner. The **scripts** in `scripts/` are real validators — they parse the generated tasks file, build the DAG, check for cycles and phantom dependencies, verify required fields are present, flag vague language, and validate subagent JSON against schemas. Where the README says "enforced," the script does the work.

## File conventions

rad-planner produces project-level planning artifacts per the [RAD 8-doc standard](../../docs/file-conventions.md) at the repository root. The standard is the canonical convention shared with rad-session: it defines target lengths, update triggers, pruning rules, and the single-writer rule that prevents collision between plugins.

## What it does NOT do

- **Does not execute the resulting plan.** It produces planning artifacts. You (or another tool) run the work.
- **Does not test that a plan is "zero-context ready."** That's the *intent* of the templates, not a verified property.
- **Does not detect every anti-pattern.** Mechanical checks cover field presence, DAG integrity, and vague language. Anti-patterns 1, 9, 11, 13 (judgment-required) are still checked by the risk-assessor agent — and several of those are opinions with thresholds, not laws.
- **Does not stop you from skipping phases.** Phase order is enforced by instructions to the model, not by code.
- **Does not auto-checkpoint or auto-clear context.** The checkpoint skill writes a handoff file; you run `/clear` and rehydrate yourself.
- **Does not track planning quality over time.** No metrics, no learning from prior plans.
- **Does not replace Claude Code's built-in Plan Mode** — it adds artifacts on top of it. See "Relationship to built-in Plan Mode" below.

## Skills

| Skill | Trigger | What it produces |
|---|---|---|
| `/rad-planner:plan-project` | "plan my project", "create implementation plan" | Full 6-phase workflow → `implementation_plan.md` + `tasks.md` + `EXECUTION-PROMPT.md`. Supports `--lite` for small work. |
| `/rad-planner:evaluate-stack` | "what stack should I use", "recommend a stack" | Stack recommendation table with live version verification. Standalone or as Phase 2 of plan-project. |
| `/rad-planner:review-plan` | "review my plan", "audit this plan" | Quality audit combining mechanical lint + judgment review. |
| `/rad-planner:status` | "plan status", "what's next", "where am I in the plan" | Quick read of an in-flight plan: % complete, blocked tasks, next eligible. |
| `/rad-planner:generate-project-config` | "generate CLAUDE.md", "setup project files" | Generates CLAUDE.md + ARCHITECTURE.md from an approved plan. |
| `/rad-planner:checkpoint` | "checkpoint", "save progress", "document and clear" | Writes HANDOFF.md + `.planner/state/<run-id>.json`. User runs `/clear` separately. |

Honest note: `evaluate-stack` and `review-plan` are also exposed as standalone skills, but they re-use the same agents (`stack-advisor`, `risk-assessor`) that `plan-project` invokes during its phases. Treat them as direct entry points for those phases, not separate functionality.

## Agents

| Agent | Role | Model |
|---|---|---|
| **plan-architect** | Lead orchestrator — read-only exploration, strategic questions, plan drafting | Opus 4.7 default, Sonnet 4.6 fallback |
| **stack-advisor** | Tech stack evaluation, live version checks via Context7/WebSearch | Opus 4.7 default, Sonnet 4.6 fallback |
| **risk-assessor** | Anti-pattern judgment, architecture concerns, TDD strategy quality. Calls `plan-lint.py` first to skip mechanical checks. | Opus 4.7 default, Sonnet 4.6 fallback |

## Mechanical validators (scripts/)

The validators are what convert "we enforce DAG integrity" from aspiration to fact.

### `scripts/plan-lint.py`

Pure-Python (3.8+ stdlib only). Modes:

| Mode | Catches |
|---|---|
| `dag` | Multi-hop cycles, phantom dependencies (`Dependencies: [S99]` where S99 doesn't exist), complexity > 7 without subtasks |
| `checklist` | Missing required fields (Validation, Rollback, Dependencies, Complexity), vague language ("verify it works", "looks right", "tbd") |
| `status` | Task state report — % complete, state breakdown, blocked tasks, next-eligible by dependency |
| `all` | dag + checklist |

Output: human-readable text or `--json` for machine consumption. Exit `0` clean, `1` issues found, `2` script error.

### `scripts/validate-json.py`

Validates JSON output (from subagents) against JSON Schema files at `references/subagent-prompts/*.schema.json`. Pure stdlib; uses the `jsonschema` package if installed for fuller draft-07 coverage.

Used by skills to validate subagent contracts before consuming them — re-prompts the agent once on schema failure rather than silently parsing whatever came back.

### `scripts/README.md`

Full invocation docs and the table of which skill / agent calls which script when.

## Relationship to built-in Plan Mode

Claude Code ships with [Plan Mode](https://docs.claude.com/en/docs/claude-code/) (Shift+Tab toggle, `--permission-mode plan`) which restricts to read-only tools. rad-planner does not replace it; the two compose:

- **Plan Mode** handles read-only enforcement at the runtime level (no Edit/Write/Bash).
- **rad-planner** adds structured artifacts on top: a 7-section plan template, a DAG, a risk audit, an executor handoff manifest, and a checkpoint schema.

You can run `/rad-planner:plan-project` inside Plan Mode for runtime-level read-only guarantees — the skill will still produce all its planning artifacts via the Write tool (which is required to save the plan).

## Pipeline with rad-brainstormer

`rad-planner` and [`rad-brainstormer`](../rad-brainstormer/) chain. They own different phases:

| Phase | Plugin | Owns | Output |
|---|---|---|---|
| **Ideation** (divergent) | `rad-brainstormer` | Exploring the problem, generating options, stress-testing assumptions | A decided idea + rough direction |
| **Design** (post-ideation) | `rad-brainstormer:design-sprint` | Architecture, components, data flow, API design, error handling, testing strategy | A reviewable design spec |
| **Planning** (pre-code) | `rad-planner:plan-project` | Dependency-aware task graph, complexity scoring, risk audit, failure states | An ordered implementation plan |
| **Code** | your tools of choice | Implementation | Working software |

If you come in with a clear idea, start with `/rad-planner:plan-project`. If the idea is fuzzy, start with `/rad-brainstormer:brainstorm-session` first.

## Reference Files

The `references/` directory contains the knowledge base agents and skills load on demand:

| Reference | Content |
|---|---|
| `golden-path-matrix.md` | AI-native proficiency tiers + project-type stack recommendations (date-stamped, opinionated) |
| `anti-patterns.md` | 14 documented "Do Not Do" constraints (some are opinions with thresholds — clearly marked) |
| `plan-template.md` | Master Implementation Plan structure (7 sections) with a "what enforces what" table |
| `task-format.md` | DAG-based task syntax, states, dependency rules, complexity scoring |
| `failure-state-template.md` | Triple-component validation (Action → Validation → Rollback) |
| `tdd-constraints.md` | Red-Green-Refactor + mutation testing requirements |
| `claude-md-template.md` | WHY/WHAT/HOW template for CLAUDE.md generation |
| `context-management.md` | Document & Clear triggers, handoff protocol, shared checkpoint schema |
| `subagent-prompts/stack-eval.md` + `.schema.json` | Stack-advisor dispatch template + JSON Schema |
| `subagent-prompts/risk-assessment.md` + `.schema.json` | Risk-assessor dispatch template + JSON Schema |

## Examples

`examples/example-plan.md` and `examples/example-tasks.md` are a complete (small) plan that passes the validators. Use them to:
- See what `plan-project` actually produces (not just templates).
- Run the validators against a real artifact: `python3 scripts/plan-lint.py --mode all examples/example-tasks.md`.
- Test the validator failure modes by introducing a cycle or stripping a field.

## What's New in 2.1

- **`scripts/plan-lint.py`** — Mechanical DAG + checklist + status validator. Converts "we enforce DAG integrity" from claim to mechanism.
- **`scripts/validate-json.py`** — JSON Schema validator for subagent output contracts. Skills now re-prompt on schema failure instead of silently falling back to markdown parsing.
- **JSON Schema files** at `references/subagent-prompts/{stack-eval,risk-assessment}.schema.json` — Concrete contract, not just documentation.
- **`/rad-planner:status` skill** — Quick read of in-flight plan progress, blocked tasks, next eligible.
- **`--lite` flag on `plan-project`** — Single-milestone workflow for small/bug-fix work, skips stack eval + risk-assessor loop, still runs `plan-lint.py`.
- **`EXECUTION-PROMPT.md` artifact** — Phase 6 now generates a copy-pasteable kickoff prompt for the next session, not just "start a fresh session and load the plan."
- **Risk-assessor calls `plan-lint.py` first** — Mechanical checks are deterministic; the agent's judgment is reserved for anti-pattern, architecture, and TDD-quality passes scripts can't do.
- **Honesty pass across the README and references** — "Enforces" softened to "guides" or "validates" depending on actual mechanism. "Zero-context ready" now framed as the intent, not a verified property. Anti-pattern #1 (Vector Sidecar) reframed from dogmatic ban to threshold-based default.
- **Date-stamped Golden Path matrix** with explicit "trust live verification over the matrix when they disagree" guidance.
- **`examples/`** — A real, validator-clean plan + tasks file ships with the plugin.

## What's New in 2.0 (prior release)

Platform-level optimization pass for Opus 4.7 (Sonnet 4.6 and Haiku 4.5 fully supported):

- **Opus-default on all three agents.** Sonnet 4.6 is a first-class fallback; Haiku 4.5 for narrow scope.
- **JSON-first subagent output contracts** with markdown fallback for model variance. (2.1 made these enforced via `validate-json.py`.)
- **Externalized subagent prompt templates** at plugin-level `references/subagent-prompts/`.
- **`--non-interactive` mode** on `plan-project`, `review-plan`, `evaluate-stack`, `generate-project-config`.
- **`--resume <run-id>` + shared checkpoint schema** at `.planner/state/<run-id>.json`.
- **Parallel-first execution guidance** in every multi-phase skill.
- **Escalation path to brainstormer** on `RETHINK` verdict.
- **Flattened agent layout** to `agents/<name>.md`.
- **Honest claims audit** across references — first pass; 2.1 extends this throughout.

## Quick Start

1. Start a new Claude Code session.
2. Run `/rad-planner:plan-project` with your project description (add `--lite` for small work).
3. Answer the strategic discovery questions.
4. Review the generated plan and approve.
5. Start a fresh session for execution — load `EXECUTION-PROMPT.md`.

For an existing plan: `/rad-planner:review-plan path/to/plan.md` for a quality audit, or `/rad-planner:status path/to/tasks.md` for a quick progress read.

## The Planning Workflow

```
┌───────────┐  ┌────────────┐  ┌─────────┐  ┌─────────┐  ┌────────────┐
│ Discovery │→ │ Stack Eval │→ │  Plan   │→ │  Risk   │→ │   Review   │
└───────────┘  └────────────┘  └─────────┘  └─────────┘  └────────────┘
                                                              ↓
                                              ┌──────────────────────────┐
                                              │ Export: plan + tasks +   │
                                              │ EXECUTION-PROMPT (with   │
                                              │ plan-lint validation)    │
                                              └──────────────────────────┘
```

`--lite` collapses Stack Eval and Risk into a single Plan→Lint→Review pass.

## What Gets Generated

After the planning workflow completes:

- `implementation_plan.md` — Master plan with 7 sections
- `tasks.md` — Machine-readable task list with dependency graph
- `EXECUTION-PROMPT.md` — Copy-pasteable kickoff for the next session
- `CLAUDE.md` — Project configuration (via `/rad-planner:generate-project-config`)
- `ARCHITECTURE.md` — Component diagram and design decisions (via `generate-project-config`)
- `HANDOFF.md` — Session state for context management (via `/rad-planner:checkpoint`)
- `.planner/state/<run-id>.json` — Resumable run state (via `--resume`)

## Requirements

- **Python 3.8+** for the validator scripts. If unavailable, the skills surface a fallback: manual review using the documented checklists. The honest framing is that without Python, the "validators" reduce to "templates the model is asked to follow."
- Optional: `pip install jsonschema` for fuller JSON Schema draft-07 coverage in `validate-json.py`. Pure-stdlib subset is used when not installed.

## License

Apache-2.0
