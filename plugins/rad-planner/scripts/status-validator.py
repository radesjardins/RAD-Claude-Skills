#!/usr/bin/env python3
"""
status-validator.py — Mechanical validation for docs/status.md.

Validates the v4.0 docs/status.md file (the project's evidence-based handoff
and audit log) against the canonical schema in docs/status-md-schema.md.

Checks:
- Freshness: how stale is status.md relative to git HEAD? (fresh/moderate/stale)
- Sections: all 8 required sections present (or explicitly marked empty)
- Evidence: 'Latest validation results' is evidence-based, not narrative
- Read order: 'If restarting from scratch' has at least 1 file reference

Modes:
  freshness  Compute status.md staleness vs git activity (fresh/moderate/stale).
  sections   Required section presence; empty sections must say "No data this
             session" explicitly rather than be silently empty.
  evidence   'Latest validation results' well-formed (command + result, no
             vague phrases like "should pass" or "tests pass" without command).
  read_order 'If restarting from scratch' has at least 1 file reference.
  all        All of the above.

Usage:
  python3 status-validator.py --mode freshness docs/status.md
  python3 status-validator.py --mode all docs/status.md --json

Output:
  Default — human-readable text. Exit 1 if CRITICAL or HIGH issues, else 0.
  --json   — single JSON object on stdout.
  Exit 2  — script errors (file not found, parse failure).

Freshness thresholds (canonical from docs/status-md-schema.md):
  fresh:    < 2 days AND < 5 commits since last status update
  stale:    > 7 days OR > 20 commits since last status update
  moderate: in between

Falls back to file mtime if git isn't available (not in a git repo, no commits,
git not installed).

No third-party dependencies. Python 3.8+.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

REQUIRED_SECTIONS = (
    "Current state",
    "Last completed",
    "Files changed recently",
    "Latest validation results",
    "Decisions made during execution",
    "Known issues or blockers",
    "Next recommended step",
    "If restarting from scratch",
)

# Phrases that signal an empty-but-explicit section. If the section body contains
# any of these, treat the section as deliberately empty rather than silently missing data.
EMPTY_MARKERS = (
    "no data this session",
    "no validation run this session",
    "no decisions captured this session",
    "no blockers this session",
    "no issues this session",
    "no work this session",
    "nothing to report this session",
    "no data yet",
    "populated by rad-session",
)

# Vague language that's especially bad in validation results
VAGUE_VALIDATION_PHRASES = (
    "should pass",
    "tests pass",
    "should work",
    "probably works",
    "looks good",
    "all green",
    "appears to work",
)

# Freshness thresholds — canonical from docs/status-md-schema.md
FRESH_MAX_SECONDS = 2 * 24 * 60 * 60   # 2 days
STALE_MIN_SECONDS = 7 * 24 * 60 * 60   # 7 days
FRESH_MAX_COMMITS = 5
STALE_MIN_COMMITS = 20

SECTION_HEADING = re.compile(r"^##\s+(.+?)\s*$")
FILE_LIKE = re.compile(
    r"`?[A-Za-z0-9_./-]+\.(?:md|json|yaml|yml|toml|py|ts|tsx|js|jsx|rs|go|java|kt|swift|rb|sh)`?",
    re.IGNORECASE,
)


@dataclass
class Section:
    name: str
    line: int
    body_lines: list[str] = field(default_factory=list)

    @property
    def body(self) -> str:
        return "\n".join(self.body_lines).strip()

    @property
    def is_empty(self) -> bool:
        return not self.body

    @property
    def is_explicit_empty(self) -> bool:
        """Section has content but explicitly marks itself empty."""
        if self.is_empty:
            return False
        body_lower = self.body.lower()
        return any(m in body_lower for m in EMPTY_MARKERS)


@dataclass
class Issue:
    severity: str   # CRITICAL | HIGH | MEDIUM | LOW
    category: str   # sections | evidence | read_order
    section: str | None
    message: str
    fix: str

    def to_dict(self) -> dict:
        return asdict(self)


# ---------- parsing ----------


def parse_sections(text: str) -> dict[str, Section]:
    sections: dict[str, Section] = {}
    current: Section | None = None
    for lineno, raw in enumerate(text.splitlines(), start=1):
        m = SECTION_HEADING.match(raw)
        if m:
            name = m.group(1).strip()
            current = Section(name=name, line=lineno)
            sections[name] = current
            continue
        if raw.startswith("# ") and current is not None:
            current = None
            continue
        if current is None:
            continue
        current.body_lines.append(raw)
    return sections


# ---------- freshness ----------


def _run_git(args: list[str], cwd: Path) -> str | None:
    """Run a git command; return stdout (stripped) on success, None on any failure."""
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            cwd=str(cwd),
            timeout=5,
        )
        if result.returncode != 0:
            return None
        return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return None


def compute_freshness(status_path: Path) -> dict:
    """Compute fresh / moderate / stale based on git history (preferred) or file mtime."""
    cwd = status_path.parent
    now = int(time.time())

    status_age_seconds: int | None = None
    commits_since_status: int | None = None
    source = "unknown"

    # Try git first — find the commit that last touched status.md
    status_commit = _run_git(["log", "-1", "--format=%H", "--", status_path.name], cwd)
    if status_commit:
        # Get the timestamp of that commit
        status_ts_str = _run_git(["log", "-1", "--format=%ct", status_commit], cwd)
        # Count commits since that commit on HEAD
        commits_count_str = _run_git(["rev-list", f"{status_commit}..HEAD", "--count"], cwd)
        try:
            status_ts = int(status_ts_str) if status_ts_str else None
            commits_count = int(commits_count_str) if commits_count_str else 0
            if status_ts is not None:
                status_age_seconds = now - status_ts
                commits_since_status = max(0, commits_count)
                source = "git"
        except (ValueError, TypeError):
            pass

    # Fall back to file mtime if git didn't yield a usable result
    if status_age_seconds is None:
        try:
            mtime = status_path.stat().st_mtime
            status_age_seconds = now - int(mtime)
            commits_since_status = 0
            source = "mtime"
        except OSError:
            return {"freshness": "unknown", "reason": "could not stat file", "source": "none"}

    days_old = status_age_seconds / 86400.0

    # Apply thresholds
    if (status_age_seconds < FRESH_MAX_SECONDS) and (commits_since_status < FRESH_MAX_COMMITS):
        level = "fresh"
    elif (status_age_seconds > STALE_MIN_SECONDS) or (commits_since_status > STALE_MIN_COMMITS):
        level = "stale"
    else:
        level = "moderate"

    return {
        "freshness": level,
        "status_age_days": round(days_old, 2),
        "commits_since_status_update": commits_since_status,
        "source": source,
    }


# ---------- section checks ----------


def check_sections(sections: dict[str, Section]) -> list[Issue]:
    issues: list[Issue] = []
    for req in REQUIRED_SECTIONS:
        if req not in sections:
            issues.append(Issue(
                severity="HIGH",
                category="sections",
                section=req,
                message=f"Missing required section: '## {req}'",
                fix=f"Add '## {req}' per docs/status-md-schema.md; if no data, mark explicitly as 'No data this session'",
            ))
            continue
        s = sections[req]
        if s.is_empty:
            issues.append(Issue(
                severity="MEDIUM",
                category="sections",
                section=req,
                message=f"Section '## {req}' is empty (not even an explicit 'No data' marker)",
                fix="If genuinely no data, write 'No data this session — last run YYYY-MM-DD' rather than leaving blank",
            ))
    return issues


# ---------- evidence checks ----------


def check_evidence(sections: dict[str, Section]) -> list[Issue]:
    """Latest validation results must be evidence-based: command + result."""
    issues: list[Issue] = []
    if "Latest validation results" not in sections:
        return issues  # missing-section already flagged by check_sections
    s = sections["Latest validation results"]
    if s.is_explicit_empty:
        return issues  # explicitly empty is fine
    if s.is_empty:
        return issues  # also caught by check_sections

    body_lower = s.body.lower()

    # Vague language detection
    flagged_phrases: set[str] = set()
    for phrase in VAGUE_VALIDATION_PHRASES:
        if phrase in body_lower and phrase not in flagged_phrases:
            flagged_phrases.add(phrase)
            issues.append(Issue(
                severity="HIGH",
                category="evidence",
                section="Latest validation results",
                message=f"Validation result contains vague phrase: '{phrase}'",
                fix="Replace with a backticked command + concrete result (pass/fail/partial/not-run)",
            ))

    # Heuristic: at least one backticked command should be present
    if "`" not in s.body:
        issues.append(Issue(
            severity="HIGH",
            category="evidence",
            section="Latest validation results",
            message="Latest validation results has no backticked commands",
            fix="Each validation should be a backticked command + result, e.g., `npm test` → pass",
        ))

    return issues


# ---------- read order checks ----------


def check_read_order(sections: dict[str, Section]) -> list[Issue]:
    """If restarting from scratch must have at least 1 file in read-order."""
    issues: list[Issue] = []
    if "If restarting from scratch" not in sections:
        return issues  # missing-section already flagged
    s = sections["If restarting from scratch"]
    if s.is_explicit_empty or s.is_empty:
        issues.append(Issue(
            severity="HIGH",
            category="read_order",
            section="If restarting from scratch",
            message="'If restarting from scratch' is empty — load-bearing for /startup",
            fix="Add at least operating-manual + planning/current.md + a resume action",
        ))
        return issues

    file_mentions = FILE_LIKE.findall(s.body)
    if not file_mentions:
        issues.append(Issue(
            severity="MEDIUM",
            category="read_order",
            section="If restarting from scratch",
            message="'If restarting from scratch' has no file references in read-order",
            fix="List specific files to read (e.g., 'AGENTS.md', 'docs/planning/current.md')",
        ))

    return issues


# ---------- output ----------


def render_text(report: dict, mode: str) -> str:
    lines: list[str] = []
    lines.append(f"status-validator: mode={mode}  file={report['file']}")
    lines.append(f"sections parsed: {report['section_count']}")

    if mode == "freshness":
        f = report["freshness"]
        lines.append("")
        lines.append(f"Freshness: {f['freshness']}")
        lines.append(f"  age: {f.get('status_age_days', 'unknown')} days")
        lines.append(f"  commits since last status update: {f.get('commits_since_status_update', 'unknown')}")
        lines.append(f"  source: {f.get('source', 'unknown')}")
        return "\n".join(lines)

    issues = report.get("issues", [])
    if mode == "all" and "freshness" in report:
        f = report["freshness"]
        lines.append("")
        lines.append(
            f"Freshness: {f['freshness']} "
            f"({f.get('status_age_days', '?')} days, "
            f"{f.get('commits_since_status_update', '?')} commits, "
            f"source={f.get('source', '?')})"
        )

    if not issues:
        lines.append("")
        lines.append("OK — no issues found.")
        return "\n".join(lines)

    by_severity: dict[str, list[dict]] = {}
    for i in issues:
        by_severity.setdefault(i["severity"], []).append(i)
    lines.append("")
    summary = ", ".join(
        f"{sev}: {len(by_severity[sev])}"
        for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW")
        if sev in by_severity
    )
    lines.append(f"Issues: {len(issues)} total — {summary}")
    for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        for i in by_severity.get(sev, []):
            tag = f"[{i['section']}]" if i["section"] else "[status-level]"
            lines.append(f"  {sev} {tag} ({i['category']}) {i['message']}")
            lines.append(f"      fix: {i['fix']}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("path", help="Path to docs/status.md")
    p.add_argument(
        "--mode",
        choices=("freshness", "sections", "evidence", "read_order", "all"),
        default="all",
    )
    p.add_argument("--json", action="store_true", help="Emit a single JSON object instead of text")
    args = p.parse_args(argv)

    file_path = Path(args.path)
    if not file_path.exists():
        print(f"error: file not found: {file_path}", file=sys.stderr)
        return 2

    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"error: failed to read {file_path}: {e}", file=sys.stderr)
        return 2

    sections = parse_sections(text)

    issues: list[Issue] = []
    if args.mode in ("sections", "all"):
        issues.extend(check_sections(sections))
    if args.mode in ("evidence", "all"):
        issues.extend(check_evidence(sections))
    if args.mode in ("read_order", "all"):
        issues.extend(check_read_order(sections))

    report: dict = {
        "file": str(file_path),
        "mode": args.mode,
        "section_count": len(sections),
        "section_names": list(sections.keys()),
        "issues": [i.to_dict() for i in issues],
    }
    if args.mode in ("freshness", "all"):
        report["freshness"] = compute_freshness(file_path)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_text(report, args.mode))

    if args.mode == "freshness":
        return 0  # freshness mode never fails — it reports a level
    fail = any(i.severity in ("CRITICAL", "HIGH") for i in issues)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
