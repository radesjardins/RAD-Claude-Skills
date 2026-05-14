# Architecture

## Current stack

- Language: TypeScript (strict mode)
- Framework: Next.js 15 (app router)
- Package manager: bun
- Test framework: bun test (built-in)
- Lint / format: biome
- Build / deploy: Vercel (preview + prod)
- Data store: Postgres via Drizzle ORM
- External services: Visual Crossing Weather API

## Repository map

- `app/`: Next.js app router pages and route handlers
- `lib/`: shared business logic (weather adapter, activity-constraint engine, trip-evaluation)
- `lib/weather/`: provider abstraction + Visual Crossing adapter
- `lib/db/`: Drizzle schema + migrations
- `tests/`: integration + unit tests (colocated unit tests live next to their target files)
- `scripts/`: build and deployment helpers

## System boundaries

- This repo owns: web UI, weather data adapter, trip-evaluation engine, user data
- This repo does not own: payment processing (deferred), notifications (future v4.1), mobile-native code (out of scope)
- Upstream dependencies: Visual Crossing API
- Downstream dependencies: none yet (consumer-facing only)

## Core invariants

- User-defined activity constraints are stored per-user; never inferred from defaults
- Every weather query is cached for at most 1 hour (per Visual Crossing terms)
- All times in storage and API are UTC; conversion to user timezone happens at render

## Canonical patterns

- For API handlers: use Drizzle for data access; never raw SQL
- For state management: server components by default; client components only for interactive widgets
- For logging and errors: structured JSON logs via the shared logger module; user-facing errors via the error-boundary component
- For database access: queries live in `lib/db/queries/`; never inline in route handlers

## Commands agents should know

- Narrowest test command: `bun test <path>`
- Full test command: `bun test`
- Lint: `bun run lint`
- Typecheck: `bun run typecheck`
- Build: `bun run build`
- Local smoke test: `bun dev` then visit http://localhost:3000

## Secrets and environment

- Required env vars: `DATABASE_URL`, `VISUAL_CROSSING_API_KEY`
- Never read or print: API key (it leaks in logs if not careful)
- Mock or local substitutes: `lib/weather/__fixtures__/` for offline test runs

## Known sharp edges

- Visual Crossing free tier limits: 1000 records/day — production load testing will need a paid plan
- Drizzle migrations are not auto-applied on Vercel preview deploys; run `bun db:migrate` manually after schema changes

## Change notes

Update this file when stack, invariants, boundaries, or canonical patterns change.
