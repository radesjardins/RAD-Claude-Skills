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
argument-hint: "[--plan path/to/plan.md] [--phase current-phase-name]"
user-invocable: true
allowed-tools: Read Glob Grep Write Bash
---

# Checkpoint — Document & Clear Context Management

Preserve the current session state so work can be resumed in a fresh session without loss. This implements the "Document & Clear" pattern that prevents context rot — the degradation of AI reasoning quality as context windows fill.

Checkpoint at milestone boundaries, after 2 consecutive failures, or when context degradation signs appear (vague responses, hallucinated paths, correction loops). See `references/context-management.md` for the full trigger matrix.

## Checkpoint Workflow

### Step 1: Assess Current State

Read the implementation plan (if one exists) and determine:
- What phase/milestone are we in?
- Which tasks are completed, in progress, or blocked?
- What files were modified in this session?
- Are there any uncommitted changes?

Run `git status` and `git log --oneline -5` using Bash to capture the current state of the working tree, branch, and recent commits.

### Step 2: Generate Handoff Document

Write a `HANDOFF.md` file (or update existing one) following the handoff template in `references/context-management.md`. The handoff must include:
- Current phase and milestone
- Last completed task and next task
- Files changed this session with current state
- Git status (branch, committed/uncommitted, recent commit hash)
- Completed and in-progress tasks
- Open decisions needing human input
- **Traps** — approaches that failed and must NOT be retried (with reasons)
- **Resume instructions** — exact steps for a fresh session to continue

### Step 3: Update the Plan

If an implementation plan exists, update task states:
- Mark completed tasks as `[DONE]` or `[VERIFIED]`
- Mark the current task as `[IN PROGRESS]`
- Update any dependency states that changed

### Step 4: Recommend Next Steps

Tell the user:

```
Checkpoint complete. State saved to HANDOFF.md.

To continue in a fresh session:
1. Start a new Claude Code session (or run /clear)
2. Say: "Read HANDOFF.md and resume from where I left off"
3. The fresh session will have a clean 200K token context

If you want to continue in this session instead, that's fine —
but be aware that context quality may degrade as the session gets longer.
```

## What Gets Preserved

| What | Where | Why |
|------|-------|-----|
| Session progress | HANDOFF.md | Resume without loss |
| Task states | implementation_plan.md / tasks.md | Track completion |
| Failed approaches | HANDOFF.md "Traps" section | Prevent repeating mistakes |
| Open decisions | HANDOFF.md | Don't lose context on unresolved questions |
| Git state | HANDOFF.md | Know what's committed vs. uncommitted |

## What Does NOT Get Preserved

- The full conversation history (that's the point — we're clearing it)
- Intermediate reasoning or exploration results (externalize important findings)
- Temporary debugging context (capture only the solution, not the journey)

## Key Reference

Load `references/context-management.md` for the full Document & Clear protocol, trigger conditions, context budget rules, and handoff document template.
