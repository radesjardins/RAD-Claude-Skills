# Next.js + Zod Integration Reference

## App Router: Server Actions (Recommended Pattern)

Server Actions are the primary place Zod validation runs in Next.js App Router. Always use `.safeParse()` — a thrown ZodError inside a Server Action crashes the action instead of returning validation errors to the client.

```typescript
// shared/schemas/post.ts
import { z } from "zod";

export const CreatePostSchema = z.strictObject({
  title: z.string().min(1).max(200),
  content: z.string().min(10),
  tags: z.array(z.string().max(30)).max(10).default([]),
  publishAt: z.iso.datetime().optional(),
});
export type CreatePostInput = z.infer<typeof CreatePostSchema>;

// app/posts/actions.ts
"use server";
import { z } from "zod";
import { CreatePostSchema } from "@/shared/schemas/post";
import { revalidatePath } from "next/cache";

type ActionResult =
  | { success: true; postId: string }
  | { success: false; errors: Record<string, string[]> };

export async function createPostAction(formData: FormData): Promise<ActionResult> {
  const raw = {
    title: formData.get("title"),
    content: formData.get("content"),
    tags: formData.getAll("tags"), // multivalue
    publishAt: formData.get("publishAt") || undefined,
  };

  const result = CreatePostSchema.safeParse(raw);
  if (!result.success) {
    return {
      success: false,
      errors: z.flattenError(result.error).fieldErrors,
    };
  }

  // result.data is typed as CreatePostInput
  const post = await db.posts.create(result.data);
  revalidatePath("/posts");
  return { success: true, postId: post.id };
}
```

## App Router: Route Handlers

```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { CreatePostSchema } from "@/shared/schemas/post";

export async function POST(req: NextRequest) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ message: "Invalid JSON" }, { status: 400 });
  }

  const result = CreatePostSchema.safeParse(body);
  if (!result.success) {
    return NextResponse.json(
      { message: "Validation failed", errors: z.flattenError(result.error).fieldErrors },
      { status: 400 }
    );
  }

  const post = await db.posts.create(result.data);
  return NextResponse.json(post, { status: 201 });
}
```

## App Router: Query Parameter Validation

```typescript
// app/api/posts/route.ts (GET)
const GetPostsQuerySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  category: z.string().optional(),
  search: z.string().max(200).optional(),
});

export async function GET(req: NextRequest) {
  const searchParams = Object.fromEntries(req.nextUrl.searchParams);

  const result = GetPostsQuerySchema.safeParse(searchParams);
  if (!result.success) {
    return NextResponse.json({ errors: z.flattenError(result.error).fieldErrors }, { status: 400 });
  }

  const posts = await db.posts.findMany(result.data);
  return NextResponse.json(posts);
}
```

## Middleware: Request Validation

```typescript
// middleware.ts
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";

const AuthTokenSchema = z.object({
  authorization: z.string().startsWith("Bearer ", "Authorization must be Bearer token"),
});

export async function middleware(req: NextRequest) {
  // Validate API routes require auth
  if (req.nextUrl.pathname.startsWith("/api/protected")) {
    const result = AuthTokenSchema.safeParse({
      authorization: req.headers.get("authorization") ?? undefined,
    });

    if (!result.success) {
      return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
    }

    // Validate token format, not the token itself (that's for the route handler)
  }

  return NextResponse.next();
}
```

## Environment Variable Validation

Validate `process.env` at module initialization — before any app code runs. Place in `lib/env.ts` and import it in root `layout.tsx` or `instrumentation.ts`:

```typescript
// lib/env.ts
import { z } from "zod";

const EnvSchema = z.object({
  // Database
  DATABASE_URL: z.url(),

  // Auth
  NEXTAUTH_URL: z.url(),
  NEXTAUTH_SECRET: z.string().min(32, "NEXTAUTH_SECRET must be at least 32 characters"),

  // External services
  STRIPE_SECRET_KEY: z.string().startsWith("sk_"),
  STRIPE_WEBHOOK_SECRET: z.string().startsWith("whsec_"),

  // Feature flags
  NEXT_PUBLIC_FEATURE_FLAGS: z.string().optional(),
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  PORT: z.coerce.number().int().default(3000),
});

// Throws on startup if any required env var is missing or malformed
export const env = EnvSchema.parse(process.env);
```

## Form Component with Client-Side Validation

Share the same schema between the Server Action and the React Hook Form resolver:

```typescript
// app/posts/create/page.tsx
"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useActionState } from "react";
import { CreatePostSchema } from "@/shared/schemas/post";
import { createPostAction } from "./actions";

export default function CreatePostPage() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(CreatePostSchema),
    defaultValues: { title: "", content: "", tags: [] },
  });

  // Client-side: zodResolver validates before even sending to server
  // Server-side: createPostAction validates again (defense in depth)
  const onSubmit = handleSubmit(async (data) => {
    const formData = new FormData();
    Object.entries(data).forEach(([k, v]) => {
      if (Array.isArray(v)) v.forEach(item => formData.append(k, item));
      else formData.append(k, v as string);
    });
    await createPostAction(formData);
  });

  return (
    <form onSubmit={onSubmit}>
      <input {...register("title")} />
      {errors.title && <span>{errors.title.message}</span>}

      <textarea {...register("content")} />
      {errors.content && <span>{errors.content.message}</span>}

      <button type="submit">Create Post</button>
    </form>
  );
}
```

## Common Anti-Patterns in Next.js + Zod

```typescript
// BAD: Direct req.json() cast without validation
export async function POST(req: NextRequest) {
  const body = (await req.json()) as CreatePostInput; // Unsafe cast
  await db.posts.create(body); // Unvalidated data reaches database
}

// BAD: .parse() in Server Action throws, crashes action, no user-visible error
export async function createPost(formData: FormData) {
  const data = CreatePostSchema.parse(Object.fromEntries(formData)); // Throws!
  // If invalid, user sees a generic "An error occurred" instead of field errors
}

// BAD: Different schemas for client and server validation — drift risk
// Client schema
const ClientSchema = z.object({ title: z.string().min(1) });
// Server schema (different file, gets out of sync)
const ServerSchema = z.object({ title: z.string().min(5) }); // Different minimum!

// GOOD: Import the same schema in both environments
import { CreatePostSchema } from "@/shared/schemas/post"; // Always the same schema
```
