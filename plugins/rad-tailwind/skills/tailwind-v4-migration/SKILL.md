---
name: tailwind-v4-migration
description: >
  This skill should be used when migrating from Tailwind CSS v3 to v4, understanding breaking
  changes, using the official upgrade tool (npx @tailwindcss/upgrade), resolving v4 migration
  issues, understanding the Oxide engine, configuring @tailwindcss/vite or @tailwindcss/postcss,
  or troubleshooting Tailwind v4 build or configuration problems.
---

# Tailwind CSS: v3 to v4 Migration

## The Oxide Engine

Tailwind v4 rebuilds the engine in Rust (codename **Oxide**):

- Full builds up to **5x faster** than v3; incremental rebuilds in **microseconds**
- **Automatic content detection** — scans project, respects `.gitignore`, skips binaries. No `content` array needed.
- **Single entry point**: `@import "tailwindcss"` replaces the three `@tailwind` directives
- **Autoprefixer built-in** — remove it from PostCSS config
- **Native CSS `@layer`** — eliminates specificity bugs from v3

### Build Tool Integration

| Tool | Plugin |
|------|--------|
| Vite | `@tailwindcss/vite` (recommended) |
| PostCSS | `@tailwindcss/postcss` (replaces old `tailwindcss` PostCSS plugin) |
| CLI | `@tailwindcss/cli` |

Do not use the generic `tailwindcss` PostCSS plugin with v4.

---

## Breaking Changes

| v3 | v4 | Impact |
|----|----|--------|
| `tailwind.config.js` | `@theme {}` in CSS | High |
| `@tailwind base/components/utilities` | `@import "tailwindcss"` | High |
| `tailwindcss` PostCSS plugin | `@tailwindcss/postcss` | High |
| `bg-gradient-to-r` | `bg-linear-to-r` | Medium |
| `bg-opacity-*`, `text-opacity-*` | Slash syntax `bg-blue-500/50` | Medium |
| `shadow-sm` | `shadow-xs` | Low |
| `rounded-sm` | `rounded-xs` | Low |
| `blur-sm` | `blur-xs` | Low |
| Default border color (gray) | `currentColor` | Medium |
| Default ring width (3px) | 1px | Low |
| `!bg-red-500` (prefix `!`) | `bg-red-500!` (suffix `!`) | Medium |
| `outline-none` | `outline-hidden` / `outline-none` (accessible) | Medium |

---

## New Features in v4

- **3D Transforms**: `rotate-x-*`, `rotate-y-*`, `translate-z-*`, `perspective-*`, `transform-3d`
- **Not variant**: `not-hover:`, `not-focus:`, `not-disabled:`
- **Container queries**: built-in, no plugin needed
- **Forced colors**: `forced-colors:` variants for Windows high-contrast
- **`@starting-style` animations**: animate elements as they mount
- **`@property` custom properties**: type-safe CSS variables
- **Expanded gradients**: `bg-radial-*`, `bg-conic-*`, color interpolation via `oklch`

---

## Using the Official Upgrade Tool

```bash
npx @tailwindcss/upgrade
```

The tool handles:
- Migrating `tailwind.config.js` to CSS `@theme`
- Rewriting `@tailwind` directives to `@import`
- Renaming deprecated utilities (`shadow-sm` -> `shadow-xs`, etc.)
- Converting `bg-opacity-*` to slash syntax
- Removing Autoprefixer from PostCSS config

**Does NOT handle:**
- Removing legacy plugins now built-in (aspect-ratio, container-queries) — do this manually
- Third-party plugin compatibility

---

## Legacy Plugin Bridge

If you rely on JS plugins not yet updated for v4:

```css
@import "tailwindcss";
@config "./tailwind.config.js"; /* Temporary bridge — migrate off it */
```

---

## Framework Setup (v4)

### Astro

```js
// astro.config.mjs
import tailwindcss from "@tailwindcss/vite"

export default defineConfig({
  vite: { plugins: [tailwindcss()] },
})
```

### React / Next.js

```css
/* app/globals.css */
@import "tailwindcss";
@theme { /* tokens */ }
```

### Vue / Nuxt

Use `@reference` in `<style scoped>` for token access without duplicate CSS:

```css
@reference "../../styles/global.css";
.custom { color: var(--color-brand-500); }
```

---

## Browser Requirements

Tailwind v4 requires modern browsers:

| Feature | Minimum |
|---------|---------|
| Native `@layer` | Chrome 99+, Safari 15.4+, Firefox 97+ |
| `color-mix()` | Chrome 111+, Safari 16.2+, Firefox 113+ |
| CSS `@property` | Chrome 85+, Safari 16.4+, Firefox 128+ |
| **v4 overall** | **Chrome 111+, Safari 16.4+, Firefox 128+** |

If you must support older browsers, stay on Tailwind v3.

---

## Production Optimization

- **Bundle size**: JIT generates only used classes. Typical: **under 10kB**.
- **Minification**: `tailwindcss --minify` or cssnano after `@tailwindcss/postcss`
- **Compression**: Always serve with **Brotli** (2-3kB over wire for 10kB bundle)
- **Safelisting dynamic classes**: `@source inline("bg-{red,blue,green}-{400,500,600}")`
- **No preprocessors**: Do not use Sass/Less/Stylus with v4 — native CSS replaces them

---

## Quick Migration Checklist

1. Run `npx @tailwindcss/upgrade`
2. Replace `tailwindcss` PostCSS plugin with `@tailwindcss/postcss` (or use `@tailwindcss/vite`)
3. Remove Autoprefixer from PostCSS config
4. Remove built-in plugins from dependencies (aspect-ratio, container-queries)
5. Update `!` important modifier from prefix to suffix
6. Replace `bg-opacity-*` / `text-opacity-*` with slash syntax
7. Replace `bg-gradient-to-*` with `bg-linear-to-*`
8. Verify `outline-none` usage (now accessible — use `outline-hidden` for old behavior)
9. Test border colors (default changed from gray to `currentColor`)
10. Verify browser support matrix meets your requirements
