#!/usr/bin/env python3
r"""
dependency-cycle-detector.py — Detect cycles in milestone dependency graphs.

Scans a planning directory (default: `docs/planning/`) for milestone-shaped
markdown files (`current.md` + `archive/*.md`) and extracts dependency
relationships, then runs DFS cycle detection on the resulting graph.

Dependency declarations recognized (any one form):

  1. Dedicated section: `## Dependencies` listing milestone IDs
       ## Dependencies
       - M1
       - M3

  2. Inline field: `Depends on: M1, M3` or `Dependencies: M2`

  3. Per-AC reference: `- [ ] Task X (depends on M2)`

Milestone IDs accepted: `M1`, `M2`, ..., `M99` (one or two digits). Case
insensitive. Whitespace around `M\d+` is permitted.

A cycle is reported with the full cycle path.

Usage:
  python3 dependency-cycle-detector.py docs/planning/
  python3 dependency-cycle-detector.py docs/planning/ --json
  python3 dependency-cycle-detector.py docs/planning/ --include-archive

Output:
  Default — human-readable text. Exit 1 if any cycle detected; else 0.
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


MILESTONE_FILE_PATTERN = re.compile(r"^(?P<id>M\d{1,2})\b", re.IGNORECASE)
MILESTONE_IN_FILENAME = re.compile(
    r"(?ix)"
    r"(?P<id>M\d{1,2})"  # M1, M2, ..., M99
    r"[-_]"               # separator (date-MN-slug pattern from archive)
)
MILESTONE_REF = re.compile(r"\bM\d{1,2}\b", re.IGNORECASE)
SECTION_HEADING = re.compile(r"^##\s+(.+?)\s*$")
CHECKBOX = re.compile(r"^\s*-\s*\[[ x]\]\s*(?P<text>.+?)\s*$")
BULLET = re.compile(r"^\s*-\s+(?P<text>.+?)\s*$")

DEPENDENCY_SECTION_NAMES = frozenset({
    "dependencies", "depends on", "depends-on", "prerequisites", "preconditions",
})

DEPENDS_FIELD = re.compile(
    r"(?im)^\s*(?:\*\*)?(?:depends\s*on|dependencies|prerequisites?)(?:\*\*)?\s*:\s*(?P<list>.+?)\s*$"
)

AC_DEPENDS = re.compile(
    r"(?i)\(\s*depends?\s+on\s*:?\s*(?P<list>[^)]+?)\)"
)


@dataclass
class Finding:
    severity: str   # HIGH (cycle), MEDIUM (self-dependency), LOW, INFO
    category: str   # cycle | self_dependency | orphan_reference | parse_warning
    file: str
    line: int
    message: str
    cycle: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_id(raw: str) -> str:
    """Normalize 'm2' / 'M02' / ' M2 ' → 'M2'."""
    raw = raw.strip().upper()
    m = re.match(r"M0*(\d+)", raw)
    if m:
        return f"M{m.group(1)}"
    return raw


def parse_dependencies_from_text(text: str) -> set[str]:
    """Extract all milestone IDs from a comma/semicolon/space-separated text."""
    return {normalize_id(m.group(0)) for m in MILESTONE_REF.finditer(text)}


def parse_milestone_id(file_path: Path, text: str) -> str | None:
    """Derive this file's milestone ID.

    Priority:
      1. `Current milestone` section's first non-blank body line: `M2: ...`
      2. Filename pattern: `2026-04-30-M3-foo.md` → `M3`
      3. None (file isn't a milestone-shaped doc).
    """
    lines = text.splitlines()
    in_current = False
    for raw in lines:
        m = SECTION_HEADING.match(raw)
        if m:
            in_current = m.group(1).strip().lower() == "current milestone"
            continue
        if in_current and raw.strip():
            m = MILESTONE_FILE_PATTERN.match(raw.strip())
            if m:
                return normalize_id(m.group("id"))
            break

    # Fallback to filename
    m = MILESTONE_IN_FILENAME.search(file_path.name)
    if m:
        return normalize_id(m.group("id"))
    return None


def parse_dependencies(file_path: Path, text: str) -> tuple[set[str], list[Finding]]:
    """Extract dependencies declared in this file. Returns (deps, warnings)."""
    deps: set[str] = set()
    warnings: list[Finding] = []
    lines = text.splitlines()

    # Form 1 — `## Dependencies` section
    in_dep_section = False
    section_line = 0
    for i, raw in enumerate(lines, start=1):
        m = SECTION_HEADING.match(raw)
        if m:
            sec = m.group(1).strip().lower()
            in_dep_section = sec in DEPENDENCY_SECTION_NAMES
            if in_dep_section:
                section_line = i
            continue
        if in_dep_section:
            stripped = raw.strip()
            if not stripped:
                continue
            cm = CHECKBOX.match(raw)
            bm = BULLET.match(raw)
            text_content = None
            if cm:
                text_content = cm.group("text")
            elif bm:
                text_content = bm.group("text")
            if text_content:
                refs = parse_dependencies_from_text(text_content)
                deps.update(refs)

    # Form 2 — inline `Depends on: M1, M3` (anywhere)
    for i, raw in enumerate(lines, start=1):
        m = DEPENDS_FIELD.match(raw)
        if m:
            refs = parse_dependencies_from_text(m.group("list"))
            deps.update(refs)

    # Form 3 — per-AC `(depends on M2)`
    for i, raw in enumerate(lines, start=1):
        for m in AC_DEPENDS.finditer(raw):
            refs = parse_dependencies_from_text(m.group("list"))
            deps.update(refs)

    return deps, warnings


def find_milestone_files(plan_dir: Path, include_archive: bool) -> list[Path]:
    files: list[Path] = []
    current = plan_dir / "current.md"
    if current.exists():
        files.append(current)
    if include_archive:
        archive = plan_dir / "archive"
        if archive.exists():
            files.extend(sorted(archive.glob("*.md")))
    return files


def detect_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    """Return a list of cycles (each cycle is a list of nodes in order)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {n: WHITE for n in graph}
    cycles: list[list[str]] = []
    stack: list[str] = []
    seen_cycles: set[tuple[str, ...]] = set()

    def dfs(node: str):
        color[node] = GRAY
        stack.append(node)
        for nxt in sorted(graph.get(node, set())):
            if nxt not in color:
                color[nxt] = WHITE  # known node, even if not in graph keys
                graph.setdefault(nxt, set())
            if color[nxt] == GRAY:
                # Found cycle — extract from stack
                if nxt in stack:
                    start = stack.index(nxt)
                    cycle = stack[start:] + [nxt]
                    key = tuple(sorted(set(cycle)))  # dedupe rotations
                    if key not in seen_cycles:
                        seen_cycles.add(key)
                        cycles.append(cycle)
            elif color[nxt] == WHITE:
                dfs(nxt)
        color[node] = BLACK
        stack.pop()

    for node in list(graph):
        if color.get(node, WHITE) == WHITE:
            dfs(node)
    return cycles


def render_text(graph: dict[str, set[str]],
                findings: list[Finding],
                files_scanned: int) -> str:
    out = [f"dependency-cycle-detector: scanned {files_scanned} milestone file(s)", ""]
    if graph:
        out.append("Dependency graph (milestone → depends on):")
        for node in sorted(graph):
            deps = sorted(graph[node])
            if deps:
                out.append(f"  {node} → {', '.join(deps)}")
            else:
                out.append(f"  {node} → (no declared dependencies)")
        out.append("")

    if not findings:
        out.append("PASS — no cycles detected.")
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
            if f.cycle:
                out.append(f"    Cycle: {' → '.join(f.cycle)}")
        out.append("")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("plan_dir", help="Path to docs/planning/ (or equivalent)")
    p.add_argument("--json", action="store_true", help="Emit a single JSON object")
    p.add_argument("--include-archive", action="store_true",
                   help="Also scan docs/planning/archive/*.md (default: current.md only)")
    args = p.parse_args(argv)

    plan_dir = Path(args.plan_dir).resolve()
    if not plan_dir.exists() or not plan_dir.is_dir():
        print(f"error: plan dir not found: {plan_dir}", file=sys.stderr)
        return 2

    files = find_milestone_files(plan_dir, include_archive=args.include_archive)
    if not files:
        msg = f"no milestone files found under {plan_dir}"
        if args.json:
            print(json.dumps({"plan_dir": str(plan_dir), "files_scanned": 0,
                              "graph": {}, "findings": []}, indent=2))
        else:
            print(msg)
        return 0

    graph: dict[str, set[str]] = {}
    findings: list[Finding] = []

    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            findings.append(Finding("HIGH", "io_error", str(f), 0,
                                    f"Cannot read: {e}"))
            continue
        mid = parse_milestone_id(f, text)
        if mid is None:
            findings.append(Finding(
                "INFO", "no_milestone_id", str(f), 1,
                "Could not derive a milestone ID — skipping for graph purposes.",
            ))
            continue
        deps, warns = parse_dependencies(f, text)
        findings.extend(warns)
        if mid in deps:
            findings.append(Finding(
                severity="MEDIUM",
                category="self_dependency",
                file=str(f),
                line=1,
                message=f"{mid} declares itself as a dependency.",
                cycle=[mid, mid],
            ))
            deps.discard(mid)
        graph.setdefault(mid, set()).update(deps)
        # Ensure deps appear in the graph as nodes even with no outbound edges
        for d in deps:
            graph.setdefault(d, set())

    cycles = detect_cycles(graph)
    for cyc in cycles:
        findings.append(Finding(
            severity="HIGH",
            category="cycle",
            file=str(plan_dir),
            line=0,
            message=f"Dependency cycle detected: {' → '.join(cyc)}",
            cycle=cyc,
        ))

    if args.json:
        report = {
            "plan_dir": str(plan_dir),
            "files_scanned": len(files),
            "graph": {k: sorted(v) for k, v in graph.items()},
            "findings": [f.to_dict() for f in findings],
        }
        print(json.dumps(report, indent=2))
    else:
        print(render_text(graph, findings, len(files)))

    has_blocker = any(f.severity == "HIGH" for f in findings)
    return 1 if has_blocker else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
