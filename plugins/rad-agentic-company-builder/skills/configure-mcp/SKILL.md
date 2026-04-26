---
name: configure-mcp
description: This skill should be used when the user says "configure MCP", "set up MCP servers", "add MCP integrations", "connect GitHub MCP", "set up Coolify MCP", "configure database MCP", "add Google Workspace MCP", "set up Docker MCP", "create .mcp.json", or wants to configure Model Context Protocol server integrations for their agentic company project.
argument-hint: "[--integrations github,coolify,postgres,google-workspace,docker,playwright,ssh]"
user-invocable: true
allowed-tools: Read Glob Grep Write Edit Bash
---

# Configure MCP Server Integrations

Set up Model Context Protocol server configurations for a Claude Code project. **Paired with `check-mcp-config.py`** — every config the skill writes is validated for syntax, missing transport, hardcoded secrets, and Windows npx wrapping before declaring done.

## Source

- MCP protocol: [Model Context Protocol spec](https://modelcontextprotocol.io)
- Official MCP registry: https://registry.modelcontextprotocol.io/
- Specific server packages: per-vendor (linked in each section below)

## When MCP servers add value vs. when they don't

Claude Code's Bash tool handles most tasks natively. MCP adds value for:
- **Structured access to vendor APIs** — typed tool calls beat arbitrary shell scripting against REST APIs
- **Claude Desktop / Routines** — these contexts have no shell, so MCP is the only option
- **Audit and policy** — MCP tool calls are loggable and policy-gateable in ways that raw `curl` is not
- **Vendor-side rate-limit / auth handling** — the server handles backoff / token refresh

When NOT worth it: if a single `gh pr list` or `curl` call gets the job done in your local context, MCP is overhead.

## Available Integrations (verified April 2026)

| Integration | MCP Server | Source | Purpose |
|---|---|---|---|
| **GitHub** | Official GitHub remote MCP | [github.com/github/github-mcp-server](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md) | Repos, PRs, issues, Actions, code scanning |
| **Coolify** | `@masonator/coolify-mcp` | [github.com/StuMason/coolify-mcp](https://github.com/StuMason/coolify-mcp) | Deployment control (38 tools per the package README; the "85% token reduction" claim is the package author's, not independently verified) |
| **PostgreSQL** | `crystaldba/postgres-mcp` | [github.com/crystaldba/postgres-mcp](https://github.com/crystaldba/postgres-mcp) | SQL execution, EXPLAIN plans, index recommendations, health checks |
| **Prisma** | Built-in `prisma mcp` | Prisma docs | Migrations, schema status |
| **Google Workspace** | `workspace-mcp` | [github.com/taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp) | Gmail, Drive, Calendar, Docs, Sheets, Slides, Forms, Tasks, Contacts, Chat (100+ tools per the project's own claim) |
| **Docker** | `mcp-server-docker` | community | Container management (local + remote) |
| **Playwright** | `@playwright/mcp` | Microsoft official | Browser automation, screenshots, accessibility |
| **SSH** | community `ssh-mcp` | community | Structured remote command execution |
| **Stripe** | Official | [docs.stripe.com/mcp](https://docs.stripe.com/mcp) | Used by `add-function-agent --function billing` |
| **HubSpot** | Official | [developers.hubspot.com/mcp](https://developers.hubspot.com/mcp) | Used by `add-function-agent --function crm-ops` |
| **QuickBooks** | Official Intuit | [github.com/intuit/quickbooks-online-mcp-server](https://github.com/intuit/quickbooks-online-mcp-server) | Used by `add-function-agent --function bookkeeping` |
| **Vanta** | Official open-source | [Vanta MCP Server](https://mcpservers.org/servers/VantaInc/vanta-mcp-server) | Used by `add-function-agent --function compliance` |

For business-function MCPs, prefer `add-function-agent` — it bundles the MCP entry with an agent definition and a scope file. Use `configure-mcp` for engineering / infrastructure MCPs that don't need a dedicated agent.

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
