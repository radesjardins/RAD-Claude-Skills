---
name: typescript-modern-features
description: >
  This skill should be used when working with TypeScript 4.9 through 5.7 features, using
  the satisfies operator, const type parameters, inferred type predicates, verbatimModuleSyntax,
  isolated declarations, or targeting ES2024. Trigger on: "satisfies operator", "const type
  parameter", "TypeScript 5.0", "TypeScript 5.5", "TypeScript 5.7", "inferred type predicate",
  "verbatimModuleSyntax", "es2024 target", "TypeScript 4.9 features", "using declaration",
  "override keyword", "TypeScript new features", "import type syntax", "isolatedDeclarations",
  "Promise.withResolvers", "satisfies vs as", "satisfies vs annotation".
---

# TypeScript Modern Features (4.9 — 5.7)

These features fundamentally change how type-safe code is written. Understanding them prevents the use of less-safe older patterns.

## `satisfies` Operator (TypeScript 4.9)

`satisfies` validates conformance to a type **without widening the inferred type**. This resolves the tension between type checking and autocomplete specificity.

```typescript
type PaletteColor = string | number[];
type Palette = Record<string, PaletteColor>;

// ❌ Type annotation — loses literal key types and specific value types
const palette: Palette = {
  red: [255, 0, 0],
  green: '#00ff00',
  blue: [0, 0, 255],
};
palette.red;       // Type: PaletteColor (lost the fact it's number[])
palette.nonexist;  // No error! (extra keys allowed in Record)

// ✅ satisfies — validates AND preserves specific types
const palette = {
  red: [255, 0, 0],
  green: '#00ff00',
  blue: [0, 0, 255],
} satisfies Palette;
palette.red;        // Type: number[] (preserved!)
palette.green;      // Type: string (preserved!)
palette.nonexist;   // Error! 'nonexist' doesn't exist
palette.red.map(v => v * 2); // Works — TypeScript knows it's number[]
```

### When to Use `satisfies`
- Configuration objects (theme palettes, route maps, feature flags)
- Lookup tables and static data
- Any object where you need both type validation AND key/value autocomplete
- Replace `as const` when you need the type constraint too

```typescript
// Route configuration
type RouteConfig = { path: string; auth: boolean; component: React.FC };

const routes = {
  home: { path: '/', auth: false, component: HomePage },
  dashboard: { path: '/dashboard', auth: true, component: DashboardPage },
} satisfies Record<string, RouteConfig>;

routes.home.path;          // '/': string (specific, not just string)
routes.nonexistent;        // Error! Catches typos
```

## `const` Type Parameters (TypeScript 5.0)

Enables automatic literal type inference for generic function arguments — without requiring `as const` at call sites.

```typescript
// Problem: generics widen literal types
function createRoutes<T extends readonly string[]>(routes: T): T {
  return routes;
}
const routes = createRoutes(['/home', '/about']); // Type: string[] (widened!)

// Before TS 5.0: callers had to add `as const`
const routes = createRoutes(['/home', '/about'] as const);

// TS 5.0+ solution: add `const` to the type parameter
function createRoutes<const T extends readonly string[]>(routes: T): T {
  return routes;
}
const routes = createRoutes(['/home', '/about']); // Type: readonly ['/home', '/about']
```

### Key Use Cases
- Configuration arrays
- Event name registries
- Generic utilities that need literal inference
- Discriminated union factories

```typescript
// Type-safe event registry — no as const needed at call sites
function createEventEmitter<const Events extends readonly string[]>(events: Events) {
  type EventName = Events[number];
  const handlers = new Map<EventName, Set<() => void>>();

  return {
    on: (event: EventName, handler: () => void) => { /* ... */ },
    emit: (event: EventName) => { /* ... */ },
  };
}

const emitter = createEventEmitter(['click', 'hover', 'focus']);
emitter.on('click', () => {}); // 'click' autocompleted and type-checked
emitter.on('invalid', () => {}); // Error! 'invalid' not in ['click','hover','focus']
```

## Inferred Type Predicates (TypeScript 5.5)

TypeScript 5.5 automatically infers return type predicates from function logic — eliminating boilerplate in `.filter()` and other filtering operations.

```typescript
// Before TS 5.5: manual predicate required
function isString(x: string | null): x is string {
  return x !== null;
}
const strings = ['a', null, 'b'].filter(isString); // string[]

// TS 5.5+: inferred automatically
const strings = ['a', null, 'b'].filter(x => x !== null); // string[] — inferred!

// Works for complex predicates too
function hasName(obj: { name?: string }): obj is { name: string } {
  return obj.name !== undefined; // Predicate inferred from logic
}

const users = potentialUsers.filter(hasName); // Inferred { name: string }[]

// Inline predicates in .filter()
const activeUsers = users.filter(
  (user): user is ActiveUser => user.status === 'active'
); // Can still be explicit when needed
```

## Isolated Declarations (TypeScript 5.5)

`isolatedDeclarations` requires that all public API types can be inferred without cross-file analysis — enabling parallel declaration emit for faster builds.

```json
{ "compilerOptions": { "isolatedDeclarations": true } }
```

```typescript
// Error with isolatedDeclarations — return type requires cross-file inference
export function getUser(id: string) { // Error! Must annotate return type
  return db.users.findById(id);
}

// Correct — explicit return type annotation
export async function getUser(id: string): Promise<User | null> {
  return db.users.findById(id);
}
```

This enforces a best practice: all exported functions have explicit return types, which also prevents silent contract changes.

## TypeScript 5.7: ES2024 Target and `--target es2024`

```json
{
  "compilerOptions": {
    "target": "es2024",
    "lib": ["es2024"]
  }
}
```

Enables native type-safe support for:

```typescript
// Promise.withResolvers — create deferred promises cleanly
const { promise, resolve, reject } = Promise.withResolvers<string>();
setTimeout(() => resolve('done'), 1000);
const result = await promise; // 'done'

// Object.groupBy — group arrays by key
const grouped = Object.groupBy(users, user => user.role);
// grouped.admin: User[] | undefined
// grouped.user: User[] | undefined

// Array.fromAsync — async iterable to array
const results = await Array.fromAsync(asyncGenerator());
```

## `verbatimModuleSyntax` (TypeScript 4.5+, critical for ESM)

Ensures `import type` is used for type-only imports and they are fully erased:

```typescript
// Required with verbatimModuleSyntax:
import type { User, Product } from './types'; // Erased — never in output
import { createUser } from './api';            // Kept — needed at runtime

// Inline form (preferred):
import { createUser, type User, type Product } from './api';

// Why this matters:
// esbuild/swc transform files individually without type analysis.
// A regular import of a type-only export produces an empty runtime import.
// In strict ESM, empty imports of non-existent files crash the process.
```

## `override` Keyword (TypeScript 4.3, required by `noImplicitOverride`)

```typescript
class Animal {
  speak(): string { return 'Generic sound'; }
  move(): void { console.log('Moving'); }
}

class Dog extends Animal {
  override speak(): string { return 'Woof'; } // Verified: Animal has speak()
  // override bark(): string { ... }          // Error! Animal has no bark()
}

// If Animal.speak() is renamed to makeSound():
// override speak() → Compile error — no longer exists in base
// Protects against silent broken overrides after refactoring
```

## TypeScript 4.9: `satisfies` and `in` Narrowing Improvements

```typescript
// Improved in operator — narrows to Record<'key', unknown> intersection
function processInput(input: string | { message: string }) {
  if ('message' in input) {
    // TS 4.9+: input is narrowed to string & Record<'message', unknown>
    // (not just { message: string })
    console.log(input.message);
  }
}
```

## Additional Resources

For comprehensive feature documentation, consult:
- **`references/ts5x-features.md`** — Full changelog of TypeScript 5.0–5.7 features with migration guidance
