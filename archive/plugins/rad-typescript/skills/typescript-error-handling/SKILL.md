---
name: typescript-error-handling
description: >
  This skill should be used when implementing error handling in TypeScript, when asked about
  try/catch patterns, Result types, error-as-value patterns, neverthrow or errore libraries,
  handling async errors, classifying errors, typed error handling, or transitioning from
  exception-based to result-based error handling. Trigger on: "error handling TypeScript",
  "Result type", "neverthrow", "errore library", "errors as values", "typed errors",
  "catch block typing", "useUnknownInCatchVariables", "error classification", "ResultAsync",
  "fromPromise", "safe error handling", "silent catch", "try catch best practices",
  "functional error handling".
---

# TypeScript Error Handling

Traditional JavaScript error handling uses `try/catch`, which is structurally "loose" — any value can be thrown, errors are invisible in function signatures, and `catch` variables were historically typed as `any`. The modern approach treats errors as first-class typed values rather than exceptions.

## The Core Problem with Exceptions

```typescript
// What the caller SEES in the type system:
async function getUser(id: string): Promise<User> { ... }

// What CAN ACTUALLY HAPPEN at runtime:
// - throws DatabaseConnectionError
// - throws UserNotFoundError
// - throws ValidationError
// - throws anything (string, number, object...)

// The type signature LIE — nothing about errors is communicated
```

Exceptions create invisible unhappy paths. Result types make errors visible, typed, and required to handle.

## Rule 1: Enable `useUnknownInCatchVariables`

This flag (on by default in `strict` since TS 4.4) types `catch` variables as `unknown` instead of `any`.

```typescript
// Without: err is any — no type safety
try {
  await fetchUser(id);
} catch (err: any) {
  console.error(err.message); // No error — but crashes if err is a string
}

// With: err is unknown — must narrow before use
try {
  await fetchUser(id);
} catch (err) {
  if (err instanceof Error) {
    console.error(err.message); // Safe
    return;
  }
  console.error('Unknown error type:', err);
}
```

## Rule 2: Classify Errors Before Deciding Action

| Category | Recoverable? | Action |
|----------|-------------|--------|
| **Transient** (timeout, 503) | Yes | Retry with exponential backoff |
| **Correctable** (validation, 400, expired token) | Sometimes | Fix input and retry |
| **Permanent** (404, 403 Forbidden) | No | Fail fast, report to user |
| **Fatal** (OOM, missing config) | No | Abort immediately, alert ops |

Never use a single `catch (err)` for all categories — each requires different handling.

## The Result Pattern

Return errors as typed values. Callers must handle them — they cannot be ignored.

### Simple Result Type

```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function divide(a: number, b: number): Result<number, 'division-by-zero'> {
  if (b === 0) return { ok: false, error: 'division-by-zero' };
  return { ok: true, value: a / b };
}

const result = divide(10, 0);
if (!result.ok) {
  console.error('Cannot divide by zero');
} else {
  console.log(result.value);
}
```

### Using `neverthrow` (Recommended for Production)

`neverthrow` provides `Result<V, E>` and `ResultAsync<V, E>` with chainable methods:

```bash
npm install neverthrow
```

```typescript
import { ok, err, Result, ResultAsync, fromPromise, fromSafePromise } from 'neverthrow';

// Synchronous Result
function parsePositive(n: number): Result<number, 'must-be-positive'> {
  if (n <= 0) return err('must-be-positive');
  return ok(n);
}

// Async Result
function fetchUser(id: string): ResultAsync<User, 'not-found' | 'network-error'> {
  return fromPromise(
    fetch(`/api/users/${id}`).then(r => r.json()),
    (e): 'not-found' | 'network-error' => {
      if (e instanceof Response && e.status === 404) return 'not-found';
      return 'network-error';
    }
  );
}

// Chaining — map transforms the success value
const result = await fetchUser('123')
  .map(user => user.name.toUpperCase())
  .mapErr(err => `Failed: ${err}`);

// Match — handle both branches
result.match(
  name => console.log(`User: ${name}`),
  err => console.error(err)
);
```

### Using `errore` (Native Union Types)

```bash
npm install errore
```

`errore` returns native TypeScript union errors `T | Error` without a wrapper class:

```typescript
import { tryit } from 'errore';

const [err, user] = await tryit(fetchUser)('123');
if (err) {
  console.error(err.message);
  return;
}
console.log(user.name);

// For async: append .catch to convert thrown promises
async function safeOperation(id: string): Promise<User | Error> {
  return fetchUser(id).catch((e) => e instanceof Error ? e : new Error(String(e)));
}
```

## Avoid These Anti-Patterns

### The Silent Catch
```typescript
// NEVER DO THIS — hides all failures
try {
  await processOrder(order);
} catch { } // Silent! Bugs become ghosts

// NEVER DO THIS — almost as bad
try {
  await processOrder(order);
} catch (err) {
  console.log(err); // Logged but not acted on — still silent in production
}
```

### Throwing Expected Errors
```typescript
// Wrong — caller has no idea this can fail
async function getUser(id: string): Promise<User> {
  const user = await db.users.findById(id);
  if (!user) throw new UserNotFoundError(id); // Hidden failure mode!
  return user;
}

// Correct — failure is explicit in the type signature
async function getUser(id: string): Promise<Result<User, 'not-found' | 'db-error'>> {
  try {
    const user = await db.users.findById(id);
    if (!user) return err('not-found');
    return ok(user);
  } catch (e) {
    return err('db-error');
  }
}
```

### Using `.parse()` Instead of `.safeParse()`
```typescript
// Wrong — throws on invalid input
const user = UserSchema.parse(requestBody); // Crashes!

// Correct — returns Result
const result = UserSchema.safeParse(requestBody);
if (!result.success) {
  return { ok: false, error: result.error.flatten() };
}
const user = result.data; // Typed and validated
```

## Typed Custom Error Classes

```typescript
class AppError extends Error {
  readonly _tag = 'AppError' as const; // Discriminant for narrowing

  constructor(
    message: string,
    readonly code: string,
    readonly statusCode: number,
    readonly retryable: boolean = false,
  ) {
    super(message);
    this.name = 'AppError';
    Object.setPrototypeOf(this, AppError.prototype); // Fix instanceof
  }

  static isAppError(err: unknown): err is AppError {
    return err instanceof AppError;
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} with id '${id}' not found`, 'NOT_FOUND', 404, false);
    this.name = 'NotFoundError';
    Object.setPrototypeOf(this, NotFoundError.prototype);
  }
}
```

## Multi-Step Operations with Result

```typescript
// Chain operations — stop on first error
async function createOrder(
  userId: string,
  items: CartItem[]
): ResultAsync<Order, 'user-not-found' | 'inventory-error' | 'payment-failed'> {
  return fetchUser(userId)
    .andThen(user => checkInventory(user, items))
    .andThen(({ user, items }) => processPayment(user, items))
    .andThen(({ payment, items }) => saveOrder(payment, items));
}

// Each step returns a Result — the chain short-circuits on error
// The error union accumulates all possible failure modes in the return type
```

## Additional Resources

For complete patterns and library guides, consult:
- **`references/result-patterns.md`** — Full neverthrow and errore usage patterns with async workflows
- **`references/error-classification.md`** — Error taxonomy, recovery strategies, and structured error metadata
