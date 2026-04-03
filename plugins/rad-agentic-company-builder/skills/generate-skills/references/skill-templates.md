# Project Skill Templates

Complete SKILL.md templates for the four standard project skills. Customize `{TEST_CMD}`, `{TYPECHECK_CMD}`, `{LINT_CMD}`, `{COVERAGE_CMD}`, `{MIGRATE_CMD}`, `{ORM}` placeholders to match the project's tech stack.

---

## sprint-cycle/SKILL.md

```yaml
---
name: sprint-cycle
description: Plan and execute a development sprint. Use when starting a new feature cycle, reviewing sprint progress, or when the user says "start a sprint" or "plan the next sprint."
---
```

```markdown
# Sprint Cycle Workflow

Run a development sprint. Follow this process:

## Phase 1: Sprint Planning
1. Read `tasks/backlog.md` for pending work items
2. Read recent git history: `git log --oneline -20`
3. Read any existing plans in `tasks/plans/`
4. Propose 3-5 items for this sprint based on priority and dependencies
5. For each item, estimate complexity (S/M/L) and identify blockers
6. Write sprint plan to `tasks/sprints/sprint-YYYY-MM-DD.md`
7. Wait for user approval before proceeding

## Phase 2: Execution
For each sprint item, in dependency order:
1. Use the architect agent to create a plan (if M or L complexity)
2. Use the implementer agent to write the code
3. Use the tester agent to verify coverage
4. Use the reviewer agent to audit the changes
5. Commit to a feature branch and note completion in sprint file

## Phase 3: Sprint Review
1. Run full test suite: `{TEST_CMD}`
2. Run typecheck: `{TYPECHECK_CMD}`
3. Generate summary of all changes: `git log --oneline main..HEAD`
4. Update sprint file with actual outcomes vs plan
5. Move completed items from backlog to `tasks/completed.md`
6. Report sprint summary to user
```

---

## api-design/SKILL.md

```yaml
---
name: api-design
description: Design a new API endpoint following project standards. Use when adding new endpoints to the backend or modifying the API contract.
---
```

```markdown
# API Endpoint Design

When designing a new API endpoint, follow this process:

## Step 1: Define the Contract in Shared Types
Add request and response types to the shared types module:

- Request type: fields with TypeScript types, required vs optional
- Response type: complete shape including nested objects
- Import and use in both frontend and backend

## Step 2: Add Validation Schema
Add input validation using Zod (TypeScript) or Pydantic (Python):

- All string fields: min/max length constraints
- ID fields: UUID or format validation
- Optional fields: explicitly marked
- Nested objects: validated recursively

## Step 3: Implement Backend Layers
Follow the layered architecture pattern:

1. **Route** — Register endpoint, apply auth and rate-limiting middleware
2. **Controller** — Validate input with schema, call service, format response envelope
3. **Service** — Business logic, orchestration, call repository methods
4. **Repository** — Database queries via {ORM}

## Step 4: Standardized Response Format
All endpoints return the envelope:
- Success: `{ success: true, data: T }`
- Error: `{ success: false, error: { code: "ERROR_CODE", message: "Human readable" } }`

## Step 5: Write Integration Tests
Test file covering:
- 200/201 happy path with valid input
- 400 with invalid/missing fields
- 401 without auth token
- 403 with insufficient permissions (if applicable)
- 404 for nonexistent resources
- 409 for conflicts (if applicable)
```

---

## release-prep/SKILL.md

```yaml
---
name: release-prep
description: Prepare a release including changelog generation, version bumping, and pre-release validation. Use when the user says "prepare a release" or "cut a release."
---
```

```markdown
# Release Preparation

## Pre-Release Validation
1. Ensure on the main branch with latest changes: `git checkout main && git pull`
2. Run full test suite: `{TEST_CMD}`
3. Run typecheck: `{TYPECHECK_CMD}`
4. Run lint: `{LINT_CMD}`
5. Run e2e tests if applicable
6. If ANY of the above fail, STOP and report failures. Do not proceed.

## Generate Changelog
1. Read commits since last tag: `git log $(git describe --tags --abbrev=0)..HEAD --oneline`
2. Categorize commits:
   - **Features**: `feat:` commits
   - **Bug fixes**: `fix:` commits
   - **Breaking changes**: commits with `BREAKING CHANGE` in body
   - **Other**: `chore:`, `refactor:`, `docs:` commits
3. Write human-readable changelog entry in `CHANGELOG.md` at the top
4. Include date and version number

## Version Bump
1. Determine version bump based on changes:
   - BREAKING CHANGE -> major version bump
   - New features -> minor version bump
   - Bug fixes only -> patch version bump
2. Update version in root package.json (or pyproject.toml)
3. Commit: `chore: bump version to x.y.z`

## Create Release
1. Create annotated git tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
2. Summary report: list contents, migration steps, known issues
```

---

## daily-standup/SKILL.md

```yaml
---
name: daily-standup
description: Run a daily standup review of recent changes, test status, and priorities. Use when starting a new work session or reviewing progress.
---
```

```markdown
# Daily Standup Review

Perform a daily standup review:

1. Run `git log --oneline --since="24 hours ago"` to see recent commits
2. Run `{TEST_CMD}` and summarize results
3. Check for TODO/FIXME comments added recently:
   `grep -rn "TODO\|FIXME" --include="*.ts" --include="*.tsx" --include="*.py" | head -30`
4. Read the project's task tracking file if one exists (tasks/backlog.md, TODO.md, or similar)
5. Summarize:
   - What was completed in the last 24 hours
   - Current test suite status (passing/failing/skipped counts)
   - Top 3 priorities for today based on task list and failing tests
   - Any blocking issues or technical debt flagged in recent commits
```
