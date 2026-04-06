# rad-coolify-orchestrator

End-to-end Coolify self-hosted PaaS management for Claude Code. Covers deployments, databases, security, CI/CD, troubleshooting, observability, and multi-server infrastructure.

**Target**: Coolify v4.x self-hosted (not Coolify Cloud)

## Skills

| Skill | Triggers | What It Covers |
|-------|----------|----------------|
| **coolify-deploy** | "deploy to Coolify", "which build pack", "Nixpacks vs Dockerfile" | Build pack selection (Nixpacks/Dockerfile/Compose/Image/Static), deployment config, zero-downtime deploys, rollbacks, registry patterns, monorepo support |
| **coolify-databases** | "Coolify database", "database backup", "restore database" | PostgreSQL/MySQL/MariaDB/MongoDB/Redis provisioning, S3 backups, restore procedures, SSL, credential rotation, resource limits |
| **coolify-security** | "Coolify secrets", "Coolify RBAC", "secure Coolify" | Secrets management (env vars vs build secrets), RBAC roles, network isolation, UFW+Docker conflict, resource limits, terminal access |
| **coolify-cicd** | "Coolify API", "GitHub Actions deploy", "Coolify webhook" | REST API reference, GitHub Actions workflows, GHCR pattern, GitLab CI, webhooks, PR preview environments |
| **coolify-troubleshoot** | "Coolify 502", "build failed", "SSL certificate" | 502/504 diagnosis, container restart loops, OOM kills, Nixpacks errors, SSL/Let's Encrypt issues, Coolify self-repair |
| **coolify-observability** | "Coolify monitoring", "Coolify Sentinel", "log drain" | Sentinel metrics, notification channels (Slack/Discord/Telegram/email), log drains (Axiom/New Relic/Loki), Uptime Kuma, Grafana+Prometheus |
| **coolify-infrastructure** | "Coolify multi-server", "Docker Swarm", "Coolify backup" | Multi-server deployment, Docker Swarm (experimental), build servers, Coolify instance backup/migration, load balancing |

## Agent

| Agent | Triggers | What It Does |
|-------|----------|-------------|
| **coolify-reviewer** | "review my Coolify config", "is my Dockerfile ready for Coolify" | Autonomous review of Dockerfiles, compose files, CI/CD pipelines, env vars, and security for Coolify deployment readiness |

## Installation

### From the rad-skills-repo marketplace

```bash
# Add to your project
claude mcp add-plugin rad-coolify-orchestrator --source ./plugins/rad-coolify-orchestrator
```

### Direct installation

```bash
claude --plugin-dir /path/to/rad-coolify-orchestrator
```

## Prerequisites

- Coolify v4.x self-hosted instance
- Basic Docker knowledge
- SSH access to Coolify server(s)

## Skill Details

### coolify-deploy

Decision tree for choosing between Nixpacks, Dockerfile, Docker Compose, pre-built image, and static build packs. Includes NIXPACKS_* override reference, monorepo patterns, and Railpack (experimental) guidance.

**References**: `build-packs.md` (detection rules, Dockerfile best practices), `registry-patterns.md` (GHCR/DockerHub/private registry workflows)

### coolify-databases

One-click database provisioning for PostgreSQL, MySQL, MariaDB, MongoDB, Redis, KeyDB, Dragonfly, and ClickHouse. S3-compatible backup configuration, restore procedures per engine, and connection patterns.

**References**: `backup-restore.md` (per-engine backup/restore commands), `connection-patterns.md` (connection strings, pooling, SSL, resource tuning)

### coolify-security

Three-tier secrets model (runtime env vars, build-time env vars, Docker Build Secrets) with decision tree. RBAC roles (Admin/Developer/Viewer), UFW+Docker conflict resolution, and hardening checklist.

**References**: `hardening-checklist.md` (server + Coolify hardening steps), `ufw-docker-guide.md` (ufw-docker utility setup)

### coolify-cicd

Full REST API v1 reference with deploy triggers, status polling, and env var management. GitHub Actions and GitLab CI workflow templates. GHCR build-push-deploy pipeline.

**References**: `api-reference.md` (all API endpoints), `gitlab-ci-pattern.md` (GitLab CI integration)

### coolify-troubleshoot

Diagnostic decision trees for 502, 504, SSL errors, container crashes, and build failures. Exit code reference, OOM kill confirmation, and Coolify self-repair procedures.

**References**: `traefik-debugging.md` (Traefik v3 routing diagnosis), `common-errors.md` (50+ error patterns with fixes)

### coolify-observability

Sentinel monitoring overview, notification channel setup (Slack, Discord, Telegram, email, webhook), log drain configuration (Axiom, New Relic, custom HTTP), and Uptime Kuma integration.

**References**: `log-drain-configs.md` (per-destination configuration), `grafana-prometheus-setup.md` (full monitoring stack)

### coolify-infrastructure

Multi-server deployment with Docker Registry requirement, Docker Swarm (experimental) setup and limitations, build server configuration, and Coolify instance backup/migration.

**References**: `multi-server-setup.md` (step-by-step guide), `swarm-guide.md` (Swarm initialization and feature matrix)

## Important Caveats

- **Coolify Cloud vs Self-Hosted**: All content assumes self-hosted Coolify v4.x. Coolify Cloud behavior may differ.
- **Railpack**: Marked as experimental. Not recommended for production.
- **Docker Swarm**: Marked as experimental in Coolify. Use with caution.
- **API Endpoints**: Verified against Coolify v4 API. Endpoints may change between releases.
- **UFW+Docker**: The known conflict requires `ufw-docker` utility — standard UFW rules do NOT protect Docker-published ports.

## Version Compatibility

| Coolify Version | Plugin Version | Status |
|----------------|---------------|--------|
| v4.x | 1.0.0 | Current |
| v3.x | Not supported | v3→v4 migration is a manual process |

## Contributing

Found an inaccuracy or missing coverage? Check the [CHANGELOG](CHANGELOG.md) for what's documented and file an issue or PR.

## License

Apache-2.0
