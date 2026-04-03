---
name: stripe-webhook-testing
description: >
  This skill should be used when writing tests for Stripe webhook handlers, implementing
  "fastify.inject() for webhooks", "Stripe webhook test", "webhook signature test",
  "idempotency test", "schema validation test", "Stripe CLI fixtures", "stripe trigger command",
  "mock Stripe API in tests", "webhook handler test", "billing integration test",
  "test invalid webhook payload", "webhook failure path test", or when the user asks how to
  test Stripe webhook handlers, billing endpoints, or subscription state machine logic.
---

# Testing Stripe Webhook Handlers

## Testing Strategy

Testing Stripe webhook handlers requires a layered approach:

1. **Unit tests** — Zod schema validation, event dispatch logic, state machine transitions
2. **Integration tests** — Full Fastify pipeline via `.inject()`, database transactions, idempotency
3. **Fixture tests** — Real Stripe event payloads from the Stripe CLI

## Fastify Injection: The Core Testing Pattern

Use `fastify.inject()` to test the full HTTP pipeline without network I/O:

```typescript
import { build } from './app'; // Your Fastify app builder

describe('Webhook Handler', () => {
  let app: FastifyInstance;

  beforeAll(async () => {
    app = await build({ testing: true });
  });

  afterAll(async () => {
    await app.close();
  });

  it('accepts a valid webhook with correct signature', async () => {
    const payload = JSON.stringify(mockCheckoutEvent);
    const signature = generateTestSignature(payload, TEST_WEBHOOK_SECRET);

    const response = await app.inject({
      method: 'POST',
      url: '/webhooks/stripe',
      headers: {
        'content-type': 'application/json',
        'stripe-signature': signature,
      },
      payload,
    });

    expect(response.statusCode).toBe(200);
    expect(response.json()).toEqual({ received: true });
  });
});
```

## Generating Test Signatures

Create an HMAC-SHA256 signature matching Stripe's format (`t={timestamp},v1={hash}`). Compute the hash over `{timestamp}.{rawPayload}` using the webhook secret. See `references/essential-test-cases.md` for the complete `generateTestSignature()` helper.

## Essential Test Cases

Six test cases must exist for any Stripe webhook handler. Full implementations with code are in **`references/essential-test-cases.md`**.

| # | Test | Asserts |
|---|------|---------|
| 1 | **Happy path** — valid webhook accepted | `checkout.session.completed` with valid signature → 200, subscription created in DB |
| 2 | **Invalid signature** | Tampered `stripe-signature` header → 400 |
| 3 | **Missing signature** | No `stripe-signature` header → 400 |
| 4 | **Idempotency** — duplicate event | Same event sent twice → processed once, `processed_events` count = 1 |
| 5 | **Schema validation** — invalid API input | Malformed billing API request → 400 before handler runs |
| 6 | **Out-of-order events** | `subscription.deleted` before `subscription.updated` → remains canceled |

## What to Mock vs. Keep Real

### Mock (External Network Boundaries)

- **Stripe API calls** — Mock `stripe.subscriptions.retrieve()` for thin events
- **JWKS endpoint** — Mock the remote JWKS URL for JWT validation
- **Email/notification services** — Mock queue additions

### Keep Real (Internal Processing)

- **Fastify pipeline** — Use `fastify.inject()`, not HTTP clients
- **Zod validation** — Let the real schemas validate
- **Database** — Use an in-memory SQLite database for real transaction testing
- **Idempotency logic** — Test with real `processed_events` table

## Stripe CLI for Fixture Generation

Use the Stripe CLI to generate realistic event payloads with valid structures:

```bash
# Generate a specific event type
stripe trigger checkout.session.completed

# Listen and forward events to local endpoint
stripe listen --forward-to http://localhost:3000/webhooks/stripe

# Generate event JSON for fixtures
stripe events resend evt_... --webhook-endpoint we_...
```

Save captured events as JSON fixtures in `tests/fixtures/`:

```
tests/fixtures/
├── checkout.session.completed.json
├── customer.subscription.updated.json
├── invoice.paid.json
└── invoice.payment_failed.json
```

## Test Database Setup

Use an in-memory SQLite database for test isolation:

```typescript
import Database from 'better-sqlite3';

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

## Additional Resources

### Reference Files

- **`references/essential-test-cases.md`** — Complete test implementations for all 6 essential test cases, including the signature helper, mock setup patterns, and test database configuration
