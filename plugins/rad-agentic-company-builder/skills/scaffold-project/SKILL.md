---
name: scaffold-project
description: This skill should be used when the user says "scaffold a project", "create new project", "add a project", "set up project structure", "initialize project workspace", or wants to create a new application project within the engineering division. By default uses the standard layout (project root = git root); the optional --wrapper flag enables a wrapper-above-git layout with explicit warnings about tooling tradeoffs.
argument-hint: "[project-name] [--stack next,react,typescript,postgres] [--division engineering] [--wrapper]"
user-invocable: true
allowed-tools: Read Glob Grep Write Edit Bash
---

# Scaffold a Project Inside the Workspace

Create a new application project under a division (default: `engineering/`). Two layout options:

1. **Default — project root IS git root.** Standard layout. CLAUDE.md, settings.json, agents, MCP config all live inside the repo. This is what every Claude Code doc, IDE, CI/CD tool, and `gh` CLI assumes.
2. **`--wrapper` opt-in — project folder above git root.** A `repo/` subdirectory holds the git boundary. CLAUDE.md and `task-specs/` live above the git boundary so they don't get committed. **Read the warnings before opting in.**

## Source

- Standard layout: documented Anthropic recommendation per [Claude Code docs](https://docs.claude.com/en/docs/claude-code/) and [best practices](https://code.claude.com/docs/en/best-practices). CLAUDE.md goes at the repo root; `CLAUDE.local.md` is the documented mechanism for personal/non-shared content.
- Wrapper-above-git: this plugin's author's invention. Some users find it useful; it has real tradeoffs. Not Anthropic-canonical.

## Default Layout (recommended)

```
engineering/{project-name}/         # Project root = git root
├── .git/
├── .claude/
│   ├── settings.json
│   ├── settings.local.json         # gitignored — personal overrides
│   ├── rules/
│   ├── agents/
│   └── skills/
├── .mcp.json
├── .gitignore                       # includes CLAUDE.local.md, settings.local.json, .env, .env.*
├── CLAUDE.md                        # committed, project-wide context
├── CLAUDE.local.md                  # gitignored — personal context (Anthropic's recommended split)
└── (source directories per stack)
```

This works seamlessly with: `gh` CLI, GitHub Desktop, IDE git integration, Dependabot, GitHub Actions, every CI tool that assumes project root = git root.

## Optional `--wrapper` Layout

```
engineering/{project-name}/         # NOT a git repo
├── CLAUDE.md                       # Project management context (sprint goals, architecture log)
├── task-specs/                     # Agent task specs (ephemeral, never committed)
│   └── TEMPLATE.md
├── artifacts/                      # Cowork/Routines output staging
└── repo/                           # Git boundary starts here
    ├── .git/
    ├── .claude/...
    ├── .mcp.json
    ├── .gitignore
    └── CLAUDE.md                   # Repo-level CLAUDE.md (developer instructions)
```

### Why someone might want this

- Separates ephemeral planning context (sprint notes, architecture-decision log) from committed code.
- Forces a hard boundary: anything in the wrapper definitely doesn't get pushed.

### What this layout BREAKS

- **`gh` CLI** assumes you `cd` into the repo, not its parent. `gh pr create` from the wrapper folder fails.
- **IDE git integration** — VS Code, JetBrains, GitHub Desktop all expect to open the git root. Opening the wrapper means the IDE doesn't see the repo at all unless you specifically open the `repo/` subfolder.
- **Dependabot, Renovate, npm/pnpm/yarn workspace tooling** — all assume project root = repo root. They don't look upward.
- **GitHub Actions** workflows triggered by file paths break because file paths are relative to the repo, not the wrapper.
- **`npm init`, `cargo new`, `cargo init`** and similar bootstrap tools create project metadata at cwd; the wrapper layout requires manually moving things.
- **CI/CD platforms** (Vercel, Railway, Coolify, Render) clone the git repo, not its parent. The wrapper context is invisible to them.

The Anthropic-documented alternative — `CLAUDE.local.md` for gitignored personal content + project root = git root — accomplishes the same separation goal without breaking any of the above.

**Use `--wrapper` only if you have a specific reason that outweighs these tradeoffs.**

## Workflow

### Step 1: Gather requirements

Use `$ARGUMENTS` if provided:

1. **Project name** — kebab-case (e.g., `acme-app`)
2. **Division** — default: `engineering/`. Other divisions (product, marketing) generally don't need a project subdirectory; their content lives directly in the division folder.
3. **Tech stack** — for the CLAUDE.md template:
   - Frontend framework
   - Backend framework
   - Language
   - Database
   - ORM
   - Testing
4. **Layout** — default (no flag) or `--wrapper`. If `--wrapper`, confirm the user has read the warnings above.
5. **Repository type** — monorepo with workspaces, or single-package

### Step 2: Create directory structure

Per the chosen layout. Default unless `--wrapper` was passed.

### Step 3: Generate CLAUDE.md files

**Default layout:**
- `CLAUDE.md` — committed project context, includes everything (sprint, architecture, tech stack, build commands)
- `CLAUDE.local.md` (gitignored) — personal scratchpad, recommended Anthropic pattern

**Wrapper layout:**
- Wrapper `CLAUDE.md` — sprint goals, architecture decisions, agent team notes
- `repo/CLAUDE.md` — developer-facing tech stack and build commands

Load `references/project-templates.md` for stack-specific repo CLAUDE.md content.

### Step 4: Generate task-spec template (wrapper layout only)

If `--wrapper`, create `task-specs/TEMPLATE.md` for agent task specifications. The default layout puts this kind of content in `docs/` or directly inside the repo at the user's choice — no enforced location.

### Step 5: Initialize git

In the repo (whether at project root or under `repo/`):

```bash
git init
```

Create `.gitignore` with:
```
node_modules/
.env
.env.*
.claude/settings.local.json
CLAUDE.local.md       # if using default layout
*.log
.DS_Store
```

Initial commit: `chore: initialize project structure`.

### Step 6: Generate project settings

Create `.claude/settings.json` inside the repo:
- Permissions for project commands (`build`, `test`, `lint`, `migrate`)
- Deny rules for dangerous operations (production deploys, destructive ops on `.env` reads)
- Optionally: TaskCompleted (Agent Teams experimental) or PostToolUse hook for typecheck-on-edit — see `configure-hooks` for the right pattern

### Step 7: Run validators

```bash
python3 ${plugin_root}/scripts/audit-structure.py <project-or-wrapper-root>
```

If a `.mcp.json` was created (rare at scaffold time), also:

```bash
python3 ${plugin_root}/scripts/check-mcp-config.py <repo>/.mcp.json
```

### Step 8: Report

Tell the user what was created, what layout was used, and the next-step skills:

```
Project scaffolded at <path>.

Layout: <default | wrapper>
Tech stack: <stack>

Next:
- generate-agents — for the 6 engineering roles (architect, implementer, etc.)
- configure-hooks — quality gates
- configure-mcp — external integrations
- add-function-agent --function <name> — opt-in business-function agents
```

If `--wrapper` was used, restate the tradeoffs in the report so the user remembers what they signed up for.

## What this skill does NOT do

- Does not run `npm install` or any package-manager bootstrap (you do that after scaffolding to keep the operation reversible).
- Does not generate source code.
- Does not configure CI/CD.
- Does not assume the wrapper layout is better — defaults to the standard Claude-Code-canonical layout.

## Reference

- `references/project-templates.md` — Stack-specific repo CLAUDE.md templates (Next.js + Express, Astro, FastAPI)
