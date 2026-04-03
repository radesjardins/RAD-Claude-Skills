---
name: tailwind-dark-mode-theming
description: >
  This skill should be used when implementing dark mode with Tailwind CSS, setting up the @theme
  directive in v4, configuring media vs class-based dark mode, building multi-theme systems,
  using @variant dark, creating semantic design tokens, working with CSS custom properties in
  Tailwind, or troubleshooting dark mode toggle behavior.
---

# Tailwind CSS: Dark Mode & Theming

## Dark Mode Strategies

### Strategy 1: OS Preference (media — default)

No configuration needed. Tailwind v4 respects `prefers-color-scheme` by default:

```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
```

Choose this when users do not need a manual toggle.

### Strategy 2: Manual Toggle (class)

Add to your CSS to switch to class-based dark mode:

```css
@import "tailwindcss";

/* Override dark mode strategy */
@variant dark (&:where(.dark, .dark *));
```

Manage the `.dark` class via JavaScript:

```js
document.documentElement.classList.toggle('dark', isDark)
localStorage.setItem('theme', isDark ? 'dark' : 'light')
```

**Critical rule:** Always compose both light and dark utilities explicitly. Tailwind never infers the dark variant:

```html
<!-- Every color needs both states declared -->
<div class="bg-white text-gray-900 dark:bg-gray-900 dark:text-white">
  <button class="bg-brand-500 hover:bg-brand-600 dark:bg-brand-400 dark:hover:bg-brand-300">
    Submit
  </button>
</div>
```

---

## CSS-First Configuration with @theme

In Tailwind v4, all configuration is CSS-native. The `tailwind.config.js` file is gone.

```css
@import "tailwindcss";

@theme {
  /* Colors -> generates bg-*, text-*, border-*, etc. */
  --color-brand-500: oklch(60% 0.18 265);
  --color-brand-600: oklch(52% 0.18 265);
  --color-surface: oklch(98% 0 0);
  --color-surface-dark: oklch(15% 0 0);

  /* Spacing -> feeds p-*, m-*, w-*, h-*, gap-* */
  --spacing-18: 4.5rem;

  /* Typography */
  --font-display: "Cal Sans", system-ui, sans-serif;

  /* Sub-properties bundle with the parent utility */
  --text-xs: 0.75rem;
  --text-xs--line-height: 1.5;
}
```

### Key Namespaces

| Namespace | Generated utilities |
|-----------|-------------------|
| `--color-*` | `bg-*`, `text-*`, `border-*`, `fill-*`, `ring-*`, `shadow-*` |
| `--spacing-*` | `p-*`, `m-*`, `w-*`, `h-*`, `gap-*`, `inset-*`, `size-*` |
| `--font-*` | `font-*` (font-family) |
| `--text-*` | `text-*` (font-size + sub-properties) |
| `--rounded-*` | `rounded-*` |
| `--shadow-*` | `shadow-*` |

### @theme reference — Lean Bundle Mode

Suppress CSS variable emission while still generating utilities:

```css
@theme reference {
  --color-brand-500: oklch(60% 0.18 265);
}
```

Use when tokens drive utility generation but are not referenced via `var()` at runtime.

### Disabling Default Theme

```css
@theme {
  --*: initial;          /* Wipe ALL defaults */
  --color-primary: oklch(60% 0.18 265);  /* Only your tokens */
}
```

Wipe a specific namespace: `--font-*: initial;`

---

## Multi-Theme Patterns

Map Tailwind tokens to semantic CSS variables swappable at runtime:

```css
@theme {
  --color-primary-500: oklch(60% 0.18 265);
  --color-secondary-500: oklch(65% 0.15 150);

  /* Semantic tokens */
  --color-action: var(--color-primary-500);
  --color-accent: var(--color-secondary-500);
}

/* Theme override via data attribute */
[data-theme="green"] {
  --color-action: var(--color-secondary-500);
  --color-accent: var(--color-primary-500);
}
```

In components, use semantic utilities: `bg-action`, `text-accent`. Switching themes requires only a data attribute change — zero HTML changes.

---

## CSS Variable Scope Gotcha

When a theme token references another CSS variable, browser scope resolution can produce unexpected results in deep DOM trees:

```css
@theme {
  --font-primary: var(--font-sans);  /* May resolve differently in nested scopes */
}

/* Fix: use inline mode for literal values */
@theme inline {
  --font-primary: Inter Variable, system-ui, sans-serif;
}
```

---

## Quick Rules

| Concern | Rule |
|---------|------|
| Default dark mode | `media` strategy — no config needed |
| Manual toggle | `@variant dark (&:where(.dark, .dark *))` in CSS |
| Dark class | Always explicit on both light and dark states |
| Design tokens | All in `@theme {}` in CSS, never in JS config |
| Multi-theme | Semantic CSS variables + data attribute switching |
| Arbitrary values | Only for truly one-off values, never for design system tokens |
| Bundle optimization | Use `@theme reference` for non-runtime tokens |
