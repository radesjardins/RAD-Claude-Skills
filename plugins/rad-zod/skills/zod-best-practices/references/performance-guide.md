# Zod Performance Guide

## Schema Hoisting: The Most Important Optimization

Zod schema construction is not free. Each `z.object()`, `z.array()`, `z.union()`, etc. call allocates validator objects. Inside a frequently-called function, this happens on every invocation.

```typescript
// BAD: ~1000 requests/sec → 1000 z.object() instantiations/sec
export async function POST(req: Request) {
  const BodySchema = z.object({
    title: z.string().min(1),
    tags: z.array(z.string()),
  });
  const body = BodySchema.parse(await req.json());
}

// GOOD: Schema instantiated once at module load
const PostBodySchema = z.object({
  title: z.string().min(1),
  tags: z.array(z.string()),
});

export async function POST(req: Request) {
  const body = PostBodySchema.parse(await req.json());
}
```

The improvement compounds with schema complexity — nested objects, unions, and refinements all add construction cost.

## `.safeParse()` in Hot Paths

Exception throwing/catching in JavaScript involves stack unwinding, which is expensive. In code paths where validation failure is expected (user input, webhooks, API responses), use `.safeParse()`:

```typescript
// Expensive in hot paths: stack trace generated on every failure
try {
  const data = Schema.parse(input);
} catch (e) { /* ... */ }

// Efficient: no exception overhead
const result = Schema.safeParse(input);
if (!result.success) { /* ... */ }
```

Benchmark impact: In a tight loop processing 100k items, switching to `.safeParse()` can reduce validation overhead by 30-60% when the failure rate is non-trivial.

## Discriminated Unions vs Regular Unions

`z.union()` tests each option sequentially until one passes. For large unions (5+ options), this is O(n) per parse.

`z.discriminatedUnion()` reads the discriminator key, looks up the matching schema in an O(1) map, and parses only that option:

```typescript
// O(n) — tests all 5 options in worst case
const EventSchema = z.union([
  z.object({ type: z.literal("click"), x: z.number() }),
  z.object({ type: z.literal("hover"), element: z.string() }),
  z.object({ type: z.literal("scroll"), delta: z.number() }),
  z.object({ type: z.literal("keydown"), key: z.string() }),
  z.object({ type: z.literal("resize"), width: z.number() }),
]);

// O(1) — jumps directly to matching option
const EventSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("click"), x: z.number() }),
  z.object({ type: z.literal("hover"), element: z.string() }),
  z.object({ type: z.literal("scroll"), delta: z.number() }),
  z.object({ type: z.literal("keydown"), key: z.string() }),
  z.object({ type: z.literal("resize"), width: z.number() }),
]);
```

## Lazy Schemas and Infinite Loop Risk

`z.lazy()` defers schema creation until first use — necessary for recursive types, but carries a risk: **passing cyclical objects to a recursive Zod schema causes an infinite loop with no stack overflow protection.**

```typescript
// Always validate that recursive data is acyclic before parsing
const CategorySchema: z.ZodType<Category> = z.lazy(() =>
  z.object({
    name: z.string(),
    children: z.array(CategorySchema),
  })
);

// DANGER: Will hang the process indefinitely
const circular: any = { name: "root", children: [] };
circular.children.push(circular);
CategorySchema.parse(circular); // Infinite loop ☠️
```

For deeply nested but non-cyclical data, lazy schemas perform well. For potentially cyclical data (graphs, linked lists), add a depth limit via `.refine()`.

## ZodMini: When Bundle Size Matters

Full Zod 4 is ~13KB gzipped. `@zod/mini` is ~2KB — a functional variant that trades method chaining for tree-shakable standalone functions.

Use ZodMini when:
- Deploying to Cloudflare Workers, Vercel Edge, or Deno Deploy where cold starts matter
- Building a frontend form library or SDK where users will install your package
- Bundle analysis shows Zod contributing >1% of total bundle

Use full Zod when:
- Running on Node.js (cold starts < 1ms for 13KB)
- Developer ergonomics matter more than bundle size
- Using `.transform()`, `.pipe()`, `.brand()`, or registry features (not in ZodMini)

## TypeScript Compiler Performance

Zod 4 reduces TypeScript type instantiations by ~100x compared to Zod 3 through simplified internal generics. However, deeply chained schemas still have compile-time cost:

```typescript
// Expensive to type-check: long method chains
const S = z.object({ a: z.string() })
  .extend({ b: z.number() })
  .extend({ c: z.boolean() })
  .extend({ d: z.date() });

// Cheaper: single object with all fields
const S = z.object({ a: z.string(), b: z.number(), c: z.boolean(), d: z.date() });
```

For large monorepos, prefer flat schema definitions over deep chains of `.extend()` calls.
