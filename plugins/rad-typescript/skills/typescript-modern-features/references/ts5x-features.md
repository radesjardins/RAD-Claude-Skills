# TypeScript 4.9 → 5.7 Feature Reference

## TypeScript 4.9 (Nov 2022)

### `satisfies` Operator
Validates conformance without widening. See SKILL.md for full details.

### Improved `in` Narrowing
```typescript
// When checking for a property not in the union, TypeScript intersects
// with Record<string, unknown> instead of giving up
function check(value: string | { data: unknown }) {
  if ('data' in value) {
    value; // string & Record<'data', unknown> | { data: unknown }
  }
}
```

### `Awaited<T>` Type Improvements
More accurate type for `Promise.resolve()`:
```typescript
async function fetchData<T>(p: Promise<T>): Promise<T> {
  return p; // Previously might return Awaited<T>
}
```

---

## TypeScript 5.0 (Mar 2023)

### `const` Type Parameters
```typescript
// Infer literal types in generics without `as const` at call sites
function identity<const T>(val: T): T { return val; }
const x = identity({ key: 'value' }); // Type: { readonly key: 'value' }
```

### Decorators (TC39 Stage 3)
```typescript
function logged<T extends { new(...args: any[]): {} }>(Base: T) {
  return class extends Base {
    constructor(...args: any[]) {
      console.log('Created');
      super(...args);
    }
  };
}

@logged
class Service {
  run() { return 'running'; }
}
```

### Multiple `extends` in Generics
```typescript
// Can now extend multiple types with comma-separated extends
type A = { a: string };
type B = { b: number };

function process<T extends A, T extends B>(val: T) { ... }
// Now: <T extends A & B>
```

### `--moduleResolution bundler`
For Vite, esbuild, webpack:
```json
{ "module": "ESNext", "moduleResolution": "Bundler" }
```

---

## TypeScript 5.1 (Jun 2023)

### Decoupled Return Types for Getters/Setters
```typescript
class State {
  private _value = 0;

  // Getter and setter can now have different types (must be related)
  get value(): number { return this._value; }
  set value(v: number | string) {
    this._value = typeof v === 'string' ? parseInt(v) : v;
  }
}
```

### Improved JSX Element Types
React 18 improvements for server components and async components.

---

## TypeScript 5.2 (Aug 2023)

### `using` Declaration (ECMAScript Explicit Resource Management)
```typescript
// Automatic resource cleanup via Symbol.dispose
class DatabaseConnection {
  [Symbol.dispose]() {
    this.close();
    console.log('Connection closed');
  }
}

// Automatically disposed at end of scope
{
  using conn = new DatabaseConnection();
  // Use conn...
} // conn.close() called automatically here

// Async version
async function withFile(path: string) {
  await using file = await openFile(path); // Symbol.asyncDispose
  // file automatically closed when scope exits
}
```

### `Symbol.hasInstance` narrowing improvements

---

## TypeScript 5.3 (Nov 2023)

### Import Attributes (`import ... with`)
```typescript
import data from './config.json' with { type: 'json' };
```

### `resolution-mode` in Import Types
```typescript
import type { User } from 'my-module' with { 'resolution-mode': 'import' };
```

---

## TypeScript 5.4 (Mar 2024)

### Preserved Narrowing in Closures
```typescript
function demo(value: string | undefined) {
  if (value !== undefined) {
    // TS 5.4: Narrowing preserved in closures when not assigned in closure
    const fn = () => value.toUpperCase(); // Previously: might be undefined
    fn(); // Safe!
  }
}
```

### `NoInfer<T>` Utility Type
Prevents inference from specific positions:
```typescript
function createState<T>(initial: T, reset: NoInfer<T>): [T, () => void] {
  let state = initial;
  return [state, () => { state = reset; }];
}

// T is inferred from `initial` only — `reset` must match
createState(0, 1); // T = number ✓
createState(0, 'x'); // Error! string not assignable to number
```

---

## TypeScript 5.5 (Jun 2024)

### Inferred Type Predicates
The compiler automatically infers type predicates from function return logic:
```typescript
// Array.filter now infers correctly:
const values = [1, null, 2, undefined, 3];
const numbers = values.filter(x => x !== null && x !== undefined);
// Type: number[] — inferred without explicit predicate
```

### Control Flow Narrowing for Constant Indexed Access
```typescript
function test(data: { [key: string]: boolean }) {
  const key = 'enabled';
  if (data[key]) {
    data[key]; // Type: boolean (true) — narrowed!
  }
}
```

### Isolated Declarations
```json
{ "isolatedDeclarations": true }
```
Requires explicit return types on exported functions for parallel declaration emit.

---

## TypeScript 5.6 (Sep 2024)

### Disallowed Nullish and Truthy Checks
```typescript
// Now errors — these checks are always true/false
if (new RegExp('hello')) { }  // Error: always truthy!
if (user?.email ?? true) { }  // Error: always true!
```

### Iterator Helpers
```typescript
// Native Iterator type with map, filter, take, etc.
function* range(start: number, end: number) {
  for (let i = start; i < end; i++) yield i;
}

const result = range(0, 10)
  .filter(n => n % 2 === 0)
  .map(n => n * 2)
  .take(3)
  .toArray(); // [0, 4, 8]
```

---

## TypeScript 5.7 (Nov 2024)

### `--target es2024` and `--lib es2024`
Full type support for:
```typescript
// Promise.withResolvers
const { promise, resolve, reject } = Promise.withResolvers<User>();
// Use: resolve(user) or reject(error) from anywhere

// Object.groupBy / Map.groupBy
const byStatus = Object.groupBy(orders, o => o.status);
// byStatus.pending: Order[] | undefined

// Array.fromAsync
const results = await Array.fromAsync(asyncIterable);
```

### Paths Without `baseUrl`
```json
{
  "compilerOptions": {
    // baseUrl no longer required when using paths
    "paths": {
      "@shared/*": ["packages/shared/src/*"]
    }
  }
}
```

### Checked Relative Import Paths in `.d.ts` Files
Declaration files now validate import paths at emit time.
