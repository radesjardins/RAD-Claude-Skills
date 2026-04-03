# Project CLAUDE.md Templates by Tech Stack

## Wrapper CLAUDE.md Template (Above Git)

```markdown
# {PROJECT_NAME} — Project Management

## Current Sprint
- Sprint start: {DATE}
- Goals: [List current sprint goals]
- Status: In Progress

## Architecture Decisions
- [Date]: [Decision and rationale]

## Agent Team
- **Architect**: Plans features and reviews structural changes
- **Implementer**: Writes production code following plans
- **Reviewer**: Audits code for bugs, security, and standards
- **Tester**: Writes and validates test coverage
- **Deployer**: Manages CI/CD and releases

## Active Task Specs
- See `task-specs/` for current task specifications
```

---

## Next.js + Express + PostgreSQL (Full-Stack)

### Repo CLAUDE.md

```markdown
# {PROJECT_NAME} — {COMPANY}

## Project overview
{DESCRIPTION}. Solo-founder company — all code review is done by one human.
Quality and test coverage are non-negotiable.

## Tech stack
- Frontend: Next.js 15, React 19, TypeScript 5.7, Tailwind CSS 4, Shadcn/ui
- Backend: Node.js 22, Express 5, TypeScript 5.7, Prisma ORM 6
- Database: PostgreSQL 17
- Testing: Vitest (unit/integration), Playwright (e2e)
- CI/CD: GitHub Actions
- Deployment: [deployment target]

## Build and run commands
- Install: `npm install` (root, runs workspaces)
- Dev server: `npm run dev`
- Build: `npm run build`
- Test all: `npm test`
- Test frontend: `npm run test:frontend`
- Test backend: `npm run test:backend`
- Test e2e: `npm run test:e2e`
- Lint: `npm run lint`
- Type check: `npm run typecheck`
- Database migrate: `cd backend && npx prisma migrate dev`
- Database seed: `cd backend && npx prisma db seed`

## Architecture rules
- Monorepo with npm workspaces: `frontend/`, `backend/`, `shared/`
- `shared/` contains TypeScript types, validation schemas (Zod), and constants
- API contracts defined in `shared/api-types.ts`
- Backend: controller -> service -> repository layering. No business logic in controllers.
- Frontend: App Router. Server components by default, client components only when needed.
- All API endpoints return: `{ success: boolean, data?: T, error?: { code: string, message: string } }`
- Database queries through Prisma. No raw SQL except in migrations.

## Testing requirements
- Every new API endpoint: integration tests (happy path, validation errors, auth failures)
- Every new UI component: at least one unit test
- E2e tests for user-facing flows
- Test files next to source: `feature.ts` -> `feature.test.ts`
- Minimum 80% line coverage on changed files

## Git workflow
- Branch naming: `feat/short-description`, `fix/short-description`, `chore/short-description`
- Commit format: conventional commits
- Rebase feature branches on main before marking complete
- PR description: what changed, why, how to test, risks

## Error handling
- Backend: throw typed AppError classes (NotFoundError, ValidationError, AuthError)
- Frontend: error boundaries for component-level failures
- All async operations in try/catch with meaningful messages
- Structured JSON logging (pino)

## Security
- Auth middleware on all endpoints except explicitly public routes
- Input validation with Zod at API boundary
- Parameterized queries (Prisma handles this)
- CORS restricted to frontend origin in production
- Rate limiting on auth endpoints

## When mistakes happen
- If a passing test now fails — that is YOUR bug. Fix before continuing.
- If TypeScript compiler reports errors — fix ALL of them.
- If linting fails — fix it. Do not disable rules.
```

---

## Astro + React (Static/Hybrid Site)

### Repo CLAUDE.md

```markdown
# {PROJECT_NAME} — {COMPANY}

## Project overview
{DESCRIPTION}.

## Tech stack
- Framework: Astro 5, React 19 (islands), TypeScript 5.7
- Styling: Tailwind CSS 4
- Content: Astro Content Collections
- Testing: Vitest (unit), Playwright (e2e)
- Deployment: [deployment target]

## Build and run commands
- Install: `npm install`
- Dev server: `npm run dev`
- Build: `npm run build`
- Preview: `npm run preview`
- Test: `npm test`
- Lint: `npm run lint`
- Type check: `npm run typecheck`

## Architecture rules
- Astro pages in `src/pages/` — static by default
- React components only for interactive islands (`client:load`, `client:visible`)
- Content collections in `src/content/` with Zod schemas
- Layouts in `src/layouts/`
- Reusable components in `src/components/`
- Utility functions in `src/lib/`

## Content conventions
- Blog posts: `src/content/blog/` with frontmatter schema
- Pages: `src/content/pages/` for CMS-managed content
- Images optimized via Astro Image

## Performance
- Zero JavaScript by default. Client directives only when interactivity required.
- Images use `<Image>` component for automatic optimization
- Prefer static rendering. Use SSR only for personalized content.
```

---

## Python + FastAPI

### Repo CLAUDE.md

```markdown
# {PROJECT_NAME} — {COMPANY}

## Project overview
{DESCRIPTION}.

## Tech stack
- Framework: FastAPI, Python 3.12
- Database: PostgreSQL 17, SQLAlchemy 2.0
- Testing: pytest, httpx
- Migrations: Alembic
- Deployment: Docker

## Build and run commands
- Install: `pip install -e ".[dev]"` or `uv sync`
- Dev server: `uvicorn app.main:app --reload`
- Test: `pytest`
- Test with coverage: `pytest --cov=app`
- Lint: `ruff check .`
- Format: `ruff format .`
- Type check: `mypy app/`
- Migrate: `alembic upgrade head`
- New migration: `alembic revision --autogenerate -m "description"`

## Architecture rules
- `app/` root package
- `app/api/` — Route handlers (thin, call services)
- `app/services/` — Business logic
- `app/models/` — SQLAlchemy models
- `app/schemas/` — Pydantic request/response schemas
- `app/core/` — Config, security, dependencies
- Dependency injection via FastAPI Depends()

## Testing
- Tests in `tests/` mirroring app/ structure
- Use httpx AsyncClient for API tests
- Test database with fixtures (conftest.py)
- Minimum 80% coverage on changed files
```

---

## `.claude/settings.json` — Project Settings Template

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run dev)",
      "Bash(npm run build)",
      "Bash(npm test)",
      "Bash(npm run test:*)",
      "Bash(npm run lint)",
      "Bash(npm run typecheck)",
      "Bash(npx prisma *)",
      "Bash(npx playwright *)",
      "Bash(git *)"
    ],
    "deny": [
      "Bash(npx prisma migrate deploy)",
      "Bash(npm publish *)",
      "Bash(rm -rf *)",
      "Read(.env)",
      "Read(.env.*)",
      "Read(secrets/**)"
    ]
  }
}
```
