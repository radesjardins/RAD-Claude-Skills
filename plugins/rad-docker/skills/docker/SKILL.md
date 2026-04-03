---
name: docker
# This is an ambient (context-only) skill — it is injected as knowledge, not invoked as a command.
# It does not execute tools autonomously; all tool use happens in docker-review and docker-scaffold.
allowed-tools: []
description: >
  This skill should be used when working on any project that includes Docker. Trigger when:
  creating or editing a Dockerfile, writing docker-compose.yml or compose.yaml, configuring
  .dockerignore, containerizing a Node.js application, containerizing a Next.js application,
  containerizing a NestJS application, building Docker images, asking about multi-stage builds,
  Docker image optimization, Docker image size, Docker security, Docker health checks,
  Docker environment variables, Docker ports, EXPOSE directive, HEALTHCHECK instruction,
  CMD vs ENTRYPOINT, non-root Docker user, Docker secrets, distroless images, Alpine images,
  slim images, node:alpine, node:slim, node:latest (to warn against it), PID 1 problem,
  graceful shutdown in Docker, dumb-init, tini, SIGTERM handling in Node.js, .dockerignore
  best practices, Docker layer caching, cache invalidation, npm ci in Docker, Docker BuildKit
  secrets, pinning Docker base images, Docker production readiness, docker run, docker build
---

# Docker: Production Best Practices

## Core Mental Model — "Build Fat, Ship Thin"

A Docker image has two distinct phases: a **build phase** (compilation, dependency resolution, artifact generation) and a **runtime phase** (executing the application). These require fundamentally different environments, and keeping them separate is the central principle of production Docker design.

**Multi-stage builds** implement this separation. Every `FROM` statement begins a new stage. The **builder stage** is a temporary, heavy environment containing compilers, dev dependencies, and build tools. The **runtime stage** is the final image — minimal, hardened, and optimized. Only compiled artifacts are promoted via `COPY --from=builder`. The builder stage is discarded automatically and never shipped.

This mental model is reinforced by three architectural philosophies:
- **Principle of Least Privilege** — the container gets exactly what it needs to run, nothing more
- **Twelve-Factor App** — configuration is injected at runtime; the same image ships to dev, staging, and production
- **Deterministic Reproducibility** — every build produces an identical result, eliminating "works on my machine" failures

Impact of correct multi-stage builds: images shrink from >1.2 GB (single-stage) to 50–200 MB (multi-stage), with up to 60% fewer CVEs.

---

## Eight Hard Rules — Never Violate in Production

### Rule 1: Always use multi-stage builds

Single-stage builds permanently bake compilers, TypeScript, testing libraries, and dev tools into production images. Use multi-stage builds for every production application.

```dockerfile
# ─── Stage 1: Builder ─────────────────────────────────────────────────────────
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --production

# ─── Stage 2: Runtime ─────────────────────────────────────────────────────────
FROM node:22-alpine AS runtime
# ... only copy compiled artifacts from builder
```

### Rule 2: Pin base images — never use `:latest`

`:latest` resolves to a different image on every pull. Pin to specific version tags (e.g., `node:22.11-alpine3.20`) or SHA256 digests for absolute immutability. Use Docker Scout or Snyk to monitor pinned digests and auto-raise PRs when security patches drop.

```dockerfile
# CORRECT — pinned and deterministic
FROM node:22.11-alpine3.20 AS builder

# WRONG — non-deterministic, surprise breaking changes
FROM node:latest
FROM node:alpine
```

### Rule 3: Execute as a non-root user

Docker runs containers as `root` by default. A compromised process running as root has an unobstructed path to container escape and host privilege escalation. Drop to an unprivileged user before the final `CMD`.

```dockerfile
# The official node image pre-creates the 'node' user — use it
COPY --from=builder --chown=node:node /app/dist ./dist
COPY --from=builder --chown=node:node /app/node_modules ./node_modules
USER node
```

### Rule 4: Copy lockfiles before source — maximize cache hits

Docker invalidates all subsequent layer caches the moment any input changes. Lockfiles change rarely; source code changes constantly. Separate them.

```dockerfile
# CORRECT — npm ci only rebuilds when dependencies change
COPY package.json package-lock.json ./
RUN npm ci
COPY . .              # Source change here does NOT bust npm ci cache

# WRONG — source copy before install busts cache on every code change
COPY . .
RUN npm ci            # Re-runs on EVERY commit
```

### Rule 5: Use `npm ci` — never `npm install`

`npm install` can silently update versions and does not guarantee lockfile adherence. `npm ci` strictly honors `package-lock.json`, deletes and reinstalls `node_modules` from scratch, and fails if the lockfile is out of sync. Equivalent: `yarn install --frozen-lockfile`, `pnpm install --frozen-lockfile`.

### Rule 6: Use exec form for CMD/ENTRYPOINT — prevent signal swallowing

Shell form (`CMD npm start`) wraps the process in `/bin/sh -c`, which intercepts SIGTERM and never forwards it to the application. The application cannot gracefully shut down, causing forced kills and dropped requests.

```dockerfile
# CORRECT — exec (JSON array) form — process receives signals directly
CMD ["node", "dist/server.js"]
ENTRYPOINT ["dumb-init", "--"]

# WRONG — shell form swallows SIGTERM
CMD node dist/server.js
```

### Rule 7: Never bake secrets into image layers

Any `ENV`, `ARG`, `COPY`, or `RUN` that writes a secret to the filesystem permanently records it in the image history — accessible to anyone with `docker history`. Use BuildKit secret mounting.

```dockerfile
# CORRECT — secret used at build time, never written to a layer
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci

# Build with: docker build --secret id=npmrc,src=.npmrc .

# WRONG — token baked into image history forever
COPY .npmrc /root/.npmrc
RUN npm ci
RUN rm /root/.npmrc   # Too late — it's in the previous layer
```

### Rule 8: Always use `.dockerignore`

Without `.dockerignore`, `COPY . .` sends the entire project to the Docker daemon: local `node_modules` (with OS-mismatched binaries), `.git` history, `.env` credentials, and build artifacts. This bloats context, invalidates caches, and leaks sensitive files.

---

## Multi-Stage Build Pattern for Node.js (Express / NestJS)

```dockerfile
# syntax=docker/dockerfile:1
# ─── Stage 1: Builder ─────────────────────────────────────────────────────────
FROM node:22-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# Prune devDependencies before copying to runtime
RUN npm prune --production

# ─── Stage 2: Runtime ─────────────────────────────────────────────────────────
FROM node:22-alpine AS runtime

# dumb-init: lightweight init for correct PID 1 signal handling
RUN apk add --no-cache dumb-init

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

# Copy ONLY what's needed to run the application
COPY --from=builder --chown=node:node /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/dist ./dist
COPY --from=builder --chown=node:node /app/package.json ./package.json

USER node

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
  CMD wget -qO- http://localhost:3000/health || exit 1

ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
```

For Next.js standalone output, see `examples/nextjs-standalone.Dockerfile`.

---

## Base Image Selection

| Image | Approx. Size | glibc | Shell | Use When |
|-------|-------------|-------|-------|----------|
| `node:22` (full Debian) | ~1.1 GB | ✓ | ✓ | Builder stage, native module compilation |
| `node:22-slim` | ~230 MB | ✓ | ✓ | Runtime with native C++ modules (bcrypt, sharp) |
| `node:22-alpine` | ~55 MB | ✗ (musl) | ✓ | Runtime: pure JS or JS-only native modules |
| `gcr.io/distroless/nodejs22-debian12` | ~110 MB | ✓ | ✗ | Runtime: maximum security, no shell needed |

**Decision rules:**
- Default runtime choice: `node:22-alpine` — smallest footprint, strong security
- If native modules fail with Alpine (`musl` incompatibility errors for `bcrypt`, `sharp`, `canvas`, etc.): switch to `node:22-slim`
- Distroless: highest security posture — no shell means no interactive attacker sessions; use `:debug` variant for troubleshooting
- Builder stage: always use full or slim (never Distroless — `npm install` cannot run inside it)

**Edge case — Alpine and native C++ modules:**
Alpine uses `musl` libc instead of `glibc`. Many native Node.js modules (compiled C++ addons) either fail to run or exhibit performance regressions under `musl`. If your project uses `bcrypt`, `sharp`, `canvas`, `argon2`, or similar: use `node:22-slim` (Debian glibc) for the runtime stage and install `libc6-compat` on Alpine if you must stay with Alpine.

---

## .dockerignore for Node.js

```
# Host dependencies — NEVER copy; may be OS-specific binaries
node_modules
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Source control
.git
.gitignore
.gitattributes

# Local build artifacts — let Docker build them fresh
dist/
build/
.next/
out/
.nuxt/
.cache/

# Secrets and local config — NEVER bake into image
.env
.env.*
.npmrc
aws.json
*.pem
*.key
*.cert
secrets/

# Docker files themselves
Dockerfile
Dockerfile.*
.dockerignore
docker-compose*.yml

# Editor and OS artifacts
.DS_Store
Thumbs.db
*.log
.vscode/
.idea/

# Test artifacts
coverage/
.nyc_output/
__tests__/
*.test.js
*.spec.js
```

---

## Runtime Configuration

### Ports

`EXPOSE` is **documentation only** — it does not publish or open any port. Actual port binding is managed by `-p host:container` at `docker run` time, or by `ports:` in Compose. Always document the application's listening port with `EXPOSE`.

### Environment Variables

```dockerfile
# Set safe non-sensitive defaults in Dockerfile
ENV NODE_ENV=production
ENV PORT=3000

# Override at runtime without rebuilding:
# docker run -e PORT=8080 -e NODE_ENV=staging my-image
```

**What must never use ENV/ARG:**
- Database credentials, connection strings
- API keys, tokens, private keys
- `.npmrc` auth tokens during build

Inject secrets at runtime via the platform secret store (Kubernetes Secrets, AWS Secrets Manager, Docker secrets). For build-time tokens (private npm packages), use `--mount=type=secret`.

**Next.js `NEXT_PUBLIC_*` exception:** Variables prefixed `NEXT_PUBLIC_` are statically inlined into the JavaScript bundle at `next build` time — they cannot be changed at runtime without rebuilding. Use `next-runtime-env` or `export const dynamic = 'force-dynamic'` to work around this and enable true runtime injection.

### HEALTHCHECK

```dockerfile
# Minimum viable health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
  CMD wget -qO- http://localhost:3000/health || exit 1
```

| Option | Recommended | Reason |
|--------|-------------|--------|
| `--interval` | 30s | Balance between fast detection and low overhead |
| `--timeout` | 5–10s | Accommodate network latency without hanging |
| `--retries` | 3 | Prevent false positives from transient glitches |
| `--start-period` | 40s+ | Allow time for cold starts, migrations, JIT warmup |

**Common health check mistakes:**
- Using `curl` or `wget` without verifying they exist in the minimal image (Alpine and Distroless often omit them — install explicitly or use a Node.js-native check)
- Only checking that the process is running (TCP ping) rather than confirming it handles requests
- Checking external dependencies (database) in a Kubernetes liveness probe — causes restart cascade when DB goes down
- Health check operations that exceed 100ms — keep checks fast

---

## Process Management

### The PID 1 Problem

In Linux, PID 1 is the `init` process and does not receive default kernel signal behavior. Node.js was not designed to run as PID 1 — it will not respond to SIGTERM unless explicit signal handlers are registered. If Node.js is started by a shell (shell form CMD), the shell takes PID 1 and swallows signals.

**Solutions:**

1. **Use `dumb-init` or `tini`** — lightweight init processes designed for containers:
```dockerfile
RUN apk add --no-cache dumb-init   # Alpine
RUN apt-get install -y dumb-init   # Debian/slim
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
```

2. **Docker `--init` flag** — wraps the process at runtime without modifying the Dockerfile:
```bash
docker run --init my-image
```

### CMD vs ENTRYPOINT

| Instruction | Purpose | Overridable |
|-------------|---------|-------------|
| `ENTRYPOINT` | Sets the main executable (fixed) | `docker run --entrypoint` only |
| `CMD` | Default arguments to ENTRYPOINT | Any `docker run` argument |

**Standard pattern:** Use `ENTRYPOINT` for the init wrapper, `CMD` for the application command:
```dockerfile
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
# docker run my-image node dist/worker.js  ← overrides CMD only
```

### Graceful Shutdown in Node.js

Node.js must register SIGTERM/SIGINT handlers to drain active connections before exiting:

```js
const server = app.listen(PORT)

const shutdown = async (signal) => {
  console.log(`Received ${signal}, shutting down gracefully`)
  server.close(() => {                    // Stop accepting new connections
    console.log('HTTP server closed')
  })
  await db.pool.end()                     // Release database connections
  process.exit(0)
}

process.on('SIGTERM', () => shutdown('SIGTERM'))
process.on('SIGINT',  () => shutdown('SIGINT'))
```

---

## RUN Instruction Best Practices

**Chain commands to minimize layers:**
```dockerfile
# CORRECT — one layer, cache cleanup effective
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      dumb-init \
      curl && \
    rm -rf /var/lib/apt/lists/*

# WRONG — three layers; apt cache persists in second layer even after removal
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*
```

**Always combine `apt-get update` + `apt-get install`:** If they are in separate `RUN` instructions, Docker caches the `update` layer. Later builds that add packages will reuse the stale cache, installing outdated versions.

**Use `--no-install-recommends`:** Reduces installed packages to the minimum required.

**Pipefail for piped commands:**
```dockerfile
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN wget -qO- https://example.com/installer.sh | sh
# Without pipefail, wget failure is silently swallowed if sh succeeds
```

**Use `COPY` not `ADD` for local files:** `ADD` auto-extracts archives and fetches remote URLs without TLS validation (MITM risk, zip bomb risk). Use `COPY` for local files. Use `RUN curl/wget` for remote resources, so cleanup happens in the same layer.

---

## Common Anti-Patterns Quick Reference

| Anti-Pattern | Consequence | Fix |
|---|---|---|
| `FROM node:latest` | Non-deterministic builds | `FROM node:22.11-alpine3.20` |
| Single-stage build | Dev tools + secrets in prod image | Use multi-stage |
| No `USER` instruction | Container runs as root | Add `USER node` before CMD |
| Shell form CMD | SIGTERM swallowed, hard kill | `CMD ["node", "server.js"]` |
| `COPY .npmrc` / `ENV TOKEN=...` | Secret in image history | Use `--mount=type=secret` |
| `COPY . .` before `npm ci` | Cache busted on every commit | Copy lockfiles first |
| `npm install` not `npm ci` | Non-deterministic install | Always `npm ci` |
| `ADD` for local files | Implicit extraction, MITM risk | Use `COPY` |
| Missing `.dockerignore` | node_modules / creds in context | Create `.dockerignore` |
| Cleaning cache in next `RUN` | Previous layer still stores data | Chain cleanup in same `RUN` |
| No HEALTHCHECK | Orchestrator can't detect crashes | Add HEALTHCHECK to runtime stage |
| `apt-get update` in separate `RUN` | Stale package cache | Chain with `apt-get install` |
| Checking external deps in liveness | Restart cascade on DB outage | Liveness = app-only; readiness = full |

---

## References

For deeper coverage of each topic:

- `references/multi-stage-builds.md` — BuildKit parallelism, secrets, advanced stage patterns
- `references/base-images.md` — full comparison, native module edge cases, Distroless debugging
- `references/security-hardening.md` — hardening checklist, capabilities, read-only filesystem, image signing
- `references/runtime-config.md` — HEALTHCHECK deep dive, Compose health conditions, env var patterns
- `references/process-management.md` — dumb-init setup, CMD vs ENTRYPOINT, graceful shutdown patterns

Working examples:
- `examples/nodejs-express.Dockerfile` — Express API multi-stage build
- `examples/nextjs-standalone.Dockerfile` — Next.js standalone output
- `examples/.dockerignore-nodejs` — complete Node.js .dockerignore
- `examples/docker-compose-healthcheck.yml` — Compose with service_healthy conditions
