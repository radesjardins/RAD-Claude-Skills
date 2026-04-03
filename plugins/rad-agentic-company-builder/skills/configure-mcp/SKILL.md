---
name: configure-mcp
description: This skill should be used when the user says "configure MCP", "set up MCP servers", "add MCP integrations", "connect GitHub MCP", "set up Coolify MCP", "configure database MCP", "add Google Workspace MCP", "set up Docker MCP", "create .mcp.json", or wants to configure Model Context Protocol server integrations for their agentic company project.
argument-hint: "[--integrations github,coolify,postgres,google-workspace,docker,playwright,ssh]"
user-invocable: true
---

# Configure MCP Server Integrations

Set up Model Context Protocol server configurations for an agentic company project. MCP provides structured, auditable interfaces for services where direct CLI access is insufficient or insecure.

## Architecture Principle

Claude Code's Bash tool already handles most tasks natively. MCP servers add value for:
- **Production safety** — structured API access is safer than raw SSH/CLI
- **Claude Desktop/Cowork** — which lack a terminal
- **Auditable operations** — typed tool calls vs. arbitrary shell commands

## Available Integrations

| Integration | MCP Server | Purpose |
|-------------|-----------|---------|
| **GitHub** | Official GitHub MCP (Go) | Repos, PRs, issues, Actions, code scanning |
| **Coolify** | @masonator/coolify-mcp | Deployment control (38 tools, 85% token reduction) |
| **PostgreSQL** | crystaldba/postgres-mcp | SQL, EXPLAIN, index recommendations, health checks |
| **Prisma** | Built-in `prisma mcp` | Migrations, schema status |
| **Google Workspace** | workspace-mcp | Gmail, Drive, Calendar, Docs, Sheets (100+ tools) |
| **Docker** | mcp-server-docker | Container management (local + remote) |
| **Playwright** | @playwright/mcp | Browser automation, screenshots, accessibility |
| **SSH** | ssh-mcp | Structured remote command execution |

## Configuration Process

### Step 1: Select Integrations

Present the integration menu. If `$ARGUMENTS` specifies integrations, use those. Otherwise ask which are needed.

### Step 2: Determine Scope

MCP configs live in three places:
- **Project** (`.mcp.json` in repo root) — shared via Git, team-wide
- **Local** (stored in `~/.claude.json` under project path) — personal tokens
- **User** (`~/.claude.json`) — available across all projects

For most integrations, use project scope with `${ENV_VAR}` references for secrets.

### Step 3: Generate Configuration

Create or update `.mcp.json` in the project repo root. Use environment variable expansion (`${VAR}`) for all secrets — never hardcode credentials.

Refer to `references/mcp-configs.md` for complete configuration JSON for each integration.

### Step 4: Document Required Environment Variables

List all environment variables that must be set:
- Where to obtain each credential (GitHub PAT, Coolify token, etc.)
- Recommended scopes and permissions
- Rotation schedule

### Step 5: Windows-Specific Notes

On Windows, wrap npx-based servers with `cmd /c`:
```json
{
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@masonator/coolify-mcp"]
}
```

### Step 6: Verification

After configuration, instruct the user to:
1. Launch Claude Code in the project directory
2. Run `/mcp` to check server connectivity
3. Test each server with a simple query

## Additional Resources

### Reference Files

- **`references/mcp-configs.md`** — Complete .mcp.json configuration blocks for every integration, including authentication setup, environment variables, and verification prompts
