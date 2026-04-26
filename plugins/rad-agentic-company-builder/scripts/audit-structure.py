#!/usr/bin/env python3
"""
audit-structure.py — Mechanical audit of an agentic company / Claude Code workspace.

Checks the structural claims in the rad-agentic-company-builder scaffold
deterministically. Replaces the "company-auditor agent makes subjective 1-10 score"
pattern with concrete pass/fail per check, so the agent's judgment can be reserved
for things that actually need judgment.

Default audit covers:
  - Company root: CLAUDE.md present? .claude/settings.json valid JSON?
                  .claude/rules/ present?
  - Each division (engineering/, product/, operations/, marketing/, finance/):
                  CLAUDE.md present?
  - Each engineering project (any subdir of engineering/ excluding shared-packages):
                  Standard layout? Wrapper/repo if opted-in? task-specs/?
                  repo/.git/? repo/CLAUDE.md? repo/.claude/agents/? repo/.mcp.json
                  if MCPs are configured?
  - Hooks/MCP files: valid JSON? Hook events reference real Claude Code events?

Usage:
  python3 audit-structure.py <company-root>
  python3 audit-structure.py <company-root> --json
  python3 audit-structure.py <company-root> --strict
  python3 audit-structure.py . --skip-hooks --skip-mcp

Exit codes:
  0  no issues
  1  issues found
  2  script error (path not found, parse failure)

Pure stdlib Python 3.8+. No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

# Real Claude Code hook events (verified April 2026).
# See validate-hooks.py for the deeper semantic check.
REAL_HOOK_EVENTS = {
    "PreToolUse",
    "PostToolUse",
    "UserPromptSubmit",
    "SessionStart",
    "SessionEnd",
    "Stop",
    "SubagentStop",
    "PreCompact",
    "Notification",
    "PermissionRequest",
    "ConfigChange",
    "WorktreeCreate",
    "WorktreeRemove",
    # Agent Teams (experimental — fires only when CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1):
    "TeammateIdle",
    "TaskCompleted",
}

STANDARD_DIVISIONS = ("engineering", "product", "operations", "marketing", "finance")


@dataclass
class Finding:
    severity: str  # CRITICAL | HIGH | MEDIUM | LOW | OK
    category: str  # company | division | project | hooks | mcp | agents
    path: str
    message: str
    fix: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# ---------- helpers ----------


def _exists(path: Path) -> bool:
    return path.exists()


def _read_json_safe(path: Path) -> tuple[dict | list | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, "file not found"
    except json.JSONDecodeError as e:
        return None, f"invalid JSON: {e}"
    except OSError as e:
        return None, f"could not read: {e}"


# ---------- company-level checks ----------


def audit_company(root: Path, findings: list[Finding]) -> None:
    if not (root / "CLAUDE.md").exists():
        findings.append(
            Finding(
                "HIGH",
                "company",
                str(root / "CLAUDE.md"),
                "Company root CLAUDE.md missing",
                "Run scaffold-company, or create CLAUDE.md by hand with the universal rules block",
            )
        )

    settings_path = root / ".claude" / "settings.json"
    if not settings_path.exists():
        findings.append(
            Finding(
                "MEDIUM",
                "company",
                str(settings_path),
                "Company .claude/settings.json missing",
                "Run scaffold-company to generate it, or create one with permissions allow/deny",
            )
        )
    else:
        data, err = _read_json_safe(settings_path)
        if err:
            findings.append(Finding("HIGH", "company", str(settings_path), err, "Fix the JSON syntax"))

    rules_dir = root / ".claude" / "rules"
    if not rules_dir.is_dir():
        findings.append(
            Finding(
                "LOW",
                "company",
                str(rules_dir),
                ".claude/rules/ missing (optional but recommended for company-wide rule files)",
                "Create .claude/rules/ with code-standards.md and security-policy.md",
            )
        )


# ---------- division checks ----------


def audit_divisions(root: Path, divisions: Iterable[str], strict: bool, findings: list[Finding]) -> None:
    for div in divisions:
        div_path = root / div
        if not div_path.is_dir():
            sev = "MEDIUM" if strict else "LOW"
            findings.append(
                Finding(
                    sev,
                    "division",
                    str(div_path),
                    f"Division '{div}' missing — note: optional unless explicitly scaffolded",
                    f"Run scaffold-company with --divisions including {div}, or remove the expectation if not used",
                )
            )
            continue

        if not (div_path / "CLAUDE.md").exists():
            findings.append(
                Finding(
                    "MEDIUM",
                    "division",
                    str(div_path / "CLAUDE.md"),
                    f"Division '{div}' has no CLAUDE.md — agents working in this folder won't get division-specific context",
                    f"Add a CLAUDE.md under {div}/ describing the division's purpose and conventions",
                )
            )


# ---------- engineering project checks ----------


def audit_projects(root: Path, strict: bool, findings: list[Finding]) -> None:
    eng = root / "engineering"
    if not eng.is_dir():
        return

    for entry in sorted(eng.iterdir()):
        if not entry.is_dir():
            continue
        # Skip well-known shared dirs
        if entry.name in {"shared-packages", "shared", "node_modules", ".git"}:
            continue
        # Skip if division-level CLAUDE.md (already audited)
        if entry.name == "CLAUDE.md":
            continue

        audit_one_project(entry, strict, findings)


def audit_one_project(project_dir: Path, strict: bool, findings: list[Finding]) -> None:
    # Layout heuristic: if a `repo/` subdir exists with .git inside, treat as wrapper/repo pattern.
    # Otherwise treat the project_dir itself as the repo root.
    repo_subdir = project_dir / "repo"
    is_wrapper_layout = repo_subdir.is_dir() and (repo_subdir / ".git").exists()

    if is_wrapper_layout:
        wrapper = project_dir
        repo = repo_subdir
    else:
        wrapper = None
        repo = project_dir if (project_dir / ".git").exists() else None

    if repo is None:
        findings.append(
            Finding(
                "MEDIUM",
                "project",
                str(project_dir),
                "No git repository found at project root or under repo/",
                "Either initialize a git repo here, or skip auditing this directory (it may not be a project)",
            )
        )
        return

    # Wrapper checks (only when wrapper layout is in use)
    if wrapper is not None:
        if not (wrapper / "CLAUDE.md").exists():
            findings.append(
                Finding(
                    "LOW",
                    "project",
                    str(wrapper / "CLAUDE.md"),
                    "Wrapper CLAUDE.md missing — wrapper layout intentionally separates management context from repo",
                    "Add a CLAUDE.md at the wrapper level with sprint/architecture context",
                )
            )
        if not (wrapper / "task-specs").is_dir():
            sev = "LOW" if not strict else "MEDIUM"
            findings.append(
                Finding(
                    sev,
                    "project",
                    str(wrapper / "task-specs"),
                    "task-specs/ directory missing in wrapper",
                    "Create task-specs/ with TEMPLATE.md if you want a structured agent-task spec home",
                )
            )

    # Repo-level checks (always required when a git repo exists)
    if not (repo / "CLAUDE.md").exists():
        findings.append(
            Finding(
                "HIGH",
                "project",
                str(repo / "CLAUDE.md"),
                "Repo CLAUDE.md missing — agents won't have project-specific tech-stack context",
                "Run scaffold-project for a template, or write one with tech stack + build commands",
            )
        )

    settings = repo / ".claude" / "settings.json"
    if settings.exists():
        data, err = _read_json_safe(settings)
        if err:
            findings.append(Finding("HIGH", "project", str(settings), err, "Fix the JSON syntax"))

    agents_dir = repo / ".claude" / "agents"
    if not agents_dir.is_dir():
        findings.append(
            Finding(
                "LOW",
                "project",
                str(agents_dir),
                ".claude/agents/ missing — optional, but you'll lose project-specific agent specialization",
                "Run generate-agents if you want the standard 6-agent engineering team",
            )
        )

    mcp_path = repo / ".mcp.json"
    if mcp_path.exists():
        data, err = _read_json_safe(mcp_path)
        if err:
            findings.append(Finding("HIGH", "project", str(mcp_path), err, "Fix the JSON syntax"))

    gitignore_path = repo / ".gitignore"
    if gitignore_path.exists():
        gitignore = gitignore_path.read_text(encoding="utf-8", errors="replace")
        for entry in ("CLAUDE.local.md", ".claude/settings.local.json", ".env"):
            if entry not in gitignore:
                findings.append(
                    Finding(
                        "MEDIUM",
                        "project",
                        str(gitignore_path),
                        f".gitignore missing entry: {entry}",
                        f"Add '{entry}' to .gitignore to prevent leaking personal/local config",
                    )
                )


# ---------- hook event sanity check ----------


def audit_hooks(root: Path, findings: list[Finding]) -> None:
    for settings in root.rglob(".claude/settings.json"):
        data, err = _read_json_safe(settings)
        if err or not isinstance(data, dict):
            continue
        hooks = data.get("hooks")
        if not isinstance(hooks, dict):
            continue
        for event_name in hooks:
            if event_name not in REAL_HOOK_EVENTS:
                findings.append(
                    Finding(
                        "HIGH",
                        "hooks",
                        str(settings),
                        f"Hook event '{event_name}' is not a documented Claude Code event",
                        f"Remove this event or replace with one of: {', '.join(sorted(REAL_HOOK_EVENTS))}",
                    )
                )


# ---------- MCP config sanity ----------


def audit_mcp(root: Path, findings: list[Finding]) -> None:
    for mcp_path in root.rglob(".mcp.json"):
        data, err = _read_json_safe(mcp_path)
        if err:
            findings.append(Finding("HIGH", "mcp", str(mcp_path), err, "Fix the JSON syntax"))
            continue
        if not isinstance(data, dict):
            continue
        servers = data.get("mcpServers")
        if not isinstance(servers, dict):
            findings.append(
                Finding(
                    "MEDIUM",
                    "mcp",
                    str(mcp_path),
                    "Top-level 'mcpServers' object missing or wrong type",
                    "Wrap server entries under a top-level 'mcpServers' key",
                )
            )
            continue

        env_var_pattern = re.compile(r"\$\{([A-Z_][A-Z0-9_]*)\}")
        for server_name, server in servers.items():
            if not isinstance(server, dict):
                findings.append(
                    Finding(
                        "MEDIUM",
                        "mcp",
                        str(mcp_path),
                        f"MCP server '{server_name}' entry is not an object",
                        "Each server must be an object with command/args/url fields",
                    )
                )
                continue

            has_stdio = "command" in server
            has_http = server.get("type") == "http" and "url" in server
            if not has_stdio and not has_http:
                findings.append(
                    Finding(
                        "HIGH",
                        "mcp",
                        str(mcp_path),
                        f"MCP server '{server_name}' has neither 'command' (stdio) nor 'type:http' + 'url'",
                        "Add a 'command'+'args' block for stdio servers, or 'type:\"http\"'+'url' for remote",
                    )
                )

            # Env var reference sanity
            env = server.get("env", {})
            for var_name, var_val in env.items() if isinstance(env, dict) else []:
                if not isinstance(var_val, str):
                    continue
                refs = env_var_pattern.findall(var_val)
                # Note: we don't error on plaintext values (some users use them in dev),
                # we only flag the case where a reference looks malformed (e.g., $VAR vs ${VAR}).
                if "$" in var_val and not refs and "${" not in var_val:
                    findings.append(
                        Finding(
                            "LOW",
                            "mcp",
                            str(mcp_path),
                            f"MCP '{server_name}' env var '{var_name}' uses '$VAR' style — Claude Code expects '${{VAR}}'",
                            "Wrap variable names in ${} for proper expansion",
                        )
                    )


# ---------- agent file frontmatter sanity ----------


AGENT_FRONTMATTER_REQUIRED = {"name", "description"}
AGENT_FRONTMATTER_RECOMMENDED = {"tools", "model"}


def audit_agents(root: Path, findings: list[Finding]) -> None:
    for agent_file in root.rglob(".claude/agents/*.md"):
        text = agent_file.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            findings.append(
                Finding(
                    "MEDIUM",
                    "agents",
                    str(agent_file),
                    "Agent file missing YAML frontmatter (should start with '---')",
                    "Add frontmatter with at minimum: name, description",
                )
            )
            continue
        # Lightweight key extraction — find lines that look like 'key: value' between
        # the opening and closing '---' fence. Avoids needing PyYAML.
        end = text.find("\n---", 3)
        if end < 0:
            findings.append(
                Finding(
                    "MEDIUM",
                    "agents",
                    str(agent_file),
                    "Agent frontmatter has no closing '---' fence",
                    "Close the YAML frontmatter with '---' on its own line",
                )
            )
            continue
        frontmatter = text[3:end]
        keys = set()
        for line in frontmatter.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("-"):
                continue
            if ":" in stripped:
                key = stripped.split(":", 1)[0].strip()
                # Ignore deeply nested keys
                if not line.startswith((" ", "\t")):
                    keys.add(key)

        for required in AGENT_FRONTMATTER_REQUIRED:
            if required not in keys:
                findings.append(
                    Finding(
                        "HIGH",
                        "agents",
                        str(agent_file),
                        f"Agent frontmatter missing required field: {required}",
                        f"Add '{required}: ...' to the YAML frontmatter",
                    )
                )
        for recommended in AGENT_FRONTMATTER_RECOMMENDED:
            if recommended not in keys:
                findings.append(
                    Finding(
                        "LOW",
                        "agents",
                        str(agent_file),
                        f"Agent frontmatter missing recommended field: {recommended}",
                        f"Add '{recommended}: ...' so Claude Code applies the right model and tool restrictions",
                    )
                )


# ---------- output ----------


def render_text(report: dict) -> str:
    lines: list[str] = []
    lines.append(f"audit-structure: root={report['root']}")
    lines.append(f"divisions checked: {', '.join(report['divisions'])}")
    if report.get("skipped"):
        lines.append(f"skipped: {', '.join(report['skipped'])}")
    findings = report["findings"]
    if not findings:
        lines.append("")
        lines.append("OK — no structural issues found.")
        return "\n".join(lines)

    by_severity: dict[str, list[dict]] = {}
    for f in findings:
        by_severity.setdefault(f["severity"], []).append(f)

    lines.append("")
    lines.append(
        f"Findings: {len(findings)} total — "
        + ", ".join(f"{sev}: {len(by_severity[sev])}" for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW") if sev in by_severity)
    )
    for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        for f in by_severity.get(sev, []):
            lines.append(f"  {sev} ({f['category']}) {f['path']}")
            lines.append(f"      {f['message']}")
            if f["fix"]:
                lines.append(f"      fix: {f['fix']}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("root", help="Path to company root directory")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    p.add_argument("--strict", action="store_true", help="Promote optional findings to higher severity")
    p.add_argument("--divisions", default=",".join(STANDARD_DIVISIONS), help="Comma-separated division names to expect")
    p.add_argument("--skip-hooks", action="store_true", help="Skip hook event sanity check")
    p.add_argument("--skip-mcp", action="store_true", help="Skip .mcp.json validation")
    p.add_argument("--skip-agents", action="store_true", help="Skip agent file frontmatter check")
    p.add_argument("--skip-projects", action="store_true", help="Skip per-project engineering audit")
    args = p.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: directory not found: {root}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    divisions = [d.strip() for d in args.divisions.split(",") if d.strip()]
    skipped: list[str] = []

    audit_company(root, findings)
    audit_divisions(root, divisions, args.strict, findings)
    if args.skip_projects:
        skipped.append("projects")
    else:
        audit_projects(root, args.strict, findings)
    if args.skip_hooks:
        skipped.append("hooks")
    else:
        audit_hooks(root, findings)
    if args.skip_mcp:
        skipped.append("mcp")
    else:
        audit_mcp(root, findings)
    if args.skip_agents:
        skipped.append("agents")
    else:
        audit_agents(root, findings)

    report = {
        "root": str(root),
        "divisions": divisions,
        "skipped": skipped,
        "findings": [f.to_dict() for f in findings],
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_text(report))

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
