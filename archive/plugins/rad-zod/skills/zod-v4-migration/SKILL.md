---
name: Zod v4 Migration and New APIs
description: This skill should be used when the user asks about "Zod 4", "Zod v4", "upgrading to Zod 4", "Zod 4 breaking changes", "Zod 4 migration", "z.merge deprecated", "Zod 4 error parameter", "z.config", "Zod registries", "z.meta", "ZodMini", "z.file", "z.templateLiteral", "z.toJSONSchema", "Zod 4 vs Zod 3", "Zod 4 optional default behavior", or "Zod 4 performance". Covers Zod v4 architecture, all breaking changes, new APIs, and migration strategies.
version: 1.0.0
---

# Zod v4 Migration and New APIs

Zod 4 is a **ground-up rewrite** focused on TypeScript compiler performance, bundle size, and tree-shaking. The core API surface is 95% backward-compatible, but several specific behaviors changed in ways that cause silent bugs if not addressed.

## Performance Improvements at a Glance

| Metric | Improvement |
|---|---|
| String parsing speed | ~14x faster than Zod 3 |
| Array parsing speed | ~7x faster |
| Object parsing speed | ~6.5x faster |
| TypeScript type instantiations | ~100x fewer (minutes off build times in monorepos) |
| Bundle size (full Zod) | ~13KB gzipped |
| Bundle size (ZodMini) | ~2KB gzipped |

## Breaking Changes Requiring Code Changes

### 1. `.merge()` Deprecated

Replace all `.merge()` calls with `.extend()` or shape destructuring:

```typescript
// Before (Zod 3)
const Combined = SchemaA.merge(SchemaB);

// After (Zod 4) — preferred for performance
const Combined = z.object({ ...SchemaA.shape, ...SchemaB.shape });
// Or
const Combined = SchemaA.extend(SchemaB.shape);
```

### 2. Unified `error` Parameter

All per-schema error configuration is now via a single `error` parameter:

```typescript
// Before (Zod 3 — deprecated in Zod 4)
z.string({ invalid_type_error: "Not a string", required_error: "Required" })
z.string().min(3, { message: "Too short" })

// After (Zod 4)
z.string({ error: (issue) => issue.input === undefined ? "Required" : "Must be text" })
z.string().min(3, { error: "Must be at least 3 characters" })
```

### 3. `.default()` Behavior Change — **Causes Silent Data Loss**

In Zod 4, `.default()` is applied **unconditionally when input is undefined**, even when wrapped in `.optional()` or `.partial()`. This breaks PATCH endpoint patterns:

```typescript
// Before (Zod 3): partial() with defaults would not apply defaults for missing fields
// After (Zod 4): partial() + default = default ALWAYS applied when field is missing

const Schema = z.object({ status: z.string().default("active") });
Schema.partial().parse({});
// Zod 3: {} (field omitted, stays undefined)
// Zod 4: { status: "active" } (default applied!) ← DATA LOSS RISK on PATCH
```

Fix: Create dedicated PATCH schemas without `.default()` values.

### 4. `.deepPartial()` Removed

Use manual nested `.partial()` calls instead:

```typescript
// Before: schema.deepPartial()
// After: manually apply .partial() at each level
const DeepPartial = z.object({
  user: z.object({ name: z.string(), address: z.object({ zip: z.string() }) })
    .partial()
    .extend({ address: z.object({ zip: z.string() }).partial() }),
});
```

### 5. `z.coerce.*` Input Types Now `unknown`

All coerce schemas now accept `unknown` input (was the target primitive type in Zod 3):

```typescript
// Zod 3: z.coerce.number() had input type "number | string | boolean | ..."
// Zod 4: z.coerce.number() has input type "unknown"

// Code that typed raw inputs as the coerced type will have TypeScript errors
```

### 6. Top-Level String Validators

String format validators are now top-level functions for tree-shaking:

```typescript
// Before (Zod 3 — deprecated chains)
z.string().email()
z.string().uuid()
z.string().url()
z.string().ip()

// After (Zod 4 — top-level, tree-shakable)
z.email()
z.uuid()
z.url()
z.ipv4()
z.ipv6()
z.iso.date()
z.iso.datetime()
```

The old chains still work as aliases but are deprecated and will be removed.

### 7. Error Formatting Methods Deprecated

```typescript
// Deprecated instance methods (Zod 3)
error.format()
error.flatten()

// Replacement top-level functions (Zod 4)
z.treeifyError(error)
z.flattenError(error)
z.prettifyError(error)
```

### 8. `z.nativeEnum()` Deprecated

`z.enum()` now handles native TypeScript enums directly:

```typescript
enum Direction { Up, Down, Left, Right }

// Before (Zod 3)
z.nativeEnum(Direction)

// After (Zod 4)
z.enum(Direction)
```

### 9. Other Removed APIs

- `z.promise()` — removed; validate the resolved value instead
- Single-argument `z.record()` — now requires explicit key and value schemas: `z.record(z.string(), z.number())`

## New APIs

### `z.config()` — Global Configuration

Replaces `z.setErrorMap()`. Set at application startup:

```typescript
import { z } from "zod";
import { en } from "zod/locales/en";

z.config(en()); // Load locale
z.config({ customError: (issue) => customErrorFn(issue) }); // Custom error handler
```

### Registries and `.meta()` — Schema Metadata

Attach metadata (id, title, description, examples) to schemas without affecting validation:

```typescript
const EmailSchema = z.email().meta({
  id: "email-field",
  title: "Email Address",
  description: "User's primary email",
  examples: ["user@example.com"],
});

// Generate JSON Schema (for OpenAPI, form generation, etc.)
const jsonSchema = z.toJSONSchema(EmailSchema);
```

**Monorepo warning:** Schema IDs must be globally unique. Using `.meta({ id })` on schemas defined inside dynamically called functions causes "ID already exists in registry" errors. Only apply `.meta({ id })` to module-level schema constants.

### `@zod/mini` — Lightweight Variant

A functional, ~2KB alternative to full Zod for bundle-sensitive environments:

```typescript
import { z } from "@zod/mini";
// Uses standalone functions instead of method chaining
import { parse, optional, string, object } from "@zod/mini";
```

Use for: Edge functions, serverless, frontend bundles where Zod adds meaningful size.
Use full Zod for: Node.js backends, apps where DX matters more than ~11KB.

### `z.file()` — File Validation

Purpose-built schema for browser `File` instances (replaces `z.instanceof(File)` patterns):

```typescript
const AvatarSchema = z.file()
  .min(1)             // minimum bytes
  .max(5 * 1024 * 1024)  // 5MB maximum
  .type("image/jpeg", "image/png", "image/webp");
```

### `z.templateLiteral()` — Structured String Patterns

```typescript
const SemVerSchema = z.templateLiteral(["v", z.number(), ".", z.number(), ".", z.number()]);
// Matches: "v1.2.3", "v0.0.1"

const CssColorSchema = z.templateLiteral(["#", z.string().length(6)]);
```

### `z.toJSONSchema()` — Native JSON Schema Export

```typescript
const jsonSchema = z.toJSONSchema(UserSchema);
// Returns valid JSON Schema for use with OpenAPI, form libraries, etc.
```

## Additional Resources

- **`references/breaking-changes.md`** — Complete breaking changes with before/after code for each
- **`references/new-apis.md`** — Full reference for all new Zod 4 APIs with usage examples
- **`references/zod-mini.md`** — When to use ZodMini, full API comparison, migration from full Zod
