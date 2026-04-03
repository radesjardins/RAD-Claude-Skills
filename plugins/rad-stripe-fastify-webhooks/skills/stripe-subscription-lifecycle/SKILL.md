---
name: stripe-subscription-lifecycle
description: >
  This skill should be used when implementing Stripe subscription management, handling
  "subscription state machine", "subscription status transitions", "Stripe subscription lifecycle",
  "trialing to active", "past_due handling", "subscription canceled", "grace period logic",
  "entitlement checks", "feature gating by plan", "customer.subscription.updated handler",
  "invoice.paid handler", "dunning flow", "subscription downgrade", or when the user asks
  how to manage subscription states and entitlements in a Fastify SaaS application.
---

# Stripe Subscription Lifecycle Management

## The Subscription State Machine

Stripe subscriptions transition through these statuses. The local database must mirror these transitions via webhook events.

```
                    ┌─────────────┐
          ┌────────►│  trialing   │
          │         └──────┬──────┘
          │                │ trial ends + payment succeeds
          │                ▼
  created │         ┌─────────────┐    payment fails    ┌──────────────┐
  ────────┤         │   active    │───────────────────►│  past_due    │
          │         └──────┬──────┘                     └──────┬───────┘
          │                │                                    │
          │                │ cancel requested                   │ all retries fail
          │                ▼                                    ▼
          │         ┌─────────────┐                     ┌──────────────┐
          └────────►│  canceled   │                     │   unpaid     │
                    └─────────────┘                     └──────────────┘
```

Additional statuses: `incomplete` (initial payment pending, 23-hour window), `incomplete_expired` (initial payment never completed), `paused`.

## Authoritative Events and Their Actions

### `checkout.session.completed`

Fires when a customer completes Stripe Checkout. This is the entry point for new subscriptions and one-time payments.

**Action:** Create the subscription record in the local database. Provision initial access. If `payment_behavior=default_incomplete`, wait for `invoice.paid` before granting full access.

### `customer.subscription.created`

Fires when the subscription object is first created in Stripe.

**Action:** Initialize the subscription record with status, plan, and period dates. If status is `trialing`, grant trial-level access.

### `customer.subscription.updated`

Fires on any subscription change: plan change, status transition, period renewal, cancel scheduling.

**Action:** Update the local record. Key fields to sync: `status`, `current_period_start`, `current_period_end`, `cancel_at_period_end`, `items[].price.id`. If the plan changed, update the entitlement mapping.

### `customer.subscription.deleted`

Fires when the subscription is fully terminated (not just `cancel_at_period_end`).

**Action:** Revoke access. Mark the subscription as canceled in the local database. Clean up any associated resources.

### `invoice.paid`

Fires when a recurring invoice is successfully paid.

**Action:** Extend access through the new period. Reset any dunning/grace period state. Update `current_period_end`.

### `invoice.payment_failed`

Fires when a recurring payment attempt fails.

**Action:** Begin the dunning flow. Start an internal grace period (3–5 days). Notify the customer to update their payment method. Do NOT immediately lock features.

### `customer.source.expiring`

Fires 30 days before a card expires.

**Action:** Send a proactive notification to the customer to update their payment method before the next charge fails.

## Entitlement Engine Pattern

Never call the Stripe API to check what a user can do. Query the local database:

```typescript
interface Entitlement {
  planName: string;
  maxUsers: number;
  maxStorageMb: number;
  features: string[];
  isActive: boolean;
  gracePeriodEnd: number | null;
}

function getEntitlement(userId: string): Entitlement {
  const row = db.prepare(`
    SELECT
      pd.plan_name, pd.max_users, pd.max_storage_mb, pd.features,
      s.status, s.grace_period_end, s.current_period_end
    FROM subscriptions s
    JOIN plan_definitions pd ON pd.stripe_price_id = s.stripe_price_id
    WHERE s.user_id = ?
  `).get(userId);

  if (!row) return defaultFreeEntitlement();

  const isActive = ['active', 'trialing'].includes(row.status)
    || (row.status === 'past_due' && row.grace_period_end > Date.now() / 1000);

  return {
    planName: row.plan_name,
    maxUsers: row.max_users,
    maxStorageMb: row.max_storage_mb,
    features: JSON.parse(row.features),
    isActive,
    gracePeriodEnd: row.grace_period_end,
  };
}
```

## Grace Period Implementation

When `invoice.payment_failed` fires:

1. Set `grace_period_end` to `now + GRACE_DAYS` (e.g., 3–5 days)
2. Continue granting access while `Date.now() < grace_period_end`
3. When `invoice.paid` fires, clear the grace period
4. When `grace_period_end` passes without payment, lock features
5. When Stripe exhausts all retries and sets `unpaid`, fully revoke

```typescript
async function handlePaymentFailed(event: Stripe.Event) {
  const invoice = event.data.object as Stripe.Invoice;
  const graceDays = 5;
  const graceEnd = Math.floor(Date.now() / 1000) + graceDays * 86400;

  await db.run(`
    UPDATE subscriptions
    SET grace_period_end = ?, updated_at = datetime('now')
    WHERE stripe_subscription_id = ?
  `, [graceEnd, invoice.subscription]);

  // Queue customer notification email
  await notificationQueue.add('payment_failed', {
    customerId: invoice.customer,
    gracePeriodEnd: graceEnd,
  });
}
```

## Prehandler Entitlement Check

Enforce plan limits in the Fastify `preHandler` hook:

```typescript
fastify.addHook('preHandler', async (request, reply) => {
  const entitlement = getEntitlement(request.user.id);

  if (!entitlement.isActive) {
    return reply.status(403).send({
      error: 'subscription_inactive',
      message: 'Your subscription is not active.',
    });
  }

  // Attach for downstream handlers
  request.entitlement = entitlement;
});
```

## Out-of-Order Event Handling

Stripe guarantees at-least-once delivery but NOT chronological order. A `customer.subscription.deleted` event can arrive before `customer.subscription.updated`.

**Mitigation strategies:**
- Use the Thin Events pattern — always fetch the latest state from Stripe
- Compare `event.created` timestamps before overwriting local state
- Use a deterministic state machine that rejects invalid transitions
- The reconciliation cron catches any events that arrive out of order

## Additional Resources

### Reference Files

- **`references/event-field-mapping.md`** — Complete field mapping for each authoritative event to local database columns

### Related Skills

- **stripe-webhook-idempotency** — For the `processed_events` table pattern and atomic event recording
- **stripe-webhook-handling** — For signature verification and thin events fetch pattern
- **stripe-webhook-security** — For rate limiting and log redaction in billing contexts
