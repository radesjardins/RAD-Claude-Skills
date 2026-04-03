---
name: generate-agents
description: This skill should be used when the user says "generate agents", "create agent definitions", "set up agent team", "add agents to project", "create architect agent", "create implementer agent", "create reviewer agent", "create tester agent", "create deployer agent", "create docs-writer agent", or wants to generate the standard set of six agent definition files for an agentic company project.
argument-hint: "[--project path/to/project/repo] [--agents architect,implementer,reviewer,tester,deployer,docs-writer]"
user-invocable: true
---

# Generate Agent Definitions

Create the standard set of six specialized agent definitions from The Agentic Bible 2026. Each agent has a narrow role, restricted tools, and clear exit criteria — embodying Anthropic's philosophy that reliability comes from specialization plus constraint.

## The Six Standard Agents

| Agent | Role | Model | Tools | Modifies Files? |
|-------|------|-------|-------|-----------------|
| **architect** | System design, feature planning | opus | Read, Grep, Glob, Bash | No — plans only |
| **implementer** | Code writing, bug fixes | sonnet | Read, Grep, Glob, Bash, Write, Edit | Yes |
| **reviewer** | Code review, security audit | opus | Read, Grep, Glob, Bash | No — reports only |
| **tester** | Test writing, coverage validation | sonnet | Read, Grep, Glob, Bash, Write, Edit | Yes |
| **deployer** | CI/CD, release management | sonnet | Read, Grep, Glob, Bash, Write, Edit | Yes |
| **docs-writer** | Documentation generation | sonnet | Read, Grep, Glob, Bash, Write, Edit | Yes |

## Design Principles

- **Read-only agents use Opus** — architect and reviewer need deep reasoning but should not modify code
- **Write agents use Sonnet** — implementer, tester, deployer, docs-writer need speed for iterative coding
- **Tool restrictions enforce roles** — an architect literally cannot write files; a reviewer cannot edit code
- **Each agent has a completion checklist** — explicit exit criteria prevent premature "done" claims

## Generation Process

### Step 1: Determine Target Location

Find the project's `.claude/agents/` directory. If `$ARGUMENTS` provides a path, use it. Otherwise:
1. Check if current directory has `.claude/agents/`
2. Check if current directory has `repo/.claude/agents/`
3. Ask the user for the project repo path

Create the agents directory if it does not exist.

### Step 2: Gather Customization

Ask for (or infer from existing CLAUDE.md):
1. **Tech stack** — frameworks, languages, ORM, testing tools
2. **Build commands** — npm/pnpm/yarn commands for test, lint, typecheck
3. **Architecture pattern** — monorepo workspaces, single package, microservices
4. **Deployment target** — Vercel, Railway, Coolify, Docker, etc.
5. **Which agents to generate** — all six or a subset

### Step 3: Generate Agent Files

Create each agent markdown file in `.claude/agents/` with:
- YAML frontmatter: name, description (with "Use for..." guidance), tools list, model
- System prompt with role identity, process steps, constraints, and completion checklist
- Customized to the project's specific tech stack and conventions

Refer to `references/agent-templates.md` for the complete agent file templates.

### Step 4: Optionally Generate Personal Utility Agent

Offer to create a `quick-research.md` agent at `~/.claude/agents/` (user-level, available across all projects):
- Read-only research agent for investigating code patterns, library APIs, debugging clues
- Restricted to: Read, Grep, Glob, Bash (read-only commands only)
- Model: sonnet (fast)

### Step 5: Report

List all generated agent files with their roles and tool access. Remind the user:
- Invoke agents via natural language: "Use the architect to plan this feature"
- Or via `/agents` interactive menu
- Sub-agents cannot spawn other sub-agents (single-level hierarchy)

## Additional Resources

### Reference Files

- **`references/agent-templates.md`** — Complete agent definition files for all six agents plus the quick-research utility agent, customizable by tech stack
