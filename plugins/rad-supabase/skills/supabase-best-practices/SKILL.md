---
name: supabase-best-practices
description: >
  This skill should be used when the user asks about Supabase best practices, project conventions,
  local development setup, or needs an overview of how the CLI and MCP tools work together.
  Trigger when: "Supabase best practices", "Supabase conventions", "supabase init",
  "Supabase local development", "supabase start", "Supabase project structure",
  "Supabase config.toml", "CLI vs MCP when to use which", "Supabase common pitfalls",
  "Supabase daily development workflow", "how to organize Supabase project",
  "Supabase environment setup", "set up local Supabase",
  or starting a new Supabase-based project. For specific tasks like creating migrations,
  managing auth, or deploying functions, the corresponding domain-specific skills are preferred.
---

# Supabase Best Practices

Comprehensive guidance for Supabase project architecture, local development workflows, and conventions. Covers both the Supabase CLI and the Supabase MCP tools available in Claude Code.

## Two Interfaces: CLI vs MCP

Supabase provides two complementary interfaces for Claude Code:

### Supabase CLI (Local Development)

The CLI is the primary tool for local development, project initialization, and CI/CD workflows.

```bash
supabase init                    # Initialize local project structure
supabase start                   # Start local Supabase stack (Postgres, Auth, Storage, etc.)
supabase stop                    # Stop local stack
supabase status                  # Show local service URLs and keys
supabase link --project-ref ID   # Link to remote project
supabase login                   # Authenticate with Supabase platform
```

### Supabase MCP (Remote Operations)

The MCP tools operate directly against remote Supabase projects. Use MCP when:
- Executing SQL against a remote project
- Applying migrations to remote databases
- Deploying edge functions
- Managing branches, projects, and organizations
- Retrieving logs, advisors, or documentation

**Decision rule:** Use the CLI for local development and CI/CD. Use MCP for remote operations and when the user is working in Claude Code without a local Supabase setup.

## Project Structure

A standard Supabase project follows this layout after `supabase init`:

```
project-root/
├── supabase/
│   ├── config.toml              # Local dev configuration
│   ├── migrations/              # SQL migration files (timestamped)
│   │   ├── 20240101000000_initial_schema.sql
│   │   └── 20240102000000_add_profiles.sql
│   ├── functions/               # Edge Functions (Deno/TypeScript)
│   │   └── hello-world/
│   │       └── index.ts
│   ├── seed.sql                 # Seed data for local development
│   └── tests/                   # pgTAP or other test files
├── src/                         # Application source code
└── .env.local                   # Local environment variables
```

**`.env.local` contents:** Store `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and optionally `SUPABASE_SERVICE_ROLE_KEY` (server-side only). Get these from `supabase status` (local) or the Dashboard (remote).

## Local Development Workflow

### Initial Setup

```bash
supabase init                              # Creates supabase/ directory
supabase login                             # Authenticate (one-time)
supabase link --project-ref <project-id>   # Link to remote project
supabase db pull                           # Pull existing remote schema
supabase start                             # Start local Supabase stack
```

### Daily Development Cycle

1. **Start local stack**: `supabase start` — spins up Postgres, Auth, Storage, Realtime, Edge Runtime
2. **Make schema changes**: Write SQL migration files or use `supabase migration new <name>`
3. **Apply locally**: `supabase db reset` applies all migrations from scratch on local DB
4. **Generate types**: `supabase gen types typescript --local > src/types/supabase.ts`
5. **Test edge functions**: `supabase functions serve` for local function development
6. **Push to remote**: `supabase db push` applies pending migrations to linked project

### Environment Management

Manage multiple environments (local, staging, production) using branches or separate projects:

| Environment | Method | When to Use |
|-------------|--------|-------------|
| Local | `supabase start` | Day-to-day development |
| Preview | Database branching | PR-based preview environments |
| Staging | Separate project | Pre-production testing |
| Production | Separate project | Live application |

Link different environments using `--project-ref`:
```bash
supabase link --project-ref <staging-id>   # Link to staging
supabase db push                            # Push migrations to staging
```

## Configuration (config.toml)

The `supabase/config.toml` file controls the local development stack. Key sections:

- **`[api]`** — Port, schemas exposed, max rows
- **`[db]`** — Postgres port, major version, connection pooling
- **`[auth]`** — Site URL, external providers, JWT expiry
- **`[storage]`** — File size limits, image transformation
- **`[edge_runtime]`** — Deno version, execution policy
- **`[realtime]`** — Realtime service configuration

## Key Conventions

### Migration Naming
Use snake_case with descriptive names: `create_profiles_table`, `add_rls_to_orders`, `create_stripe_webhook_function`.

### Schema Organization
- Use the `public` schema for application tables
- Use `auth` schema (managed by Supabase) for authentication
- Use `storage` schema (managed by Supabase) for file storage metadata
- Create custom schemas for internal/admin logic if needed

### Row Level Security (RLS)
Enable RLS on every public table. This is the single most important security practice in Supabase. Create policies that match the application's access patterns.

### Edge Function Naming
Use kebab-case for function directories: `send-email`, `stripe-webhook`, `generate-og-image`.

### Type Generation
Always regenerate TypeScript types after schema changes:
```bash
# Local types
supabase gen types typescript --local > src/types/supabase.ts

# Remote types (via MCP)
# Use mcp__supabase__generate_typescript_types with project_id
```

## MCP Quick Reference

MCP tools are prefixed with `mcp__supabase__` when called (e.g., `mcp__supabase__list_projects`). Short names used below for brevity.

| Task | MCP Tool |
|------|----------|
| List projects | `list_projects` |
| Get project details | `get_project` |
| Execute SQL | `execute_sql` |
| Apply migration | `apply_migration` |
| List tables | `list_tables` |
| Deploy function | `deploy_edge_function` |
| Get logs | `get_logs` |
| Search docs | `search_docs` |
| Security check | `get_advisors` (type: security) |
| Performance check | `get_advisors` (type: performance) |

## CLI Quick Reference

| Task | CLI Command |
|------|------------|
| Initialize project | `supabase init` |
| Start local stack | `supabase start` |
| Stop local stack | `supabase stop` |
| Link remote project | `supabase link --project-ref ID` |
| Pull remote schema | `supabase db pull` |
| Push migrations | `supabase db push` |
| Reset local DB | `supabase db reset` |
| Create migration | `supabase migration new <name>` |
| Generate types | `supabase gen types typescript` |
| Serve functions | `supabase functions serve` |
| Deploy functions | `supabase functions deploy` |
| Manage secrets | `supabase secrets set/list/unset` |
| View DB status | `supabase inspect db` |

## Common Pitfalls

1. **Forgetting RLS** — Always enable RLS on public tables. Run `get_advisors` with type "security" to catch missing policies.
2. **Direct schema edits** — Never modify the remote database schema via Dashboard SQL editor in production. Use migrations.
3. **Hardcoded keys** — Store API keys in environment variables, never in code. Use `supabase secrets set` for edge function secrets.
4. **Missing type regeneration** — Regenerate TypeScript types after every schema change to maintain type safety.
5. **Ignoring advisors** — Run both security and performance advisors regularly after DDL changes.
