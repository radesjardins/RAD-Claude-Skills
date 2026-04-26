# Additional Hook Patterns

Documented Claude Code hook events as of April 2026. The `validate-hooks.py` script catches anything not in this list.

## All documented hook events

| Event | When It Fires | Matcher? | Exit 2 blocks? |
|---|---|---|---|
| `PreToolUse` | Before a tool executes | Yes (tool name; exact match unless regex chars) | Yes |
| `PostToolUse` | After a tool succeeds | Yes | No (tool already executed) |
| `UserPromptSubmit` | When user submits a prompt | No | Yes |
| `SessionStart` | Session begins or resumes from compact | Yes (`compact`) | No |
| `SessionEnd` | Session ends | No | No |
| `Stop` | Agent about to stop | No | Yes (loop risk) |
| `SubagentStop` | Sub-agent completes | No | No |
| `PreCompact` | Before context compaction | No | No |
| `Notification` | permission_prompt, idle_prompt, auth_success, elicitation_dialog | No | No |
| `PermissionRequest` | Permission dialog appears | No | No |
| `ConfigChange` | Settings file modified | No | No |
| `WorktreeCreate` | Git worktree created | No | No |
| `WorktreeRemove` | Git worktree removed | No | No |
| `TeammateIdle` *(Agent Teams, experimental)* | Teammate going idle | No | Yes (keeps working) |
| `TaskCompleted` *(Agent Teams, experimental)* | Task being marked complete | No | Yes (prevents completion) |

## Events that DON'T exist (common mistakes)

| Wrong name | What people probably meant |
|---|---|
| `PostToolUseFailure` | Use `PostToolUse` and inspect the tool result for failure |
| `SubagentStart` | No equivalent — there is no pre-spawn hook |
| `Setup` | Not a hook event — installation runs once outside the hook lifecycle |
| `InstructionsLoaded` | CLAUDE.md loading is not hookable |
| `TaskCreated` | Not in main hooks reference; check Agent Teams docs before relying on it |

The `validate-hooks.py` script catches all of these and suggests the closest valid alternative.

---

## Auto-format on write

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "cd \"$CLAUDE_PROJECT_DIR\" && npx prettier --write \"$TOOL_INPUT_FILE\" 2>/dev/null; exit 0",
        "timeout": 10
      }]
    }]
  }
}
```

Always `exit 0` — format failures shouldn't block writes.

---

## Secret scan (PreToolUse, blocking)

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "echo \"$TOOL_INPUT_CONTENT\" | grep -iE '(api[_-]?key|secret|password|token|credential)\\s*[=:]\\s*[\"'\\'']?[A-Za-z0-9+/]{20,}' && echo 'BLOCKED: possible secret detected' >&2 && exit 2 || exit 0",
        "timeout": 5
      }]
    }]
  }
}
```

This is a heuristic. False positives are normal (long base64 strings in test fixtures, etc.). Tune the regex for your codebase or add an allow-list directory.

---

## Quality gate on TaskCompleted (Agent Teams, experimental)

```json
{
  "hooks": {
    "TaskCompleted": [{
      "hooks": [{
        "type": "command",
        "command": "cd \"$CLAUDE_PROJECT_DIR\" && npm run typecheck 2>&1 | tail -20; TC=$?; npm test 2>&1 | tail -30; TEST=$?; if [ $TC -ne 0 ] || [ $TEST -ne 0 ]; then echo 'BLOCKED: typecheck or tests failed' >&2; exit 2; fi",
        "timeout": 120
      }]
    }]
  }
}
```

Only fires when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set in your environment or settings.json.

---

## Stop hook with sentinel guard

Unguarded `exit 2` on Stop creates infinite loops. This pattern allows N continuation cycles, then exits cleanly:

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "COUNT=$(cat /tmp/stop-count 2>/dev/null || echo 0); if [ $COUNT -ge 3 ]; then rm -f /tmp/stop-count; exit 0; fi; echo $((COUNT+1)) > /tmp/stop-count; echo 'Continuing — '$((3-COUNT))' more cycles' >&2; exit 2",
        "timeout": 5
      }]
    }]
  }
}
```

The sentinel file ensures the loop has a bound. The `validate-hooks.py` script flags Stop hooks with `exit 2` and no obvious guard so you can confirm the pattern is intentional.

---

## Context restoration after compact

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "compact",
      "hooks": [{
        "type": "command",
        "command": "cat .claude/post-compact-context.md 2>/dev/null || echo 'Reminder: continue with current sprint priorities.'"
      }]
    }]
  }
}
```

Useful when long sessions get auto-compacted and you want to re-inject critical context (current task, branch, etc.) before the agent continues.

---

## Hook execution model (verified April 2026)

- **Multiple hooks for the same event run in parallel.** Each handler entry can specify its own `timeout` (default 600 seconds).
- **Matcher behavior:** exact string match for plain values (`"Bash"`), regex when special characters are present (`"Edit|Write"`, `"^Notebook"`, `"mcp__.*"`).
- **Environment variables available in commands:** `$CLAUDE_PROJECT_DIR`, `$TOOL_NAME`, and tool-specific vars like `$TOOL_INPUT_FILE` for Write/Edit.
- **Exit codes:** `0` proceed, `2` block (where supported — see event table), anything else logged as non-blocking error.

## When NOT to use hooks

- Don't use a hook to enforce something a CLAUDE.md instruction handles fine. Hooks are for what cannot be left to the model's judgment.
- Don't add a slow hook to a high-frequency event (`PostToolUse` fires on every tool call). 30-second hooks on `PostToolUse` will make every action sluggish.
- Don't use `Stop` with `exit 2` without a guard. Always.
