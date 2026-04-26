# Zod Monorepo Architecture Guide

## The Single Source of Truth Pattern

The goal: one Zod schema definition, shared by frontend, backend, CLI tools, and any other consumers — with a single Zod instance in memory.

## Repository Structure

```
workspace/
├── package.json                    # Root workspace config with version override
├── pnpm-workspace.yaml             # (pnpm) or workspaces: in package.json
├── packages/
│   └── schemas/                    # Shared validation package
│       ├── package.json
│       └── src/
│           ├── user.ts
│           ├── post.ts
│           ├── common.ts           # Shared primitives (pagination, id, etc.)
│           └── index.ts            # Barrel export
├── apps/
│   ├── web/                        # Frontend (Next.js, Vite, etc.)
│   │   └── package.json            # "zod" NOT listed here
│   └── api/                        # Backend (Fastify, Express, etc.)
│       └── package.json            # "zod" NOT listed here
```

## packages/schemas/package.json

```json
{
  "name": "@workspace/schemas",
  "version": "1.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "peerDependencies": {
    "zod": "^4.0.0"
  },
  "devDependencies": {
    "zod": "^4.0.0"
  }
}
```

**Critical:** `zod` is a `peerDependency`, NOT a `dependency`. This prevents bundlers from creating a nested, isolated copy of Zod inside the `@workspace/schemas` package.

## Root Package.json: Version Override

Force all packages in the workspace to use the same Zod version:

```json
// pnpm
{
  "pnpm": {
    "overrides": {
      "zod": "^4.0.0"
    }
  }
}

// npm
{
  "overrides": {
    "zod": "^4.0.0"
  }
}

// yarn
{
  "resolutions": {
    "zod": "^4.0.0"
  }
}
```

## Schema Package: Example Implementation

```typescript
// packages/schemas/src/common.ts
import { z } from "zod";

export const IdSchema = z.string().uuid();
export const PaginationSchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});
export const TimestampsSchema = z.object({
  createdAt: z.date(),
  updatedAt: z.date(),
});

// packages/schemas/src/user.ts
import { z } from "zod";
import { IdSchema, TimestampsSchema } from "./common";

export const UserSchema = z.object({
  id: IdSchema,
  email: z.email(),
  name: z.string().min(1).max(100),
  role: z.enum(["admin", "user", "moderator"]),
  bio: z.string().max(500).nullable(),
}).merge(TimestampsSchema);

export const CreateUserSchema = z.strictObject({
  email: z.email(),
  name: z.string().min(1).max(100),
  password: z.string().min(12),
});

export const PatchUserSchema = z.strictObject({
  email: z.email().optional(),
  name: z.string().min(1).max(100).optional(),
  bio: z.string().max(500).nullable().optional(),
});

export type User = z.infer<typeof UserSchema>;
export type CreateUserInput = z.infer<typeof CreateUserSchema>;
export type PatchUserInput = z.infer<typeof PatchUserSchema>;

// packages/schemas/src/index.ts
export * from "./common";
export * from "./user";
export * from "./post";
```

## Frontend Usage (Next.js / React)

```typescript
// apps/web/src/app/users/create/actions.ts
"use server";
import { CreateUserSchema } from "@workspace/schemas"; // ← Shared schema

export async function createUserAction(formData: FormData) {
  const result = CreateUserSchema.safeParse({
    email: formData.get("email"),
    name: formData.get("name"),
    password: formData.get("password"),
  });
  if (!result.success) {
    return { success: false, errors: z.flattenError(result.error).fieldErrors };
  }
  // call API
}

// apps/web/src/app/users/create/form.tsx
import { CreateUserSchema } from "@workspace/schemas";
import { zodResolver } from "@hookform/resolvers/zod";
// Uses the exact same schema for client-side validation
```

## Backend Usage (Fastify)

```typescript
// apps/api/src/routes/users.ts
import { CreateUserSchema, PatchUserSchema, UserSchema } from "@workspace/schemas";
import { ZodTypeProvider } from "fastify-type-provider-zod";

export default async function userRoutes(app: FastifyInstance) {
  app.post<{ Body: CreateUserInput }>("/users", {
    schema: {
      body: CreateUserSchema,
      response: { 201: UserSchema.omit({ password: true }) },
    },
  }, async (req, reply) => {
    // req.body fully typed as CreateUserInput
    const user = await userService.create(req.body);
    return reply.status(201).send(user);
  });
}
```

## tRPC Integration

```typescript
// packages/schemas is imported by tRPC router
import { CreateUserSchema, UserSchema } from "@workspace/schemas";
import { initTRPC } from "@trpc/server";

const t = initTRPC.create();

export const appRouter = t.router({
  users: t.router({
    create: t.procedure
      .input(CreateUserSchema)
      .mutation(async ({ input }) => {
        // input is typed as CreateUserInput
        return userService.create(input);
      }),

    getById: t.procedure
      .input(z.object({ id: z.string().uuid() }))
      .query(async ({ input }) => {
        return userService.findById(input.id);
      }),
  }),
});

export type AppRouter = typeof appRouter;
```

## Resolving the "ID already exists in registry" Error

**Symptom:** `Error: Schema with id "X" already exists in registry`

**Root causes and fixes:**

### Cause 1: Multiple Zod instances
Two copies of Zod loaded (CJS and ESM, or two versions):

```bash
# Check for duplicate Zod installations
pnpm list zod --recursive
# Should show ONE version. Multiple → add pnpm.overrides
```

### Cause 2: Schema with `.meta({ id })` in a called function

```typescript
// WRONG: Called twice → second registration fails
function getSchema() {
  return z.string().meta({ id: "my-id" }); // Re-registered each call!
}

// CORRECT: Static export
export const MySchema = z.string().meta({ id: "my-id" }); // Registered once
```

### Cause 3: Dynamic imports causing double evaluation in hot reload

In development with hot module replacement, schemas may be re-evaluated. Either:
1. Remove `.meta({ id })` from schemas that don't need JSON Schema export
2. Use a custom registry that handles duplicate IDs gracefully:

```typescript
const SafeRegistry = z.registry();
// Check before adding
function registerSchema(schema: z.ZodType, meta: { id: string; title: string }) {
  if (!SafeRegistry.has(schema)) {
    SafeRegistry.add(schema, meta);
  }
}
```
