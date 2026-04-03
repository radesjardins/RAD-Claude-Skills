# Architecture Patterns: Stripe Webhooks with Fastify & Zod

## Fastify Plugin Registration Pattern

Register the billing plugin as an encapsulated async Fastify plugin:

```typescript
import fp from 'fastify-plugin';
import type { FastifyInstance } from 'fastify';

async function billingPlugin(fastify: FastifyInstance) {
  // Register webhook routes with raw body parsing
  fastify.register(webhookRoutes, { prefix: '/webhooks' });

  // Register protected billing API routes
  fastify.register(billingApiRoutes, { prefix: '/api/v1/billing' });
}

// Do NOT wrap with fp() — keep encapsulated
export default billingPlugin;
```

**When to use `fastify-plugin` (fp):** Only when the plugin needs to share decorators or hooks with sibling contexts. Billing plugins should NOT use fp — they should remain encapsulated.

## Lifecycle Hook Boundaries

```
Request arrives
  │
  ├── onRequest → JWT validation (reject unauthenticated, cheapest check)
  │                Exception: webhook routes skip this — they use signature verification
  │
  ├── preParsing → For webhook routes: capture raw body before JSON parsing
  │
  ├── preValidation → Zod schema validation (automatic via type provider)
  │
  ├── preHandler → Authorization checks, entitlement verification
  │                 Check: does this user's plan allow this action?
  │
  ├── handler → Business logic (keep thin — delegate to service layer)
  │
  ├── preSerialization → Response schema filters sensitive fields
  │
  └── onClose → Graceful shutdown (drain DB connections, flush queues)
```

## Config Namespace Pattern

Validate all environment variables at startup with Zod:

```typescript
import { z } from 'zod';

const envSchema = z.object({
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  STRIPE_WEBHOOK_SECRET: z.string().startsWith('whsec_'),
  DATABASE_URL: z.string().min(1),
  JWT_SECRET: z.string().min(32),
  NODE_ENV: z.enum(['development', 'staging', 'production']).default('development'),
});

type Env = z.infer<typeof envSchema>;

// Validate at startup — fail fast if misconfigured
const env = envSchema.parse(process.env);
```

Register via `@fastify/env` or validate manually in the plugin's `onReady` hook. Never let the app start with missing secrets.

## Database Schema for Webhook Processing

### Subscriptions Table

```sql
CREATE TABLE subscriptions (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id),
  stripe_subscription_id TEXT UNIQUE NOT NULL,
  stripe_customer_id TEXT NOT NULL,
  stripe_price_id TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN (
    'trialing', 'active', 'past_due', 'canceled',
    'unpaid', 'incomplete', 'incomplete_expired', 'paused'
  )),
  current_period_start INTEGER NOT NULL,
  current_period_end INTEGER NOT NULL,
  cancel_at_period_end INTEGER NOT NULL DEFAULT 0,
  grace_period_end INTEGER,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
```

### Processed Events Table (Idempotency)

```sql
CREATE TABLE processed_events (
  event_id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  processed_at TEXT NOT NULL DEFAULT (datetime('now')),
  snapshot_event_id TEXT  -- For thin events migration correlation
);

CREATE INDEX idx_processed_events_type ON processed_events(event_type);
```

### Entitlements Table

```sql
CREATE TABLE plan_definitions (
  stripe_price_id TEXT PRIMARY KEY,
  plan_name TEXT NOT NULL,
  max_users INTEGER NOT NULL DEFAULT 1,
  max_storage_mb INTEGER NOT NULL DEFAULT 100,
  features TEXT NOT NULL DEFAULT '[]'  -- JSON array of feature flags
);
```

## Addon Stacking Pattern

Instead of creating separate Stripe products for every feature combination, use a single Stripe Product per addon and vary the `quantity`. The backend computes the effective limit:

```typescript
function computeEffectiveLimit(
  basePlan: PlanDefinition,
  addons: Addon[]
): number {
  return basePlan.maxUsers + addons
    .filter(a => a.type === 'extra_users')
    .reduce((sum, a) => sum + a.quantity, 0);
}
```

## Trial Independence Pattern

Model trials in the local database, not exclusively in Stripe. This allows:
- Trial countdowns independent of Stripe state
- Trial extensions without Stripe API calls
- Feature-gating during trials from local data
- Stripe is only introduced at checkout/upgrade

## Downgrade Scheduling

When handling plan downgrade webhooks, apply the downgrade at the next billing cycle — not immediately. This prevents mid-cycle feature loss:

```typescript
if (newPlan.tier < currentPlan.tier) {
  // Schedule downgrade for period end
  await db.run(`
    UPDATE subscriptions
    SET pending_downgrade_price_id = ?,
        pending_downgrade_at = current_period_end
    WHERE stripe_subscription_id = ?
  `, [newPriceId, subscriptionId]);
} else {
  // Upgrades apply immediately
  await updatePlanNow(subscriptionId, newPriceId);
}
```

## SQLite Production Configuration

For SQLite-backed SaaS, set these PRAGMAs at connection time:

```typescript
const db = new Database('./data/app.db');
db.pragma('journal_mode = WAL');
db.pragma('busy_timeout = 5000');
db.pragma('synchronous = NORMAL');
db.pragma('foreign_keys = ON');
db.pragma('cache_size = -64000'); // 64MB
```

WAL mode enables concurrent readers with a single writer. `busy_timeout` prevents immediate `SQLITE_BUSY` errors by waiting up to 5 seconds for the write lock. Use `BEGIN IMMEDIATE` for any transaction that will write, to avoid the read-to-write upgrade deadlock.
