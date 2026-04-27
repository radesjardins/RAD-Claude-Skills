#!/usr/bin/env python3
"""
check-coolify-env.py — Coolify environment-handling validator.

Catches common env-handling mistakes that lead to leaked secrets, broken
deploys, or non-reproducible builds. Specifically Coolify-aware:
  - .env files in git (huge security issue)
  - Hardcoded secrets in compose/Dockerfile
  - NIXPACKS_* version pins (for reproducibility now that Nixpacks is in
    maintenance mode and runtime versions can shift)
  - Build vs runtime env separation hints

Used by:
  - coolify-reviewer agent (Step 5 Environment Variable Review)
  - Standalone CLI

Usage:
  python3 check-coolify-env.py <project-root>
  python3 check-coolify-env.py <project-root> --json
  python3 check-coolify-env.py <project-root> --strict

Exit codes:
  0  no issues
  1  issues found
  2  script error

Pure stdlib Python 3.8+. No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

SECRET_LIKE_NAMES = re.compile(
    r"(?:^|_)(SECRET|TOKEN|KEY|PASSWORD|PASSWD|PWD|API[-_]?KEY|ACCESS[-_]?KEY|"
    r"PRIVATE[-_]?KEY|AUTH|CREDENTIAL|DATABASE_URL|DB_PASS)(?:_|$)",
    re.IGNORECASE,
)
SECRET_LIKE_VALUE = re.compile(
    r"\b(?:sk_live_|sk_test_|pk_live_|gh[ousp]_|ghp_|xoxb-|xoxp-|AIza[0-9A-Za-z_-]{35}|"
    r"AKIA[0-9A-Z]{16}|[A-Za-z0-9+/]{40,})",
)
NIXPACKS_VAR_RE = re.compile(r"^NIXPACKS_(\w+)$")


@dataclass
class Finding:
    severity: str
    category: str
    file: str | None
    line: int | None
    message: str
    fix: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def check_gitignore(root: Path, findings: list[Finding]) -> None:
    """Verify .env files are not tracked / are in .gitignore."""
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        findings.append(Finding(
            severity="WARNING", category="git-hygiene",
            file=str(gitignore), line=None,
            message="No .gitignore found at project root — .env files may be committable",
            fix="Create .gitignore with at minimum: .env, .env.*, !.env.example, "
                ".claude/settings.local.json, node_modules/, dist/, build/, *.log",
        ))
        return

    gitignore_text = gitignore.read_text(encoding="utf-8", errors="replace")
    required_patterns = [".env", ".env.*"]
    for pattern in required_patterns:
        # Allow .env.example etc. via negation (! prefix)
        has_pattern = any(
            line.strip() in {pattern, pattern + "/", "**/" + pattern}
            for line in gitignore_text.splitlines()
        )
        if not has_pattern:
            findings.append(Finding(
                severity="CRITICAL", category="git-hygiene",
                file=str(gitignore), line=None,
                message=f".gitignore missing '{pattern}' pattern — .env files at risk of being committed",
                fix=f"Add '{pattern}' to .gitignore (use '!.env.example' below it to allow the example file).",
            ))


def check_env_files_committed(root: Path, findings: list[Finding]) -> None:
    """Find .env files that exist at the root — they shouldn't be committed."""
    for env_file in root.glob(".env"):
        if env_file.exists():
            findings.append(Finding(
                severity="CRITICAL", category="git-hygiene",
                file=str(env_file), line=None,
                message=f"{env_file.name} exists at project root — verify it's NOT committed (check `git ls-files .env`)",
                fix="Move secrets to Coolify UI environment variables. Keep .env.example (with placeholder values) "
                    "as a template, but never commit the real .env file.",
            ))


def scan_text_for_secrets(path: Path, text: str, findings: list[Finding]) -> None:
    """Generic scan of text content for secret-shaped tokens."""
    for lineno, line in enumerate(text.splitlines(), start=1):
        # Skip comments
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("//") or not stripped:
            continue
        # Skip env interpolation references like ${VAR}
        if "${" in line and "${VAR}" in line.upper():
            continue

        # Look for KEY=value patterns
        if "=" in line:
            key, _, value = line.partition("=")
            key = key.strip().lstrip("-").lstrip("*").strip()
            value = value.strip().strip('"').strip("'")
            if not value or value.startswith("$"):
                continue

            if SECRET_LIKE_NAMES.search(key) and value not in (
                "", "placeholder", "change-me", "TODO", "REPLACE_ME",
                "your-key-here", "your-secret-here", "xxx", "***",
            ):
                # .env.example exemption: connection-string-shaped values with obvious placeholders
                # (user/password/localhost/host) and no real-secret tokens are template content, not leaks.
                if path.name == ".env.example":
                    looks_like_template = any(marker in value.lower() for marker in (
                        "user:password", "user:pass", "username:password",
                        "your-", "<your", "<replace", "@localhost", "@127.0.0.1",
                        "@host", "@example", "changeme", "placeholder",
                    ))
                    if looks_like_template and not SECRET_LIKE_VALUE.search(value):
                        continue
                    if len(value) < 30 and not SECRET_LIKE_VALUE.search(value):
                        continue
                findings.append(Finding(
                    severity="CRITICAL", category="hardcoded-secret",
                    file=str(path), line=lineno,
                    message=f"'{key}' appears to be a hardcoded secret in {path.name}",
                    fix=f"Move to Coolify UI env vars. In .env.example, use placeholder like 'your-{key.lower()}-here'.",
                ))
            elif SECRET_LIKE_VALUE.search(value):
                findings.append(Finding(
                    severity="CRITICAL", category="hardcoded-secret",
                    file=str(path), line=lineno,
                    message=f"Value of '{key}' looks like a real secret token (in {path.name})",
                    fix="Replace with a reference to a runtime env var; never commit secrets.",
                ))


def check_env_example(root: Path, findings: list[Finding]) -> None:
    env_example = root / ".env.example"
    if not env_example.exists():
        findings.append(Finding(
            severity="SUGGESTION", category="documentation",
            file=str(env_example), line=None,
            message="No .env.example — new contributors don't know which env vars are required",
            fix="Create .env.example with all required env vars and placeholder values (DATABASE_URL=, API_KEY=, etc.)",
        ))
        return

    text = env_example.read_text(encoding="utf-8", errors="replace")
    scan_text_for_secrets(env_example, text, findings)


def check_nixpacks_pinning(root: Path, findings: list[Finding]) -> None:
    """If a Nixpacks-detected stack is present, recommend version pinning since
    Nixpacks is in maintenance mode and runtime versions can drift unexpectedly."""
    has_nixpacks_signal = any(
        (root / marker).exists() for marker in (
            "package.json", "requirements.txt", "Pipfile", "pyproject.toml",
            "Gemfile", "go.mod", "Cargo.toml", "composer.json",
        )
    )
    if not has_nixpacks_signal:
        return

    # Check if user has any NIXPACKS_* config — either via nixpacks.toml or .env
    nixpacks_toml = root / "nixpacks.toml"
    has_pinning = nixpacks_toml.exists()
    if not has_pinning:
        # Look for NIXPACKS_ vars in .env.example (read-only check)
        for candidate in (".env.example", ".env"):
            f = root / candidate
            if f.exists():
                text = f.read_text(encoding="utf-8", errors="replace")
                if "NIXPACKS_" in text:
                    has_pinning = True
                    break

    if not has_pinning:
        findings.append(Finding(
            severity="SUGGESTION", category="reproducibility",
            file=None, line=None,
            message="Project uses Nixpacks (auto-detected from stack markers) but no NIXPACKS_* version pins found. "
                    "Nixpacks is in maintenance mode (Railway, 2025) — runtime versions may drift unexpectedly.",
            fix="Pin runtime versions to keep builds reproducible. Examples: NIXPACKS_NODE_VERSION=22, "
                "NIXPACKS_PYTHON_VERSION=3.12, NIXPACKS_GO_VERSION=1.22. Set these in Coolify UI Build env vars, "
                "or create a nixpacks.toml with [phases.setup] pinned packages. Note: very recent runtime versions "
                "(Node 24+) may not be available in Nixpacks at all — fall back to Dockerfile if needed.",
        ))


def find_secret_scan_targets(root: Path) -> list[Path]:
    """Files where hardcoded secrets are most damaging to find."""
    targets: list[Path] = []
    for pattern in (".env*", "Dockerfile*", "docker-compose*.yml", "docker-compose*.yaml",
                    "compose*.yml", "compose*.yaml"):
        targets.extend(root.glob(pattern))
    # Skip node_modules / .git / etc.
    return [p for p in targets if p.is_file() and not any(part in {"node_modules", ".git"} for part in p.parts)]


def render_text(report: dict) -> str:
    lines: list[str] = []
    lines.append(f"check-coolify-env: {report['root']}")
    findings = report["findings"]
    if not findings:
        lines.append("OK — no env-handling issues.")
        return "\n".join(lines)

    by_severity: dict[str, list[dict]] = {}
    for f in findings:
        by_severity.setdefault(f["severity"], []).append(f)

    lines.append("")
    lines.append(
        f"Issues: {len(findings)} total — "
        + ", ".join(f"{sev}: {len(by_severity[sev])}" for sev in ("CRITICAL", "WARNING", "SUGGESTION") if sev in by_severity)
    )
    for sev in ("CRITICAL", "WARNING", "SUGGESTION"):
        for f in by_severity.get(sev, []):
            location = f"{Path(f['file']).name}:L{f['line']}" if f.get("file") and f.get("line") else \
                       Path(f["file"]).name if f.get("file") else "(project)"
            lines.append(f"  {sev:11} {location:30} ({f['category']}) {f['message']}")
            if f["fix"]:
                lines.append(f"      fix: {f['fix']}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("root", help="Project root directory")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    p.add_argument("--strict", action="store_true", help="Promote SUGGESTION to WARNING")
    args = p.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    check_gitignore(root, findings)
    check_env_files_committed(root, findings)
    check_env_example(root, findings)
    check_nixpacks_pinning(root, findings)

    # Scan all secret-target files for hardcoded values
    for target in find_secret_scan_targets(root):
        if target.name == ".env.example":
            continue  # handled in check_env_example
        text = target.read_text(encoding="utf-8", errors="replace")
        scan_text_for_secrets(target, text, findings)

    if args.strict:
        for f in findings:
            if f.severity == "SUGGESTION":
                f.severity = "WARNING"

    report = {"root": str(root), "findings": [f.to_dict() for f in findings]}

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_text(report))

    return 1 if any(f.severity in ("CRITICAL", "WARNING") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
