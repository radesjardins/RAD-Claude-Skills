#!/usr/bin/env python3
"""
check-mcp-config.py — Validate .mcp.json structure and flag common configuration mistakes.

Catches:
  - JSON syntax errors
  - Missing top-level 'mcpServers' object
  - Servers with neither stdio (command/args) nor http (type+url)
  - Env var references in $VAR form (Claude Code expects ${VAR})
  - Hardcoded secrets (heuristic — flags long tokens, raw bearer headers, etc.)
  - Windows-incompatible npx invocations (will warn on Windows-only projects)
  - Optionally: env vars referenced but not currently set in the user's shell

Usage:
  python3 check-mcp-config.py <path-to-.mcp.json>
  python3 check-mcp-config.py <directory>          # finds .mcp.json recursively
  python3 check-mcp-config.py <path> --check-env   # also verify referenced env vars are set
  python3 check-mcp-config.py <path> --json

Exit codes:
  0  no issues
  1  one or more issues found
  2  script error

Pure stdlib Python 3.8+.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ENV_REF_BRACED = re.compile(r"\$\{([A-Z_][A-Z0-9_]*)\}")
ENV_REF_BARE = re.compile(r"\$([A-Z_][A-Z0-9_]*)")
SECRET_LIKE = re.compile(r"\b[A-Za-z0-9+/_\-]{32,}\b")
BEARER_LITERAL = re.compile(r"Bearer\s+[A-Za-z0-9+/_\-.=]{16,}", re.IGNORECASE)


def find_mcp_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    if target.is_dir():
        return sorted(target.rglob(".mcp.json"))
    return []


def validate_one(path: Path, check_env: bool) -> list[dict]:
    issues: list[dict] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [{"severity": "CRITICAL", "path": str(path), "message": "file not found"}]
    except json.JSONDecodeError as e:
        return [{"severity": "CRITICAL", "path": str(path), "message": f"invalid JSON: {e}"}]

    if not isinstance(data, dict):
        return [{
            "severity": "HIGH",
            "path": str(path),
            "message": "top-level value must be a JSON object",
            "fix": 'Wrap the file in a {"mcpServers": {...}} object',
        }]

    servers = data.get("mcpServers")
    if not isinstance(servers, dict):
        return [{
            "severity": "HIGH",
            "path": str(path),
            "message": "missing top-level 'mcpServers' object",
            "fix": 'Wrap server entries: {"mcpServers": {"servername": {...}}}',
        }]

    if not servers:
        return [{
            "severity": "LOW",
            "path": str(path),
            "message": "'mcpServers' is empty — no MCPs configured",
            "fix": "Add server entries, or remove the file if no MCPs are needed",
        }]

    for name, server in servers.items():
        if not isinstance(server, dict):
            issues.append({
                "severity": "HIGH",
                "path": str(path),
                "server": name,
                "message": "server entry is not an object",
                "fix": "Each server must be an object with command/args or type+url",
            })
            continue

        # Transport check
        has_stdio = "command" in server
        has_http = server.get("type") in {"http", "sse"} and "url" in server
        if not has_stdio and not has_http:
            issues.append({
                "severity": "HIGH",
                "path": str(path),
                "server": name,
                "message": "server has neither stdio ('command') nor remote ('type:http' + 'url') transport",
                "fix": 'Add either {"command": "npx", "args": [...]} or {"type":"http", "url":"..."}',
            })

        # Env var checks (env block)
        env = server.get("env", {})
        if isinstance(env, dict):
            for var_name, var_val in env.items():
                if not isinstance(var_val, str):
                    continue
                braced_refs = ENV_REF_BRACED.findall(var_val)
                # Look for $VAR (without braces) — Claude Code does not expand this form
                bare_refs = [m for m in ENV_REF_BARE.findall(var_val) if f"${{{m}}}" not in var_val]
                if bare_refs:
                    issues.append({
                        "severity": "MEDIUM",
                        "path": str(path),
                        "server": name,
                        "message": f"env var '{var_name}' uses '$VAR' form for {bare_refs} — Claude Code expects '${{VAR}}'",
                        "fix": "Wrap variable names in ${} so the value resolves at startup",
                    })
                if check_env:
                    for ref in braced_refs:
                        if not os.environ.get(ref):
                            issues.append({
                                "severity": "LOW",
                                "path": str(path),
                                "server": name,
                                "message": f"env var '{ref}' (referenced by '{var_name}') is not set in current shell",
                                "fix": f"export {ref}=... before launching Claude Code, or document the requirement",
                            })

                # Secret-literal heuristic
                if SECRET_LIKE.search(var_val) and "${" not in var_val:
                    issues.append({
                        "severity": "HIGH",
                        "path": str(path),
                        "server": name,
                        "message": f"env var '{var_name}' looks like a hardcoded secret (long token-shaped value)",
                        "fix": "Replace the literal with ${ENV_VAR} and set the secret in your shell / secrets manager",
                    })

        # Headers check (HTTP servers)
        headers = server.get("headers", {})
        if isinstance(headers, dict):
            for h_name, h_val in headers.items():
                if not isinstance(h_val, str):
                    continue
                if BEARER_LITERAL.search(h_val) and "${" not in h_val:
                    issues.append({
                        "severity": "HIGH",
                        "path": str(path),
                        "server": name,
                        "message": f"header '{h_name}' contains a literal bearer token",
                        "fix": 'Replace with "Bearer ${YOUR_TOKEN_VAR}" and export the token in your shell',
                    })

        # Windows npx wrap warning (heuristic)
        cmd = server.get("command", "")
        if cmd == "npx" and sys.platform == "win32":
            issues.append({
                "severity": "LOW",
                "path": str(path),
                "server": name,
                "message": "on Windows, npx-based MCP servers usually need 'cmd /c' wrapping",
                "fix": 'Try {"command": "cmd", "args": ["/c", "npx", "-y", "<package>"]}',
            })

    return issues


def render_text(report: dict) -> str:
    lines: list[str] = []
    lines.append(f"check-mcp-config: {report['files_checked']} .mcp.json file(s) inspected")
    issues = report["issues"]
    if not issues:
        lines.append("OK — no MCP config issues found.")
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
            label = f"[{i.get('server', '-')}]"
            lines.append(f"  {sev} {label} {i['path']}")
            lines.append(f"      {i['message']}")
            if i.get("fix"):
                lines.append(f"      fix: {i['fix']}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", help="Path to a .mcp.json or a directory containing .mcp.json files")
    p.add_argument("--check-env", action="store_true", help="Also verify referenced env vars are set in current shell")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = p.parse_args(argv)

    target = Path(args.path).resolve()
    if not target.exists():
        print(f"error: not found: {target}", file=sys.stderr)
        return 2

    files = find_mcp_files(target)
    if not files:
        print(f"error: no .mcp.json files found under {target}", file=sys.stderr)
        return 2

    all_issues: list[dict] = []
    for f in files:
        all_issues.extend(validate_one(f, args.check_env))

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
