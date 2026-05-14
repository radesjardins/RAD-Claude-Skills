# Agent Operating Manual

## Project

Wayfinder is a weather-aware trip planning tool that recommends optimal travel windows for outdoor activities by combining real-time forecast data with user-defined activity constraints.

## Read order

- Before implementation, read `docs/status.md` and `docs/planning/current.md`.
- Read `docs/architecture.md` before any structural, cross-cutting, or multi-file change.
- Read `docs/vision.md` before changing user-facing behavior or product scope.
- Read `docs/decisions/` before revisiting choices already made.

## Hard boundaries

- Do not expand scope beyond `docs/planning/current.md`.
- Do not invent requirements. Record missing requirements under "Open questions" in `docs/planning/current.md`.
- Do not change package manager (bun), database schema, authentication model, or deployment strategy unless the current plan explicitly calls for it.
- Do not add a new dependency without explicit approval — record the proposal as a candidate ADR first.
- Do not silently replace an existing pattern with a new abstraction unless `docs/architecture.md` says to.

## Commands

- Install: `bun install`
- Dev server: `bun dev`
- Unit tests: `bun test`
- Lint: `bun run lint`
- Typecheck: `bun run typecheck`
- Build: `bun run build`

## Engineering rules

- Prefer the smallest change that satisfies the acceptance criteria.
- Reuse existing patterns before introducing new abstractions.
- When behavior changes, update tests in the same change set.
- When behavior or workflow changes, update the relevant docs in the same change set.
- If a decision becomes durable, record it in `docs/decisions/`.

## Definition of done

- The acceptance criteria in `docs/planning/current.md` are satisfied.
- Relevant validation commands have been run and results are recorded in `docs/status.md`.
- The diff stays within the stated scope and non-goals.
- New durable lessons are promoted into this operating manual, a path rule, or a skill when appropriate.

## Escalate instead of guessing

- Missing requirement or conflicting requirement
- Change would affect security, billing, auth, data model, or production operations
- Existing code patterns conflict with the current plan
- Validation fails and the fix requires scope expansion

## Compact Instructions

When using compact:
- preserve the current objective
- preserve non-goals and hard boundaries
- preserve acceptance criteria
- preserve the current list of changed files
- preserve latest validation commands and results
- preserve blockers, open questions, and next step
- drop superseded exploration paths and abandoned ideas
