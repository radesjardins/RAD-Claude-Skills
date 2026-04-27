#!/usr/bin/env python3
"""
audit-edge-functions.py — Static audit of Supabase Edge Functions for current-best-practice
violations and security smells.

Targets supabase/functions/<name>/*.ts (and config.toml for verify_jwt overrides).

Checks:
  - Deprecated import: `import { serve } from "https://deno.land/std@*/http/server.ts"`
    (use `Deno.serve(...)` instead).
  - CORS wildcard `Access-Control-Allow-Origin: *` in responses.
  - Hardcoded API-key shaped strings (sk_live_*, sk_test_*, eyJ... JWTs >= 120 chars,
    sb_secret_*).
  - Stripe import older than v22:
      `import Stripe from "npm:stripe@<N>"` where N is missing or < 22.
  - `[functions.<name>] verify_jwt = false` in config.toml without a `#` comment
    explaining why (warning) or with a comment (info).

Pure stdlib Python 3.8+. Exits 0 (clean), 1 (warnings only), 2 (critical findings).

Usage:
    python audit-edge-functions.py [PATH ...] [--json] [--functions-dir DIR] [--config FILE]

Defaults to ./supabase/functions and ./supabase/config.toml if no paths given.
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
# Patterns
# -----------------------------------------------------------------------------
DEPRECATED_SERVE_RE = re.compile(
    r"""import\s*\{\s*serve\s*\}\s*from\s*["']https://deno\.land/std@[^"']+/http/server\.ts["']""",
    re.IGNORECASE,
)
CORS_WILDCARD_RE = re.compile(
    r"""['"]Access-Control-Allow-Origin['"]\s*[:,]\s*['"]\*['"]""",
    re.IGNORECASE,
)
STRIPE_IMPORT_RE = re.compile(
    r"""import\s+Stripe\s+from\s+["']npm:stripe(?:@(?P<ver>[^"']+))?["']"""
)
STRIPE_OK_MAJOR = 22

JWT_LITERAL_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}")
STRIPE_LIVE_RE = re.compile(r"\bsk_live_[A-Za-z0-9]{20,}")
STRIPE_TEST_RE = re.compile(r"\bsk_test_[A-Za-z0-9]{20,}")
SECRET_KEY_LITERAL_RE = re.compile(r"\bsb_secret_[A-Za-z0-9_-]{16,}")

CONFIG_FN_BLOCK_RE = re.compile(
    r"""\[functions\.(?P<name>[A-Za-z0-9_-]+)\](?P<body>(?:.|\n)*?)(?=^\[|\Z)""",
    re.MULTILINE,
)
VERIFY_JWT_FALSE_RE = re.compile(r"verify_jwt\s*=\s*false", re.IGNORECASE)


# -----------------------------------------------------------------------------
# Scanning
# -----------------------------------------------------------------------------
def find_function_files(paths, functions_dir):
    files = []
    if paths:
        for p in paths:
            if p.is_dir():
                files.extend(sorted(p.rglob("*.ts")))
                files.extend(sorted(p.rglob("*.tsx")))
                files.extend(sorted(p.rglob("*.js")))
            elif p.is_file():
                files.append(p)
        return files
    if functions_dir and functions_dir.is_dir():
        out = []
        out.extend(sorted(functions_dir.rglob("*.ts")))
        out.extend(sorted(functions_dir.rglob("*.tsx")))
        out.extend(sorted(functions_dir.rglob("*.js")))
        return out
    return files


def parse_stripe_major(version):
    if not version:
        return None
    v = version.strip()
    if v in ("latest", "next", "beta"):
        return None
    v = v.lstrip("^~")
    m = re.match(r"(\d+)", v)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None


def scan_function_file(path, report):
    rel = str(path)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    for ln, line in enumerate(text.splitlines(), start=1):
        if DEPRECATED_SERVE_RE.search(line):
            report.add(
                code="DEPRECATED-SERVE",
                severity=WARNING,
                file=rel,
                line=ln,
                message="Importing `serve` from deno.land/std is deprecated for Edge Functions",
                fix="Use the built-in `Deno.serve(...)` (no import needed in Deno 2.x).",
            )
        if CORS_WILDCARD_RE.search(line):
            report.add(
                code="CORS-WILDCARD",
                severity=WARNING,
                file=rel,
                line=ln,
                message="CORS Access-Control-Allow-Origin set to '*' — allows any origin to call this function",
                fix="Restrict to known origins, or document why wildcard is intentional "
                    "(public unauthenticated webhooks are one valid case).",
            )
        m = STRIPE_IMPORT_RE.search(line)
        if m:
            ver = m.group("ver") or ""
            major = parse_stripe_major(ver)
            if major is None:
                report.add(
                    code="STRIPE-UNPINNED",
                    severity=INFO,
                    file=rel,
                    line=ln,
                    message=f"Stripe imported without a pinned major version (saw '{ver or 'no version'}')",
                    fix=f"Pin to `npm:stripe@{STRIPE_OK_MAJOR}` or later.",
                )
            elif major < STRIPE_OK_MAJOR:
                report.add(
                    code="STRIPE-OUTDATED",
                    severity=WARNING,
                    file=rel,
                    line=ln,
                    message=f"Stripe v{major} is outdated (current major: {STRIPE_OK_MAJOR}+)",
                    fix=f"Upgrade to `npm:stripe@{STRIPE_OK_MAJOR}` (note: v22+ requires "
                        "`new Stripe(...)` constructor — it is now a true ES6 class).",
                )

        if SECRET_KEY_LITERAL_RE.search(line):
            report.add(
                code="LITERAL-SB-SECRET",
                severity=CRITICAL,
                file=rel,
                line=ln,
                message="Literal sb_secret_... key in edge function — rotate immediately",
                fix="Use Deno.env.get('SUPABASE_SECRET_KEY'); set via `supabase secrets set`.",
            )
        if JWT_LITERAL_RE.search(line):
            report.add(
                code="LITERAL-JWT",
                severity=CRITICAL,
                file=rel,
                line=ln,
                message="JWT-shaped literal in edge function — looks like a hardcoded service_role/anon key",
                fix="Use Deno.env.get(...) and `supabase secrets set` for any non-public key.",
            )
        if STRIPE_LIVE_RE.search(line):
            report.add(
                code="LITERAL-STRIPE-LIVE",
                severity=CRITICAL,
                file=rel,
                line=ln,
                message="Stripe LIVE secret key in edge function source",
                fix="Move to env var; rotate at https://dashboard.stripe.com/apikeys.",
            )
        if STRIPE_TEST_RE.search(line):
            report.add(
                code="LITERAL-STRIPE-TEST",
                severity=WARNING,
                file=rel,
                line=ln,
                message="Stripe TEST secret key in edge function source",
                fix="Move to env var.",
            )


def scan_config_toml(path, report):
    rel = str(path)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    for m in CONFIG_FN_BLOCK_RE.finditer(text):
        body = m.group("body") or ""
        name = m.group("name")
        if VERIFY_JWT_FALSE_RE.search(body):
            has_comment = re.search(r"^\s*#", body, re.MULTILINE) is not None
            severity = INFO if has_comment else WARNING
            report.add(
                code="VERIFY-JWT-FALSE",
                severity=severity,
                file=rel,
                line=text[:m.start()].count("\n") + 1,
                message=f"[functions.{name}] sets verify_jwt = false — function is publicly callable",
                fix="If intentional (webhook, public health check), add a `#` comment explaining "
                    "why; otherwise remove and rely on the default `verify_jwt = true`.",
            )


# -----------------------------------------------------------------------------
# Output
# -----------------------------------------------------------------------------
def render_text(report):
    lines = []
    crit = report.critical_count()
    warn = report.warning_count()
    info = sum(1 for f in report.findings if f.severity == INFO)
    lines.append(f"audit-edge-functions — scanned {report.files_scanned} file(s)")
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
    p = argparse.ArgumentParser(description="Static audit of Supabase Edge Functions.")
    p.add_argument("paths", nargs="*", type=Path, help="Files or directories to scan")
    p.add_argument("--functions-dir", type=Path, default=None,
                   help="Functions directory (default: ./supabase/functions if no paths given)")
    p.add_argument("--config", type=Path, default=None,
                   help="Path to supabase/config.toml (default: ./supabase/config.toml if present)")
    p.add_argument("--json", action="store_true", help="Output JSON instead of text")
    args = p.parse_args(argv)

    functions_dir = args.functions_dir
    if not args.paths and functions_dir is None:
        default = Path("supabase/functions")
        if default.is_dir():
            functions_dir = default

    files = find_function_files(args.paths, functions_dir)
    config_path = args.config
    if config_path is None:
        default_cfg = Path("supabase/config.toml")
        if default_cfg.is_file():
            config_path = default_cfg

    if not files and not config_path:
        msg = "no edge function source files found"
        if args.json:
            print(json.dumps({"error": msg, "files_scanned": 0, "findings": []}))
        else:
            print(msg)
        return 0

    report = Report(files_scanned=len(files))
    for f in files:
        scan_function_file(f, report)
    if config_path and config_path.is_file():
        scan_config_toml(config_path, report)
        report.files_scanned += 1

    out = render_json(report) if args.json else render_text(report)
    print(out)
    if report.critical_count() > 0:
        return 2
    if report.warning_count() > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
