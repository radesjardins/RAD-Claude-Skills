# Context Management: Document & Clear Protocol

AI reasoning quality degrades as context windows fill. This isn't a theoretical concern -- it's the primary failure mode in long coding sessions. The planner must proactively manage context to prevent "hallucination entropy."

## The Document & Clear Pattern

### Step 1: Status Checkpoint (Dump)
Before clearing, instruct the AI to write a handoff document capturing:
- **Completed milestones** -- what's done and verified
- **Current state** -- what files were modified, what's in progress
- **Open decisions** -- unresolved questions that need human input
- **Traps to avoid** -- approaches that were tried and failed
- **Immediate next steps** -- exactly what to do when resuming

Save to: `HANDOFF.md`, `activeContext.md`, or `SCRATCHPAD.md`

### Step 2: Wipe
Run `/clear` to completely reset the session. This erases all conversational context.

### Step 3: Rehydration
Start a fresh session. Point the AI to:
1. The saved handoff document
2. The master plan (`PLAN.md` or `implementation_plan.md`)
3. Any committed changes in the Git branch
4. The project's CLAUDE.md for conventions

The AI now operates with a pristine context window, focused only on the next phase of work.

## Trigger Conditions

### Mandatory Triggers (Always clear)
| Condition | Why |
|-----------|-----|
| **Task transitions** | Moving between unrelated features prevents context bleed |
| **Milestone completion** | Natural boundary; commit, celebrate, reset |
| **After 2 consecutive failures** | Context is polluted with failed approaches; fresh start needed |
| **Major topic change** | Database refactoring context should never bleed into UI work |

### Warning Triggers (Clear soon)
| Condition | Why |
|-----------|-----|
| **Approaching 60% context capacity** | Reasoning quality begins degrading at 20-40% |
| **Agent starts repeating itself** | Sign of attention mechanism losing earlier instructions |
| **Responses getting vague** | Model losing grip on specific details |
| **Unexpected suggestions** | AI proposing things outside the plan scope |

### Critical Trigger (Clear immediately)
| Condition | Why |
|-----------|-----|
| **Agent stuck in correction loop** | 2+ failed attempts = polluted context. STOP. Clear. Restart. |
| **Auto-compaction triggered** | At ~83.5% capacity, AI silently summarizes history -- lossy and unpredictable |
| **Agent hallucinating file paths or APIs** | Confidence in non-existent code = context corruption |

## Context Budget Rules

### Session Duration
- **Target:** 30-45 minute focus sessions
- **Maximum:** One bounded task per session
- **Rule:** Better to clear too early than too late

### What to Keep in Active Context
- The current phase of the plan (not the entire plan)
- Files being actively modified (not the whole codebase)
- Relevant test files for the current task
- The task's validation criteria and rollback procedure

### What to Externalize
- Completed work summaries (commit to git, reference in handoff)
- Architecture decisions (store in `decisions.md`)
- Stack/library choices (store in `CLAUDE.md`)
- Test strategies (store in `TESTING.md`)
- Full project plan (store in `PLAN.md`, load only current phase)

## Dynamic Context Loading

Instead of hardwiring everything into CLAUDE.md (burns tokens on every message), store detailed references in separate files and load them on demand:

```markdown
## References (load when needed)
@docs/ARCHITECTURE.md — Read when: modifying system architecture
@docs/API.md — Read when: adding or modifying API endpoints
@references/golden-path-matrix.md — Read when: evaluating tech stack choices
```

This "progressive disclosure" pattern keeps the active context lean while making deep knowledge available when needed.

## Handoff Document Template

```markdown
# Session Handoff — [Date] [Time]

## Status
**Phase:** [Current phase name]
**Milestone:** [M1/M2/etc.]
**Last completed task:** [Task ID and title]
**Next task:** [Task ID and title]

## What Changed This Session
- [File 1]: [What was done]
- [File 2]: [What was done]
- Committed as: [commit hash or "uncommitted"]

## Open Decisions
- [ ] [Decision needed about X — context: Y]

## Traps (Do NOT Retry)
- [Approach A failed because B — do not attempt again]

## To Resume
1. Read this file
2. Read PLAN.md, focus on Phase [N]
3. Start with task [ID]: [title]
4. Run `[validation command]` to verify current state
```

## Integration with Plan Checkpoints

The plan template includes checkpoints after every milestone. Each checkpoint should:
1. Run all validation checks for completed tasks
2. Commit all verified work to git
3. Generate/update the handoff document
4. Assess context usage (are we near 60%?)
5. If context is high: dump state, recommend `/clear`, provide rehydration instructions
6. If context is low: continue to next phase
