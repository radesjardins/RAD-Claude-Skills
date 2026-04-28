#!/usr/bin/env python3
"""
lint-aria.py — Wraps eslint-plugin-jsx-a11y when available; regex fallback otherwise.

Behavior:
  - If `eslint-plugin-jsx-a11y` is in package.json and `npx` is on PATH,
    runs `npx eslint --no-eslintrc -c <generated-config> --format json <files>`
    against a minimal config that loads the plugin's recommended ruleset.
    Parses the JSON result into rad-a11y's finding format.
  - If the plugin isn't installed (or `npx` isn't available), falls back to
    a curated regex ruleset covering ~10 of the highest-confidence
    jsx-a11y rules. Findings are tagged [STATIC] (regex fallback) or
    [STATIC] (real eslint).

Pure stdlib Python 3.8+ for the fallback. Subprocess for the wrapper path.

Honest scope:
  - The wrapper trusts `npx eslint`'s output verbatim — if eslint fails to
    parse a file (TS syntax errors, JSX weirdness), those files are skipped
    silently and counted in `parse_failures`.
  - The fallback regex set covers a deliberately limited rule subset. It is
    NOT a substitute for real eslint-plugin-jsx-a11y. Always recommend the
    user install the real plugin if they don't have it.
  - Does NOT install eslint-plugin-jsx-a11y for the user. Detects, runs,
    or falls back. The caller decides what to do about a missing plugin.

Usage:
  lint-aria.py <path>             # auto-detect, run best available
  lint-aria.py <path> --fallback  # force regex fallback even if plugin exists
  lint-aria.py <path> --no-fallback  # error if plugin missing (CI use)
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_EXCLUDES = {
    "node_modules", "dist", "build", ".next", ".astro", "coverage",
    ".turbo", ".cache", ".git", ".svelte-kit", "out", ".vercel",
}

SCANNED_EXTS = {".tsx", ".jsx"}

ESLINT_CONFIG = {
    "parser": "@typescript-eslint/parser",
    "parserOptions": {
        "ecmaVersion": "latest",
        "sourceType": "module",
        "ecmaFeatures": {"jsx": True},
    },
    "plugins": ["jsx-a11y"],
    "extends": ["plugin:jsx-a11y/recommended"],
    "settings": {
        "jsx-a11y": {
            "components": {}
        }
    },
}

# Curated regex fallback rules
# Each is (name, wcag, severity, pattern, description, fix)
FALLBACK_RULES = [
    (
        "alt-text",
        "1.1.1", "serious",
        re.compile(r"<img\b(?![^>]*\balt\s*=)[^>]*/?>", re.IGNORECASE),
        "Image missing alt attribute",
        "Add alt attribute. Use alt=\"\" for decorative images.",
    ),
    (
        "anchor-has-content",
        "2.4.4", "serious",
        re.compile(r"<a\b[^>]*>\s*</a>", re.IGNORECASE),
        "Anchor has no text content",
        "Add visible link text or aria-label.",
    ),
    (
        "no-autofocus",
        "2.4.3", "moderate",
        re.compile(r"\bautoFocus\b", re.IGNORECASE),
        "autoFocus disrupts user expectation of focus order",
        "Remove autoFocus unless absolutely necessary; "
        "prefer programmatic focus on user action.",
    ),
    (
        "no-distracting-elements",
        "2.2.2", "serious",
        re.compile(r"<(marquee|blink)\b", re.IGNORECASE),
        "<marquee> / <blink> are distracting and inaccessible",
        "Remove. Use CSS animations with prefers-reduced-motion if motion is needed.",
    ),
    (
        "tabindex-no-positive",
        "2.4.3", "moderate",
        re.compile(r'\btab[Ii]ndex\s*=\s*["\']?[1-9]\d*["\']?'),
        "Positive tabindex breaks natural DOM order",
        "Use tabindex=\"0\" or tabindex=\"-1\" only.",
    ),
    (
        "iframe-has-title",
        "2.4.1", "serious",
        re.compile(r"<iframe\b(?![^>]*\btitle\s*=)[^>]*>", re.IGNORECASE),
        "<iframe> missing title attribute",
        "Add a title attribute describing the iframe contents.",
    ),
    (
        "html-has-lang",
        "3.1.1", "serious",
        re.compile(r"<html\b(?![^>]*\blang\s*=)[^>]*>", re.IGNORECASE),
        "<html> missing lang attribute",
        "Add lang=\"en\" (or appropriate language code) to <html>.",
    ),
    (
        "scope",
        "1.3.1", "moderate",
        re.compile(r"<th\b[^>]*\bscope\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE),
        "<th scope> validation",
        "scope must be one of: row, col, rowgroup, colgroup.",
    ),
    (
        "media-has-caption",
        "1.2.2", "serious",
        re.compile(r"<video\b(?![^>]*<track\b[^>]*kind\s*=\s*[\"']captions[\"'])[^>]*>",
                    re.IGNORECASE | re.DOTALL),
        "<video> missing captions track",
        "Add <track kind=\"captions\" src=\"...\" /> as a child.",
    ),
    (
        "no-redundant-roles",
        "4.1.2", "minor",
        re.compile(r"<(button|nav|main|h[1-6])\b[^>]*\brole\s*=\s*[\"'](\w+)[\"']",
                    re.IGNORECASE),
        "Redundant ARIA role on native element",
        "Remove the role — native element already provides it.",
    ),
]


def has_jsx_a11y_installed(root: Path) -> bool:
    """Check whether eslint-plugin-jsx-a11y appears in package.json."""
    pkg = root / "package.json"
    if not pkg.exists():
        return False
    try:
        data = json.loads(pkg.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    deps = {}
    deps.update(data.get("dependencies", {}))
    deps.update(data.get("devDependencies", {}))
    return "eslint-plugin-jsx-a11y" in deps


def npx_available() -> bool:
    return shutil.which("npx") is not None


def run_real_eslint(root: Path, files: list) -> dict:
    """Run npx eslint with jsx-a11y/recommended. Return parsed result."""
    with tempfile.NamedTemporaryFile(
        "w", suffix=".json", delete=False, encoding="utf-8"
    ) as cfg:
        json.dump(ESLINT_CONFIG, cfg)
        cfg_path = cfg.name

    cmd = ["npx", "--yes", "eslint",
            "--no-eslintrc", "-c", cfg_path,
            "--format", "json",
            "--no-error-on-unmatched-pattern"]
    cmd.extend(str(f) for f in files)

    try:
        result = subprocess.run(
            cmd, cwd=root, capture_output=True, text=True, timeout=120,
        )
    except (subprocess.TimeoutExpired, OSError) as e:
        return {"ok": False, "error": str(e), "findings": []}
    finally:
        try:
            os.unlink(cfg_path)
        except OSError:
            pass

    # eslint exits 1 when findings exist; both 0 and 1 are normal
    if result.returncode not in (0, 1):
        return {
            "ok": False,
            "error": result.stderr.strip() or "eslint failed",
            "findings": [],
        }

    try:
        eslint_results = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "error": "eslint output not JSON",
                 "findings": []}

    findings = []
    parse_failures = 0
    for file_result in eslint_results:
        file_path = file_result.get("filePath", "").replace("\\", "/")
        if file_result.get("messages"):
            for msg in file_result["messages"]:
                rule = msg.get("ruleId") or "parse-error"
                if not rule.startswith("jsx-a11y/"):
                    if msg.get("fatal"):
                        parse_failures += 1
                    continue
                findings.append({
                    "category": rule.replace("jsx-a11y/", ""),
                    "wcag": "?",  # eslint doesn't surface WCAG; downstream maps it
                    "severity": "serious" if msg.get("severity") == 2 else "moderate",
                    "confidence": "STATIC",
                    "source": "eslint-plugin-jsx-a11y",
                    "file": file_path,
                    "line": msg.get("line", 1),
                    "column": msg.get("column", 1),
                    "snippet": (msg.get("source") or "").strip()[:200],
                    "message": msg.get("message", ""),
                    "fix": "",
                })
    return {"ok": True, "findings": findings, "parse_failures": parse_failures}


def line_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def run_fallback(root: Path, files: list) -> list:
    """Curated regex fallback ruleset."""
    findings = []
    for fp in files:
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
        file_str = str(fp).replace("\\", "/")
        for name, wcag, severity, pattern, msg, fix in FALLBACK_RULES:
            for m in pattern.finditer(text):
                findings.append({
                    "category": name,
                    "wcag": wcag,
                    "severity": severity,
                    "confidence": "STATIC",
                    "source": "regex-fallback",
                    "file": file_str,
                    "line": line_at(text, m.start()),
                    "snippet": m.group(0).strip()[:200],
                    "message": msg,
                    "fix": fix,
                })
    return findings


def iter_files(root: Path, excludes: set):
    if root.is_file():
        if root.suffix in SCANNED_EXTS:
            yield root
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in excludes]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix in SCANNED_EXTS:
                yield p


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ARIA / a11y lint via eslint-plugin-jsx-a11y when "
                    "available, regex fallback otherwise.",
    )
    parser.add_argument("path", help="File or directory to scan")
    parser.add_argument(
        "--exclude",
        default=",".join(sorted(DEFAULT_EXCLUDES)),
        help="Comma-separated dir names to exclude",
    )
    parser.add_argument("--pretty", action="store_true",
                         help="Human-readable output instead of JSON")
    parser.add_argument("--fallback", action="store_true",
                         help="Force regex fallback even if eslint-plugin-jsx-a11y is installed")
    parser.add_argument("--no-fallback", action="store_true",
                         help="Error out if eslint-plugin-jsx-a11y is not "
                              "installed (use this in CI to enforce setup)")
    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"error: path not found: {root}", file=sys.stderr)
        return 2

    project_root = root if root.is_dir() else root.parent
    excludes = {e.strip() for e in args.exclude.split(",") if e.strip()}
    files = list(iter_files(root, excludes))

    plugin_installed = has_jsx_a11y_installed(project_root)
    npx_ok = npx_available()

    use_real = (plugin_installed and npx_ok and not args.fallback)

    if not use_real and args.no_fallback:
        print(
            "error: eslint-plugin-jsx-a11y not installed (or npx unavailable) "
            "and --no-fallback was set. Install with: "
            "npm i -D eslint eslint-plugin-jsx-a11y",
            file=sys.stderr,
        )
        return 3

    if use_real:
        result = run_real_eslint(project_root, files)
        source = "eslint-plugin-jsx-a11y"
        ok = result["ok"]
        findings = result["findings"]
        parse_failures = result.get("parse_failures", 0)
        error = result.get("error")
    else:
        findings = run_fallback(project_root, files)
        source = "regex-fallback"
        ok = True
        parse_failures = 0
        error = None

    if args.pretty:
        for f in findings:
            print(f"[{f['severity'].upper()}] [{f['confidence']}] "
                   f"({f['source']}) {f['category']} — WCAG {f['wcag']}")
            print(f"  {f['file']}:{f['line']}")
            if f.get("snippet"):
                print(f"  {f['snippet']}")
            if f.get("message"):
                print(f"  {f['message']}")
            if f.get("fix"):
                print(f"  Fix: {f['fix']}")
            print()
        print(f"Source: {source}. Files: {len(files)}. Findings: {len(findings)}.")
        if parse_failures:
            print(f"Parse failures: {parse_failures}")
        if not ok:
            print(f"Error: {error}")
            print("Falling back to regex ruleset.")
            findings = run_fallback(project_root, files)
            print(f"Fallback findings: {len(findings)}")
    else:
        # If real-eslint failed, automatically fall back
        if not ok:
            findings = run_fallback(project_root, files)
            source = "regex-fallback"
        out = {
            "tool": "lint-aria",
            "version": "1.0.0",
            "source": source,
            "plugin_installed": plugin_installed,
            "npx_available": npx_ok,
            "real_eslint_ok": ok,
            "real_eslint_error": error,
            "files_scanned": len(files),
            "findings_count": len(findings),
            "parse_failures": parse_failures,
            "findings": findings,
            "recommendation": (
                None if use_real and ok else
                "Install eslint-plugin-jsx-a11y for higher-coverage a11y "
                "linting: `npm i -D eslint eslint-plugin-jsx-a11y` and add "
                "`{ \"extends\": [\"plugin:jsx-a11y/recommended\"] }` to "
                "your eslint config."
            ),
        }
        print(json.dumps(out, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
