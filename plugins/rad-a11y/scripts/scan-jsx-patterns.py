#!/usr/bin/env python3
"""
scan-jsx-patterns.py — High-confidence static a11y pattern scanner.

Scans .tsx / .jsx / .astro / .html / .svelte / .vue source for WCAG 2.2 AA
failure patterns that can be detected deterministically from source. Emits
findings as JSON for the /a11y-review skill and a11y-reviewer agent to
consume.

Designed to replace the LLM regex passes in a11y-review with deterministic
output. The LLM still handles [HEURISTIC] judgment (alt meaningfulness,
complex ARIA logic, reading order) — this script handles [STATIC] findings.

Pure stdlib Python 3.8+. No pip install required.

Patterns covered (all [STATIC] confidence):
  - outline-none / outline:none without focus-visible replacement
  - aria-hidden="true" on focusable elements
  - <img> missing alt attribute
  - Bad alt patterns (alt="image", alt="photo", alt="filename.jpg")
  - Hardcoded ARIA states in JSX (aria-expanded="true" string literal)
  - <div onClick> / <span onClick> without role + keyboard handlers
  - Redundant ARIA roles (role="button" on <button>, etc.)
  - tabindex > 0 (positive tabindex breaks DOM order)
  - <a> without href used as button substitute

Patterns explicitly NOT covered (kept for LLM [HEURISTIC] pass):
  - Whether alt text is meaningful (only checks presence + obvious bad values)
  - Empty buttons / icon-only labeling (cross-element analysis)
  - placeholder-as-label (cross-element)
  - Fieldset grouping correctness (cross-element)
  - Reading order (DOM-runtime concern)

Usage:
  scan-jsx-patterns.py <path>           # scan dir or file, JSON to stdout
  scan-jsx-patterns.py <path> --pretty  # human-readable instead
  scan-jsx-patterns.py <path> --exclude "node_modules,dist"

Exit code: always 0 (finding violations is not an error). Non-zero only on
fatal scan errors (path not readable, etc.).
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Iterable

DEFAULT_EXCLUDES = {
    "node_modules", "dist", "build", ".next", ".astro", "coverage",
    ".turbo", ".cache", ".git", ".svelte-kit", "out", ".vercel",
}

SCANNED_EXTENSIONS = {".tsx", ".jsx", ".astro", ".html", ".svelte", ".vue"}
CSS_EXTENSIONS = {".css", ".scss", ".module.css"}

# Elements that are natively focusable (default tabindex=0 in tab order)
FOCUSABLE_TAGS = {"button", "a", "input", "select", "textarea", "summary", "details"}

# WCAG criterion mapping per category
WCAG_MAP = {
    "outline-none-no-focus-visible": "2.4.7",
    "aria-hidden-on-focusable": "1.3.1",
    "missing-alt": "1.1.1",
    "bad-alt-value": "1.1.1",
    "hardcoded-aria-state": "4.1.2",
    "div-onclick-no-role": "4.1.2",
    "redundant-aria-role": "4.1.2",
    "positive-tabindex": "2.4.3",
    "anchor-no-href": "2.1.1",
}

SEVERITY_MAP = {
    "outline-none-no-focus-visible": "critical",
    "aria-hidden-on-focusable": "critical",
    "missing-alt": "serious",
    "bad-alt-value": "serious",
    "hardcoded-aria-state": "moderate",
    "div-onclick-no-role": "critical",
    "redundant-aria-role": "minor",
    "positive-tabindex": "moderate",
    "anchor-no-href": "serious",
}

FIX_MAP = {
    "outline-none-no-focus-visible":
        "Replace outline removal with a visible focus indicator. "
        "Tailwind: `focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500`. "
        "CSS: `:focus-visible { outline: 2px solid; outline-offset: 2px; }`.",
    "aria-hidden-on-focusable":
        "Remove aria-hidden, OR remove focusability (set tabindex=-1 and remove from interactive flow). "
        "Hidden focusable elements trap screen reader users.",
    "missing-alt":
        "Add alt attribute. Use alt=\"\" for purely decorative images, "
        "or descriptive alt text for informative images.",
    "bad-alt-value":
        "Replace generic/filename alt with a description of what the image conveys "
        "in context. If decorative, use alt=\"\".",
    "hardcoded-aria-state":
        "Drive the ARIA state from component state, not a string literal. "
        "JSX: aria-expanded={isOpen} (boolean), not aria-expanded=\"true\" (string).",
    "div-onclick-no-role":
        "Use a <button> instead, OR add role=\"button\", tabindex=\"0\", "
        "and keyboard handlers (onKeyDown for Enter and Space).",
    "redundant-aria-role":
        "Remove the role — the native element already provides it. "
        "Adding a redundant role is at best noise, at worst can confuse assistive tech.",
    "positive-tabindex":
        "Use tabindex=\"0\" (insert in DOM order) or tabindex=\"-1\" "
        "(programmatically focusable only). Positive values break natural tab order.",
    "anchor-no-href":
        "If it navigates, give it an href. If it's a button, use <button>. "
        "An <a> without href is not focusable by keyboard and not a button.",
}


def iter_files(root: Path, excludes: set, extensions: set) -> Iterable[Path]:
    """Walk root, yield files matching extensions and not under excludes."""
    if root.is_file():
        if root.suffix in extensions:
            yield root
        return

    for dirpath, dirnames, filenames in os.walk(root):
        # Mutate dirnames in-place to skip excluded subdirs
        dirnames[:] = [d for d in dirnames if d not in excludes]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix in extensions:
                yield p


def line_at(text: str, offset: int) -> int:
    """Return 1-based line number for a character offset in text."""
    return text.count("\n", 0, offset) + 1


def make_finding(category: str, file: str, line: int, snippet: str, extra: dict = None) -> dict:
    f = {
        "category": category,
        "wcag": WCAG_MAP.get(category, "?"),
        "severity": SEVERITY_MAP.get(category, "moderate"),
        "confidence": "STATIC",
        "file": file,
        "line": line,
        "snippet": snippet.strip()[:200],
        "fix": FIX_MAP.get(category, ""),
    }
    if extra:
        f.update(extra)
    return f


# ---------------------------------------------------------------------------
# Pattern detectors
# ---------------------------------------------------------------------------

# Match <tag ... > opening tags. Captures tag name and attribute string.
# Permissive — won't perfectly handle nested generics, but good enough for JSX.
TAG_OPEN_RE = re.compile(
    r"<([A-Za-z][A-Za-z0-9]*)((?:\s+[^>]*?)?)\s*/?>",
    re.DOTALL,
)


def detect_outline_none(file: str, text: str, ext: str) -> list:
    """outline-none / outline:none without focus-visible replacement."""
    findings = []

    if ext in CSS_EXTENSIONS:
        # CSS context: find `outline: none` or `outline: 0` per ruleset
        for m in re.finditer(r"outline\s*:\s*(none|0)\b", text):
            line = line_at(text, m.start())
            # Look for focus-visible in nearby ±400 chars
            window = text[max(0, m.start() - 400):m.end() + 400]
            if not re.search(r":focus(-visible)?\s*\{[^}]*outline\s*:", window):
                findings.append(make_finding(
                    "outline-none-no-focus-visible",
                    file, line,
                    text[m.start():m.end() + 60],
                ))
    else:
        # JSX/HTML context: find `outline-none` / `focus:outline-none` in className
        for m in re.finditer(r'className=(?:"([^"]+)"|\'([^\']+)\'|`([^`]+)`)', text):
            class_str = m.group(1) or m.group(2) or m.group(3) or ""
            if not re.search(r"\b(focus:)?outline-none\b", class_str):
                continue
            # Check for any focus-visible replacement on this element
            has_replacement = bool(re.search(
                r"\bfocus(?:-visible)?:(?:ring|outline|border|shadow)-",
                class_str,
            ))
            if not has_replacement:
                line = line_at(text, m.start())
                findings.append(make_finding(
                    "outline-none-no-focus-visible",
                    file, line,
                    class_str,
                ))
    return findings


def parse_attrs(attr_str: str) -> dict:
    """Parse JSX/HTML attribute string into a dict.

    Returns mapping of attr-name -> raw value string (with quotes/braces stripped
    where unambiguous). Boolean-style attrs map to True. Best-effort, not a
    full parser.
    """
    attrs = {}
    # name="value" or name='value' or name=`value`
    for m in re.finditer(
        r'\b([A-Za-z][A-Za-z0-9_:.-]*)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|`([^`]*)`|\{([^}]*)\})',
        attr_str,
    ):
        name = m.group(1)
        val = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else (
                m.group(4) if m.group(4) is not None else
                ("{" + (m.group(5) or "") + "}")
            )
        )
        attrs[name] = val
    # Boolean attrs (no =)
    for m in re.finditer(r'\b([A-Za-z][A-Za-z0-9_:-]*)\b(?!\s*=)', attr_str):
        name = m.group(1)
        if name not in attrs:
            attrs[name] = True
    return attrs


def detect_aria_hidden_on_focusable(file: str, text: str) -> list:
    """aria-hidden="true" on a focusable element."""
    findings = []
    for m in TAG_OPEN_RE.finditer(text):
        tag = m.group(1).lower()
        attr_str = m.group(2) or ""
        attrs = parse_attrs(attr_str)
        aria_hidden = attrs.get("aria-hidden")
        if not aria_hidden or aria_hidden in (False, "false"):
            continue
        # Truthy: "true", True, "{true}"
        is_truthy = (aria_hidden is True or
                     (isinstance(aria_hidden, str) and
                      aria_hidden.strip().lower() in ("true", "{true}", "")))
        if not is_truthy:
            continue
        # Is the element focusable?
        focusable = False
        if tag in FOCUSABLE_TAGS:
            if tag == "a":
                focusable = "href" in attrs
            elif tag in ("input", "select", "textarea", "button"):
                # Disabled inputs aren't focusable, but conservatively flag
                focusable = "disabled" not in attrs
            else:
                focusable = True
        elif "tabindex" in attrs or "tabIndex" in attrs:
            ti = attrs.get("tabindex", attrs.get("tabIndex", ""))
            if isinstance(ti, str) and re.match(r"^\s*-?\d", ti):
                focusable = not ti.strip().startswith("-")
            else:
                focusable = True
        elif "role" in attrs and attrs["role"] in (
            "button", "link", "checkbox", "radio", "switch", "tab", "menuitem"
        ):
            focusable = True

        if focusable:
            line = line_at(text, m.start())
            findings.append(make_finding(
                "aria-hidden-on-focusable",
                file, line,
                text[m.start():m.end()],
                {"tag": tag},
            ))
    return findings


BAD_ALT_VALUES = re.compile(
    r"^\s*(image|photo|picture|graphic|icon|img|untitled|"
    r"[\w\-]+\.(jpg|jpeg|png|gif|webp|svg|bmp))\s*$",
    re.IGNORECASE,
)


def detect_alt_issues(file: str, text: str) -> list:
    """Missing alt or bad alt values on <img>."""
    findings = []
    for m in re.finditer(r"<img\b([^>]*)/?>", text, re.IGNORECASE | re.DOTALL):
        attr_str = m.group(1)
        attrs = parse_attrs(attr_str)
        line = line_at(text, m.start())
        snippet = text[m.start():m.end()]
        if "alt" not in attrs:
            findings.append(make_finding("missing-alt", file, line, snippet))
            continue
        alt_val = attrs["alt"]
        if isinstance(alt_val, str) and BAD_ALT_VALUES.match(alt_val):
            findings.append(make_finding("bad-alt-value", file, line, snippet))
    return findings


HARDCODED_ARIA_STATES = {"aria-expanded", "aria-pressed", "aria-checked",
                          "aria-selected", "aria-current"}


def detect_hardcoded_aria_states(file: str, text: str, ext: str) -> list:
    """ARIA state attributes hardcoded as string literals in JSX/TSX."""
    if ext not in {".tsx", ".jsx", ".astro", ".svelte", ".vue"}:
        return []
    findings = []
    for state in HARDCODED_ARIA_STATES:
        # Match aria-expanded="true" or aria-expanded='false' (string literal)
        # NOT aria-expanded={isOpen}
        pattern = rf'\b{re.escape(state)}\s*=\s*["\'](?:true|false)["\']'
        for m in re.finditer(pattern, text):
            line = line_at(text, m.start())
            # Skip plain HTML files — string literals are correct there
            findings.append(make_finding(
                "hardcoded-aria-state",
                file, line,
                m.group(0),
                {"attribute": state},
            ))
    return findings


def detect_div_onclick(file: str, text: str) -> list:
    """<div onClick> or <span onClick> without role + keyboard handlers."""
    findings = []
    for m in TAG_OPEN_RE.finditer(text):
        tag = m.group(1).lower()
        if tag not in ("div", "span"):
            continue
        attr_str = m.group(2) or ""
        attrs = parse_attrs(attr_str)
        has_click = "onclick" in {k.lower() for k in attrs.keys()}
        if not has_click:
            continue
        # Is there a role + keyboard handler?
        attrs_lower = {k.lower() for k in attrs.keys()}
        has_role = "role" in attrs_lower
        has_keyhandler = "onkeydown" in attrs_lower or "onkeyup" in attrs_lower or \
                         "onkeypress" in attrs_lower
        if not (has_role and has_keyhandler):
            line = line_at(text, m.start())
            findings.append(make_finding(
                "div-onclick-no-role",
                file, line,
                text[m.start():m.end()],
                {"tag": tag, "has_role": has_role, "has_keyhandler": has_keyhandler},
            ))
    return findings


REDUNDANT_ROLES = {
    ("button", "button"),
    ("a", "link"),
    ("nav", "navigation"),
    ("main", "main"),
    ("header", "banner"),
    ("footer", "contentinfo"),
    ("aside", "complementary"),
    ("h1", "heading"), ("h2", "heading"), ("h3", "heading"),
    ("h4", "heading"), ("h5", "heading"), ("h6", "heading"),
    ("ul", "list"), ("ol", "list"),
    ("li", "listitem"),
    ("table", "table"),
    ("form", "form"),
}


def detect_redundant_aria_roles(file: str, text: str) -> list:
    """role="X" applied to a native element where X is the implicit role."""
    findings = []
    for m in TAG_OPEN_RE.finditer(text):
        tag = m.group(1).lower()
        attr_str = m.group(2) or ""
        attrs = parse_attrs(attr_str)
        role = attrs.get("role")
        if not role or not isinstance(role, str):
            continue
        role_norm = role.strip().lower()
        if (tag, role_norm) in REDUNDANT_ROLES:
            # Tailwind list-none on <ul role="list"> exception:
            # if className contains list-none, role="list" is intentional.
            if (tag in ("ul", "ol") and role_norm == "list" and
                isinstance(attrs.get("className"), str) and
                "list-none" in attrs["className"]):
                continue
            line = line_at(text, m.start())
            findings.append(make_finding(
                "redundant-aria-role",
                file, line,
                text[m.start():m.end()],
                {"tag": tag, "role": role_norm},
            ))
    return findings


def detect_positive_tabindex(file: str, text: str) -> list:
    """tabindex / tabIndex with a value > 0."""
    findings = []
    pattern = re.compile(
        r'\btab[Ii]ndex\s*=\s*(?:"([^"]+)"|\'([^\']+)\'|\{([^}]+)\})'
    )
    for m in pattern.finditer(text):
        val = m.group(1) or m.group(2) or m.group(3) or ""
        val = val.strip()
        # Try to parse as int
        try:
            n = int(val)
        except ValueError:
            continue
        if n > 0:
            line = line_at(text, m.start())
            findings.append(make_finding(
                "positive-tabindex",
                file, line,
                m.group(0),
                {"value": n},
            ))
    return findings


def detect_anchor_no_href(file: str, text: str) -> list:
    """<a> without href used as a click target (has onClick but no href)."""
    findings = []
    for m in TAG_OPEN_RE.finditer(text):
        tag = m.group(1).lower()
        if tag != "a":
            continue
        attr_str = m.group(2) or ""
        attrs = parse_attrs(attr_str)
        attrs_lower = {k.lower() for k in attrs.keys()}
        if "href" in attrs_lower:
            continue
        if "onclick" in attrs_lower or "onclick" in attr_str.lower():
            line = line_at(text, m.start())
            findings.append(make_finding(
                "anchor-no-href",
                file, line,
                text[m.start():m.end()],
            ))
    return findings


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def scan_file(path: Path) -> list:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return []

    file_str = str(path).replace("\\", "/")
    ext = path.suffix.lower()
    findings = []

    findings.extend(detect_outline_none(file_str, text, ext))

    if ext in {".tsx", ".jsx", ".astro", ".html", ".svelte", ".vue"}:
        findings.extend(detect_aria_hidden_on_focusable(file_str, text))
        findings.extend(detect_alt_issues(file_str, text))
        findings.extend(detect_hardcoded_aria_states(file_str, text, ext))
        findings.extend(detect_div_onclick(file_str, text))
        findings.extend(detect_redundant_aria_roles(file_str, text))
        findings.extend(detect_positive_tabindex(file_str, text))
        findings.extend(detect_anchor_no_href(file_str, text))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Static a11y pattern scanner. Pure stdlib Python 3.8+. "
                    "Emits JSON for the /a11y-review skill.",
    )
    parser.add_argument("path", help="File or directory to scan")
    parser.add_argument(
        "--exclude",
        default=",".join(sorted(DEFAULT_EXCLUDES)),
        help="Comma-separated dir names to exclude (default: %(default)s)",
    )
    parser.add_argument(
        "--pretty", action="store_true",
        help="Human-readable output instead of JSON",
    )
    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"error: path not found: {root}", file=sys.stderr)
        return 2

    excludes = {e.strip() for e in args.exclude.split(",") if e.strip()}
    extensions = SCANNED_EXTENSIONS | CSS_EXTENSIONS

    all_findings = []
    files_scanned = 0
    for fp in iter_files(root, excludes, extensions):
        files_scanned += 1
        all_findings.extend(scan_file(fp))

    if args.pretty:
        for f in all_findings:
            print(f"[{f['severity'].upper()}] [STATIC] WCAG {f['wcag']} — {f['category']}")
            print(f"  {f['file']}:{f['line']}")
            print(f"  {f['snippet']}")
            print(f"  Fix: {f['fix']}")
            print()
        print(f"Scanned {files_scanned} files. {len(all_findings)} findings.")
    else:
        out = {
            "tool": "scan-jsx-patterns",
            "version": "1.0.0",
            "files_scanned": files_scanned,
            "findings_count": len(all_findings),
            "findings": all_findings,
        }
        print(json.dumps(out, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
