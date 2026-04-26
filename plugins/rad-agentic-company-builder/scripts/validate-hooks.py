#!/usr/bin/env python3
"""
validate-hooks.py — Validate Claude Code hook configurations against the real
documented event list (April 2026).

Why this exists: the previous version of this plugin shipped configs referencing
fictional hook events (PostToolUseFailure, SubagentStart, Setup, InstructionsLoaded).
This script catches those before users wonder why their hooks never fire.

Usage:
  python3 validate-hooks.py <path-to-settings.json>
  python3 validate-hooks.py <path-to-dir-containing-settings.json>
  python3 validate-hooks.py <root> --recursive
  python3 validate-hooks.py <root> --json

Exit codes:
  0  all hook events valid
  1  one or more invalid / fictional events found
  2  script error (file not found, parse failure)

Pure stdlib Python 3.8+.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Verified against Claude Code documentation — April 2026.
# Source: https://docs.claude.com/en/docs/claude-code/hooks
REAL_EVENTS = {
    "PreToolUse": {
        "fires": "Before a tool executes",
        "matcher_supported": True,
        "exit_2_blocks": True,
    },
    "PostToolUse": {
        "fires": "After a tool succeeds",
        "matcher_supported": True,
        "exit_2_blocks": False,  # cannot block; tool already executed
    },
    "UserPromptSubmit": {
        "fires": "When user submits a prompt",
        "matcher_supported": False,
        "exit_2_blocks": True,
    },
    "SessionStart": {
        "fires": "Session begins or resumes from compact",
        "matcher_supported": True,  # optional 'compact' matcher
        "exit_2_blocks": False,
    },
    "SessionEnd": {
        "fires": "Session ends",
        "matcher_supported": False,
        "exit_2_blocks": False,
    },
    "Stop": {
        "fires": "Agent about to stop",
        "matcher_supported": False,
        "exit_2_blocks": True,  # can prevent stop — guard against infinite loops
    },
    "SubagentStop": {
        "fires": "Sub-agent completes",
        "matcher_supported": False,
        "exit_2_blocks": False,
    },
    "PreCompact": {
        "fires": "Before context compaction",
        "matcher_supported": False,
        "exit_2_blocks": False,
    },
    "Notification": {
        "fires": "Agent sends notification (permission_prompt, idle_prompt, auth_success, elicitation_dialog)",
        "matcher_supported": False,
        "exit_2_blocks": False,
    },
    "PermissionRequest": {
        "fires": "Permission prompt appears",
        "matcher_supported": False,
        "exit_2_blocks": False,
    },
    "ConfigChange": {
        "fires": "Settings file modified",
        "matcher_supported": False,
        "exit_2_blocks": False,
    },
    "WorktreeCreate": {
        "fires": "Git worktree created",
        "matcher_supported": False,
        "exit_2_blocks": False,
    },
    "WorktreeRemove": {
        "fires": "Git worktree removed",
        "matcher_supported": False,
        "exit_2_blocks": False,
    },
    # Agent Teams (experimental — fires only when CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1):
    "TeammateIdle": {
        "fires": "Agent Teams: teammate about to go idle (experimental)",
        "matcher_supported": False,
        "exit_2_blocks": True,  # exit 2 keeps teammate working
        "experimental": True,
    },
    "TaskCompleted": {
        "fires": "Agent Teams: task being marked complete (experimental)",
        "matcher_supported": False,
        "exit_2_blocks": True,  # exit 2 prevents completion
        "experimental": True,
    },
}

# Events that prior plugin versions mistakenly listed but don't exist.
# Kept here so we can give a specific "you probably meant X" suggestion.
KNOWN_FICTIONAL = {
    "PostToolUseFailure": "Use PostToolUse and inspect tool result for failure",
    "SubagentStart": "Not a documented event — there is no pre-hook for sub-agent spawn",
    "Setup": "Not a documented hook event",
    "InstructionsLoaded": "Not a documented event — CLAUDE.md loading is not hookable",
    "TaskCreated": "Not in main hooks reference; only mentioned in Agent Teams docs — verify before relying on it",
}


def find_settings_files(target: Path, recursive: bool) -> list[Path]:
    if target.is_file():
        return [target]
    if target.is_dir():
        if recursive:
            return sorted(target.rglob(".claude/settings.json"))
        candidate = target / ".claude" / "settings.json"
        if candidate.exists():
            return [candidate]
        candidate = target / "settings.json"
        if candidate.exists():
            return [candidate]
    return []


def validate_one(path: Path) -> list[dict]:
    issues: list[dict] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [{"severity": "CRITICAL", "path": str(path), "message": "file not found"}]
    except json.JSONDecodeError as e:
        return [{"severity": "CRITICAL", "path": str(path), "message": f"invalid JSON: {e}"}]

    hooks = data.get("hooks") if isinstance(data, dict) else None
    if not isinstance(hooks, dict):
        return [{
            "severity": "LOW",
            "path": str(path),
            "message": "no 'hooks' object found — nothing to validate",
        }]

    for event_name, handlers in hooks.items():
        if event_name in REAL_EVENTS:
            spec = REAL_EVENTS[event_name]
            # Lightweight handler-shape check
            if not isinstance(handlers, list):
                issues.append({
                    "severity": "HIGH",
                    "path": str(path),
                    "event": event_name,
                    "message": f"hooks.{event_name} should be an array of handler entries",
                    "fix": "Wrap in [...] — see Claude Code hooks reference for the exact shape",
                })
                continue
            # If experimental, note it but don't error
            if spec.get("experimental"):
                issues.append({
                    "severity": "LOW",
                    "path": str(path),
                    "event": event_name,
                    "message": f"'{event_name}' is experimental (Agent Teams) — fires only with CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1",
                    "fix": "OK if you've explicitly enabled Agent Teams; remove if you haven't",
                })
            # Stop-with-exit-2 sanity (can create infinite loops)
            if event_name == "Stop":
                for entry in handlers:
                    if not isinstance(entry, dict):
                        continue
                    cmds = entry.get("hooks", [])
                    if isinstance(cmds, list):
                        for c in cmds:
                            if isinstance(c, dict) and "exit 2" in str(c.get("command", "")):
                                issues.append({
                                    "severity": "MEDIUM",
                                    "path": str(path),
                                    "event": event_name,
                                    "message": "Stop hook can exit 2 — without guard logic this loops indefinitely",
                                    "fix": "Add a counter / sentinel file so the hook eventually allows the stop",
                                })
            continue

        if event_name in KNOWN_FICTIONAL:
            issues.append({
                "severity": "HIGH",
                "path": str(path),
                "event": event_name,
                "message": f"'{event_name}' is not a documented Claude Code hook event",
                "fix": KNOWN_FICTIONAL[event_name],
            })
        else:
            issues.append({
                "severity": "HIGH",
                "path": str(path),
                "event": event_name,
                "message": f"'{event_name}' is not in the documented Claude Code hook event list",
                "fix": f"Check spelling. Real events: {', '.join(sorted(REAL_EVENTS))}",
            })

    return issues


def render_text(report: dict) -> str:
    lines: list[str] = []
    lines.append(f"validate-hooks: {report['files_checked']} settings.json file(s) inspected")
    issues = report["issues"]
    if not issues:
        lines.append("OK — all hook events reference documented Claude Code events.")
        return "\n".join(lines)

    by_severity: dict[str, list[dict]] = {}
    for i in issues:
        by_severity.setdefault(i["severity"], []).append(i)

    lines.append("")
    lines.append(
        f"Issues: {len(issues)} total — "
        + ", ".join(f"{sev}: {len(by_severity[sev])}" for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW") if sev in by_severity)
    )
    for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        for i in by_severity.get(sev, []):
            label = f"[{i.get('event', '-')}]"
            lines.append(f"  {sev} {label} {i['path']}")
            lines.append(f"      {i['message']}")
            if i.get("fix"):
                lines.append(f"      fix: {i['fix']}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", help="Path to a settings.json or a directory")
    p.add_argument("--recursive", "-r", action="store_true", help="Recursively find all .claude/settings.json under the directory")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = p.parse_args(argv)

    target = Path(args.path).resolve()
    if not target.exists():
        print(f"error: not found: {target}", file=sys.stderr)
        return 2

    files = find_settings_files(target, args.recursive)
    if not files:
        print(f"error: no settings.json files found under {target}", file=sys.stderr)
        return 2

    all_issues: list[dict] = []
    for f in files:
        all_issues.extend(validate_one(f))

    report = {
        "files_checked": len(files),
        "issues": all_issues,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_text(report))

    return 1 if all_issues else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
