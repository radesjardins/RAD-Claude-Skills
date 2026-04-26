#!/usr/bin/env python3
"""
plan-lint.py — Mechanical validation for rad-planner task files.

This script converts the rad-planner README's "DAG enforcement / failure-state coverage"
claims from aspirational to actual. It parses a tasks file produced by rad-planner and
runs deterministic checks that an LLM can miss.

Modes:
  dag        DAG integrity — cycles, orphans, phantom dependencies, complexity caps.
  checklist  Field presence (Validation, Rollback, Dependencies, Complexity, Test Strategy)
             plus vague-language detection on validation/rollback fields.
  status     Task state report — % complete, blocked, next eligible by dependency.
  all        Run dag + checklist (status excluded; invoke separately for reports).

Usage:
  python3 plan-lint.py --mode dag tasks.md
  python3 plan-lint.py --mode all tasks.md --json
  python3 plan-lint.py --mode status tasks.md

Input format: see references/task-format.md. Tasks are parsed by matching the documented
markdown shape:
  - [ ] **[STATE]** TASK_ID: Title
    - **Field name:** value

Tolerant of minor formatting drift (extra whitespace, optional bold). Strict on the
task-id/state pattern that downstream agents rely on.

Output:
  Default — human-readable text, exit code 1 if any issue, else 0.
  --json   — single JSON object on stdout for skill consumption, same exit semantics.
  Exit 2 reserved for script errors (file not found, parse failure beyond recovery).

This script has no third-party dependencies and runs on Python 3.8+.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterable

VALID_STATES = {"PENDING", "IN PROGRESS", "BLOCKED", "DONE", "VERIFIED", "DEFERRED"}
COMPLETED_STATES = {"DONE", "VERIFIED"}
VAGUE_PHRASES = (
    "verify it works",
    "verify that it works",
    "check that it works",
    "make sure it runs",
    "make sure it works",
    "ensure functionality",
    "ensure it works",
    "confirm it's working",
    "confirm it is working",
    "test it manually",
    "looks right",
    "looks good",
    "should work",
    "tbd",
    "to be determined",
)

TASK_HEADER = re.compile(
    r"""^\s*-\s*\[(?P<box>[ x])\]\s*
        (?:\*\*)?\[(?P<state>[A-Z][A-Z\s]*)\](?:\*\*)?\s*
        (?P<id>[A-Za-z0-9.]+):\s*
        (?P<title>.+?)\s*$""",
    re.VERBOSE,
)
FIELD_LINE = re.compile(
    r"""^\s*-\s*(?:\*\*)?(?P<name>[A-Za-z][A-Za-z \-/]+?)(?:\*\*)?:\s*(?P<value>.*)$"""
)
DEP_TOKEN = re.compile(r"[A-Za-z0-9.]+")


@dataclass
class Task:
    id: str
    title: str
    state: str
    line: int
    fields: dict[str, str] = field(default_factory=dict)
    dependencies: list[str] = field(default_factory=list)

    @property
    def complexity(self) -> int | None:
        raw = self.fields.get("Complexity")
        if not raw:
            return None
        match = re.search(r"\d+", raw)
        return int(match.group()) if match else None

    @property
    def is_complete(self) -> bool:
        return self.state in COMPLETED_STATES


@dataclass
class Issue:
    severity: str  # CRITICAL | HIGH | MEDIUM | LOW
    category: str  # dag | checklist | status
    task_id: str | None
    message: str
    fix: str

    def to_dict(self) -> dict:
        return asdict(self)


# ---------- parsing ----------


def parse_tasks(text: str) -> tuple[list[Task], list[Issue]]:
    tasks: list[Task] = []
    parse_issues: list[Issue] = []
    current: Task | None = None

    for lineno, raw in enumerate(text.splitlines(), start=1):
        header = TASK_HEADER.match(raw)
        if header:
            state = header.group("state").strip()
            if state not in VALID_STATES:
                parse_issues.append(
                    Issue(
                        severity="MEDIUM",
                        category="checklist",
                        task_id=header.group("id"),
                        message=f"Unknown state '[{state}]' at line {lineno}",
                        fix=f"Use one of: {', '.join(sorted(VALID_STATES))}",
                    )
                )
            current = Task(
                id=header.group("id"),
                title=header.group("title").strip(),
                state=state,
                line=lineno,
            )
            tasks.append(current)
            continue

        if current is None:
            continue

        # Stop attaching fields to a task once we hit a blank-line boundary
        # followed by a non-indented line. Cheap heuristic: a non-indented `#` or `-`
        # at column 0 ends the previous task block.
        if raw and not raw.startswith((" ", "\t")) and raw.lstrip().startswith(("#", "-", "|")):
            current = None
            continue

        fld = FIELD_LINE.match(raw)
        if not fld:
            continue
        name = fld.group("name").strip()
        value = fld.group("value").strip()
        # Normalize a few common header variants
        canonical = {
            "deps": "Dependencies",
            "dependency": "Dependencies",
            "rollback procedure": "Rollback",
            "validation check": "Validation",
            "test strategy": "Test Strategy",
            "definition of done": "Definition of Done",
            "anti-pattern watch": "Anti-Pattern Watch",
        }.get(name.lower(), name)
        current.fields[canonical] = value

        if canonical == "Dependencies":
            current.dependencies = parse_deps(value)

    return tasks, parse_issues


def parse_deps(value: str) -> list[str]:
    if not value:
        return []
    cleaned = value.strip().lower()
    if cleaned in {"none", "n/a", "[]", "[none]", "-"}:
        return []
    # Strip enclosing brackets / backticks
    stripped = value.strip().strip("`[]")
    if not stripped or stripped.lower() in {"none", "n/a"}:
        return []
    return [tok for tok in DEP_TOKEN.findall(stripped) if tok.lower() != "none"]


# ---------- DAG checks ----------


def check_dag(tasks: list[Task]) -> list[Issue]:
    issues: list[Issue] = []
    by_id = {t.id: t for t in tasks}

    # Phantom dependencies
    for t in tasks:
        for dep in t.dependencies:
            if dep not in by_id:
                issues.append(
                    Issue(
                        severity="HIGH",
                        category="dag",
                        task_id=t.id,
                        message=f"Phantom dependency: {t.id} depends on '{dep}' which is not defined",
                        fix=f"Either define task '{dep}' or remove it from {t.id}'s Dependencies",
                    )
                )

    # Cycle detection (DFS with white/gray/black)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {t.id: WHITE for t in tasks}
    parent: dict[str, str | None] = {t.id: None for t in tasks}
    cycles: list[list[str]] = []

    def dfs(start: str) -> None:
        stack: list[tuple[str, Iterable[str]]] = [(start, iter(by_id[start].dependencies))]
        color[start] = GRAY
        while stack:
            node, deps = stack[-1]
            try:
                nxt = next(deps)
            except StopIteration:
                color[node] = BLACK
                stack.pop()
                continue
            if nxt not in by_id:
                continue  # phantom — already reported
            if color[nxt] == GRAY:
                # found a cycle: walk back from `node` to `nxt`
                cycle = [nxt, node]
                p = parent.get(node)
                while p and p != nxt:
                    cycle.append(p)
                    p = parent.get(p)
                cycles.append(list(reversed(cycle + [nxt])))
                continue
            if color[nxt] == WHITE:
                color[nxt] = GRAY
                parent[nxt] = node
                stack.append((nxt, iter(by_id[nxt].dependencies)))

    for t in tasks:
        if color[t.id] == WHITE:
            dfs(t.id)

    seen_cycles: set[tuple[str, ...]] = set()
    for cyc in cycles:
        # canonical form: rotate to smallest id first, then tuple
        if not cyc:
            continue
        idx = cyc.index(min(cyc))
        canonical = tuple(cyc[idx:] + cyc[:idx])
        if canonical in seen_cycles:
            continue
        seen_cycles.add(canonical)
        issues.append(
            Issue(
                severity="CRITICAL",
                category="dag",
                task_id=None,
                message=f"Circular dependency: {' → '.join(canonical)}",
                fix="Break the cycle at the least-coupled edge — usually by extracting shared setup into a new prerequisite task",
            )
        )

    # Complexity > 7 must have subtasks (= some other task's id starts with this id + ".")
    for t in tasks:
        if t.complexity is not None and t.complexity > 7:
            children = [other for other in tasks if other.id.startswith(t.id + ".")]
            if not children:
                issues.append(
                    Issue(
                        severity="HIGH",
                        category="dag",
                        task_id=t.id,
                        message=f"Complexity {t.complexity} > 7 without subtasks",
                        fix=f"Break {t.id} into subtasks {t.id}.1, {t.id}.2, ... each scoring ≤ 7",
                    )
                )

    return issues


# ---------- Checklist checks ----------


REQUIRED_FIELDS = ("Dependencies", "Validation", "Rollback", "Complexity")
CODE_TASK_FIELDS = ("Test Strategy",)


def check_checklist(tasks: list[Task]) -> list[Issue]:
    issues: list[Issue] = []
    for t in tasks:
        for fld in REQUIRED_FIELDS:
            if fld not in t.fields:
                issues.append(
                    Issue(
                        severity="HIGH" if fld in ("Validation", "Rollback") else "MEDIUM",
                        category="checklist",
                        task_id=t.id,
                        message=f"Missing required field: {fld}",
                        fix=f"Add a '- **{fld}:** ...' line to task {t.id}",
                    )
                )

        # Vague language in Validation / Rollback
        for fld in ("Validation", "Rollback"):
            value = t.fields.get(fld, "").lower()
            if not value:
                continue
            for phrase in VAGUE_PHRASES:
                if phrase in value:
                    issues.append(
                        Issue(
                            severity="HIGH",
                            category="checklist",
                            task_id=t.id,
                            message=f"{fld} contains vague phrase: '{phrase}'",
                            fix=f"Replace with a runnable command or specific verifiable condition",
                        )
                    )
                    break

        # Validation should look like a runnable command — at minimum, a non-trivial
        # length and not just prose. Heuristic: under 8 chars or no word-with-symbol
        # is suspicious.
        val = t.fields.get("Validation", "")
        if val and len(val) < 8:
            issues.append(
                Issue(
                    severity="MEDIUM",
                    category="checklist",
                    task_id=t.id,
                    message=f"Validation looks too short to be runnable: '{val}'",
                    fix="Provide an exact command (e.g., `npm test -- --grep auth`) or a clear verifiable condition",
                )
            )

    return issues


# ---------- Status report ----------


def status_report(tasks: list[Task]) -> dict:
    by_id = {t.id: t for t in tasks}
    state_counts: dict[str, int] = {}
    for t in tasks:
        state_counts[t.state] = state_counts.get(t.state, 0) + 1

    completed = sum(1 for t in tasks if t.is_complete)
    total = len(tasks)
    pct = round(100 * completed / total, 1) if total else 0.0

    next_eligible: list[str] = []
    blocked: list[dict] = []
    for t in tasks:
        if t.is_complete or t.state == "DEFERRED":
            continue
        unmet = [d for d in t.dependencies if d in by_id and not by_id[d].is_complete]
        if not unmet:
            next_eligible.append(t.id)
        else:
            blocked.append({"id": t.id, "blocked_by": unmet})

    return {
        "total": total,
        "completed": completed,
        "percent_complete": pct,
        "state_counts": state_counts,
        "next_eligible": next_eligible,
        "blocked": blocked,
    }


# ---------- output ----------


def render_text(report: dict, mode: str) -> str:
    lines: list[str] = []
    lines.append(f"plan-lint: mode={mode}  file={report['file']}")
    lines.append(f"tasks parsed: {report['task_count']}")

    if mode == "status":
        s = report["status"]
        lines.append("")
        lines.append(f"Progress: {s['completed']}/{s['total']} ({s['percent_complete']}%)")
        lines.append(f"State counts: {s['state_counts']}")
        if s["next_eligible"]:
            lines.append(f"Next eligible (deps satisfied): {', '.join(s['next_eligible'])}")
        else:
            lines.append("Next eligible: (none — all remaining tasks have unmet deps or are complete)")
        if s["blocked"]:
            lines.append("Blocked tasks:")
            for b in s["blocked"]:
                lines.append(f"  {b['id']} ← blocked by {', '.join(b['blocked_by'])}")
        return "\n".join(lines)

    issues = report["issues"]
    if not issues:
        lines.append("")
        lines.append("OK — no issues found.")
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
            tag = f"[{i['task_id']}]" if i["task_id"] else "[plan-level]"
            lines.append(f"  {sev} {tag} ({i['category']}) {i['message']}")
            lines.append(f"      fix: {i['fix']}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", help="Path to tasks.md (or implementation_plan.md if tasks are inline)")
    p.add_argument("--mode", choices=("dag", "checklist", "status", "all"), default="all")
    p.add_argument("--json", action="store_true", help="Emit a single JSON object instead of text")
    args = p.parse_args(argv)

    file_path = Path(args.path)
    if not file_path.exists():
        print(f"error: file not found: {file_path}", file=sys.stderr)
        return 2

    text = file_path.read_text(encoding="utf-8", errors="replace")
    tasks, parse_issues = parse_tasks(text)

    issues: list[Issue] = list(parse_issues)
    if args.mode in ("dag", "all"):
        issues.extend(check_dag(tasks))
    if args.mode in ("checklist", "all"):
        issues.extend(check_checklist(tasks))

    report: dict = {
        "file": str(file_path),
        "mode": args.mode,
        "task_count": len(tasks),
        "issues": [i.to_dict() for i in issues],
    }
    if args.mode == "status":
        report["status"] = status_report(tasks)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_text(report, args.mode))

    if args.mode == "status":
        return 0
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
