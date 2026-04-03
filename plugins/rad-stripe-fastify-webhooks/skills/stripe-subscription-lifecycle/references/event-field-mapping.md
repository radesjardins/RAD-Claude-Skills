# Event-to-Database Field Mapping

## checkout.session.completed

```typescript
// Event: checkout.session.completed
// Object: Stripe.Checkout.Session
const session = event.data.object as Stripe.Checkout.Session;

// Fields to extract:
// session.customer        → subscriptions.stripe_customer_id
// session.subscription    → subscriptions.stripe_subscription_id
// session.metadata.userId → subscriptions.user_id (set during checkout creation)
// session.mode            → 'subscription' | 'payment' (determines handler path)
```

**Action:** Create subscription record. If `mode === 'subscription'`, insert into `subscriptions` table. If `mode === 'payment'`, handle as one-time purchase.

## customer.subscription.created

```typescript
// Event: customer.subscription.created
// Object: Stripe.Subscription
const sub = event.data.object as Stripe.Subscription;

// Fields to map:
// sub.id                            → subscriptions.stripe_subscription_id
// sub.customer                      → subscriptions.stripe_customer_id
// sub.items.data[0].price.id        → subscriptions.stripe_price_id
// sub.status                        → subscriptions.status
// sub.current_period_start          → subscriptions.current_period_start (Unix timestamp)
// sub.current_period_end            → subscriptions.current_period_end (Unix timestamp)
// sub.cancel_at_period_end          → subscriptions.cancel_at_period_end (boolean → 0/1)
// sub.trial_start                   → (optional) for trial tracking
// sub.trial_end                     → (optional) for trial tracking
```

## customer.subscription.updated

```typescript
// Event: customer.subscription.updated
// Object: Stripe.Subscription
const sub = event.data.object as Stripe.Subscription;

// Fields to update (same as created, but UPDATE not INSERT):
// sub.items.data[0].price.id        → subscriptions.stripe_price_id (plan may have changed)
// sub.status                        → subscriptions.status
// sub.current_period_start          → subscriptions.current_period_start
// sub.current_period_end            → subscriptions.current_period_end
// sub.cancel_at_period_end          → subscriptions.cancel_at_period_end

// Previous attributes available at:
// event.data.previous_attributes    → useful for detecting what changed
```

**Important:** Check `event.data.previous_attributes` to determine what changed. If `status` changed from `active` to `past_due`, trigger the grace period logic.

## customer.subscription.deleted

```typescript
// Event: customer.subscription.deleted
// Object: Stripe.Subscription
const sub = event.data.object as Stripe.Subscription;

// sub.id     → Look up subscription by stripe_subscription_id
// sub.status → Will be 'canceled'

// Action: UPDATE subscriptions SET status = 'canceled', updated_at = datetime('now')
//         WHERE stripe_subscription_id = ?
```

**Note:** This event fires when the subscription is fully terminated. If `cancel_at_period_end` was set, this fires at the end of the billing period — not when the user clicked "cancel."

## invoice.paid

```typescript
// Event: invoice.paid
// Object: Stripe.Invoice
const invoice = event.data.object as Stripe.Invoice;

// Fields:
// invoice.subscription           → subscriptions.stripe_subscription_id (look up)
// invoice.customer               → subscriptions.stripe_customer_id
// invoice.period_end             → subscriptions.current_period_end (extend access)
// invoice.billing_reason         → 'subscription_cycle' | 'subscription_create' | ...

// Action:
// 1. Update current_period_end
// 2. Clear grace_period_end (payment succeeded, dunning over)
// 3. Ensure status is 'active'
```

## invoice.payment_failed

```typescript
// Event: invoice.payment_failed
// Object: Stripe.Invoice
const invoice = event.data.object as Stripe.Invoice;

// Fields:
// invoice.subscription           → subscriptions.stripe_subscription_id
// invoice.attempt_count          → How many times Stripe has retried
// invoice.next_payment_attempt   → When Stripe will retry next (Unix timestamp or null)

// Action:
// 1. Set grace_period_end = now + GRACE_DAYS
// 2. If attempt_count > threshold, escalate notification urgency
// 3. Queue notification to customer
```

## invoice.finalization_failed

```typescript
// Event: invoice.finalization_failed
// Object: Stripe.Invoice
const invoice = event.data.object as Stripe.Invoice;

// This happens when Stripe cannot finalize an invoice (e.g., missing tax location).
// Action: Log the failure, notify the customer to provide missing details.
// This is NOT a payment failure — it's a pre-payment configuration issue.
```

## customer.source.expiring

```typescript
// Event: customer.source.expiring
// Object: Stripe.Card (or Stripe.Source)
const card = event.data.object as Stripe.Card;

// card.customer    → Look up user by stripe_customer_id
// card.exp_month   → Expiring month
// card.exp_year    → Expiring year

// Action: Send proactive notification 30 days before expiration.
// This prevents invoice.payment_failed from firing later.
```

## Status-to-Access Mapping

| Stripe Status | Local Access | Notes |
|---------------|-------------|-------|
| `trialing` | Full access | Trial features may be limited |
| `active` | Full access | Normal operating state |
| `past_due` | Grace period access | 3-5 day grace window |
| `canceled` | No access | Immediate revocation |
| `unpaid` | No access | All retries exhausted |
| `incomplete` | No access | Initial payment pending (23-hour window) |
| `incomplete_expired` | No access | Initial payment never completed |
| `paused` | No access | Manually paused by admin or API |
