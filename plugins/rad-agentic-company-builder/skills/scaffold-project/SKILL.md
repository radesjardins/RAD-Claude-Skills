---
name: scaffold-project
description: This skill should be used when the user says "scaffold a project", "create new project", "add a project", "new app project", "set up project structure", "create wrapper repo", "initialize project workspace", or wants to create a new application project within the engineering division using the wrapper/repo separation pattern.
argument-hint: "[project-name] [--stack next,react,typescript,postgres] [--division engineering]"
user-invocable: true
---

# Scaffold Project with Wrapper/Repo Pattern

Create a new application project within the agentic company structure using the **wrapper/repo separation pattern** from The Agentic Bible 2026. This pattern separates project management context (above git) from developer instructions (inside git).

## Why the Wrapper/Repo Pattern

The wrapper folder is NOT a git repository — it is an orchestration layer. The actual git repo lives inside `repo/`. Three reasons:

1. **Agent context that should not be committed** — Task specs, sprint context, and agent team notes are ephemeral management artifacts. They change constantly and have no place in version history.
2. **Git boundary as trust boundary** — Files inside `repo/` can be pushed to GitHub. Files outside stay local. Agent instructions and API keys never leave the machine accidentally.
3. **Upward discovery makes it seamless** — When Claude Code runs inside `repo/`, it automatically loads CLAUDE.md files from the wrapper, division, and company root. No configuration needed.

## Scaffolding Process

### Step 1: Gather Requirements

Collect from the user (use `$ARGUMENTS` if provided):

1. **Project name** — kebab-case (e.g., "soulcat-app", "company-website")
2. **Division** — which division to create under (default: `engineering/`)
3. **Tech stack** — for the repo-level CLAUDE.md:
   - Frontend framework (Next.js, Astro, React, etc.)
   - Backend framework (Express, Fastify, etc.)
   - Language (TypeScript, Python, etc.)
   - Database (PostgreSQL, SQLite, etc.)
   - ORM (Prisma, Drizzle, etc.)
   - Testing (Vitest, Jest, Playwright, etc.)
   - CSS (Tailwind, etc.)
4. **Repository type** — monorepo with workspaces or single-package

### Step 2: Create Directory Structure

```
engineering/{project-name}/
├── CLAUDE.md                    # Project management context (above git)
├── task-specs/
│   └── TEMPLATE.md              # Standard task specification format
├── repo/                        # Git boundary starts here
│   ├── CLAUDE.md                # Developer-facing instructions (committed)
│   ├── CLAUDE.local.md          # Personal overrides (gitignored)
│   ├── .claude/
│   │   ├── settings.json        # Project permissions (committed)
│   │   ├── settings.local.json  # Personal settings (gitignored)
│   │   ├── rules/               # Scoped instruction files
│   │   ├── skills/              # Project-specific skills
│   │   └── agents/              # Project-specific agents
│   ├── .mcp.json                # MCP server config (committed)
│   ├── .gitignore
│   └── (source directories per stack)
└── artifacts/                   # Cowork output staging area
```

### Step 3: Generate CLAUDE.md Files

**Wrapper CLAUDE.md** (`engineering/{project}/CLAUDE.md`) — project management context:
- Current sprint goals and priorities
- Architecture decision log
- Agent team composition notes
- Links to active task specs

**Repo CLAUDE.md** (`engineering/{project}/repo/CLAUDE.md`) — developer instructions:
- Project overview (one paragraph)
- Tech stack listing with versions
- Build and run commands (install, dev, build, test, lint, typecheck, migrate, seed)
- Architecture rules (directory structure, layering, patterns)
- Testing requirements (coverage gates, test types, file colocation)
- Git workflow (branch naming, commit format, PR requirements)
- Error handling patterns
- Security requirements

Refer to `references/project-templates.md` for complete repo CLAUDE.md templates by tech stack.

### Step 4: Generate Task Spec Template

Create `task-specs/TEMPLATE.md`:

```markdown
# Task: [Title]

## Objective
[One sentence describing what needs to be accomplished]

## Context
[Background information the agent needs to understand the task]

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Notes
[Implementation hints, constraints, or references]

## Estimated Complexity
[ ] Small (1-2 files) [ ] Medium (3-8 files) [ ] Large (8+ files)
```

### Step 5: Initialize Git Repository

Inside `repo/`:
1. Run `git init`
2. Create `.gitignore` with standard entries plus `CLAUDE.local.md`, `.claude/settings.local.json`, `.env`, `.env.*`
3. Create initial commit: `chore: initialize project structure`

### Step 6: Generate Project Settings

Create `.claude/settings.json` inside repo with:
- Permissions for project-specific commands (build, test, lint, migrate)
- Deny rules for dangerous operations (production deploys, rm -rf, .env reads)
- Optional: TaskCompleted hook for quality gates
- Optional: PostToolUse hook for typecheck-on-edit

### Step 7: Report and Next Steps

Summarize the created structure and suggest:
1. Run `generate-agents` to add agent definitions to `.claude/agents/`
2. Run `generate-skills` to add project skills to `.claude/skills/`
3. Run `configure-mcp` to set up external integrations
4. Run `configure-hooks` to enable quality gates

## Additional Resources

### Reference Files

- **`references/project-templates.md`** — Complete repo CLAUDE.md templates for common tech stacks (Next.js+Express, Astro, Python+FastAPI)
