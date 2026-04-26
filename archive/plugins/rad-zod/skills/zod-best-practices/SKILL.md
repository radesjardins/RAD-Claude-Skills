---
name: Zod Best Practices
description: This skill should be used when the user asks about "how to use Zod", "where should I put Zod validation", "Zod best practices", "should I use Zod here", "Zod vs TypeScript types", "parse don't validate", "overvalidation", "Zod single source of truth", or when reviewing or writing TypeScript code that imports from "zod". Provides the core mental model and foundational rules for effective Zod usage.
version: 1.0.0
---

# Zod Best Practices

Zod is a TypeScript-first schema declaration and runtime validation library. Its core purpose is to fill the gap that TypeScript cannot: **TypeScript type safety disappears at compile time**, leaving runtime data — API payloads, form inputs, database results, environment variables — completely unguarded. Zod validates that gap.

## The Core Mental Model: Parse, Don't Validate

Zod's foundational principle is **"parse, don't validate."** The distinction matters:

- **Validating** returns a boolean: `isValid(data)` → `true/false`
- **Parsing** returns a typed value or throws: `schema.parse(data)` → `T | throws ZodError`

Parsing is superior because it forces you to handle the failure case, and the success case produces a strongly-typed value — not just a boolean. After a successful parse, the data is a **deep clone** of the input, with all coercions and transformations applied. Trust the parsed output type completely; treat the raw input as `unknown`.

## The Single Source of Truth Principle

A schema defined once becomes both the **runtime validator** and the **TypeScript type**:

```typescript
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.email(),
  role: z.enum(["admin", "user", "guest"]),
});

// Extract the TypeScript type — no separate interface needed
type User = z.infer<typeof UserSchema>;
```

Never write a TypeScript `interface` or `type` that duplicates a Zod schema. The schema IS the type definition. Use `z.infer<typeof Schema>` everywhere the type is needed.

## Boundary Placement: Where Zod Lives

Validate data **exactly once, at system entry points.** After successful parsing, trust the inferred TypeScript type throughout the rest of the application. Re-validating the same data in multiple layers is overvalidation — an anti-pattern.

**Correct placement:**

| Entry Point | Example |
|---|---|
| HTTP request handlers | API route body, query params, path params |
| Form submission handlers | React Hook Form resolver, Server Action `FormData` |
| External API responses | Third-party REST/GraphQL responses |
| Database query results | When schema may have diverged from TypeScript types |
| Environment variables | At app startup, before any code runs |
| Message queue consumers | Event payloads from queues/streams |

**After parsing, stop.** Internal function calls between modules in the same codebase do not need Zod re-validation. The TypeScript compiler already enforces the contract there.

## The Overvalidation Anti-Pattern

Overvalidation is the most common performance and maintenance problem with Zod:

```typescript
// BAD: Parsing the same user object at every layer
function getUser(id: string) {
  const raw = db.find(id);
  return UserSchema.parse(raw); // First parse
}

function updateUser(id: string, data: unknown) {
  const user = UserSchema.parse(getUser(id)); // Re-parsing already-parsed data
  // ...
}
```

```typescript
// GOOD: Parse once at the boundary
async function handleUpdateUser(req: Request) {
  const body = UpdateUserSchema.parse(req.body); // Single parse at the HTTP boundary
  const existing = await userService.get(body.id); // Trust internal types
  await userService.update(existing, body); // No re-parsing
}
```

## Schema Definition: Hoist to Module Level

Never define schemas inside functions, loops, or component render cycles. Each call to `z.object({...})` instantiates new validator objects, wasting CPU and memory.

```typescript
// BAD: Schema instantiated on every request
app.post("/user", (req, res) => {
  const BodySchema = z.object({ name: z.string(), age: z.number() }); // Re-created every request
  const body = BodySchema.parse(req.body);
});

// GOOD: Schema defined once at module scope
const CreateUserBodySchema = z.object({
  name: z.string(),
  age: z.number().int().positive(),
});

app.post("/user", (req, res) => {
  const body = CreateUserBodySchema.parse(req.body);
});
```

## Strict vs. Loose Object Boundaries

By default, `z.object()` **strips unknown keys** silently. This is convenient for internal reshaping but dangerous at public API boundaries. Use `z.strictObject()` at all external-facing endpoints:

```typescript
// DANGEROUS at API boundary: strips unknown keys, never rejects them
const UserSchema = z.object({ name: z.string() });

// CORRECT at API boundary: rejects requests with unexpected keys
const CreateUserBodySchema = z.strictObject({ name: z.string() });
```

Use `z.object()` (strip) only for internal data transformation where you intentionally want to discard extra fields.

## The z.infer / z.input / z.output Distinction

- **`z.infer<typeof S>`** — The output type after parsing. Use this for internal business logic types.
- **`z.output<typeof S>`** — Identical to `z.infer`. Use when the context benefits from explicitness.
- **`z.input<typeof S>`** — The raw input type before coercions/transforms. Use when typing raw incoming data (e.g., form data before Zod processes it).

When a schema has transforms, input and output types differ:

```typescript
const S = z.string().transform(s => s.length);
type Input = z.input<typeof S>;  // string
type Output = z.output<typeof S>; // number
```

## Quick Invariants

| Rule | Enforcement |
|---|---|
| Define schemas at module scope | Prevents per-call instantiation |
| Use `z.strictObject()` at public API boundaries | Prevents over-posting attacks |
| Use `z.infer<>` for internal types; never duplicate | Keeps types in sync |
| Parse once per data lifetime | Prevents overvalidation |
| Use `.safeParse()` for expected-to-fail paths | Avoids exception overhead |
| Never use `z.custom()` without a validation function | Bypasses all validation |

## Additional Resources

- **`references/mental-model.md`** — Deep dive on parse-don't-validate, lifecycle examples
- **`references/performance-guide.md`** — Performance optimization: lazy schemas, discriminated unions, ZodMini
