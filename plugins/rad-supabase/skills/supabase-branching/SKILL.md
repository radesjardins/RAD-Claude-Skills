---
name: supabase-branching
description: >
  This skill should be used when working with Supabase database branching, creating preview
  environments, merging branches to production, rebasing branches, or managing branch lifecycle.
  Trigger when: "database branch", "create branch", "merge branch", "rebase branch",
  "reset branch", "delete branch", "preview environment", "Supabase branching",
  "branch workflow", "migration drift", "branch status", "list branches",
  "Branching 2.0", "preview branch", "persistent branch",
  or managing Supabase development branches for schema isolation.
---

# Supabase Database Branching

Guidance for using Supabase's database branching feature to create isolated development environments. **Branching 2.0** (Pro plan and above) ships two branch types.

## Overview

Database branching creates isolated Postgres instances that inherit all migrations from the main project. Branches are ideal for:
- PR-based preview environments (auto-managed by GitHub PR integration)
- Testing schema changes in isolation
- Parallel feature development without conflicts
- Safe migration testing before production

**Important:** Branch databases are fresh — production data does not carry over. Only schema (via migrations) is applied.

## Branch types (Branching 2.0)

| Type | Lifecycle | Cost shape | Best for |
|------|-----------|-----------|----------|
| **Preview** | Auto-paused on PR close, auto-deleted shortly after | Compute-hours when active + egress | PR review environments |
| **Persistent** | Long-lived; never auto-deleted | Compute-hours (continuously running) + egress | Staging, QA, integration test environments |

**Cost model:** branches bill compute-hours (per the project's instance size) plus egress. Disk stays within the project's plan allowance (8 GB on Pro). Always run `get_cost` first; never assume flat fees.

## Branch Lifecycle

```
Production DB ──→ Create Branch ──→ Develop & Test ──→ Merge to Production
                       ↑                                       ↓
                   (applies all migrations)            (applies branch migrations
                                                        + edge functions to prod)
```

## Creating a Branch (MCP)

Branch creation requires cost confirmation:

1. **Get cost:**
   ```
   mcp__supabase__get_cost(type: "branch", organization_id: "<org_id>")
   ```

2. **Confirm cost** with user:
   ```
   mcp__supabase__confirm_cost(type: "branch", recurrence: "hourly", amount: <amount>)
   ```

3. **Create branch:**
   ```
   mcp__supabase__create_branch(
     project_id: "<project_id>",
     name: "feature-user-profiles",
     confirm_cost_id: "<cost_id>"
   )
   ```

The branch gets its own `project_ref` (project ID). Use this ID for all MCP operations on the branch (`execute_sql`, `apply_migration`, `deploy_edge_function`, etc.).

## Listing Branches (MCP)

```
mcp__supabase__list_branches(project_id: "<project_id>")
```

Returns branch details including:
- Branch ID
- Branch name
- Type (Preview vs Persistent)
- Status (creating, active, paused, etc.)
- Created at timestamp

Use the status field to check when operations like merge, rebase, or reset complete.

## Working with Branches

Once a branch is created, treat its `project_ref` like any other project:

### Apply Migrations to Branch
```
mcp__supabase__apply_migration(
  project_id: "<branch_project_ref>",
  name: "add_user_preferences",
  query: "create table public.user_preferences (...);"
)
```

### Execute SQL on Branch
```
mcp__supabase__execute_sql(
  project_id: "<branch_project_ref>",
  query: "SELECT * FROM public.user_preferences;"
)
```

### Deploy Edge Functions to Branch
```
mcp__supabase__deploy_edge_function(
  project_id: "<branch_project_ref>",
  name: "my-function",
  ...
)
```

## Merging to Production (MCP)

Merge applies branch migrations and edge functions to the production database:

```
mcp__supabase__merge_branch(branch_id: "<branch_id>")
```

**Pre-merge checklist:**
1. Verify all migrations apply cleanly on the branch (`list_migrations`).
2. Test edge functions on the branch.
3. Run `get_advisors(type: "security")` on the branch to check for missing RLS, lint violations.
4. Optionally run `python plugins/rad-supabase/scripts/audit-rls.py` on the local migration files for static checks.
5. Ensure no migration conflicts with production.

**After merge:** the branch is consumed. Its migrations and edge functions are now part of production.

## Rebasing a Branch (MCP)

Rebase applies newer production migrations onto the branch. Use this to handle migration drift when production has moved ahead:

```
mcp__supabase__rebase_branch(branch_id: "<branch_id>")
```

**When to rebase:**
- Production received new migrations since the branch was created.
- Another branch was merged to production, introducing schema changes.
- Periodic sync to keep the branch up to date.

Monitor branch status after rebase — it runs asynchronously:
```
mcp__supabase__list_branches(project_id: "<project_id>")
```

## Resetting a Branch (MCP)

Reset drops all untracked changes and re-applies migrations from scratch:

```
mcp__supabase__reset_branch(branch_id: "<branch_id>")
```

**With specific migration version:**
```
mcp__supabase__reset_branch(
  branch_id: "<branch_id>",
  migration_version: "20240101000000"
)
```

**Warning:** Any untracked data or schema changes on the branch will be lost.

## Deleting a Branch (MCP)

```
mcp__supabase__delete_branch(branch_id: "<branch_id>")
```

Delete branches that are no longer needed to stop incurring costs. Preview branches auto-delete on PR close; persistent branches need explicit deletion.

## Branch Workflow: Feature Development

A typical feature development workflow:

1. **Create branch** from production project (Preview type).
2. **Apply migrations** for the new feature schema.
3. **Deploy edge functions** to the branch for testing.
4. **Run tests** against the branch endpoint.
5. **Rebase** if production has moved ahead.
6. **Merge** when feature is complete and tested.
7. **Delete** the branch (automatic for Preview branches on PR close).

## Branch Workflow: PR Preview Environments

Integrate branching with GitHub PR integration (built into Supabase Branching 2.0):

1. On PR open → Supabase creates a Preview branch automatically.
2. PR migrations are applied on push.
3. Edge functions deploy to the branch.
4. Vercel Marketplace integration syncs branch env vars to Vercel preview deployments.
5. On PR merge → branch merges to production.
6. On PR close (without merge) → branch auto-deletes.

For non-GitHub setups, drive the same lifecycle via Management API + `create_branch` / `merge_branch` / `delete_branch`.

## CLI Branch Commands

```bash
supabase branches create <name>         # Create a branch
supabase branches list                  # List branches
supabase branches update <id> --notify-url <url>  # Update branch settings (e.g., GitHub webhook URL)
supabase branches delete <id>           # Delete a branch
```

Most branch operations (merge, rebase, reset) are more commonly done via MCP or the dashboard.

## Cost Considerations

- Branches bill compute-hours (per instance size) plus egress.
- Disk stays within the project's plan allowance.
- Preview branches auto-pause when idle and auto-delete on PR close — cost-effective.
- Persistent branches run continuously — most expensive, but stable for staging/QA.
- Always check costs with `get_cost` before creating; the live dashboard usage page is the source of truth for current rates and per-project caps.

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| Branch stuck in "creating" | Provisioning delay | Wait and poll `list_branches` |
| Merge fails | Migration conflict | Rebase first, resolve conflicts |
| Drift after merge | Concurrent migrations | Rebase remaining branches |
| Branch not responding | Branch may be paused (Preview) | Check status via `list_branches`; activity unpauses |
| Preview branch unexpectedly deleted | PR was closed/merged | Expected behavior; create a Persistent branch if you need durability |
