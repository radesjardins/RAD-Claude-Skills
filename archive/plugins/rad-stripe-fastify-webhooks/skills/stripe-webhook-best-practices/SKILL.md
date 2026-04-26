---
name: stripe-webhook-best-practices
description: >
  This skill should be used when working on any Fastify project that integrates with Stripe webhooks,
  or when the user asks about "Stripe webhook architecture", "Stripe Fastify best practices",
  "SaaS billing architecture", "entitlement engine", "Stripe subscription patterns",
  "webhook handler design", "billing state machine", "Stripe plugin structure", or mentions building
  a payment/billing backend with Fastify and Zod. Provides the core mental model and architectural
  rules for production-grade Stripe webhook handling.
---

# Stripe Webhooks with Fastify & Zod: Core Architecture

## Mental Model

A production SaaS billing backend separates two concerns completely:

- **Stripe handles the money** — charges, invoices, subscription transitions, payment retries.
- **The local database is the single source of truth for entitlements** — what features a user can access, what plan they are on, what limits apply.

Webhooks are the bridge: a high-speed, secure intake queue that receives Stripe events, verifies their authenticity, and updates the local database. Webhook handlers must never execute heavy business logic synchronously — return `200 OK` immediately and process asynchronously.

Stripe is the authority on "what was paid." The local database is the authority on "what can this user do."

## The 5 Backend Rules

These rules are non-negotiable for any Fastify + Stripe + Zod codebase:

### Rule 1: Strict Validation

Every route MUST have a Zod schema for `body`, `querystring`, and `params`. Use `withTypeProvider<ZodTypeProvider>()` for all route handlers. Zod schemas are the single source of truth for both runtime validation and TypeScript types.

### Rule 2: Webhook Integrity

All Stripe webhook handlers MUST use `req.rawBody` for signature verification. Skip global JSON body parsing for the `/webhooks` route prefix. Never allow a framework to pre-parse the JSON body before signature verification — this alters the byte payload and breaks the HMAC check.

### Rule 3: Persistence Safety

Never perform database writes outside of an explicit transaction. For SQLite, always use `db.transaction()` with `BEGIN IMMEDIATE` for any billing-related logic. For PostgreSQL, use explicit transactions and consider `SELECT FOR UPDATE` for operations like credit deductions.

### Rule 4: Hook-Based Auth

Implement authentication in the `onRequest` hook (cheapest rejection point — before body parsing). Implement authorization and entitlement checks in the `preHandler` hook (after Zod validation). Attach verified user identity to `request.user` via `fastify.decorateRequest`.

### Rule 5: Idempotent Billing

Every billing-related webhook event must be checked against a `processed_events` table before executing business logic. Record the event ID **after** (or atomically with) the business logic — never before. If you record the ID before processing and crash mid-operation, the event is permanently lost when Stripe retries.

## Fastify Plugin Architecture

Structure the billing domain as an encapsulated Fastify plugin:

```
src/plugins/billing/
├── index.ts          # Plugin registration (fastify.register)
├── webhook.route.ts  # Webhook POST handler (rawBody, signature verify)
├── billing.service.ts # Business logic (private, not exported)
├── billing.repo.ts   # Database access (private, not exported)
└── schemas.ts        # Zod schemas (exported for type inference)
```

Register as a Fastify plugin with encapsulation. The webhook route bypasses global JSON parsing. The service and repository layers remain private inside the plugin context.

The plugin must be `async` because webhook handling involves signature verification, Stripe API calls (for thin events), and database transactions.

## Authoritative Webhook Events

These events drive subscription state in the local database:

| Event | Action |
|-------|--------|
| `checkout.session.completed` | Create subscription record, provision access |
| `customer.subscription.created` | Initialize subscription in local DB |
| `customer.subscription.updated` | Update plan, status, period dates |
| `customer.subscription.deleted` | Revoke access, mark canceled |
| `invoice.paid` | Extend access, reset dunning state |
| `invoice.payment_failed` | Begin grace period, notify customer |
| `invoice.finalization_failed` | Retry or collect missing details |
| `customer.source.expiring` | 30-day warning to update payment method |

## Key Architectural Patterns

### Webhook-First, Pull-Second

Rely on webhooks for real-time state changes. Run a daily reconciliation cron that fetches recent events from the Stripe API to catch any missed webhooks. Webhooks are push-based and will eventually fail — the cron is the safety net.

### Thin Events Pattern

Instead of trusting large "snapshot" webhook payloads, use Stripe's Thin Events which provide only `event_type` and object `id`. The handler then fetches the latest state from the Stripe API, ensuring it always acts on current data regardless of delivery order.

### Internal Entitlement Engine

Never store feature limits in Stripe metadata. Map `stripePriceId` to an internal plan definition that declares what features, quotas, and limits that plan includes. Compute entitlements from the local database in a single query — never call Stripe to check what a user can do.

### Grace Periods

Map Stripe's `past_due` status to an internal grace period (3–5 days) before locking features. This reduces support tickets from transient card failures and gives automatic retry logic time to succeed.

## Additional Resources

### Reference Files

For detailed implementation patterns, consult:
- **`references/architecture-patterns.md`** — Full architectural patterns including plugin registration, Fastify lifecycle hooks, config namespace, and database schema
