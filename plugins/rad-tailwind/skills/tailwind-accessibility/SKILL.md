---
name: tailwind-accessibility
description: >
  This skill should be used when working on accessibility with Tailwind CSS, implementing focus
  rings with focus-visible:, using sr-only and not-sr-only, syncing ARIA state with Tailwind
  variants, handling forced-colors mode, ensuring color contrast with Tailwind tokens, or
  reviewing Tailwind code for accessibility issues.
---

# Tailwind CSS: Accessibility

Tailwind handles visual styling only. Accessibility is always the developer's responsibility.

---

## Focus Management

### Always Use `focus-visible:` — Never `focus:`

`focus:` fires on mouse clicks. `focus-visible:` fires only when the browser determines a visible indicator is needed (keyboard navigation, programmatic focus).

```html
<!-- WRONG: ring appears on mouse click -->
<button class="focus:ring-2 focus:ring-blue-500">

<!-- WRONG: no ring at all — accessibility failure -->
<button class="focus:outline-none">

<!-- CORRECT: ring only during keyboard navigation -->
<button class="outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2">
```

### Standard Focus Pattern

Apply to **every** interactive element:

```html
<button
  type="button"
  class="
    outline-none
    focus-visible:ring-2
    focus-visible:ring-brand-500
    focus-visible:ring-offset-2
    focus-visible:ring-offset-white
    dark:focus-visible:ring-offset-gray-900
  "
>
```

### v4 Note on `outline-none`

In v4, `outline-none` was redefined to be accessible (`outline: 2px solid transparent`). The old behavior moved to `outline-hidden`. Using `focus-visible:ring-*` is still the preferred pattern.

---

## Screen Reader Utilities

### `sr-only` — Visually Hidden, Accessible

```html
<!-- Icon-only button with accessible label -->
<button class="p-2 rounded-md hover:bg-gray-100">
  <svg aria-hidden="true" class="h-5 w-5"><!-- icon --></svg>
  <span class="sr-only">Open navigation menu</span>
</button>
```

### `not-sr-only` — Reverse sr-only

Useful for skip-to-content links that become visible on focus:

```html
<a href="#main" class="sr-only focus-visible:not-sr-only focus-visible:absolute focus-visible:top-4 focus-visible:left-4 focus-visible:z-50 focus-visible:bg-white focus-visible:px-4 focus-visible:py-2 focus-visible:rounded-md focus-visible:shadow-lg">
  Skip to content
</a>
```

---

## ARIA State Synchronization

Tailwind provides variants that sync visual and semantic state automatically:

```html
<button
  aria-expanded="false"
  class="aria-expanded:bg-gray-100 aria-expanded:rotate-180"
>
  <svg class="transition-transform duration-200"><!-- chevron --></svg>
</button>
```

Available ARIA variants:
- `aria-checked:` — checkboxes, toggles
- `aria-disabled:` — disabled state
- `aria-expanded:` — dropdowns, accordions
- `aria-hidden:` — hidden elements
- `aria-pressed:` — toggle buttons
- `aria-required:` — required form fields
- `aria-selected:` — tabs, listbox items
- `aria-invalid:` — form validation

---

## High Contrast Mode (forced-colors)

Windows and some accessibility tools force a high-contrast color palette. Tailwind v4 provides `forced-colors:` variants:

```html
<button
  class="
    bg-brand-500 text-white
    forced-colors:border-2 forced-colors:border-current
  "
>
  <!-- In forced-colors mode, background may be overridden;
       border ensures button boundary is perceivable -->
</button>
```

---

## Color Contrast Requirements

WCAG 2.1 AA minimums:

| Element | Minimum ratio |
|---------|--------------|
| Normal text (< 18px or < 14px bold) | **4.5:1** |
| Large text (>= 18px or >= 14px bold) | **3:1** |
| Interactive component boundaries | **3:1** |
| Focus indicators | **3:1** |

Using `oklch()` in `@theme` tokens makes contrast predictable — lightness (`L`) maps directly to perceived brightness:

```css
@theme {
  --color-brand-600: oklch(40% 0.18 265);   /* on white: high contrast */
  --color-brand-300: oklch(80% 0.12 265);   /* on dark: high contrast */
}
```

---

## Semantic HTML Reminder

Tailwind is visual-only. It cannot make a `<div>` behave like a `<button>`:

```html
<!-- WRONG — inaccessible to keyboard/screen readers -->
<div class="cursor-pointer" onclick="handleClick()">Click me</div>

<!-- CORRECT — semantic element + Tailwind styling -->
<button type="button" class="text-blue-500 hover:text-blue-600 focus-visible:ring-2">
  Click me
</button>
```

---

## Quick Rules

| Concern | Rule |
|---------|------|
| Focus rings | `focus-visible:` always, never `focus:` |
| Suppressing outlines | Only with a custom replacement ring |
| Icon buttons | Always add `<span class="sr-only">Label</span>` |
| Skip links | `sr-only` + `focus-visible:not-sr-only` |
| ARIA sync | Use `aria-expanded:`, `aria-checked:`, etc. |
| High contrast | Add `forced-colors:border-2` to interactive elements |
| Contrast ratios | 4.5:1 text, 3:1 large text/components |
| Semantic HTML | Use `<button>`, `<a>`, `<input>` — not styled `<div>` |
