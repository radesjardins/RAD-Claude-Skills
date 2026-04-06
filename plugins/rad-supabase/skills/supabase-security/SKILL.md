---
name: supabase-security
description: >
  This skill should be used when implementing Row Level Security (RLS) policies, running security
  advisors, managing secrets, hardening Supabase projects, or addressing security concerns.
  Trigger when: "RLS", "Row Level Security", "security policy", "create policy",
  "enable RLS", "security advisor", "Supabase secrets", "service role key safety",
  "auth.uid() in RLS policies", "security hardening", "policy patterns",
  "Supabase security best practices", "fix security warning",
  "restrict row access", "table is publicly accessible",
  "prevent unauthorized access", "who can read this table",
  or implementing any authorization or access control in Supabase.
---

# Supabase Security

Guidance for implementing Row Level Security, managing secrets, and hardening Supabase projects.

## Row Level Security (RLS)

RLS is the primary authorization mechanism in Supabase. It restricts which rows a user can access based on their identity (JWT claims).

### Enable RLS

**Every public table must have RLS enabled.** This is non-negotiable for production.

```sql
alter table public.profiles enable row level security;
```

Without RLS enabled, any authenticated user (or anon key holder) can read/write all rows.

### Policy Structure

```sql
create policy "<descriptive_name>"
  on <schema>.<table>
  for <operation>          -- select, insert, update, delete, all
  to <role>                -- anon, authenticated, service_role (optional, defaults to public)
  using (<read_condition>) -- Filter rows for SELECT, UPDATE, DELETE
  with check (<write_condition>); -- Validate rows for INSERT, UPDATE
```

**`using`** — Filters rows the user can see (read path). Applied to SELECT, UPDATE (existing rows), DELETE.

**`with check`** — Validates new/updated row data (write path). Applied to INSERT, UPDATE (new values).

### Common Policy Patterns

#### Users Read Own Data
```sql
create policy "Users read own data"
  on public.profiles for select
  to authenticated
  using (auth.uid() = user_id);
```

#### Public Read, Authenticated Write
```sql
create policy "Anyone can read posts"
  on public.posts for select
  using (true);

create policy "Authenticated users create posts"
  on public.posts for insert
  to authenticated
  with check (auth.uid() = author_id);
```

#### Role-Based Access
```sql
create policy "Admins can do everything"
  on public.settings for all
  to authenticated
  using (
    exists (
      select 1 from public.user_roles
      where user_roles.user_id = auth.uid()
      and user_roles.role = 'admin'
    )
  );
```

#### Team/Organization Access
```sql
create policy "Team members can read team data"
  on public.team_documents for select
  to authenticated
  using (
    exists (
      select 1 from public.team_members
      where team_members.team_id = team_documents.team_id
      and team_members.user_id = auth.uid()
    )
  );
```

#### Owner + Admin Pattern
```sql
create policy "Owner or admin can update"
  on public.projects for update
  to authenticated
  using (
    auth.uid() = owner_id
    or exists (
      select 1 from public.project_members
      where project_id = projects.id
      and user_id = auth.uid()
      and role = 'admin'
    )
  );
```

**Note:** Omitting `with check` on UPDATE allows any column values. Add a `with check` clause to constrain what values the updated row may contain.

### RLS Performance Tips

- **Index columns used in policies** — `auth.uid()` comparisons need indexes on the FK column
- **Avoid complex subqueries** in hot-path policies — use materialized views or denormalization for complex authorization
- **Use `security definer` functions** for reusable policy logic:
  ```sql
  create function public.is_team_member(team_id uuid)
  returns boolean as $$
    select exists (
      select 1 from public.team_members
      where team_members.team_id = $1
      and team_members.user_id = auth.uid()
    );
  $$ language sql security definer stable set search_path = '';
  ```

## Security Advisors (MCP)

Run security advisors regularly, especially after DDL changes:

```
mcp__supabase__get_advisors(
  project_id: "<project_id>",
  type: "security"
)
```

This returns advisory notices for:
- Tables without RLS enabled
- Tables with RLS enabled but no policies
- Functions with security definer that may be exploitable
- Other security vulnerabilities

**Include remediation URLs as clickable links** so users can reference issues directly.

**When to run:** After every migration that creates or alters tables, after enabling/disabling RLS, and periodically as a health check.

## Secrets Management

### Via CLI

```bash
# Set secrets (available as env vars in edge functions)
supabase secrets set STRIPE_SECRET_KEY=sk_live_xxx
supabase secrets set RESEND_API_KEY=re_xxx WEBHOOK_SECRET=whsec_xxx

# List secrets (names only, values are hidden)
supabase secrets list

# Remove secrets
supabase secrets unset STRIPE_SECRET_KEY
```

### Secret Best Practices

- Never hardcode secrets in edge function code
- Use `Deno.env.get("SECRET_NAME")` in edge functions
- Rotate secrets periodically
- Use different secrets for staging vs production
- Never commit `.env` files with real secrets to git

## API Key Security

| Key | Exposure | RLS | Use For |
|-----|----------|-----|---------|
| **Anon key** | Client-safe | Enforced | Browser/mobile apps |
| **Publishable key** | Client-safe | Enforced | Modern replacement for anon key |
| **Service role key** | Server-only | Bypassed | Admin operations, edge functions |

**Critical:** The service role key bypasses all RLS policies. Never expose it to the client.

## Security Hardening Checklist

1. **Enable RLS** on every `public` table
2. **Create appropriate policies** for each table and operation
3. **Run security advisors** after schema changes
4. **Use anon/publishable key** on client, service role key only server-side
5. **Enable email confirmation** in production auth settings
6. **Set restrictive CORS** on edge functions
7. **Validate inputs** in edge functions before database operations
8. **Use parameterized queries** — never concatenate user input into SQL
9. **Review `security definer` functions** for privilege escalation
10. **Enable 2FA** on the Supabase Dashboard account

## Disabling RLS (When Appropriate)

Some tables may legitimately not need RLS:
- Lookup/reference tables with public data
- Tables only accessed via `security definer` functions
- Internal tables in non-public schemas

To explicitly allow public access without policy warnings:
```sql
-- Option 1: RLS enabled with permissive policy
alter table public.countries enable row level security;
create policy "Public read" on public.countries for select using (true);

-- Option 2: Grant direct access (less recommended)
grant select on public.countries to anon, authenticated;
```

## Searching Security Docs (MCP)

For the latest security documentation:
```
mcp__supabase__search_docs(query: "RLS policies security <specific topic>")
```
