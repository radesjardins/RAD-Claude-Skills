# Zod v4 Breaking Changes: Complete Reference

## Quick Migration Matrix

| Zod 3 | Zod 4 | Action Required |
|---|---|---|
| `SchemaA.merge(SchemaB)` | `.merge()` deprecated | Replace with `.extend()` or shape spread |
| `invalid_type_error`, `required_error` | Unified `error` param | Replace per-field error props |
| `z.setErrorMap()` | `z.config()` | Replace call |
| `error.format()` | `z.treeifyError(error)` | Replace method call |
| `error.flatten()` | `z.flattenError(error)` | Replace method call |
| `schema.deepPartial()` | Removed | Manual nesting |
| `z.nativeEnum(E)` | `z.enum(E)` | Replace function |
| `z.string().email()` | `z.email()` | Replace (old still works but deprecated) |
| `z.string().uuid()` | `z.uuid()` | Replace (old still works but deprecated) |
| `z.string().ip()` | `z.ipv4()` / `z.ipv6()` | Replace with specific version |
| `z.promise()` | Removed | Validate resolved value instead |
| `z.record(z.string())` | `z.record(z.string(), z.unknown())` | Add explicit value schema |
| `.default()` with `.optional()` | Default always applied | Review PATCH schemas |
| `z.coerce.*` input: primitive | Input type: `unknown` | Update TypeScript types |
| Schema-level `errorMap` | Schema-level `error` | Rename property |

## Detailed Change: `.merge()` Deprecation

`.merge()` created ambiguity about which schema's strictness mode (strip/strict/passthrough) won. The new approach is explicit:

```typescript
// Zod 3
const C = A.merge(B); // B's config "wins" in some cases

// Zod 4 — explicit control
// Shape only (inherits A's config):
const C = A.extend(B.shape);
// New object with both shapes (strip mode by default):
const C = z.object({ ...A.shape, ...B.shape });
// Strict combination:
const C = z.strictObject({ ...A.shape, ...B.shape });
```

## Detailed Change: `.default()` Behavior

This is the most dangerous silent change in Zod 4:

```typescript
// Zod 3 behavior:
const S = z.object({ x: z.number().default(0) }).partial();
S.parse({}); // → {} (x not present, undefined stays undefined)
S.parse({ x: undefined }); // → {} (x not present)

// Zod 4 behavior:
const S = z.object({ x: z.number().default(0) }).partial();
S.parse({}); // → { x: 0 } (default applied!)
S.parse({ x: undefined }); // → { x: 0 } (default applied!)
```

Migration path:
1. Audit all schemas with `.default()` used for PATCH/partial update endpoints
2. Create dedicated update schemas without `.default()` values
3. Use `undefined` check in database update logic to skip unset fields

## Detailed Change: Coerce Input Types

```typescript
// Zod 3
type Input3 = z.input<typeof z.coerce.number()>; // number | string | boolean | bigint | null | undefined

// Zod 4
type Input4 = z.input<typeof z.coerce.number()>; // unknown

// Impact: TypeScript code passing typed values to coerce schemas may show errors
function processAge(age: string) {
  return z.coerce.number().parse(age); // Fine in both versions
}

// But:
const AgeInput: z.input<typeof z.coerce.number()> = "25";
// Zod 3: string assignable to inferred type ✓
// Zod 4: string NOT assignable to unknown directly (need explicit widening)
```

## Detailed Change: String Format Validators

The old method chains are deprecated (still work as aliases, will be removed in a future version):

```typescript
// All deprecated in Zod 4 (still functional until removal):
z.string().email()
z.string().uuid()
z.string().url()
z.string().cuid()
z.string().cuid2()
z.string().ulid()
z.string().nanoid()
z.string().ip()
z.string().cidr()
z.string().base64()
z.string().base64url()
z.string().jwt()
z.string().datetime()
z.string().date()
z.string().time()
z.string().duration()

// Zod 4 top-level (tree-shakable):
z.email()
z.uuid()
z.url()
z.cuid()
z.cuid2()
z.ulid()
z.nanoid()
z.ipv4()
z.ipv6()
z.cidr()
z.base64()
z.base64url()
z.jwt()
z.iso.datetime()
z.iso.date()
z.iso.time()
z.iso.duration()
```

**UUID strictness change:** `z.uuid()` in Zod 4 validates UUID format more strictly than `z.string().uuid()` in Zod 3. Some non-standard UUID strings that passed in Zod 3 may fail in Zod 4.

## Detailed Change: `.pipe()` Type Strictness

Zod 4 fixed type unsoundness in `.pipe()`. The output type of the left schema must be assignable to the input type of the right schema:

```typescript
// May error in Zod 4 where it worked in Zod 3:
const S = z.string()
  .transform(s => parseInt(s))  // Output: number
  .pipe(z.string());             // Input: string ← TypeScript error

// Fix: Ensure type alignment
const S = z.string()
  .pipe(z.coerce.number());     // coerce accepts unknown → no mismatch

// Or: return unknown from transform to satisfy any pipe input
const S = z.string()
  .transform((s): unknown => parseInt(s))
  .pipe(z.number());
```

## New `z.check()` vs `.refine()`

Zod 4 adds `.check()` as a more flexible alternative to `.refine()`. The difference: `.check()` can return `void` (pass) or call `ctx.issue()` to add custom issues:

```typescript
// .refine() — returns boolean or string
const S = z.string().refine(
  s => /^\d{5}$/.test(s),
  "Must be a 5-digit ZIP code"
);

// .check() — explicit issue creation for multiple errors or custom codes
const S = z.string().check((ctx) => {
  if (!/^\d{5}(-\d{4})?$/.test(ctx.value)) {
    ctx.issue({ code: "custom", message: "Invalid ZIP format" });
  }
  if (ctx.value.startsWith("000")) {
    ctx.issue({ code: "custom", message: "ZIP cannot start with 000" });
  }
  // Multiple issues can be added
});
```
