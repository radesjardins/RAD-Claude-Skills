# Fastify + Zod Integration Reference

## Installation

```bash
npm install fastify fastify-type-provider-zod zod
```

## Complete Setup

```typescript
import Fastify from "fastify";
import {
  ZodTypeProvider,
  serializerCompiler,
  validatorCompiler,
  FastifyZodOpenApiOptions,
} from "fastify-type-provider-zod";
import { z } from "zod";

const app = Fastify({ logger: true }).withTypeProvider<ZodTypeProvider>();

app.setValidatorCompiler(validatorCompiler);
app.setSerializerCompiler(serializerCompiler);
```

## Route Schema Patterns

### POST Route (Body Validation)

```typescript
const CreatePostBody = z.strictObject({
  title: z.string().min(1).max(200),
  content: z.string().min(10),
  tags: z.array(z.string()).max(10).default([]),
  publishedAt: z.iso.datetime().optional(),
});

const PostResponse = z.object({
  id: z.string().uuid(),
  title: z.string(),
  content: z.string(),
  tags: z.array(z.string()),
  createdAt: z.date(),
});

app.post("/posts", {
  schema: {
    body: CreatePostBody,
    response: {
      201: PostResponse,
      400: z.object({ message: z.string(), errors: z.record(z.string(), z.array(z.string())) }),
    },
  },
}, async (req, reply) => {
  // req.body is fully typed as z.infer<typeof CreatePostBody>
  const post = await postService.create(req.body);
  return reply.status(201).send(post);
});
```

### GET Route (Query Parameters)

```typescript
const GetPostsQuery = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  category: z.string().optional(),
  sort: z.enum(["newest", "oldest", "popular"]).default("newest"),
});

app.get("/posts", {
  schema: { querystring: GetPostsQuery },
}, async (req, reply) => {
  // req.query fully typed, page and limit already numbers (coerced from query string)
  const posts = await postService.findAll(req.query);
  return posts;
});
```

### GET Route (Path Parameters)

```typescript
const PostParams = z.object({
  id: z.string().uuid("Post ID must be a valid UUID"),
});

app.get("/posts/:id", {
  schema: {
    params: PostParams,
    response: {
      200: PostResponse,
      404: z.object({ message: z.string() }),
    },
  },
}, async (req, reply) => {
  // req.params.id is typed as string (UUID validated)
  const post = await postService.findById(req.params.id);
  if (!post) {
    return reply.status(404).send({ message: "Post not found" });
  }
  return post;
});
```

### PATCH Route

```typescript
const PatchPostBody = z.strictObject({
  title: z.string().min(1).max(200).optional(),
  content: z.string().min(10).optional(),
  tags: z.array(z.string()).max(10).optional(),
});

app.patch("/posts/:id", {
  schema: {
    params: PostParams,
    body: PatchPostBody,
    response: { 200: PostResponse },
  },
}, async (req, reply) => {
  const updates = Object.fromEntries(
    Object.entries(req.body).filter(([, v]) => v !== undefined)
  );
  return postService.update(req.params.id, updates);
});
```

## Authentication Header Validation

```typescript
const AuthHeaders = z.object({
  authorization: z.string().startsWith("Bearer "),
});

app.addHook("preHandler", async (req, reply) => {
  const result = AuthHeaders.safeParse(req.headers);
  if (!result.success) {
    return reply.status(401).send({ message: "Missing or invalid Authorization header" });
  }
  // Access token
  req.token = result.data.authorization.slice(7);
});
```

## Global Zod Error Handler

```typescript
app.setErrorHandler((error, req, reply) => {
  if (error instanceof z.ZodError) {
    return reply.status(400).send({
      message: "Validation error",
      errors: z.flattenError(error).fieldErrors,
    });
  }
  // Other error handling
  reply.status(500).send({ message: "Internal server error" });
});
```

## Response Schema Security

The `response` schema in Fastify strips fields not defined in the schema — this is your protection against accidentally leaking sensitive fields:

```typescript
const UserDbRow = {
  id: "...",
  email: "...",
  password: "$2b$12$hashedpassword",  // Never expose this
  internalNotes: "...",                // Never expose this
  role: "admin",
};

// Response schema only includes safe fields
const PublicUserResponse = z.object({
  id: z.string(),
  email: z.string(),
  role: z.string(),
  // password and internalNotes NOT included → stripped from response
});

app.get("/users/:id", {
  schema: { response: { 200: PublicUserResponse } },
}, async (req, reply) => {
  const user = await db.users.findById(req.params.id);
  return user; // Fastify strips password and internalNotes automatically
});
```
