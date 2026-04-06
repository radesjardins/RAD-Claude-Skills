# Extended Workflow Recipes

## Recipe: Full Deployment Pipeline with Verification

Complete deploy-and-verify sequence for production:

```
1. coolify_healthcheck                              → verify API is reachable
2. coolify_get_application(uuid)                    → snapshot current state (save current image tag for rollback)
3. coolify_deploy(uuid, force: false)               → trigger deploy, capture deployment_uuid
4. Wait 15 seconds
5. coolify_get_deployment(deployment_uuid)           → check status
   - If "in_progress" → wait 15 more seconds, repeat step 5 (max 20 attempts)
   - If "finished" → continue to step 6
   - If "failed" → report failure, get logs from deployment response
6. coolify_get_application_logs(uuid, lines: 20)    → verify app is healthy post-deploy
7. Report: deploy succeeded, show app URL
```

## Recipe: Bulk Status Check (All Resources)

Morning check or incident triage — get a complete picture:

```
1. coolify_list_servers                     → check all servers reachable
2. coolify_list_all_resources               → get every resource with status
3. Filter for any resource NOT in "running" state
4. For each non-running resource:
   - coolify_get_application(uuid) or coolify_get_database(uuid)  → check config/logs
5. Report: summary table of all resources, flag anything down
```

## Recipe: Environment Variable Bulk Update

Update a shared secret across multiple apps:

```
1. coolify_list_applications                → get all apps
2. Filter for apps that need the updated variable
3. For each app:
   a. coolify_list_env_vars(uuid)           → check if var exists
   b. coolify_create_env_var(uuid, key, value)  → create/update
4. For each updated app:
   a. coolify_restart_application(uuid)     → apply changes
5. Verify each app is running after restart
```

**Caution**: Confirm with the user before restarting multiple apps — this may cause brief downtime across services.

## Recipe: Deploy by Tag (Microservices Fleet)

Deploy all services tagged "backend" simultaneously:

```
1. coolify_deploy(tag: "backend")           → triggers deploy for ALL resources with tag
2. Response contains multiple deployment_uuids
3. For each deployment_uuid:
   a. Poll coolify_get_deployment(uuid) until terminal status
4. Report: which succeeded, which failed
```

Tags are configured in the Coolify UI on each resource. Common patterns:
- `backend` — all API services
- `frontend` — all web apps
- `staging` — all staging resources
- `v2.0` — specific release version

## Recipe: Pre-Deploy Safety Check

Before deploying to production, verify the environment is healthy:

```
1. coolify_get_server(uuid)                         → server reachable?
2. coolify_get_application(uuid)                    → app currently running?
3. coolify_list_deployments(uuid, take: 3)          → are recent deploys succeeding?
4. coolify_get_application_logs(uuid, lines: 50)    → any errors in current logs?
5. If all checks pass → proceed with coolify_deploy
   If any check fails → report the issue before deploying
```

## Recipe: Database Health Check

Verify databases are running and accessible:

```
1. coolify_list_databases                           → all databases with status
2. For each database:
   a. coolify_get_database(uuid)                    → check config, version, resource limits
3. Flag any database that:
   - Has no memory limit set (OOM risk)
   - Is publicly accessible (security risk)
   - Shows as stopped or restarting
4. Report findings with remediation suggestions
```

## Recipe: Incident Response — App Down

When a user reports their app is down:

```
1. coolify_list_applications                        → find the app, check status
2. coolify_get_application(uuid)                    → get full config
3. coolify_get_application_logs(uuid, lines: 200)   → check for errors/crashes
4. coolify_list_deployments(uuid, take: 5)          → was there a recent bad deploy?

If container is crashed/stopped:
   5a. coolify_restart_application(uuid)            → attempt restart
   5b. coolify_get_application_logs(uuid, lines: 50) → verify it came back

If recent deploy caused the issue:
   5a. Identify last successful deployment
   5b. Follow Workflow 9 (Rollback) from the main skill

If app is running but returning errors:
   5a. Check port configuration in app details
   5b. Check domain/SSL configuration
   5c. Advise checking proxy logs via SSH: docker logs coolify-proxy --tail 100
```

## Recipe: New Project Setup Verification

After setting up a new project in Coolify, verify everything is configured:

```
1. coolify_list_projects                            → find the project
2. coolify_get_project(uuid)                        → check environments
3. coolify_list_applications                        → find apps in the project
4. For each app:
   a. coolify_get_application(uuid)                 → check config
   b. Verify: port set, domain configured, health check path set
   c. coolify_list_env_vars(uuid)                   → check required env vars present
5. coolify_list_databases                           → find databases in the project
6. For each database:
   a. coolify_get_database(uuid)                    → check config
   b. Verify: resource limits set, backup configured
7. Report: checklist of what's configured vs what's missing
```

## Polling Best Practices

When waiting for deployment completion:

- **Initial wait**: 10-15 seconds after triggering deploy (builds take time to start)
- **Poll interval**: 15 seconds between status checks
- **Max attempts**: 20 (5 minutes total) for standard deploys
- **Extended timeout**: 40 attempts (10 minutes) for large builds or first-time deploys
- **Status values**: `queued` → `in_progress` → `finished` | `failed` | `cancelled`
- **Never poll faster than 10 seconds** — Coolify's database handles many other operations
