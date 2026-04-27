# rad-supabase scripts

Three deterministic Python validators (pure stdlib, 3.8+) backing the plugin's security and current-state claims. Each takes optional paths, supports `--json` for machine-readable output, and uses standard exit codes:

| Exit | Meaning |
|------|---------|
| 0 | No findings |
| 1 | Warnings only |
| 2 | Critical findings present |

These are static checks. They cannot replace `supabase db lint` or running `mcp__supabase__get_advisors` against a live project — those see runtime state. Static checks complement them by running fast, in CI, and without a live database.

---

## audit-rls.py

Parses `supabase/migrations/*.sql` and flags violations of Supabase's [Splinter](https://supabase.github.io/splinter/) lint catalog that are statically detectable, plus a few structural checks.

**Lints covered:**

| Code | Splinter ref | What it catches |
|------|-------------|-----------------|
| 0002 | auth_users_exposed | `create view` in non-internal schema selecting from `auth.users` |
| 0003 | auth_rls_initplan | Bare `auth.uid()` / `auth.jwt()` / `auth.role()` in policy expressions (recommend `(select auth.<fn>())`) |
| 0008 | rls_enabled_no_policy | Table with `enable row level security` but no `create policy` in any scanned migration |
| 0011 | function_search_path_mutable | `SECURITY DEFINER` function without `set search_path = ...` |
| 0013 | rls_disabled_in_public | `create table public.<x>` without a matching `enable row level security` |
| 0015 | rls_references_user_metadata | Policy referencing `raw_user_meta_data` (user-writable, never trustworthy) |
| STRUCT-using-true-no-check | — | INSERT/UPDATE/ALL policy with `using (true)` and no `with check` |
| STRUCT-for-all | — | Policy uses `FOR ALL` (recommend separate per-command policies) |

**What it cannot catch:**
- Policies created via Dashboard SQL editor (no migration trace).
- Tables created via `apply_migration` MCP without a corresponding file.
- `0001 unindexed_foreign_keys`, `0006 multiple_permissive_policies`, `0017 foreign_table_in_api`, `0019 insecure_queue_exposed_in_api` — runtime state required. Use `mcp__supabase__get_advisors`.

**Usage:**
```bash
python audit-rls.py                                  # scans ./supabase/migrations
python audit-rls.py --migrations-dir db/migrations
python audit-rls.py path/to/some/migration.sql
python audit-rls.py --json | jq .
```

---

## check-secret-leaks.py

Walks the project tree looking for secret-key leaks and committed env files.

**What it catches:**
- `SUPABASE_SERVICE_ROLE_KEY` / `SUPABASE_SECRET_KEY` referenced from client-side paths (heuristics: `app/`, `pages/`, `src/components/`, `src/pages/`, `src/app/`, `public/`, `routes/`, `static/`, `*.client.ts`, `+page.svelte`). Bypasses RLS — a critical security failure.
- Literal `sb_secret_*` keys in any source file (rotate immediately).
- JWT-shaped literals (`eyJ...`) — likely leaked anon or service_role legacy keys.
- Stripe `sk_live_*` / `sk_test_*` literals.
- `.env` / `.env.local` / `.env.production` etc. present in the project tree (likely committed). `.env.example` / `.env.sample` / `.env.template` are exempt.
- `SUPABASE_ANON_KEY` references in `.env.example` — info-level prompt to migrate to `SUPABASE_PUBLISHABLE_KEY`.

**Heuristics, not proofs.** Path classification is conservative — `unknown` paths get the benefit of the doubt for service-role var references but JWT-shaped literals are flagged as critical regardless. Review findings; don't auto-fix.

**What it cannot catch:**
- Secrets passed through CI variables and never written to disk.
- Secrets transformed/encoded before being stored.
- Misuse where a service role client is constructed in a server file but its responses leak through to the browser.

**Usage:**
```bash
python check-secret-leaks.py                # scans current directory
python check-secret-leaks.py src/ supabase/ # specific subtrees
python check-secret-leaks.py --json
```

Files larger than 2 MB and binary asset extensions (images, fonts, archives, lockfiles) are skipped.

---

## audit-edge-functions.py

Static audit of `supabase/functions/<name>/*.ts` plus `supabase/config.toml`.

**What it catches:**
- Deprecated import: `import { serve } from "https://deno.land/std@*/http/server.ts"`. Use `Deno.serve(...)` (built-in in Deno 2.x).
- CORS wildcard: `'Access-Control-Allow-Origin': '*'` in response headers.
- Hardcoded API keys: `sb_secret_*`, JWT literals, `sk_live_*`, `sk_test_*`.
- Stripe import older than v22 (`import Stripe from "npm:stripe@<N>"` where N < 22). v22 introduced a real ES6 class — `new Stripe(...)` is now required.
- `[functions.<name>] verify_jwt = false` in `config.toml` without a `#` comment explaining why.

**What it cannot catch:**
- Auth header forwarding bugs that bypass JWT verification semantically.
- Functions that import secrets via custom SDK wrappers.
- Logic errors inside the function body.

**Usage:**
```bash
python audit-edge-functions.py                              # scans ./supabase/functions
python audit-edge-functions.py --functions-dir functions/   # custom dir
python audit-edge-functions.py supabase/functions/my-fn/    # single function
python audit-edge-functions.py --json
```

---

## CI integration

```yaml
- name: Static Supabase audits
  run: |
    python plugins/rad-supabase/scripts/audit-rls.py --json > rls.json
    python plugins/rad-supabase/scripts/check-secret-leaks.py --json > leaks.json
    python plugins/rad-supabase/scripts/audit-edge-functions.py --json > edge.json
```

Exit code 2 fails the build. Use `|| true` to soften.

## Pinned facts (verified April 2026)

These scripts encode the following pinned facts:

- Splinter lint codes: 0002, 0003, 0008, 0011, 0013, 0015 (full catalog at https://supabase.github.io/splinter/).
- Stripe Node SDK current major: **22** (v22.0.2, March 2026; ES6-class breaking change).
- Edge Runtime: Deno **2.1.4**; `Deno.serve` is the built-in pattern.
- API key formats: `sb_publishable_*` (client-safe) and `sb_secret_*` (server-only) replace legacy `anon`/`service_role`.

If any of these change, update the constants at the top of the relevant script.
