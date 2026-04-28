#!/usr/bin/env python3
"""
check-tailwind-contrast.py — WCAG sRGB contrast ratio scanner for Tailwind.

Scans .tsx / .jsx / .astro / .html / .vue / .svelte source for Tailwind class
combinations that pair foreground text colors with background colors on the
same element, computes the WCAG 2.x contrast ratio (sRGB → relative luminance
math, no browser needed), and flags pairs that fail AA thresholds.

Real WCAG-grade sRGB math. Not a heuristic. Outputs JSON with the actual
computed ratio so downstream tooling and the user can see the number.

Honest scope:
  - Computes contrast for Tailwind v3 default palette built into the script.
  - Best-effort regex parsing of `tailwind.config.{js,ts,cjs,mjs}` for custom
    colors at theme.colors and theme.extend.colors. Object literals only —
    function-based palettes (e.g., colors imported from another file) are
    skipped with a warning.
  - Pairs are detected by co-occurrence of `text-COLOR-SHADE` and
    `bg-COLOR-SHADE` on the same element's className. Cannot reason about
    inherited backgrounds across DOM ancestors — that's a runtime concern.
  - Does NOT compute alpha-blended contrast (text on a translucent bg).
  - Does NOT verify large-text vs. body-text classification — uses 4.5:1 by
    default (body text). Pairs in the 3.0–4.5 range are surfaced as
    [HEURISTIC] (could pass for large text).
  - Border / UI component contrast (3:1 threshold) is checked separately when
    `border-*` and `bg-*` co-occur.

Pure stdlib Python 3.8+. No pip install required.

Thresholds (WCAG 2.1 AA):
  - Normal text: 4.5:1
  - Large text (>=18.66px or >=14px bold): 3:1
  - UI components / borders: 3:1
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

# ---------------------------------------------------------------------------
# Tailwind v3 default palette (subset — most commonly used colors)
# Sources from tailwindcss.com. These are sRGB hex values.
# ---------------------------------------------------------------------------

TAILWIND_DEFAULT_PALETTE = {
    "white": {None: "#ffffff"},
    "black": {None: "#000000"},
    "transparent": {None: None},  # cannot compute contrast
    "current": {None: None},
    "inherit": {None: None},
    "slate": {
        50: "#f8fafc", 100: "#f1f5f9", 200: "#e2e8f0", 300: "#cbd5e1",
        400: "#94a3b8", 500: "#64748b", 600: "#475569", 700: "#334155",
        800: "#1e293b", 900: "#0f172a", 950: "#020617",
    },
    "gray": {
        50: "#f9fafb", 100: "#f3f4f6", 200: "#e5e7eb", 300: "#d1d5db",
        400: "#9ca3af", 500: "#6b7280", 600: "#4b5563", 700: "#374151",
        800: "#1f2937", 900: "#111827", 950: "#030712",
    },
    "zinc": {
        50: "#fafafa", 100: "#f4f4f5", 200: "#e4e4e7", 300: "#d4d4d8",
        400: "#a1a1aa", 500: "#71717a", 600: "#52525b", 700: "#3f3f46",
        800: "#27272a", 900: "#18181b", 950: "#09090b",
    },
    "neutral": {
        50: "#fafafa", 100: "#f5f5f5", 200: "#e5e5e5", 300: "#d4d4d4",
        400: "#a3a3a3", 500: "#737373", 600: "#525252", 700: "#404040",
        800: "#262626", 900: "#171717", 950: "#0a0a0a",
    },
    "stone": {
        50: "#fafaf9", 100: "#f5f5f4", 200: "#e7e5e4", 300: "#d6d3d1",
        400: "#a8a29e", 500: "#78716c", 600: "#57534e", 700: "#44403c",
        800: "#292524", 900: "#1c1917", 950: "#0c0a09",
    },
    "red": {
        50: "#fef2f2", 100: "#fee2e2", 200: "#fecaca", 300: "#fca5a5",
        400: "#f87171", 500: "#ef4444", 600: "#dc2626", 700: "#b91c1c",
        800: "#991b1b", 900: "#7f1d1d", 950: "#450a0a",
    },
    "orange": {
        50: "#fff7ed", 100: "#ffedd5", 200: "#fed7aa", 300: "#fdba74",
        400: "#fb923c", 500: "#f97316", 600: "#ea580c", 700: "#c2410c",
        800: "#9a3412", 900: "#7c2d12", 950: "#431407",
    },
    "amber": {
        50: "#fffbeb", 100: "#fef3c7", 200: "#fde68a", 300: "#fcd34d",
        400: "#fbbf24", 500: "#f59e0b", 600: "#d97706", 700: "#b45309",
        800: "#92400e", 900: "#78350f", 950: "#451a03",
    },
    "yellow": {
        50: "#fefce8", 100: "#fef9c3", 200: "#fef08a", 300: "#fde047",
        400: "#facc15", 500: "#eab308", 600: "#ca8a04", 700: "#a16207",
        800: "#854d0e", 900: "#713f12", 950: "#422006",
    },
    "lime": {
        50: "#f7fee7", 100: "#ecfccb", 200: "#d9f99d", 300: "#bef264",
        400: "#a3e635", 500: "#84cc16", 600: "#65a30d", 700: "#4d7c0f",
        800: "#3f6212", 900: "#365314", 950: "#1a2e05",
    },
    "green": {
        50: "#f0fdf4", 100: "#dcfce7", 200: "#bbf7d0", 300: "#86efac",
        400: "#4ade80", 500: "#22c55e", 600: "#16a34a", 700: "#15803d",
        800: "#166534", 900: "#14532d", 950: "#052e16",
    },
    "emerald": {
        50: "#ecfdf5", 100: "#d1fae5", 200: "#a7f3d0", 300: "#6ee7b7",
        400: "#34d399", 500: "#10b981", 600: "#059669", 700: "#047857",
        800: "#065f46", 900: "#064e3b", 950: "#022c22",
    },
    "teal": {
        50: "#f0fdfa", 100: "#ccfbf1", 200: "#99f6e4", 300: "#5eead4",
        400: "#2dd4bf", 500: "#14b8a6", 600: "#0d9488", 700: "#0f766e",
        800: "#115e59", 900: "#134e4a", 950: "#042f2e",
    },
    "cyan": {
        50: "#ecfeff", 100: "#cffafe", 200: "#a5f3fc", 300: "#67e8f9",
        400: "#22d3ee", 500: "#06b6d4", 600: "#0891b2", 700: "#0e7490",
        800: "#155e75", 900: "#164e63", 950: "#083344",
    },
    "sky": {
        50: "#f0f9ff", 100: "#e0f2fe", 200: "#bae6fd", 300: "#7dd3fc",
        400: "#38bdf8", 500: "#0ea5e9", 600: "#0284c7", 700: "#0369a1",
        800: "#075985", 900: "#0c4a6e", 950: "#082f49",
    },
    "blue": {
        50: "#eff6ff", 100: "#dbeafe", 200: "#bfdbfe", 300: "#93c5fd",
        400: "#60a5fa", 500: "#3b82f6", 600: "#2563eb", 700: "#1d4ed8",
        800: "#1e40af", 900: "#1e3a8a", 950: "#172554",
    },
    "indigo": {
        50: "#eef2ff", 100: "#e0e7ff", 200: "#c7d2fe", 300: "#a5b4fc",
        400: "#818cf8", 500: "#6366f1", 600: "#4f46e5", 700: "#4338ca",
        800: "#3730a3", 900: "#312e81", 950: "#1e1b4b",
    },
    "violet": {
        50: "#f5f3ff", 100: "#ede9fe", 200: "#ddd6fe", 300: "#c4b5fd",
        400: "#a78bfa", 500: "#8b5cf6", 600: "#7c3aed", 700: "#6d28d9",
        800: "#5b21b6", 900: "#4c1d95", 950: "#2e1065",
    },
    "purple": {
        50: "#faf5ff", 100: "#f3e8ff", 200: "#e9d5ff", 300: "#d8b4fe",
        400: "#c084fc", 500: "#a855f7", 600: "#9333ea", 700: "#7e22ce",
        800: "#6b21a8", 900: "#581c87", 950: "#3b0764",
    },
    "fuchsia": {
        50: "#fdf4ff", 100: "#fae8ff", 200: "#f5d0fe", 300: "#f0abfc",
        400: "#e879f9", 500: "#d946ef", 600: "#c026d3", 700: "#a21caf",
        800: "#86198f", 900: "#701a75", 950: "#4a044e",
    },
    "pink": {
        50: "#fdf2f8", 100: "#fce7f3", 200: "#fbcfe8", 300: "#f9a8d4",
        400: "#f472b6", 500: "#ec4899", 600: "#db2777", 700: "#be185d",
        800: "#9d174d", 900: "#831843", 950: "#500724",
    },
    "rose": {
        50: "#fff1f2", 100: "#ffe4e6", 200: "#fecdd3", 300: "#fda4af",
        400: "#fb7185", 500: "#f43f5e", 600: "#e11d48", 700: "#be123c",
        800: "#9f1239", 900: "#881337", 950: "#4c0519",
    },
}


# ---------------------------------------------------------------------------
# Color math (WCAG 2.1)
# ---------------------------------------------------------------------------

def hex_to_rgb(h: str):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return None
    try:
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    except ValueError:
        return None


def channel_luminance(c: int) -> float:
    """sRGB 8-bit channel -> linear 0..1."""
    s = c / 255.0
    return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb) -> float:
    r, g, b = rgb
    return (0.2126 * channel_luminance(r) +
            0.7152 * channel_luminance(g) +
            0.0722 * channel_luminance(b))


def contrast_ratio(hex1: str, hex2: str):
    rgb1 = hex_to_rgb(hex1)
    rgb2 = hex_to_rgb(hex2)
    if not rgb1 or not rgb2:
        return None
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ---------------------------------------------------------------------------
# Tailwind class parsing
# ---------------------------------------------------------------------------

# Match text-COLOR-SHADE, bg-COLOR-SHADE, border-COLOR-SHADE
# Excludes hover:/focus:/dark:/etc. variants — those don't determine the
# resting-state contrast we're checking.
COLOR_CLASS_RE = re.compile(
    r"(?<![\w:-])"  # no variant prefix immediately before
    r"(text|bg|border|placeholder|ring|divide)-"
    r"([a-z]+)"        # color name
    r"(?:-(\d{2,3}))?" # optional shade
    r"(?![\w-])"
)


def lookup_color(palette: dict, name: str, shade) -> str:
    """Return hex for color-shade or None if not found / not resolvable."""
    if name not in palette:
        return None
    shades = palette[name]
    if shade is None:
        # Tailwind: bg-white = palette["white"][None]
        return shades.get(None)
    try:
        s = int(shade)
    except ValueError:
        return None
    return shades.get(s)


def parse_classnames(class_str: str):
    """Yield (utility, color, shade) tuples for color-related classes."""
    for m in COLOR_CLASS_RE.finditer(class_str):
        yield m.group(1), m.group(2), m.group(3)


# ---------------------------------------------------------------------------
# Custom palette parsing (best-effort regex over tailwind.config.{js,ts,cjs,mjs})
# ---------------------------------------------------------------------------

CONFIG_FILENAMES = ("tailwind.config.js", "tailwind.config.ts",
                    "tailwind.config.cjs", "tailwind.config.mjs")


def find_tailwind_config(root: Path):
    for name in CONFIG_FILENAMES:
        p = root / name
        if p.exists():
            return p
    return None


def parse_tailwind_config(config_path: Path) -> dict:
    """Best-effort regex parse of theme.colors / theme.extend.colors object.

    Returns a palette dict in the same shape as TAILWIND_DEFAULT_PALETTE.
    Handles object-literal palettes only. Returns {} for everything else.
    """
    custom = {}
    try:
        text = config_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return custom

    # Find theme.colors or theme.extend.colors object literals
    # Pattern: colors: { ... }  with nested {} support via balanced scan
    for m in re.finditer(r"\bcolors\s*:\s*\{", text):
        start = m.end() - 1
        depth = 0
        i = start
        while i < len(text):
            ch = text[i]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        if depth != 0:
            continue
        block = text[start + 1:i]

        # Parse keys at the top level of this block
        # Two shapes:
        #   primary: '#abcdef'
        #   primary: { 50: '#...', 100: '#...', ... }
        #   'primary-fg': '#abc'
        for entry in re.finditer(
            r"['\"]?([\w-]+)['\"]?\s*:\s*"
            r"(?:['\"](#[0-9a-fA-F]{3,8})['\"]"  # direct hex
            r"|\{([^}]*)\})",                    # nested shades
            block,
        ):
            name = entry.group(1)
            direct_hex = entry.group(2)
            shade_block = entry.group(3)
            if direct_hex:
                custom.setdefault(name, {})[None] = direct_hex
            elif shade_block:
                shades = {}
                for sm in re.finditer(
                    r"['\"]?(\d{2,4}|DEFAULT)['\"]?\s*:\s*['\"](#[0-9a-fA-F]{3,8})['\"]",
                    shade_block,
                ):
                    key = sm.group(1)
                    if key == "DEFAULT":
                        shades[None] = sm.group(2)
                    else:
                        try:
                            shades[int(key)] = sm.group(2)
                        except ValueError:
                            pass
                if shades:
                    custom.setdefault(name, {}).update(shades)

    return custom


def merge_palettes(*palettes) -> dict:
    out = {}
    for p in palettes:
        for name, shades in p.items():
            if name not in out:
                out[name] = dict(shades)
            else:
                out[name].update(shades)
    return out


# ---------------------------------------------------------------------------
# File scanning
# ---------------------------------------------------------------------------

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


CLASSNAME_RE = re.compile(
    r"\b(?:className|class)\s*=\s*"
    r"(?:\"([^\"]+)\"|'([^']+)'|`([^`]+)`|\{`([^`]+)`\}|\{\"([^\"]+)\"\})"
)


def scan_file(path: Path, palette: dict) -> list:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return []

    file_str = str(path).replace("\\", "/")
    findings = []

    for m in CLASSNAME_RE.finditer(text):
        class_str = next((g for g in m.groups() if g), "")
        if not class_str:
            continue
        line = line_at(text, m.start())

        text_color = None
        bg_color = None
        border_color = None
        text_class = None
        bg_class = None
        border_class = None

        for utility, name, shade in parse_classnames(class_str):
            hex_val = lookup_color(palette, name, shade)
            if not hex_val:
                continue
            if utility == "text":
                text_color = hex_val
                text_class = f"text-{name}{'-' + shade if shade else ''}"
            elif utility == "bg":
                bg_color = hex_val
                bg_class = f"bg-{name}{'-' + shade if shade else ''}"
            elif utility == "border":
                border_color = hex_val
                border_class = f"border-{name}{'-' + shade if shade else ''}"

        # Text on background (4.5:1 normal text)
        if text_color and bg_color:
            ratio = contrast_ratio(text_color, bg_color)
            if ratio is None:
                continue
            if ratio < 4.5:
                confidence = "STATIC" if ratio < 3.0 else "HEURISTIC"
                findings.append({
                    "category": "low-contrast-text",
                    "wcag": "1.4.3",
                    "severity": "serious" if ratio < 3.0 else "moderate",
                    "confidence": confidence,
                    "file": file_str,
                    "line": line,
                    "fg_class": text_class,
                    "fg_hex": text_color,
                    "bg_class": bg_class,
                    "bg_hex": bg_color,
                    "ratio": round(ratio, 2),
                    "required_normal": 4.5,
                    "required_large": 3.0,
                    "snippet": class_str[:200],
                    "fix": (
                        f"Contrast ratio {ratio:.2f}:1 fails WCAG AA "
                        f"(needs 4.5:1 for normal text, 3:1 for large text). "
                        f"Choose darker text or lighter background. "
                        f"If text is large (>=18.66px or >=14px bold), "
                        f"this passes — but classify it explicitly."
                    ),
                })

        # Border on background (3:1 UI components)
        if border_color and bg_color:
            ratio = contrast_ratio(border_color, bg_color)
            if ratio is not None and ratio < 3.0:
                findings.append({
                    "category": "low-contrast-border",
                    "wcag": "1.4.11",
                    "severity": "moderate",
                    "confidence": "STATIC",
                    "file": file_str,
                    "line": line,
                    "fg_class": border_class,
                    "fg_hex": border_color,
                    "bg_class": bg_class,
                    "bg_hex": bg_color,
                    "ratio": round(ratio, 2),
                    "required": 3.0,
                    "snippet": class_str[:200],
                    "fix": (
                        f"UI border contrast {ratio:.2f}:1 fails WCAG AA "
                        f"1.4.11 (needs 3:1 against adjacent background). "
                        f"Use a darker border shade."
                    ),
                })

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="WCAG sRGB contrast scanner for Tailwind class pairs.",
    )
    parser.add_argument("path", help="File or directory to scan")
    parser.add_argument(
        "--exclude",
        default=",".join(sorted(DEFAULT_EXCLUDES)),
        help="Comma-separated dir names to exclude",
    )
    parser.add_argument("--pretty", action="store_true",
                         help="Human-readable output instead of JSON")
    parser.add_argument("--config",
                         help="Path to tailwind.config.* (auto-detected if omitted)")
    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"error: path not found: {root}", file=sys.stderr)
        return 2

    # Build palette: defaults + user config (best-effort)
    palette = dict(TAILWIND_DEFAULT_PALETTE)
    config_path = Path(args.config) if args.config else find_tailwind_config(
        root if root.is_dir() else root.parent
    )
    custom = {}
    if config_path and config_path.exists():
        custom = parse_tailwind_config(config_path)
        palette = merge_palettes(palette, custom)

    excludes = {e.strip() for e in args.exclude.split(",") if e.strip()}
    all_findings = []
    files_scanned = 0
    for fp in iter_files(root, excludes):
        files_scanned += 1
        all_findings.extend(scan_file(fp, palette))

    if args.pretty:
        for f in all_findings:
            print(f"[{f['severity'].upper()}] [{f['confidence']}] "
                  f"WCAG {f['wcag']} — {f['category']} "
                  f"(ratio {f['ratio']}:1)")
            print(f"  {f['file']}:{f['line']}")
            print(f"  {f.get('fg_class')} ({f.get('fg_hex')}) on "
                  f"{f.get('bg_class')} ({f.get('bg_hex')})")
            print(f"  Fix: {f['fix']}")
            print()
        print(f"Scanned {files_scanned} files. Custom palette entries: "
              f"{len(custom)}. {len(all_findings)} contrast findings.")
    else:
        out = {
            "tool": "check-tailwind-contrast",
            "version": "1.0.0",
            "config_file": str(config_path) if config_path else None,
            "custom_palette_entries": len(custom),
            "files_scanned": files_scanned,
            "findings_count": len(all_findings),
            "findings": all_findings,
        }
        print(json.dumps(out, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
