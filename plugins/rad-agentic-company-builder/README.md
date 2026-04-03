# rad-agentic-company-builder

Scaffold and configure an AI-agent-driven company infrastructure — folder hierarchies, CLAUDE.md files, agent definitions, skills, hooks, MCP configs, and operational patterns. Based on *The Agentic Bible 2026*.

## What's Inside

| Component | Count |
|-----------|-------|
| Skills | 7 |
| Agents | 1 |

## Skills

| Skill | Trigger Phrases | What It Does |
|-------|----------------|--------------|
| `scaffold-company` | "scaffold a company", "create agentic company", "set up company structure" | Creates the top-level company folder hierarchy with CLAUDE.md files and shared infrastructure |
| `scaffold-project` | "scaffold a project", "create new project", "add a project" | Adds a new application project within the company structure |
| `generate-agents` | "generate agents", "create agent definitions", "set up agent team" | Generates 6 standard agent types: architect, implementer, reviewer, tester, deployer, docs-writer |
| `generate-skills` | "generate skills", "create project skills", "add skills to project" | Generates 4 standard skills: sprint-cycle, api-design, release-prep, daily-standup |
| `configure-hooks` | "configure hooks", "set up quality gates", "add TaskCompleted hook" | Sets up deterministic enforcement hooks and quality gates |
| `configure-mcp` | "configure MCP", "set up MCP servers", "add MCP integrations" | Configures MCP server connections (GitHub, Coolify, PostgreSQL, Prisma, Google Workspace, Docker, Playwright, SSH) |
| `agentic-operations` | "daily operating rhythm", "agentic operations", "token optimization" | Reference guide for daily ops, cost optimization, credential rotation, and maintenance patterns |

## Agent

| Agent | When To Use | What It Does |
|-------|------------|--------------|
| `company-auditor` | "audit my agentic company structure", "is my setup complete?" | Audits company structure for completeness against Agentic Bible best practices |

## Installation

```bash
claude plugins add ./plugins/rad-agentic-company-builder
```

## Requirements

- Claude Code CLI installed and authenticated
- Familiarity with the Agentic Bible 2026 patterns (recommended)

## License

Apache-2.0
