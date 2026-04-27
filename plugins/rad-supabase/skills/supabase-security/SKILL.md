---
name: supabase-security
description: >
  This skill should be used when implementing Row Level Security (RLS) policies, running security
  advisors, managing secrets, hardening Supabase projects, or addressing security concerns.
  Trigger when: "RLS", "Row Level Security", "security policy", "create policy",
  "enable RLS", "security advisor", "Supabase secrets", "service role key safety",
  "secret key", "publishable key", "auth.uid() in RLS policies", "(select auth.uid())",
  "initPlan", "Splinter lint", "security definer", "search_path",
  "raw_user_meta_data", "raw_app_meta_data", "Custom Access Token Hook", "RBAC",
  "Supabase security best practices", "fix security warning",
  "restrict row access", "table is publicly accessible",
  "prevent unauthorized access", "who can read this table",
  or implementing any authorization or access control in Supabase.
---

# Supabase Security

Guidance for implementing Row Level Security, managing secrets, and hardening Supabase projects. Pinned to April 2026 best practices.

## Row Level Security (RLS)

RLS is the primary authorization mechanism in Supabase. It restricts which rows a user can access based on their identity (JWT claims).

### Enable RLS

**Every public table must have RLS enabled.** This is non-negotiable for production.

```sql
alter table public.profiles enable row level security;
```

Without RLS enabled, any client holding the anon/publishable key can read/write all rows. Enforced by Splinter lint **0013 (`rls_disabled_in_public`)** and statically by `scripts/audit-rls.py`.

### Policy Structure

```sql
create policy "<descriptive_name>"
  on <schema>.<table>
  for <operation>          -- select, insert, update, delete (avoid FOR ALL)
  to <role>                -- anon, authenticated, service_role (optional, defaults to public)
  using (<read_condition>) -- Filter rows for SELECT, UPDATE, DELETE
  with check (<write_condition>); -- Validate rows for INSERT, UPDATE
```

**`using`** — Filters rows the user can see (read path). Applied to SELECT, UPDATE (existing rows), DELETE.

**`with check`** — Validates new/updated row data (write path). Applied to INSERT, UPDATE (new values).

**Prefer separate policies per command.** A `FOR ALL` policy mixes read and write logic in a single `using` clause, which is hard to reason about. The current docs recommend one policy per SELECT / INSERT / UPDATE / DELETE.

### The `(select auth.uid())` initPlan rule

**Always wrap `auth.uid()`, `auth.jwt()`, and `auth.role()` in a subquery** in policy expressions:

```sql
-- Slow on large tables (auth.uid() called per row)
using (auth.uid() = user_id)

-- Fast (Postgres caches the result via initPlan, called once per statement)
using ((select auth.uid()) = user_id)
```

This is enforced by Splinter lint **0003 (`auth_rls_initplan`)** and is the single biggest RLS performance lever after indexing. Documented in [RLS Performance & Best Practices](https://supabase.com/docs/guides/troubleshooting/rls-performance-and-best-practices-Z5Jjwv). Same advice for `(select auth.jwt())` and helper-function calls like `(select is_admin())` whose result doesn't depend on row data.

### Common Policy Patterns

#### Users Read Own Data
```sql
create policy "Users read own profile"
  on public.profiles for select
  to authenticated
  using ((select auth.uid()) = user_id);
```

#### Public Read, Authenticated Write
```sql
create policy "Anyone reads posts"
  on public.posts for select
  using (true);

create policy "Authenticated users create their own posts"
  on public.posts for insert
  to authenticated
  with check ((select auth.uid()) = author_id);
```

#### Team-Based Access — INVERTED form (faster)

The fast form pivots the membership check to the *table being filtered*:

```sql
create policy "Team members read team documents"
  on public.team_documents for select
  to authenticated
  using (
    team_id in (
      select team_id from public.team_members
      where user_id = (select auth.uid())
    )
  );
```

The slower-but-equivalent form (avoid):
```sql
-- AVOID: outer reference auth.uid() forces re-evaluation per row
using (
  exists (
    select 1 from public.team_members
    where team_members.team_id = team_documents.team_id
    and team_members.user_id = auth.uid()
  )
);
```

#### Owner + Admin Pattern (with helper function)

For reusable role checks, use a `security definer` helper function with **explicit `set search_path`**:

```sql
create or replace function public.is_team_admin(check_team_id uuid)
returns boolean
language sql
security definer
set search_path = ''
stable
as $$
  select exists (
    select 1 from public.team_members
    where team_id = check_team_id
    and user_id = (select auth.uid())
    and role = 'admin'
  );
$$;

create policy "Owner or team admin can update"
  on public.projects for update
  to authenticated
  using (
    (select auth.uid()) = owner_id
    or public.is_team_admin(team_id)
  )
  with check (
    (select auth.uid()) = owner_id
    or public.is_team_admin(team_id)
  );
```

The empty `set search_path = ''` prevents the function-search-path-mutable vulnerability (Splinter lint **0011**) — without it, an attacker who controls a schema in the search path can shadow Supabase's built-in functions.

### RBAC via Custom Access Token Hook (recommended)

The current best-practice for role-based access is to **populate JWT claims from an Auth Hook** rather than join `user_roles` per query:

1. Store roles in a `user_roles` table (admin-managed).
2. Register a [Custom Access Token Hook](https://supabase.com/docs/guides/auth/auth-hooks/custom-access-token-hook) — a Postgres function that runs on token mint:
   ```sql
   create or replace function public.add_role_to_jwt(event jsonb)
   returns jsonb
   language plpgsql
   security definer
   set search_path = ''
   as $$
   declare
     user_role text;
   begin
     select role into user_role from public.user_roles
     where user_id = (event->>'user_id')::uuid;
     return jsonb_set(event, '{claims,app_metadata,role}', to_jsonb(coalesce(user_role, 'user')));
   end;
   $$;
   ```
3. Read the claim in RLS — no join required:
   ```sql
   create policy "Admins manage settings"
     on public.settings for all
     to authenticated
     using ((select auth.jwt() -> 'app_metadata' ->> 'role') = 'admin')
     with check ((select auth.jwt() -> 'app_metadata' ->> 'role') = 'admin');
   ```

See [Custom Claims & RBAC guide](https://supabase.com/docs/guides/database/postgres/custom-claims-and-role-based-access-control-rbac) for the full setup.

### Critical: never read `raw_user_meta_data` in RLS

Supabase Auth stores two metadata columns:

- **`raw_app_meta_data`** — server-only writes. Safe in RLS.
- **`raw_user_meta_data`** — **user-writable** via `supabase.auth.updateUser({ data: ... })`. A user can set `{ "role": "admin" }` themselves.

Splinter lint **0015 (`rls_references_user_metadata`)** flags any policy that reads `raw_user_meta_data`. Use `raw_app_meta_data` or a JWT claim populated by an Auth Hook.

### RLS Performance Tips

- **Index columns referenced in policies** — `(select auth.uid()) = user_id` needs an index on `user_id`. Docs report >100× speedups on large tables.
- **Use the inverted team-access form** (see above).
- **Wrap stable function calls** in `(select fn())` for initPlan caching.
- **Add GIN indexes** for array/`ANY` predicates in policies.
- **Use security definer helpers** to skip RLS on read-only join tables.

## Static audit before pushing

Run the bundled validators before any `db push` to a shared remote:

```bash
python plugins/rad-supabase/scripts/audit-rls.py            # Splinter 0002/0003/0008/0011/0013/0015 + structural
python plugins/rad-supabase/scripts/check-secret-leaks.py    # service_role/secret keys in client paths
python plugins/rad-supabase/scripts/audit-edge-functions.py  # Edge Function anti-patterns
```

All three exit non-zero on findings (1 = warnings, 2 = critical). Hook into CI to block PRs with critical findings.

## Security Advisors (live database, MCP)

The static validator complements but does not replace the live advisor:

```
mcp__supabase__get_advisors(project_id: "<project_id>", type: "security")
```

Returns advisory notices including lints that need a live database (`0006 multiple_permissive_policies`, `0017 foreign_table_in_api`, `0019 insecure_queue_exposed_in_api`) plus all the static lints applied to the actual deployed schema (catches drift from migrations).

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

- Never hardcode secrets in edge function code (caught by `audit-edge-functions.py` and `check-secret-leaks.py`).
- Use `Deno.env.get("SECRET_NAME")` in edge functions.
- Rotate secrets periodically — secret keys (`sb_secret_*`) support instant revocation in the dashboard.
- Use different secrets for staging vs production.
- Never commit `.env` files with real secrets to git (caught by `check-secret-leaks.py`).

## API Key Security

| Key | Format | Exposure | RLS | Use For |
|-----|--------|----------|-----|---------|
| **Publishable key** | `sb_publishable_*` | Client-safe | Enforced | Browser/mobile (modern, recommended) |
| **Anon key** (legacy) | `eyJ...` JWT | Client-safe | Enforced | Browser/mobile (legacy projects) |
| **Secret key** | `sb_secret_*` | Server-only | **Bypasses** | Edge Functions, server routes (modern) |
| **Service role key** (legacy) | `eyJ...` JWT | Server-only | **Bypasses** | Edge Functions, server routes (legacy) |

**Critical:** The service role key and secret key bypass all RLS policies. Never expose them to the client. `check-secret-leaks.py` enforces this — references in client-side paths (heuristic: `app/`, `pages/`, `src/components/`, `+page.svelte`, `*.client.ts`) trigger a critical finding.

The new `sb_secret_*` keys also implement **client-side refusal**: if a browser-bound HTTP client tries to use one, the request is rejected. Service role JWTs don't have this — leaking one was always silently fatal.

## Security Hardening Checklist

1. **Enable RLS** on every `public` table (lint 0013).
2. **Create at least one policy per command per table** (lint 0008; avoid `FOR ALL`).
3. **Wrap `auth.uid()` / `auth.jwt()` in `(select ...)`** in policies (lint 0003).
4. **Set `search_path = ''`** on every SECURITY DEFINER function (lint 0011).
5. **Never reference `raw_user_meta_data`** in policies (lint 0015) — use `raw_app_meta_data` or JWT claims via Auth Hook.
6. **Run `get_advisors` (security)** after schema changes.
7. **Use publishable / secret keys** (`sb_publishable_*` / `sb_secret_*`) on new projects; secret/service-role keys server-side only.
8. **Enable email confirmation** in production auth settings.
9. **Set restrictive CORS** on edge functions (caught by `audit-edge-functions.py`).
10. **Validate inputs** in edge functions before database operations.
11. **Use parameterized queries** — never concatenate user input into SQL.
12. **Review SECURITY DEFINER views** — Splinter 0010 (`security_definer_view`) flags them.
13. **Enable MFA** on the Supabase Dashboard account (TOTP, Phone, or WebAuthn).

## Disabling RLS (When Appropriate)

Some tables may legitimately not need restrictive RLS:
- Lookup/reference tables with public data
- Tables only accessed via `security definer` functions
- Internal tables in non-public schemas

Always **enable RLS and grant permissive read** rather than leaving RLS off:
```sql
alter table public.countries enable row level security;
create policy "Public read" on public.countries for select using (true);
```

This satisfies lint 0013 (RLS enabled) and makes intent explicit. Splinter still surfaces 0008 for the table if it has no policies — adding even a `using (true)` policy resolves it.

## Searching Security Docs (MCP)

For the latest security documentation:
```
mcp__supabase__search_docs(query: "RLS policies security <specific topic>")
```
