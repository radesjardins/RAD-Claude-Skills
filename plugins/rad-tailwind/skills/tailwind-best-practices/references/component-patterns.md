# Tailwind CSS: Component Patterns & Tooling

## The Abstraction Decision Tree

```
Does the same UI pattern appear in multiple files?
├── NO  → Keep utilities inline (or use multi-cursor/loop if same file)
└── YES → Extract to framework component
         └── Does the component need multiple variants (size, intent, state)?
             ├── NO  → Simple component with inline utilities
             └── YES → Use CVA (Class Variance Authority)
                       └── Does the component accept external className overrides?
                           └── YES → Use cn() = clsx + tailwind-merge
```

The `@apply` directive is only appropriate when you **cannot control the HTML** (third-party output, Markdown, CMS content, legacy backend templates).

---

## Class Variance Authority (CVA)

CVA is the standard tool for building type-safe, multi-variant UI components. Install once, use everywhere:

```bash
npm install class-variance-authority
```

### Anatomy of a CVA Definition

```ts
import { cva, type VariantProps } from "class-variance-authority"

const badge = cva(
  // Base — always applied regardless of variants
  [
    "inline-flex items-center gap-1",
    "rounded-full px-2.5 py-0.5",
    "text-xs font-medium",
    "transition-colors",
  ],
  {
    variants: {
      // Intent defines the color/role
      intent: {
        default:     "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100",
        success:     "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
        warning:     "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
        destructive: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
        brand:       "bg-brand-100 text-brand-800 dark:bg-brand-900 dark:text-brand-100",
      },
      // Removable for icon-only badges
      dot: {
        true:  "before:mr-1 before:h-1.5 before:w-1.5 before:rounded-full before:bg-current",
        false: "",
      },
    },
    // Compound variants — apply only when multiple conditions are true
    compoundVariants: [
      {
        intent: "destructive",
        dot: true,
        class: "before:animate-pulse",
      },
    ],
    defaultVariants: {
      intent: "default",
      dot: false,
    },
  }
)

// TypeScript integration
type BadgeProps = React.HTMLAttributes<HTMLSpanElement> & VariantProps<typeof badge>

export function Badge({ className, intent, dot, ...props }: BadgeProps) {
  return (
    <span className={cn(badge({ intent, dot }), className)} {...props} />
  )
}
```

### CVA Rules

- **Base classes** — use an array for readability when there are many; CVA flattens them automatically
- **Variants** — one key per visual dimension (intent, size, shape, outline, etc.)
- **Compound variants** — style combinations that require both conditions to be true
- **Default variants** — always provide defaults so the component renders correctly without props
- **`className` merging** — always wrap CVA output in `cn()` when the component accepts `className` from consumers

---

## tailwind-merge

`tailwind-merge` resolves Tailwind class conflicts at runtime. The problem it solves:

```ts
// Without tailwind-merge
twJoin("px-2 py-1", "px-4")
// → "px-2 py-1 px-4"  — BOTH px- values exist; browser applies the one later in the stylesheet
//   Result: unpredictable, depends on compiled CSS order

// With tailwind-merge
twMerge("px-2 py-1", "px-4")
// → "py-1 px-4"  — px-2 is correctly removed
```

### Install

```bash
npm install tailwind-merge clsx
```

### When to Use Which Function

| Function | Use case | Cost |
|----------|----------|------|
| `twMerge()` | Merging default styles with consumer `className` overrides | Higher (conflict resolution) |
| `twJoin()` | Conditional joining of internal classes (no override merging needed) | Lower (no conflict resolution) |
| `clsx()` | Conditional class logic (boolean/object/array syntax) | Minimal |
| `cn()` | All-purpose: conditional joining + conflict resolution | Medium |

**Performance rule:** Inside a component, use `twJoin` for internal class assembly and `twMerge` only at the boundary where consumer overrides arrive.

### The `cn()` Utility

Create once in a shared utilities file, import everywhere:

```ts
// lib/utils.ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### Advanced: Configure tailwind-merge with CVA

For design systems where CVA and tailwind-merge work together across many components, configure them once:

```ts
// lib/variants.ts
import { defineConfig } from "class-variance-authority"
import { extendTailwindMerge } from "tailwind-merge"

// Extend tailwind-merge with custom tokens from your @theme
const twMerge = extendTailwindMerge({
  extend: {
    classGroups: {
      "font-size": [
        { text: ["2xs", "3xs"] },  // Custom text sizes from @theme
      ],
    },
  },
})

export const { cva, cx, compose } = defineConfig({
  hooks: {
    onComplete: (className) => twMerge(className),
  },
})
```

This pattern means every CVA component in your codebase automatically gets conflict resolution without manual `cn()` wrapping.

---

## Container Queries

### Basic Usage

```html
<!-- Mark the container boundary -->
<div class="@container">
  <!-- Child responds to parent width, not viewport width -->
  <article class="flex flex-col @sm:flex-row @md:gap-6 @lg:grid @lg:grid-cols-[1fr_2fr]">
    <img class="w-full @sm:w-32 @md:w-48" />
    <div class="@sm:pl-4">...</div>
  </article>
</div>
```

### Container Size Breakpoints

| Variant | Min-width |
|---------|-----------|
| `@xs:` | 320px |
| `@sm:` | 384px |
| `@md:` | 448px |
| `@lg:` | 512px |
| `@xl:` | 576px |
| `@2xl:` | 672px |
| `@3xl:` | 768px |
| `@4xl:` | 896px |
| `@5xl:` | 1024px |
| `@6xl:` | 1152px |
| `@7xl:` | 1280px |

Max-width variants are also supported: `@max-sm:`, `@max-md:`, etc.

### Named Containers (Avoiding Context Clashes)

In deeply nested layouts, a child element might accidentally respond to the wrong ancestor container. Use named containers to be explicit:

```html
<div class="@container/sidebar">
  <div class="@container/card">
    <!-- This targets the /card container, not /sidebar -->
    <div class="@sm/card:text-lg @lg/card:text-2xl">
      Card-responsive text
    </div>

    <!-- This explicitly targets the outer /sidebar container -->
    <div class="@lg/sidebar:hidden">
      Hidden when sidebar is wide
    </div>
  </div>
</div>
```

### Container Queries vs. Viewport Breakpoints

| Use viewport `md:` | Use container `@md:` |
|--------------------|----------------------|
| Page-level layout | Reusable UI component |
| Navigation, sidebars | Card, badge, avatar |
| App shell structure | Form fields |
| Document layout shifts | List items |

**Rule of thumb:** If a component can appear in multiple contexts at different parent widths, use container queries. If you are styling the page frame, use viewport breakpoints.

---

## Responsive Design Patterns

### Mobile-First Class Composition

```tsx
// Card component — builds up from mobile
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

### Conditional State Composition

```tsx
// Using clsx for conditional logic
function Button({ isLoading, isDisabled, variant = "primary" }) {
  return (
    <button
      className={cn(
        button({ intent: variant }),
        // Conditional classes via clsx object syntax
        {
          "opacity-50 cursor-not-allowed": isDisabled,
          "cursor-wait": isLoading,
        }
      )}
      disabled={isDisabled || isLoading}
    >
      {isLoading ? <Spinner /> : children}
    </button>
  )
}
```

---

## Framework-Specific Integration

### Astro

In Astro, Tailwind v4 requires `@tailwindcss/vite`:

```js
// astro.config.mjs
import { defineConfig } from "astro/config"
import tailwindcss from "@tailwindcss/vite"

export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
  },
})
```

CSS entry point:
```css
/* src/styles/global.css */
@import "tailwindcss";

@theme {
  /* tokens */
}
```

Import in layout:
```astro
---
import "../styles/global.css"
---
```

**Scoped Astro styles with Tailwind tokens:**
```astro
<style>
  @reference "../styles/global.css";

  .custom-element {
    color: var(--color-brand-500);
  }
</style>
```

### React / Next.js

```ts
// tailwind.css (entry point)
@import "tailwindcss";
@theme { /* tokens */ }
```

```tsx
// app/layout.tsx
import "./globals.css"  // or wherever your CSS entry point lives
```

The `cn()` utility is standard in Next.js projects — many templates include it in `lib/utils.ts`.

### Vue / Nuxt

In Vue/Nuxt SFCs, use `@reference` to access theme tokens in `<style scoped>` without emitting duplicate CSS:

```vue
<style scoped>
@reference "assets/css/main.css";

.custom-dropdown {
  background-color: var(--color-surface);
  border-color: var(--color-brand-200);
}
</style>
```
