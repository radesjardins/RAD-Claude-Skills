---
name: typescript-api-safety
description: >
  This skill should be used when writing API endpoints, handling external data, validating
  HTTP requests or responses, parsing user input, working with environment variables, designing
  type-safe API boundaries, integrating Zod for runtime validation, implementing Fastify with
  type providers, sharing types in monorepos, or setting up parse-don't-validate patterns.
  Trigger on: "API boundary", "parse don't validate", "Zod schema", "runtime validation",
  "validate request body", "safe parse", "schema-first", "type-safe API", "Fastify type provider",
  "shared types monorepo", "validate environment variables", "external data", "unknown input",
  "z.infer", "request validation", "response validation", "API contract".
---

# TypeScript API Safety: Parse, Don't Validate

The most dangerous data in any application is the data entering from the outside world. API responses, request bodies, environment variables, and file contents are all `unknown` at runtime — no matter what your TypeScript types say. The solution is a single guiding principle: **parse, don't validate**.

## The Core Principle

**Validate** checks if data matches a type and returns boolean. **Parse** transforms untyped data into a strictly-typed object at the boundary. After parsing, the data is trusted throughout the application.

```typescript
// ❌ Validate (type assertion — lying to the compiler)
const user = response.json() as User; // No runtime check — crashes on malformed data

// ❌ Validate (boolean check — type widening, no transformation)
function isUser(data: unknown): boolean {
  return typeof data === 'object' && data !== null;
}
// ...TypeScript still doesn't know data is User

// ✅ Parse (transform + prove type simultaneously)
const result = UserSchema.safeParse(await response.json());
if (!result.success) return sendError(400, result.error.flatten());
const user = result.data; // User — validated, typed, trustworthy
```

## Schema-First Design with Zod

Zod schemas are the **single source of truth** for both runtime validation and TypeScript types. Never maintain separate interfaces and validators.

```typescript
import { z } from 'zod';

// One schema — generates both the validator and the type
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1).max(100),
  role: z.enum(['admin', 'user', 'moderator']),
  createdAt: z.coerce.date(), // Coerce string → Date automatically
  metadata: z.record(z.string()).optional(),
});

// Derive TypeScript type from schema — never write the interface manually
type User = z.infer<typeof UserSchema>;

// Export schema for validation + type for usage
export { UserSchema, type User };
```

## Always Use `.safeParse()` at Boundaries

`.parse()` throws on invalid input. `.safeParse()` returns a Result-like object. Always use `.safeParse()` at API boundaries.

```typescript
// ❌ .parse() — throws ZodError, requires try/catch overhead
const user = UserSchema.parse(body); // Throws if invalid

// ✅ .safeParse() — returns Result, no throws
const result = UserSchema.safeParse(body);
if (!result.success) {
  // result.error is ZodError with detailed validation failures
  return {
    status: 400,
    errors: result.error.flatten().fieldErrors,
  };
}
const user = result.data; // Fully typed User
```

## Where to Place Validation Boundaries

Validate at **every entry point into your system**:

1. **HTTP request bodies** — before handler logic
2. **HTTP response parsing** — when consuming external APIs
3. **Environment variables** — at app startup
4. **File/config reading** — JSON config, CSV, YAML
5. **Message queue payloads** — events from other services
6. **Database query results** — only if DB schema can diverge from TS types

```typescript
// Environment variables — validate at startup, crash fast if missing
const EnvSchema = z.object({
  DATABASE_URL: z.string().url(),
  PORT: z.coerce.number().int().min(1024).max(65535),
  NODE_ENV: z.enum(['development', 'production', 'test']),
  JWT_SECRET: z.string().min(32),
  API_KEY: z.string().min(16),
});

const env = EnvSchema.parse(process.env); // Throw at startup if misconfigured
export type Env = typeof env;
export { env }; // env is fully typed throughout the app
```

## Fastify with Type Providers

Fastify's type provider architecture automatically synchronizes JSON Schema and TypeScript types:

```typescript
import Fastify from 'fastify';
import { serializerCompiler, validatorCompiler, ZodTypeProvider } from 'fastify-type-provider-zod';

const app = Fastify().withTypeProvider<ZodTypeProvider>();
app.setValidatorCompiler(validatorCompiler);
app.setSerializerCompiler(serializerCompiler);

// Route types are inferred from schemas — no manual generics
app.post(
  '/users',
  {
    schema: {
      body: z.object({
        email: z.string().email(),
        name: z.string().min(1),
        role: z.enum(['admin', 'user']),
      }),
      response: {
        201: z.object({
          id: z.string().uuid(),
          email: z.string(),
          name: z.string(),
        }),
        400: z.object({ error: z.string() }),
      },
    },
  },
  async (request, reply) => {
    // request.body is fully typed: { email: string; name: string; role: 'admin' | 'user' }
    const user = await createUser(request.body);
    return reply.status(201).send(user); // Validated against response schema
  }
);
```

## Consuming External APIs Safely

Never trust external API responses, even when the API has TypeScript SDKs.

```typescript
const GithubUserSchema = z.object({
  login: z.string(),
  id: z.number(),
  avatar_url: z.string().url(),
  name: z.string().nullable(),
  email: z.string().email().nullable(),
  public_repos: z.number().int().nonnegative(),
});

type GithubUser = z.infer<typeof GithubUserSchema>;

async function fetchGithubUser(username: string): Promise<Result<GithubUser, 'not-found' | 'api-error'>> {
  const response = await fetch(`https://api.github.com/users/${username}`);

  if (response.status === 404) return err('not-found');
  if (!response.ok) return err('api-error');

  const json = await response.json();
  const parsed = GithubUserSchema.safeParse(json);

  if (!parsed.success) {
    // API returned unexpected shape — treat as api-error
    console.error('Github API schema drift:', parsed.error.flatten());
    return err('api-error');
  }

  return ok(parsed.data);
}
```

## Shared Types in Monorepos

The universal contract pattern: share Zod schemas across packages to maintain a single source of truth.

```
packages/
  @org/shared/
    src/
      schemas/
        user.schema.ts    ← Zod schema + z.infer type
        order.schema.ts
      index.ts            ← Re-exports schemas and types
  api/                    ← imports schema for validation
  web/                    ← imports schema for form validation + type safety
```

```typescript
// @org/shared/src/schemas/user.schema.ts
import { z } from 'zod';

export const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
  role: z.enum(['admin', 'user']),
});

export const UserSchema = CreateUserSchema.extend({
  id: z.string().uuid(),
  createdAt: z.coerce.date(),
});

export type CreateUser = z.infer<typeof CreateUserSchema>;
export type User = z.infer<typeof UserSchema>;

// API (backend):
import { CreateUserSchema } from '@org/shared';
app.post('/users', { schema: { body: CreateUserSchema } }, handler);

// Web (frontend):
import { CreateUserSchema, type CreateUser } from '@org/shared';
const form = useForm<CreateUser>({ resolver: zodResolver(CreateUserSchema) });
```

## Type-Only Imports for ESM Safety

Always use `import type` for type-only imports to prevent bundler issues:

```typescript
// ✅ Correct — type is erased at compile time
import type { User } from '@org/shared';
import { UserSchema } from '@org/shared'; // Runtime value — kept

// ✅ Inline form
import { UserSchema, type User } from '@org/shared';
```

## Additional Resources

For complete implementation guides, consult:
- **`references/zod-boundaries.md`** — Advanced Zod patterns, coercion, transformations, and error formatting
- **`references/fastify-type-providers.md`** — Full Fastify + Zod type provider setup, shared schemas, and response narrowing
