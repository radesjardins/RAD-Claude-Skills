#!/usr/bin/env python3
"""
check-target-size.py — WCAG 2.5.8 Target Size (Minimum) scanner.

Scans .tsx / .jsx / .astro / .html / .vue / .svelte source for interactive
elements with Tailwind sizing/padding classes that produce sub-24×24px touch
targets. WCAG 2.5.8 (added in 2.2) requires interactive targets be at least
24×24 CSS pixels, with documented exceptions.

Pure stdlib Python 3.8+. JSON output for the /a11y-review skill.

Honest scope:
  - Detects Tailwind v3 default sizing/padding scale (assumes 1rem = 16px).
  - Considers an interactive element under-sized when its computed
    width OR height (size + padding × 2) on the explicit side falls below
    24px AND no min-w/min-h class brings it back up.
  - Cannot resolve runtime CSS, custom config sizing scales, or sizing
    inherited from parents. Best-effort source analysis.
  - Inline links inside paragraphs (not standalone clickable rows) are an
    explicit exception per WCAG 2.5.8 — not flagged when surrounded by text.
    This script does NOT distinguish inline from block context, so all <a>
    findings are tagged [HEURISTIC] (could be a valid inline-link exception).
  - <button> and role="button" findings are tagged [STATIC] when the source
    sizing classes are unambiguously below threshold.

Tailwind v3 default spacing scale (rem -> px @ 16px base):
  0    -> 0       0.5  -> 2      1    -> 4
  1.5  -> 6       2    -> 8      2.5  -> 10
  3    -> 12      3.5  -> 14     4    -> 16
  5    -> 20      6    -> 24     7    -> 28
  8    -> 32      ...
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_EXCLUDES = {
    "node_modules", "dist", "build", ".next", ".astro", "coverage",
    ".turbo", ".cache", ".git", ".svelte-kit", "out", ".vercel",
}

SCANNED_EXTS = {".tsx", ".jsx", ".astro", ".html", ".svelte", ".vue"}

# Tailwind v3 default spacing scale (key -> pixels, assuming 1rem = 16px)
SPACING_PX = {
    "0": 0, "px": 1,
    "0.5": 2, "1": 4, "1.5": 6, "2": 8, "2.5": 10,
    "3": 12, "3.5": 14, "4": 16, "5": 20, "6": 24,
    "7": 28, "8": 32, "9": 36, "10": 40, "11": 44,
    "12": 48, "14": 56, "16": 64, "20": 80, "24": 96,
    "28": 112, "32": 128, "36": 144, "40": 160, "44": 176,
    "48": 192, "52": 208, "56": 224, "60": 240, "64": 256,
    "72": 288, "80": 320, "96": 384,
}

THRESHOLD = 24  # WCAG 2.5.8 minimum CSS pixels

# Match utilities like w-4, h-4, w-[16px], min-w-12, p-2, px-1, py-0.5
SIZING_RE = re.compile(
    r"\b(w|h|min-w|min-h|max-w|max-h|p|px|py|pt|pr|pb|pl)-"
    r"(\[[^\]]+\]|[\w.]+)"
    r"(?![\w-])"
)

INTERACTIVE_TAG_RE = re.compile(
    r"<(button|a|input|select|textarea)\b([^>]*)>",
    re.IGNORECASE,
)

ROLE_INTERACTIVE_RE = re.compile(
    r'<(div|span)\b([^>]*?\brole\s*=\s*["\']?(?:button|link|checkbox|radio|switch|tab|menuitem)["\']?[^>]*)>',
    re.IGNORECASE,
)

CLASSNAME_RE = re.compile(
    r"\b(?:className|class)\s*=\s*"
    r"(?:\"([^\"]+)\"|'([^']+)'|`([^`]+)`)"
)


def parse_arbitrary_px(val: str):
    """Parse arbitrary value like [16px] or [1rem]."""
    inner = val.strip("[]")
    m = re.match(r"^([\d.]+)(px|rem|em)$", inner)
    if not m:
        return None
    n = float(m.group(1))
    unit = m.group(2)
    if unit == "px":
        return int(n)
    if unit in ("rem", "em"):
        return int(n * 16)
    return None


def class_to_px(value: str):
    """Convert a Tailwind size token to pixels. Returns None if unknown."""
    if value.startswith("["):
        return parse_arbitrary_px(value)
    return SPACING_PX.get(value)


def computed_dimensions(class_str: str):
    """Return (width_px, height_px) inferred from sizing classes.

    Each is None if not determinable. Considers w/h plus padding contributions
    on the relevant axis.
    """
    width_base = None
    height_base = None
    px_total = 0   # padding x (px)
    py_total = 0   # padding y (py)
    p_each = 0     # general padding (p) applies both axes
    has_min_w = False
    has_min_h = False
    min_w_meets = False
    min_h_meets = False

    for m in SIZING_RE.finditer(class_str):
        prop = m.group(1)
        val = m.group(2)
        px = class_to_px(val)
        if px is None:
            continue

        if prop == "w":
            width_base = px
        elif prop == "h":
            height_base = px
        elif prop == "min-w":
            has_min_w = True
            if px >= THRESHOLD:
                min_w_meets = True
        elif prop == "min-h":
            has_min_h = True
            if px >= THRESHOLD:
                min_h_meets = True
        elif prop == "p":
            p_each = px * 2
        elif prop == "px":
            px_total = px * 2
        elif prop == "py":
            py_total = px * 2
        elif prop in ("pt", "pb"):
            py_total += px
        elif prop in ("pl", "pr"):
            px_total += px

    width = None
    height = None
    if width_base is not None:
        width = width_base + max(px_total, p_each)
    if height_base is not None:
        height = height_base + max(py_total, p_each)

    return {
        "width": width,
        "height": height,
        "min_w_meets": min_w_meets if has_min_w else None,
        "min_h_meets": min_h_meets if has_min_h else None,
    }


def extract_classname(tag_attrs: str):
    m = CLASSNAME_RE.search(tag_attrs)
    if not m:
        return None
    return m.group(1) or m.group(2) or m.group(3) or ""


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


def line_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def evaluate_element(file: str, text: str, m, is_anchor: bool, tag: str) -> list:
    attrs = m.group(2)
    class_str = extract_classname(attrs)
    if not class_str:
        return []
    dims = computed_dimensions(class_str)
    if dims["width"] is None and dims["height"] is None:
        return []
    findings = []
    line = line_at(text, m.start())

    # Skip if min-* classes ensure threshold is met
    if dims["min_w_meets"] and dims["min_h_meets"]:
        return []

    width = dims["width"]
    height = dims["height"]
    too_small_w = width is not None and width < THRESHOLD and not dims["min_w_meets"]
    too_small_h = height is not None and height < THRESHOLD and not dims["min_h_meets"]

    if not (too_small_w or too_small_h):
        return []

    # Anchors get [HEURISTIC] because inline-link exception applies
    confidence = "HEURISTIC" if is_anchor else "STATIC"

    findings.append({
        "category": "target-size-below-24px",
        "wcag": "2.5.8",
        "severity": "moderate",
        "confidence": confidence,
        "file": file,
        "line": line,
        "tag": tag,
        "computed_width_px": width,
        "computed_height_px": height,
        "threshold_px": THRESHOLD,
        "snippet": class_str[:200],
        "fix": (
            f"Interactive <{tag}> target appears to be "
            f"{width if width is not None else '?'}×"
            f"{height if height is not None else '?'}px. "
            "WCAG 2.5.8 requires ≥24×24px. Increase w-/h- or padding to meet "
            "the threshold, or add `min-w-6 min-h-6` (24px) as a floor."
            + (" If this is an inline link inside a paragraph, the "
               "WCAG 2.5.8 inline-link exception applies — verify."
               if is_anchor else "")
        ),
    })
    return findings


def scan_file(path: Path) -> list:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return []

    file_str = str(path).replace("\\", "/")
    findings = []

    for m in INTERACTIVE_TAG_RE.finditer(text):
        tag = m.group(1).lower()
        if tag in ("input", "select", "textarea"):
            # Form controls have a different baseline; skip in this checker
            continue
        is_anchor = tag == "a"
        findings.extend(evaluate_element(file_str, text, m, is_anchor, tag))

    for m in ROLE_INTERACTIVE_RE.finditer(text):
        tag = m.group(1).lower()
        findings.extend(evaluate_element(file_str, text, m, False, tag))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="WCAG 2.5.8 target-size scanner for Tailwind interactive "
                    "elements.",
    )
    parser.add_argument("path", help="File or directory to scan")
    parser.add_argument(
        "--exclude",
        default=",".join(sorted(DEFAULT_EXCLUDES)),
        help="Comma-separated dir names to exclude",
    )
    parser.add_argument("--pretty", action="store_true",
                         help="Human-readable output instead of JSON")
    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"error: path not found: {root}", file=sys.stderr)
        return 2

    excludes = {e.strip() for e in args.exclude.split(",") if e.strip()}

    all_findings = []
    files_scanned = 0
    for fp in iter_files(root, excludes):
        files_scanned += 1
        all_findings.extend(scan_file(fp))

    if args.pretty:
        for f in all_findings:
            print(f"[{f['severity'].upper()}] [{f['confidence']}] "
                  f"WCAG {f['wcag']} — {f['category']}")
            print(f"  {f['file']}:{f['line']}")
            print(f"  <{f['tag']}> computed "
                  f"{f.get('computed_width_px')}×{f.get('computed_height_px')}px "
                  f"(threshold {f['threshold_px']}px)")
            print(f"  classes: {f['snippet']}")
            print(f"  Fix: {f['fix']}")
            print()
        print(f"Scanned {files_scanned} files. {len(all_findings)} findings.")
    else:
        out = {
            "tool": "check-target-size",
            "version": "1.0.0",
            "files_scanned": files_scanned,
            "findings_count": len(all_findings),
            "findings": all_findings,
        }
        print(json.dumps(out, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
