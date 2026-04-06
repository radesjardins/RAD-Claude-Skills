# rad-coolify-orchestrator — Deploy, manage, and troubleshoot self-hosted apps on Coolify — from Claude Code.

Coolify is a self-hosted Heroku/Netlify alternative, and it has its own patterns for Dockerfiles, environment variables, Traefik routing, and zero-downtime deployments. rad-coolify-orchestrator teaches Claude those patterns so you're not guessing at configuration or debugging 502s without a clear mental model of what Traefik is doing.

## What You Can Do With This

- Deploy an application to Coolify with the right build pack and health check configuration
- Diagnose 502/504 errors, failed deployments, and Traefik routing issues with a structured approach
- Set up environment variables and secrets without exposing them in Dockerfiles or build logs
- Configure CI/CD pipelines that trigger Coolify deployments from GitHub Actions

## How It Works

| Skill | Purpose |
|-------|---------|
| `coolify-deploy` | Build packs, Dockerfile patterns, Docker Compose, deployment configuration |
| `coolify-databases` | Database provisioning, backups, restore, connection strings |
| `coolify-security` | Secrets management, environment variables, Docker BuildKit secrets |
| `coolify-cicd` | GitHub Actions integration, webhook triggers, Coolify REST API |
| `coolify-infrastructure` | Multi-server, Docker Swarm, server configuration |
| `coolify-observability` | Sentinel monitoring, notification channels, log configuration |
| `coolify-troubleshoot` | 502/504 diagnosis, Traefik routing, container failures, deployment errors |
| `coolify-actions` | MCP-based operational actions against a live Coolify instance |

| Agent | Purpose |
|-------|---------|
| `coolify-reviewer` | Reviews Coolify configs, Dockerfiles, and environment setups for anti-patterns and security issues |

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-coolify-orchestrator
```

```
Review my Coolify deployment config
Why is my deployment failing?
Set up CI/CD for Coolify
Is my Dockerfile ready for Coolify?
```

## License
Apache-2.0
