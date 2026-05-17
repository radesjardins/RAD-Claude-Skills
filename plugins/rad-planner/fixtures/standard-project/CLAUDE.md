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

## Lanes

Role separation between human and agent. This contract applies to every session — planning, coding, review, anything else.

### What you (the human) decide

- Product boundaries — what's in scope, what isn't
- User value — who the product is for, what they need
- Pricing, monetization, business model
- Ethics posture and policy
- Feature priority and ordering
- What gets deferred or parked
- Whether any agent suggestion changes the product
- All changes to vision.md and the operating manual's Hard boundaries

### What the agent may do during PLANNING

- Identify gaps in existing plans or docs
- Propose implementation sequences and milestones
- Find contradictions between docs (vision vs current.md, plan vs status)
- Draft acceptance criteria for human review
- Generate test-case skeletons
- Summarize trade-offs of competing approaches
- Suggest simpler alternatives when complexity looks unjustified

### What the agent may do during CODING

- Implement only the current milestone — nothing more
- Avoid unrelated refactors
- Update docs ONLY when explicitly instructed
- Write tests for the milestone being implemented
- Report blockers instead of inventing scope to work around them
- Ask before changing user-visible product behavior

### What the agent must NOT do

- Add new major features mid-milestone (even if "small")
- Reinterpret the product vision or change vision.md
- Revive retired or parked frames without explicit user approval
- Change pricing, tier, or monetization logic
- Replace source authority (the canonical docs) with model judgment
- "Improve" the architecture outside the current milestone's scope
- Refactor unrelated modules because they "looked off"
- Add dependencies outside the active milestone's dependency cone
- Skip stop conditions to make progress

### When in doubt

Stop and ask. The cost of pausing is low; the cost of an unwanted product change is high. Use the milestone's "Stop conditions" section in `docs/planning/current.md` as the primary check — and when none of those fire but something still feels load-bearing, ask anyway.

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
