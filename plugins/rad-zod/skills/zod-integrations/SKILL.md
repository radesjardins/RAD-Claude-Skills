---
name: Zod Framework Integrations
description: This skill should be used when the user asks about "Zod with Fastify", "Zod type provider", "fastify-type-provider-zod", "Zod with Next.js", "Zod server actions", "Zod React Hook Form", "zodResolver", "Zod tRPC", "Zod monorepo", "shared Zod schemas", "Zod shared package", "Zod dual instance error", "ID already exists registry", "Zod frontend backend", "Zod AI SDK", or when integrating Zod with any web framework. Provides patterns for all major framework integrations and monorepo architecture.
version: 1.0.0
---

# Zod Framework Integrations

## Fastify: Type-Provider Integration

The `fastify-type-provider-zod` package connects Zod schemas directly to Fastify's type inference system:

```typescript
import Fastify from "fastify";
import { ZodTypeProvider, serializerCompiler, validatorCompiler } from "fastify-type-provider-zod";
import { z } from "zod";

const app = Fastify().withTypeProvider<ZodTypeProvider>();

// Required: attach Zod compilers
app.setValidatorCompiler(validatorCompiler);
app.setSerializerCompiler(serializerCompiler);

const CreateUserBody = z.strictObject({
  name: z.string().min(1),
  email: z.email(),
});

const UserResponse = z.object({
  id: z.string().uuid(),
  name: z.string(),
  email: z.email(),
});

app.post("/users", {
  schema: {
    body: CreateUserBody,
    response: { 201: UserResponse },
  },
}, async (req, reply) => {
  // req.body is fully typed as z.infer<typeof CreateUserBody>
  // Response schema prevents leaking fields not in UserResponse
  const user = await db.createUser(req.body);
  return reply.status(201).send(user);
});
```

**Key benefits:**
- Request body, query params, path params automatically validated and typed
- Response schema enforced — extra fields not in the schema are stripped from responses
- 400 errors returned automatically on validation failure — no manual error handling needed

**Security note:** Use `z.strictObject()` for request body schemas to prevent over-posting. The response schema can use `z.object()` (strip mode) since you're controlling what goes out.

## Next.js: Server Actions

Use `.safeParse()` inside Server Actions — never `.parse()`. A thrown exception in a Server Action crashes the action instead of returning a validation error to the client:

```typescript
// shared/schemas.ts — shared between client and server
export const CreatePostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(10),
});
export type CreatePostInput = z.infer<typeof CreatePostSchema>;

// app/actions/posts.ts
"use server";
import { CreatePostSchema } from "@/shared/schemas";

export async function createPost(formData: FormData) {
  const raw = {
    title: formData.get("title"),
    content: formData.get("content"),
  };

  const result = CreatePostSchema.safeParse(raw);
  if (!result.success) {
    return {
      success: false,
      errors: z.flattenError(result.error).fieldErrors,
    };
  }

  // result.data is fully typed
  await db.posts.create(result.data);
  return { success: true };
}
```

## React Hook Form: `zodResolver`

```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

// Form schemas often need coercion for HTML input types
const RegisterSchema = z.object({
  email: z.email(),
  age: z.coerce.number().int().min(13).max(120), // HTML inputs return strings
  birthdate: z.coerce.date(), // <input type="date"> returns string
  avatar: z.file().max(5 * 1024 * 1024).type("image/*"),
});
type RegisterForm = z.infer<typeof RegisterSchema>;

function RegisterForm() {
  const { register, handleSubmit, formState: { errors } } =
    useForm<RegisterForm>({ resolver: zodResolver(RegisterSchema) });

  return (
    <form onSubmit={handleSubmit(async (data) => { /* data is typed RegisterForm */ })}>
      <input {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}
    </form>
  );
}
```

**Form schema vs API schema:** Form schemas often differ from API schemas due to coercion needs (`z.coerce.number()`, `z.coerce.date()`). Share a base schema and layer coercions on top for the form layer rather than duplicating the entire schema.

**Multi-step forms:** Wrap with `FormProvider` and use `useFormContext()` in step components — avoid prop drilling the register/errors objects.

## Monorepo: Shared Schema Package

The canonical architecture for full-stack type safety:

```
packages/
  schemas/          ← Shared Zod schemas
    package.json    ← "zod" as peerDependency (NOT dependency)
    src/
      user.ts
      post.ts
      index.ts      ← Re-export all schemas

apps/
  web/              ← Frontend (imports from @workspace/schemas)
  api/              ← Backend (imports from @workspace/schemas)
```

```typescript
// packages/schemas/src/user.ts
import { z } from "zod"; // Resolved to the single workspace Zod instance

export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.email(),
  role: z.enum(["admin", "user"]),
});
export type User = z.infer<typeof UserSchema>;

// apps/web/src/auth.tsx
import { UserSchema } from "@workspace/schemas"; // ✅ Same Zod instance
// NOT: import { z } from "zod" // ❌ May create a second instance
```

**Force single Zod version at workspace root:**

```jsonc
// package.json (workspace root)
{
  "pnpm": {
    "overrides": { "zod": "^4.0.0" }
  },
  // npm: "overrides": { "zod": "^4.0.0" }
  // yarn: "resolutions": { "zod": "^4.0.0" }
}
```

### The "ID already exists in registry" Error

This error occurs in Zod 4.1.13+ when the same schema with `.meta({ id })` is evaluated twice — either from duplicate Zod instances or from schema definitions inside dynamic/called functions:

```typescript
// WRONG: Dynamic schema creation generates duplicate IDs
function buildSchema(fields: string[]) {
  return z.object({ name: z.string() }).meta({ id: "user-schema" }); // Re-registered on each call!
}

// CORRECT: Static, module-level schema with .meta() id
export const UserSchema = z.object({ name: z.string() }).meta({ id: "user-schema" });
```

Resolution steps:
1. Ensure `"zod"` is a `peerDependency` in shared packages (not `dependency`)
2. Add workspace-root version override to force single Zod instance
3. Move all `.meta({ id })` assignments to module-level constants
4. Centralize all Zod imports through the shared package

## Vercel AI SDK: `zodSchema()` Helper

When using Zod schemas with the Vercel AI SDK for structured output or tool definitions:

```typescript
import { generateObject } from "ai";
import { zodSchema } from "ai/zod";
import { z } from "zod";

const RecipeSchema = z.object({
  name: z.string(),
  ingredients: z.array(z.object({ item: z.string(), amount: z.string() })),
  steps: z.array(z.string()),
});

const { object } = await generateObject({
  model: openai("gpt-4o"),
  schema: zodSchema(RecipeSchema),
  prompt: "Generate a recipe for chocolate cake",
});
// object is typed as z.infer<typeof RecipeSchema>
```

## Additional Resources

- **`references/fastify-integration.md`** — Complete Fastify setup with query params, path params, response schemas, error handling
- **`references/nextjs-integration.md`** — Next.js App Router patterns, Server Actions, route handlers, middleware validation
- **`references/rhf-integration.md`** — React Hook Form: coercion patterns, file inputs, date fields, multi-step forms, create/edit form hooks
- **`references/monorepo-guide.md`** — Full monorepo architecture: peerDependencies, workspace overrides, centralized imports, tRPC integration
