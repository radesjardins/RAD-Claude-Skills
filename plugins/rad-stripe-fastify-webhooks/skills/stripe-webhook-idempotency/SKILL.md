---
name: stripe-webhook-idempotency
description: >
  This skill should be used when implementing idempotent webhook processing, handling
  "duplicate webhook events", "processed_events table", "idempotency key", "at-least-once delivery",
  "webhook deduplication", "event ID tracking", "reconciliation cron", "Stripe retry behavior",
  "crash-safe event processing", "atomic event recording", "webhook reliability patterns", or when
  the user asks how to prevent double-processing of Stripe webhook events.
---

# Idempotent Webhook Processing

## Why Idempotency Is Mandatory

Stripe guarantees **at-least-once delivery** — the same event may be sent multiple times. Without idempotency guards, duplicate events cause:
- Double-charging customers (if creating invoices)
- Double-sending emails
- Double-provisioning resources
- Corrupted subscription state

Idempotency is not optional. Every webhook handler must check before executing.

## The Processed Events Table

Track every successfully processed event by its Stripe event ID:

```sql
CREATE TABLE processed_events (
  event_id TEXT PRIMARY KEY,           -- Stripe event ID (evt_...)
  event_type TEXT NOT NULL,            -- e.g., 'invoice.paid'
  processed_at TEXT NOT NULL DEFAULT (datetime('now')),
  snapshot_event_id TEXT,              -- For thin events migration correlation
  payload_hash TEXT                    -- Optional: hash of key fields for debugging
);

CREATE INDEX idx_processed_events_type ON processed_events(event_type);
CREATE INDEX idx_processed_events_snapshot ON processed_events(snapshot_event_id)
  WHERE snapshot_event_id IS NOT NULL;
```

## The Critical Ordering Rule

Record the event ID **after** (or atomically with) the business logic. Never before.

### Wrong — Record First, Process Later

```typescript
// DANGEROUS: If we crash after INSERT but before updateSubscription,
// the event is marked "done" forever. Stripe retries will be ignored.
await db.run('INSERT INTO processed_events (event_id, event_type) VALUES (?, ?)',
  [event.id, event.type]);
await updateSubscription(event); // Crash here = permanent data loss
```

### Correct — Atomic Transaction

```typescript
const processEvent = db.transaction((event: Stripe.Event) => {
  // Check idempotency inside the transaction
  const existing = db.prepare(
    'SELECT 1 FROM processed_events WHERE event_id = ?'
  ).get(event.id);

  if (existing) return { skipped: true };

  // Execute business logic
  updateSubscriptionSync(event);

  // Record event ID — only if business logic succeeded
  db.prepare(
    'INSERT INTO processed_events (event_id, event_type) VALUES (?, ?)'
  ).run(event.id, event.type);

  return { skipped: false };
});

// Execute atomically
const result = processEvent(event);
if (result.skipped) {
  request.log.info({ eventId: event.id }, 'Duplicate event skipped');
}
```

For SQLite, use `BEGIN IMMEDIATE` to prevent the read-to-write upgrade deadlock. The `db.transaction()` helper in `better-sqlite3` does this automatically.

For PostgreSQL, wrap the check-and-process in a single transaction with `INSERT ... ON CONFLICT DO NOTHING` or use advisory locks.

## Thin Events Deduplication

During migration from snapshot to thin events, the same logical event may arrive twice — once as a snapshot event and once as a thin event. Deduplicate using the `snapshot_event` correlation field:

```typescript
function isAlreadyProcessed(
  eventId: string,
  snapshotEventId?: string
): boolean {
  if (snapshotEventId) {
    const row = db.prepare(
      'SELECT 1 FROM processed_events WHERE event_id = ? OR event_id = ? OR snapshot_event_id = ?'
    ).get(eventId, snapshotEventId, snapshotEventId);
    return !!row;
  }
  return !!db.prepare(
    'SELECT 1 FROM processed_events WHERE event_id = ?'
  ).get(eventId);
}
```

## Stripe Retry Behavior

When a webhook delivery fails (non-2xx response or timeout):

- Stripe retries for up to **3 days** using exponential backoff
- First retry: ~1 hour after initial failure
- Subsequent retries: increasing intervals
- After 3 days of failures, Stripe marks the endpoint as disabled

Return `200 OK` within a few seconds to prevent retries. If the handler needs more time, return 200 immediately and process asynchronously in a queue.

## Reconciliation Cron

Webhooks are push-based and can be lost (network issues, server downtime, bugs). Run a daily pull-based reconciliation:

```typescript
async function reconcileEvents() {
  // Fetch recent events from Stripe API
  const events = await stripe.events.list({
    created: { gte: Math.floor(Date.now() / 1000) - 86400 }, // Last 24 hours
    limit: 100,
  });

  for (const event of events.data) {
    const existing = db.prepare(
      'SELECT 1 FROM processed_events WHERE event_id = ?'
    ).get(event.id);

    if (!existing) {
      log.warn({ eventId: event.id, type: event.type }, 'Missed event detected');
      await dispatchEvent(event);
    }
  }
}

// Schedule daily
// cron: '0 3 * * *' — run at 3 AM
```

## Idempotency for Stripe API Calls (Outbound)

When creating Stripe objects from the application, use the `Idempotency-Key` header to prevent duplicate charges from retried requests:

```typescript
const session = await stripe.checkout.sessions.create(
  {
    mode: 'subscription',
    customer: customerId,
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: '...',
    cancel_url: '...',
  },
  {
    idempotencyKey: `checkout_${userId}_${priceId}_${Date.now()}`,
  }
);
```

Stripe caches the response for 24 hours. If the same idempotency key is sent again, Stripe returns the original response without creating a duplicate.

## Cleanup

Periodically clean up old processed event records to prevent unbounded table growth:

```sql
DELETE FROM processed_events
WHERE processed_at < datetime('now', '-90 days');
```

Run this in a scheduled job, not during webhook processing.
