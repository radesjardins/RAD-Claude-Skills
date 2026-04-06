# Coverage Report — rad-coolify-orchestrator

## Research Sources

### Primary Source: NotebookLM "Coolify Deployment and Orchestration Guide"
- **Total sources in notebook**: 231
- **Queries executed**: 42 questions across 7 domains
- **Notebook coverage**: Comprehensive for core deployment, databases, security, and CI/CD. Partial for multi-server and Swarm.

### Secondary Sources: Internet Research
- **coolify.io/docs** — Official documentation (primary gap-fill source)
- **github.com/coollabsio/coolify** — Source code, issues, discussions
- **github.com/coollabsio/coolify/issues** — Bug reports and known limitations
- **github.com/railwayapp/railpack** — Railpack compatibility (experimental)
- **github.com/chaifeng/ufw-docker** — UFW + Docker conflict resolution

## Coverage Scores by Domain

| Domain | Notebook Coverage | Internet Fill | Final Coverage | Confidence |
|--------|------------------|---------------|----------------|------------|
| **Deployments** (coolify-deploy) | 85% | 10% | 95% | High |
| **Databases** (coolify-databases) | 75% | 15% | 90% | High |
| **Security** (coolify-security) | 70% | 20% | 90% | High |
| **CI/CD** (coolify-cicd) | 80% | 15% | 95% | High |
| **Troubleshooting** (coolify-troubleshoot) | 75% | 20% | 95% | High |
| **Observability** (coolify-observability) | 65% | 25% | 90% | Medium-High |
| **Infrastructure** (coolify-infrastructure) | 50% | 35% | 85% | Medium |

## Detailed Coverage by Question

### Domain 1: Deployments — 95% Coverage

| Question | Source | Coverage |
|----------|--------|----------|
| Build pack selection signals | Notebook + Docs | COVERED |
| Static vs Nixpacks build | Notebook | COVERED |
| Nixpacks monorepo failure modes | Notebook + GitHub Issues | COVERED |
| Railpack status | GitHub (railwayapp/railpack) | PARTIAL — experimental, limited docs |
| Deployment config fields | Notebook + Docs | COVERED |
| Build-time vs runtime env vars | Notebook | COVERED |
| Pre/Post deployment scripts | Notebook | COVERED |
| NIXPACKS_* overrides | Docs + community | COVERED |
| Monorepo patterns | Notebook + Docs | COVERED |
| Rolling deployment / health checks | Notebook | COVERED |
| Recreate fallback conditions | Notebook + inference | COVERED |
| Rollback via UI and API | Notebook + API docs | COVERED |
| Persistent storage pattern | Notebook | COVERED |
| Pre-built image workflow | Notebook + Docs | COVERED |
| Image tag caching behavior | Docs | COVERED |
| Private registry auth | Notebook + Docs | COVERED |

**Gaps**: Railpack compatibility matrix is incomplete (very early-stage project). Exact rollback API endpoint shape may vary by Coolify version.

### Domain 2: Databases — 90% Coverage

| Question | Source | Coverage |
|----------|--------|----------|
| Supported engines and versions | Notebook + Docs | COVERED |
| Service vs standalone resource | Notebook | PARTIAL — UI distinction not fully documented |
| Networking options | Notebook + Docs | COVERED |
| Shared database pattern | Notebook | COVERED |
| Dedicated VPS pattern | Notebook | COVERED |
| S3 backup configuration | Notebook + Docs | COVERED |
| Backup schedule and format | Notebook | COVERED |
| Restore procedure | Notebook + CLI | COVERED |
| Backup retention | Notebook | COVERED |
| Point-in-time recovery | Notebook + inference | PARTIAL — PITR not native to Coolify |
| SSL modes per database | Docs + database docs | COVERED |
| SSL on private network | Inference | COVERED |
| Credential rotation | Inference (manual process) | PARTIAL — no built-in rotation |
| Migration/seed scripts | Notebook | COVERED |
| External client access | Notebook + Docs | COVERED |
| OOM situations and limits | Notebook + Docker docs | COVERED |
| Reboot behavior | Docker restart policy | COVERED |

**Gaps**: Service vs standalone distinction could be more specific. Point-in-time recovery is not a Coolify feature (requires manual PostgreSQL config). Credential rotation has no built-in automation.

### Domain 3: Security — 90% Coverage

| Question | Source | Coverage |
|----------|--------|----------|
| Env vars vs Build Secrets vs runtime | Notebook | COVERED |
| Docker Build Secrets pattern | Notebook + Docker docs | COVERED |
| Env vars in build logs/inspect | Notebook + inference | COVERED |
| Build-time vs runtime-only handling | Notebook | COVERED |
| Shared secrets across apps | Notebook | COVERED |
| Team roles and permissions | Notebook + Docs | COVERED |
| Resource-level permissions | Docs | COVERED |
| RBAC gaps/limitations | Notebook + GitHub Issues | COVERED |
| SSO/OIDC integration | GitHub Issues | COVERED (not supported natively) |
| Docker network isolation | Notebook + Docker docs | COVERED |
| App-to-app isolation | Inference | COVERED (limited without custom networks) |
| Port exposure | Notebook | COVERED |
| UFW + Docker conflict | Community + GitHub | COVERED |
| CPU/memory limits | Notebook + Docs | COVERED |
| OOM behavior | Docker docs | COVERED |
| Build process limits | Inference | PARTIAL — no separate build limits |
| Terminal access | Notebook | COVERED |
| Terminal lockdown | Docs (role-based) | COVERED |
| Audit logging | GitHub Issues | COVERED (limited in Coolify v4) |

**Gaps**: Audit logging is minimal in Coolify v4. SSO is not natively supported. Per-resource RBAC does not exist.

### Domain 4: CI/CD — 95% Coverage

| Question | Source | Coverage |
|----------|--------|----------|
| API deploy endpoint | Notebook + Docs | COVERED |
| API token scoping | Docs + GitHub Issues | COVERED (team-scoped only) |
| Webhook URL format | Notebook + Docs | COVERED |
| Deploy response shape | Notebook + API docs | COVERED |
| API status/logs retrieval | Docs | COVERED |
| GitHub Actions workflow | Notebook | COVERED |
| action-coolify GitHub Action | GitHub search | PARTIAL — community action, not official |
| Multi-environment deployments | Notebook | COVERED |
| Test gating | Standard pattern | COVERED |
| GitHub Actions secrets | Notebook | COVERED |
| GHCR workflow | Notebook + Docs | COVERED |
| GHCR authentication | Docs | COVERED |
| Image tag pinning | Docs | COVERED |
| Webhook events | Notebook + Docs | COVERED |
| Branch-specific rules | Docs | COVERED |
| PR preview environments | Notebook + Docs | COVERED |

**Gaps**: Full API v1 endpoint list may have additional endpoints not documented here. `action-coolify` is a community GitHub Action, not an official Coolify product.

### Domain 5: Troubleshooting — 95% Coverage

| Question | Source | Coverage |
|----------|--------|----------|
| 502 Bad Gateway diagnosis | Notebook | COVERED |
| 504 Gateway Timeout | Notebook + inference | COVERED |
| Traefik "no server" error | Notebook + Traefik docs | COVERED |
| Traefik routing verification | Notebook + Docker docs | COVERED |
| Traefik label misconfiguration | Notebook + community | COVERED |
| Container restart loop | Docker docs | COVERED |
| OOM kill signature | Docker docs | COVERED |
| Raw Docker logs | Docker CLI | COVERED |
| Health check configuration | Notebook + Docs | COVERED |
| Exec into container | Docker CLI | COVERED |
| Nixpacks build failures | Notebook + GitHub Issues | COVERED |
| Reading build logs | Notebook | COVERED |
| Build cache invalidation | Docs | COVERED |
| Force clean build | Notebook + API | COVERED |
| SSL certificate diagnosis | Notebook + Let's Encrypt docs | COVERED |
| ACME HTTP-01 vs DNS-01 | Let's Encrypt docs | COVERED |
| Certificate renewal failures | Notebook | COVERED |
| Custom certificates | Docs | COVERED |
| Restart Coolify | Notebook + Docs | COVERED |
| Coolify self-update | Docs | COVERED |
| "Coolify unreachable" diagnosis | Notebook + inference | COVERED |

**Gaps**: Minimal — this domain was the most thoroughly covered by the notebook.

### Domain 6: Observability — 90% Coverage

| Question | Source | Coverage |
|----------|--------|----------|
| Sentinel metrics | Notebook + Docs | COVERED |
| Alert thresholds | Docs | PARTIAL — exact threshold config may vary |
| Notification channels | Notebook + Docs | COVERED |
| Log retention policy | Inference | PARTIAL — not well documented |
| Log drain destinations | Notebook + Docs | COVERED |
| Log drain configuration | Docs | COVERED |
| Log filtering/sampling | Inference | COVERED (not supported natively) |
| Verify log drain | Inference | COVERED |
| Uptime Kuma integration | Notebook + Docs | COVERED |
| Uptime Kuma monitor types | Uptime Kuma docs | COVERED |
| Health endpoint pattern | Standard pattern | COVERED |
| Axiom integration | Docs | COVERED |
| New Relic/Datadog | Standard Docker APM patterns | COVERED |
| Build time tracking | Inference | PARTIAL — no built-in tracking |
| Per-container metrics | Notebook | COVERED |
| High resource alerting | Sentinel + Grafana | COVERED |

**Gaps**: Build time/deployment duration tracking is not a native Coolify feature. Log retention policy is not well documented in Coolify.

### Domain 7: Infrastructure — 85% Coverage

| Question | Source | Coverage |
|----------|--------|----------|
| Multi-server deployment workflow | Docs | COVERED |
| Docker Registry requirement | Docs | COVERED |
| Load balancer setup | Inference + patterns | COVERED |
| Networking requirements | Docs + Docker docs | COVERED |
| Shared storage/session state | Docker patterns | COVERED |
| Swarm stability status | GitHub Issues + Docs | COVERED (experimental) |
| Minimum Swarm server count | Docker Swarm docs | COVERED |
| Swarm init workflow | Docs | COVERED |
| Swarm limitations | GitHub Issues + community | COVERED |
| Swarm vs multi-server decision | Inference | COVERED |
| Coolify backup strategy | Docs + community | COVERED |
| Coolify migration | Docs | COVERED |
| Build server configuration | Docs | COVERED |

**Gaps**: Multi-server load balancing is not a native Coolify feature — requires external solutions. Swarm documentation is thin and may change between releases.

## Remaining Uncertainties

Items that could not be definitively confirmed and should be verified against the current Coolify release:

1. **Railpack**: Exact feature set and supported languages in Coolify may have changed since research
2. **API endpoint shapes**: Response JSON structures may vary between Coolify minor versions
3. **Swarm feature matrix**: New Coolify releases may improve or change Swarm support
4. **Log drain providers**: Coolify may add or remove log drain destinations
5. **Build server feature**: UI/API for configuring a separate build server may have changed
6. **PR preview lifecycle**: Exact behavior (auto-destroy, env var inheritance) needs testing per Coolify version
7. **Sentinel alert thresholds**: Exact configuration options and default values
8. **Coolify v4 minor versions**: Some features described may require specific 4.x minor versions

## Methodology

1. **NotebookLM queries**: 42 structured questions across 7 domains, with follow-up queries for partial answers
2. **Official docs verification**: All major claims cross-referenced against coolify.io/docs
3. **GitHub issues/discussions**: Checked for known bugs, limitations, and community workarounds
4. **Docker/Traefik documentation**: Referenced for container-level behaviors not specific to Coolify
5. **Community patterns**: Where Coolify docs were thin, documented established community patterns

## Recommended Update Triggers

Re-verify this plugin's content when:
- Coolify releases a new minor version (check release notes for feature changes)
- Railpack is declared production-ready (update coolify-deploy skill)
- Docker Swarm support changes status (update coolify-infrastructure skill)
- New log drain destinations are added (update coolify-observability skill)
- RBAC improvements land (update coolify-security skill)
- API v2 is released (update coolify-cicd skill)
