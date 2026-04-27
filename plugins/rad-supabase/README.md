# rad-supabase — Supabase development for Claude Code

Pinned to **Supabase CLI v2.95+**, **Supabase MCP server v0.7+ (31 tools)**, **Edge Runtime Deno 2.1.4**, **Stripe SDK v22**. Verified April 2026.

## Read this first — what this plugin does and doesn't do

**What it does**
- Teaches Claude when to use the Supabase CLI (local development) vs the Supabase MCP server (remote operations) and surfaces the 31 MCP tools verbatim.
- Encodes current security guidance: `(select auth.uid())` initPlan-cached policies, separate-policy-per-command pattern, Custom Access Token Hook for RBAC, the `sb_publishable_*` / `sb_secret_*` API key model, Realtime Authorization, Branching 2.0.
- Ships three deterministic Python validators that statically catch the Splinter lints `audit-rls.py` can detect without a live database, plus secret-key leaks and Edge Function anti-patterns.

**What it does not do**
- It does not replace `supabase db lint` or `mcp__supabase__get_advisors` — those see runtime state. The static validators complement them.
- It does not crawl your live Supabase project. Every check that needs the dashboard or a live database is delegated to the appropriate MCP tool.
- It does not auto-fix anything. All scripts are read-only and emit findings; you decide what to change.
- It does not cover Supabase-as-IdP (OAuth 2.1 server), Iceberg ETL / Vector Buckets / Analytics Buckets, or AWS Marketplace billing — those are too new or too niche to be the plugin's primary focus.

## Skills

| Skill | Triggers | Coverage |
|-------|----------|----------|
| **supabase-best-practices** | "set up Supabase", "supabase init", "local development", "config.toml" | Project structure, local dev workflow, CLI vs MCP decision guide, full `config.toml` section list, conventions |
| **supabase-projects** | "create project", "list projects", "API keys", "publishable key", "secret key" | Project + org management, asymmetric JWT signing keys (default for new projects since May 1, 2025), `sb_publishable_*` / `sb_secret_*` migration, regions, pause/restore, cost confirmation |
| **supabase-database** | "execute SQL", "list tables", "generate types", "extensions" | SQL execution, schema inspection, common extensions, TypeScript type generation, push/pull, schema design patterns |
| **supabase-migrations** | "create migration", "apply migration", "drift" | Migration creation, application, naming, drift detection/repair, squashing, `db diff` |
| **supabase-edge-functions** | "deploy function", "Deno", "serverless", "scheduled function" | Function development on Deno 2.1.4, deployment via MCP/CLI, Stripe v22 (`new Stripe()` constructor), Supabase Cron (first-class) + raw `pg_cron`+`pg_net`, secrets, logs |
| **supabase-auth** | "auth", "sign up", "OAuth", "MFA", "anonymous", "JWT" | Auth providers, anonymous sign-in (`signInAnonymously`), MFA factors (TOTP/Phone/WebAuthn), asymmetric JWTs, Custom Access Token Hook for RBAC, Auth Hooks list |
| **supabase-branching** | "database branch", "preview environment", "merge branch" | Branching 2.0 (Preview vs Persistent branches), lifecycle, GitHub PR integration, cost model (compute hours + egress), CI/CD patterns |
| **supabase-security** | "RLS", "policy", "service role", "secret key" | RLS with `(select auth.uid())` wrapping, per-command policies, inverted team-access pattern, Custom Access Token Hook RBAC, full Splinter lint inventory, secrets management |
| **supabase-storage** | "storage bucket", "S3", "file upload", "image transformation" | Bucket management, three protocols (REST / TUS / S3-compatible — all GA), storage RLS policies, image transformations (Pro+, billed per 1000 origin images), Smart CDN |
| **supabase-realtime** | "subscribe to table", "broadcast", "presence", "realtime authorization" | Postgres Changes (legacy path) vs Broadcast-from-Database (recommended for scale) vs Presence; Realtime Authorization (RLS on `realtime.messages`) |
| **supabase-troubleshooting** | "logs", "advisors", "diagnose" | Log viewing per service, Splinter lint codes, doc search, CLI inspection, common error patterns |

## Agent

| Agent | Triggers | Behavior |
|-------|----------|----------|
| **supabase-reviewer** | "review my Supabase setup", "production ready?", "audit RLS" | Runs the 3 validators in Step 0, then layers schema/auth/storage/realtime checks. Defaults to Opus 4.7 with JSON output mode. |

## Validators (static, pure stdlib Python 3.8+)

| Script | What it parses | What it catches |
|--------|---------------|-----------------|
| **`scripts/audit-rls.py`** | `supabase/migrations/*.sql` | Splinter 0002/0003/0008/0011/0013/0015 + structural checks (`using (true)` without `with check`, `FOR ALL` policies) |
| **`scripts/check-secret-leaks.py`** | Project tree | `SUPABASE_SERVICE_ROLE_KEY` / `sb_secret_*` in client paths; literal JWTs / `sk_live_` / `sk_test_`; committed `.env` files |
| **`scripts/audit-edge-functions.py`** | `supabase/functions/**/*.ts` + `config.toml` | Deprecated `serve` import, CORS wildcard, hardcoded keys, Stripe < v22, undocumented `verify_jwt = false` |

All exit 0 (clean) / 1 (warnings only) / 2 (critical). All accept `--json` for machine-readable output. Full docs at `scripts/README.md`.

## MCP tools covered (31 — verified against `@supabase/mcp-server-supabase` v0.7.0, March 2026)

| Category | MCP Tools |
|----------|-----------|
| **Account** (9) | `list_projects`, `get_project`, `create_project`, `pause_project`, `restore_project`, `list_organizations`, `get_organization`, `get_cost`, `confirm_cost` |
| **Knowledge Base** (1) | `search_docs` |
| **Database** (5) | `list_tables`, `list_extensions`, `list_migrations`, `apply_migration`, `execute_sql` |
| **Debugging** (2) | `get_logs`, `get_advisors` |
| **Development** (3) | `get_project_url`, `get_publishable_keys`, `generate_typescript_types` |
| **Edge Functions** (3) | `list_edge_functions`, `get_edge_function`, `deploy_edge_function` |
| **Branching** (6) | `create_branch`, `list_branches`, `delete_branch`, `merge_branch`, `reset_branch`, `rebase_branch` |
| **Storage** (3) | `list_storage_buckets`, `get_storage_config`, `update_storage_config` |

Notes:
- The Storage tool group is **off by default** — enable with `--features=...,storage` when starting the MCP server.
- `get_anon_key` was removed in v0.5.9 (Oct 2025) and replaced by `get_publishable_keys`.
- `--read-only` mode disables all mutating tools (recommended for safety; you can re-enable selectively per session).
- `--project-ref <id>` scopes the server to one project and disables account-level tools.
- Authentication: hosted (`mcp.supabase.com/mcp`) uses OAuth 2.1; self-hosted uses a Personal Access Token via `SUPABASE_ACCESS_TOKEN`.

## CLI commands covered (Supabase CLI v2.95+)

| Category | CLI Commands |
|----------|-------------|
| **Setup** | `init`, `start`, `stop`, `status`, `login`, `link` |
| **Database** | `db push`, `db pull`, `db reset`, `db lint`, `db diff` |
| **Migrations** | `migration new`, `migration list`, `migration repair`, `migration squash` |
| **Functions** | `functions new`, `functions serve`, `functions deploy`, `functions download`, `functions delete`, `functions list` |
| **Secrets** | `secrets set`, `secrets list`, `secrets unset` |
| **Types** | `gen types typescript` |
| **Inspection** | `inspect db {calls,long-running,outliers,bloat,cache-hit,index-usage,locks,replication-slots,role-connections,seq-scans,table-sizes,unused-indexes,vacuum-stats}` |
| **Branches** | `branches create`, `branches list`, `branches update`, `branches delete` |

## Critical 2025-2026 platform changes this plugin reflects

1. **New API keys** — `sb_publishable_*` (client-safe) and `sb_secret_*` (server-only) replace legacy `anon` / `service_role`. Projects restored after **Nov 1, 2025** no longer get legacy keys.
2. **Asymmetric JWT signing** (ES256/RS256) is the default for new projects since **May 1, 2025**. Verify via JWKS instead of shared HS256 secret.
3. **Branching 2.0** distinguishes Preview branches (ephemeral, auto-paused/deleted on PR close) from Persistent branches (long-lived staging/QA).
4. **Realtime Authorization** ships RLS-on-`realtime.messages` for Broadcast and Presence. Recommendation pivoted toward Broadcast-from-Database for scale.
5. **Storage S3-compatible API** is GA — three interoperable upload protocols (REST, TUS, S3) operate on the same objects.
6. **Anonymous sign-in** (`signInAnonymously()`) is GA. JWT carries `is_anonymous` claim usable in RLS.
7. **Edge Runtime** is on Deno 2.1.4. `Deno.serve` is the built-in pattern; `import { serve } from deno.land/std/...` is deprecated.
8. **Supabase Cron** ships a first-class scheduled-functions UI (built on `pg_cron` + `pg_net` underneath; sub-minute schedules supported).
9. **MCP Storage tools** added (`list_storage_buckets`, `get_storage_config`, `update_storage_config`) — off by default.

## Installation

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-supabase
```

### Prerequisites

- **Supabase CLI** v2.95+ installed (`supabase --version`).
- **Supabase MCP server** connected in Claude Code (hosted or self-hosted).
- A Supabase project (hosted) for any MCP tool that requires `project_id`.
- **Python 3.8+** to run the validators (most systems already have this).

## Important caveats

- **CLI vs MCP**: CLI for local development and CI/CD; MCP for remote operations and interactive Claude Code sessions.
- **Cost confirmation is enforced**: `create_project` and `create_branch` require `get_cost` → `confirm_cost` → pass `confirm_cost_id` into the create call. Don't skip.
- **RLS on every public table**: enforced by `audit-rls.py` and surfaced by `mcp__supabase__get_advisors`.
- **Service role / secret keys never reach the browser**: `check-secret-leaks.py` flags this.
- **`raw_user_meta_data` is user-writable** — never use it in RLS. Use `raw_app_meta_data` or a JWT custom claim from the Custom Access Token Hook.

## Version compatibility

| Plugin Version | Supabase CLI | Supabase MCP | Edge Runtime | Stripe SDK |
|---------------|-------------|-------------|-------------|-----------|
| 2.0.0 | v2.95+ | v0.7+ (31 tools) | Deno 2.1.4 | v22+ (`new Stripe()`) |
| 1.0.0 | v1.x+ | "Official" (28 tools claim, actually 29) | unspecified | v17 |

If you're on the 1.0.0 mental model, the priority migration path is:
1. Switch keys to `sb_publishable_*` / `sb_secret_*`.
2. Wrap RLS `auth.uid()` calls in `(select auth.uid())`.
3. Upgrade Stripe imports to `npm:stripe@22` (use the new `new Stripe()` constructor).
4. Replace `import { serve } from "https://deno.land/std@*/http/server.ts"` with `Deno.serve(...)`.
