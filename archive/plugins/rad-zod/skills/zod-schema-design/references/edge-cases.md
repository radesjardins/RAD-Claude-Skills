# Zod Edge Cases and Exceptions

## The `.pipe()` Strictness Change in Zod 4

Zod 4 made `.pipe()` significantly stricter to fix type unsoundness. The output type of the first schema must be assignable to the input type of the second.

```typescript
// This TypeScript error is expected in Zod 4 — the pipe types don't align
const S = z.string()
  .transform(s => ({ value: s }))  // Output: { value: string }
  .pipe(z.object({ value: z.number() })); // Input expects { value: number } ← mismatch

// Fix option 1: Return unknown from transform to satisfy any pipe input
const S = z.string()
  .transform((s): unknown => ({ value: s }))
  .pipe(z.object({ value: z.string() }));

// Fix option 2: Use .transform() after the object schema
const S = z.object({ value: z.string() })
  .transform(d => d.value.length);
```

When pipe errors are confusing, check that the transform's return type matches the next schema's input type. Returning `unknown` from the transform is a valid workaround that satisfies the type checker without losing safety.

## Refinements Lost After `.omit()` / `.pick()` / `.partial()`

**As of Zod 4.3, this throws an error** (previously silently dropped refinements):

```typescript
const ValidatedSchema = z.object({
  email: z.email(),
  age: z.number(),
}).refine(d => d.age >= 18, "Must be adult");

ValidatedSchema.omit({ age: true }); // ❌ Throws in Zod 4.3+

// Fix: Extract refinement logic, apply after structural modification
const BaseSchema = z.object({ email: z.email(), age: z.number() });
const AdultSchema = BaseSchema.refine(d => d.age >= 18, "Must be adult");
const PublicSchema = BaseSchema.omit({ age: true }); // ✅ No refinement to lose
```

## Transform Runs After Failed Refinement

```typescript
// Dangerous pattern: transform assumes data is valid from refine
const SafeJsonSchema = z.string()
  .refine(s => {
    try { JSON.parse(s); return true; }
    catch { return false; }
  }, "Invalid JSON")
  .transform(s => JSON.parse(s)); // Runs even if refine fails → SyntaxError

// The fix: abort: true
const SafeJsonSchema = z.string()
  .refine(s => {
    try { JSON.parse(s); return true; }
    catch { return false; }
  }, { message: "Invalid JSON", abort: true }) // ← abort: true
  .transform(s => JSON.parse(s)); // Only runs when refine passes
```

## TypeScript Cannot Infer Recursive Types

TypeScript's type inference fails on self-referential schemas. Always define the type manually:

```typescript
// TypeScript cannot infer this — will produce "any" or error
const TreeNode = z.lazy(() => z.object({
  value: z.number(),
  children: z.array(TreeNode), // Can't infer the type of TreeNode
}));

// Correct: explicit type annotation
type TreeNode = {
  value: number;
  children: TreeNode[];
};

const TreeNodeSchema: z.ZodType<TreeNode> = z.lazy(() =>
  z.object({
    value: z.number(),
    children: z.array(TreeNodeSchema),
  })
);
```

## Branded Types Have No Runtime Effect

A common misconception: branded types modify the runtime value. They don't:

```typescript
const UserIdSchema = z.string().uuid().brand("UserId");

const id = UserIdSchema.parse("123e4567-e89b-12d3-a456-426614174000");
// id at runtime: "123e4567-e89b-12d3-a456-426614174000" (just a string)
// id TypeScript type: string & { readonly [brand]: "UserId" }

// The brand is ONLY a compile-time marker
// Runtime: typeof id === "string" (not a special type)
```

Use branded types for compile-time protection against misuse, not runtime enforcement.

## `.safeExtend()` for Extending Refined Schemas

`.extend()` throws on refined schemas. Use `.safeExtend()`:

```typescript
const BaseSchema = z.object({ name: z.string() })
  .refine(d => d.name.length > 0, "Name required");

BaseSchema.extend({ age: z.number() }); // ❌ Throws

BaseSchema.safeExtend({ age: z.number() }); // ✅
// safeExtend also prevents overwriting existing fields with incompatible types
```

## `z.intersection()` Limitations

Intersections work well for combining object schemas but have edge cases:

```typescript
// Works fine: two compatible object schemas
const A = z.object({ name: z.string() });
const B = z.object({ age: z.number() });
const AB = z.intersection(A, B); // ✅ { name: string; age: number }

// Problematic: intersecting schemas with conflicting transforms
const C = z.object({ x: z.string() }).transform(d => ({ x: d.x.length }));
const D = z.object({ y: z.number() });
const CD = z.intersection(C, D);
// Both schemas parse independently — transforms may not compose as expected
// Prefer manual schema design when transforms are involved
```

## `z.enum()` vs Native TypeScript Enums

Zod 4 unifies these — `z.enum()` accepts both string literal arrays and TypeScript native enums:

```typescript
// String literal enum (preferred)
const StatusSchema = z.enum(["pending", "active", "inactive"]);
type Status = z.infer<typeof StatusSchema>; // "pending" | "active" | "inactive"

// Native TypeScript enum (supported in Zod 4)
enum Direction { Up = "UP", Down = "DOWN" }
const DirectionSchema = z.enum(Direction); // z.nativeEnum() is deprecated
```

## Optional vs Nullable vs Nullish

These three are commonly confused:

```typescript
z.string().optional()  // string | undefined — field can be absent
z.string().nullable()  // string | null — field present but null
z.string().nullish()   // string | null | undefined — either absent or null

// In objects:
z.object({ field: z.string().optional() })  // { field?: string }
z.object({ field: z.string().nullable() })  // { field: string | null }
```

The JSON distinction: `null` is a valid JSON value. `undefined` means the key is missing. Use `.nullable()` for fields that exist in the JSON payload but have no value. Use `.optional()` for fields that may not be present in the payload at all.

## Default Value Type Constraints

```typescript
// .default() — value must be output type (bypasses parsing)
const S1 = z.string().toLowerCase().default("HELLO");
// default "HELLO" is NOT lowercased — parsing is skipped entirely
// Result: "HELLO" (not "hello") ← Surprising!

// .prefault() — value must be input type (goes through pipeline)
const S2 = z.string().toLowerCase().prefault("HELLO");
// prefault "HELLO" runs through toLowerCase()
// Result: "hello" ← Expected behavior
```

When the default value needs transformation, use `.prefault()`. When the default is already in the final form, use `.default()`.
