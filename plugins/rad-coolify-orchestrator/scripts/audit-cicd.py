#!/usr/bin/env python3
"""
audit-cicd.py — Coolify CI/CD pipeline validator.

Catches the patterns the coolify-reviewer agent currently checks subjectively
on GitHub Actions and GitLab CI files for Coolify deployments.

Used by:
  - coolify-reviewer agent (Step 4 CI/CD Review)
  - Standalone CLI

Usage:
  python3 audit-cicd.py <project-root>
  python3 audit-cicd.py <path-to-workflow-yml>
  python3 audit-cicd.py <path> --json

Exit codes:
  0  no issues
  1  issues found
  2  script error

Heuristic checks (regex-based, not full YAML parse):
  - curl to Coolify webhook without --fail (silent failures)
  - Hardcoded Coolify tokens (vs $secrets reference)
  - Webhook URL exposed in workflow (vs secret reference)
  - :latest image tags vs SHA pinning
  - Missing test gate before deploy
  - Missing post-deploy status check

Pure stdlib Python 3.8+. No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class Finding:
    severity: str
    category: str
    file: str
    line: int | None
    message: str
    fix: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# Detect a curl invocation hitting a Coolify deploy endpoint
COOLIFY_DEPLOY_URL_RE = re.compile(
    r"https?://[^\s'\"]+/api/v\d+/deploy",
    re.IGNORECASE,
)
CURL_LINE_RE = re.compile(r"\bcurl\b", re.IGNORECASE)  # match curl anywhere on the line (handles YAML 'run: curl ...')
HAS_FAIL_FLAG_RE = re.compile(r"--fail\b|--fail-with-body\b|-fsSL\b")
HAS_BEARER_RE = re.compile(r"Authorization:\s*Bearer\s+([^\s\"']+)", re.IGNORECASE)

# Token-shaped values
TOKEN_LITERAL_RE = re.compile(r"\b[A-Za-z0-9_-]{20,}\b")
SECRET_REF_RE = re.compile(r"\$\{?\{?\s*(?:secrets|env)\.[\w_]+\s*\}?\}?", re.IGNORECASE)
ENV_VAR_RE = re.compile(r"\$\{?[A-Z_][A-Z0-9_]*\}?")

# Image tag patterns
IMAGE_LATEST_RE = re.compile(r"\b(image|tag|tags):\s*[\"']?([\w./-]+:latest|[\w./-]+)[\"']?", re.IGNORECASE)
IMAGE_TAG_FIELD_RE = re.compile(r"^\s*tags?:\s*[\"']?([\w./:-]+)[\"']?", re.IGNORECASE)

# Webhook URL token shape (matches both query params and headers)
WEBHOOK_URL_TOKEN_RE = re.compile(
    r"https?://[^\s'\"]+\?(?:uuid|tag|token)=[\w-]{8,}",
    re.IGNORECASE,
)


def lint_workflow(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()

    has_test_step = False
    has_deploy_step = False
    deploy_step_lines: list[int] = []
    has_post_deploy_check = False

    # First pass: structural detection
    test_keywords = re.compile(r"\b(test|tests|pytest|vitest|jest|cargo test|go test|rspec|phpunit|npm test|yarn test|pnpm test|bun test)\b", re.IGNORECASE)
    deploy_keywords = re.compile(r"\b(deploy|deployment)\b", re.IGNORECASE)
    status_check_keywords = re.compile(r"coolify_get_deployment|/api/v\d+/deployments?/|deployment.*status", re.IGNORECASE)

    for lineno, line in enumerate(lines, start=1):
        if test_keywords.search(line) and not line.strip().startswith("#"):
            has_test_step = True
        if deploy_keywords.search(line) and "name:" in line.lower():
            has_deploy_step = True
            deploy_step_lines.append(lineno)
        if status_check_keywords.search(line):
            has_post_deploy_check = True

    # Second pass: line-by-line issue detection
    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue

        # ---------- curl checks ----------
        if CURL_LINE_RE.search(line) and COOLIFY_DEPLOY_URL_RE.search(line):
            # We have a curl hitting Coolify — check for --fail
            # Look at surrounding lines too (curl can span multiple lines with \)
            block = line
            # Look forward up to 5 lines for --fail flag
            for follow in lines[lineno:lineno + 5]:
                if "\\" in lines[lineno - 1] or follow.strip().startswith(("-", "https://", "http://")):
                    block += " " + follow.strip()
                else:
                    break

            if not HAS_FAIL_FLAG_RE.search(block):
                findings.append(Finding(
                    severity="CRITICAL", category="silent-failure",
                    file=str(path), line=lineno,
                    message="curl to Coolify deploy endpoint without --fail flag — HTTP errors return success exit code, "
                            "CI passes even when deployment trigger fails",
                    fix="Add --fail (or --fail-with-body for visibility): "
                        "'curl --fail-with-body -H \"Authorization: Bearer ${{ secrets.COOLIFY_TOKEN }}\" "
                        "\"https://coolify.example.com/api/v1/deploy?uuid=APP_UUID\"'",
                ))

            # Check for hardcoded webhook URL with embedded token
            if WEBHOOK_URL_TOKEN_RE.search(line) and "${{" not in line and "$WEBHOOK" not in line.upper():
                findings.append(Finding(
                    severity="CRITICAL", category="exposed-secret",
                    file=str(path), line=lineno,
                    message="Webhook URL with embedded token/uuid is hardcoded in workflow file — secret in git history",
                    fix="Move the URL to a secret: 'curl --fail \"${{ secrets.COOLIFY_DEPLOY_WEBHOOK }}\"'. "
                        "Or split: keep base URL in workflow, put token-bearing parts in secrets.",
                ))

        # ---------- Authorization header checks ----------
        bearer_match = HAS_BEARER_RE.search(line)
        if bearer_match:
            # Check the whole rest of the line for a secret reference, not just the
            # small capture (GitHub Actions '${{ secrets.X }}' has spaces inside braces).
            after_bearer = line[bearer_match.start():]
            has_secret_ref = SECRET_REF_RE.search(after_bearer) is not None
            has_env_var = ENV_VAR_RE.search(after_bearer) is not None
            token_part = bearer_match.group(1)
            if not has_secret_ref and not has_env_var:
                findings.append(Finding(
                    severity="CRITICAL", category="exposed-secret",
                    file=str(path), line=lineno,
                    message="Bearer token in Authorization header looks hardcoded (not a secret reference)",
                    fix="Use 'Authorization: Bearer ${{ secrets.COOLIFY_TOKEN }}' (GitHub Actions) "
                        "or '$COOLIFY_TOKEN' (GitLab CI) backed by a CI/CD secret store.",
                ))

        # ---------- Image tag checks ----------
        if "image:" in line.lower() or "tags:" in line.lower():
            tag_match = IMAGE_TAG_FIELD_RE.search(line)
            if tag_match:
                tag = tag_match.group(1)
                if tag.endswith(":latest") or (":" not in tag.rsplit("/", 1)[-1]):
                    findings.append(Finding(
                        severity="WARNING", category="reproducibility",
                        file=str(path), line=lineno,
                        message=f"Image tag '{tag}' uses ':latest' or no tag — Coolify deploys won't be reproducible",
                        fix="Pin to git SHA: 'tags: ghcr.io/owner/repo:${{ github.sha }}'. "
                            "Avoid ':latest' for production deploys.",
                    ))

    # ---------- Workflow-level structural checks ----------
    if has_deploy_step and not has_test_step:
        findings.append(Finding(
            severity="WARNING", category="quality-gate",
            file=str(path), line=deploy_step_lines[0] if deploy_step_lines else 1,
            message="Workflow has a deploy step but no detectable test step — broken code can ship",
            fix="Add a test job that runs before the deploy job. In GitHub Actions, use 'needs: [test]' on "
                "the deploy job so it only runs when tests pass.",
        ))

    if has_deploy_step and not has_post_deploy_check:
        findings.append(Finding(
            severity="SUGGESTION", category="observability",
            file=str(path), line=deploy_step_lines[0] if deploy_step_lines else 1,
            message="Deploy step doesn't poll deployment status — CI succeeds as soon as trigger returns 200, "
                    "even if the actual deployment fails 30s later",
            fix="After triggering deploy, poll '/api/v1/deployments/<uuid>' (or use the bundled "
                "@radoriginllc/coolify-mcp 'coolify_get_deployment' tool) until status is finished/failed. "
                "Fail the workflow if final status is failed.",
        ))

    return findings


def find_workflow_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    if target.is_dir():
        results: list[Path] = []
        # GitHub Actions
        results.extend(target.glob(".github/workflows/*.yml"))
        results.extend(target.glob(".github/workflows/*.yaml"))
        # GitLab CI
        for gl in (".gitlab-ci.yml", ".gitlab-ci.yaml"):
            f = target / gl
            if f.exists():
                results.append(f)
        return results
    return []


def render_text(report: dict) -> str:
    lines: list[str] = []
    lines.append(f"audit-cicd: {report['file']}")
    findings = report["findings"]
    if not findings:
        lines.append("OK — no CI/CD issues.")
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
            loc = f"L{f['line']}" if f.get("line") else ""
            lines.append(f"  {sev:11} {loc:6} ({f['category']}) {f['message']}")
            if f["fix"]:
                lines.append(f"      fix: {f['fix']}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", help="Path to a workflow file or project root")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = p.parse_args(argv)

    target = Path(args.path).resolve()
    if not target.exists():
        print(f"error: not found: {target}", file=sys.stderr)
        return 2

    files = find_workflow_files(target)
    if not files:
        print(f"error: no CI/CD workflow files found at {target}", file=sys.stderr)
        return 2

    all_reports: list[dict] = []
    any_blocking = False
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        findings = lint_workflow(f, text)
        if any(fd.severity in ("CRITICAL", "WARNING") for fd in findings):
            any_blocking = True
        all_reports.append({"file": str(f), "findings": [fd.to_dict() for fd in findings]})

    if args.json:
        print(json.dumps({"reports": all_reports}, indent=2))
    else:
        for r in all_reports:
            print(render_text(r))
            print()

    return 1 if any_blocking else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
