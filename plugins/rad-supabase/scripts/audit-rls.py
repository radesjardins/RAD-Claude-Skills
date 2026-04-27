#!/usr/bin/env python3
"""
audit-rls.py — Static audit of Supabase migration SQL for RLS / policy / SECURITY DEFINER issues.

Mirrors a subset of Supabase Splinter lints that can be checked without a live database:
  0002 auth_users_exposed              — views in non-internal schemas selecting from auth.users
  0003 auth_rls_initplan               — policies using bare auth.uid() / auth.jwt() / auth.role()
                                         (recommend (select auth.<fn>()) for initPlan caching)
  0008 rls_enabled_no_policy           — table has `enable row level security` but no policies
                                         in any scanned migration
  0011 function_search_path_mutable    — SECURITY DEFINER function without
                                         `set search_path = ...`
  0013 rls_disabled_in_public          — `create table public.X` without a matching
                                         `enable row level security` in any scanned migration
  0015 rls_references_user_metadata    — policy expressions referencing raw_user_meta_data
                                         (user-writable, never trustworthy in RLS)

Plus structural checks not in Splinter:
  - Policy with `using (true)` and no `with check` on insert/update
  - `FOR ALL` policies (recommend separate select/insert/update/delete policies)

Targets: supabase/migrations/*.sql by default.

Pure stdlib Python 3.8+. Exits 0 (clean), 1 (warnings only), 2 (critical findings).

Usage:
    python audit-rls.py [PATH ...] [--json] [--migrations-dir DIR]

If no PATH given and --migrations-dir is unset, defaults to ./supabase/migrations.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Iterable


# -----------------------------------------------------------------------------
# Severity
# -----------------------------------------------------------------------------
CRITICAL = "critical"
WARNING = "warning"
INFO = "info"


@dataclass
class Finding:
    code: str
    severity: str
    file: str
    line: int
    message: str
    fix: str = ""


@dataclass
class Report:
    findings: list = field(default_factory=list)
    files_scanned: int = 0

    def add(self, **kw):
        self.findings.append(Finding(**kw))

    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == CRITICAL)

    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == WARNING)


# -----------------------------------------------------------------------------
# SQL preprocessing
# -----------------------------------------------------------------------------
_LINE_COMMENT_RE = re.compile(r"--[^\n]*")
_BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)


def strip_sql_comments(sql: str) -> str:
    sql = _BLOCK_COMMENT_RE.sub(" ", sql)
    sql = _LINE_COMMENT_RE.sub("", sql)
    return sql


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


# -----------------------------------------------------------------------------
# Patterns
# -----------------------------------------------------------------------------
CREATE_TABLE_RE = re.compile(
    r"create\s+table\s+(?:if\s+not\s+exists\s+)?(?:(?P<schema>[a-z0-9_]+)\s*\.\s*)?(?P<name>[a-z0-9_]+)\s*\(",
    re.IGNORECASE,
)

ENABLE_RLS_RE = re.compile(
    r"alter\s+table\s+(?:(?P<schema>[a-z0-9_]+)\s*\.\s*)?(?P<name>[a-z0-9_]+)\s+enable\s+row\s+level\s+security",
    re.IGNORECASE,
)

CREATE_POLICY_RE = re.compile(
    r"create\s+policy\s+\"?(?P<polname>[^\"]+?)\"?\s+on\s+(?:(?P<schema>[a-z0-9_]+)\s*\.\s*)?(?P<table>[a-z0-9_]+)\s+(?P<rest>(?:.|\n)*?);",
    re.IGNORECASE,
)

BARE_AUTH_FN_RE = re.compile(r"\b(auth\.(?:uid|jwt|role))\s*\(\s*\)", re.IGNORECASE)
SELECT_PREFIX_RE = re.compile(r"\(\s*select\s*$", re.IGNORECASE)

CREATE_FN_HEAD_RE = re.compile(
    r"create\s+(?:or\s+replace\s+)?function\s+(?P<sig>[^(]+\([^)]*\))",
    re.IGNORECASE,
)

SECURITY_DEFINER_RE = re.compile(r"\bsecurity\s+definer\b", re.IGNORECASE)
SET_SEARCH_PATH_RE = re.compile(r"\bset\s+search_path\s*(?:=|to)\s*", re.IGNORECASE)


def split_statements(sql: str):
    """Split SQL into (start_offset, statement_text), respecting dollar-quoted blocks ($$...$$, $tag$...$tag$)."""
    out = []
    i = 0
    n = len(sql)
    cur_start = 0
    while i < n:
        ch = sql[i]
        if ch == '$':
            tag_end = sql.find('$', i + 1)
            if 0 < tag_end - i < 100:
                tag = sql[i:tag_end + 1]
                close = sql.find(tag, tag_end + 1)
                if close != -1:
                    i = close + len(tag)
                    continue
        if ch == ';':
            out.append((cur_start, sql[cur_start:i + 1]))
            cur_start = i + 1
        i += 1
    if cur_start < n and sql[cur_start:].strip():
        out.append((cur_start, sql[cur_start:]))
    return out

CREATE_VIEW_RE = re.compile(
    r"create\s+(?:or\s+replace\s+)?view\s+(?:(?P<schema>[a-z0-9_]+)\s*\.\s*)?(?P<name>[a-z0-9_]+)\s+(?:with\s*\([^)]*\)\s+)?as\b(?P<body>(?:.|\n)*?);",
    re.IGNORECASE,
)
AUTH_USERS_REF_RE = re.compile(r"\bauth\s*\.\s*users\b", re.IGNORECASE)

USER_META_REF_RE = re.compile(r"\braw_user_meta_data\b", re.IGNORECASE)

INTERNAL_SCHEMAS = {
    "auth", "storage", "realtime", "supabase_functions", "supabase_migrations",
    "extensions", "graphql", "graphql_public", "pgsodium", "pgsodium_masks",
    "vault", "_analytics", "_realtime", "net", "pgbouncer",
}


# -----------------------------------------------------------------------------
# File scanning
# -----------------------------------------------------------------------------
def find_migration_files(paths, migrations_dir):
    files = []
    explicit = list(paths)
    if explicit:
        for p in explicit:
            if p.is_dir():
                files.extend(sorted(p.rglob("*.sql")))
            elif p.is_file():
                files.append(p)
        return files
    if migrations_dir and migrations_dir.is_dir():
        return sorted(migrations_dir.rglob("*.sql"))
    return files


# -----------------------------------------------------------------------------
# Audit passes
# -----------------------------------------------------------------------------
def audit_file(path, raw, report, public_tables_seen, rls_enabled_tables, policies_per_table):
    sql = strip_sql_comments(raw)
    rel = str(path)

    for m in CREATE_TABLE_RE.finditer(sql):
        schema = (m.group("schema") or "public").lower()
        name = m.group("name").lower()
        if schema == "public":
            key = f"{schema}.{name}"
            public_tables_seen.setdefault(key, (rel, line_of(raw, m.start())))

    for m in ENABLE_RLS_RE.finditer(sql):
        schema = (m.group("schema") or "public").lower()
        name = m.group("name").lower()
        rls_enabled_tables.add(f"{schema}.{name}")

    for m in CREATE_POLICY_RE.finditer(sql):
        schema = (m.group("schema") or "public").lower()
        table = m.group("table").lower()
        polname = m.group("polname")
        rest = m.group("rest") or ""
        full = m.group(0)
        line = line_of(raw, m.start())
        key = f"{schema}.{table}"
        policies_per_table.setdefault(key, []).append(polname)

        rest_lower = rest.lower()

        for am in BARE_AUTH_FN_RE.finditer(full):
            window_start = max(0, am.start() - 24)
            preceding = full[window_start:am.start()]
            if SELECT_PREFIX_RE.search(preceding):
                continue
            report.add(
                code="0003",
                severity=WARNING,
                file=rel,
                line=line + full[:am.start()].count("\n"),
                message=f"Policy \"{polname}\" on {key} uses bare {am.group(1)}() — "
                        "wrap in (select ...) for initPlan caching",
                fix=f"using ((select {am.group(1)}()) = ...)",
            )

        op_match = re.search(r"\bfor\s+(?P<op>all|select|insert|update|delete)\b", rest_lower)
        op = (op_match.group("op") if op_match else "all").lower()
        has_using_true = re.search(r"\busing\s*\(\s*true\s*\)", rest_lower) is not None
        has_with_check = re.search(r"\bwith\s+check\b", rest_lower) is not None
        if op in ("insert", "update", "all") and has_using_true and not has_with_check:
            report.add(
                code="STRUCT-using-true-no-check",
                severity=WARNING,
                file=rel,
                line=line,
                message=f"Policy \"{polname}\" on {key} (FOR {op.upper()}) uses USING (true) "
                        "without WITH CHECK — write path is unconstrained",
                fix="Add WITH CHECK (...) to constrain the values that can be inserted/updated",
            )

        if op == "all":
            report.add(
                code="STRUCT-for-all",
                severity=INFO,
                file=rel,
                line=line,
                message=f"Policy \"{polname}\" on {key} uses FOR ALL — "
                        "split into separate SELECT/INSERT/UPDATE/DELETE policies for clarity",
                fix="Create one policy per command; SELECT and DELETE use only USING; "
                    "INSERT uses only WITH CHECK; UPDATE uses both",
            )

        if USER_META_REF_RE.search(rest):
            report.add(
                code="0015",
                severity=CRITICAL,
                file=rel,
                line=line,
                message=f"Policy \"{polname}\" on {key} references raw_user_meta_data — "
                        "this column is user-writable and unsafe in RLS",
                fix="Use raw_app_meta_data (server-only) or a JWT custom claim populated by an "
                    "Auth Hook (Custom Access Token Hook)",
            )

    for stmt_start, stmt in split_statements(sql):
        head = CREATE_FN_HEAD_RE.search(stmt)
        if not head:
            continue
        if SECURITY_DEFINER_RE.search(stmt) and not SET_SEARCH_PATH_RE.search(stmt):
            sig = (head.group("sig") or "").strip()
            report.add(
                code="0011",
                severity=CRITICAL,
                file=rel,
                line=line_of(raw, stmt_start + head.start()),
                message=f"SECURITY DEFINER function {sig} has no SET search_path — "
                        "search_path is mutable and exploitable",
                fix="Add `set search_path = ''` (or an explicit schema list) to the function definition",
            )

    for m in CREATE_VIEW_RE.finditer(sql):
        schema = (m.group("schema") or "public").lower()
        name = m.group("name").lower()
        body = m.group("body") or ""
        if schema in INTERNAL_SCHEMAS:
            continue
        if AUTH_USERS_REF_RE.search(body):
            report.add(
                code="0002",
                severity=CRITICAL,
                file=rel,
                line=line_of(raw, m.start()),
                message=f"View {schema}.{name} references auth.users — exposes user PII via the API",
                fix="Drop the view, or replace with a function that filters columns and uses "
                    "SECURITY INVOKER (default).",
            )


def cross_file_lints(report, public_tables_seen, rls_enabled_tables, policies_per_table):
    for key, (rel, line) in public_tables_seen.items():
        if key not in rls_enabled_tables:
            report.add(
                code="0013",
                severity=CRITICAL,
                file=rel,
                line=line,
                message=f"Table {key} created without `enable row level security` — "
                        "any anon/authenticated client can read/write all rows",
                fix=f"alter table {key} enable row level security;",
            )

    for key in rls_enabled_tables:
        if key not in policies_per_table or not policies_per_table[key]:
            report.add(
                code="0008",
                severity=WARNING,
                file="(cross-file)",
                line=0,
                message=f"Table {key} has RLS enabled but no policies — all access is denied",
                fix="Add at least one policy, or document that the table is intentionally locked.",
            )


# -----------------------------------------------------------------------------
# Output
# -----------------------------------------------------------------------------
def render_text(report):
    lines = []
    crit = report.critical_count()
    warn = report.warning_count()
    info = sum(1 for f in report.findings if f.severity == INFO)
    lines.append(f"audit-rls — scanned {report.files_scanned} file(s)")
    lines.append(f"  critical: {crit}   warning: {warn}   info: {info}")
    lines.append("")
    if not report.findings:
        lines.append("  no findings")
        return "\n".join(lines)
    by_sev = {CRITICAL: [], WARNING: [], INFO: []}
    for f in report.findings:
        by_sev.setdefault(f.severity, []).append(f)
    for sev in (CRITICAL, WARNING, INFO):
        items = by_sev.get(sev, [])
        if not items:
            continue
        lines.append(f"--- {sev.upper()} ({len(items)}) ---")
        for f in items:
            loc = f"{f.file}:{f.line}" if f.line else f.file
            lines.append(f"  [{f.code}] {loc}")
            lines.append(f"    {f.message}")
            if f.fix:
                lines.append(f"    fix: {f.fix}")
        lines.append("")
    return "\n".join(lines)


def render_json(report):
    return json.dumps(
        {
            "files_scanned": report.files_scanned,
            "summary": {
                "critical": report.critical_count(),
                "warning": report.warning_count(),
                "info": sum(1 for f in report.findings if f.severity == INFO),
            },
            "findings": [asdict(f) for f in report.findings],
        },
        indent=2,
    )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main(argv=None):
    p = argparse.ArgumentParser(description="Static RLS / policy audit for Supabase migrations.")
    p.add_argument("paths", nargs="*", type=Path, help="SQL files or directories to scan")
    p.add_argument("--migrations-dir", type=Path, default=None,
                   help="Migrations directory (default: ./supabase/migrations if no paths given)")
    p.add_argument("--json", action="store_true", help="Output JSON instead of text")
    args = p.parse_args(argv)

    migrations_dir = args.migrations_dir
    if not args.paths and migrations_dir is None:
        default = Path("supabase/migrations")
        if default.is_dir():
            migrations_dir = default

    files = find_migration_files(args.paths, migrations_dir)
    if not files:
        msg = "no .sql files found to scan"
        if args.json:
            print(json.dumps({"error": msg, "files_scanned": 0, "findings": []}))
        else:
            print(msg)
        return 0

    report = Report(files_scanned=len(files))
    public_tables_seen = {}
    rls_enabled_tables = set()
    policies_per_table = {}

    for path in files:
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            report.add(
                code="IO",
                severity=WARNING,
                file=str(path),
                line=0,
                message=f"could not read file: {e}",
            )
            continue
        audit_file(path, raw, report, public_tables_seen, rls_enabled_tables, policies_per_table)

    cross_file_lints(report, public_tables_seen, rls_enabled_tables, policies_per_table)

    out = render_json(report) if args.json else render_text(report)
    print(out)
    if report.critical_count() > 0:
        return 2
    if report.warning_count() > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
