#!/usr/bin/env python3
r"""
audit-functions-permissions.py — Static audit of Supabase migration SQL for
PostgreSQL function permission patterns.

Companion to `audit-rls.py` (which mirrors Splinter lints 0002/0003/0008/0011/0013/0015).
This validator focuses on the function-permission dimension specifically:

  - CREATE FUNCTION in `public` schema with implicit EXECUTE TO PUBLIC
    (Postgres default — anyone with role membership can call)
  - SECURITY DEFINER functions in `public` schema (privilege-escalation risk
    if EXECUTE is not tightly granted)
  - Missing REVOKE EXECUTE FROM PUBLIC on SECURITY DEFINER functions
  - GRANT EXECUTE TO PUBLIC explicitly (review whether this is intended)
  - GRANT ALL ON ... TO PUBLIC (almost always wrong for Supabase)
  - Functions created without explicit `SET search_path` (already in audit-rls
    via Splinter 0011, but re-surfaced here for completeness when reviewers
    are looking at permissions in isolation)

Targets: `supabase/migrations/*.sql` by default. Mirrors audit-rls.py's CLI.

Severity:
  critical — GRANT EXECUTE TO PUBLIC on SECURITY DEFINER without prior REVOKE;
             GRANT ALL ON ... TO PUBLIC
  warning  — SECURITY DEFINER in public schema with no GRANT trace at all
             (implicit default = TO PUBLIC); missing REVOKE pattern
  info     — public-schema function without explicit GRANT/REVOKE controls
             (Postgres default is TO PUBLIC; explicit is safer)

Usage:
  python3 audit-functions-permissions.py [PATH ...] [--json] [--migrations-dir DIR]

Output:
  Default — human-readable text. Exit 1 if warnings; exit 2 if critical.
  --json   — single JSON object on stdout.

No third-party dependencies. Python 3.8+.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path


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

    def to_dict(self) -> dict:
        return asdict(self)


# CREATE [OR REPLACE] FUNCTION public.name(...) RETURNS ... [LANGUAGE ...] [...] AS $$ ... $$
# We need the function name, schema, body up to next CREATE/end-of-file.
CREATE_FN_RE = re.compile(
    r"""(?ix)
    \bCREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+
    (?:(?P<schema>[\"\w]+)\.)?
    (?P<name>[\"\w]+)
    \s*\(
    """,
)

GRANT_EXECUTE_RE = re.compile(
    r"(?ix)\bGRANT\s+EXECUTE\s+ON\s+(?:FUNCTION\s+)?(?:(?P<schema>[\"\w]+)\.)?(?P<name>[\"\w]+)\s*\([^)]*\)\s+TO\s+(?P<grantee>[\"\w]+)"
)
REVOKE_EXECUTE_RE = re.compile(
    r"(?ix)\bREVOKE\s+(?:ALL\s+(?:PRIVILEGES\s+)?|EXECUTE\s+)ON\s+(?:FUNCTION\s+)?(?:(?P<schema>[\"\w]+)\.)?(?P<name>[\"\w]+)\s*\([^)]*\)\s+FROM\s+(?P<grantee>[\"\w]+)"
)
GRANT_ALL_PUBLIC_RE = re.compile(
    r"(?ix)\bGRANT\s+ALL(?:\s+PRIVILEGES)?\s+ON\s+(?:TABLE\s+|SCHEMA\s+|SEQUENCE\s+)?(?:[\"\w.]+)\s+TO\s+PUBLIC\b"
)

SECURITY_DEFINER_RE = re.compile(r"(?i)\bSECURITY\s+DEFINER\b")
SET_SEARCH_PATH_RE = re.compile(r"(?i)\bSET\s+search_path\s*=")


def find_create_function_blocks(sql: str) -> list[tuple[int, int, str | None, str, bool, bool]]:
    """Return list of (start_line, end_line, schema, name, has_security_definer, has_set_search_path).

    'end_line' is heuristic — until next CREATE FUNCTION or 5000 chars later, whichever first.
    """
    out = []
    matches = list(CREATE_FN_RE.finditer(sql))
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(sql)
        # cap block at 5000 chars to avoid runaway false positives
        end = min(end, start + 5000)
        block = sql[start:end]
        start_line = sql.count("\n", 0, start) + 1
        end_line = sql.count("\n", 0, end) + 1
        schema = m.group("schema").strip('"') if m.group("schema") else None
        name = m.group("name").strip('"')
        has_definer = bool(SECURITY_DEFINER_RE.search(block))
        has_search_path = bool(SET_SEARCH_PATH_RE.search(block))
        out.append((start_line, end_line, schema, name, has_definer, has_search_path))
    return out


def collect_grants_revokes(sql: str):
    """Return ({(schema_or_None, name): set(grantees)}, {(schema_or_None, name): set(grantees)})."""
    grants: dict[tuple[str | None, str], set[str]] = {}
    revokes: dict[tuple[str | None, str], set[str]] = {}
    for m in GRANT_EXECUTE_RE.finditer(sql):
        schema = m.group("schema").strip('"') if m.group("schema") else None
        name = m.group("name").strip('"')
        grantee = m.group("grantee").strip('"').lower()
        grants.setdefault((schema, name), set()).add(grantee)
    for m in REVOKE_EXECUTE_RE.finditer(sql):
        schema = m.group("schema").strip('"') if m.group("schema") else None
        name = m.group("name").strip('"')
        grantee = m.group("grantee").strip('"').lower()
        revokes.setdefault((schema, name), set()).add(grantee)
    return grants, revokes


def audit_sql_file(path: Path, findings: list[Finding]) -> None:
    try:
        sql = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        findings.append(Finding(
            code="io_error", severity=CRITICAL, file=str(path), line=0,
            message=f"Cannot read file: {e}",
        ))
        return

    # GRANT ALL ... TO PUBLIC — almost always wrong
    for m in GRANT_ALL_PUBLIC_RE.finditer(sql):
        line = sql.count("\n", 0, m.start()) + 1
        findings.append(Finding(
            code="grant_all_to_public",
            severity=CRITICAL,
            file=str(path),
            line=line,
            message=f"GRANT ALL ... TO PUBLIC is almost always wrong for Supabase. "
                    f"Use granular grants to specific roles (anon, authenticated, service_role).",
            fix="Replace with GRANT SELECT/INSERT/UPDATE/DELETE on specific tables to "
                "specific roles, scoped by RLS policies.",
        ))

    fn_blocks = find_create_function_blocks(sql)
    grants, revokes = collect_grants_revokes(sql)

    for start_line, _, schema, name, has_definer, has_search_path in fn_blocks:
        key = (schema, name)
        in_public = schema == "public" or schema is None
        fn_grants = grants.get(key, set())
        fn_revokes = revokes.get(key, set())
        explicit_public_grant = "public" in fn_grants
        explicit_public_revoke = "public" in fn_revokes

        # CRITICAL: SECURITY DEFINER + GRANT EXECUTE TO PUBLIC without prior REVOKE
        if has_definer and explicit_public_grant and not explicit_public_revoke:
            findings.append(Finding(
                code="security_definer_grant_public_no_revoke",
                severity=CRITICAL,
                file=str(path),
                line=start_line,
                message=f"SECURITY DEFINER function "
                        f"{schema + '.' if schema else ''}{name} grants EXECUTE to "
                        f"PUBLIC without a preceding REVOKE. Anyone can call it with "
                        f"the function-owner's privileges.",
                fix=f"REVOKE EXECUTE ON FUNCTION {schema + '.' if schema else ''}"
                    f"{name}(<args>) FROM PUBLIC;\n"
                    f"GRANT EXECUTE ON FUNCTION {schema + '.' if schema else ''}"
                    f"{name}(<args>) TO authenticated;  -- or service_role",
            ))

        # WARNING: SECURITY DEFINER in public schema with no explicit GRANT/REVOKE trace
        if has_definer and in_public and not fn_grants and not fn_revokes:
            findings.append(Finding(
                code="security_definer_implicit_public_execute",
                severity=WARNING,
                file=str(path),
                line=start_line,
                message=f"SECURITY DEFINER function "
                        f"public.{name} has no explicit GRANT/REVOKE — Postgres "
                        f"default is EXECUTE TO PUBLIC, which means any role can "
                        f"call it with the owner's privileges.",
                fix=f"Add: REVOKE EXECUTE ON FUNCTION public.{name}(<args>) FROM PUBLIC;\n"
                    f"     GRANT EXECUTE ON FUNCTION public.{name}(<args>) TO authenticated;",
            ))

        # WARNING: SECURITY DEFINER without SET search_path (cross-link to Splinter 0011)
        if has_definer and not has_search_path:
            findings.append(Finding(
                code="security_definer_no_search_path",
                severity=WARNING,
                file=str(path),
                line=start_line,
                message=f"SECURITY DEFINER function "
                        f"{schema + '.' if schema else ''}{name} does not SET search_path. "
                        f"Splinter lint 0011 (function_search_path_mutable). "
                        f"Mutable search_path enables schema-injection attacks.",
                fix=f"Add to the function definition: SET search_path = public, extensions;\n"
                    f"(or whatever schemas the function actually needs)",
            ))

        # INFO: public-schema function without any explicit permission control
        if in_public and not has_definer and not fn_grants and not fn_revokes:
            findings.append(Finding(
                code="public_function_no_explicit_grants",
                severity=INFO,
                file=str(path),
                line=start_line,
                message=f"public.{name} has no explicit GRANT/REVOKE. Postgres "
                        f"default grants EXECUTE TO PUBLIC. For a Supabase project "
                        f"this is usually fine for read-only helpers but worth a "
                        f"second look for state-mutating functions.",
                fix=f"If intended: leave alone. Otherwise: REVOKE EXECUTE ON FUNCTION "
                    f"public.{name}(<args>) FROM PUBLIC and GRANT to specific roles.",
            ))


def render_text(all_findings: list[Finding], files_scanned: int) -> str:
    out = ["audit-functions-permissions", "", f"Files scanned: {files_scanned}", ""]
    if not all_findings:
        out.append("PASS — no function-permission issues detected.")
        return "\n".join(out)
    by_sev = {CRITICAL: [], WARNING: [], INFO: []}
    for f in all_findings:
        by_sev.setdefault(f.severity, []).append(f)
    for sev in (CRITICAL, WARNING, INFO):
        items = by_sev.get(sev, [])
        if not items:
            continue
        out.append(f"[{sev.upper()}] {len(items)} finding{'s' if len(items) != 1 else ''}")
        for f in items:
            out.append(f"  {f.code}  {f.file}:{f.line}")
            out.append(f"    {f.message}")
            if f.fix:
                out.append(f"    fix:\n      " + "\n      ".join(f.fix.splitlines()))
        out.append("")
    return "\n".join(out)


def iter_sql_files(paths: list[Path], migrations_dir: Path | None):
    seen: set[Path] = set()
    if migrations_dir:
        for p in sorted(migrations_dir.glob("*.sql")):
            if p not in seen:
                seen.add(p)
                yield p
    for p in paths:
        if p.is_file() and p.suffix == ".sql":
            if p not in seen:
                seen.add(p)
                yield p
        elif p.is_dir():
            for s in sorted(p.glob("**/*.sql")):
                if s not in seen:
                    seen.add(s)
                    yield s


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("paths", nargs="*", help="SQL files or directories (default: supabase/migrations)")
    p.add_argument("--migrations-dir", help="Migrations directory override")
    p.add_argument("--json", action="store_true", help="Emit a single JSON object")
    args = p.parse_args(argv)

    migrations_dir: Path | None = None
    if args.migrations_dir:
        migrations_dir = Path(args.migrations_dir).resolve()
    elif not args.paths:
        default = Path("supabase/migrations").resolve()
        if default.exists():
            migrations_dir = default

    paths = [Path(s).resolve() for s in args.paths]
    if not paths and not migrations_dir:
        print("error: no paths supplied and no supabase/migrations/ directory found", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    files = list(iter_sql_files(paths, migrations_dir))
    for sql_path in files:
        audit_sql_file(sql_path, findings)

    if args.json:
        out = {
            "validator": "audit-functions-permissions",
            "version": "1.0.0",
            "files_scanned": len(files),
            "findings": [f.to_dict() for f in findings],
        }
        print(json.dumps(out, indent=2))
    else:
        print(render_text(findings, len(files)))

    has_critical = any(f.severity == CRITICAL for f in findings)
    has_warning = any(f.severity == WARNING for f in findings)
    if has_critical:
        return 2
    if has_warning:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
