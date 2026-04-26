# Zod Mental Model: Parse, Don't Validate

## Why TypeScript Isn't Enough

TypeScript provides compile-time safety. Once compiled to JavaScript, all type information is erased. The code running in production has no knowledge of `interface User` or `type OrderStatus`. Any data entering your application from outside — HTTP requests, database queries, file reads, environment variables — arrives as `unknown` at runtime.

Without runtime validation, TypeScript's safety guarantees are a lie at the boundary. Consider:

```typescript
interface User { id: string; email: string; role: "admin" | "user"; }

async function getUser(id: string): Promise<User> {
  const row = await db.query(`SELECT * FROM users WHERE id = ?`, [id]);
  return row as User; // ← Cast from unknown. No check. TypeScript lies here.
}
```

The database might return `role: "superuser"` from a legacy migration. TypeScript is silent. Your code proceeds with a `User` that violates its own contract.

## The Parse-Don't-Validate Pattern

**Validate:** A function that takes data and returns `true/false`. The caller must still decide what the data means.

**Parse:** A function that takes `unknown` and returns a typed value — or throws. The type is guaranteed by the act of parsing.

```typescript
// Validate pattern — still requires unsafe cast
function isUser(data: unknown): data is User {
  return typeof data === "object" && data !== null && "email" in data;
}
// Caller: const user = data as User; // Still a cast

// Parse pattern — type emerges from parsing
const UserSchema = z.object({ email: z.email(), role: z.enum(["admin", "user"]) });
const user = UserSchema.parse(data); // user: User — guaranteed by structure
```

## Zod as the Type System at Runtime

The mental model: **Zod schemas are the TypeScript type system extended to runtime.** Where TypeScript enforces `email: string` at compile time, Zod enforces `email: z.email()` at runtime. They should mirror each other perfectly — and Zod's `z.infer<>` ensures they do.

## The Lifecycle Diagram

```
External World          Zod Boundary              Internal Application
─────────────────────   ─────────────────         ────────────────────────────
HTTP request body    →  schema.safeParse()  →      Typed data (trusted)
URL query params     →  schema.parse()      →      Business logic
API response         →  schema.parse()      →      Rendering / computation
FormData             →  resolver.resolve()  →      Form state
Environment vars     →  schema.parse()      →      Config object
DB result set        →  schema.parse()      →      Domain model
```

After the Zod boundary, never re-validate. The TypeScript compiler enforces contracts from that point on.

## Coercion vs Transformation

**Coercion** converts types to match the schema's expected primitive (e.g., `"42"` → `42`). Use at boundaries with loose input types (query strings, form data, CLI args).

**Transformation** reshapes the parsed value into a different structure. The output type can differ from the input type.

```typescript
// Coercion: same semantic meaning, different runtime type
const AgeSchema = z.coerce.number(); // "25" → 25

// Transformation: semantic change
const FullNameSchema = z.object({ first: z.string(), last: z.string() })
  .transform(({ first, last }) => `${first} ${last}`);
// Input: { first: "Alice", last: "Smith" } → Output: "Alice Smith"
```

Coercions are for raw data ingestion. Transformations are for domain model shaping. The distinction matters for `z.input` vs `z.output` typing — both diverge the types.

## Environment Variable Validation

Always validate env vars at startup. Never access `process.env` directly in business code:

```typescript
// config.ts — run at startup before any other imports
const EnvSchema = z.object({
  DATABASE_URL: z.url(),
  JWT_SECRET: z.string().min(32),
  PORT: z.coerce.number().int().default(3000),
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
});

export const config = EnvSchema.parse(process.env);
// Any missing or malformed env var throws immediately with a clear error
// Rest of app uses config.DATABASE_URL (typed string), config.PORT (typed number)
```
