---
name: nextjs-best-practices
description: >
  Next.js best practices, App Router, Server/Client Components, RSC, data fetching, caching,
  "use cache", ISR, revalidation, next/image, next/font, next/script, PPR, Suspense, route
  groups, nested layouts, Turbopack, Core Web Vitals, next.config.ts — any Next.js 14/15/16
  App Router work.
---

# Next.js App Router: Coding Standards & Best Practices

Comprehensive reference for building Next.js applications with the App Router. Apply these standards whenever writing or reviewing Next.js code. Security-specific patterns are in the `nextjs-security` skill; testing in `nextjs-testing`; debugging in `nextjs-troubleshooting`.

## Core Philosophy

> **Server First**: Default every component to a React Server Component. Only opt into `'use client'` at leaf components that strictly require state, effects, or browser APIs. This minimizes the JavaScript shipped to the browser.

---

## 1. Project Structure

```
app/
  layout.tsx              # Root layout (replaces _app and _document)
  page.tsx                # Home route
  error.tsx               # Error boundary for this segment
  not-found.tsx           # 404 handling
  (marketing)/            # Route Group — no URL impact
    about/page.tsx
  (shop)/
    products/page.tsx
  api/                    # Route Handlers
lib/
  dal.ts                  # Data Access Layer (server-only)
  auth.ts                 # Authentication utilities
components/
  ui/                     # Client Components (interactive leaf nodes)
  server/                 # Server Components (data-fetching wrappers)
```

### Rules

- Use **Route Groups** `(name)` to organize routes without affecting URLs. Effective for separate layouts or logical grouping (e.g., `(auth)`, `(dashboard)`).
- For large apps, adopt a **monorepo** strategy (Turborepo) for shared components.
- Place all database queries and external API calls in a dedicated **Data Access Layer** (`lib/dal.ts`) marked with `import 'server-only'`.

---

## 2. Server vs. Client Component Boundaries

**Server Components (default)** — execute on the server, ship zero JS to the browser. Use for data fetching, backend logic, and static UI.

**Client Components** (`'use client'`) — required only for `useState`, `useEffect`, event handlers, or browser APIs (`localStorage`, `window`).

### The Composition Pattern

A Server Component **cannot** be imported into a Client Component. Instead, pass it as a `children` prop from a parent Server Component. React resolves the server code first, then passes the serialized RSC Payload to the client. See `references/server-client-patterns.md` for complete code examples.

### Boundary Rules

- Mark modules with sensitive logic using `import 'server-only'` — build fails if accidentally imported client-side.
- Props crossing the boundary must be **serializable** (no `Date`, `Map`, `Set`, or functions).
- Push `'use client'` to the deepest leaf possible to minimize the client bundle.

---

## 3. Data Fetching Patterns

### Server Components

Fetch data directly with `async/await` in Server Components — no `useEffect` or client-side libraries needed. See `references/server-client-patterns.md` for complete data fetching and streaming examples.

### Critical Patterns

- **Data Access Layer (DAL):** Centralize all queries in a server-only module. Perform authorization checks and return minimal DTOs, never raw database records.
- **Parallel Fetching:** Use `Promise.all()` or `Promise.allSettled()` for independent requests. Sequential `await` statements create waterfalls.
- **Request Deduplication:** Wrap DAL functions with `React.cache()` so multiple components requesting the same data in one render only trigger one query.
- **Streaming with Suspense:** Wrap async components in `<Suspense fallback={<Skeleton />}>` to stream content progressively.

### Server Actions

Server Actions are public POST endpoints — always treat input as hostile:
- Validate all input with Zod or Valibot using `safeParse()`.
- Re-verify authentication and authorization inside every action (never rely solely on middleware).
- Use `revalidatePath()` or `revalidateTag()` after successful mutations.
- Native `<form action={serverAction}>` works even before client JS loads.

See `references/server-client-patterns.md` for complete Server Action patterns with form submission and streaming examples.

### Anti-Patterns

- Avoid placing sequential `await` calls that don't depend on each other — use `Promise.all()` instead.
- Avoid accessing `cookies()`, `headers()`, or `searchParams` outside a `<Suspense>` boundary — doing so forces the entire route dynamic.
- Never perform mutations (database writes, cookie setting) during component rendering — use Server Actions or Route Handlers.

---

## 4. Caching & Revalidation

### Next.js 15+ Defaults

`fetch` requests, GET Route Handlers, and the Client Router Cache are **uncached by default**. Opt into caching explicitly.

### Caching Patterns

- **`"use cache"` directive (Next.js 16):** Apply at the function, component, or page level for explicit caching. The compiler generates cache keys automatically.
- **On-demand revalidation:** After mutations, call `revalidatePath('/path')` or `revalidateTag('tag')` inside Server Actions.
- **ISR (time-based):** Configure expiration for content that changes periodically (product catalogs, blog posts). Serves cached content while regenerating in the background.
- **Streaming Promises to Client:** Pass an unresolved Promise as a prop and unwrap with React `use()` inside a `<Suspense>` boundary.

---

## 5. Performance Optimization

See `references/performance-checklist.md` for the complete CWV optimization reference.

**Key rules:**
- **LCP:** `priority` prop on above-the-fold `next/image`. Never lazy-load the LCP image.
- **CLS:** Always set `width`/`height` on images. Use `transform` for animations, not `top`/`margin`.
- **INP:** Break long tasks with `scheduler.yield()`. Move logic to Server Components.
- **Assets:** `next/image` for all images, `next/font` for self-hosted fonts, `next/script` with `lazyOnload`, `next/dynamic` for heavy below-fold components.
- **PPR:** Wrap dynamic components in `<Suspense>` to serve static shell instantly while streaming dynamic content.

---

## 6. Layout & Error Handling Patterns

### Layouts

- `layout.tsx` shares UI across sibling routes and **preserves state** on navigation (does not re-render).
- Root layout replaces legacy `_app` and `_document` — customize `<html>` and `<body>` here.
- **Do not place auth checks in layouts** — they won't re-run on sibling navigation. Put auth in `page.tsx` or the DAL.

### Error Handling

- `error.tsx` creates an isolated React Error Boundary for its child segment.
- `error.tsx` does **not** catch errors in its sibling `layout.tsx` — only in the layout's children.
- Use `not-found.tsx` for graceful 404 handling.

---

## 7. Middleware & Deployment

### Middleware (proxy.ts in Next.js 16)

Use for edge-level routing: redirects, header injection (CSP, HSTS), A/B testing, geo-routing. **Never rely on middleware as the sole security boundary** — always re-verify auth in Route Handlers and Server Actions.

### Production Checklist

1. Run `npm run build && npm run start` locally before deploying.
2. Audit bundle sizes with `@next/bundle-analyzer`.
3. Verify all images use `next/image`, fonts use `next/font`, scripts use `next/script`.
4. Confirm security headers are applied (see `nextjs-security` skill).
5. Set up monitoring with `instrumentation.ts` (OpenTelemetry, Sentry, Datadog).
6. Track Core Web Vitals with Real User Monitoring (Vercel Analytics or equivalent).

### Turbopack

The Rust-based Turbopack compiler is stable in Next.js 15+ for dev and production. Delivers up to 10x faster HMR and 2-5x faster builds.

---

## Additional Resources

### Reference Files

For detailed patterns and code examples, consult:
- **`references/server-client-patterns.md`** — Server/Client component boundary patterns, composition examples, and data fetching code
- **`references/performance-checklist.md`** — Complete Core Web Vitals optimization reference with specific metrics and techniques

### Related Skills

- **`nextjs-security`** — Authentication, API protection, CSP, CSRF, XSS, environment variables
- **`nextjs-testing`** — Vitest, Cypress, Playwright setup and patterns
- **`nextjs-troubleshooting`** — Common bugs, error diagnosis, debugging patterns
