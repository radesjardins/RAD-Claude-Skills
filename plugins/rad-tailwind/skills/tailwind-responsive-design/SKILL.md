---
name: tailwind-responsive-design
description: >
  This skill should be used when working on responsive layouts with Tailwind CSS, implementing
  mobile-first design, using container queries (@container), choosing between viewport breakpoints
  and container queries, creating responsive grid or flex layouts, using @sm/@md/@lg container
  variants, named containers, or troubleshooting responsive behavior in Tailwind v4.
---

# Tailwind CSS: Responsive Design

## Mobile-First Is Not Negotiable

Unprefixed utilities apply to **all** screen sizes. Breakpoint prefixes (`sm:`, `md:`, `lg:`, `xl:`, `2xl:`) apply **upward** from their threshold. Never design desktop-first and add mobile overrides.

```html
<!-- CORRECT: mobile-first — base is mobile, md: enhances for larger -->
<div class="flex flex-col md:flex-row gap-4">

<!-- WRONG: desktop-first with mobile undoing -->
<div class="flex-row max-md:flex-col gap-4">
```

**Rule:** Start with the smallest screen, then layer enhancements with ascending breakpoint prefixes.

---

## Container Queries — Component-Level Responsive Design

Container queries let a component respond to its **parent's width**, not the browser viewport. This makes components truly portable across layouts.

### Setup

```html
<!-- Parent declares itself a container -->
<div class="@container">
  <!-- Child adapts to parent width -->
  <div class="flex flex-col @sm:flex-row @lg:grid @lg:grid-cols-3">
    ...
  </div>
</div>
```

### Container Breakpoints

| Variant | Min-width |
|---------|-----------|
| `@xs:` | 320px |
| `@sm:` | 384px |
| `@md:` | 448px |
| `@lg:` | 512px |
| `@xl:` | 576px |
| `@2xl:` | 672px |
| `@3xl:` | 768px |

Max-width variants: `@max-sm:`, `@max-md:`, etc.

### Named Containers — Avoid Context Clashes

In nested layouts, a child can accidentally respond to the wrong ancestor. Name containers to be explicit:

```html
<div class="@container/sidebar">
  <div class="@container/card">
    <!-- Targets /card, not /sidebar -->
    <div class="@sm/card:text-lg @lg/card:text-2xl">
      Card-responsive text
    </div>
    <!-- Explicitly targets /sidebar -->
    <div class="@lg/sidebar:hidden">Hidden when sidebar is wide</div>
  </div>
</div>
```

---

## When to Use Which

| Use viewport `md:` | Use container `@md:` |
|--------------------|----------------------|
| Page-level layout | Reusable UI component |
| Navigation, sidebars | Card, badge, avatar |
| App shell structure | Form fields |
| Document layout shifts | List items |

**Rule:** If a component can appear in multiple contexts at different parent widths, use container queries. If you are styling the page frame, use viewport breakpoints.

---

## Mobile-First Class Composition Pattern

```tsx
function ProductCard({ product }) {
  return (
    <div className={cn(
      // Mobile: single column, full width
      "flex flex-col gap-3 p-4 rounded-xl border",
      // Tablet: horizontal layout
      "@sm:flex-row @sm:items-center @sm:gap-4",
      // Wide: expand image
      "@lg:gap-6"
    )}>
      <img className="w-full rounded-lg @sm:w-24 @sm:shrink-0 @lg:w-32" />
      <div className="space-y-1">...</div>
    </div>
  )
}
```

---

## Quick Rules

| Concern | Rule |
|---------|------|
| Base styles | Always the mobile view — unprefixed utilities |
| Breakpoint direction | Upward only (`sm:`, `md:`, `lg:`) — never `max-*:` as primary strategy |
| Component responsive | `@container` for portable components |
| Page responsive | Viewport breakpoints (`md:`, `lg:`) for layout shell |
| Nested containers | Always use named containers (`@container/name`) |
| Container queries in v4 | Built-in, no plugin needed |
