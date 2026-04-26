# Thin Events Migration Guide

## Overview

Stripe is transitioning from "snapshot events" (full object in payload) to "thin events" (only event type + object ID). This guide covers the migration path and interop handling.

## Snapshot Events (Legacy)

The webhook payload contains the full Stripe object at the time the event was created:

```json
{
  "id": "evt_1234",
  "type": "customer.subscription.updated",
  "data": {
    "object": {
      "id": "sub_abc123",
      "status": "active",
      "current_period_end": 1735689600,
      "items": { "data": [{ "price": { "id": "price_xyz" } }] }
    }
  }
}
```

**Risk:** The object may have changed between event creation and delivery. If two events for the same subscription arrive out of order, acting on stale snapshot data corrupts local state.

## Thin Events (Recommended)

The payload contains only the event metadata:

```json
{
  "id": "evt_thin_5678",
  "type": "v1.customer.subscription.updated",
  "data": {
    "id": "sub_abc123"
  },
  "snapshot_event": "evt_1234"
}
```

The handler must fetch the current state from the Stripe API:

```typescript
async function handleThinSubscriptionEvent(event: StripeThinEvent) {
  const subscriptionId = event.data.id;

  // Always fetch the latest — immune to delivery order
  const subscription = await stripe.subscriptions.retrieve(subscriptionId);

  await db.transaction(() => {
    // Check idempotency using both thin event ID and snapshot correlation
    const existing = db.prepare(`
      SELECT 1 FROM processed_events
      WHERE event_id = ? OR snapshot_event_id = ?
    `).get(event.id, event.snapshot_event);

    if (existing) return;

    // Update local state from the fetched (current) object
    db.prepare(`
      UPDATE subscriptions SET
        status = ?,
        stripe_price_id = ?,
        current_period_end = ?,
        updated_at = datetime('now')
      WHERE stripe_subscription_id = ?
    `).run(
      subscription.status,
      subscription.items.data[0].price.id,
      subscription.current_period_end,
      subscription.id
    );

    // Record both event IDs for deduplication
    db.prepare(`
      INSERT INTO processed_events (event_id, event_type, snapshot_event_id)
      VALUES (?, ?, ?)
    `).run(event.id, event.type, event.snapshot_event || null);
  })();
}
```

## Migration Interop Period

During migration, both event types may be delivered for the same logical change:

1. Stripe sends snapshot event `evt_1234` (type: `customer.subscription.updated`)
2. Stripe sends thin event `evt_thin_5678` (type: `v1.customer.subscription.updated`, `snapshot_event: evt_1234`)

### Deduplication Strategy

Use the `snapshot_event` field to correlate:

```typescript
function shouldProcess(eventId: string, snapshotEventId?: string): boolean {
  if (snapshotEventId) {
    // Check if the snapshot event was already processed
    const row = db.prepare(`
      SELECT 1 FROM processed_events
      WHERE event_id IN (?, ?)
         OR snapshot_event_id IN (?, ?)
    `).get(eventId, snapshotEventId, eventId, snapshotEventId);
    return !row;
  }

  return !db.prepare('SELECT 1 FROM processed_events WHERE event_id = ?').get(eventId);
}
```

### Routing During Interop

Handle both event type formats:

```typescript
const eventHandlers: Record<string, (event: any) => Promise<void>> = {
  // Snapshot event types (legacy)
  'customer.subscription.updated': handleSnapshotSubscriptionUpdate,
  'customer.subscription.deleted': handleSnapshotSubscriptionDelete,

  // Thin event types (new, prefixed with v1.)
  'v1.customer.subscription.updated': handleThinSubscriptionUpdate,
  'v1.customer.subscription.deleted': handleThinSubscriptionDelete,
};
```

### Migration Completion

Once all handlers support thin events:
1. Remove snapshot event handlers
2. Remove `snapshot_event_id` deduplication (simplify to just `event_id`)
3. Update the webhook endpoint configuration in Stripe Dashboard to only send thin events
4. Clean up the `snapshot_event_id` column from `processed_events`

## Rate Limiting Consideration for Thin Events

Thin events require an API call to Stripe for every event. During high-volume periods (batch subscription updates, end-of-month billing), this can hit Stripe's API rate limits.

**Mitigations:**
- Queue webhook processing and rate-limit Stripe API calls
- Use a local cache for recently fetched objects
- Batch fetches where possible
- Fall back to the snapshot payload if the API call fails (with a flag to re-fetch later)
