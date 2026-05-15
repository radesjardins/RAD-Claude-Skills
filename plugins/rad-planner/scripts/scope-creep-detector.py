#!/usr/bin/env python3
"""
scope-creep-detector.py — Detect when current.md is doing things vision.md said are non-goals.

Different from `doc-contradiction.py` (which flags any vision non-goal whose
tokens appear in current ACs) by being more targeted: this validator focuses
specifically on the scope-creep pattern — vision.md non-goals that are NOT
preserved in current.md's own non-goals AND ARE present in current.md's
acceptance criteria or planned changes.

Two signals:

  1. DROPPED non-goal: a vision.md non-goal whose substantive tokens don't
     appear in current.md's `## Non-goals` section. The project-level boundary
     is no longer being acknowledged at the milestone level.

  2. ACTIVE creep: a dropped vision.md non-goal whose tokens DO appear in
     current.md's `## Acceptance criteria` or `## Planned changes`. The
     milestone appears to be doing exactly what vision.md said it would not.

Severity:
- HIGH: ACTIVE creep (dropped + appears in plan content)
- MEDIUM: DROPPED non-goal (boundary forgotten but not yet acted on)
- LOW: weak match below the high-confidence threshold but worth review

Usage:
  python3 scope-creep-detector.py /path/to/project
  python3 scope-creep-detector.py /path/to/project --threshold 0.35
  python3 scope-creep-detector.py /path/to/project --json

Output:
  Default — human-readable text. Exit 1 if HIGH or MEDIUM findings; else 0.
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


DEFAULT_THRESHOLD = 0.35
LOW_THRESHOLD = 0.20

SECTION_HEADING = re.compile(r"^##\s+(.+?)\s*$")
CHECKBOX = re.compile(r"^\s*-\s*\[[ x]\]\s*(?P<text>.+?)\s*$")
BULLET = re.compile(r"^\s*-\s+(?P<text>.+?)\s*$")
TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")

NEGATION_WORDS = frozenset({
    "not", "no", "never", "won't", "wont", "without",
    "neither", "nor", "none", "skip", "skipping", "skipped",
    "avoid", "avoiding", "exclude", "excluded", "excluding",
})

STOPWORDS = frozenset({
    "a", "an", "the", "of", "to", "in", "on", "at", "by", "for", "with",
    "and", "or", "but", "if", "then", "else", "when", "where",
    "is", "are", "was", "were", "be", "been", "being",
    "this", "that", "these", "those", "it", "its", "as",
    "do", "does", "did", "have", "has", "had",
    "will", "would", "could", "should", "can",
    "i", "you", "we", "they", "he", "she",
    "all", "any", "some", "each", "every", "via", "from", "into",
})


@dataclass
class NonGoal:
    file: str
    line: int
    text: str
    tokens: frozenset


@dataclass
class PlanItem:
    section: str
    line: int
    text: str
    tokens: frozenset


@dataclass
class Finding:
    severity: str         # HIGH | MEDIUM | LOW | INFO
    category: str         # active_creep | dropped_non_goal | weak_match
    file_a: str           # vision.md
    line_a: int
    text_a: str
    file_b: str           # current.md
    line_b: int
    text_b: str
    overlap: float
    section_b: str = ""   # which section in current.md showed the conflict
    note: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _stem(tok: str) -> str:
    if len(tok) > 3:
        if tok.endswith("ies"):
            return tok[:-3] + "y"
        if tok.endswith("es") and not tok.endswith("ses") and not tok.endswith("ues"):
            return tok[:-2]
        if tok.endswith("s") and not tok.endswith("ss") and not tok.endswith("us"):
            return tok[:-1]
    return tok


def tokenize(text: str, strip_negation: bool = True) -> frozenset:
    raw = TOKEN_RE.findall(text.lower())
    filtered = [_stem(t) for t in raw if t not in STOPWORDS and len(t) > 1]
    if strip_negation:
        filtered = [t for t in filtered if t not in NEGATION_WORDS]
    return frozenset(filtered)


def parse_section_bullets(file_path: Path, section_name_lower: str) -> tuple[int, list[tuple[int, str]]]:
    """Return (section_heading_line, [(item_line, text), ...]) for bullet/checkbox items
    in a named section."""
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0, []

    section_line = 0
    items: list[tuple[int, str]] = []
    in_section = False

    for i, raw in enumerate(text.splitlines(), start=1):
        m = SECTION_HEADING.match(raw)
        if m:
            heading = m.group(1).strip().lower()
            if heading == section_name_lower:
                in_section = True
                section_line = i
            else:
                in_section = False
            continue
        if not in_section:
            continue

        cm = CHECKBOX.match(raw)
        bm = BULLET.match(raw)
        if cm:
            content = cm.group("text").strip()
        elif bm:
            content = bm.group("text").strip()
        else:
            continue
        if len(content) >= 4:
            items.append((i, content))

    return section_line, items


def jaccard(a: frozenset, b: frozenset) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def best_overlap(target: frozenset, candidates: list) -> tuple[float, object]:
    """Return (best_overlap, best_candidate) where candidates have .tokens."""
    best = 0.0
    best_cand = None
    for c in candidates:
        score = jaccard(target, c.tokens)
        if score > best:
            best = score
            best_cand = c
    return best, best_cand


def detect_scope_creep(project_dir: Path, threshold: float) -> tuple[list[NonGoal],
                                                                    list[PlanItem],
                                                                    list[Finding]]:
    vision = project_dir / "docs" / "vision.md"
    current = project_dir / "docs" / "planning" / "current.md"
    findings: list[Finding] = []

    if not vision.exists():
        findings.append(Finding(
            severity="INFO",
            category="missing_vision",
            file_a=str(vision), line_a=0, text_a="",
            file_b="", line_b=0, text_b="", overlap=0.0,
            note="No docs/vision.md — scope-creep detection requires both vision.md and current.md.",
        ))
        return [], [], findings
    if not current.exists():
        findings.append(Finding(
            severity="INFO",
            category="missing_current",
            file_a="", line_a=0, text_a="",
            file_b=str(current), line_b=0, text_b="", overlap=0.0,
            note="No docs/planning/current.md — nothing to check creep against.",
        ))
        return [], [], findings

    # Vision non-goals
    _, vision_items = parse_section_bullets(vision, "non-goals")
    vision_non_goals: list[NonGoal] = [
        NonGoal(str(vision), line, text, tokenize(text))
        for line, text in vision_items
        if tokenize(text)
    ]

    # Current non-goals
    _, current_ng_items = parse_section_bullets(current, "non-goals")
    current_non_goals: list[NonGoal] = [
        NonGoal(str(current), line, text, tokenize(text))
        for line, text in current_ng_items
        if tokenize(text)
    ]

    # Current ACs + planned changes
    ac_line, ac_items = parse_section_bullets(current, "acceptance criteria")
    pc_line, pc_items = parse_section_bullets(current, "planned changes")
    current_plan_items: list[PlanItem] = []
    for line, text in ac_items:
        toks = tokenize(text)
        if toks:
            current_plan_items.append(PlanItem("Acceptance criteria", line, text, toks))
    for line, text in pc_items:
        toks = tokenize(text)
        if toks:
            current_plan_items.append(PlanItem("Planned changes", line, text, toks))

    if not vision_non_goals:
        findings.append(Finding(
            severity="LOW",
            category="no_vision_non_goals",
            file_a=str(vision), line_a=0, text_a="",
            file_b="", line_b=0, text_b="", overlap=0.0,
            note="vision.md has no '## Non-goals' section. Scope creep cannot be checked.",
        ))
        return vision_non_goals, current_plan_items, findings

    # For each vision non-goal, check whether current.md preserves it
    for vng in vision_non_goals:
        preserved_score, preserved_cand = best_overlap(vng.tokens, current_non_goals)
        is_preserved = preserved_score >= threshold

        # If preserved, no further check needed
        if is_preserved:
            continue

        # Not preserved — check if it's actively being violated
        creep_score, creep_cand = best_overlap(vng.tokens, current_plan_items)

        if creep_score >= threshold:
            findings.append(Finding(
                severity="HIGH",
                category="active_creep",
                file_a=vng.file, line_a=vng.line, text_a=vng.text,
                file_b=creep_cand.file if hasattr(creep_cand, "file") else str(current),
                line_b=creep_cand.line,
                text_b=creep_cand.text,
                section_b=creep_cand.section,
                overlap=creep_score,
                note="Vision non-goal not preserved in current.md non-goals AND its "
                     "concepts appear in current.md plan content.",
            ))
        elif creep_score >= LOW_THRESHOLD:
            findings.append(Finding(
                severity="LOW",
                category="weak_match",
                file_a=vng.file, line_a=vng.line, text_a=vng.text,
                file_b=str(current), line_b=creep_cand.line if creep_cand else 0,
                text_b=creep_cand.text if creep_cand else "",
                section_b=creep_cand.section if creep_cand else "",
                overlap=creep_score,
                note="Weak match — possible creep but below high-confidence threshold.",
            ))
        else:
            findings.append(Finding(
                severity="MEDIUM",
                category="dropped_non_goal",
                file_a=vng.file, line_a=vng.line, text_a=vng.text,
                file_b=str(current), line_b=0, text_b="",
                overlap=preserved_score,
                note="Vision non-goal is not preserved in current.md non-goals (boundary "
                     "no longer acknowledged at milestone level), but not currently visible "
                     "in plan content.",
            ))

    return vision_non_goals, current_plan_items, findings


def render_text(vng: list[NonGoal], pi: list[PlanItem],
                findings: list[Finding]) -> str:
    out = ["scope-creep-detector", ""]
    out.append(f"Vision non-goals: {len(vng)}")
    out.append(f"Current plan items (ACs + planned changes): {len(pi)}")
    out.append("")
    if not findings:
        out.append("PASS — every vision non-goal is preserved in current.md or absent from plan content.")
        return "\n".join(out)

    by_sev = {"HIGH": [], "MEDIUM": [], "LOW": [], "INFO": []}
    for f in findings:
        by_sev.setdefault(f.severity, []).append(f)
    for sev in ("HIGH", "MEDIUM", "LOW", "INFO"):
        items = by_sev.get(sev, [])
        if not items:
            continue
        out.append(f"[{sev}] {len(items)} finding{'s' if len(items) != 1 else ''}")
        for f in items:
            out.append(f"  {f.category}  (overlap {f.overlap:.2f})")
            if f.text_a:
                out.append(f"    vision.md:{f.line_a}  '{f.text_a}'")
            if f.text_b:
                section = f" ({f.section_b})" if f.section_b else ""
                out.append(f"    current.md:{f.line_b}{section}  '{f.text_b}'")
            if f.note:
                out.append(f"    Note: {f.note}")
        out.append("")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("project_dir", help="Path to project root (containing docs/)")
    p.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                   help=f"Token-overlap threshold (default {DEFAULT_THRESHOLD})")
    p.add_argument("--json", action="store_true", help="Emit a single JSON object")
    args = p.parse_args(argv)

    project_dir = Path(args.project_dir).resolve()
    if not project_dir.exists() or not project_dir.is_dir():
        print(f"error: project dir not found: {project_dir}", file=sys.stderr)
        return 2

    vng, pi, findings = detect_scope_creep(project_dir, args.threshold)

    if args.json:
        report = {
            "project_dir": str(project_dir),
            "threshold": args.threshold,
            "vision_non_goals_count": len(vng),
            "current_plan_items_count": len(pi),
            "findings": [f.to_dict() for f in findings],
        }
        print(json.dumps(report, indent=2))
    else:
        print(render_text(vng, pi, findings))

    has_blocker = any(f.severity in ("HIGH", "MEDIUM") for f in findings)
    return 1 if has_blocker else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
