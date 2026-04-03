# rad-docker

Production-grade Docker guidance for Claude Code. Provides comprehensive best practices for building, optimizing, and hardening Node.js and Next.js container images.

## What This Plugin Does

- **Auto-triggers** when you work on any Dockerfile, docker-compose.yml, or .dockerignore
- **Reviews** Dockerfiles for anti-patterns, security issues, and production gaps
- **Scaffolds** production-ready Dockerfiles for Node.js, Next.js, and NestJS projects

## Skills

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `docker` | Auto | Core knowledge: multi-stage builds, security, optimization |
| `docker-review` | `/rad-docker:docker-review` | Audit a Dockerfile for issues |
| `docker-scaffold` | `/rad-docker:docker-scaffold [type]` | Generate a production Dockerfile |

## Agents

| Agent | Trigger | Purpose |
|-------|---------|---------|
| `docker-reviewer` | Proactive / on request | Autonomous Dockerfile quality review |

## Core Principles

1. **Build fat, ship thin** — multi-stage builds separate compilation from runtime
2. **Least privilege** — non-root user, minimal base images, no extra packages
3. **Twelve-Factor** — config via env vars, same image across all environments
4. **Deterministic** — pinned images, `npm ci`, lockfiles, no `:latest`

## Examples

- `skills/docker/examples/nodejs-express.Dockerfile` — Express API multi-stage build
- `skills/docker/examples/nextjs-standalone.Dockerfile` — Next.js standalone output
- `skills/docker/examples/.dockerignore-nodejs` — complete Node.js .dockerignore
- `skills/docker/examples/docker-compose-healthcheck.yml` — Compose with health conditions
