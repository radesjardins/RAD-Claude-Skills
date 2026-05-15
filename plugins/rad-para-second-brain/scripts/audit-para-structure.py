#!/usr/bin/env python3
r"""
audit-para-structure.py — Validate a PARA folder structure.

PARA (Tiago Forte's framework) organizes a knowledge base into exactly four
top-level folders:

  Projects    — short-term efforts with measurable outcomes and a finish line
  Areas       — ongoing responsibilities with maintenance, no end date
  Resources   — reference material, read-mostly
  Archive     — completed projects, dormant areas, retired resources

This validator scans a directory and reports common anti-patterns:

  - Wrong number of top-level folders (must be exactly 4)
  - Top-level folders named other than the canonical four (case-insensitive)
  - "False projects" — Projects/* entries with no apparent outcome / end-state
  - "Topic folders" — Projects/* entries whose name reads as a topic (single
    noun, no verb, no date-shape) rather than a project (verb-noun, has-deadline)
  - Excessive active project count (warn at >10, info at >20)
  - Orphaned files at the root level (files outside the four canonical folders)

Severity:
  critical  — wrong top-level structure (PARA is broken)
  warning   — anti-patterns within an otherwise-correct structure
  info      — count-based observations

Heuristics are conservative — when in doubt, info not warning.

Usage:
  python3 audit-para-structure.py [<root>]
  python3 audit-para-structure.py <root> --json
  python3 audit-para-structure.py <root> --strict       # tighter heuristics

Output:
  Default — human-readable text. Exit 1 on warning/critical.
  --json   — single JSON object on stdout.
  Exit 2   — script error.

No third-party dependencies. Python 3.8+.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


CANONICAL_FOLDERS = ("Projects", "Areas", "Resources", "Archive")
CANONICAL_FOLDERS_LOWER = {f.lower() for f in CANONICAL_FOLDERS}

# Folders that suggest a non-PARA system has been mixed in
ANTI_PARA_FOLDERS = frozenset({
    "inbox", "todo", "notes", "documents", "downloads", "misc", "general",
    "stuff", "random", "untitled", "new folder",
})

# Words that signal "this name is a project" (verb-leading or outcome-shape)
PROJECT_VERB_PREFIXES = (
    "build", "ship", "launch", "write", "publish", "deliver", "create",
    "design", "implement", "migrate", "rewrite", "refactor", "research",
    "investigate", "decide", "choose", "evaluate", "plan", "draft",
    "produce", "record", "organize", "complete", "finish", "fix",
    "audit", "review", "prepare", "buy", "sell", "move", "renovate",
)
# Words that signal "topic" rather than "project"
TOPIC_WORDS = frozenset({
    "ideas", "thoughts", "notes", "stuff", "thinking", "general",
    "miscellaneous", "misc", "untitled", "topics", "things",
})

DATE_HINT = re.compile(r"(?:20\d{2}|q[1-4]|h[12]|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", re.IGNORECASE)
NUMBER_HINT = re.compile(r"\b\d+\b")


@dataclass
class Finding:
    severity: str  # critical | warning | info
    category: str
    code: str
    path: str
    message: str
    fix: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def is_hidden(name: str) -> bool:
    return name.startswith(".") or name == "$RECYCLE.BIN" or name == "System Volume Information"


def list_visible(p: Path) -> tuple[list[Path], list[Path]]:
    """Return (dirs, files) at this level, excluding hidden/system entries."""
    dirs, files = [], []
    try:
        for entry in p.iterdir():
            if is_hidden(entry.name):
                continue
            if entry.is_dir():
                dirs.append(entry)
            elif entry.is_file():
                files.append(entry)
    except OSError:
        pass
    return sorted(dirs, key=lambda x: x.name.lower()), sorted(files, key=lambda x: x.name.lower())


def looks_like_project_name(name: str) -> bool:
    """Heuristic: is this a project (verb-leading or outcome-shaped) vs topic?"""
    lower = name.lower().strip()
    # Strip leading date prefixes (2026-03-launch-x → launch-x)
    lower_clean = re.sub(r"^\d{4}[-_]?(?:\d{2}[-_]?)?(?:\d{2}[-_]?)?", "", lower)
    first_word = re.split(r"[\s_\-]", lower_clean.lstrip("-_ "))[0]
    if first_word in TOPIC_WORDS:
        return False
    if first_word in PROJECT_VERB_PREFIXES:
        return True
    # Date or number anywhere is a positive signal (deadline-shaped or version-shaped)
    if DATE_HINT.search(name):
        return True
    # Single-word topics are likely not projects
    if " " not in name and "_" not in name and "-" not in name and len(name.split()) <= 1:
        return False
    return True  # default: give benefit of the doubt


def project_has_outcome_marker(project_dir: Path) -> bool:
    """Heuristic: does this project directory contain anything that looks like an outcome
    or completion criterion?"""
    # Look for files named like README/CHARTER/PLAN/DEFINITION/SCOPE/OUTCOME/DOD/_index
    for f in project_dir.glob("*"):
        if not f.is_file():
            continue
        name = f.stem.lower()
        if name in {"readme", "charter", "plan", "definition", "scope",
                    "outcome", "dod", "_index", "00-readme", "0-readme",
                    "deliverable", "criteria"}:
            return True
        if name.endswith("plan") or name.endswith("outcome") or name.endswith("scope"):
            return True
    return False


def audit(root: Path, strict: bool, findings: list[Finding]) -> dict:
    top_dirs, top_files = list_visible(root)
    top_names_lower = {d.name.lower() for d in top_dirs}

    # 1. Exactly four canonical folders
    present = top_names_lower & CANONICAL_FOLDERS_LOWER
    missing = CANONICAL_FOLDERS_LOWER - top_names_lower
    extra = top_names_lower - CANONICAL_FOLDERS_LOWER

    if len(present) < 4:
        for m in sorted(missing):
            findings.append(Finding(
                severity="critical",
                category="structure",
                code=f"missing_canonical_folder:{m}",
                path=str(root / m.capitalize()),
                message=f"Canonical PARA folder '{m.capitalize()}' is missing.",
                fix=f"Create it: mkdir '{m.capitalize()}'",
            ))

    for e in sorted(extra):
        sev = "warning"
        msg = f"Top-level folder '{e}' is outside the canonical PARA four (Projects/Areas/Resources/Archive)."
        fix = "Move its contents into one of the four canonical folders, or remove the folder."
        if e in ANTI_PARA_FOLDERS:
            sev = "warning"
            msg = f"Top-level folder '{e}' is a non-PARA anti-pattern (inbox/todo/notes/etc.). Move into one of the four canonical folders."
        findings.append(Finding(
            severity=sev,
            category="structure",
            code=f"extra_top_level_folder:{e}",
            path=str(root / e),
            message=msg,
            fix=fix,
        ))

    # 2. Orphaned files at the root
    for f in top_files:
        # Allow README, .gitignore, .gitkeep, LICENSE — those are infrastructural
        if f.name.lower() in {"readme.md", "license", "license.md", ".gitignore",
                              ".gitkeep", ".gitattributes"}:
            continue
        findings.append(Finding(
            severity="warning",
            category="structure",
            code="orphan_root_file",
            path=str(f),
            message=f"File '{f.name}' sits at the root, outside the four canonical folders.",
            fix="Move it into Projects/, Areas/, Resources/, or Archive/ depending on its kind.",
        ))

    # 3. Inside Projects/: look for false-project / topic-shaped subdirs
    projects_dir = None
    for d in top_dirs:
        if d.name.lower() == "projects":
            projects_dir = d
            break

    active_project_count = 0
    if projects_dir is not None:
        project_subdirs, _ = list_visible(projects_dir)
        for p in project_subdirs:
            active_project_count += 1
            if not looks_like_project_name(p.name):
                findings.append(Finding(
                    severity="warning",
                    category="false_project",
                    code="topic_shaped_name",
                    path=str(p),
                    message=f"'{p.name}' reads as a topic, not a project. Projects should be verb-leading "
                            f"or have a clear outcome / date.",
                    fix=f"Rename to a project shape (e.g. 'Launch {p.name}', 'Migrate {p.name}', or move "
                        f"into Areas/ if this is an ongoing responsibility, or Resources/ if it's reference.",
                ))
            if strict and not project_has_outcome_marker(p):
                findings.append(Finding(
                    severity="info",
                    category="false_project",
                    code="no_outcome_marker",
                    path=str(p),
                    message=f"'{p.name}' has no README/CHARTER/PLAN/OUTCOME/DOD file declaring what done looks like.",
                    fix="Add a short README.md with the outcome and finish criteria.",
                ))

        # 4. Active project count
        if active_project_count > 20:
            findings.append(Finding(
                severity="warning",
                category="count",
                code="too_many_projects",
                path=str(projects_dir),
                message=f"{active_project_count} active projects. PARA recommends 5-10; above 20 suggests "
                        f"the list contains stale projects or false projects that should be Areas/Resources.",
                fix="Archive completed, demote stalled-but-permanent items to Areas/, "
                    "move reference material to Resources/.",
            ))
        elif active_project_count > 10:
            findings.append(Finding(
                severity="info",
                category="count",
                code="elevated_project_count",
                path=str(projects_dir),
                message=f"{active_project_count} active projects. PARA recommends 5-10; "
                        f"review whether all of these are truly active.",
            ))
        elif active_project_count == 0:
            findings.append(Finding(
                severity="info",
                category="count",
                code="no_active_projects",
                path=str(projects_dir),
                message="Projects/ is empty. Either there are genuinely no active projects, "
                        "or active work lives outside this PARA system.",
            ))

    return {
        "top_dirs": [d.name for d in top_dirs],
        "top_files": [f.name for f in top_files],
        "canonical_present": sorted(present),
        "canonical_missing": sorted(missing),
        "extra_top_level": sorted(extra),
        "active_project_count": active_project_count,
    }


def render_text(summary: dict, findings: list[Finding]) -> str:
    out = ["audit-para-structure", ""]
    out.append(f"Top-level folders: {summary['top_dirs']}")
    out.append(f"Top-level files:   {summary['top_files']}")
    out.append(f"Canonical present: {summary['canonical_present']}")
    if summary["canonical_missing"]:
        out.append(f"Canonical MISSING: {summary['canonical_missing']}")
    if summary["extra_top_level"]:
        out.append(f"Non-canonical:     {summary['extra_top_level']}")
    out.append(f"Active projects:   {summary['active_project_count']}")
    out.append("")
    if not findings:
        out.append("PASS — PARA structure is sound.")
        return "\n".join(out)
    by_sev = {"critical": [], "warning": [], "info": []}
    for f in findings:
        by_sev.setdefault(f.severity, []).append(f)
    for sev in ("critical", "warning", "info"):
        items = by_sev.get(sev, [])
        if not items:
            continue
        out.append(f"[{sev.upper()}] {len(items)} finding{'s' if len(items) != 1 else ''}")
        for f in items:
            out.append(f"  {f.code}  {f.path}")
            out.append(f"    {f.message}")
            if f.fix:
                out.append(f"    fix: {f.fix}")
        out.append("")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("root", nargs="?", default=".")
    p.add_argument("--strict", action="store_true", help="Tighten heuristics (flag missing project outcome markers)")
    p.add_argument("--json", action="store_true", help="Emit a single JSON object")
    args = p.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        print(f"error: root not found: {root}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    summary = audit(root, args.strict, findings)

    if args.json:
        out = {
            "validator": "audit-para-structure",
            "version": "1.0.0",
            "root": str(root),
            "strict": args.strict,
            "summary": summary,
            "findings": [f.to_dict() for f in findings],
        }
        print(json.dumps(out, indent=2))
    else:
        print(render_text(summary, findings))

    has_blocker = any(f.severity in ("critical", "warning") for f in findings)
    return 1 if has_blocker else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
