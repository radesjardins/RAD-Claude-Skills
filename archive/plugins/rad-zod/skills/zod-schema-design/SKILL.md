---
name: Zod Schema Design
description: This skill should be used when the user asks about "composing Zod schemas", "extending a schema", "Zod pick omit partial", "discriminatedUnion vs union", "Zod transforms", "Zod refinements", "z.refine vs z.check", "Zod pipe", "input output types", "z.infer input output", "Zod branded types", "recursive schemas", "Zod lazy", or is designing data models with Zod schemas. Provides comprehensive patterns for schema composition, transformation, and refinement.
version: 1.0.0
---

# Zod Schema Design

## Schema Composition: The Hard Rules

### Prefer `.extend()` and Destructuring over `.merge()`

`.merge()` is **deprecated in Zod 4**. The preferred approaches, in order of TypeScript performance:

```typescript
// BEST: Language-level destructuring (optimal TypeScript performance)
const ExtendedSchema = z.object({ ...BaseSchema.shape, extra: z.string() });

// GOOD: .extend() (preferred over merge)
const ExtendedSchema = BaseSchema.extend({ extra: z.string() });

// DEPRECATED: .merge() — do not use in Zod 4
const ExtendedSchema = BaseSchema.merge(OtherSchema); // ❌
```

Prefer destructuring via `.shape` for deeply composed schemas in large monorepos — it yields a measurable reduction in TypeScript compiler instantiations.

### Refinements Lock Structural Methods

Once `.refine()` or `.check()` is applied to a schema, **structural modification methods are blocked**:

```typescript
const RefinedUser = z.object({ age: z.number() }).refine(u => u.age >= 0);

// As of Zod 4.3, these throw an error:
RefinedUser.pick({ age: true });   // ❌ Throws
RefinedUser.omit({ age: true });   // ❌ Throws
RefinedUser.partial();             // ❌ Throws

// Fix: extract refinement, apply to derived schema
const BaseUser = z.object({ age: z.number() });
const PartialUser = BaseUser.partial().refine(u => u.age === undefined || u.age >= 0);
```

Similarly, use `.safeExtend()` (not `.extend()`) when extending a refined schema:

```typescript
const Extended = RefinedUser.safeExtend({ name: z.string() }); // ✅
const Extended = RefinedUser.extend({ name: z.string() });     // ❌ Throws
```

### Transforms Lock All Object Methods

Applying `.transform()` or `.refine()` to an object schema changes its type from `ZodObject` to `ZodEffects` (Zod 3) or `ZodPipe` (Zod 4). Object-specific methods are no longer available:

```typescript
const Schema = z.object({ name: z.string() }).transform(d => ({ ...d, name: d.name.trim() }));
Schema.pick({ name: true }); // ❌ Runtime error: .pick is not a function
```

**Rule: Always apply transforms LAST.** Complete all structural composition before chaining `.transform()`.

## Input vs. Output Types

Every schema tracks two types internally:

- **Input type**: Shape of raw data before parsing
- **Output type**: Shape of data after all coercions and transforms

These are identical for simple schemas (`z.string()`, `z.number()`), but diverge when transforms or coercions are used.

```typescript
const AgeSchema = z.string().pipe(z.coerce.number().int().positive());
type AgeInput = z.input<typeof AgeSchema>;   // string
type AgeOutput = z.output<typeof AgeSchema>; // number

// Always type incoming form/query parameters with z.input
// Always type internal business types with z.infer (= z.output)
```

### `.default()` vs `.prefault()`

This distinction matters critically in Zod 4:

```typescript
// .default(): value must match OUTPUT type; applied AFTER parsing would occur
// If input is undefined, Zod returns the default directly without running validation
const WithDefault = z.string().toLowerCase().default("hello");
// default "hello" is an output-type string — parsing is skipped entirely

// .prefault(): value must match INPUT type; injected BEFORE the parse pipeline runs
const WithPrefault = z.string().toLowerCase().prefault("HELLO");
// prefault "HELLO" is an input-type string — it runs through toLowerCase()
// Result: "hello"
```

Use `.prefault()` when the default value should go through the transform pipeline. Use `.default()` when you want to short-circuit parsing entirely.

## Discriminated Unions

Always prefer `z.discriminatedUnion()` over `z.union()` for objects sharing a common discriminator key:

```typescript
// SLOW: Checks every option in sequence
const EventSchema = z.union([
  z.object({ type: z.literal("click"), x: z.number(), y: z.number() }),
  z.object({ type: z.literal("keydown"), key: z.string() }),
  z.object({ type: z.literal("scroll"), delta: z.number() }),
]);

// FAST: Uses discriminator key to jump directly to correct option
const EventSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("click"), x: z.number(), y: z.number() }),
  z.object({ type: z.literal("keydown"), key: z.string() }),
  z.object({ type: z.literal("scroll"), delta: z.number() }),
]);
```

Discriminated unions also produce more specific error messages — errors describe the matched shape, not every option.

## Transforms: Ordering and the `abort` Flag

Transforms execute even if a preceding refinement fails in Zod 4. This can cause runtime crashes:

```typescript
// DANGEROUS: transform runs even if refine fails
const ParsedJson = z.string()
  .refine(s => s.startsWith("{"), "Must be JSON object")
  .transform(s => JSON.parse(s)); // Runs even if refine fails → SyntaxError

// SAFE: abort: true halts the pipeline on refine failure
const ParsedJson = z.string()
  .refine(s => s.startsWith("{"), { message: "Must be JSON object", abort: true })
  .transform(s => JSON.parse(s)); // Only runs if refine passed
```

Always pass `{ abort: true }` to `.refine()` when a subsequent `.transform()` assumes the data is valid.

## Safe Coercion with `.pipe()`

Never apply `z.coerce` directly to completely unknown data. Constrain the input type first, then pipe:

```typescript
// RISKY: Coercion on unconstrained input can throw before Zod catches it
const AgeSchema = z.coerce.number();

// SAFE: Constrain to expected input shapes, then coerce
const AgeSchema = z.union([z.string(), z.number()])
  .pipe(z.coerce.number().int().min(0).max(150));
```

## Deriving DTOs: pick, omit, partial, required

Use these to derive specialized schemas from a base without duplicating rules:

```typescript
const UserSchema = z.strictObject({
  id: z.string().uuid(),
  email: z.email(),
  password: z.string().min(12),
  role: z.enum(["admin", "user"]),
  createdAt: z.date(),
});

// API response (strip sensitive fields)
const PublicUserSchema = UserSchema.omit({ password: true });

// Create endpoint (no id/createdAt — server assigns these)
const CreateUserSchema = UserSchema.omit({ id: true, createdAt: true });

// PATCH endpoint (all fields optional, no defaults that could overwrite)
const PatchUserSchema = UserSchema.pick({ email: true, role: true }).partial();
```

**Critical Zod 4 warning:** Do NOT use `.partial()` on schemas with `.default()` values for PATCH endpoints. In Zod 4, defaults are always applied even when a field is absent — this will overwrite existing database records with default values instead of leaving them untouched.

## Merging Refined Schemas

Spreading `.shape` loses refinements. Use `z.intersection()` to combine schemas with their logic intact:

```typescript
const WithTrimmed = z.object({ name: z.string() }).refine(d => d.name.length > 0);
const WithAge = z.object({ age: z.number() }).refine(d => d.age >= 0);

// WRONG: Loses both refinements
const Combined = z.object({ ...WithTrimmed.shape, ...WithAge.shape });

// CORRECT: Preserves both refinements
const Combined = z.intersection(WithTrimmed, WithAge);
```

## Recursive Schemas

TypeScript cannot infer the type of recursive schemas — define the type explicitly first:

```typescript
type Category = {
  name: string;
  subcategories: Category[];
};

const CategorySchema: z.ZodType<Category> = z.lazy(() =>
  z.object({
    name: z.string(),
    subcategories: z.array(CategorySchema),
  })
);
```

Never pass cyclical JavaScript objects to a recursive Zod schema — this causes an infinite loop at runtime.

## Branded Types

Branded types enforce nominal typing at compile time. They have **zero runtime effect** — `.parse()` returns the same data; the brand is only a TypeScript type-level marker:

```typescript
const UserIdSchema = z.string().uuid().brand("UserId");
type UserId = z.infer<typeof UserIdSchema>; // string & { readonly [brand]: "UserId" }

function getUser(id: UserId) { /* ... */ }
getUser("raw-string"); // ❌ TypeScript error
getUser(UserIdSchema.parse(someId)); // ✅ Passes through parse to get branded type
```

## Additional Resources

- **`references/composition-patterns.md`** — Complete pattern reference with code examples for each composition method
- **`references/edge-cases.md`** — Edge cases: pipe strictness, lazy inference limitations, intersection limits
