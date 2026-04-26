---
name: generate-skills
description: This skill should be used when the user says "generate skills", "create project skills", "add skills to project", "set up sprint skill", "create api-design skill", "create release-prep skill", "create daily-standup skill", or wants to generate a starting set of four project-level skills (sprint-cycle, api-design, release-prep, daily-standup) for a Claude Code project. These are reasonable starting workflows — adapt to your team's actual practices.
argument-hint: "[--project path/to/project] [--skills sprint-cycle,api-design,release-prep,daily-standup]"
user-invocable: true
allowed-tools: Read Glob Grep Write Edit Bash
---

# Generate Project Skills

Create a starting set of project-level skills that coordinate the engineering agents through common workflows. **These are starting templates** — keep what's useful, discard or rewrite what doesn't match your team's practices.

## Source

- Skill file format: documented at [Claude Code Skills](https://docs.claude.com/en/docs/claude-code/) (sub-section on skills)
- Specific four-skill set (sprint-cycle, api-design, release-prep, daily-standup): opinionated by this plugin's author. Common patterns; not Anthropic-canonical.

## The four starter skills

| Skill | Purpose | Triggers |
|---|---|---|
| **sprint-cycle** | Plan, execute, and review development sprints | "start a sprint", "plan the next sprint" |
| **api-design** | Design new API endpoints following project standards | "design an API endpoint", "add new endpoint" |
| **release-prep** | Prepare releases with changelog, versioning, validation | "prepare a release", "cut a release" |
| **daily-standup** | Morning review of changes, test status, priorities | "daily standup", "morning review" |

## Workflow

### Step 1: Determine target

Find the project's `.claude/skills/` directory. Use `--project <path>` if provided. Otherwise check current dir, then `repo/.claude/skills/`, then ask.

### Step 2: Gather customization

Infer or ask for:

1. **Tech stack** — affects build/test/lint commands in skill templates
2. **Package manager** — npm, pnpm, yarn, bun, pip
3. **Test runner** — Vitest, Jest, pytest, Go test
4. **ORM** — affects api-design skill (Prisma, Drizzle, SQLAlchemy)
5. **Which skills** — all four or a subset

### Step 3: Generate skill directories and SKILL.md files

For each skill, create:

```
.claude/skills/{skill-name}/
└── SKILL.md
```

Load `references/skill-templates.md` and customize each:

- **sprint-cycle:** Phase 1 planning → Phase 2 execution (architect → implementer → tester → reviewer per item) → Phase 3 review with full test suite
- **api-design:** Define contract in shared types → add validation schemas → implement layered backend → standardize response → write integration tests
- **release-prep:** Pre-release validation → changelog from git log → semver bump → tag and release notes
- **daily-standup:** Recent commits → test status → TODO/FIXME scan → task list review → top 3 priorities

### Step 4: Customize commands

Replace generic commands with project-specific ones:
- `npm test` → `pnpm test`, `bun test`, `pytest`
- `npx prisma migrate dev` → `alembic upgrade head` for Python, `drizzle-kit migrate` for Drizzle
- Adjust paths for monorepo workspaces

### Step 5: Report

List generated skills with their trigger phrases. Remind:
- Skills auto-activate when Claude detects matching context
- User-invocable skills available via `/skills` menu in Claude Code
- Skills can reference agents (e.g., sprint-cycle coordinates architect + implementer + tester + reviewer)

## What this skill does NOT do

- Does not enforce the workflows. They're prompts to the model; the model can deviate.
- Does not run sprints, ship releases, or do standups for you. They structure the conversation.
- Does not assume your team uses sprints. If you don't, skip `sprint-cycle`.

## Reference

- `references/skill-templates.md` — Complete SKILL.md templates for all four starter skills
