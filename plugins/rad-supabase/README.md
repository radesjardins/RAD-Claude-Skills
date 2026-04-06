# rad-supabase

End-to-end Supabase development and operations for Claude Code. Covers both the **Supabase CLI** (local development, CI/CD) and **Supabase MCP tools** (remote project operations).

**Target:** Supabase platform (hosted projects). Compatible with Supabase CLI v1.x+ and the official Supabase MCP server.

## Skills

| Skill | Triggers | What It Covers |
|-------|----------|---------------|
| **supabase-best-practices** | "set up Supabase", "supabase init", "local development" | Project structure, local dev workflow, CLI vs MCP decision guide, config.toml, conventions |
| **supabase-projects** | "create project", "list projects", "API keys", "pause project" | Project/org management, costs, API keys, regions, pause/restore, linking |
| **supabase-database** | "execute SQL", "list tables", "generate types", "database schema" | SQL execution, table management, extensions, TypeScript type generation, push/pull |
| **supabase-migrations** | "create migration", "apply migration", "migration history" | Migration creation, application, naming, drift handling, squashing, repair |
| **supabase-edge-functions** | "deploy function", "edge function", "Deno", "serverless" | Function development, deployment, local serving, secrets, Deno patterns, logs |
| **supabase-auth** | "Supabase auth", "sign up", "OAuth", "JWT" | Auth providers, client-side auth, server-side verification, config, user management |
| **supabase-branching** | "database branch", "create branch", "merge branch" | Branch lifecycle, merge, rebase, reset, delete, PR preview environments, costs |
| **supabase-security** | "RLS", "Row Level Security", "security advisor", "secrets" | RLS policies, policy patterns, security advisors, secrets management, hardening |
| **supabase-storage** | "storage bucket", "file upload", "storage policy" | Bucket management, file operations, storage policies, image transformations, signed URLs |
| **supabase-realtime** | "Supabase Realtime", "subscribe to table", "broadcast", "presence" | Postgres changes, broadcast, presence, channel management, publication config |
| **supabase-troubleshooting** | "Supabase logs", "debug", "error", "performance" | Log viewing, security/performance advisors, doc search, CLI diagnostics, common fixes |

## Agents

| Agent | Triggers | What It Does |
|-------|----------|-------------|
| **supabase-reviewer** | "review my Supabase setup", "check Supabase security", "production ready?" | Autonomous audit of schema, RLS policies, edge functions, migrations, and configuration for security and best practices |

## Installation

### From Plugin Directory

```bash
claude --plugin-dir /path/to/rad-supabase
```

### Prerequisites

- **Supabase CLI** installed and authenticated (`supabase login`)
- **Supabase MCP server** connected in Claude Code (for remote operations)
- A Supabase project (hosted) for MCP tool usage

## MCP Tools Covered

This plugin teaches Claude how and when to use all 28 Supabase MCP tools:

| Category | MCP Tools |
|----------|-----------|
| **Projects** | `list_projects`, `create_project`, `get_project`, `get_project_url`, `get_publishable_keys`, `pause_project`, `restore_project` |
| **Organizations** | `list_organizations`, `get_organization` |
| **Costs** | `get_cost`, `confirm_cost` |
| **Database** | `execute_sql`, `list_tables`, `list_extensions`, `generate_typescript_types` |
| **Migrations** | `apply_migration`, `list_migrations` |
| **Edge Functions** | `deploy_edge_function`, `get_edge_function`, `list_edge_functions` |
| **Branching** | `create_branch`, `list_branches`, `merge_branch`, `rebase_branch`, `reset_branch`, `delete_branch` |
| **Observability** | `get_logs`, `get_advisors` |
| **Documentation** | `search_docs` |

## CLI Commands Covered

| Category | CLI Commands |
|----------|-------------|
| **Setup** | `init`, `start`, `stop`, `status`, `login`, `link` |
| **Database** | `db push`, `db pull`, `db reset`, `db lint`, `db diff` |
| **Migrations** | `migration new`, `migration list`, `migration repair`, `migration squash` |
| **Functions** | `functions new`, `functions serve`, `functions deploy`, `functions download`, `functions delete`, `functions list` |
| **Secrets** | `secrets set`, `secrets list`, `secrets unset` |
| **Types** | `gen types typescript` |
| **Inspection** | `inspect db calls`, `inspect db long-running`, `inspect db outliers`, `inspect db bloat`, `inspect db cache-hit`, `inspect db index-usage` |
| **Branches** | `branches create`, `branches list`, `branches delete` |

## Important Caveats

- **CLI vs MCP:** The CLI is for local development workflows. MCP tools operate on remote projects. Skills explain when to use each.
- **Cost confirmation:** Creating projects and branches via MCP requires a cost confirmation flow. Never skip this.
- **RLS is mandatory:** Every public table must have RLS enabled in production. The security skill and reviewer agent enforce this.
- **Service role key:** Never expose to client-side code. Skills reinforce this throughout.

## Version Compatibility

| Plugin Version | Supabase CLI | Supabase MCP | Supabase Platform |
|---------------|-------------|-------------|-------------------|
| 1.0.0 | v1.x+ | Official MCP server | Current |
