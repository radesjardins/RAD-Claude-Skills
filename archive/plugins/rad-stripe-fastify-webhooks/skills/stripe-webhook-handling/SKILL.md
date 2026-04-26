---
name: stripe-webhook-handling
description: >
  This skill should be used when implementing Stripe webhook endpoints in Fastify, handling
  "Stripe signature verification", "raw body access in Fastify", "stripe.webhooks.constructEvent",
  "Stripe-Signature header", "thin events", "snapshot events", "webhook route setup",
  "preParsing hook for webhooks", "Stripe event routing", "webhook event dispatch", or when
  the user asks how to receive and verify Stripe webhooks in a Fastify application.
---

# Stripe Webhook Handling in Fastify

## Core Invariant: Raw Body Before Everything

Stripe webhook signature verification requires the **exact bytes** that Stripe sent. If any middleware or framework feature parses, re-serializes, or transforms the body before verification, the HMAC check fails silently and the webhook is rejected as invalid.

In Fastify, this means the webhook route must capture `req.rawBody` before Fastify's default JSON content-type parser runs.

## Webhook Route Setup

### Step 1: Enable Raw Body Access

Configure Fastify to preserve the raw body on webhook routes. Two approaches:

**Option A — addContentTypeParser override (recommended):**

```typescript
async function webhookRoutes(fastify: FastifyInstance) {
  // Override content-type parser for this encapsulated context only
  fastify.addContentTypeParser(
    'application/json',
    { parseAs: 'buffer' },
    (req, body, done) => {
      // Preserve raw bytes for signature verification
      (req as any).rawBody = body;
      try {
        done(null, JSON.parse(body.toString()));
      } catch (err) {
        done(err as Error, undefined);
      }
    }
  );

  fastify.post('/stripe', stripeWebhookHandler);
}
```

**Option B — fastify-raw-body plugin:**

```typescript
import rawBody from 'fastify-raw-body';

fastify.register(rawBody, {
  field: 'rawBody',
  global: false,        // Only on routes that need it
  encoding: 'utf8',
  runFirst: true,
});
```

### Step 2: Verify Signature and Construct Event

```typescript
import Stripe from 'stripe';
import type { FastifyRequest, FastifyReply } from 'fastify';

const stripe = new Stripe(env.STRIPE_SECRET_KEY);

async function stripeWebhookHandler(
  request: FastifyRequest,
  reply: FastifyReply
) {
  const sig = request.headers['stripe-signature'];
  const rawBody = (request as any).rawBody;

  if (!sig || !rawBody) {
    return reply.status(400).send({ error: 'Missing signature or body' });
  }

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      rawBody,
      sig,
      env.STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    request.log.warn({ err }, 'Webhook signature verification failed');
    return reply.status(400).send({ error: 'Invalid signature' });
  }

  // Return 200 immediately — process asynchronously
  reply.status(200).send({ received: true });

  // Dispatch to event handlers (fire-and-forget or queue)
  await dispatchEvent(event);
}
```

### Step 3: Dispatch Events by Type

Route verified events to their handlers using a type-safe dispatch map:

```typescript
const eventHandlers: Record<string, (event: Stripe.Event) => Promise<void>> = {
  'checkout.session.completed': handleCheckoutCompleted,
  'customer.subscription.created': handleSubscriptionCreated,
  'customer.subscription.updated': handleSubscriptionUpdated,
  'customer.subscription.deleted': handleSubscriptionDeleted,
  'invoice.paid': handleInvoicePaid,
  'invoice.payment_failed': handlePaymentFailed,
};

async function dispatchEvent(event: Stripe.Event): Promise<void> {
  const handler = eventHandlers[event.type];
  if (!handler) {
    // Log unhandled event types but do not fail
    return;
  }
  await handler(event);
}
```

## Thin Events vs. Snapshot Events

### Snapshot Events (Legacy Default)

The webhook payload contains the full object at the time the event was created. Risk: the object may have changed between event creation and delivery.

### Thin Events (Recommended)

The payload contains only the event `type` and object `id`. The handler fetches the latest state from the Stripe API:

```typescript
async function handleThinEvent(event: StripeThinEvent) {
  // Fetch the current state — always up-to-date
  const subscription = await stripe.subscriptions.retrieve(event.data.id);
  await updateLocalSubscription(subscription);
}
```

### Migration Interop

During migration, the same logical event may arrive as both a snapshot event and a thin event. Use the `snapshot_event` correlation field to deduplicate:

```typescript
// Check if the corresponding snapshot event was already processed
const existing = db.prepare(
  'SELECT 1 FROM processed_events WHERE event_id = ? OR snapshot_event_id = ?'
).get(event.id, event.snapshot_event_id);

if (existing) return; // Already handled
```

## Encapsulation: Why a Separate Plugin

Webhook routes must skip global JSON body parsing — they need raw bytes. By registering webhook routes in a separate encapsulated Fastify plugin, the custom content-type parser applies only to those routes. The rest of the application continues to use standard JSON parsing.

Never register the raw body parser at the root Fastify instance — it would affect every route in the application.

## Error Handling

- **Invalid signature:** Return `400`. Log a warning (never log the raw body or signature secret).
- **Unknown event type:** Return `200`. Stripe should not retry events the handler does not process.
- **Handler failure:** Return `200` anyway if the event was queued. If processing inline, return `500` so Stripe retries (but prefer async processing).
- **Stripe API failure (thin events):** Retry with exponential backoff. If persistent, queue for the reconciliation cron.

## Additional Resources

### Reference Files

- **`references/thin-events-migration.md`** — Complete thin events migration guide with interop handling

### Related Skills

- **stripe-webhook-idempotency** — For the deduplication strategy when processing thin events and handling duplicates
- **stripe-subscription-lifecycle** — For the complete event-to-database field mapping and state machine transitions
