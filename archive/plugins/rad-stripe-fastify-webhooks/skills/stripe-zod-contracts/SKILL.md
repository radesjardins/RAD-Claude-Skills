---
name: stripe-zod-contracts
description: >
  This skill should be used when defining Zod schemas for Stripe webhook handling, implementing
  "Zod type provider with Fastify", "webhook payload schema", "Stripe event Zod validation",
  "z.discriminatedUnion for events", "config schema with Zod", "env validation Zod",
  "z.infer for Stripe types", "Zod response schema", "request validation schema",
  "fastify-type-provider-zod setup", "Stripe webhook Zod", "billing Zod schemas", or when
  the user asks how to define type-safe validation contracts for Stripe-related Fastify routes.
---

# Zod Contracts for Stripe Webhook Handling

## Core Principle: Schemas Are the Single Source of Truth

Zod schemas define both runtime validation AND TypeScript types. Never write a separate TypeScript interface for data that has a Zod schema — use `z.infer<typeof schema>` instead. Export the schemas, not the types.

## Fastify Type Provider Setup

Install and configure `fastify-type-provider-zod` so that Zod schemas on routes automatically infer request/response types:

```typescript
import Fastify from 'fastify';
import {
  serializerCompiler,
  validatorCompiler,
  type ZodTypeProvider,
} from 'fastify-type-provider-zod';

const app = Fastify();
app.setValidatorCompiler(validatorCompiler);
app.setSerializerCompiler(serializerCompiler);

// All routes registered on this instance get Zod type inference
const typedApp = app.withTypeProvider<ZodTypeProvider>();
```

## Webhook-Specific Schemas

### The Webhook Route Exception

The webhook POST route does NOT use standard Zod body validation because:
1. The raw body must be preserved for signature verification
2. Zod validation would require parsing the body first, breaking the HMAC

Instead, validate the event AFTER signature verification:

```typescript
import { z } from 'zod';

// Validated after constructEvent() succeeds
const stripeEventSchema = z.object({
  id: z.string().startsWith('evt_'),
  type: z.string(),
  data: z.object({
    object: z.record(z.unknown()),
  }),
  created: z.number(),
});

type StripeEventParsed = z.infer<typeof stripeEventSchema>;
```

### Discriminated Union for Event Types

Use `z.discriminatedUnion` on the `type` field for type-safe event dispatch:

```typescript
const subscriptionEventSchema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('customer.subscription.created'),
    data: z.object({ object: subscriptionObjectSchema }),
  }),
  z.object({
    type: z.literal('customer.subscription.updated'),
    data: z.object({ object: subscriptionObjectSchema }),
  }),
  z.object({
    type: z.literal('customer.subscription.deleted'),
    data: z.object({ object: subscriptionObjectSchema }),
  }),
  z.object({
    type: z.literal('invoice.paid'),
    data: z.object({ object: invoiceObjectSchema }),
  }),
  z.object({
    type: z.literal('invoice.payment_failed'),
    data: z.object({ object: invoiceObjectSchema }),
  }),
]);

type SubscriptionEvent = z.infer<typeof subscriptionEventSchema>;
```

This is more efficient than `z.union` — it checks the `type` discriminator first, then validates only the matching branch.

## Environment Config Schema

Validate all configuration at startup:

```typescript
export const envSchema = z.object({
  // Stripe
  STRIPE_SECRET_KEY: z.string().regex(/^sk_(test|live)_/, 'Invalid Stripe secret key format'),
  STRIPE_WEBHOOK_SECRET: z.string().startsWith('whsec_', 'Invalid webhook secret format'),

  // Database
  DATABASE_URL: z.string().min(1, 'DATABASE_URL is required'),

  // Auth
  JWT_SECRET: z.string().min(32, 'JWT_SECRET must be at least 32 characters'),
  JWT_ISSUER: z.string().url().optional(),
  JWT_AUDIENCE: z.string().optional(),

  // Server
  PORT: z.coerce.number().int().min(1).max(65535).default(3000),
  HOST: z.string().default('0.0.0.0'),
  NODE_ENV: z.enum(['development', 'staging', 'production']).default('development'),

  // Rate limiting
  RATE_LIMIT_MAX: z.coerce.number().int().positive().default(1000),
  RATE_LIMIT_WINDOW: z.string().default('1 minute'),
});

export type Env = z.infer<typeof envSchema>;
```

## API Route Schemas

For protected billing API routes (NOT webhooks), use full Zod validation:

### Request Schemas

```typescript
// POST /api/v1/billing/checkout
export const createCheckoutSchema = {
  body: z.object({
    priceId: z.string().startsWith('price_'),
    successUrl: z.string().url(),
    cancelUrl: z.string().url(),
  }),
  response: {
    200: z.object({
      sessionUrl: z.string().url(),
    }),
  },
};

// GET /api/v1/billing/subscription
export const getSubscriptionSchema = {
  response: {
    200: z.object({
      planName: z.string(),
      status: z.enum([
        'trialing', 'active', 'past_due', 'canceled',
        'unpaid', 'incomplete', 'incomplete_expired', 'paused',
      ]),
      currentPeriodEnd: z.number(),
      cancelAtPeriodEnd: z.boolean(),
      // stripe_customer_id NOT exposed — internal only
    }),
  },
};
```

### Pagination Schema (Reusable)

```typescript
export const paginationSchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});
```

### PATCH Schema Pattern (Sparse Updates)

```typescript
export const updateSubscriptionSchema = {
  body: z.object({
    cancelAtPeriodEnd: z.boolean().optional(),
    newPriceId: z.string().startsWith('price_').optional(),
  }).refine(
    (data) => Object.keys(data).length > 0,
    { message: 'At least one field must be provided' }
  ),
};
```

## Type Export Pattern

Export schemas, derive types with `z.infer`:

```typescript
// schemas.ts — export these
export const subscriptionSchema = z.object({ /* ... */ });
export const entitlementSchema = z.object({ /* ... */ });
export const checkoutRequestSchema = z.object({ /* ... */ });

// Types derived from schemas — export these too
export type Subscription = z.infer<typeof subscriptionSchema>;
export type Entitlement = z.infer<typeof entitlementSchema>;
export type CheckoutRequest = z.infer<typeof checkoutRequestSchema>;
```

## What Should Never Be Trusted from the Client

- Entitlement claims (always compute server-side)
- Subscription status (always read from local DB)
- Price IDs without server-side validation against known plans
- User IDs from request body (use `request.user.id` from JWT)
- Any field that determines billing amounts or access levels

## Transform and Coerce Patterns

Use `z.coerce` for query parameters (which arrive as strings):

```typescript
const querySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  status: z.enum(['active', 'canceled', 'all']).default('all'),
});
```

Use `z.transform` for data normalization:

```typescript
const emailSchema = z.string().email().transform((s) => s.toLowerCase().trim());
```

Use `z.preprocess` for complex input coercion:

```typescript
const timestampSchema = z.preprocess(
  (val) => typeof val === 'string' ? new Date(val).getTime() / 1000 : val,
  z.number().int().positive()
);
```
