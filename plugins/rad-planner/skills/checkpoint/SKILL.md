---
name: checkpoint
description: >
  This skill should be used when the user says "checkpoint", "save progress",
  "document and clear", "dump context", "save state", "prepare to clear", "session
  handoff", "wrap up this session", "context is getting long", "I need to clear",
  "save my work", "handoff", "I need to switch tasks", "before I close",
  or when the conversation is approaching context limits and work needs to be
  preserved before clearing the session. Also trigger proactively when detecting
  signs of context degradation (repeated suggestions, vague responses, hallucinated
  file paths).
argument-hint: "[--plan path/to/plan.md] [--phase current-phase-name] [--run-id <id>]"
user-invocable: true
allowed-tools: Read Glob Grep Write Bash
---

# Checkpoint — Document & Clear Context Management

Preserve the current session state so work can be resumed in a fresh session without loss. This implements the "Document & Clear" pattern that prevents context rot — the degradation of AI reasoning quality as context windows fill.

Checkpoint at milestone boundaries, after 2 consecutive failures, or when context degradation signs appear (vague responses, hallucinated paths, correction loops). See `references/context-management.md` for the full trigger matrix and the shared checkpoint schema.

## Cross-model note

This skill works identically across Opus 4.7, Sonnet 4.6, and Haiku 4.5. The git state capture and handoff file generation are deterministic; parallel Reads of the plan file plus `git status` / `git log` are independent and should be batched.

## Execution: parallel-first

Step 1's reads — implementation plan file, `git status`, `git log --oneline -5`, `git rev-parse --abbrev-ref HEAD` — are all independent. Batch into a single parallel burst. Only serialize when Step 3's plan update requires the prior read's contents.

## Checkpoint Workflow

### Step 1: Assess Current State (parallel batch)

Read the implementation plan (if one exists) and run git commands in parallel. Capture:
- What phase/milestone are we in?
- Which tasks are completed, in progress, or blocked?
- What files were modified in this session?
- Are there any uncommitted changes?
- Current branch, recent commits, ahead/behind vs. remote

### Step 2: Generate Handoff Document

Write a `HANDOFF.md` file (or update existing one) following the handoff template in `references/context-management.md`. The handoff must include:
- Current phase and milestone
- Last completed task and next task
- Files changed this session with current state
- Git status (branch, committed/uncommitted, recent commit hash)
- Completed and in-progress tasks
- Open decisions needing human input
- **Traps** — approaches that failed and must NOT be retried (TRIED / FAILED BECAUSE / CORRECT APPROACH format)
- **Resume instructions** — exact steps for a fresh session to continue

### Step 3: Write Planner State File (if run-id is available)

If `--run-id <id>` is provided, or if a prior `plan-project` / `review-plan` / `evaluate-stack` run is in progress, write/update the planner state file at `.planner/state/<run-id>.json` per the shared schema in `references/context-management.md`. This lets the next session resume the specific skill that was in flight via `--resume <run-id>`, not just the general HANDOFF.md.

The shared schema allows the `plan-project`, `review-plan`, and `evaluate-stack` skills to all use the same state file format — different `skill` values, same structure.

### Step 4: Update the Plan

If an implementation plan exists, update task states:
- Mark completed tasks as `[DONE]` or `[VERIFIED]`
- Mark the current task as `[IN PROGRESS]`
- Update any dependency states that changed

### Step 5: Recommend Next Steps

Tell the user:

```
Checkpoint complete. State saved to HANDOFF.md[ and .planner/state/<run-id>.json].

To continue in a fresh session:
1. Start a new Claude Code session (or run /clear)
2. Say: "Read HANDOFF.md and resume from where I left off"
   OR if a run-id was saved: "/rad-planner:plan-project --resume <run-id>"
3. The fresh session will have a clean context window

If you want to continue in this session instead, that's fine —
but be aware that context quality may degrade as the session gets longer.
```

## What Gets Preserved

| What | Where | Why |
|------|-------|-----|
| Session progress | HANDOFF.md | Resume without loss |
| Active skill run state | `.planner/state/<run-id>.json` | Resume specific skill via `--resume` |
| Task states | implementation_plan.md / tasks.md | Track completion |
| Failed approaches | HANDOFF.md "Traps" section | Prevent repeating mistakes |
| Open decisions | HANDOFF.md | Don't lose context on unresolved questions |
| Git state | HANDOFF.md | Know what's committed vs. uncommitted |

## What Does NOT Get Preserved

- The full conversation history (that's the point — we're clearing it)
- Intermediate reasoning or exploration results (externalize important findings)
- Temporary debugging context (capture only the solution, not the journey)

## Key Reference

Load `references/context-management.md` for the full Document & Clear protocol, trigger conditions, context budget rules, handoff document template, and the shared checkpoint schema used by `plan-project`, `review-plan`, and `evaluate-stack`.
