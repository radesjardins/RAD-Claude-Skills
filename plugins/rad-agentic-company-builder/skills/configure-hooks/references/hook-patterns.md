# Advanced Hook Patterns

## All Supported Hook Events

| Event | When It Fires | Matcher? |
|-------|---------------|----------|
| PreToolUse | Before a tool executes | Yes — tool name regex |
| PostToolUse | After a tool succeeds | Yes — tool name regex |
| PostToolUseFailure | After a tool fails | Yes — tool name regex |
| UserPromptSubmit | When user submits a prompt | No |
| SessionStart | Session begins or resumes from compact | Yes — "compact" |
| SessionEnd | Session ends | No |
| Stop | Agent about to stop | No |
| SubagentStart | Sub-agent spawns | No |
| SubagentStop | Sub-agent completes | No |
| PreCompact | Before context compaction | No |
| Notification | Agent sends notification | No |
| PermissionRequest | Permission prompt appears | No |
| Setup | Plugin setup | No |
| TeammateIdle | Agent Teams: teammate idle | No |
| TaskCompleted | Agent Teams: task marked complete | No |
| ConfigChange | Settings file modified | No |
| WorktreeCreate | Git worktree created | No |
| WorktreeRemove | Git worktree removed | No |
| InstructionsLoaded | CLAUDE.md file loaded | No |

---

## Auto-Format on Write

```json
{
  "PostToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "cd \"$CLAUDE_PROJECT_DIR\" && npx prettier --write \"$TOOL_INPUT_FILE\" 2>/dev/null; exit 0",
      "timeout": 10
    }]
  }]
}
```

Note: Always `exit 0` to avoid blocking writes on format failures.

---

## Secret Scanning Pre-Write

```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "echo \"$TOOL_INPUT_CONTENT\" | grep -iE '(api[_-]?key|secret|password|token|credential)\\s*[=:]\\s*[\"'\\']?[A-Za-z0-9+/]{20,}' && echo 'BLOCKED: Possible secret detected in file content.' >&2 && exit 2 || exit 0",
      "timeout": 5
    }]
  }]
}
```

---

## Agent Teams: Quality Gate on Task Completion

```json
{
  "TaskCompleted": [{
    "hooks": [{
      "type": "command",
      "command": "cd \"$CLAUDE_PROJECT_DIR\" && npm run typecheck 2>&1 | tail -20; TC=$?; npm test 2>&1 | tail -30; TEST=$?; if [ $TC -ne 0 ] || [ $TEST -ne 0 ]; then echo 'BLOCKED: Type check or tests failed. Fix before completing task.' >&2; exit 2; fi",
      "timeout": 120
    }]
  }]
}
```

---

## Agent Teams: Keep Teammates Working

```json
{
  "TeammateIdle": [{
    "hooks": [{
      "type": "command",
      "command": "echo 'Check the task list for pending items. If no pending tasks, report status to the team lead.' >&2; exit 2",
      "timeout": 5
    }]
  }]
}
```

---

## Final Lint Check Before Session Ends

```json
{
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "cd \"$CLAUDE_PROJECT_DIR\" && npm run lint 2>&1 | tail -10; if [ $? -ne 0 ]; then echo 'Lint errors remain. Consider fixing before ending session.' >&2; exit 2; fi",
      "timeout": 30
    }]
  }]
}
```

**Warning:** Stop hooks with exit 2 can create infinite loops if the agent has no corrective action. Add guard logic or use exit 0 with a warning instead.

---

## Complete settings.json with All Patterns

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run dev)",
      "Bash(npm run build)",
      "Bash(npm test)",
      "Bash(npm run test:*)",
      "Bash(npm run lint)",
      "Bash(npm run typecheck)",
      "Bash(npx prisma *)",
      "Bash(npx playwright *)",
      "Bash(git *)"
    ],
    "deny": [
      "Bash(npx prisma migrate deploy)",
      "Bash(npm publish *)",
      "Bash(rm -rf *)",
      "Read(.env)",
      "Read(.env.*)",
      "Read(secrets/**)"
    ]
  },
  "hooks": {
    "TaskCompleted": [{
      "hooks": [{
        "type": "command",
        "command": "cd \"$CLAUDE_PROJECT_DIR\" && npm run typecheck 2>&1 | tail -20; TC=$?; npm test 2>&1 | tail -30; TEST=$?; if [ $TC -ne 0 ] || [ $TEST -ne 0 ]; then echo 'BLOCKED: Type check or tests failed.' >&2; exit 2; fi",
        "timeout": 120
      }]
    }],
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "cd \"$CLAUDE_PROJECT_DIR\" && npm run typecheck 2>&1 | tail -5; if [ $? -ne 0 ]; then echo 'Warning: TypeScript errors.' >&2; fi; exit 0",
        "timeout": 30
      }]
    }]
  },
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```
