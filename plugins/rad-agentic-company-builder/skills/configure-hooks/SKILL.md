---
name: configure-hooks
description: This skill should be used when the user says "configure hooks", "set up quality gates", "add TaskCompleted hook", "configure PostToolUse hook", "set up permission hooks", "create hook configuration", "add typecheck hook", "set up test-on-complete hook", or wants to configure event-driven hooks and quality gates for their agentic company project.
argument-hint: "[--project path/to/project/repo] [--hooks quality-gates,typecheck-on-edit,format-on-write]"
user-invocable: true
---

# Configure Hooks and Quality Gates

Set up deterministic enforcement hooks for an agentic company project. Unlike CLAUDE.md instructions which Claude may interpret loosely, hooks execute external commands that mechanically block or allow agent actions.

## Core Concept

Hooks are configured in `.claude/settings.json`. They fire on specific events and their exit codes control behavior:
- **Exit 0** — Proceed (stdout added to context for some events)
- **Exit 2** — Block the action (stderr becomes feedback to Claude)
- **Any other exit** — Logged as error, does not block

## Standard Hook Patterns

### Quality Gate: TaskCompleted

The most critical hook. Runs typecheck and tests when an agent marks a task complete. Blocks completion if either fails:

```json
{
  "hooks": {
    "TaskCompleted": [{
      "hooks": [{
        "type": "command",
        "command": "cd \"$CLAUDE_PROJECT_DIR\" && npm run typecheck 2>&1 | tail -20; TC=$?; npm test 2>&1 | tail -30; TEST=$?; if [ $TC -ne 0 ] || [ $TEST -ne 0 ]; then echo 'BLOCKED: Type check or tests failed. Fix before completing.' >&2; exit 2; fi",
        "timeout": 120
      }]
    }]
  }
}
```

### Typecheck on Edit: PostToolUse

Warns (but does not block) when a Write or Edit introduces TypeScript errors:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "cd \"$CLAUDE_PROJECT_DIR\" && npm run typecheck 2>&1 | tail -5; if [ $? -ne 0 ]; then echo 'Warning: TypeScript errors introduced by this edit.' >&2; fi; exit 0",
        "timeout": 30
      }]
    }]
  }
}
```

### Context Restoration After Compaction: SessionStart

Re-injects critical context after automatic compaction:

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "compact",
      "hooks": [{
        "type": "command",
        "command": "echo 'Reminder: Current sprint focus is [SPRINT_GOAL]. Use the project agents for implementation.'"
      }]
    }]
  }
}
```

## Configuration Process

### Step 1: Determine Target

Find the project's `.claude/settings.json`. If it exists, read current content and merge. If not, create it.

### Step 2: Select Hook Patterns

Present available patterns. If `$ARGUMENTS` specifies hooks, use those. Standard options:

| Pattern | Event | Behavior |
|---------|-------|----------|
| **quality-gates** | TaskCompleted | Block completion if tests/typecheck fail |
| **typecheck-on-edit** | PostToolUse (Write\|Edit) | Warn on TypeScript errors after edits |
| **format-on-write** | PostToolUse (Write\|Edit) | Auto-format with Prettier after writes |
| **secret-scan** | PreToolUse (Write\|Edit) | Scan for secrets in content about to be written |
| **compact-restore** | SessionStart (compact) | Re-inject context after compaction |

### Step 3: Customize Commands

Adjust commands for the project's tech stack:
- `npm run typecheck` -> `pnpm typecheck` or `mypy app/`
- `npm test` -> `pytest` or `bun test`
- Timeout values based on project test suite speed

### Step 4: Generate Configuration

Merge hook configuration into `.claude/settings.json`, preserving any existing permissions and settings.

### Step 5: Add Agent Teams Support (Optional)

If Agent Teams is enabled, add:
- **TeammateIdle** hook to auto-assign follow-up tasks
- **TaskCompleted** hook for team task validation
- Enable experimental flag: `"env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" }`

### Step 6: Document and Warn

Inform the user about important hook behaviors:
- `matcher` is a **case-sensitive regex** against tool names
- All matching hooks run in **parallel** with configurable timeout
- Stop hooks with exit 2 can create infinite loops — guard logic is essential
- Hook exit code 2 means "block and feedback", not "error"

## Additional Resources

### Reference Files

- **`references/hook-patterns.md`** — Advanced hook patterns including secret scanning, auto-formatting, Agent Teams hooks, and common pitfalls
