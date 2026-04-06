---
name: supabase-migrations
description: >
  This skill should be used when creating, applying, listing, or managing database migrations
  in Supabase projects, or when making DDL schema changes that need to be tracked.
  Trigger when: "create migration", "apply migration", "list migrations", "migration history",
  "schema change", "DDL change", "supabase migration new", "supabase db push",
  "migration best practices", "migration drift", "repair migration", "squash migrations",
  "migration workflow", "database versioning", or any tracked schema modification.
---

# Supabase Migration Workflows

Guidance for creating, applying, and managing database migrations using both MCP tools and CLI.

## Core Concept

Migrations are versioned SQL files that track database schema changes. They run in timestamp order and provide a reproducible path from an empty database to the current schema. Supabase stores migration history in the `supabase_migrations.schema_migrations` table.

## Applying Migrations (MCP)

Use `apply_migration` for all DDL operations against remote projects:

```
mcp__supabase__apply_migration(
  project_id: "<project_id>",
  name: "create_profiles_table",
  query: "create table public.profiles (id uuid primary key, name text not null);"
)
```

**Critical rules:**
- Use `apply_migration` for DDL (CREATE, ALTER, DROP). Never use `execute_sql` for DDL.
- Use snake_case for migration names: `create_profiles_table`, `add_rls_to_orders`
- Do not hardcode references to generated IDs in data migrations
- Each migration should be atomic — one logical change per migration

### Multi-Statement Migrations

Wrap related changes in a single migration:

```sql
-- name: add_profiles_with_rls
create table public.profiles (
  id uuid references auth.users(id) on delete cascade primary key,
  display_name text,
  bio text,
  created_at timestamptz default now() not null
);

alter table public.profiles enable row level security;

create policy "Users can read all profiles"
  on public.profiles for select
  using (true);

create policy "Users can update own profile"
  on public.profiles for update
  using (auth.uid() = id);
```

## Listing Migrations (MCP)

```
mcp__supabase__list_migrations(project_id: "<project_id>")
```

Returns all applied migrations with timestamps and names. Use this to verify migration state before applying new ones.

## Creating Migrations (CLI)

### New Empty Migration

```bash
supabase migration new <name>
```

Creates `supabase/migrations/<timestamp>_<name>.sql`. Write the DDL SQL in this file.

### Pull Remote Schema as Migration

```bash
supabase db pull
```

Creates a migration file reflecting the current remote schema. Use when schema changes were made outside of migrations (e.g., via Dashboard).

### Diff-Based Migration

```bash
supabase db diff --use-migra -f <name>
```

Compares local database state against migration files and generates a diff. Useful for capturing manual local changes.

## Pushing Migrations (CLI)

```bash
supabase db push
```

Applies all pending local migrations to the linked remote project. Migrations that have already been applied (tracked in `schema_migrations`) are skipped.

**Dry run first:**
```bash
supabase db push --dry-run
```

## Migration Best Practices

### Naming Conventions

Use descriptive snake_case names that indicate the action:

| Prefix | Use For | Example |
|--------|---------|---------|
| `create_` | New tables | `create_profiles_table` |
| `add_` | New columns, indexes, policies | `add_avatar_to_profiles` |
| `alter_` | Column type changes | `alter_price_to_numeric` |
| `drop_` | Removing objects | `drop_legacy_logs_table` |
| `enable_` | Enabling features | `enable_rls_on_orders` |
| `create_fn_` | Functions | `create_fn_handle_updated_at` |
| `seed_` | Data seeding | `seed_default_categories` |

### Atomic Migrations

Each migration should represent one logical change. Group related DDL (table + RLS + policies) together, but separate unrelated changes into distinct migrations.

### Idempotent Patterns

Use `if not exists` / `if exists` for safety:

```sql
create table if not exists public.profiles (...);
create index if not exists idx_profiles_user on public.profiles(user_id);
drop table if exists public.legacy_logs;
```

### Migration Order Dependencies

Migrations run in timestamp order. Ensure dependent migrations have later timestamps:
1. `20240101000000_create_profiles.sql` (table first)
2. `20240101000001_add_rls_to_profiles.sql` (policies depend on table)

## Handling Migration Drift

Migration drift occurs when the remote schema diverges from migration files. Common causes:
- Dashboard schema edits
- Manual SQL execution
- Multiple developers with conflicting migrations

### Detection

```bash
supabase db diff --use-migra    # Compare local state vs migrations
supabase db lint                 # Check for schema issues
```

### Resolution

1. **Pull current remote schema**: `supabase db pull`
2. **Review the generated migration**: Verify it captures the actual drift
3. **Decide**: Keep the drift (commit the migration) or revert (write a corrective migration)

### Repairing Migration History

If a migration was applied manually and needs to be marked as applied:

```bash
supabase migration repair --status applied <version>
```

To mark a migration as reverted:
```bash
supabase migration repair --status reverted <version>
```

## Squashing Migrations (CLI)

Combine multiple migrations into fewer files:

```bash
supabase migration squash --version <target_version>
```

This combines all migrations up to the target version into a single file. Useful for cleaning up long migration histories before releases.

## CLI vs MCP Decision Matrix

| Task | Use CLI | Use MCP |
|------|---------|---------|
| Create migration file | `migration new` | Not available — write file manually |
| Apply to remote | `db push` | `apply_migration` |
| List migrations | `migration list` | `list_migrations` |
| Pull remote schema | `db pull` | Not available |
| Diff check | `db diff` | Not available |
| Repair history | `migration repair` | Not available |
| Squash | `migration squash` | Not available |
| Reset local DB | `db reset` | Not available |

**When to use MCP `apply_migration`:** When operating directly in Claude Code without a local Supabase setup, or when making one-off schema changes to a remote project interactively.

**When to use CLI `db push`:** When following a local-first development workflow with migration files tracked in git.
