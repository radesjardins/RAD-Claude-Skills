---
name: tailwind-best-practices
description: >
  This skill should be used when working on any project that uses Tailwind CSS, or when the user
  asks about Tailwind CSS best practices, conventions, or patterns — including writing or reviewing
  utility classes, configuring Tailwind v4 with @theme, migrating from v3 to v4, building
  multi-variant components with CVA, setting up tailwind-merge or the cn() utility, implementing
  dark mode or theming, using container queries with @container, organizing class ordering,
  avoiding class soup or @apply overuse, optimizing Tailwind bundle size, integrating Tailwind with
  Astro/React/Vue/Svelte, handling responsive design, enforcing design token consistency, or
  troubleshooting Tailwind configuration issues.
---

# Tailwind CSS: Coding Standards & Best Practices

Comprehensive reference for building with Tailwind CSS consistently, readably, and at scale. Apply these standards whenever writing or reviewing Tailwind code.

## Core Mental Model

Tailwind enforces styling through a **predefined design system of constraints**. This is not a limitation — it is the feature. The constraint model guarantees visual consistency and keeps CSS bundles from growing linearly.

**Five invariants that govern all Tailwind decisions:**

1. **Inline utilities are the default.** Keep classes in HTML/JSX. Reach for abstraction only when duplication spans multiple files.
2. **Component abstraction beats CSS abstraction.** Extract to a framework component (React, Vue, Astro) first. Use `@apply` only when you cannot control the HTML.
3. **The `@theme` directive is the single source of truth.** All design tokens (colors, spacing, typography) live in CSS, not in JavaScript config files (v4+).
4. **Class ordering must be deterministic.** Unsorted class soup is unmaintainable. Use the Outside-In order enforced by `prettier-plugin-tailwindcss`.
5. **Mobile-first is not negotiable.** Unprefixed utilities apply to all screens. Prefixes (`md:`, `lg:`) apply upward. Never design desktop-first and add mobile overrides.

---

## 1. Class Ordering — Outside-In

Apply the Outside-In methodology: order classes from the element's macro-context inward to its visual details. Automate this with `prettier-plugin-tailwindcss`.

```
1. Layout & Positioning  → container, flex, grid, absolute, relative, inset-0, z-10
2. Box Model             → w-full, h-64, p-4, m-2, gap-4, overflow-hidden
3. Typography            → text-center, text-lg, font-bold, leading-tight, tracking-wide
4. Visual Styling        → bg-blue-500, text-white, border, rounded-lg, shadow-md, opacity-80
5. Interactivity/States  → hover:bg-gray-100, focus-visible:ring-2, transition-all, cursor-pointer
6. Responsive/Container  → md:grid-cols-2, lg:flex-row, @lg:flex-row, dark:bg-gray-900
```

Always install `prettier-plugin-tailwindcss` — it enforces this order automatically and eliminates class ordering debates.

---

## 2. Design Tokens — v4 CSS-First Configuration

In Tailwind v4, all configuration is CSS-native. The `tailwind.config.js` file is gone.

```css
/* src/styles/global.css */
@import "tailwindcss";

@theme {
  /* Colors — generates bg-brand, text-brand, border-brand, etc. */
  --color-brand-500: #6366f1;
  --color-brand-600: #4f46e5;
  --color-surface: oklch(98% 0 0);
  --color-surface-dark: oklch(15% 0 0);

  /* Spacing — feeds padding, margin, width, gap utilities */
  --spacing-18: 4.5rem;

  /* Typography */
  --font-display: "Cal Sans", system-ui, sans-serif;
  --text-xs--line-height: 1.5;   /* sub-property: bundles with text-xs */
}
```

**Rules:**
- Define tokens here — never use `w-[347px]` or `bg-[#ff0000]` for values that appear more than once
- Use `@theme reference` if tokens only drive utility generation but should not emit CSS variables (keeps bundle lean)
- Disable the default theme with `--*: initial;` to enforce a strict proprietary design system
- Reference tokens in non-Tailwind CSS via `var(--color-brand-500)` — they are real CSS variables

---

## 3. Responsive Design — Mobile-First + Container Queries

### Viewport Breakpoints (page-level)
```html
<!-- CORRECT: mobile-first — base style for all, md: enhances -->
<div class="flex flex-col md:flex-row gap-4">

<!-- WRONG: desktop-first with mobile overrides -->
<div class="flex-row max-md:flex-col gap-4">
```

### Container Queries (component-level)
Use `@container` for portable components that must adapt to their parent, not the viewport:

```html
<!-- Parent declares itself a container -->
<div class="@container">
  <!-- Child adapts to parent width, not browser width -->
  <div class="flex flex-col @sm:flex-row @lg:grid @lg:grid-cols-3">
    ...
  </div>
</div>
```

Use **named containers** in complex nested layouts to target a specific ancestor:
```html
<div class="@container/card">
  <div class="@sm/card:text-lg @lg/card:text-xl">...</div>
</div>
```

**Rule:** Use viewport breakpoints for page-level layout shifts. Use container queries for reusable UI components.

---

## 4. Component Patterns — When to Extract

**Keep inline when:**
- Duplication is rendered via a loop (the class string is written once)
- Duplication is localized to a single file (use multi-cursor editing)

**Extract to framework component when:**
- The same UI pattern spans multiple files
- The element requires multiple variants (size, intent, state)

**Extract to `@apply` only when:**
- The HTML is not under your control (third-party library output, CMS-rendered Markdown)
- You are in a non-component environment (plain HTML, backend templating)

### CVA for Multi-Variant Components

Use Class Variance Authority (CVA) when a component needs variants:

```ts
import { cva, type VariantProps } from "class-variance-authority"

const button = cva(
  // Base classes — always applied
  "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:opacity-50",
  {
    variants: {
      intent: {
        primary: "bg-brand-500 text-white hover:bg-brand-600",
        secondary: "bg-white text-gray-900 border border-gray-200 hover:bg-gray-50",
        destructive: "bg-red-500 text-white hover:bg-red-600",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base",
      },
    },
    defaultVariants: { intent: "primary", size: "md" },
  }
)

type ButtonProps = VariantProps<typeof button> & { className?: string }
```

### The `cn()` Utility — Always Use for Override-Accepting Components

```ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

// Standard cn() pattern — use everywhere a component accepts className
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

**Rule:** Use `cn()` whenever a component accepts an external `className` prop. CSS specificity is resolved by stylesheet order, not HTML attribute order — without `tailwind-merge`, override classes fail unpredictably.

**Performance:** Use `twJoin` (not `twMerge`) for internal-only class joining where no external override conflicts can occur.

---

## 5. Dark Mode

Tailwind v4 has two dark mode strategies:

- **`media` (default)** — respects the user's OS preference via `prefers-color-scheme`. No configuration needed. Choose this when users do not need a manual toggle.
- **`class`** — activates dark mode by applying `.dark` to the `<html>` element. Required when users need an explicit light/dark toggle independent of OS settings.

To switch to class-based dark mode, add this to your CSS:

```css
/* global.css — override the default media strategy */
@variant dark (&:where(.dark, .dark *));
```

Then manage the `.dark` class via JavaScript:
```js
document.documentElement.classList.toggle('dark', prefersDark)
localStorage.setItem('theme', prefersDark ? 'dark' : 'light')
```

Always compose both light and dark utilities explicitly — Tailwind never infers the dark variant:

```html
<!-- Every color needs both states declared -->
<div class="bg-white text-gray-900 dark:bg-gray-900 dark:text-white">
  <button class="bg-brand-500 text-white hover:bg-brand-600 dark:bg-brand-400 dark:hover:bg-brand-300">
    Submit
  </button>
</div>
```

For multi-theme or portal scenarios, use semantic CSS variables in `@theme` that can be swapped via a data attribute. See `references/v4-config-theming.md` for the full multi-theme pattern.

---

## 6. Accessibility Requirements

Tailwind handles visual styling only. Accessibility responsibilities are always the developer's:

**Focus management (critical):**
- **Always use `focus-visible:` not `focus:`** — `focus:` fires on mouse clicks; `focus-visible:` fires only when the browser determines a visible indicator is needed (keyboard navigation, programmatic focus). This is the correct pattern for every interactive element.
- **Never suppress focus rings without a custom replacement.** In v4, `outline-none` applies an accessible transparent outline. Use it with an explicit `focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2`.

```html
<!-- CORRECT pattern for all interactive elements -->
<button class="outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2">
```

**Screen reader support:**
- `sr-only` hides text visually while keeping it available to assistive technology. Use it for icon-only buttons and decorative labels.
- `not-sr-only` reverses `sr-only`, useful for skip-to-content links that become visible on focus.

**ARIA state variants:** Tailwind provides variants that sync visual and semantic state automatically:
```html
<button aria-expanded="false" class="aria-expanded:bg-gray-100 aria-expanded:rotate-180">
```
Available: `aria-checked:`, `aria-disabled:`, `aria-expanded:`, `aria-pressed:`, `aria-selected:`, `aria-invalid:`.

**High-contrast mode:** Use `forced-colors:` variants to ensure components remain perceivable when Windows forced-colors mode overrides your color tokens.

---

## 7. Browser Support & Preprocessors

Tailwind v4 is built on modern CSS platform features — native `@layer`, `color-mix()`, and `@property`. This requires up-to-date browsers: **Chrome 111+, Safari 16.4+, and Firefox 128+**. If your project must support older browsers, remain on Tailwind v3.

Do not use Sass, Less, or Stylus alongside Tailwind v4. The Oxide engine's native CSS support (`color-mix()`, CSS nesting, logical properties) replaces everything these preprocessors provide. Running them together degrades build performance without benefit.

---

## 8. Quick Rules Checklist

| Concern | Rule |
|---------|------|
| Class ordering | Outside-In; enforced by `prettier-plugin-tailwindcss` |
| Design tokens | All in `@theme {}` in CSS, not JS config |
| Arbitrary values | Only for truly one-off values; never for design system values |
| `@apply` | Only when HTML is not controllable |
| Responsive | Mobile-first, always |
| Component responsive | Container queries (`@container`) over viewport breakpoints |
| Variants | CVA for multi-variant components |
| Class override merging | `cn()` = `clsx` + `tailwind-merge` on all className-accepting components |
| Focus states | `focus-visible:` always; never suppress focus rings without replacement |
| v4 config | CSS `@theme` directive; no `tailwind.config.js` |
| Dark mode | `@variant dark` in CSS; `.dark` on `<html>` element |
| Sass/Less | Never use with Tailwind v4; native CSS replaces preprocessors |
| Browser support | v4 requires Chrome 111+, Safari 16.4+, Firefox 128+ |

---

## Additional Resources

### Reference Files

For detailed patterns and deep technical content, consult:

- **`references/v4-config-theming.md`** — Full @theme syntax, design token namespaces, dark mode strategies, multi-theme patterns, production bundle optimization, v3→v4 migration breaking changes
- **`references/component-patterns.md`** — CVA compound variants, tailwind-merge configuration, cn() advanced patterns, container query named containers, CSS variable scoping
- **`references/anti-patterns-edge-cases.md`** — Complete anti-pattern catalog, dynamic class safety, edge cases (container query nesting, CSS variable scope, legacy browser support), accessibility implementation guide
