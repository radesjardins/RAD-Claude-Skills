# Discriminated Unions: Advanced Patterns

## Core Pattern Review

A discriminated union requires:
1. A **shared literal property** (the discriminant) — use `kind`, `type`, or `status`
2. **Distinct literal values** for each member
3. **No optional properties** to differentiate members

```typescript
// The discriminant is 'kind' — each member has a unique literal
type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'square'; side: number }
  | { kind: 'rectangle'; width: number; height: number };
```

## Application State Machine Pattern

Model UI state with discriminated unions to eliminate impossible states:

```typescript
// Problematic: allows impossible states like { loading: true, data: user, error: 'failed' }
interface BadState {
  loading: boolean;
  data?: User;
  error?: string;
}

// Correct: mutually exclusive states
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T; timestamp: Date }
  | { status: 'error'; error: Error; retryable: boolean };

// Usage in a component
function UserCard({ state }: { state: AsyncState<User> }) {
  switch (state.status) {
    case 'idle':    return <Placeholder />;
    case 'loading': return <Spinner />;
    case 'success': return <Profile user={state.data} />;
    case 'error':   return <ErrorMessage error={state.error} retryable={state.retryable} />;
  }
}
```

## Event System Pattern

```typescript
type AppEvent =
  | { type: 'USER_LOGIN'; payload: { userId: string; timestamp: Date } }
  | { type: 'USER_LOGOUT'; payload: { userId: string } }
  | { type: 'ITEM_ADDED'; payload: { itemId: string; quantity: number } }
  | { type: 'CHECKOUT_STARTED'; payload: { cartId: string; total: number } };

// Type-safe event handler
function handleEvent(event: AppEvent): void {
  switch (event.type) {
    case 'USER_LOGIN':
      trackLogin(event.payload.userId, event.payload.timestamp);
      break;
    case 'USER_LOGOUT':
      clearSession(event.payload.userId);
      break;
    case 'ITEM_ADDED':
      updateCart(event.payload.itemId, event.payload.quantity);
      break;
    case 'CHECKOUT_STARTED':
      initCheckout(event.payload.cartId, event.payload.total);
      break;
  }
}
```

## API Response Pattern

```typescript
type ApiResponse<T, E = Error> =
  | { ok: true; data: T; statusCode: 200 | 201 }
  | { ok: false; error: E; statusCode: 400 | 401 | 403 | 404 | 500 };

// Generic fetch wrapper
async function apiFetch<T>(url: string): Promise<ApiResponse<T>> {
  const res = await fetch(url);
  if (res.ok) {
    const data = await res.json() as T;
    return { ok: true, data, statusCode: res.status as 200 | 201 };
  }
  const error = new Error(`Request failed: ${res.status}`);
  return { ok: false, error, statusCode: res.status as 400 | 401 | 403 | 404 | 500 };
}

// Consuming it
const result = await apiFetch<User>('/api/users/1');
if (result.ok) {
  console.log(result.data.name); // result.data: User
} else {
  console.error(result.error.message); // result.error: Error
}
```

## Nested Discriminated Unions

```typescript
type PaymentMethod =
  | { type: 'card'; cardNumber: string; expiry: string; cvv: string }
  | { type: 'bank'; accountNumber: string; routingNumber: string }
  | { type: 'crypto'; walletAddress: string; currency: 'BTC' | 'ETH' | 'USDC' };

type OrderStatus =
  | { status: 'pending'; createdAt: Date; paymentMethod: PaymentMethod }
  | { status: 'processing'; startedAt: Date; processor: string }
  | { status: 'completed'; completedAt: Date; transactionId: string }
  | { status: 'failed'; failedAt: Date; reason: string; retryable: boolean };

// Nested narrowing
function processOrder(order: OrderStatus): string {
  if (order.status === 'pending') {
    if (order.paymentMethod.type === 'crypto') {
      return `Crypto wallet: ${order.paymentMethod.walletAddress}`;
    }
    return `Payment method: ${order.paymentMethod.type}`;
  }
  return `Order status: ${order.status}`;
}
```

## Mapping Over Discriminated Unions

```typescript
// Extract a specific member by discriminant
type ExtractByKind<T extends { kind: string }, K extends T['kind']> =
  Extract<T, { kind: K }>;

type CircleShape = ExtractByKind<Shape, 'circle'>; // { kind: 'circle'; radius: number }

// Create a handler map for all union members
type ShapeHandlers = {
  [K in Shape['kind']]: (shape: ExtractByKind<Shape, K>) => number;
};

const areaCalculators: ShapeHandlers = {
  circle: s => Math.PI * s.radius ** 2,
  square: s => s.side ** 2,
  rectangle: s => s.width * s.height,
};
```

## Union Narrowing Utilities

```typescript
// Filter union members by discriminant value
function matchKind<T extends { kind: string }, K extends T['kind']>(
  value: T,
  kind: K,
): value is Extract<T, { kind: K }> {
  return value.kind === kind;
}

// Usage
if (matchKind(shape, 'circle')) {
  // shape: { kind: 'circle'; radius: number }
  return shape.radius;
}
```

## Common Mistakes

### Mistake: Optional Properties Instead of Union Members
```typescript
// Wrong — allows invalid states
interface BadUser {
  id: string;
  type: 'admin' | 'user';
  adminLevel?: number; // Should only exist for admin!
  permissions?: string[];
}

// Correct — each type has exactly the properties it needs
type User =
  | { type: 'admin'; id: string; adminLevel: number }
  | { type: 'user'; id: string; permissions: string[] };
```

### Mistake: String Discriminant Without Literal Types
```typescript
// Wrong — discriminant is too broad
interface BadResult {
  status: string; // Could be anything!
  data?: unknown;
  error?: string;
}

// Correct — discriminant is a literal union
type Result<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };
```

### Mistake: Forgetting Exhaustiveness Check
```typescript
// Dangerous — silently ignores new union members
function process(shape: Shape): number {
  if (shape.kind === 'circle') return shape.radius;
  if (shape.kind === 'square') return shape.side;
  return 0; // What if 'rectangle' is added? Silent wrong result!
}

// Correct — compile error when new members added
function process(shape: Shape): number {
  switch (shape.kind) {
    case 'circle': return shape.radius;
    case 'square': return shape.side;
    case 'rectangle': return shape.width;
    default: return assertNever(shape);
  }
}
```
