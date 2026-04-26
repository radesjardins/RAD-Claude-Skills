# TypeScript Narrowing: Complete Guide

## How Control Flow Analysis Works

The TypeScript compiler performs Control Flow Analysis (CFA) — it builds a graph of every possible execution path through a function and tracks the type at each node. When you write `if (typeof x === 'string')`, the compiler knows that inside the branch, `x` is `string`, and outside (in the `else`), it's whatever remains.

CFA is not just for `if` statements — it works through `while`, `for`, `switch`, ternaries, and even early returns.

## Narrowing Techniques Reference

### 1. `typeof` Narrowing
Best for primitive types.

```typescript
type Input = string | number | boolean | null | undefined;

function process(input: Input): string {
  if (typeof input === 'string') return input.toUpperCase();
  if (typeof input === 'number') return input.toFixed(2);
  if (typeof input === 'boolean') return input ? 'yes' : 'no';
  if (input === null) return 'null';
  return 'undefined'; // TS knows: input is undefined here
}
```

### 2. Equality Narrowing
```typescript
function demo(x: string | number, y: string | boolean) {
  if (x === y) {
    // Both x and y must be string here (the only overlap)
    console.log(x.toUpperCase());
  }
}

// Null checks via equality:
function printName(name: string | null | undefined) {
  if (name != null) { // == null checks both null and undefined
    console.log(name.length); // string
  }
}
```

### 3. `instanceof` Narrowing
Best for class instances and error handling.

```typescript
class NetworkError extends Error {
  constructor(message: string, public statusCode: number) {
    super(message);
    this.name = 'NetworkError';
  }
}

class ValidationError extends Error {
  constructor(message: string, public field: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

function handleError(err: unknown): void {
  if (err instanceof NetworkError) {
    console.error(`Network ${err.statusCode}: ${err.message}`);
    return;
  }
  if (err instanceof ValidationError) {
    console.error(`Validation on ${err.field}: ${err.message}`);
    return;
  }
  if (err instanceof Error) {
    console.error(`Error: ${err.message}`);
    return;
  }
  console.error('Unknown error:', err);
}
```

### 4. `in` Operator Narrowing
Best for checking object shape/structure.

```typescript
interface Circle { kind: 'circle'; radius: number; }
interface Square { kind: 'square'; side: number; }
interface Triangle { kind: 'triangle'; base: number; height: number; }

type Shape = Circle | Square | Triangle;

function getPerimeter(shape: Shape): number {
  if ('radius' in shape) {
    return 2 * Math.PI * shape.radius; // shape: Circle
  }
  if ('side' in shape) {
    return 4 * shape.side; // shape: Square
  }
  return shape.base + 2 * Math.sqrt((shape.height ** 2) + (shape.base / 2) ** 2); // shape: Triangle
}
```

**Note on `in` with TS 4.9+:** The compiler now safely narrows properties not in the listed types by intersecting with `Record<'key', unknown>`.

### 5. Type Predicates (User-Defined Guards)
Best for complex validation logic that needs to be reusable.

```typescript
// Pattern: guard receives unknown, returns type predicate
function isStringArray(value: unknown): value is string[] {
  return (
    Array.isArray(value) &&
    value.every(item => typeof item === 'string')
  );
}

// More complex: API response guard
interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
}

function isPaginatedResponse<T>(
  value: unknown,
  isItem: (v: unknown) => v is T
): value is PaginatedResponse<T> {
  if (typeof value !== 'object' || value === null) return false;
  const obj = value as Record<string, unknown>;
  return (
    Array.isArray(obj.data) &&
    obj.data.every(isItem) &&
    typeof obj.total === 'number' &&
    typeof obj.page === 'number' &&
    typeof obj.pageSize === 'number'
  );
}
```

### 6. Assertion Functions
For invariant checks at the start of a function. Throws if the condition fails, narrowing for subsequent code.

```typescript
function assertIsString(val: unknown, name: string): asserts val is string {
  if (typeof val !== 'string') {
    throw new TypeError(`Expected ${name} to be string, got ${typeof val}`);
  }
}

function processConfig(config: unknown) {
  assertIsString((config as any)?.name, 'config.name');
  // config.name is string from here forward
}
```

## CFA Edge Cases

### Early Returns as Narrowing
```typescript
function getUserName(user: User | null): string {
  if (!user) return 'Anonymous'; // Narrows away null
  return user.name; // user: User
}
```

### Narrowing in Loops
CFA resets at each loop iteration — don't assume narrowing from a previous iteration persists.

```typescript
let value: string | number = getValue();

while (shouldContinue()) {
  // value is string | number — not narrowed from outside
  if (typeof value === 'string') {
    value = value.length; // Re-assign changes type!
  }
  // value is now string | number again
}
```

### Assignment Narrowing
TypeScript tracks assignments and narrows accordingly:

```typescript
let id: string | number;
id = getStringId();
console.log(id.toUpperCase()); // OK — id narrowed to string
id = getNumericId();
console.log(id.toFixed()); // OK — id narrowed to number
```

### Object Property Narrowing
Note: TypeScript does NOT narrow mutable object properties across function calls (potential mutations).

```typescript
interface Response {
  data?: string;
}

function process(res: Response) {
  if (res.data) {
    doSomething(res); // Could mutate res.data!
    console.log(res.data.length); // TypeScript still considers res.data possibly undefined
  }
}

// Fix: Capture in local variable
function processSafe(res: Response) {
  const { data } = res;
  if (data) {
    doSomething(res);
    console.log(data.length); // data is narrowed — local variable can't be mutated externally
  }
}
```

## TS 5.5: Inferred Type Predicates

TypeScript 5.5 allows the compiler to infer type predicates from function return logic:

```typescript
// Before TS 5.5 — needed explicit predicate
const hasValue = <T>(x: T | null | undefined): x is T => x !== null && x !== undefined;
const numbers = [1, null, 2, undefined, 3].filter(hasValue); // number[]

// TS 5.5+ — inferred automatically
const numbers = [1, null, 2, undefined, 3].filter(x => x !== null && x !== undefined); // number[]

// Also inferred for named functions:
function isNonEmpty(arr: unknown[]): arr is [unknown, ...unknown[]] {
  return arr.length > 0; // Inferred predicate
}
```

## `never` for Exhaustiveness Patterns

```typescript
// Helper function — always use this pattern
function assertNever(value: never, message?: string): never {
  throw new Error(message ?? `Unexpected value: ${JSON.stringify(value)}`);
}

// Use in exhaustive switches
type Direction = 'north' | 'south' | 'east' | 'west';

function move(direction: Direction): [number, number] {
  switch (direction) {
    case 'north': return [0, 1];
    case 'south': return [0, -1];
    case 'east': return [1, 0];
    case 'west': return [-1, 0];
    default: return assertNever(direction);
  }
}

// Use in conditional chains
function processStatus(status: 'active' | 'inactive' | 'pending') {
  if (status === 'active') { /* ... */ }
  else if (status === 'inactive') { /* ... */ }
  else if (status === 'pending') { /* ... */ }
  else {
    const _exhaustive: never = status; // Compile error if new status added
    throw new Error(`Unhandled: ${_exhaustive}`);
  }
}
```
