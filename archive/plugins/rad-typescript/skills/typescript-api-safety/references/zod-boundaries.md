# Zod at API Boundaries: Advanced Patterns

## Schema Composition

```typescript
import { z } from 'zod';

// Base schemas — compose into larger schemas
const TimestampsSchema = z.object({
  createdAt: z.coerce.date(),
  updatedAt: z.coerce.date(),
});

const PaginationSchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  pageSize: z.coerce.number().int().min(1).max(100).default(20),
});

// Extend base schemas
const UserSchema = TimestampsSchema.extend({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1).max(100).trim(),
  role: z.enum(['admin', 'user', 'moderator']),
});

// Create request/response variants from one schema
const CreateUserSchema = UserSchema.omit({ id: true, createdAt: true, updatedAt: true });
const UpdateUserSchema = UserSchema.omit({ id: true, createdAt: true, updatedAt: true }).partial();
const UserResponseSchema = UserSchema.omit({ /* sensitive fields */ });

// Type derivation
type User = z.infer<typeof UserSchema>;
type CreateUser = z.infer<typeof CreateUserSchema>;
type UpdateUser = z.infer<typeof UpdateUserSchema>;
```

## Coercion Patterns

```typescript
// Coerce query params (always strings from URL)
const QuerySchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  active: z.coerce.boolean().default(true), // "true" → true
  date: z.coerce.date(),                    // "2024-01-01" → Date
});

// Transform during parsing
const SearchSchema = z.object({
  q: z.string().trim().min(1).transform(s => s.toLowerCase()),
  tags: z
    .string()
    .transform(s => s.split(','))
    .pipe(z.array(z.string().min(1))),
});
```

## Error Formatting

```typescript
import { z, ZodError } from 'zod';

// Flatten errors for API responses
function formatZodError(error: ZodError): Record<string, string[]> {
  return error.flatten().fieldErrors as Record<string, string[]>;
}

// Usage in request handler
const result = CreateUserSchema.safeParse(body);
if (!result.success) {
  return reply.status(400).send({
    error: 'VALIDATION_FAILED',
    details: formatZodError(result.error),
  });
}
```

## Discriminated Unions in Zod

```typescript
const EventSchema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('user.created'),
    payload: z.object({ userId: z.string().uuid(), email: z.string().email() }),
  }),
  z.object({
    type: z.literal('order.placed'),
    payload: z.object({ orderId: z.string().uuid(), total: z.number().positive() }),
  }),
  z.object({
    type: z.literal('payment.failed'),
    payload: z.object({ orderId: z.string().uuid(), reason: z.string() }),
  }),
]);

type AppEvent = z.infer<typeof EventSchema>;
// TypeScript union type with discriminant 'type' — narrows perfectly
```

## Custom Validators

```typescript
// Brand types for domain safety
const BrandedIdSchema = z.string().uuid().brand<'UserId'>();
type UserId = z.infer<typeof BrandedIdSchema>; // string & { __brand: 'UserId' }

// Custom refinement
const PasswordSchema = z.string()
  .min(8, 'At least 8 characters')
  .regex(/[A-Z]/, 'Must contain uppercase')
  .regex(/[0-9]/, 'Must contain digit')
  .regex(/[!@#$%^&*]/, 'Must contain special character');

// Cross-field validation with superRefine
const SignupSchema = z.object({
  password: PasswordSchema,
  confirmPassword: z.string(),
}).superRefine(({ password, confirmPassword }, ctx) => {
  if (password !== confirmPassword) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['confirmPassword'],
      message: 'Passwords do not match',
    });
  }
});
```

## Async Validation

```typescript
// Async refinement (e.g., uniqueness check)
const UniqueEmailSchema = z.string().email().superRefine(async (email, ctx) => {
  const exists = await db.users.exists({ email });
  if (exists) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'Email already registered',
    });
  }
});

// Use parseAsync for async schemas
const result = await UniqueEmailSchema.safeParseAsync(body.email);
```

## Performance: Define Schemas Outside Loops

```typescript
// ❌ Wrong — schema re-instantiated on every call
async function processItems(items: unknown[]) {
  return items.map(item => {
    const schema = z.object({ id: z.string(), value: z.number() }); // Re-created each iteration!
    return schema.safeParse(item);
  });
}

// ✅ Correct — schema defined once
const ItemSchema = z.object({ id: z.string(), value: z.number() });

async function processItems(items: unknown[]) {
  return items.map(item => ItemSchema.safeParse(item));
}
```

## Versioned API Schemas

```typescript
// Maintain backward-compatible schema evolution
const UserV1Schema = z.object({ id: z.string(), name: z.string() });
const UserV2Schema = UserV1Schema.extend({ email: z.string().email() });

// Auto-migrate V1 → V2
function migrateUser(data: unknown): z.infer<typeof UserV2Schema> {
  const v1 = UserV1Schema.parse(data);
  return { ...v1, email: '' }; // Provide default for new field
}
```
