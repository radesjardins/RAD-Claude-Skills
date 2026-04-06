# rad-agentic-company-builder — Scaffold an AI-agent-driven company structure in a single session.

Running a company with AI agents requires a specific infrastructure: folder hierarchies that agents can navigate, CLAUDE.md files that give each agent its context, hooks that enforce quality gates, and MCP configs that connect agents to the tools they need. rad-agentic-company-builder creates all of that from scratch — based on *The Agentic Bible 2026* — so you can start operating with a full agent team instead of building scaffolding by hand.

## What You Can Do With This

- Scaffold a full company folder hierarchy with CLAUDE.md files for each function
- Generate a standard 6-agent team: architect, implementer, reviewer, tester, deployer, docs-writer
- Configure quality gate hooks and MCP connections (GitHub, Coolify, PostgreSQL, Google Workspace, and more)
- Audit your existing agentic structure for gaps against Agentic Bible best practices

## How It Works

| Skill | Trigger Phrases | What It Does |
|-------|----------------|--------------|
| `scaffold-company` | "scaffold a company", "create agentic company" | Creates company folder hierarchy with CLAUDE.md files and shared infrastructure |
| `scaffold-project` | "scaffold a project", "add a project" | Adds a new application project within the company structure |
| `generate-agents` | "generate agents", "set up agent team" | Generates 6 standard agent types |
| `generate-skills` | "generate skills", "add skills to project" | Generates 4 standard skills: sprint-cycle, api-design, release-prep, daily-standup |
| `configure-hooks` | "configure hooks", "set up quality gates" | Sets up enforcement hooks and quality gates |
| `configure-mcp` | "configure MCP", "add MCP integrations" | Configures MCP server connections |
| `agentic-operations` | "daily operating rhythm", "token optimization" | Reference guide for daily ops, cost optimization, credential rotation |

| Agent | Purpose |
|-------|---------|
| `company-auditor` | Audits company structure for completeness against Agentic Bible best practices |

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-agentic-company-builder
```

```
Scaffold a company
Generate agents for my project
Configure MCP for my setup
Audit my agentic company structure
```

## Requirements

- Claude Code CLI installed and authenticated
- Familiarity with the Agentic Bible 2026 patterns (recommended)

## License
Apache-2.0
