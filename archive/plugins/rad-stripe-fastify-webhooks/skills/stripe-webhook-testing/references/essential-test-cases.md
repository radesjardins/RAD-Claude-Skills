# Essential Webhook Test Cases

Complete test implementations using `fastify.inject()` for Stripe webhook handlers.

## Test Signature Helper

```typescript
import crypto from 'node:crypto';

const TEST_WEBHOOK_SECRET = 'whsec_test_secret_for_testing_only';

function generateTestSignature(payload: string, secret: string): string {
  const timestamp = Math.floor(Date.now() / 1000);
  const signedPayload = `${timestamp}.${payload}`;
  const signature = crypto
    .createHmac('sha256', secret)
    .update(signedPayload)
    .digest('hex');
  return `t=${timestamp},v1=${signature}`;
}
```

## Test 1: Happy Path — Valid Webhook Accepted

Sends a valid `checkout.session.completed` event with correct signature and verifies the subscription record was created in the database.

```typescript
it('processes checkout.session.completed and creates subscription', async () => {
  const payload = JSON.stringify(mockCheckoutSessionCompleted);
  const sig = generateTestSignature(payload, TEST_WEBHOOK_SECRET);

  const response = await app.inject({
    method: 'POST',
    url: '/webhooks/stripe',
    headers: { 'stripe-signature': sig, 'content-type': 'application/json' },
    payload,
  });

  expect(response.statusCode).toBe(200);

  // Verify subscription was created in database
  const sub = db.prepare(
    'SELECT * FROM subscriptions WHERE stripe_subscription_id = ?'
  ).get(mockCheckoutSessionCompleted.data.object.subscription);
  expect(sub).toBeDefined();
  expect(sub.status).toBe('active');
});
```

## Test 2: Signature Verification Failure

Sends a webhook with an invalid `stripe-signature` header. Must return `400`.

```typescript
it('rejects webhooks with invalid signature', async () => {
  const response = await app.inject({
    method: 'POST',
    url: '/webhooks/stripe',
    headers: {
      'stripe-signature': 't=123,v1=invalid_signature_here',
      'content-type': 'application/json',
    },
    payload: JSON.stringify(mockCheckoutSessionCompleted),
  });

  expect(response.statusCode).toBe(400);
});
```

## Test 3: Missing Signature Header

Sends a webhook without the `stripe-signature` header at all. Must return `400`.

```typescript
it('rejects webhooks without stripe-signature header', async () => {
  const response = await app.inject({
    method: 'POST',
    url: '/webhooks/stripe',
    headers: { 'content-type': 'application/json' },
    payload: JSON.stringify(mockCheckoutSessionCompleted),
  });

  expect(response.statusCode).toBe(400);
});
```

## Test 4: Idempotency — Duplicate Event Skipped

Sends the same event twice. The first should process, the second should be silently skipped. The `processed_events` table should have exactly one record.

```typescript
it('processes the same event only once', async () => {
  const payload = JSON.stringify(mockInvoicePaid);
  const sig = generateTestSignature(payload, TEST_WEBHOOK_SECRET);

  // First delivery — should process
  const first = await app.inject({
    method: 'POST',
    url: '/webhooks/stripe',
    headers: { 'stripe-signature': sig, 'content-type': 'application/json' },
    payload,
  });
  expect(first.statusCode).toBe(200);

  // Second delivery (duplicate) — should skip silently
  const second = await app.inject({
    method: 'POST',
    url: '/webhooks/stripe',
    headers: { 'stripe-signature': sig, 'content-type': 'application/json' },
    payload,
  });
  expect(second.statusCode).toBe(200);

  // Verify event was recorded only once
  const count = db.prepare(
    'SELECT COUNT(*) as c FROM processed_events WHERE event_id = ?'
  ).get(mockInvoicePaid.id);
  expect(count.c).toBe(1);
});
```

## Test 5: Schema Validation — Invalid Input Rejected

Tests that Zod validation on protected billing API routes rejects malformed requests before they reach the handler.

```typescript
it('rejects malformed API requests via Zod validation', async () => {
  const response = await app.inject({
    method: 'POST',
    url: '/api/v1/billing/checkout',
    headers: {
      authorization: `Bearer ${validJwt}`,
      'content-type': 'application/json',
    },
    payload: JSON.stringify({
      priceId: 'not_a_valid_price_id', // Missing price_ prefix
      successUrl: 'not-a-url',         // Invalid URL
    }),
  });

  expect(response.statusCode).toBe(400);
});
```

## Test 6: Out-of-Order Event Handling

Sends `customer.subscription.deleted` before `customer.subscription.updated` to verify the state machine handles chronological mismatches correctly.

```typescript
it('handles subscription.deleted arriving before subscription.updated', async () => {
  // Send deleted event first
  const deletedPayload = JSON.stringify(mockSubscriptionDeleted);
  await app.inject({
    method: 'POST',
    url: '/webhooks/stripe',
    headers: {
      'stripe-signature': generateTestSignature(deletedPayload, TEST_WEBHOOK_SECRET),
      'content-type': 'application/json',
    },
    payload: deletedPayload,
  });

  // Then send the earlier updated event
  const updatedPayload = JSON.stringify(mockSubscriptionUpdated);
  await app.inject({
    method: 'POST',
    url: '/webhooks/stripe',
    headers: {
      'stripe-signature': generateTestSignature(updatedPayload, TEST_WEBHOOK_SECRET),
      'content-type': 'application/json',
    },
    payload: updatedPayload,
  });

  // Verify the subscription remains deleted (not reverted)
  const sub = db.prepare(
    'SELECT status FROM subscriptions WHERE stripe_subscription_id = ?'
  ).get(mockSubscriptionDeleted.data.object.id);
  expect(sub.status).toBe('canceled');
});
```

## Test Database Setup

Use an in-memory SQLite database for test isolation:

```typescript
import Database from 'better-sqlite3';
import { readFileSync } from 'node:fs';

function createTestDb(): Database.Database {
  const db = new Database(':memory:');
  db.pragma('journal_mode = WAL');
  db.pragma('foreign_keys = ON');

  // Run migrations
  db.exec(readFileSync('./migrations/001_init.sql', 'utf8'));

  return db;
}
```

Each test suite gets a fresh database. No cleanup needed — the in-memory database is destroyed when the connection closes.

## Mock Setup Pattern

```typescript
import { vi } from 'vitest';

// Mock Stripe API for thin events
vi.mock('stripe', () => ({
  default: vi.fn().mockImplementation(() => ({
    webhooks: {
      constructEvent: vi.fn().mockImplementation((body, sig, secret) => {
        // Use real verification or return mock event based on test
        return JSON.parse(body.toString());
      }),
    },
    subscriptions: {
      retrieve: vi.fn().mockResolvedValue(mockSubscription),
    },
  })),
}));
```
