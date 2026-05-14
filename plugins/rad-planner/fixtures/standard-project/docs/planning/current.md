# Current Plan

## Objective

Ship the M2 milestone: user-defined activity constraints with per-constraint evaluation against weather forecasts. By end of M2, a user can define a constraint set (e.g., "clear visibility, wind <15mph, temp 50–75°F") and see go/no-go decisions for the next 7 days against a chosen location.

## Why this matters

M1 shipped the basic weather lookup. Without constraint-based evaluation (M2), the tool is no better than a weather app. M2 is the milestone where Wayfinder becomes useful for trip-planning, not just weather-viewing.

## Non-goals

- Not adding social features (sharing/comments) — those are v3 or later
- Not auto-inferring constraints from activity type — explicit user-defined only

## Current milestone

M2: Activity-constraint engine + per-constraint go/no-go evaluation

## Acceptance criteria

- [x] User can create a named constraint set with at least 5 constraint types (visibility, wind, temp range, precipitation, time-of-day)
- [ ] Constraint evaluator returns per-day go/no-go for the next 7-day forecast
- [ ] Failure reasons are surfaced (which constraint failed, by how much)
- [ ] UI handles 1+ constraint sets per user; selection at evaluation time
- [ ] Visual Crossing rate-limit handling: graceful degradation with cached data when over quota

## Validation commands

- `bun test lib/constraints/` — constraint evaluator unit tests
- `bun test tests/integration/m2-flow.test.ts` — end-to-end constraint creation + evaluation
- `bun run typecheck` — strict type-checking passes
- `bun run lint` — biome lint passes

## Planned changes

- [x] `lib/constraints/types.ts` — constraint type definitions
- [x] `lib/constraints/evaluator.ts` — per-day evaluation logic
- [ ] `lib/constraints/queries.ts` — CRUD via Drizzle
- [ ] `app/constraints/page.tsx` — constraint-set CRUD UI
- [ ] `app/evaluate/[constraint-set-id]/page.tsx` — evaluation results UI

## Open questions

- How to handle partial constraint matches (some satisfied, some not)? Show overall go/no-go with breakdown, or per-constraint scoring? Lean toward go/no-go + breakdown.
- Default constraint sets shipped with the product, or onboarding-only?

## Risks

- Risk: Visual Crossing API changes pricing tier mid-M2
  - Mitigation: cache layer + ability to swap provider via the weather adapter abstraction
- Risk: constraint evaluation becomes a performance hot spot at >7 days lookahead
  - Mitigation: server-side eval + client-side caching of evaluation results per constraint-set-id

## Stop conditions

Stop and ask for approval if:

- Scope must expand beyond the 5 constraint types listed
- A new dependency must be added beyond what's in package.json
- A schema or contract must change (especially `constraint_sets` or `user_preferences` tables)
- Validation exposes a requirement conflict
- The constraint-evaluator API surface needs to change in a way that affects existing M1 callers

## Notes for the next session

- Most likely next step: implement `lib/constraints/queries.ts` (the Drizzle CRUD layer) since the evaluator is done and the UI needs persistence to connect
- Files likely to change: `lib/constraints/queries.ts`, `lib/db/schema.ts` (add `constraint_sets` table), `lib/db/migrations/0003_*.sql`
- What must remain true: existing weather adapter (`lib/weather/`) keeps working untouched; M1 lookup flow stays intact
