# ZodMini: Lightweight Validation for Bundle-Sensitive Environments

## What is ZodMini?

`@zod/mini` is a functional variant of Zod 4 that trades method chaining for standalone wrapper functions. The result is a ~2KB gzipped bundle (vs ~13KB for full Zod).

## When to Use ZodMini

**Use ZodMini when:**
- Building an npm package or SDK that will be consumed by others (don't bloat your users' bundles)
- Deploying to Cloudflare Workers, Vercel Edge, Deno Deploy, or AWS Lambda@Edge where cold start time is critical
- Building a frontend form library where Zod is one of many dependencies
- Bundle analysis shows Zod contributing a meaningful percentage of total bundle size

**Use full Zod when:**
- Running on Node.js backend (13KB adds <1ms to lambda cold starts)
- Developer experience matters (method chaining is more ergonomic)
- Using `.transform()`, `.pipe()`, or `.brand()` (not available in ZodMini)
- Using registries, `.meta()`, or `z.toJSONSchema()`

## API Comparison

ZodMini uses standalone wrapper functions instead of method chaining:

```typescript
// Full Zod — method chaining
import { z } from "zod";
const UserSchema = z.object({
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).optional(),
  email: z.email(),
});

// ZodMini — wrapper functions
import { z, string, number, object, email, optional, minLength, maxLength } from "@zod/mini";
const UserSchema = object({
  name: pipe(string(), minLength(1), maxLength(100)),
  age: optional(pipe(number(), int(), minimum(0))),
  email: email(),
});
```

## ZodMini Available Primitives

```typescript
import {
  // Types
  string, number, boolean, bigint, symbol, date, undefined, null, any, unknown, never, void,
  // Collections
  array, object, tuple, record, map, set,
  // Format validators
  email, uuid, url, ipv4, ipv6, base64, cuid, cuid2, ulid, nanoid,
  // ISO
  iso, // iso.date(), iso.datetime(), iso.time(), iso.duration()
  // Logic
  union, intersection, discriminatedUnion, literal, enum,
  // Modifiers
  optional, nullable, nullish,
  // Utilities
  pipe, preprocess, catch,
  // Coerce
  coerce, // coerce.string(), coerce.number(), etc.
  // Parsing
  parse, safeParse, parseAsync, safeParseAsync,
  // Errors
  z, // z.treeifyError, z.flattenError, z.prettifyError
} from "@zod/mini";
```

## What ZodMini Does NOT Have

| Full Zod Feature | ZodMini Alternative |
|---|---|
| `.transform()` | Not available — use `z.preprocess()` for simple coercions |
| `.brand()` | Not available |
| `.meta()` / registries | Not available |
| `z.toJSONSchema()` | Not available |
| `.safeExtend()` | Not available |
| `.check()` | `.refine()` is available |
| Method chaining on schemas | Use wrapper functions: `pipe(schema, modifier)` |

## Migrating a Specific Schema from Full Zod to ZodMini

```typescript
// Full Zod
const ProductSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(100),
  price: z.number().positive().finite(),
  category: z.enum(["electronics", "clothing", "food"]),
  tags: z.array(z.string()).default([]),
  metadata: z.record(z.string(), z.unknown()).optional(),
});

// ZodMini equivalent
import { object, string, number, array, record, enum as zenum, optional, pipe, uuid, minimum, maximum, finite } from "@zod/mini";

const ProductSchema = object({
  id: uuid(),
  name: pipe(string(), minLength(1), maxLength(100)),
  price: pipe(number(), gt(0), finite()),
  category: zenum(["electronics", "clothing", "food"]),
  tags: optional(array(string())), // No .default() in ZodMini
  metadata: optional(record(string(), unknown())),
});
```

## Bundle Size Impact

| Scenario | Full Zod | ZodMini | Saving |
|---|---|---|---|
| Core bundle (gzip) | ~13KB | ~2KB | 11KB |
| With tree-shaking (typical app) | ~8-10KB | ~1-3KB | 7-8KB |
| Lambda cold start impact | <1ms | <0.1ms | Negligible in practice |

For most Node.js backends, the difference is not noticeable. For frontend SDKs published to npm, the ~11KB saving is meaningful to your users.
