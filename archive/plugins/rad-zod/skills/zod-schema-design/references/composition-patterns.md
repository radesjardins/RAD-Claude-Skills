# Zod Schema Composition Patterns

## Complete Pattern Reference

### Pattern 1: Base Schema + Derived DTOs

The canonical pattern for API development — one base schema, multiple derived shapes:

```typescript
// Base schema — complete domain model
const UserSchema = z.strictObject({
  id: z.string().uuid(),
  email: z.email(),
  password: z.string().min(12),
  role: z.enum(["admin", "user", "moderator"]),
  bio: z.string().max(500).nullable(),
  createdAt: z.date(),
  updatedAt: z.date(),
});

// POST /users — create endpoint (client provides email, password, optional bio)
const CreateUserSchema = UserSchema.pick({ email: true, password: true, bio: true })
  .extend({ bio: z.string().max(500).nullable().default(null) });

// GET /users/:id response — never expose password
const PublicUserSchema = UserSchema.omit({ password: true });

// PATCH /users/:id — all fields optional, NO defaults (prevent data loss)
const PatchUserSchema = z.strictObject({
  email: z.email().optional(),
  bio: z.string().max(500).nullable().optional(),
  role: z.enum(["admin", "user", "moderator"]).optional(),
});
// Note: Built fresh, not derived from UserSchema.partial() — avoids default injection

// Admin-only view
const AdminUserSchema = UserSchema; // Full schema with all fields
```

### Pattern 2: Extending Without Merge (Zod 4)

```typescript
const BaseEventSchema = z.object({
  id: z.string().uuid(),
  timestamp: z.date(),
  source: z.string(),
});

// Extend with shape destructuring (best TypeScript performance)
const ClickEventSchema = z.object({
  ...BaseEventSchema.shape,
  type: z.literal("click"),
  x: z.number(),
  y: z.number(),
  target: z.string(),
});

// Extend with .extend() (good, preferred over .merge())
const KeydownEventSchema = BaseEventSchema.extend({
  type: z.literal("keydown"),
  key: z.string(),
  modifiers: z.array(z.enum(["ctrl", "alt", "shift", "meta"])),
});
```

### Pattern 3: Intersections for Refined Schema Merging

```typescript
const HasTimestamps = z.object({
  createdAt: z.date(),
  updatedAt: z.date(),
}).refine(d => d.updatedAt >= d.createdAt, "updatedAt must be after createdAt");

const HasOwner = z.object({
  ownerId: z.string().uuid(),
}).refine(d => d.ownerId.length > 0, "Owner required");

// Intersection preserves BOTH refinements
const OwnedDocument = z.intersection(HasTimestamps, HasOwner).extend({
  title: z.string(),
  content: z.string(),
});
```

### Pattern 4: Discriminated Union for State Machines

```typescript
const AsyncStateSchema = z.discriminatedUnion("status", [
  z.object({
    status: z.literal("idle"),
  }),
  z.object({
    status: z.literal("loading"),
    startedAt: z.date(),
  }),
  z.object({
    status: z.literal("success"),
    data: z.unknown(),
    completedAt: z.date(),
  }),
  z.object({
    status: z.literal("error"),
    error: z.string(),
    failedAt: z.date(),
  }),
]);

type AsyncState = z.infer<typeof AsyncStateSchema>;
// Narrowing works perfectly:
// if (state.status === "success") { state.data; state.completedAt; }
```

### Pattern 5: Nested Discriminated Unions

Zod 4 supports discriminated unions inside other discriminated unions:

```typescript
const NotificationSchema = z.discriminatedUnion("channel", [
  z.object({
    channel: z.literal("email"),
    payload: z.discriminatedUnion("type", [
      z.object({ type: z.literal("welcome"), recipientEmail: z.email() }),
      z.object({ type: z.literal("reset"), token: z.string(), expiresAt: z.date() }),
    ]),
  }),
  z.object({
    channel: z.literal("sms"),
    payload: z.object({ phoneNumber: z.string(), message: z.string().max(160) }),
  }),
]);
```

### Pattern 6: Records and Maps

```typescript
// Record with enum keys
const PermissionsSchema = z.record(
  z.enum(["read", "write", "delete", "admin"]),
  z.boolean()
);

// Record with string keys, validated values
const MetadataSchema = z.record(z.string(), z.union([z.string(), z.number(), z.boolean()]));

// Typed map (object with known structure)
const LocaleStringsSchema = z.record(
  z.string().regex(/^[a-z]{2}(-[A-Z]{2})?$/), // e.g., "en", "en-US"
  z.string()
);
```

### Pattern 7: Tuples for Fixed-Length Arrays

```typescript
// Route coordinate: [longitude, latitude]
const CoordinateSchema = z.tuple([
  z.number().min(-180).max(180), // longitude
  z.number().min(-90).max(90),   // latitude
]);

// With rest parameter
const AtLeastOneNumberSchema = z.tuple([z.number()]).rest(z.number());
```

### Pattern 8: Pipeline for Multi-Stage Validation

```typescript
// Parse a date string from a form, validate it's in the future
const FutureDateSchema = z.string()
  .regex(/^\d{4}-\d{2}-\d{2}$/, "Must be YYYY-MM-DD")
  .pipe(z.coerce.date())
  .refine(d => d > new Date(), "Date must be in the future");

// Parse CSV row
const CsvRowSchema = z.string()
  .transform(s => s.split(","))
  .pipe(z.tuple([z.string(), z.coerce.number(), z.coerce.boolean()]));
```

### Pattern 9: Reusable Schema Factories

For schemas that share shape but need different constraints in different contexts:

```typescript
function paginationSchema(maxLimit = 100) {
  return z.object({
    page: z.coerce.number().int().min(1).default(1),
    limit: z.coerce.number().int().min(1).max(maxLimit).default(20),
    sortBy: z.string().optional(),
    sortDir: z.enum(["asc", "desc"]).default("asc"),
  });
}

const PublicPaginationSchema = paginationSchema(100);    // limit ≤ 100
const AdminPaginationSchema = paginationSchema(10000);   // limit ≤ 10000
```

Note: These factory functions return new schema instances each call. Hoist the returned schemas to module scope if used in hot paths.

### Pattern 10: Conditional Refinements

```typescript
const TransferSchema = z.object({
  amount: z.number().positive(),
  currency: z.enum(["USD", "EUR", "GBP"]),
  recipient: z.string(),
  note: z.string().optional(),
  requiresApproval: z.boolean().default(false),
}).refine(
  d => !(d.amount > 10000 && !d.requiresApproval),
  { message: "Transfers over $10,000 require approval", path: ["requiresApproval"] }
);
```
