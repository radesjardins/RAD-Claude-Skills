# Tailwind CSS: Anti-Patterns, Edge Cases & Accessibility

## Anti-Pattern Catalog

### 1. `@apply` Overuse

**The pattern:**
```css
/* WRONG — recreating traditional CSS with @apply */
.btn {
  @apply inline-flex items-center px-4 py-2 rounded-md font-medium;
  @apply bg-blue-500 text-white hover:bg-blue-600;
}
.btn-sm {
  @apply px-3 py-1.5 text-sm;
}
.btn-lg {
  @apply px-6 py-3 text-lg;
}
```

**Why it fails:**
- Duplicates property-value pairs in the CSS output (bloat)
- Interaction variants (`hover:`, `focus:`, `active:`) inside `@apply` still require separate rules
- Breaks the utility-first contract — you are now back to writing semantic CSS
- Styles are not co-located with markup; the mental model fragments

**Correct replacement:**
```tsx
// Use a framework component with CVA
const button = cva("inline-flex items-center rounded-md font-medium", {
  variants: {
    intent: {
      primary: "bg-blue-500 text-white hover:bg-blue-600",
    },
    size: {
      sm: "px-3 py-1.5 text-sm",
      md: "px-4 py-2 text-base",
      lg: "px-6 py-3 text-lg",
    },
  },
  defaultVariants: { intent: "primary", size: "md" },
})
```

**Legitimate `@apply` uses:**
- Styling Markdown or rich-text CMS content (`prose` equivalents)
- Styling third-party library output where class names cannot be added
- Plain HTML projects without component frameworks

---

### 2. Arbitrary "Magic" Values

**The pattern:**
```html
<!-- WRONG — magic values that fragment the design system -->
<div class="w-[347px] h-[203px] bg-[#5B3BFF] text-[13px] mt-[18px]">
```

**Why it fails:**
- One-off values create an inconsistent visual system
- Cannot be globally updated
- Reviewers have no way to verify design intent

**Correct approach:**
```css
/* Define in @theme — generates utilities automatically */
@theme {
  --color-brand-500: #5B3BFF;
  --spacing-18: 4.5rem;  /* 18 × 4 = 72px but using rem */
}
```

```html
<!-- CORRECT — tokens, not magic numbers -->
<div class="w-64 bg-brand-500 text-sm mt-18">
```

**When arbitrary values are acceptable:**
- Truly one-off values that will never be reused (e.g., matching a specific legacy layout measurement)
- Values from external data (always use inline `style` for these, not arbitrary classes)

---

### 3. Class Soup (Unsorted Classes)

**The pattern:**
```html
<!-- WRONG — random ordering makes scanning impossible -->
<div class="hover:bg-blue-700 w-full p-4 text-white font-bold flex bg-blue-500 rounded-lg items-center justify-between text-lg shadow-md md:p-6">
```

**Why it fails:**
- Cannot quickly scan for layout, spacing, or typography
- Merge conflicts are harder to resolve
- Inconsistency across team members

**Correct approach:**
```html
<!-- CORRECT — Outside-In order -->
<div class="flex w-full items-center justify-between rounded-lg p-4 text-lg font-bold text-white shadow-md bg-blue-500 hover:bg-blue-700 md:p-6">
```

**Enforcement:** Install `prettier-plugin-tailwindcss`. It sorts classes to the canonical order on save. No manual effort required after initial setup.

```bash
npm install --save-dev prettier prettier-plugin-tailwindcss
```

```json
// .prettierrc
{
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

---

### 4. String Concatenation for Overrides

**The pattern:**
```tsx
// WRONG — specificity is determined by stylesheet order, not HTML order
function Button({ className }) {
  return (
    <button className={`bg-blue-500 text-white ${className}`}>
  )
}

// Consumer passes "bg-red-500" — may or may not work
<Button className="bg-red-500" />
```

**Why it fails:**
- CSS specificity is determined by the order rules appear in the compiled stylesheet
- `bg-blue-500` and `bg-red-500` both exist in the attribute; the browser picks based on CSS position
- Result is non-deterministic from the developer's perspective

**Correct approach:**
```tsx
// CORRECT — cn() resolves conflicts at runtime
function Button({ className }) {
  return (
    <button className={cn("bg-blue-500 text-white", className)}>
  )
}
// tailwind-merge removes bg-blue-500 when bg-red-500 is passed
```

---

### 5. Neglecting Semantic HTML

**The pattern:**
```html
<!-- WRONG — divs everywhere, Tailwind handles "all" styling -->
<div class="flex items-center gap-2 cursor-pointer" onclick="handleClick()">
  <div class="text-blue-500 text-sm font-medium">Click me</div>
</div>
```

**Why it fails:**
- Screen readers cannot identify the element as interactive
- Keyboard users cannot tab to or activate it
- Tailwind is visual-only; it cannot make a `<div>` behave like a `<button>`

**Correct approach:**
```html
<!-- CORRECT — semantic HTML + Tailwind for styling -->
<button
  class="inline-flex items-center gap-2 text-sm font-medium text-blue-500 hover:text-blue-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
  type="button"
>
  Click me
</button>
```

---

### 6. Using Legacy Preprocessors with Tailwind v4

**The pattern:**
```scss
// WRONG — Sass with Tailwind v4
$brand-color: #5B3BFF;

.card {
  @apply bg-blue-500;  // Already an anti-pattern
  background: mix($brand-color, white, 80%);  // Sass-specific
}
```

**Why it fails:**
- Tailwind v4's Oxide engine replaces Sass features with native CSS
- `color-mix()` replaces Sass `mix()`
- CSS nesting replaces Sass nesting
- `@property` replaces typed Sass variables
- Running Sass alongside Oxide degrades build performance

**Migration:**
```css
/* CORRECT — native CSS equivalents in Tailwind v4 */
.card {
  background: color-mix(in oklch, var(--color-brand-500) 80%, white);
}
```

---

## Edge Cases

### Dynamic Class Construction

Tailwind's scanner uses **static analysis** — it cannot detect runtime-constructed class strings:

```tsx
// WRONG — scanner cannot detect this class
const colorClass = `text-${props.color}-500`  // → class never generated

// CORRECT option 1 — complete class strings
const colorClass = props.color === "red" ? "text-red-500" : "text-blue-500"

// CORRECT option 2 — lookup table
const COLOR_CLASSES = {
  red:   "text-red-500",
  blue:  "text-blue-500",
  green: "text-green-500",
}
const colorClass = COLOR_CLASSES[props.color] ?? "text-gray-500"

// CORRECT option 3 — truly dynamic values from API/database
// → Use inline style attribute, not arbitrary classes
<div style={{ color: product.brandColor }}>
```

**Safelisting in v4** (last resort for dynamic patterns):
```css
@source inline("bg-{red,blue,green}-{400,500,600}");
```

---

### CSS Variable Scope in @theme (v4)

Tailwind v4 tokens are CSS custom properties. When a theme token references another CSS variable, browser scope resolution can produce unexpected fallbacks in deep DOM trees.

**The problem:**
```css
@theme {
  /* --font-sans may be overridden in a child component's styles */
  --font-primary: var(--font-sans);
}
```

If `--font-sans` is redefined deeper in the DOM, `--font-primary` resolves to the redefined value.

**Workaround — use `inline` mode for literal values:**
```css
@theme inline {
  /* Outputs the resolved value, not a var() reference */
  --font-primary: Inter Variable, system-ui, sans-serif;
}
```

---

### Container Query Context Clashes

In complex nested layouts, a component might accidentally respond to the wrong ancestor container.

**The problem:**
```html
<div class="@container">  <!-- Sidebar: 280px wide -->
  <div class="@container">  <!-- Card: 240px wide -->
    <!-- This responds to the INNER container (card), which is correct -->
    <!-- But if we want the outer (sidebar), there's no way to specify -->
    <div class="@sm:flex-row">...</div>
  </div>
</div>
```

**Solution — named containers:**
```html
<div class="@container/sidebar">
  <div class="@container/card">
    <div class="@sm/card:flex-row @lg/sidebar:hidden">
      <!-- Now explicit: @sm responds to /card, @lg responds to /sidebar -->
    </div>
  </div>
</div>
```

---

### The Mouse-Click Focus Ring Problem

**The problem:**
Using `focus:ring-2` adds a focus ring on both mouse clicks and keyboard navigation. Removing it entirely (`outline-none` with no replacement) destroys keyboard accessibility.

**Correct solution — `focus-visible:`:**
```html
<!-- WRONG: ring appears on mouse click -->
<button class="focus:ring-2 focus:ring-blue-500">

<!-- WRONG: no ring at all — accessibility failure -->
<button class="focus:outline-none">

<!-- CORRECT: ring only during keyboard nav -->
<button class="outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
```

`focus-visible:` defers to browser heuristics: it shows the ring only when the browser determines it is needed (keyboard navigation, not mouse click).

**v4 note:** `outline-none` was redefined in v4 to remove the outline in an accessible manner (using `outline: 2px solid transparent`). The old behavior moved to `outline-hidden`. However, using `focus-visible:ring-*` is still the preferred pattern.

---

### Conflicting Utilities Override Pattern

When you need CSS-level override guarantees without `tailwind-merge`:

**Option 1: The `!` important modifier (v4 — suffix position)**
```html
<!-- v4: exclamation is a SUFFIX, not a prefix -->
<div class="bg-blue-500 bg-red-500!">  <!-- bg-red-500 always wins -->
```

**Option 2: `:where()` variant to lower base specificity**
```css
/* In component CSS — base styles with intentionally low specificity */
@layer components {
  :where(.card-base) {
    @apply rounded-lg p-4 bg-white;
  }
}
/* Any utility class now overrides .card-base due to higher specificity */
```

**Recommendation:** Use `tailwind-merge` in components (runtime solution) instead of CSS specificity tricks (build-time fragility).

---

## Accessibility Implementation Guide

### Focus Management Checklist

```html
<!-- Every interactive element pattern -->
<!-- Classes: outline-none (remove browser default) -->
<!--          focus-visible:ring-2 (keyboard-only ring) -->
<!--          focus-visible:ring-brand-500 (brand color) -->
<!--          focus-visible:ring-offset-2 (breathing room) -->
<!--          focus-visible:ring-offset-white (contrast on light) -->
<!--          dark:focus-visible:ring-offset-gray-900 (contrast on dark) -->
<button
  type="button"
  class="outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:focus-visible:ring-offset-gray-900"
>
```

### Screen Reader Utilities

```html
<!-- sr-only: visually hidden, accessible to screen readers -->
<button class="p-2 rounded-md hover:bg-gray-100">
  <svg aria-hidden="true" class="h-5 w-5"><!-- icon --></svg>
  <span class="sr-only">Open navigation menu</span>
</button>

<!-- not-sr-only: reverse sr-only (make visible again) -->
<span class="sr-only focus-visible:not-sr-only">Skip to content</span>
```

### High Contrast Mode (forced-colors)

Windows and some accessibility tools force a high-contrast color palette. Tailwind v4 provides `forced-colors:` variants:

```html
<button
  class="
    bg-brand-500 text-white
    forced-colors:border-2 forced-colors:border-current
  "
>
  <!-- In forced-colors mode, background may be overridden;
       add a visible border to ensure the button boundary is perceivable -->
</button>
```

### ARIA + Tailwind State Synchronization

Tailwind provides variants for ARIA states — keep visual state in sync with ARIA state:

```html
<button
  aria-expanded="false"
  class="
    aria-expanded:bg-gray-100
    aria-expanded:rotate-180
  "
>
  <svg class="transition-transform duration-200"><!-- chevron --></svg>
</button>
```

Available ARIA variants: `aria-checked:`, `aria-disabled:`, `aria-expanded:`, `aria-hidden:`, `aria-pressed:`, `aria-required:`, `aria-selected:`, `aria-invalid:`.

### Color Contrast Requirements

WCAG 2.1 AA minimums:
- Normal text (< 18px or < 14px bold): **4.5:1 contrast ratio**
- Large text (≥ 18px or ≥ 14px bold): **3:1 contrast ratio**
- Interactive component boundaries (buttons, inputs): **3:1 against adjacent color**
- Focus indicators: **3:1 against adjacent color**

Using `oklch()` color space in `@theme` tokens makes contrast calculation predictable because lightness (`L`) maps directly to perceived brightness.

```css
@theme {
  /* High-contrast pair — L 60% on white, L 90% on dark */
  --color-brand-600: oklch(40% 0.18 265);   /* on white: high contrast */
  --color-brand-300: oklch(80% 0.12 265);   /* on dark: high contrast */
}
```

---

## Legacy Browser Support

Tailwind v4 requires modern browser features:

| Feature | Minimum browser |
|---------|----------------|
| Native CSS `@layer` | Chrome 99, Safari 15.4, Firefox 97 |
| `color-mix()` | Chrome 111, Safari 16.2, Firefox 113 |
| CSS `@property` | Chrome 85, Safari 16.4, Firefox 128 |
| CSS nesting | Chrome 112, Safari 16.5, Firefox 117 |
| **Tailwind v4 overall** | **Chrome 111+, Safari 16.4+, Firefox 128+** |

If your project requires support for older browsers (IE11, older Safari, pre-2023 Chrome), remain on **Tailwind v3** and use PostCSS plugins to polyfill modern CSS features. Do not attempt to use Tailwind v4 with a polyfill stack — the Oxide engine generates CSS that relies on browser-native feature support.
