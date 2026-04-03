# Tailwind v4: Configuration, Theming & v3→v4 Migration

## The Oxide Engine (v4 Architecture)

Tailwind v4 rebuilds the engine in Rust under the name **Oxide**. Key architectural facts:

- Full builds are up to **5x faster** than v3; incremental rebuilds happen in **microseconds**
- **Automatic content detection** — Oxide scans the project using smart heuristics, respects `.gitignore`, skips binary assets. No `content` array needed.
- **Single entry point**: `@import "tailwindcss"` replaces the three `@tailwind` directives
- **Autoprefixer is built-in** — remove it from your PostCSS config; it is no longer needed
- **CSS-native cascade layers** — Tailwind v4 emits CSS using native `@layer` rules, eliminating specificity bugs from the v3 era

### Build Tool Integration (v4)

| Tool | Plugin |
|------|--------|
| Vite | `@tailwindcss/vite` (first-party, recommended) |
| PostCSS | `@tailwindcss/postcss` (replaces `tailwindcss` PostCSS plugin) |
| CLI | `@tailwindcss/cli` |

Do not use the generic `tailwindcss` PostCSS plugin with v4 — it no longer applies.

---

## CSS-First Configuration with `@theme`

The `tailwind.config.js` file is fully replaced by the **`@theme` directive** in your main CSS file.

```css
@import "tailwindcss";

@theme {
  /* ---- Colors ---- */
  /* Namespace: --color-* → generates bg-*, text-*, border-*, fill-*, stroke-*, etc. */
  --color-brand-50: oklch(97% 0.02 265);
  --color-brand-500: oklch(60% 0.18 265);
  --color-brand-600: oklch(52% 0.18 265);
  --color-brand-900: oklch(20% 0.06 265);

  /* Semantic colors — reference foundation tokens */
  --color-surface: var(--color-brand-50);
  --color-surface-foreground: var(--color-brand-900);

  /* ---- Spacing ---- */
  /* Namespace: --spacing-* → feeds p-*, m-*, w-*, h-*, gap-*, inset-*, etc. */
  --spacing-18: 4.5rem;
  --spacing-22: 5.5rem;

  /* ---- Typography ---- */
  /* Namespace: --font-* → font-* utilities */
  --font-display: "Cal Sans", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  /* Namespace: --text-* → text-* utilities */
  /* Sub-properties bundle multiple CSS properties into one utility */
  --text-xs: 0.75rem;
  --text-xs--line-height: 1.5;
  --text-xs--letter-spacing: 0.01em;

  /* ---- Shadows ---- */
  --shadow-brand: 0 4px 14px 0 oklch(60% 0.18 265 / 0.4);
}
```

### Theme Namespaces → Generated Utilities

| Namespace | Generated utilities |
|-----------|-------------------|
| `--color-*` | `bg-*`, `text-*`, `border-*`, `fill-*`, `stroke-*`, `ring-*`, `shadow-*` |
| `--spacing-*` | `p-*`, `m-*`, `w-*`, `h-*`, `gap-*`, `inset-*`, `translate-*`, `size-*` |
| `--font-*` | `font-*` (font-family) |
| `--text-*` | `text-*` (font-size, with sub-properties for line-height, letter-spacing) |
| `--leading-*` | `leading-*` |
| `--tracking-*` | `tracking-*` |
| `--rounded-*` | `rounded-*` |
| `--shadow-*` | `shadow-*` |
| `--blur-*` | `blur-*` |
| `--animate-*` | `animate-*` |

### `@theme reference` — Lean Bundle Mode

By default, `@theme` emits all tokens as CSS custom properties in the output. To suppress variable emission (keeping the bundle lean while still generating utilities):

```css
@theme reference {
  --color-brand-500: oklch(60% 0.18 265);
  /* ... */
}
```

Use `@theme reference` for extensive token sets where the CSS variables are not needed at runtime (e.g., tokens used only for utility generation, not referenced via `var()`).

### Disabling the Default Theme

To enforce a strict proprietary design system with no Tailwind defaults:

```css
@theme {
  /* Wipe all default tokens */
  --*: initial;

  /* Only your tokens exist */
  --color-primary: oklch(60% 0.18 265);
}
```

To wipe only a specific namespace:
```css
@theme {
  --font-*: initial;
  --font-body: "Inter Variable", sans-serif;
}
```

---

## Multi-Theme Patterns

### Context-Aware CSS Variables (Multi-Portal / White-Label)

Map Tailwind theme tokens to semantic CSS variables that can be swapped at runtime:

```css
@theme {
  /* Foundation tokens */
  --color-primary-500: oklch(60% 0.18 265);
  --color-secondary-500: oklch(65% 0.15 150);

  /* Semantic tokens pointing to foundation tokens */
  --color-action: var(--color-primary-500);
  --color-accent: var(--color-secondary-500);
}

/* Theme override via data attribute */
[data-theme="green"] {
  --color-action: var(--color-secondary-500);
  --color-accent: var(--color-primary-500);
}
```

In components, use semantic utilities: `bg-action`, `text-accent`. Switching themes only requires changing the data attribute on a wrapper — zero HTML changes.

---

## Dark Mode

### Default: OS Preference (`media` strategy)

No configuration needed. Tailwind v4 respects `prefers-color-scheme` by default. Use `dark:` variants:

```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
```

### Manual Toggle (`class` strategy — v4)

Add this to your CSS to switch to class-based dark mode:

```css
@import "tailwindcss";

/* Override dark mode strategy */
@variant dark (&:where(.dark, .dark *));
```

Apply `.dark` to `<html>` to activate dark mode:

```js
// React ThemeProvider pattern
document.documentElement.classList.toggle('dark', isDark)
localStorage.setItem('theme', isDark ? 'dark' : 'light')
```

**Composing light + dark in markup — always explicit, never implicit:**
```html
<!-- Every color decision needs both states -->
<button class="bg-brand-500 text-white hover:bg-brand-600 dark:bg-brand-400 dark:hover:bg-brand-300">
  Submit
</button>
```

---

## v3 → v4 Migration

### Breaking Changes (must handle manually or with upgrade tool)

| v3 | v4 | Impact |
|----|----|--------|
| `tailwind.config.js` | `@theme {}` in CSS | High — all custom tokens |
| `@tailwind base/components/utilities` | `@import "tailwindcss"` | High — every CSS entry point |
| `tailwindcss` PostCSS plugin | `@tailwindcss/postcss` | High — every build config |
| `bg-gradient-to-r` | `bg-linear-to-r` | Medium — all gradient utilities |
| `bg-opacity-*`, `text-opacity-*` | Slash syntax `bg-blue-500/50` | Medium — all opacity utilities |
| `shadow-sm` | `shadow-xs` | Low — visual shift |
| `rounded-sm` | `rounded-xs` | Low — visual shift |
| `blur-sm` | `blur-xs` | Low — visual shift |
| Default border color (gray) | `currentColor` | Medium — borders inherit text color |
| Default ring width (3px) | 1px | Low — focus rings appear thinner |
| `!bg-red-500` (prefix `!`) | `bg-red-500!` (suffix `!`) | Medium — all important modifiers |
| `outline-none` | `outline-hidden` (remove) / `outline-none` (accessible) | Medium — accessibility impact |

### New Utilities in v4

- **3D Transforms**: `rotate-x-*`, `rotate-y-*`, `translate-z-*`, `perspective-*`, `transform-3d`
- **Not variant**: `not-hover:`, `not-focus:`, `not-disabled:` — style when a condition is NOT met
- **Container queries**: built-in, no plugin needed
- **Forced colors**: `forced-colors:` variants for Windows high-contrast mode
- **`@starting-style` animations**: animate elements as they mount to the DOM
- **`@property` registered custom properties**: type-safe CSS variables
- **Expanded gradients**: `bg-radial-*`, `bg-conic-*`, color interpolation via `oklch`

### Using the Official Upgrade Tool

```bash
npx @tailwindcss/upgrade
```

The upgrade tool handles:
- Migrating `tailwind.config.js` to CSS `@theme`
- Rewriting `@tailwind` directives to `@import`
- Renaming deprecated utilities (`shadow-sm` → `shadow-xs`, etc.)
- Converting `bg-opacity-*` to slash syntax
- Removing Autoprefixer from PostCSS config

**Limitation:** Does not remove legacy plugins that are now built-in (aspect-ratio, container-queries). Remove these manually from your config and package.json.

### Legacy Plugin Bridge (`@config`)

If you rely on third-party JavaScript plugins not yet updated for v4:

```css
@import "tailwindcss";
@config "./tailwind.config.js"; /* Loads legacy JS config alongside CSS engine */
```

This is a temporary bridge — migrate off it as plugins are updated.

---

## Production Optimization

### Bundle Size Reality

Tailwind v4's JIT compiler generates only the CSS classes present in your templates. Typical production bundles are **under 10kB**. A single cached CSS file is more efficient than route-level CSS splitting.

### Minification

```bash
# CLI
tailwindcss --input ./src/styles/global.css --output ./dist/styles.css --minify

# PostCSS — add cssnano after @tailwindcss/postcss
```

### Server Compression

Always serve the CSS file with **Brotli** (first choice) or Gzip compression. For a 10kB Tailwind bundle, Brotli typically yields 2-3kB over the wire.

### `@reference` in Component Styles

When using `@apply` or `var(--color-*)` in Vue/Svelte `<style>` blocks or CSS Modules, use `@reference` to provide context without duplicating CSS output:

```css
/* Inside Vue <style scoped> */
@reference "../../styles/global.css";

.custom-class {
  color: var(--color-brand-500);
}
```

### Safelist / Dynamic Classes

Tailwind's scanner uses static analysis. Dynamic class construction is invisible to the scanner:

```jsx
// WRONG — scanner cannot detect these
const bg = `bg-${color}-500`  // → class never generated

// CORRECT — full class strings must appear in source
const bg = color === 'blue' ? 'bg-blue-500' : 'bg-red-500'
```

For genuinely dynamic values (from API/database), use inline `style` attributes. To safelist specific utility classes in v4:

```css
@source inline("bg-{blue,red,green}-{400,500,600}");
```
