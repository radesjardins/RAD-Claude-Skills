---
name: typescript-type-patterns
description: >
  This skill should be used when writing TypeScript types, working with union types,
  implementing type guards or type predicates, using the satisfies operator, handling
  unknown or never types, creating discriminated unions, narrowing types, or modeling
  complex application state. Trigger on: "discriminated union", "type guard", "type predicate",
  "narrowing", "satisfies operator", "unknown type", "never type", "exhaustive switch",
  "is operator", "typeof check", "instanceof check", "union type pattern", "type narrowing",
  "as const pattern", "readonly type", "model state with types".
---

# TypeScript Type Patterns

Control Flow Analysis (CFA) is the intelligence layer of the TypeScript compiler — it tracks the specific type of a variable at every point in the execution path. Mastering these patterns is essential for managing union types and building APIs that are impossible to misuse.

## The Foundational Mental Model

TypeScript types model **sets of possible values**. The type system is *structural*, not nominal — two types with the same shape are compatible. Every pattern below builds on this: narrowing refines the set, discriminated unions segment it, `never` represents the empty set, `unknown` represents the universal set.

## Type Narrowing

Use narrowing to refine a broad type to a specific one through runtime control flow.

### `typeof` — Primitive narrowing
```typescript
function formatId(id: string | number): string {
  if (typeof id === 'string') {
    return id.toUpperCase(); // id: string
  }
  return id.toFixed(0); // id: number
}
```

### `instanceof` — Class and error narrowing
```typescript
function handleError(err: unknown): string {
  if (err instanceof Error) {
    return err.message; // err: Error
  }
  return String(err);
}
```

### `in` operator — Object shape narrowing
```typescript
function processShape(shape: Circle | Square) {
  if ('radius' in shape) {
    return Math.PI * shape.radius ** 2; // shape: Circle
  }
  return shape.side ** 2; // shape: Square
}
```

### Truthiness — Null/undefined filtering
```typescript
const users = [null, { name: 'Alice' }, null, { name: 'Bob' }];
const activeUsers = users.filter(Boolean); // (typeof users[0] | null)[]
// TS 5.5+: filter(Boolean) infers truthy type automatically
```

## Discriminated Unions — The Primary State Pattern

Discriminated unions are the most effective pattern for modeling complex application states, API responses, and messaging schemas. The **discriminant** is a shared literal property (`kind`, `type`, `status`) that distinguishes union members.

```typescript
// Define the union with a shared literal discriminant
type ApiResult<T> =
  | { kind: 'success'; data: T; statusCode: 200 }
  | { kind: 'error'; message: string; statusCode: 400 | 404 | 500 }
  | { kind: 'loading' };

// The compiler narrows based on the discriminant
function renderResult<T>(result: ApiResult<T>): string {
  switch (result.kind) {
    case 'success':
      return JSON.stringify(result.data); // result: { kind: 'success'; data: T; ... }
    case 'error':
      return `Error ${result.statusCode}: ${result.message}`;
    case 'loading':
      return 'Loading...';
  }
}
```

**Rules for discriminated unions:**
- Always use a literal `kind` or `type` property as the discriminant
- Never use optional properties to differentiate members — use `kind` instead
- Each member should have only the properties relevant to that state

## Exhaustiveness Checking with `never`

`never` represents a type with no possible values — the empty set. Use it to create compile-time guarantees that all union members are handled.

```typescript
function assertNever(value: never): never {
  throw new Error(`Unhandled case: ${JSON.stringify(value)}`);
}

function handleResult<T>(result: ApiResult<T>): string {
  switch (result.kind) {
    case 'success': return JSON.stringify(result.data);
    case 'error': return result.message;
    case 'loading': return 'Loading...';
    default: return assertNever(result); // Compiler error if a case is missed
  }
}
```

If a new union member (e.g., `{ kind: 'cancelled' }`) is added but not handled in the `switch`, the compiler flags the `assertNever` call as an error — the missing case is not assignable to `never`.

## Type Predicates — Reusable Narrowing Logic

Type predicates (`parameter is Type`) encapsulate complex validation into reusable guard functions.

```typescript
interface User { id: string; name: string; email: string; }

// Pre-TS-4.9 pattern: `in` narrowing required `as any` to access the property
// after the existence check. This is legacy — prefer TS 5.5 inferred predicates
// or Zod parsing for new code (see typescript-api-safety skill).
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj && typeof (obj as Record<string, unknown>).id === 'string' &&
    'name' in obj && typeof (obj as Record<string, unknown>).name === 'string' &&
    'email' in obj && typeof (obj as Record<string, unknown>).email === 'string'
  );
}
// Note: use `as Record<string, unknown>` not `as any` — it's still an assertion
// but it preserves the constraint that values are unknown, not typed-but-unsafe.

// TypeScript now knows `data` is User after the guard
if (isUser(data)) {
  console.log(data.email); // data: User
}
```

> **Modern alternative (TS 5.5+):** For validating external data, Zod schemas with `.safeParse()` are preferred over hand-written type predicates — they are safer, self-documenting, and free from manual assertion. See `typescript-api-safety` skill.

**TS 5.5 Inferred Type Predicates:** The compiler can automatically infer that `x => x !== null` is a type guard, eliminating boilerplate in `.filter()` calls:
```typescript
const values = [1, null, 2, null, 3];
const numbers = values.filter(x => x !== null); // number[] — inferred!
```

## `unknown` vs `any`

- **`unknown`** — The safe counterpart to `any`. Accepts any value but forces narrowing before use.
- **`any`** — Disables type checking entirely. Never use in production code.

```typescript
// any: no safety
function badProcess(data: any) {
  return data.userId.trim(); // No error — crashes if userId is undefined
}

// unknown: forces proof
function safeProcess(data: unknown) {
  if (isUser(data)) {
    return data.email.trim(); // Narrowed to User — safe
  }
  throw new Error('Invalid user data');
}
```

**Rule:** Any data from an external source (API, file, user input) starts as `unknown`. Parse it with Zod or a type predicate before use.

## The `satisfies` Operator

`satisfies` validates that an expression matches a type without widening the most specific inferred type. Use it for configuration objects and lookup tables.

```typescript
type Routes = Record<string, { path: string; auth: boolean }>;

// With type annotation — specific keys are lost (widened to string)
const routes: Routes = {
  home: { path: '/', auth: false },
  dashboard: { path: '/dashboard', auth: true },
};
routes.home; // Type: { path: string; auth: boolean }

// With satisfies — validation + literal preservation
const routes = {
  home: { path: '/', auth: false },
  dashboard: { path: '/dashboard', auth: true },
} satisfies Routes;
routes.home; // Type: { path: string; auth: boolean } AND routes.home is autocompleted
// routes.nonexistent; // Error! 'nonexistent' doesn't exist
```

**Use `satisfies` for:**
- Configuration objects where you need autocomplete on known keys
- Theme/palette definitions
- Route maps and constant lookup tables
- Any object that must conform to a type but where you want the narrowest inferred type

## `as const` — Literal Preservation and Immutability

`as const` recursively marks all properties `readonly` and prevents type widening.

```typescript
// Without as const:
const config = { theme: 'dark', locale: 'en' };
// Type: { theme: string; locale: string } — widened!

// With as const:
const config = { theme: 'dark', locale: 'en' } as const;
// Type: { readonly theme: 'dark'; readonly locale: 'en' }

// Derive runtime list + compile-time union from single source of truth:
const STATUS_OPTIONS = ['pending', 'active', 'completed'] as const;
type Status = typeof STATUS_OPTIONS[number]; // 'pending' | 'active' | 'completed'

// Use STATUS_OPTIONS for iteration, Status for type checking
```

## `readonly` — Mutation Prevention

Signal immutability intent and prevent side effects in shared state:

```typescript
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
  readonly retryPolicy: readonly ['immediate', 'exponential'];
}

// readonly is SHALLOW — object properties of readonly fields can still mutate
interface DeepConfig {
  readonly nested: { value: string }; // nested.value can still be mutated!
}

// For deep immutability: use as const or Readonly<T> / ReadonlyArray<T>
type DeepReadonly<T> = { readonly [K in keyof T]: DeepReadonly<T[K]> };
```

## Additional Resources

For detailed patterns and advanced techniques, consult:
- **`references/narrowing-guide.md`** — Comprehensive guide to all narrowing techniques with edge cases
- **`references/discriminated-unions.md`** — Advanced discriminated union patterns including state machines and event systems
