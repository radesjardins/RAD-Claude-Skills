# Result Patterns: Complete Reference

## neverthrow API Reference

### Core Constructors
```typescript
import { ok, err, Result, ResultAsync } from 'neverthrow';

// Success
const success: Result<number, never> = ok(42);

// Failure
const failure: Result<never, string> = err('validation failed');

// Async versions
const asyncSuccess = ResultAsync.fromSafePromise(Promise.resolve(42));
const asyncFailure = ResultAsync.fromPromise(
  fetch('/api').then(r => r.json()),
  (e): NetworkError => new NetworkError(String(e))
);
```

### Transformation Methods

```typescript
// map — transform success value, preserve error type
const doubled = ok(5).map(n => n * 2); // Result<number, never>

// mapErr — transform error value, preserve success type
const withMessage = err('NOT_FOUND').mapErr(e => new Error(e)); // Result<never, Error>

// andThen — chain operations (flatMap/bind)
function validateAge(n: number): Result<number, 'too-young'> {
  return n >= 18 ? ok(n) : err('too-young');
}

const result = ok(20)
  .andThen(validateAge)
  .map(age => `Age: ${age}`);

// orElse — handle error, potentially recover
const recovered = err('NOT_FOUND').orElse(e => ok('default value'));

// match — consume result (no chaining after this)
result.match(
  value => console.log('Success:', value),
  error => console.error('Error:', error),
);

// unwrapOr — extract value with fallback
const value = result.unwrapOr('fallback');

// isOk / isErr — type guards
if (result.isOk()) {
  console.log(result.value); // TypeScript knows .value exists
}
if (result.isErr()) {
  console.log(result.error); // TypeScript knows .error exists
}
```

### Async Patterns (ResultAsync)

```typescript
import { fromPromise, fromSafePromise, ResultAsync } from 'neverthrow';

type DbError = 'connection-failed' | 'query-failed' | 'not-found';

// Wrap a promise that can reject
function queryUser(id: string): ResultAsync<User, DbError> {
  return fromPromise(
    db.users.findById(id),
    (e): DbError => {
      if (e instanceof ConnectionError) return 'connection-failed';
      if (e instanceof QueryError) return 'query-failed';
      return 'not-found';
    }
  );
}

// fromSafePromise — for promises you know won't reject
function delay(ms: number): ResultAsync<void, never> {
  return fromSafePromise(new Promise(resolve => setTimeout(resolve, ms)));
}

// Async chain
async function createUserSession(email: string, password: string) {
  return findUserByEmail(email)
    .andThen(user => verifyPassword(user, password))
    .andThen(user => createSession(user))
    .map(session => ({ sessionId: session.id, expiresAt: session.expiresAt }));
}

// Combining multiple Results
import { combine, combineWithAllErrors } from 'neverthrow';

// combine — stops on first error
const combined = combine([ok(1), ok(2), ok(3)]); // Result<[1,2,3], E>

// combineWithAllErrors — collects all errors
const allResults = combineWithAllErrors([ok(1), err('a'), err('b')]);
// Result<[1,...], ['a','b',...]>
```

### neverthrow + Zod Integration

```typescript
import { z } from 'zod';
import { ok, err } from 'neverthrow';

const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1),
});

type User = z.infer<typeof UserSchema>;
type ValidationError = { field: string; message: string }[];

function parseUser(data: unknown): Result<User, ValidationError> {
  const result = UserSchema.safeParse(data);
  if (!result.success) {
    return err(
      result.error.issues.map(issue => ({
        field: issue.path.join('.'),
        message: issue.message,
      }))
    );
  }
  return ok(result.data);
}
```

## errore API Reference

```bash
npm install errore
```

`errore` uses native TypeScript union types (`T | Error`) without wrapper classes:

```typescript
import { tryit, isError } from 'errore';

// Wrap a function to return [error, result] tuple
const [err, user] = await tryit(fetchUser)('123');

if (err) {
  // err is Error | specific error type
  console.error(err.message);
  return;
}
// user is typed correctly here
console.log(user.name);

// Multiple steps
const [err1, data1] = await tryit(step1)(input);
if (err1) return handleError(err1);

const [err2, data2] = await tryit(step2)(data1);
if (err2) return handleError(err2);

// isError utility
function processResult(result: User | Error) {
  if (isError(result)) {
    console.error(result.message);
    return;
  }
  console.log(result.name);
}
```

## Pure TypeScript Result (No Library)

For minimal dependencies:

```typescript
export type Ok<T> = { readonly _tag: 'Ok'; readonly value: T };
export type Err<E> = { readonly _tag: 'Err'; readonly error: E };
export type Result<T, E> = Ok<T> | Err<E>;

export const ok = <T>(value: T): Ok<T> => ({ _tag: 'Ok', value });
export const err = <E>(error: E): Err<E> => ({ _tag: 'Err', error });

export function isOk<T, E>(result: Result<T, E>): result is Ok<T> {
  return result._tag === 'Ok';
}

export function isErr<T, E>(result: Result<T, E>): result is Err<E> {
  return result._tag === 'Err';
}

export function mapResult<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => U
): Result<U, E> {
  return isOk(result) ? ok(fn(result.value)) : result;
}
```

## Converting Existing Promise Code

```typescript
// Before: throws exceptions
async function fetchProfile(userId: string): Promise<Profile> {
  const response = await fetch(`/api/users/${userId}/profile`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

// After: returns Result
function fetchProfile(userId: string): ResultAsync<Profile, 'not-found' | 'network-error'> {
  return fromPromise(
    fetch(`/api/users/${userId}/profile`).then(res => {
      if (!res.ok) throw Object.assign(new Error(), { status: res.status });
      return res.json() as Promise<Profile>;
    }),
    (e): 'not-found' | 'network-error' => {
      if (typeof e === 'object' && e !== null && 'status' in e && (e as any).status === 404) {
        return 'not-found';
      }
      return 'network-error';
    }
  );
}
```
