# Decision 0001

## Title

Use TypeScript strict mode across the entire codebase

## Status

Accepted

## Date

2026-04-22

## Context

The codebase started with TypeScript but `strict: false` in `tsconfig.json` to ease early prototyping. As M1 approached completion, several runtime errors traced back to `null` values that strict mode would have caught at compile time. We need to decide whether to leave strict mode off (faster prototyping, more runtime risk) or flip it on (slower iteration on existing files, much safer).

## Decision

Enable `strict: true` in `tsconfig.json` for the entire project. Fix existing type errors during M1 cleanup, before M2 begins.

## Why

The cost of fixing existing type errors was bounded (~12 files, ~2 hours of work). The cost of *not* having strict mode compounds with every new file. Strict mode catches a class of bugs that the team would otherwise spend time debugging at runtime. Given Wayfinder's product principle "trust requires transparency," surfacing type errors at compile time aligns with our reliability bar.

## Alternatives considered

- Option: Leave strict mode off; rely on runtime tests
  - Why rejected: Tests catch fewer bugs than strict types in TS; runtime debugging is more expensive than compile-time fixing.
- Option: Enable strict mode per-file via `// @ts-strict` comments
  - Why rejected: Adds opt-in friction; new files would inherit strict mode anyway; partial enforcement creates an inconsistent codebase.

## Consequences

- Positive: Compile-time catches for `null` / `undefined` errors; type errors surface during `bun run typecheck` in CI before deploy.
- Positive: New contributors land in a strict-mode codebase from day one — no "we'll turn it on later" debt.
- Negative: Existing files needed updates (mostly added `!` non-null assertions where the runtime guarantee held, and proper null checks where it didn't).
- Follow-up work: None. Strict mode is now the baseline.

## Related files

- `tsconfig.json`
- `lib/weather/adapter.ts` (was the highest-error file pre-strict; cleaned up during the flip)

## Supersedes or related decisions

- None (first decision).
