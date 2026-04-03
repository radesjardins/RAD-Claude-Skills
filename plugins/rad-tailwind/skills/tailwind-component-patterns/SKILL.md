---
name: tailwind-component-patterns
description: >
  This skill should be used when building reusable Tailwind CSS components, implementing CVA
  (Class Variance Authority), setting up tailwind-merge, creating the cn() utility, deciding
  when to extract components vs use inline utilities, building multi-variant components, or
  working with class conflict resolution in Tailwind CSS.
---

# Tailwind CSS: Component Patterns

## The Abstraction Decision Tree

```
Does the same UI pattern appear in multiple files?
+-- NO  -> Keep utilities inline (or use multi-cursor/loop if same file)
+-- YES -> Extract to framework component
         +-- Does the component need multiple variants (size, intent, state)?
             +-- NO  -> Simple component with inline utilities
             +-- YES -> Use CVA (Class Variance Authority)
                       +-- Does the component accept external className overrides?
                           +-- YES -> Use cn() = clsx + tailwind-merge
```

Use `@apply` **only** when HTML is not under your control (third-party library output, CMS Markdown, legacy templates).

---

## CVA — Class Variance Authority

CVA is the standard tool for type-safe, multi-variant UI components.

```bash
npm install class-variance-authority
```

### Anatomy

```ts
import { cva, type VariantProps } from "class-variance-authority"

const badge = cva(
  // Base — always applied
  [
    "inline-flex items-center gap-1",
    "rounded-full px-2.5 py-0.5",
    "text-xs font-medium transition-colors",
  ],
  {
    variants: {
      intent: {
        default:     "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100",
        success:     "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
        destructive: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
      },
      dot: {
        true:  "before:mr-1 before:h-1.5 before:w-1.5 before:rounded-full before:bg-current",
        false: "",
      },
    },
    compoundVariants: [
      { intent: "destructive", dot: true, class: "before:animate-pulse" },
    ],
    defaultVariants: { intent: "default", dot: false },
  }
)

type BadgeProps = React.HTMLAttributes<HTMLSpanElement> & VariantProps<typeof badge>

export function Badge({ className, intent, dot, ...props }: BadgeProps) {
  return <span className={cn(badge({ intent, dot }), className)} {...props} />
}
```

### CVA Rules

- **Base classes** — use an array for readability; CVA flattens automatically
- **Variants** — one key per visual dimension (intent, size, shape)
- **Compound variants** — style combinations requiring multiple conditions
- **Default variants** — always provide so component renders without props
- **className merging** — always wrap CVA output in `cn()` when accepting external `className`

---

## tailwind-merge & the cn() Utility

### The Problem

CSS specificity is determined by stylesheet order, not HTML attribute order. Without `tailwind-merge`, class overrides fail unpredictably:

```ts
// Without tailwind-merge — BROKEN
`px-2 py-1 ${className}` // if className="px-4", BOTH px-2 and px-4 exist

// With tailwind-merge — CORRECT
twMerge("px-2 py-1", "px-4") // -> "py-1 px-4" (px-2 removed)
```

### Setup

```bash
npm install tailwind-merge clsx
```

```ts
// lib/utils.ts — create once, import everywhere
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### When to Use Which Function

| Function | Use case | Cost |
|----------|----------|------|
| `twMerge()` | Merging defaults with consumer `className` overrides | Higher |
| `twJoin()` | Conditional joining of internal classes (no overrides) | Lower |
| `clsx()` | Conditional class logic (boolean/object syntax) | Minimal |
| `cn()` | All-purpose: conditional + conflict resolution | Medium |

**Performance rule:** Use `twJoin` for internal class assembly, `twMerge` (via `cn()`) only at the boundary where consumer overrides arrive.

---

## String Concatenation Anti-Pattern

```tsx
// WRONG — specificity is non-deterministic
function Button({ className }) {
  return <button className={`bg-blue-500 text-white ${className}`}>
}

// CORRECT — cn() resolves conflicts at runtime
function Button({ className }) {
  return <button className={cn("bg-blue-500 text-white", className)}>
}
```

---

## Conditional State Composition

```tsx
function Button({ isLoading, isDisabled, variant = "primary" }) {
  return (
    <button
      className={cn(
        button({ intent: variant }),
        {
          "opacity-50 cursor-not-allowed": isDisabled,
          "cursor-wait": isLoading,
        }
      )}
      disabled={isDisabled || isLoading}
    />
  )
}
```

---

## Quick Rules

| Concern | Rule |
|---------|------|
| When to extract | Multi-file duplication -> framework component |
| When CVA | Multiple variants (size, intent, state) |
| When cn() | Component accepts external `className` |
| When @apply | Only when HTML is not controllable |
| twMerge vs twJoin | twMerge at boundaries, twJoin internally |
| String concat | Never use template literals for class merging |
