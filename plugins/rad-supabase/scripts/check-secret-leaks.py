#!/usr/bin/env python3
"""
check-secret-leaks.py — Static scan for Supabase secret-key leaks and legacy-key usage.

Detects:
  - SUPABASE_SERVICE_ROLE_KEY / sb_secret_* / SUPABASE_SECRET_KEY referenced from client-side paths
    (heuristics: app/, pages/, src/components/, src/pages/, src/app/, public/, components/,
    routes/+page*.svelte, *.client.*).
  - Literal-string secret-shaped values in any tracked file:
      - sb_secret_<rand>  (new-format secret keys)
      - sb_publishable_<rand> in non-client config (warning only — these are client-safe)
      - eyJ... JWT-shaped strings >= 120 chars
      - sk_live_... / sk_test_... (Stripe)
  - .env files committed to git (anything matching .env, .env.local, .env.production, etc.,
    but NOT .env.example / .env.sample / .env.template).
  - Legacy SUPABASE_ANON_KEY / SUPABASE_SERVICE_ROLE_KEY references in .env.example
    (warning to migrate to sb_publishable_/sb_secret_).

Pure stdlib Python 3.8+. Exits 0 (clean), 1 (warnings only), 2 (critical findings).

Usage:
    python check-secret-leaks.py [PATH ...] [--json]

If no PATH given, defaults to current working directory.
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
# Path classification
# -----------------------------------------------------------------------------
CLIENT_INDICATORS = (
    "/app/", "/pages/", "/src/components/", "/src/pages/", "/src/app/", "/components/",
    "/public/", "/routes/", "/static/",
)
CLIENT_FILE_SUFFIXES = (".client.ts", ".client.tsx", ".client.js", ".client.jsx",
                        "+page.svelte", "+layout.svelte")
SERVER_INDICATORS = (
    "/api/", "/server/", "/lib/server/", "/src/server/", "/edge/", "/functions/",
    "/supabase/functions/", "/_server/", "/.netlify/", "/.vercel/", "/scripts/",
    "/api-routes/",
)
SERVER_FILE_SUFFIXES = (".server.ts", ".server.tsx", ".server.js", ".server.jsx",
                        "+page.server.ts", "+layout.server.ts", "+server.ts")

SKIP_DIRS = {".git", "node_modules", ".next", ".nuxt", "dist", "build", ".turbo",
             ".svelte-kit", ".output", ".cache", "out", ".vercel", ".netlify",
             "coverage", "__pycache__", ".pytest_cache"}
SKIP_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".pdf",
             ".woff", ".woff2", ".ttf", ".otf", ".eot",
             ".mp4", ".mov", ".avi", ".webm", ".mp3", ".wav",
             ".zip", ".tar", ".gz", ".7z", ".rar",
             ".lock", ".lockb"}

ENV_TEMPLATE_NAMES = {".env.example", ".env.sample", ".env.template", ".env.dist", ".env.defaults"}


def classify_path(path: Path) -> str:
    parts = "/" + str(path).replace("\\", "/").lstrip("./") + "/"
    name = path.name
    for suf in SERVER_FILE_SUFFIXES:
        if name.endswith(suf):
            return "server"
    for suf in CLIENT_FILE_SUFFIXES:
        if name.endswith(suf):
            return "client"
    is_server = any(s in parts for s in SERVER_INDICATORS)
    is_client = any(s in parts for s in CLIENT_INDICATORS)
    if is_server and not is_client:
        return "server"
    if is_client and not is_server:
        return "client"
    return "unknown"


# -----------------------------------------------------------------------------
# Patterns
# -----------------------------------------------------------------------------
SERVICE_ROLE_VAR_RE = re.compile(
    r"\b(SUPABASE_SERVICE_ROLE_KEY|SUPABASE_SECRET_KEY)\b"
)
SECRET_KEY_LITERAL_RE = re.compile(r"\bsb_secret_[A-Za-z0-9_-]{16,}")
PUBLISHABLE_KEY_LITERAL_RE = re.compile(r"\bsb_publishable_[A-Za-z0-9_-]{16,}")
JWT_LITERAL_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}")
STRIPE_LIVE_RE = re.compile(r"\bsk_live_[A-Za-z0-9]{20,}")
STRIPE_TEST_RE = re.compile(r"\bsk_test_[A-Za-z0-9]{20,}")
LEGACY_ANON_VAR_RE = re.compile(r"\bSUPABASE_ANON_KEY\b")


# -----------------------------------------------------------------------------
# File scanning
# -----------------------------------------------------------------------------
def iter_files(roots):
    for root in roots:
        if root.is_file():
            yield root
            continue
        if not root.is_dir():
            continue
        for p in root.rglob("*"):
            if p.is_dir():
                continue
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            if p.suffix.lower() in SKIP_EXTS:
                continue
            try:
                if p.stat().st_size > 2_000_000:
                    continue
            except OSError:
                continue
            yield p


def scan_file(path, report):
    name = path.name
    rel = str(path)

    if name == ".env" or (name.startswith(".env.") and name not in ENV_TEMPLATE_NAMES
                          and not name.endswith(".example") and not name.endswith(".sample")
                          and not name.endswith(".template")):
        report.add(
            code="ENV-FILE",
            severity=CRITICAL,
            file=rel,
            line=0,
            message=f"{name} is in the project tree — likely committed. .env files contain real secrets.",
            fix="Add to .gitignore, rotate any leaked secrets, and use .env.example for templates.",
        )

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    cls = classify_path(path)

    for ln, line in enumerate(text.splitlines(), start=1):
        sr = SERVICE_ROLE_VAR_RE.search(line)
        if sr:
            if cls == "client":
                report.add(
                    code="SERVICE-ROLE-CLIENT",
                    severity=CRITICAL,
                    file=rel,
                    line=ln,
                    message=f"{sr.group(1)} referenced from client-side path — bypasses ALL RLS",
                    fix="Move this code to a server-only path (route handler / edge function / "
                        "+page.server.ts). Service role / secret keys must never reach the browser.",
                )

        if SECRET_KEY_LITERAL_RE.search(line):
            report.add(
                code="LITERAL-SECRET-KEY",
                severity=CRITICAL,
                file=rel,
                line=ln,
                message="Literal sb_secret_... key in source — rotate immediately",
                fix="Replace with environment variable; rotate the leaked key in the dashboard.",
            )

        if JWT_LITERAL_RE.search(line):
            severity = CRITICAL if cls != "client" else WARNING
            report.add(
                code="LITERAL-JWT",
                severity=severity,
                file=rel,
                line=ln,
                message="JWT-shaped literal in source — likely a leaked Supabase or third-party key",
                fix="Move to environment variables and rotate any leaked legacy "
                    "anon/service_role keys (or migrate to sb_publishable_/sb_secret_).",
            )

        if STRIPE_LIVE_RE.search(line):
            report.add(
                code="LITERAL-STRIPE-LIVE",
                severity=CRITICAL,
                file=rel,
                line=ln,
                message="Stripe LIVE secret key in source — rotate immediately",
                fix="Move to environment variables and rotate at https://dashboard.stripe.com/apikeys",
            )
        if STRIPE_TEST_RE.search(line):
            report.add(
                code="LITERAL-STRIPE-TEST",
                severity=WARNING,
                file=rel,
                line=ln,
                message="Stripe TEST secret key in source — should still be in env vars",
                fix="Move to environment variables.",
            )

        if PUBLISHABLE_KEY_LITERAL_RE.search(line) and cls == "unknown" and name not in (
            ".env.example", ".env.sample", ".env.template",
        ):
            report.add(
                code="LITERAL-PUBLISHABLE-KEY",
                severity=INFO,
                file=rel,
                line=ln,
                message="sb_publishable_... key as literal — these are client-safe, "
                        "but env vars are still preferred",
                fix="Consider moving to environment variable for rotatability.",
            )

    if name in ENV_TEMPLATE_NAMES or name.endswith(".example") or name.endswith(".sample"):
        for ln, line in enumerate(text.splitlines(), start=1):
            if LEGACY_ANON_VAR_RE.search(line):
                report.add(
                    code="LEGACY-KEY-NAME",
                    severity=INFO,
                    file=rel,
                    line=ln,
                    message="SUPABASE_ANON_KEY is the legacy variable name — "
                            "new projects should use SUPABASE_PUBLISHABLE_KEY (sb_publishable_...)",
                    fix="Rename to SUPABASE_PUBLISHABLE_KEY when migrating off legacy keys.",
                )


# -----------------------------------------------------------------------------
# Output
# -----------------------------------------------------------------------------
def render_text(report):
    lines = []
    crit = report.critical_count()
    warn = report.warning_count()
    info = sum(1 for f in report.findings if f.severity == INFO)
    lines.append(f"check-secret-leaks — scanned {report.files_scanned} file(s)")
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
    p = argparse.ArgumentParser(description="Scan for Supabase secret-key leaks.")
    p.add_argument("paths", nargs="*", type=Path, help="Files or directories to scan")
    p.add_argument("--json", action="store_true", help="Output JSON instead of text")
    args = p.parse_args(argv)

    roots = args.paths if args.paths else [Path(".")]

    report = Report()
    count = 0
    for f in iter_files(roots):
        count += 1
        scan_file(f, report)
    report.files_scanned = count

    out = render_json(report) if args.json else render_text(report)
    print(out)
    if report.critical_count() > 0:
        return 2
    if report.warning_count() > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
