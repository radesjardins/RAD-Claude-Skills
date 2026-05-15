#!/usr/bin/env python3
"""
estimate-validator.py — Flag milestones without effort estimates.

A milestone-shaped plan (rad-planner canonical `docs/planning/current.md`) should
carry SOME signal of effort/size — either a t-shirt size, a time range, or a
context-window bar (per rad-planner's "size discipline" methodology). This
validator scans `current.md` for any of several conventional estimate signals
and flags MEDIUM if none are present.

Accepted forms (any one passes):

  1. Dedicated section heading: `## Effort`, `## Estimate`, `## Size`,
     `## Sizing`, `## Effort estimate`, or `## Complexity`.
  2. Inline field in any section body:
       Effort: M
       Estimate: ~2 days
       Size: Large
       Sizing: 3 of 5
       Complexity: medium-high
       Context bar: ~50%
  3. T-shirt size suffix on the `Current milestone` line:
       M2 (M): User-defined activity constraints
       M3 [L] — Live evaluation engine
  4. Per-AC parenthetical estimates in `Acceptance criteria`:
       - [ ] Constraint evaluator returns go/no-go (S)
       - [ ] Visual Crossing rate-limit handling (~1d)

Usage:
  python3 estimate-validator.py docs/planning/current.md
  python3 estimate-validator.py docs/planning/current.md --json

Output:
  Default — human-readable text. Exit 1 if MEDIUM or higher findings; else 0.
  --json   — single JSON object on stdout.
  Exit 2   — script errors.

No third-party dependencies. Python 3.8+.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path


SECTION_HEADING = re.compile(r"^##\s+(.+?)\s*$")
CHECKBOX = re.compile(r"^\s*-\s*\[[ x]\]\s*(?P<text>.+?)\s*$")

EFFORT_SECTION_NAMES = frozenset({
    "effort", "estimate", "size", "sizing", "effort estimate",
    "effort estimates", "complexity", "sizing & effort", "estimation",
})

# Inline field — matches `Effort: ...` (with or without bold)
INLINE_FIELD = re.compile(
    r"(?im)^\s*(?:\*\*)?(?P<label>effort|estimate|size|sizing|complexity|context bar)(?:\*\*)?\s*:\s*(?P<value>\S.+?)\s*$"
)

# T-shirt size or duration in the Current milestone heading (line after `## Current milestone`)
MILESTONE_SIZE = re.compile(
    r"(?ix)"
    r"(\bM\d+\s*[\(\[]\s*(?:xs|s|m|l|xl)\s*[\)\]]"   # M2 (M) or M2 [L]
    r"|\bM\d+\s*[—\-]\s*(?:xs|s|m|l|xl)\b"           # M2 — L
    r"|~?\s*\d+\s*(?:min|minute|h|hr|hour|d|day|w|week)s?\b"  # ~3 days, 5min
    r")"
)

# Per-AC trailing parenthetical estimate
AC_ESTIMATE = re.compile(
    r"(?ix)"
    r"\((?:"
    r"xs|s|m|l|xl"                                   # t-shirt
    r"|~?\s*\d+\s*(?:min|minute|h|hr|hour|d|day|w|week)s?"  # 3d, ~2hr
    r"|\d+\s*pts?"                                   # 5pt, 3 points
    r"|\d+/\d+"                                      # 3/5
    r")\)\s*$"
)


@dataclass
class Finding:
    severity: str       # MEDIUM | LOW | INFO
    category: str       # missing_estimate | estimate_in_body_only | partial_coverage
    file: str
    line: int
    message: str
    fix: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Result:
    file: str
    estimate_signals_found: list[str] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "estimate_signals_found": self.estimate_signals_found,
            "findings": [f.to_dict() for f in self.findings],
        }


def parse_sections(lines: list[str]) -> dict[str, tuple[int, list[str]]]:
    """Return {section_name_lower: (heading_line_1indexed, body_lines)}."""
    sections: dict[str, tuple[int, list[str]]] = {}
    current = None
    current_line = 0
    body: list[str] = []
    for i, raw in enumerate(lines, start=1):
        m = SECTION_HEADING.match(raw)
        if m:
            if current is not None:
                sections[current] = (current_line, body)
            current = m.group(1).strip().lower()
            current_line = i
            body = []
        else:
            body.append(raw)
    if current is not None:
        sections[current] = (current_line, body)
    return sections


def find_estimate_signals(file_path: Path) -> tuple[list[str], list[Finding]]:
    """Scan a planning/current.md for any conventional estimate signals.

    Returns (signals_found, findings). signals_found is a list of human-readable
    signal names (e.g., "section:Effort", "inline:Size=M", "milestone-suffix").
    findings contains MEDIUM/LOW issues for missing or weak coverage.
    """
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return [], [Finding("HIGH", "io_error", str(file_path), 0,
                            f"Cannot read file: {e}")]

    lines = text.splitlines()
    sections = parse_sections(lines)
    signals: list[str] = []
    findings: list[Finding] = []

    # Signal 1 — dedicated section heading
    for name in sections:
        if name in EFFORT_SECTION_NAMES:
            line, body = sections[name]
            body_text = "\n".join(body).strip()
            if body_text:
                signals.append(f"section:{name}")
            else:
                findings.append(Finding(
                    severity="LOW",
                    category="empty_estimate_section",
                    file=str(file_path),
                    line=line,
                    message=f"Section '## {name}' is present but empty.",
                    fix="Add an effort estimate (t-shirt size, time range, "
                        "or context-bar percentage).",
                ))

    # Signal 2 — inline field anywhere
    for i, raw in enumerate(lines, start=1):
        m = INLINE_FIELD.match(raw)
        if m:
            signals.append(f"inline:{m.group('label').lower()}={m.group('value').strip()[:40]}")

    # Signal 3 — milestone-line size suffix
    if "current milestone" in sections:
        line, body = sections["current milestone"]
        for j, raw in enumerate(body, start=1):
            if not raw.strip():
                continue
            if MILESTONE_SIZE.search(raw):
                signals.append("milestone-suffix")
                break
            break  # Only check the first non-blank body line

    # Signal 4 — per-AC parenthetical estimates
    if "acceptance criteria" in sections:
        line, body = sections["acceptance criteria"]
        ac_count = 0
        ac_with_estimate = 0
        for raw in body:
            if CHECKBOX.match(raw):
                ac_count += 1
                if AC_ESTIMATE.search(raw):
                    ac_with_estimate += 1
        if ac_with_estimate > 0:
            ratio = ac_with_estimate / ac_count if ac_count else 0
            signals.append(f"per-ac:{ac_with_estimate}/{ac_count}")
            if 0 < ratio < 0.5:
                findings.append(Finding(
                    severity="LOW",
                    category="partial_ac_estimate_coverage",
                    file=str(file_path),
                    line=line,
                    message=f"Only {ac_with_estimate} of {ac_count} acceptance "
                            f"criteria carry an estimate parenthetical.",
                    fix="Either add estimates to the remaining ACs or move the "
                        "estimate signal up to a milestone-level field.",
                ))

    # If NO signals found, flag MEDIUM
    if not signals:
        findings.append(Finding(
            severity="MEDIUM",
            category="missing_estimate",
            file=str(file_path),
            line=1,
            message="No effort/size estimate detected in this plan. "
                    "Plans should carry some sizing signal so reviewers and "
                    "scheduling can reason about scope vs. capacity.",
            fix="Add ONE of: (a) a '## Effort' section, (b) an inline "
                "'Effort: M' / 'Estimate: ~2 days' field, (c) a t-shirt size "
                "suffix on the milestone line like 'M2 (M):', or "
                "(d) per-AC parentheticals like '- [ ] Task X (S)'.",
        ))

    return signals, findings


def render_text(result: Result) -> str:
    out = [f"estimate-validator: {result.file}", ""]
    if result.estimate_signals_found:
        out.append("Estimate signals found:")
        for sig in result.estimate_signals_found:
            out.append(f"  - {sig}")
        out.append("")
    else:
        out.append("No estimate signals detected.")
        out.append("")

    if not result.findings:
        out.append("PASS — at least one estimate signal present.")
        return "\n".join(out)

    by_sev = {"HIGH": [], "MEDIUM": [], "LOW": [], "INFO": []}
    for f in result.findings:
        by_sev.setdefault(f.severity, []).append(f)
    for sev in ("HIGH", "MEDIUM", "LOW", "INFO"):
        items = by_sev.get(sev, [])
        if not items:
            continue
        out.append(f"[{sev}] {len(items)} finding{'s' if len(items) != 1 else ''}")
        for f in items:
            out.append(f"  {f.file}:{f.line}  {f.category}")
            out.append(f"    {f.message}")
            if f.fix:
                out.append(f"    Fix: {f.fix}")
        out.append("")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("plan_file", help="Path to docs/planning/current.md (or equivalent)")
    p.add_argument("--json", action="store_true", help="Emit a single JSON object")
    args = p.parse_args(argv)

    plan_path = Path(args.plan_file).resolve()
    if not plan_path.exists() or not plan_path.is_file():
        print(f"error: plan file not found: {plan_path}", file=sys.stderr)
        return 2

    signals, findings = find_estimate_signals(plan_path)
    result = Result(
        file=str(plan_path),
        estimate_signals_found=signals,
        findings=findings,
    )

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(render_text(result))

    has_blocker = any(f.severity in ("HIGH", "MEDIUM") for f in findings)
    return 1 if has_blocker else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
