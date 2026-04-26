# TypeScript Anti-Patterns: Code Review Checklist

Use this checklist when reviewing TypeScript code — whether human-written or AI-generated.

## Level 1: Compiler Bypasses (Critical)

### `any` Usage
- [ ] No explicit `any` annotations (`let x: any`, `function f(arg: any)`)
- [ ] No implicit `any` (caught by `noImplicitAny`)
- [ ] No `as any` intermediary in double assertions (`value as any as Target`)
- [ ] `JSON.parse()` result is passed through Zod, not cast with `as`
- [ ] `fetch()` response `.json()` is parsed with schema, not cast

**Grep pattern:** `\bany\b`, `as any`, `as unknown as`

### Non-Null Assertions
- [ ] No `!` on values from external sources
- [ ] No chained `!` operators (`obj!.nested!.value!`)
- [ ] No `querySelector(...)!` without a fallback check
- [ ] Each `!` usage has a comment explaining why the value is guaranteed non-null

**Grep pattern:** `[a-zA-Z0-9)>]\!\.`, `[a-zA-Z0-9)>]\!;`

### Type Assertions (`as Type`)
- [ ] No `as Type` on API response data (use Zod instead)
- [ ] No `as Type` on `unknown` variables (use type guard instead)
- [ ] No object literal assertions bypassing excess property checks
- [ ] `as const` is used correctly for immutability (this is fine)
- [ ] `satisfies` is used instead of annotation for config objects

**Grep pattern:** `\) as (?!const)`, `\] as (?!const)`, `\} as (?!const)`

### `@ts-ignore` and `@ts-expect-error`
- [ ] No `@ts-ignore` without documented justification
- [ ] `@ts-expect-error` only for known third-party type issues with clear comment
- [ ] Consider filing a bug/issue instead of suppression

**Grep pattern:** `@ts-ignore`, `@ts-expect-error`

---

## Level 2: Error Handling (High Priority)

### Catch Blocks
- [ ] No empty `catch {}` blocks
- [ ] No `catch (e: any)` — use `unknown`
- [ ] `useUnknownInCatchVariables` enabled in tsconfig
- [ ] All `catch` blocks either handle the error or rethrow with context
- [ ] Errors are classified (transient/correctable/permanent/fatal) where appropriate

**Grep pattern:** `catch\s*\{\s*\}`, `catch.*:\s*any`

### Promise Handling
- [ ] No floating promises (unhandled `async` function calls without `await`)
- [ ] `@typescript-eslint/no-floating-promises` enabled
- [ ] No `.catch(console.error)` — this hides the error from callers

### Zod Error Handling
- [ ] `.safeParse()` used, not `.parse()`, at API boundaries
- [ ] `result.success` checked before accessing `result.data`
- [ ] `result.error.flatten()` used for user-facing error messages

---

## Level 3: Type Design (Medium Priority)

### Union Types
- [ ] Discriminated unions use a `kind`/`type` literal discriminant
- [ ] No optional properties to differentiate union members
- [ ] Exhaustive `switch` statements with `assertNever` in the default case
- [ ] State machines modeled as discriminated unions (not boolean flags)

### Generics
- [ ] No more than 3 generic type parameters per function/type
- [ ] All generic parameters can be inferred (no required explicit `<Type>` at call sites)
- [ ] Generic constraints use `extends` to narrow the domain
- [ ] No recursive generics for simple data transformations

### Enums
- [ ] No numeric enums (auto-incrementing `enum Foo { A, B, C }`)
- [ ] Prefer string literal unions over string enums
- [ ] `as const` on arrays for runtime + type derivation
- [ ] `const enum` only if bundler supports it (not with esbuild/swc)

---

## Level 4: Module Safety (Medium Priority)

### Imports
- [ ] `import type` for type-only imports
- [ ] No circular import dependencies
- [ ] Shared types come from a single source of truth (not duplicated)
- [ ] No barrel files (`index.ts` re-exporting everything) in hot paths

### Exports
- [ ] No exported mutable arrays (`export const items: Item[] = []`)
- [ ] No exported mutable plain objects
- [ ] Mutable state exposed through controlled functions
- [ ] `Object.freeze()` on exported constants

### Monorepo
- [ ] Types shared from `@org/shared` package, not duplicated
- [ ] Zod schemas exported alongside `z.infer` types
- [ ] No `any` in shared package types
- [ ] No backend-only types in shared package (use `.universal.ts` suffix)

---

## Level 5: Performance & Maintainability

### Type Complexity
- [ ] No types that take >1s to check (watch for conditional type chains)
- [ ] Mapped types are readable and have clear intent
- [ ] Utility types used appropriately (`Pick`, `Omit`, `Partial`, `Required`)
- [ ] `Partial<T>` not used where `T | undefined` is more accurate

### `readonly`
- [ ] Immutable data uses `readonly` modifier or `ReadonlyArray<T>`
- [ ] Shallow `readonly` pitfalls acknowledged (nested objects still mutable)
- [ ] `as const` used for deep literal immutability

---

## Quick Reference: What to Grep For

```bash
# any usage
grep -rn '\bany\b' src/ --include="*.ts"

# Non-null assertions (excluding test files)
grep -rn '![\.\[]' src/ --include="*.ts" --exclude="*.test.ts"

# Type assertions (excluding as const)
grep -rn ' as ' src/ --include="*.ts" | grep -v 'as const'

# Suppression comments
grep -rn '@ts-ignore\|@ts-expect-error' src/ --include="*.ts"

# Empty catch blocks
grep -rn 'catch\s*{' src/ --include="*.ts"

# .parse() (should be .safeParse())
grep -rn '\.parse(' src/ --include="*.ts" | grep -v '\.safeParse\|test\|spec'

# Floating promises (basic heuristic)
grep -rn '^\s*fetch\|^\s*axios\|^\s*db\.' src/ --include="*.ts" | grep -v 'await\|return'
```
