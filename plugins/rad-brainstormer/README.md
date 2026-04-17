# rad-brainstormer — A thinking partner that knows when to diverge and when to decide.

Brainstorming alone loops back to the same ideas. rad-brainstormer brings 10 proven methodologies — SCAMPER, Six Thinking Hats, Five Whys, reverse brainstorming, design sprints — into a structured session with autonomous agents that research your domain, stress-test your assumptions, and review your specs for completeness. Works for software features, business strategy, product decisions, content, and anything else you need to think through clearly.

## What You Can Do With This

- Run a guided brainstorm on a new feature — diverge broadly, then converge to a decision
- Use Five Whys to find the real root cause of a recurring problem
- Do a design sprint to go from vague idea to reviewable spec in one session
- Stress-test your plan with a pre-mortem before you build

## How It Works

| Skill | Purpose |
|-------|---------|
| `brainstorm-session` | Facilitated session with structured divergent/convergent phases |
| `idea-generation` | Generate diverse ideas using multiple creative techniques |
| `idea-evaluation` | Evaluate and prioritize ideas with structured criteria |
| `creative-unblock` | Break through blocks with lateral thinking techniques |
| `scamper` | SCAMPER — Substitute, Combine, Adapt, Modify, Put to other uses, Eliminate, Reverse |
| `six-hats` | Six Thinking Hats — explore all perspectives systematically |
| `reverse-brainstorm` | Make the problem worse to find what's actually causing it |
| `five-whys` | Root cause analysis — ask why until you hit the real issue |
| `how-might-we` | Reframe problems as opportunity statements |
| `design-sprint` | Structured spec creation and architecture design — hands off to `/rad-planner:plan-project` for implementation planning |

| Agent | Purpose |
|-------|---------|
| `domain-researcher` | Research any topic — landscape, approaches, constraints, recent innovations |
| `idea-challenger` | Pre-mortem analysis — feasibility, desirability, viability stress-test |
| `spec-reviewer` | Review design specs for completeness, consistency, and implementation readiness |

## When to Use This vs rad-planner

`rad-brainstormer` and [`rad-planner`](../rad-planner/) are designed to chain, not compete. They own different phases of the idea → ship pipeline:

| Phase | Plugin | Owns | Output |
|-------|--------|------|--------|
| **Ideation** (divergent) | `rad-brainstormer` | Exploring the problem, generating options, stress-testing assumptions, converging on a chosen direction | A decided idea + rough direction |
| **Design** (post-ideation) | `rad-brainstormer:design-sprint` | Architecture, components, data flow, API design, error handling, testing strategy | A reviewable design spec |
| **Planning** (pre-code) | `rad-planner:plan-project` | Dependency-aware task graph, complexity scoring, parallel waves, risk audit, failure states | An ordered implementation plan |
| **Code** | your tools of choice | Implementation | Working software |

**The boundary that matters:** `design-sprint` answers *"what are we building and how is it shaped?"* (spec). `plan-project` answers *"in what order do we build it, what could go wrong, and how do we know each step is done?"* (plan). Use both if the project is non-trivial.

If you come in with a clear idea already and just need a plan, skip `brainstormer` and go straight to `rad-planner:plan-project`. If you come in with a vague problem, start with `brainstorm-session`.

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-brainstormer
```

> **Using Claude.ai instead of CLI?** See [`skills/rad-brainstormer/`](../../skills/rad-brainstormer/) for the Claude.ai skill version — a single ZIP covering 3 consolidated workflows, with domain research via web search and deliverables as artifacts.

Then just say:

```
Let's brainstorm
I need ideas for X
Run a design sprint for this feature
Do a Five Whys on why this keeps happening
Help me evaluate these three options
```

## License
Apache-2.0
