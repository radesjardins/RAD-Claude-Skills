# Fastify Type Providers: Complete Setup Guide

## Installation

```bash
npm install fastify fastify-type-provider-zod zod
npm install --save-dev @types/node
```

## Application Setup

```typescript
import Fastify from 'fastify';
import {
  serializerCompiler,
  validatorCompiler,
  ZodTypeProvider,
} from 'fastify-type-provider-zod';
import { z } from 'zod';

const app = Fastify({ logger: true })
  .withTypeProvider<ZodTypeProvider>();

// Set compilers — required for Zod integration
app.setValidatorCompiler(validatorCompiler);
app.setSerializerCompiler(serializerCompiler);

// Global error handler for Zod validation errors
app.setErrorHandler((error, request, reply) => {
  if (error.validation) {
    // Fastify validation error (from Zod)
    return reply.status(400).send({
      error: 'VALIDATION_FAILED',
      details: error.validation,
    });
  }
  reply.status(500).send({ error: 'INTERNAL_SERVER_ERROR' });
});
```

## Route Definition with Full Type Safety

```typescript
import { z } from 'zod';

// Shared schemas — define once, use across routes
const UserIdParamSchema = z.object({
  id: z.string().uuid('Invalid user ID format'),
});

const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string(),
  role: z.enum(['admin', 'user']),
  createdAt: z.coerce.date(),
});

const CreateUserBodySchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  role: z.enum(['admin', 'user']).default('user'),
});

const ErrorSchema = z.object({
  error: z.string(),
  message: z.string().optional(),
  details: z.record(z.string(), z.array(z.string())).optional(),
});

// GET /users/:id
app.get(
  '/users/:id',
  {
    schema: {
      params: UserIdParamSchema,
      response: {
        200: UserSchema,
        404: ErrorSchema,
      },
    },
  },
  async (request, reply) => {
    // request.params.id is string (UUID validated) — fully typed!
    const user = await getUserById(request.params.id);
    if (!user) {
      return reply.status(404).send({ error: 'NOT_FOUND', message: `User ${request.params.id} not found` });
    }
    return reply.status(200).send(user); // Validates against UserSchema before sending
  }
);

// POST /users
app.post(
  '/users',
  {
    schema: {
      body: CreateUserBodySchema,
      response: {
        201: UserSchema,
        400: ErrorSchema,
        409: ErrorSchema,
      },
    },
  },
  async (request, reply) => {
    // request.body is { email: string; name: string; role: 'admin' | 'user' }
    const existing = await getUserByEmail(request.body.email);
    if (existing) {
      return reply.status(409).send({ error: 'CONFLICT', message: 'Email already registered' });
    }
    const user = await createUser(request.body);
    return reply.status(201).send(user);
  }
);
```

## Schema Registration with `$ref`

For shared schemas across routes, register them to avoid duplication:

```typescript
// Register shared schema
app.addSchema({
  $id: 'User',
  ...UserSchema, // Spread Zod schema or use TypeBox directly
});

// Reference by $id in routes
app.get(
  '/me',
  {
    schema: {
      response: { 200: { $ref: 'User#' } },
    },
  },
  async (request, reply) => {
    const user = await getAuthenticatedUser(request);
    return reply.status(200).send(user);
  }
);
```

## Plugin Architecture for Route Organization

```typescript
// routes/users/index.ts
import type { FastifyPluginAsyncZod } from 'fastify-type-provider-zod';

const usersPlugin: FastifyPluginAsyncZod = async (fastify) => {
  fastify.get(
    '/',
    {
      schema: {
        querystring: PaginationSchema,
        response: {
          200: z.object({
            data: z.array(UserSchema),
            total: z.number(),
            page: z.number(),
          }),
        },
      },
    },
    async (request) => {
      const { page, pageSize } = request.query;
      const { data, total } = await listUsers({ page, pageSize });
      return { data, total, page };
    }
  );

  fastify.post(
    '/',
    {
      schema: {
        body: CreateUserBodySchema,
        response: { 201: UserSchema, 400: ErrorSchema },
      },
    },
    async (request, reply) => {
      const user = await createUser(request.body);
      return reply.status(201).send(user);
    }
  );
};

export default usersPlugin;

// app.ts
app.register(usersPlugin, { prefix: '/users' });
```

## Authentication Hook with Type Safety

```typescript
const AuthHeadersSchema = z.object({
  authorization: z.string().regex(/^Bearer .+$/),
});

// Prehandler that adds user to request
app.decorateRequest('user', null);

app.addHook('preHandler', async (request, reply) => {
  const headers = AuthHeadersSchema.safeParse(request.headers);
  if (!headers.success) {
    return reply.status(401).send({ error: 'UNAUTHORIZED' });
  }

  const token = headers.data.authorization.replace('Bearer ', '');
  const user = await verifyToken(token);
  if (!user) {
    return reply.status(401).send({ error: 'UNAUTHORIZED' });
  }

  request.user = user;
});
```

## TypeBox Alternative (for OpenAPI generation)

When OpenAPI spec generation is needed:

```bash
npm install @fastify/swagger @fastify/swagger-ui @sinclair/typebox
```

```typescript
import { Type } from '@sinclair/typebox';

// TypeBox schemas generate valid JSON Schema + TypeScript types
const UserSchema = Type.Object({
  id: Type.String({ format: 'uuid' }),
  email: Type.String({ format: 'email' }),
  name: Type.String({ minLength: 1 }),
});

type User = Static<typeof UserSchema>; // TypeScript type from TypeBox schema
```

## End-to-End Type Safety with tRPC

For frontend + backend in the same monorepo:

```typescript
// server/router.ts (backend)
import { initTRPC } from '@trpc/server';
import { z } from 'zod';

const t = initTRPC.create();

export const appRouter = t.router({
  users: t.router({
    getById: t.procedure
      .input(z.object({ id: z.string().uuid() }))
      .query(async ({ input }) => {
        return getUserById(input.id); // Return type inferred
      }),
    create: t.procedure
      .input(CreateUserBodySchema)
      .mutation(async ({ input }) => {
        return createUser(input);
      }),
  }),
});

export type AppRouter = typeof appRouter;

// client/api.ts (frontend) — types flow automatically
import type { AppRouter } from '../server/router';
import { createTRPCClient } from '@trpc/client';

const client = createTRPCClient<AppRouter>({ ... });
const user = await client.users.getById.query({ id: '...' }); // Fully typed!
```
