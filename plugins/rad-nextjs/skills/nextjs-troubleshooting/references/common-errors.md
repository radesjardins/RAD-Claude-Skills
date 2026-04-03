# Next.js Additional Errors: Quick Reference

Supplementary error lookup table. For the most common issues (hydration, serialization, caching, waterfalls, memory), see the main SKILL.md. This file covers additional errors not addressed there.

---

## Build & Module Errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `Dynamic server usage: headers/cookies` | Accessing runtime APIs in a statically generated route | Wrap in `<Suspense>`, use `export const dynamic = 'force-dynamic'` |
| `Module not found: Can't resolve 'fs'` | Server-only module imported in Client Component | Add `import 'server-only'` to the module, or move import to Server Component |
| `You're importing a component that needs X` (useState, useEffect) | Server Component using client-only hooks | Add `'use client'` directive to the component file |
| `Attempted import error: 'X' is not exported from 'Y'` | Named export doesn't exist or barrel file issue | Check export name, import directly from source file instead of barrel |

---

## Runtime Errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `Unhandled Runtime Error: Error: Unauthorized` | Auth check failed in Server Action or DAL | Verify session cookie is set, check auth middleware, ensure tokens aren't expired |
| `Error: NEXT_NOT_FOUND` | `notFound()` called or page doesn't exist | Check route file exists, verify dynamic params, check `not-found.tsx` |
| `Error: cookies/headers was called outside a request scope` | Accessing request-scoped APIs outside of a request | Move to a Route Handler, Server Action, or Server Component (not module scope) |

---

## Caching & Configuration

| Error Message / Symptom | Cause | Fix |
|--------------------------|-------|-----|
| ISR page not regenerating | `revalidate` value too long or tag not matched | Check `revalidateTag` matches, verify revalidation interval |
| `"use cache"` not working | Feature not enabled | Enable in `next.config.ts`: `experimental: { dynamicIO: true }` |
| `Invalid environment variables` | Env validation failing at startup | Check `instrumentation.ts` or Zod env schema, verify all vars are set |

---

## Middleware & Routing

| Error Message / Symptom | Cause | Fix |
|--------------------------|-------|-----|
| Middleware not running on expected routes | Incorrect `matcher` config | Check `config.matcher` in `middleware.ts`, verify patterns match routes |
| Infinite redirect loop | Middleware redirect targeting a route that also triggers middleware | Add the redirect target to `matcher` exclusions |
| `proxy.ts` not recognized | Using Next.js 16 renamed file | Rename `middleware.ts` → `proxy.ts` (Next.js 16+) |

---

## Performance Symptoms

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| High CLS score | Images/fonts shifting layout on load | Set `width`/`height` on images, use `next/font` |
| Slow interactions (INP > 200ms) | Long tasks blocking main thread | Use `scheduler.yield()`, move logic to Server Components |

---

## TypeScript Errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `Type 'Promise<Element>' is not assignable to type 'ReactNode'` | Async Server Component in a context expecting sync ReactNode | Ensure parent supports async children, or wrap in Suspense |
| `Property 'params' does not exist` | Missing type annotation for page props | Use `{ params: { slug: string } }` or generate types |
| `Argument of type 'FormData' is not assignable` | Server Action receiving raw FormData | Use `formData.get()` to extract values, then validate with Zod |
