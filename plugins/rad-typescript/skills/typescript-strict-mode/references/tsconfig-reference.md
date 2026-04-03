# tsconfig.json Production Reference

Complete reference for TypeScript compiler options in production environments.

## Full Production tsconfig.json

```json
{
  "compilerOptions": {
    // === STRICTNESS ENGINE ===
    "strict": true,                        // Baseline: enables 8 sub-options
    "noUncheckedIndexedAccess": true,      // arr[i] → T | undefined
    "exactOptionalPropertyTypes": true,    // optional ≠ optional+undefined
    "noImplicitOverride": true,            // Explicit override keyword required
    "verbatimModuleSyntax": true,          // type imports must be marked
    "noImplicitReturns": true,             // All code paths must return
    "noFallthroughCasesInSwitch": true,    // Explicit fallthrough required
    "noPropertyAccessFromIndexSignature": true, // Bracket notation for index sigs

    // === MODULE SYSTEM (Node.js) ===
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "esModuleInterop": true,
    "resolveJsonModule": true,

    // === MODULE SYSTEM (Browser/Bundler) ===
    // "module": "ESNext",
    // "moduleResolution": "Bundler",

    // === TARGET ===
    "target": "es2024",
    "lib": ["es2024"],

    // === OUTPUT ===
    "outDir": "./dist",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,

    // === MONOREPO (add for composite packages) ===
    // "composite": true,
    // "incremental": true,

    // === QUALITY ===
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "skipLibCheck": false               // Set true only if dependency types are broken
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

## What `strict: true` Enables (Sub-Options)

| Sub-option | Mechanism | Prevents |
|-----------|-----------|---------|
| `noImplicitAny` | Disallows inferring `any` | Type blindness, unchecked logic |
| `strictNullChecks` | Null/undefined as separate types | NPE crashes, billion-dollar mistake |
| `strictFunctionTypes` | Contravariant parameter checking | Unsafe callback assignments |
| `strictBindCallApply` | Types `bind`, `call`, `apply` accurately | Mismatched `this` crashes |
| `strictPropertyInitialization` | Class properties must init in constructor | Accessing undefined properties |
| `noImplicitThis` | Disallows `this: any` | `this` context bugs in callbacks |
| `useUnknownInCatchVariables` | `catch (e)` defaults to `unknown` | Accessing `.message` on non-Error throws |
| `alwaysStrict` | Emits `"use strict"` in output | Legacy JS silent failures |

## Options NOT in `strict` — Must Add Explicitly

### `noUncheckedIndexedAccess`
Adds `| undefined` to all index signatures and array access.

```typescript
// Without: arr[0] is T
// With: arr[0] is T | undefined

const first = arr[0];
if (first !== undefined) {
  // Safe to use first here
}

// Use nullish coalescing for defaults:
const value = record[key] ?? defaultValue;

// Use non-null only when guaranteed (e.g., after length check):
if (arr.length > 0) {
  const first = arr[0]!; // Still bad — prefer conditional
}
```

### `exactOptionalPropertyTypes`
Makes `?:` mean "absent" strictly, not "absent OR undefined".

```typescript
interface Theme {
  color?: 'red' | 'blue';
}

// Without exact: { color: undefined } allowed
// With exact: { color: undefined } is a type error

// Pattern to check: use `'color' in obj` not `obj.color !== undefined`
function applyTheme(theme: Theme) {
  if ('color' in theme) {
    // theme.color is 'red' | 'blue' here (not undefined)
    applyColor(theme.color);
  }
}
```

### `verbatimModuleSyntax`
Enforces `import type` for type-only imports.

```typescript
// Required pattern:
import type { User, Product } from './types';
import { createUser } from './api';

// Or inline (preferred for mixed imports):
import { createUser, type User, type Product } from './api';

// Why it matters for bundlers:
// esbuild and swc do single-file transforms without type analysis.
// Without verbatimModuleSyntax, a regular import of a type-only
// entity produces an empty runtime import — which can crash in ESM.
```

### `noImplicitOverride`
Requires `override` keyword in subclasses.

```typescript
class Base {
  process(): void { /* ... */ }
}

class Child extends Base {
  override process(): void { // Compiler verifies this exists in Base
    super.process();
  }
}

// If Base.process() is renamed, the override keyword causes a compile error
// rather than a silent, broken shadow method.
```

## Module Resolution Guide

### For Node.js Applications
```json
{
  "module": "NodeNext",
  "moduleResolution": "NodeNext"
}
```
Requires `.js` extensions in imports (`import './utils.js'`), even for `.ts` source files.

### For Bundler-Based Apps (Vite, webpack, esbuild)
```json
{
  "module": "ESNext",
  "moduleResolution": "Bundler"
}
```
Allows extensionless imports. Bundler handles resolution.

### For CommonJS Libraries
```json
{
  "module": "CommonJS",
  "moduleResolution": "Node"
}
```

## Monorepo Configuration

### Root tsconfig.json (workspace)
```json
{
  "files": [],
  "references": [
    { "path": "packages/shared" },
    { "path": "packages/api" },
    { "path": "packages/web" }
  ]
}
```

### Package tsconfig.json
```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "composite": true,
    "declarationMap": true,
    "rootDir": "./src",
    "outDir": "./dist"
  },
  "references": [
    { "path": "../shared" }
  ]
}
```

### tsconfig.base.json (shared strict settings)
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "verbatimModuleSyntax": true,
    "target": "es2022",
    "lib": ["es2022"]
  }
}
```

## Path Aliases

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@shared/*": ["packages/shared/src/*"],
      "@api/*": ["packages/api/src/*"]
    }
  }
}
```

> Path aliases require bundler or ts-node path registration to work at runtime. TypeScript only handles them at type-check time.

## Common Errors and Fixes

| Error | Flag | Fix |
|-------|------|-----|
| `Object is possibly undefined` | strictNullChecks | Add null check or use `?.` |
| `Element implicitly has an 'any' type` | noUncheckedIndexedAccess | Check for `undefined` before use |
| `Type 'undefined' is not assignable` | exactOptionalPropertyTypes | Remove explicit `undefined`, omit property |
| `Property does not exist on base type` | noImplicitOverride | Add `override` keyword |
| `Cannot use import statement` | module/moduleResolution | Add `.js` extension or use bundler mode |
| `Argument of type 'unknown'` | useUnknownInCatchVariables | Narrow with `instanceof Error` |
