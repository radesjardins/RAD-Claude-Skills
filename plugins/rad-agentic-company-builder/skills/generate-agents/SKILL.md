---
name: generate-agents
description: This skill should be used when the user says "generate agents", "create engineering agent team", "set up agent team", "add agents to project", "create architect agent", "create implementer agent", "create reviewer agent", "create tester agent", "create deployer agent", "create docs-writer agent", or wants to generate a starting set of six engineering-role agents for a Claude Code project. These are reasonable starting agents — not industry-standard convergence.
argument-hint: "[--project path/to/project] [--agents architect,implementer,reviewer,tester,deployer,docs-writer]"
user-invocable: true
allowed-tools: Read Glob Grep Write Edit Bash
---

# Generate Engineering-Role Agents

Create a starting set of six engineering-role agent definitions. The pattern: narrow role + tool restrictions + completion checklist. Anthropic's documented subagent system enforces tool restrictions at runtime — a read-only agent literally cannot modify files, regardless of what the user prompts it to do.

**These are reasonable starting agents, not an industry-standard team.** Customize the set to your actual workflow. For business-function agents (billing, recruiting, support, etc.), use `add-function-agent` instead.

## Source

- Subagent file format: documented at [Claude Code Subagents](https://docs.claude.com/en/docs/claude-code/subagents)
- Tool restrictions via `tools:` frontmatter — documented behavior
- Six-role split: opinionated by this plugin's author. Common in practice; not Anthropic-canonical.

## The six engineering roles

| Agent | Role | Model | Tools | Modifies files? |
|---|---|---|---|---|
| **architect** | System design, feature planning | opus | Read, Grep, Glob, Bash | No — plans only |
| **implementer** | Code writing, bug fixes | sonnet | Read, Grep, Glob, Bash, Write, Edit | Yes |
| **reviewer** | Code review, security audit | opus | Read, Grep, Glob, Bash | No — reports only |
| **tester** | Test writing, coverage validation | sonnet | Read, Grep, Glob, Bash, Write, Edit | Yes |
| **deployer** | CI/CD, release management | sonnet | Read, Grep, Glob, Bash, Write, Edit | Yes |
| **docs-writer** | Documentation generation | sonnet | Read, Grep, Glob, Bash, Write, Edit | Yes |

### Why this split

- **Read-only agents on Opus.** Architect and reviewer benefit from deeper reasoning but should not modify code. The tool restriction is the enforcement.
- **Write agents on Sonnet.** Implementer, tester, deployer, docs-writer favor speed for iterative work.
- **Tool restrictions enforce roles.** A reviewer that lacks Write/Edit literally cannot modify code mid-review.
- **Each agent has a completion checklist.** Explicit exit criteria reduce the "I'm done" → "actually nothing was tested" failure.

### Why not more agents?

Each additional agent multiplies the failure surface. Multi-agent systems deployed before single-agent systems are proven fail faster (per Gartner / HBR / multiple production retrospectives). The six-role split is a pragmatic floor, not a target. If your workflow doesn't need a deployer (you deploy by hand), don't generate one.

## Workflow

### Step 1: Determine target location

Find the project's `.claude/agents/` directory. Use `--project <path>` if provided. Otherwise:

1. Check current directory for `.claude/agents/`
2. Check current directory for `repo/.claude/agents/` (wrapper layout)
3. Walk up looking for a project root
4. Ask the user

Create `.claude/agents/` if it doesn't exist.

### Step 2: Gather customization

Ask for (or infer from existing CLAUDE.md):

1. **Tech stack** — affects build/test/typecheck commands in agent prompts
2. **Build commands** — specific `npm` / `pnpm` / `bun` / `cargo` / `pytest` etc.
3. **Architecture pattern** — monorepo, single-package, microservices
4. **Deployment target** — used by the deployer agent
5. **Which agents to generate** — all six or a subset; default is all six

### Step 3: Generate agent files

Load `references/agent-templates.md` and write each requested agent file to `.claude/agents/`. Each file uses YAML frontmatter (`name`, `description`, `tools`, `model`) and a system prompt with role identity, process steps, constraints, and completion checklist.

Customize per project: build commands, test commands, ORM, deployment target.

### Step 4: Optionally generate user-level utility agents

Offer to create a `quick-research.md` agent at `~/.claude/agents/` (user-level, available across all projects):
- Read-only research agent for code patterns, library APIs, debugging clues
- Tools: Read, Grep, Glob, Bash (read-only commands only)
- Model: sonnet (fast)

This is useful enough to recommend; users can decline.

### Step 5: Validate

```bash
python3 ${plugin_root}/scripts/audit-structure.py <project> --skip-projects --skip-hooks --skip-mcp
```

The audit script checks each generated agent's frontmatter for required fields. Surface any HIGH findings before declaring done.

### Step 6: Report

List generated files with their roles. Remind the user:
- Invoke via natural language: "Use the architect to plan this feature"
- Or via `/agents` interactive menu in Claude Code
- Subagents cannot spawn other subagents (single-level hierarchy — documented Anthropic constraint)
- For Agent Teams (experimental, multi-level coordination), see Anthropic's experimental docs

## What this skill does NOT do

- Does not generate business-function agents (billing, support, recruiting, etc.) — use `add-function-agent` for those.
- Does not invoke the agents — the user does that in their own workflow.
- Does not validate agent output quality — that's runtime behavior, not scaffolding.
- Does not pretend the six engineering roles are universal. They're a useful starting point.

## Reference

- `references/agent-templates.md` — Complete agent definition templates for all six roles plus the quick-research utility
