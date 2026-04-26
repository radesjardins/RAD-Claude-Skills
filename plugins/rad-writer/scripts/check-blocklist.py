#!/usr/bin/env python3
"""
check-blocklist.py — Deterministic scan of text against the rad-writer word blocklist.

Replaces the LLM doing string-matching against the blocklist. Returns line-and-column
locations for every match, plus replacement suggestions where defined. Saves tokens
and gives reproducible results.

Usage:
  python3 check-blocklist.py <file.md|->                  # text or stdin
  python3 check-blocklist.py file.md --json
  python3 check-blocklist.py file.md --severity always-avoid
  python3 check-blocklist.py file.md --top 20             # only show top 20 by count
  python3 check-blocklist.py --list                       # print the blocklist itself

Output:
  Default — text report with locations and suggested replacements
  --json  — single JSON object suitable for skill consumption

Exit codes:
  0  no matches found
  1  matches found
  2  script error

Honest framing — read this before relying on the output:

  Word blocklist matching is a SOFT signal in 2026. The "delve / leverage / foster"
  vocabulary became famous as AI tells in 2023-2024. Several of these words have
  since been actively suppressed by newer model training (e.g., "delve" dropped
  sharply in 2025 per Wikipedia's "Signs of AI Writing"). Human writers also use
  many of these words in normal writing. Treat matches as STYLE NOISE worth
  considering, not proof of AI authorship. The most reliable AI signals in 2026
  are structural (specificity gap, copula avoidance, rule-of-three abuse), not
  lexical — see references/ai-writing-patterns.md for the durable list.

Pure stdlib Python 3.8+. No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# (word, severity, replacement_suggestion)
# severity: "always-avoid" | "context" | "watch"
# Drawn from references/word-blocklist.md but with severity downgraded for
# words that 2025+ models actively suppress.
BLOCKLIST: list[tuple[str, str, str]] = [
    # Verbs (always-avoid in general writing)
    ("delve", "always-avoid", "explore, examine, dig into, look at, investigate"),
    ("leverage", "always-avoid", "use, apply, build on, take advantage of"),
    ("utilize", "always-avoid", "use"),
    ("harness", "always-avoid", "use, channel, apply, direct"),
    ("streamline", "always-avoid", "simplify, speed up, cut steps from, automate"),
    ("underscore", "always-avoid", "emphasize, highlight, show, reveal"),
    ("foster", "always-avoid", "encourage, support, build, grow, create"),
    ("elevate", "always-avoid", "improve, raise, strengthen"),
    ("empower", "always-avoid", "enable, give the ability to, let"),
    ("spearhead", "always-avoid", "lead, start, drive, run"),
    ("bolster", "always-avoid", "support, strengthen, reinforce"),
    ("catalyze", "always-avoid", "cause, trigger, spark, start"),
    ("endeavor", "always-avoid", "try, attempt, work to"),
    ("facilitate", "always-avoid", "help, enable, make possible, run"),
    ("embark", "always-avoid", "start, begin, launch"),
    ("unpack", "always-avoid", "explain, break down, examine"),
    ("captivate", "always-avoid", "interest, engage, hold attention"),
    ("resonate", "always-avoid", "connect with, matter to, strike a chord with"),
    ("encompass", "always-avoid", "include, cover, span"),
    ("revolutionize", "always-avoid", "change, rethink, redesign"),
    ("transform", "always-avoid", "change, reshape, rethink"),
    ("elucidate", "always-avoid", "explain, clarify, spell out"),
    ("ascertain", "always-avoid", "find out, determine, learn"),
    ("envision", "always-avoid", "imagine, picture, plan"),
    ("unleash", "always-avoid", "release, enable, open up"),
    # Adjectives
    ("pivotal", "always-avoid", "important, key, critical, decisive"),
    ("robust", "context", "strong, solid, thorough — context-OK in engineering/statistics"),
    ("innovative", "always-avoid", "new, original, novel — describe the actual innovation"),
    ("seamless", "always-avoid", "smooth, easy, simple, integrated"),
    ("comprehensive", "context", "complete, full, thorough — context-OK in research"),
    ("nuanced", "always-avoid", "subtle, complex, layered"),
    ("multifaceted", "always-avoid", "complex, varied, many-sided"),
    ("groundbreaking", "always-avoid", "new, significant, first-of-its-kind"),
    ("transformative", "always-avoid", "significant, major, substantial"),
    ("holistic", "always-avoid", "complete, whole, full-picture, integrated"),
    ("meticulous", "always-avoid", "careful, precise, detailed, thorough"),
    ("intricate", "always-avoid", "complex, detailed, layered"),
    ("invaluable", "always-avoid", "valuable, essential, useful, important"),
    ("paramount", "always-avoid", "most important, top priority, critical"),
    ("indispensable", "always-avoid", "essential, necessary, critical"),
    ("cutting-edge", "always-avoid", "new, latest, advanced"),
    # Nouns (most are watch — many flag in clusters but are fine alone)
    ("landscape", "watch", "field, space, market, industry, world (when metaphorical)"),
    ("realm", "always-avoid", "area, field, domain, world"),
    ("tapestry", "always-avoid", "mix, combination, pattern, set"),
    ("synergy", "always-avoid", "compatibility, fit, working together"),
    ("synergies", "always-avoid", "compatibilities, ways of working together"),
    ("paradigm", "watch", "approach, model, framework, way"),
    ("cornerstone", "always-avoid", "foundation, key part, core"),
    ("linchpin", "always-avoid", "key part, critical piece"),
    ("nexus", "always-avoid", "connection, point, intersection"),
    ("plethora", "always-avoid", "many, lots of, a range of"),
    ("myriad", "always-avoid", "many, numerous, lots of"),
    # Adverbs (mostly watch — not categorically wrong, but cluster signal)
    ("arguably", "watch", "consider just stating the claim"),
    ("undeniably", "always-avoid", "clearly, definitely, unmistakably"),
    ("notably", "watch", "consider whether the emphasis is needed"),
    ("remarkably", "watch", "say what's remarkable, not just that it is"),
    ("fundamentally", "watch", "consider whether 'fundamentally' adds meaning"),
    ("inherently", "watch", "consider whether 'inherently' adds meaning"),
    # Throat-clearing phrases — match across word boundaries
    # (we handle these separately below as PHRASE_PATTERNS)
]

# Multi-word AI patterns — flagged with a regex match
PHRASE_PATTERNS: list[tuple[str, str, str, str]] = [
    # (label, regex, severity, suggestion)
    ("it's important to note", r"\bit'?s\s+important\s+to\s+note\b", "always-avoid", "[delete — just state the thing]"),
    ("in today's [X] landscape", r"\bin\s+today'?s\s+[a-z\-]+\s+(?:landscape|world)\b", "always-avoid", "open with the actual point"),
    ("at the end of the day", r"\bat\s+the\s+end\s+of\s+the\s+day\b", "always-avoid", "[delete or restate the conclusion directly]"),
    ("when it comes to", r"\bwhen\s+it\s+comes\s+to\b", "always-avoid", "[delete — name the thing directly]"),
    ("in the realm of", r"\bin\s+the\s+realm\s+of\b", "always-avoid", "in [field/area/topic]"),
    ("here's the thing", r"\bhere'?s\s+the\s+thing\b", "watch", "[delete — make the point directly]"),
    ("let's dive in", r"\blet'?s\s+dive\s+in\b", "always-avoid", "[delete or replace with substantive lead]"),
    ("game-changer", r"\bgame[-\s]chang(?:er|ing|e)\b", "always-avoid", "explain what changed and how"),
    ("paradigm shift", r"\bparadigm\s+shift\b", "always-avoid", "describe the actual change"),
    ("furthermore", r"\bfurthermore\b", "watch", "consider natural flow without explicit transition"),
    ("additionally", r"\badditionally\b", "watch", "consider 'also' or natural flow"),
    ("moreover", r"\bmoreover\b", "watch", "consider natural flow without explicit transition"),
    # AI verb substitution: "serves as / stands as / represents" replacing "is/are"
    ("serves as", r"\bserves?\s+as\b", "watch", "consider 'is' or 'acts as' if either works"),
    ("stands as", r"\bstands?\s+as\b", "watch", "consider 'is' if it works"),
]


def scan_text(text: str, severity_filter: str | None = None) -> list[dict]:
    findings: list[dict] = []
    lines = text.splitlines()

    # Single-word matches
    word_map = {w: (sev, sug) for w, sev, sug in BLOCKLIST}
    pattern_words = re.compile(r"\b([\w'-]+)\b")
    for lineno, line in enumerate(lines, start=1):
        for m in pattern_words.finditer(line):
            w = m.group(1).lower()
            if w in word_map:
                sev, sug = word_map[w]
                if severity_filter and sev != severity_filter:
                    continue
                findings.append({
                    "type": "word",
                    "match": m.group(1),
                    "lemma": w,
                    "line": lineno,
                    "column": m.start() + 1,
                    "severity": sev,
                    "suggestion": sug,
                    "context": line[max(0, m.start() - 20):m.end() + 20].strip(),
                })

    # Phrase matches
    for label, pattern, sev, sug in PHRASE_PATTERNS:
        if severity_filter and sev != severity_filter:
            continue
        rx = re.compile(pattern, re.IGNORECASE)
        for lineno, line in enumerate(lines, start=1):
            for m in rx.finditer(line):
                findings.append({
                    "type": "phrase",
                    "match": m.group(0),
                    "label": label,
                    "line": lineno,
                    "column": m.start() + 1,
                    "severity": sev,
                    "suggestion": sug,
                    "context": line[max(0, m.start() - 20):m.end() + 20].strip(),
                })

    # Sort: severity (always-avoid first), then count
    sev_order = {"always-avoid": 0, "context": 1, "watch": 2}
    findings.sort(key=lambda f: (sev_order.get(f["severity"], 9), f["line"], f["column"]))
    return findings


def render_text(report: dict) -> str:
    lines: list[str] = []
    lines.append(f"check-blocklist: {report['file']}  ({report['total_findings']} match(es))")
    lines.append("")
    lines.append("NOTE: Word-list matching is a SOFT signal in 2026. Many of these were strong")
    lines.append("AI tells in 2023-2024 but newer models are suppressing them and human writers")
    lines.append("use many of them naturally. Treat as style noise, not proof of AI authorship.")

    if not report["findings"]:
        lines.append("")
        lines.append("OK — no blocklist matches.")
        return "\n".join(lines)

    by_severity: dict[str, list[dict]] = {}
    for f in report["findings"]:
        by_severity.setdefault(f["severity"], []).append(f)

    lines.append("")
    lines.append("Summary by severity:")
    for sev in ("always-avoid", "context", "watch"):
        if sev in by_severity:
            lines.append(f"  {sev}: {len(by_severity[sev])} match(es)")

    # Top words by count
    counts: dict[str, int] = {}
    for f in report["findings"]:
        key = f.get("lemma") or f.get("label", "?")
        counts[key] = counts.get(key, 0) + 1
    top = sorted(counts.items(), key=lambda kv: -kv[1])[: report.get("top_n") or 10]
    lines.append("")
    lines.append(f"Top {len(top)} (by count):")
    for word, c in top:
        lines.append(f"  {c}× {word}")

    lines.append("")
    lines.append("Findings (always-avoid first):")
    for f in report["findings"]:
        marker = "▸"
        loc = f"L{f['line']}:C{f['column']}"
        what = f.get("label") or f.get("lemma") or f.get("match")
        lines.append(f"  {marker} {f['severity']:13} {loc:10} {what}")
        if f.get("context"):
            lines.append(f"    context: …{f['context']}…")
        if f.get("suggestion"):
            lines.append(f"    suggest: {f['suggestion']}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", nargs="?", help="Path to text file, or '-' for stdin")
    p.add_argument("--severity", choices=("always-avoid", "context", "watch"),
                   help="Only show findings of this severity")
    p.add_argument("--top", type=int, default=10, help="How many 'top by count' entries to show (default 10)")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    p.add_argument("--list", action="store_true", help="Print the blocklist itself and exit")
    args = p.parse_args(argv)

    if args.list:
        print("# Single-word blocklist")
        for w, sev, sug in BLOCKLIST:
            print(f"  [{sev}] {w} → {sug}")
        print()
        print("# Phrase patterns")
        for label, _, sev, sug in PHRASE_PATTERNS:
            print(f"  [{sev}] {label} → {sug}")
        return 0

    if not args.path:
        print("error: path required (or '-' for stdin)", file=sys.stderr)
        return 2

    if args.path == "-":
        text = sys.stdin.read()
        source = "<stdin>"
    else:
        path = Path(args.path)
        if not path.exists():
            print(f"error: file not found: {path}", file=sys.stderr)
            return 2
        text = path.read_text(encoding="utf-8", errors="replace")
        source = str(path)

    if not text.strip():
        print("error: empty input", file=sys.stderr)
        return 2

    findings = scan_text(text, args.severity)
    report = {
        "file": source,
        "total_findings": len(findings),
        "top_n": args.top,
        "findings": findings,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_text(report))

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
