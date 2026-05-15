#!/usr/bin/env python3
"""
coverage-validator.py — Flag acceptance criteria without apparent verification.

For each AC in `docs/planning/current.md` `## Acceptance criteria`, compute
token overlap against the `## Validation commands` section. If no validation
command plausibly verifies an AC (overlap below threshold), flag that AC as
uncovered.

Severity policy:
- HIGH: `## Validation commands` is missing or empty entirely — every AC is
  uncovered by definition.
- MEDIUM: A specific AC has token overlap below the threshold with every
  validation command (the AC has no apparent verification path).
- LOW: There are AC items but the validation-to-AC ratio looks suspicious
  (e.g., 10 ACs, 1 command — likely under-validation).

This is heuristic. Token overlap can miss legitimate validation pairings
(an AC about "rate limiting" validated by a command named "test:api"). The
validator surfaces signals; the user judges.

Usage:
  python3 coverage-validator.py docs/planning/current.md
  python3 coverage-validator.py docs/planning/current.md --threshold 0.15
  python3 coverage-validator.py docs/planning/current.md --json

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


DEFAULT_THRESHOLD = 0.15
LOW_RATIO_THRESHOLD = 0.2  # ACs-per-validation-command ratio below this is suspicious

SECTION_HEADING = re.compile(r"^##\s+(.+?)\s*$")
CHECKBOX = re.compile(r"^\s*-\s*\[(?P<box>[ x])\]\s*(?P<text>.+?)\s*$")
BULLET = re.compile(r"^\s*-\s+(?P<text>.+?)\s*$")
TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")
BACKTICK = re.compile(r"`([^`]+)`")

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
class ACItem:
    line: int
    text: str
    tokens: frozenset
    checked: bool


@dataclass
class ValCommand:
    line: int
    text: str
    tokens: frozenset


@dataclass
class Finding:
    severity: str       # HIGH | MEDIUM | LOW | INFO
    category: str       # no_validation_section | empty_validation | uncovered_ac | low_ratio
    file: str
    line: int
    message: str
    ac_text: str = ""
    best_overlap: float = 0.0
    fix: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _stem(tok: str) -> str:
    """Strip simple English plurals so 'commands' matches 'command'."""
    if len(tok) > 3:
        if tok.endswith("ies"):
            return tok[:-3] + "y"
        if tok.endswith("es") and not tok.endswith("ses") and not tok.endswith("ues"):
            return tok[:-2]
        if tok.endswith("s") and not tok.endswith("ss") and not tok.endswith("us"):
            return tok[:-1]
    return tok


def tokenize(text: str) -> frozenset:
    """Return a stemmed, stopword-filtered token set for overlap math."""
    # Treat backtick-quoted content as plain text — `bun test` should expose `bun` and `test`
    text = BACKTICK.sub(r" \1 ", text)
    raw = TOKEN_RE.findall(text.lower())
    return frozenset(_stem(t) for t in raw if t not in STOPWORDS and len(t) > 1)


def parse_sections(file_path: Path) -> dict[str, tuple[int, list[str]]]:
    """Return {section_name_lower: (heading_line_1indexed, body_lines)}."""
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}

    sections: dict[str, tuple[int, list[str]]] = {}
    current = None
    current_line = 0
    body: list[str] = []
    for i, raw in enumerate(text.splitlines(), start=1):
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


def collect_acs(section_line: int, body: list[str]) -> list[ACItem]:
    acs: list[ACItem] = []
    for offset, raw in enumerate(body, start=1):
        m = CHECKBOX.match(raw)
        if m:
            text = m.group("text").strip()
            acs.append(ACItem(
                line=section_line + offset,
                text=text,
                tokens=tokenize(text),
                checked=m.group("box") == "x",
            ))
    return acs


def collect_val_commands(section_line: int, body: list[str]) -> list[ValCommand]:
    cmds: list[ValCommand] = []
    for offset, raw in enumerate(body, start=1):
        m = BULLET.match(raw) or CHECKBOX.match(raw)
        if not m:
            continue
        text = m.group("text").strip() if hasattr(m, "group") else None
        # CHECKBOX has named groups; BULLET also has 'text' group
        if not text:
            continue
        cmds.append(ValCommand(
            line=section_line + offset,
            text=text,
            tokens=tokenize(text),
        ))
    return cmds


def jaccard(a: frozenset, b: frozenset) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def check_coverage(plan_path: Path, threshold: float) -> tuple[list[ACItem],
                                                               list[ValCommand],
                                                               list[Finding]]:
    sections = parse_sections(plan_path)
    findings: list[Finding] = []

    if "acceptance criteria" not in sections:
        findings.append(Finding(
            severity="INFO",
            category="no_acceptance_criteria_section",
            file=str(plan_path),
            line=1,
            message="No '## Acceptance criteria' section found — nothing to check.",
        ))
        return [], [], findings

    ac_line, ac_body = sections["acceptance criteria"]
    acs = collect_acs(ac_line, ac_body)
    if not acs:
        findings.append(Finding(
            severity="LOW",
            category="empty_acceptance_criteria",
            file=str(plan_path),
            line=ac_line,
            message="'## Acceptance criteria' section has no checkbox items.",
            fix="Add at least one `- [ ] <criterion>` item.",
        ))
        return acs, [], findings

    if "validation commands" not in sections:
        findings.append(Finding(
            severity="HIGH",
            category="no_validation_section",
            file=str(plan_path),
            line=ac_line,
            message=f"{len(acs)} acceptance criteria but no '## Validation "
                    f"commands' section. Every AC is uncovered.",
            fix="Add a '## Validation commands' section with at least one "
                "command per major AC.",
        ))
        return acs, [], findings

    vc_line, vc_body = sections["validation commands"]
    cmds = collect_val_commands(vc_line, vc_body)
    if not cmds:
        findings.append(Finding(
            severity="HIGH",
            category="empty_validation_section",
            file=str(plan_path),
            line=vc_line,
            message=f"'## Validation commands' is present but empty. "
                    f"{len(acs)} ACs are uncovered.",
            fix="Add at least one validation command. Common shapes: a test "
                "command, a typecheck, a linter, a build verification.",
        ))
        return acs, cmds, findings

    # Per-AC overlap check
    for ac in acs:
        best = max((jaccard(ac.tokens, c.tokens) for c in cmds), default=0.0)
        if best < threshold:
            findings.append(Finding(
                severity="MEDIUM",
                category="uncovered_ac",
                file=str(plan_path),
                line=ac.line,
                message=f"AC has no apparent verification (best overlap "
                        f"{best:.2f} < threshold {threshold:.2f}).",
                ac_text=ac.text,
                best_overlap=best,
                fix="Add a validation command whose name or description "
                    "references the same concepts as this AC.",
            ))

    # Ratio check
    if len(acs) >= 5 and len(cmds) / len(acs) < LOW_RATIO_THRESHOLD:
        findings.append(Finding(
            severity="LOW",
            category="low_ratio",
            file=str(plan_path),
            line=vc_line,
            message=f"{len(acs)} ACs vs {len(cmds)} validation command(s) — "
                    f"ratio {len(cmds)/len(acs):.2f} is below "
                    f"{LOW_RATIO_THRESHOLD:.2f}. Consider whether each AC has "
                    f"a clear verification path.",
        ))

    return acs, cmds, findings


def render_text(plan_path: Path, acs: list[ACItem], cmds: list[ValCommand],
                findings: list[Finding]) -> str:
    out = [f"coverage-validator: {plan_path}", ""]
    out.append(f"Acceptance criteria: {len(acs)} item(s)")
    out.append(f"Validation commands: {len(cmds)} command(s)")
    if not acs:
        out.append("")
    elif not cmds:
        out.append("")
        out.append("All ACs are uncovered (no validation commands).")
    else:
        out.append("")
    if not findings:
        out.append("PASS — every AC has plausible validation coverage.")
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
            out.append(f"  {f.file}:{f.line}  {f.category}")
            out.append(f"    {f.message}")
            if f.ac_text:
                out.append(f"    AC: {f.ac_text}")
            if f.fix:
                out.append(f"    Fix: {f.fix}")
        out.append("")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("plan_file", help="Path to docs/planning/current.md")
    p.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                   help=f"Token-overlap threshold (default {DEFAULT_THRESHOLD})")
    p.add_argument("--json", action="store_true", help="Emit a single JSON object")
    args = p.parse_args(argv)

    plan_path = Path(args.plan_file).resolve()
    if not plan_path.exists() or not plan_path.is_file():
        print(f"error: plan file not found: {plan_path}", file=sys.stderr)
        return 2

    acs, cmds, findings = check_coverage(plan_path, args.threshold)

    if args.json:
        report = {
            "file": str(plan_path),
            "threshold": args.threshold,
            "ac_count": len(acs),
            "validation_command_count": len(cmds),
            "findings": [f.to_dict() for f in findings],
        }
        print(json.dumps(report, indent=2))
    else:
        print(render_text(plan_path, acs, cmds, findings))

    has_blocker = any(f.severity in ("HIGH", "MEDIUM") for f in findings)
    return 1 if has_blocker else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
