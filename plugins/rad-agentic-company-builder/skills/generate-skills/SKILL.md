---
name: generate-skills
description: This skill should be used when the user says "generate skills", "create project skills", "add skills to project", "set up sprint skill", "create api-design skill", "create release-prep skill", "create daily-standup skill", or wants to generate the standard set of four project skills for an agentic company project.
argument-hint: "[--project path/to/project/repo] [--skills sprint-cycle,api-design,release-prep,daily-standup]"
user-invocable: true
---

# Generate Project Skills

Create the standard set of four project-level skills from The Agentic Bible 2026. These skills provide reusable workflows that coordinate the agent team through planning, implementation, release, and daily operations.

## The Four Standard Skills

| Skill | Purpose | Invocation |
|-------|---------|------------|
| **sprint-cycle** | Plan, execute, and review development sprints | "start a sprint", "plan the next sprint" |
| **api-design** | Design new API endpoints following project standards | "design an API endpoint", "add new endpoint" |
| **release-prep** | Prepare releases with changelog, versioning, validation | "prepare a release", "cut a release" |
| **daily-standup** | Morning review of changes, test status, priorities | "daily standup", "morning review" |

## Generation Process

### Step 1: Determine Target Location

Find the project's `.claude/skills/` directory. If `$ARGUMENTS` provides a path, use it. Otherwise:
1. Check current directory for `.claude/skills/`
2. Check for `repo/.claude/skills/`
3. Ask user for the project repo path

Create the skills directory if it does not exist.

### Step 2: Gather Customization

Infer or ask for:
1. **Tech stack** — affects build/test/lint commands in skill templates
2. **Package manager** — npm, pnpm, yarn, bun
3. **Test runner** — Vitest, Jest, pytest
4. **ORM** — Prisma, Drizzle, SQLAlchemy (affects api-design skill)
5. **Which skills** — all four or a subset

### Step 3: Generate Skill Directories and SKILL.md Files

For each skill, create:
```
.claude/skills/{skill-name}/
└── SKILL.md
```

**sprint-cycle** — orchestrates the full sprint lifecycle:
- Phase 1: Planning (read backlog, propose items, estimate complexity)
- Phase 2: Execution (architect -> implementer -> tester -> reviewer per item)
- Phase 3: Review (full test suite, summary, backlog updates)

**api-design** — structured endpoint design workflow:
- Step 1: Define contract in shared types
- Step 2: Add validation schemas
- Step 3: Implement backend layers (route -> controller -> service -> repository)
- Step 4: Standardized response format
- Step 5: Write integration tests

**release-prep** — release preparation checklist:
- Pre-release validation (tests, typecheck, lint, e2e)
- Changelog generation from git log
- Version bump (semver based on change types)
- Git tag and release summary

**daily-standup** — morning status review:
- Recent commits (last 24 hours)
- Test suite status
- TODO/FIXME scan
- Task list review
- Top 3 priorities

### Step 4: Customize to Tech Stack

Replace generic commands with project-specific ones:
- `npm test` -> `pnpm test` or `pytest` as appropriate
- `npx prisma migrate dev` -> `alembic upgrade head` for Python
- Adjust directory paths for monorepo vs single-package

### Step 5: Report

List all generated skills with their trigger phrases. Remind:
- Skills auto-activate when Claude detects matching context
- User-invocable skills available via `/skills` menu
- Skills can reference agents (e.g., sprint-cycle coordinates architect + implementer)

## Additional Resources

### Reference Files

- **`references/skill-templates.md`** — Complete SKILL.md templates for all four standard skills (sprint-cycle, api-design, release-prep, daily-standup) with customizable placeholders for tech stack commands
