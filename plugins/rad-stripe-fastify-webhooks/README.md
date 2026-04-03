# rad-stripe-fastify-webhooks

Production-grade Stripe webhook handling with Fastify and Zod for Claude Code.

## What This Plugin Does

Guides AI assistants and developers in building resilient Stripe webhook handlers that follow the "Stripe handles money, your database handles entitlements" architecture. Enforces signature verification, idempotent processing, Zod validation contracts, and subscription state machine patterns.

## Skills

| Skill | Purpose |
|-------|---------|
| `stripe-webhook-best-practices` | Core mental model, 5 backend rules, architecture overview |
| `stripe-webhook-handling` | Signature verification, raw body access, thin events, event routing |
| `stripe-subscription-lifecycle` | Subscription state machine, authoritative events, grace periods |
| `stripe-webhook-idempotency` | Processed events table, deduplication, reconciliation crons |
| `stripe-webhook-security` | Rate limiting, secret management, log redaction, abuse controls |
| `stripe-zod-contracts` | Zod schemas for webhooks, config validation, type inference |
| `stripe-webhook-testing` | fastify.inject(), Stripe CLI fixtures, schema tests, failure paths |

## Agent

| Agent | Purpose |
|-------|---------|
| `stripe-webhook-reviewer` | Autonomous code review for Stripe webhook handlers — catches missing signature verification, pre-parsed JSON bodies, absent idempotency, missing rate limits |

## Installation

```bash
claude --plugin-dir /path/to/rad-stripe-fastify-webhooks
```

## The 5 Backend Rules

1. **Strict Validation** — Every route MUST have a Zod schema for body, querystring, and params
2. **Webhook Integrity** — All Stripe webhook handlers MUST use `req.rawBody` for signature verification
3. **Persistence Safety** — Never perform database writes outside of an explicit transaction
4. **Hook-Based Auth** — Authentication in `onRequest`, authorization in `preHandler`
5. **Idempotent Billing** — Every billing event checked against `processed_events` table before execution

## Built From

55 curated sources including Stripe official docs, Fastify lifecycle references, Zod documentation, SaaS billing architecture guides, JWT/JOSE specifications, SQLite WAL mode references, and production case studies.
