---
name: typescript-strict-mode
description: >
  This skill should be used when configuring TypeScript projects, creating or reviewing
  tsconfig.json, enabling strict mode, asking what TypeScript compiler flags do, setting up
  a new TypeScript project for production, or reviewing existing TypeScript configuration.
  Trigger on: "configure tsconfig", "enable strict mode", "what does strictNullChecks do",
  "noUncheckedIndexedAccess", "exactOptionalPropertyTypes", "verbatimModuleSyntax",
  "TypeScript configuration best practices", "strict mode options", "tsconfig for production",
  "compiler options", "noImplicitAny", "useUnknownInCatchVariables", "noImplicitOverride".
---

# TypeScript Strict-Mode Configuration

The TypeScript compiler configuration is the project's constitutional framework. `strict: true` activates a suite of sub-options that collectively enforce a "narrow corridor" of logic—making it structurally difficult for developers or AI agents to introduce common classes of runtime bugs.

## The Non-Negotiable Production tsconfig.json

Every production TypeScript project requires the following minimum configuration:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "verbatimModuleSyntax": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "target": "es2024",
    "lib": ["es2024"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true
  }
}
```

> `strict: true` already enables: `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitThis`, `useUnknownInCatchVariables`, and `alwaysStrict`. The additional options above extend that baseline.

## Critical Flags and What They Prevent

### `strictNullChecks` — Eliminates the Billion-Dollar Mistake
Removes `null` and `undefined` from the domain of all other types. Forces explicit handling of potential absences.

```typescript
// Without strictNullChecks — silent runtime crash
const user = users.find(u => u.id === id);
console.log(user.name); // Crashes if not found

// With strictNullChecks — compiler forces handling
const user = users.find(u => u.id === id);
if (!user) throw new Error(`User ${id} not found`);
console.log(user.name); // Safe
```

### `noUncheckedIndexedAccess` — NOT in `strict`, MUST add explicitly
Appends `| undefined` to any array index or record string-key access. This is the single most impactful flag not in `strict`.

```typescript
const items = ['a', 'b', 'c'];
const first = items[0]; // Type: string | undefined

const record: Record<string, number> = { a: 1 };
const val = record['a']; // Type: number | undefined

// Force handling before use:
if (first !== undefined) {
  console.log(first.toUpperCase()); // Safe
}
```

### `exactOptionalPropertyTypes` — NOT in `strict`, MUST add explicitly
Distinguishes between a property being absent and being present with `undefined`. Prevents subtle bugs in object spreading and API payload construction.

```typescript
interface Config {
  theme?: 'dark' | 'light';
}

// Not allowed with exactOptionalPropertyTypes:
const config: Config = { theme: undefined }; // Error!

// Correct — property simply absent:
const config: Config = {};
```

### `useUnknownInCatchVariables` (in `strict` since TS 4.4)
Changes caught error type from `any` to `unknown`. Forces type verification before accessing error properties.

```typescript
try {
  await fetchUser(id);
} catch (err) {
  // err is unknown — must narrow
  if (err instanceof Error) {
    console.error(err.message);
  }
}
```

### `noImplicitOverride` — NOT in `strict`, MUST add explicitly
Enforces the `override` keyword in class inheritance. Prevents accidental method shadowing after base class refactoring.

### `verbatimModuleSyntax` — NOT in `strict`, MUST add explicitly
Ensures type-only imports use `import type` and are erased at compile time. Required for esbuild, swc, and ESM environments.

```typescript
import type { User } from './types';         // Erased
import { createUser } from './api';           // Kept
import { createUser, type User } from './api'; // Inline form also valid
```

## Flags Quick Reference

| Flag | In `strict`? | Catches |
|------|-------------|---------|
| `strictNullChecks` | ✅ | Null/undefined access crashes |
| `noImplicitAny` | ✅ | Silent any leakage |
| `strictFunctionTypes` | ✅ | Unsafe callback assignments |
| `strictPropertyInitialization` | ✅ | Uninitialized class properties |
| `useUnknownInCatchVariables` | ✅ | Unsafe `any` catch variables |
| `noUncheckedIndexedAccess` | ❌ Add | Unsafe array/record access |
| `exactOptionalPropertyTypes` | ❌ Add | Optional property misuse |
| `noImplicitOverride` | ❌ Add | Accidental method shadowing |
| `verbatimModuleSyntax` | ❌ Add | Type-import erasure bugs |
| `noImplicitReturns` | ❌ Add | Missing return paths |
| `noFallthroughCasesInSwitch` | ❌ Add | Switch fallthrough |

## Modern Target Configuration

Enable modern ECMAScript with full type safety:

```json
{
  "target": "es2024",
  "lib": ["es2024"],
  "module": "NodeNext",
  "moduleResolution": "NodeNext"
}
```

Unlocks native `Promise.withResolvers`, `Object.groupBy`, and other ES2024 APIs with compiler-verified types.

## Monorepo Project References

For monorepos, use TypeScript project references for incremental builds:

```json
{
  "references": [
    { "path": "../packages/shared" },
    { "path": "../packages/api" }
  ],
  "compilerOptions": {
    "composite": true,
    "declarationMap": true
  }
}
```

## The Interaction That Creates Maximum Safety

`strictNullChecks` + `noUncheckedIndexedAccess` together form the most powerful combination: every array access becomes `T | undefined`, and the compiler forces proof of existence at the origin—shifting the burden from consumers to producers.

## Additional Resources

For complete details, consult:
- **`references/tsconfig-reference.md`** — Full option reference with production examples and monorepo patterns
- **`references/eslint-rules.md`** — Complementary ESLint/typescript-eslint rules that extend compiler enforcement into runtime patterns
