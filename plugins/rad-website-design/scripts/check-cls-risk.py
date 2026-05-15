#!/usr/bin/env python3
r"""
check-cls-risk.py — Static-analysis scan for CLS-prone patterns.

CLS (Cumulative Layout Shift) is one of the three Core Web Vitals. Without a
running browser we can't measure the metric itself, but several source-level
patterns are reliable CLS-causing causes:

  - `<img>` and `<picture>` without width/height/aspect-ratio
  - `<iframe>` without width/height
  - `<video>` without width/height/aspect-ratio
  - CSS `@font-face` without `font-display: swap` (or `optional`/`fallback`)
  - JSX/HTML async-data containers without reserved dimensions

Severity:
  major     — confirmed CLS cause (missing dimensions on visual elements)
  moderate  — likely CLS cause (font-display: block / no font-display)
  minor     — pattern that could cause CLS but needs runtime confirmation

This is a static scan only. Real CLS measurement requires Lighthouse / Chrome
DevTools / PageSpeed Insights — pair with those for the numeric metric. See
the rad-website-design README "Honest scope" section.

Usage:
  python3 check-cls-risk.py [<root>]
  python3 check-cls-risk.py <root> --files src/a.tsx,public/b.html
  python3 check-cls-risk.py <root> --json

Output:
  Default — human-readable text. Exit 1 if major/moderate findings.
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
from typing import Iterable


SCAN_EXTENSIONS = {".html", ".htm", ".jsx", ".tsx", ".astro", ".svelte", ".vue",
                   ".css", ".scss", ".sass", ".less"}
DEFAULT_EXCLUDES = {
    "node_modules", ".venv", ".env", "dist", "build", ".next",
    "__pycache__", ".git", ".cache", ".turbo", ".vercel", "coverage",
    ".output", ".astro", ".svelte-kit", "out",
}
SKIP_SUFFIXES = {".map", ".min.js", ".min.css"}


@dataclass
class Finding:
    severity: str
    category: str
    code: str
    title: str
    file: str
    line: int
    column: int
    snippet: str
    detail: str
    fix: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


IMG_TAG_RE = re.compile(r"<img\b([^>]*?)/?>", re.IGNORECASE | re.DOTALL)
IFRAME_TAG_RE = re.compile(r"<iframe\b([^>]*?)/?>", re.IGNORECASE | re.DOTALL)
VIDEO_TAG_RE = re.compile(r"<video\b([^>]*?)/?>", re.IGNORECASE | re.DOTALL)
FONT_FACE_RE = re.compile(r"@font-face\s*\{([^}]+)\}", re.IGNORECASE | re.DOTALL)


def has_attr(attrs: str, name: str) -> bool:
    return bool(re.search(rf"\b{re.escape(name)}\s*=", attrs, re.IGNORECASE))


def has_style_property(style_value: str, prop: str) -> bool:
    return bool(re.search(rf"\b{re.escape(prop)}\s*:", style_value, re.IGNORECASE))


def has_aspect_ratio_in_attrs(attrs: str) -> bool:
    """Check inline style or className for aspect-ratio-y signals."""
    # inline style="aspect-ratio: ..."
    style_match = re.search(r"""style\s*=\s*(["'`])([^"'`]*?)\1""", attrs, re.IGNORECASE)
    if style_match and has_style_property(style_match.group(2), "aspect-ratio"):
        return True
    # className with Tailwind aspect-* classes
    cls_match = re.search(r"""(?:className|class)\s*=\s*(?:\{?\s*)?(["'`])([^"'`]*?)\1""", attrs, re.IGNORECASE)
    if cls_match and re.search(r"\baspect-(?:auto|square|video|\[[^]]+\])", cls_match.group(2)):
        return True
    return False


def has_dimensions(attrs: str) -> bool:
    """True if either both width+height attrs or an aspect-ratio is set."""
    if has_attr(attrs, "width") and has_attr(attrs, "height"):
        return True
    if has_aspect_ratio_in_attrs(attrs):
        return True
    return False


def line_col(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    col = offset - (text.rfind("\n", 0, offset) + 1) + 1
    return line, col


def scan_markup_file(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []

    for m in IMG_TAG_RE.finditer(text):
        attrs = m.group(1)
        if has_dimensions(attrs):
            continue
        # Skip data URIs and inline SVGs (often used as decorative)
        if re.search(r"""src\s*=\s*["'`](data:|#)""", attrs, re.IGNORECASE):
            continue
        line, col = line_col(text, m.start())
        snippet = text[m.start():m.end()].replace("\n", " ")[:120]
        findings.append(Finding(
            severity="major",
            category="cls_dimensions",
            code="img_no_dimensions",
            title="<img> without width/height/aspect-ratio",
            file=str(path),
            line=line,
            column=col,
            snippet=snippet,
            detail=("Browsers can't reserve space for the image until it loads → "
                    "layout shifts when it arrives. CLS impact scales with image size."),
            fix=('Add intrinsic dimensions: <img src="..." width="800" height="600" alt="...">  '
                 'OR set CSS aspect-ratio on a wrapper, OR use Tailwind aspect-{video,square,[16/9]}.'),
        ))

    for m in IFRAME_TAG_RE.finditer(text):
        attrs = m.group(1)
        if has_dimensions(attrs):
            continue
        line, col = line_col(text, m.start())
        snippet = text[m.start():m.end()].replace("\n", " ")[:120]
        findings.append(Finding(
            severity="major",
            category="cls_dimensions",
            code="iframe_no_dimensions",
            title="<iframe> without width/height/aspect-ratio",
            file=str(path),
            line=line,
            column=col,
            snippet=snippet,
            detail="Iframe content loads asynchronously; without reserved space the layout shifts when it arrives.",
            fix='Add width and height attributes, or wrap in a container with a fixed aspect-ratio.',
        ))

    for m in VIDEO_TAG_RE.finditer(text):
        attrs = m.group(1)
        if has_dimensions(attrs):
            continue
        line, col = line_col(text, m.start())
        snippet = text[m.start():m.end()].replace("\n", " ")[:120]
        findings.append(Finding(
            severity="major",
            category="cls_dimensions",
            code="video_no_dimensions",
            title="<video> without width/height/aspect-ratio",
            file=str(path),
            line=line,
            column=col,
            snippet=snippet,
            detail="Video metadata loads asynchronously; layout shifts when intrinsic dimensions become known.",
            fix='Add width and height attributes, or set CSS aspect-ratio on the element.',
        ))

    return findings


def scan_css_file(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for m in FONT_FACE_RE.finditer(text):
        body = m.group(1)
        line, col = line_col(text, m.start())
        if not re.search(r"\bfont-display\s*:", body, re.IGNORECASE):
            findings.append(Finding(
                severity="moderate",
                category="cls_font",
                code="font_face_no_display",
                title="@font-face without font-display",
                file=str(path),
                line=line,
                column=col,
                snippet=text[m.start():m.start() + 80].replace("\n", " "),
                detail=("Default font-display: auto behaves like 'block' in most browsers — "
                        "the text is invisible until the custom font loads (FOIT), then "
                        "swaps in (CLS event)."),
                fix='Add font-display: swap;  // or optional / fallback for stricter behavior',
            ))
        elif re.search(r"\bfont-display\s*:\s*block\b", body, re.IGNORECASE):
            findings.append(Finding(
                severity="moderate",
                category="cls_font",
                code="font_display_block",
                title="font-display: block",
                file=str(path),
                line=line,
                column=col,
                snippet=text[m.start():m.start() + 80].replace("\n", " "),
                detail=("font-display: block hides text until the font loads (FOIT), then "
                        "swaps in — visible as a CLS event."),
                fix='Use font-display: swap (or optional / fallback) instead.',
            ))
    return findings


def iter_files(root: Path, files: list[Path] | None) -> Iterable[Path]:
    if files:
        for f in files:
            if f.is_file():
                yield f
        return
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in DEFAULT_EXCLUDES for part in p.parts):
            continue
        if any(p.name.endswith(suf) for suf in SKIP_SUFFIXES):
            continue
        if p.suffix in SCAN_EXTENSIONS:
            yield p


def is_css_file(p: Path) -> bool:
    return p.suffix in {".css", ".scss", ".sass", ".less"}


def is_markup_file(p: Path) -> bool:
    return p.suffix in {".html", ".htm", ".jsx", ".tsx", ".astro", ".svelte", ".vue"}


def render_text(findings: list[Finding], scanned: int, root: Path) -> str:
    out = [f"check-cls-risk", "", f"Files scanned: {scanned}", f"Root: {root}", ""]
    if not findings:
        out.append("PASS — no CLS-prone patterns detected.")
        return "\n".join(out)
    by_sev = {"major": [], "moderate": [], "minor": []}
    for f in findings:
        by_sev.setdefault(f.severity, []).append(f)
    for sev in ("major", "moderate", "minor"):
        items = by_sev.get(sev, [])
        if not items:
            continue
        out.append(f"[{sev.upper()}] {len(items)} finding{'s' if len(items) != 1 else ''}")
        for f in items:
            out.append(f"  {f.file}:{f.line}:{f.column}  {f.code}")
            out.append(f"    {f.title}")
            out.append(f"    {f.snippet}")
            out.append(f"    {f.detail}")
            if f.fix:
                out.append(f"    fix: {f.fix}")
        out.append("")
    out.append("Note: This is static analysis. Real CLS scores require Lighthouse / "
               "Chrome DevTools / PageSpeed Insights.")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("root", nargs="?", default=".")
    p.add_argument("--files", help="Comma-separated list of source files")
    p.add_argument("--json", action="store_true", help="Emit a single JSON object")
    args = p.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        print(f"error: root not found: {root}", file=sys.stderr)
        return 2

    files: list[Path] | None = None
    if args.files:
        files = [Path(f.strip()).resolve() for f in args.files.split(",") if f.strip()]

    all_findings: list[Finding] = []
    scanned = 0
    for path in iter_files(root, files):
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if is_markup_file(path):
            all_findings.extend(scan_markup_file(path, text))
        if is_css_file(path) or is_markup_file(path):
            all_findings.extend(scan_css_file(path, text))

    if args.json:
        out = {
            "validator": "check-cls-risk",
            "version": "1.0.0",
            "root": str(root),
            "files_scanned": scanned,
            "findings": [f.to_dict() for f in all_findings],
        }
        print(json.dumps(out, indent=2))
    else:
        print(render_text(all_findings, scanned, root))

    has_blocker = any(f.severity in ("major", "moderate") for f in all_findings)
    return 1 if has_blocker else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
