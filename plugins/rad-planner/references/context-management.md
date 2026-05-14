# Context Management: Document & Clear Protocol

AI reasoning quality tends to degrade as context windows fill — observable in longer coding sessions as repeated suggestions, hallucinated paths, and dropped instructions. The exact threshold and mechanism varies by model and workload; the directional effect is widely reported. The planner provides a Document & Clear protocol to mitigate this; the user (or a wrapping skill) must actually invoke `/clear` and rehydrate from the saved file.

## The Document & Clear Pattern

### Step 1: Status Checkpoint (Dump)

There are two complementary state files in the RAD 8-doc standard (3.0+). Use both for a full handoff:

**Planner-side (this plugin's job — `/checkpoint`):** write `.planner/state/<run-id>.json` per the shared checkpoint schema below. This captures:
- Which skill was in flight (`plan` / `review-plan` / `evaluate-stack`)
- Current phase, run-id, model, codebase context, stack recommendation, risk-history
- Whatever the skill needs to resume mid-flight via `--resume <run-id>`

**Session-side (rad-session's job — `/rad-session:wrapup`):** generate `HANDOFF.md` and append to `.claude/session-log.md`. This captures:
- What was tried and didn't work (TRIED / FAILED BECAUSE / CORRECT APPROACH traps)
- Where you left off, modified files, open work, key decisions, key insights
- The "what NOT to retry" record that the next `/rad-session:startup` reads

Per the single-writer rule (see `docs/doc-conventions.md` → canonical at `docs/doc-conventions.md`), **rad-planner does NOT write HANDOFF.md.** Run `/rad-session:wrapup` *before or after* `/rad-planner:checkpoint` if you want both kinds of state captured.

The two-step idiom is:
```
/rad-planner:checkpoint --run-id <id>    # saves .planner/state/<id>.json
/rad-session:wrapup                      # writes HANDOFF.md + session-log
/clear
```

For projects that aren't running a planner skill (just executing the plan), only `/rad-session:wrapup` is needed.

### Step 2: Wipe
Run `/clear` to completely reset the session. This erases all conversational context.

### Step 3: Rehydration
Start a fresh session. Point the AI to:
1. The saved handoff document
2. The master plan (`PLAN.md` in RAD 3.0+, or `implementation_plan.md` in v2.x legacy projects)
3. Any committed changes in the Git branch
4. The project's CLAUDE.md for conventions

If a `.planner/state/<run-id>.json` file exists for a skill that was in flight, use the skill's `--resume <run-id>` flag instead of re-orienting from scratch.

The AI now operates with a pristine context window, focused only on the next phase of work.

## Shared Checkpoint Schema

All three multi-phase skills (`plan`, `review-plan`, `evaluate-stack`) share a single state file format at `.planner/state/<run-id>.json`:

```json
{
  "run_id": "string",
  "skill": "plan | review-plan | evaluate-stack",
  "phase": "string — skill-specific phase identifier",
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

Skills may add skill-specific fields without breaking the shared contract — use additive extension, not renaming. The `checkpoint` skill can read and write this file generically by passing `--run-id`.

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
| **Approaching context capacity** | Reasoning quality begins degrading well before the hard limit |
| **Agent starts repeating itself** | Sign of attention mechanism losing earlier instructions |
| **Responses getting vague** | Model losing grip on specific details |
| **Unexpected suggestions** | AI proposing things outside the plan scope |

### Critical Trigger (Clear immediately)
| Condition | Why |
|-----------|-----|
| **Agent stuck in correction loop** | 2+ failed attempts = polluted context. STOP. Clear. Restart. |
| **Auto-compaction triggered** | The runtime silently summarizes history near capacity — lossy and unpredictable |
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

The canonical HANDOFF.md template is owned by rad-session, not rad-planner. See:
- `plugins/rad-session/references/handoff-template.md` for the format
- `docs/doc-conventions.md` for the per-section rules (length caps, "What NOT To Do" structure, etc.)

The `.planner/state/<run-id>.json` schema is documented above ("Shared Checkpoint Schema"). That's the only state file rad-planner writes directly.

## Integration with Plan Checkpoints

The plan template includes checkpoints after every milestone. Each checkpoint should:
1. Run all validation checks for completed tasks
2. Commit all verified work to git
3. Update `.planner/state/<run-id>.json` if a planner skill is in flight (rad-planner's responsibility)
4. Run `/rad-session:wrapup` if you want a session-level HANDOFF.md (rad-session's responsibility — keeps the single-writer rule intact)
5. Assess context usage — if approaching capacity, dump state, recommend `/clear`, provide rehydration instructions
6. If context is low: continue to next phase
