# Multi-Stage Builds: Deep Dive

## Why Multi-Stage Builds Exist

Before multi-stage builds, teams used two separate Dockerfiles: one for building (with all tools) and one for production (minimal). This required external orchestration scripts and easily fell out of sync. Multi-stage builds consolidate everything into one declarative Dockerfile while achieving the same separation.

**Measured impact:**
- Single-stage Node.js image: typically 1.0–1.4 GB
- Multi-stage with Alpine runtime: typically 50–180 MB
- CVE reduction: up to 60% fewer vulnerable components

## Stage Naming and References

Name every stage with `AS <name>` — anonymous stages can only be referenced by their zero-based index, which breaks when stages are reordered.

```dockerfile
FROM node:22-alpine AS deps          # Stage: deps
FROM node:22-alpine AS builder       # Stage: builder
FROM node:22-alpine AS runtime       # Stage: runtime (the final, shipped image)
```

Reference named stages in `COPY --from`:
```dockerfile
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
```

## Separating Dependency Installation from Build

For large TypeScript or Next.js projects, split dependency installation into its own stage. This stage is cached independently — if only source code changes, Docker skips reinstalling packages entirely.

```dockerfile
# ─── Stage 1: Dependency installation ────────────────────────────────────────
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production          # Production-only for runtime
# OR: npm ci                          # All deps if build needs devDependencies

# ─── Stage 2: Build ───────────────────────────────────────────────────────────
FROM node:22 AS builder               # Full image for native compile if needed
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY package.json package-lock.json ./
RUN npm ci                            # Re-install with devDeps for build tools
COPY . .
RUN npm run build

# ─── Stage 3: Runtime ─────────────────────────────────────────────────────────
FROM node:22-alpine AS runtime
WORKDIR /app
RUN apk add --no-cache dumb-init
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules   # Already pruned
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./package.json
USER node
EXPOSE 3000
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
```

## BuildKit Parallelism

Docker BuildKit (the default engine since Docker 23+) executes independent stages in parallel automatically. Design stages without unnecessary dependencies to maximize parallel execution.

Enable BuildKit explicitly in older installations:
```bash
DOCKER_BUILDKIT=1 docker build .
# Or set in /etc/docker/daemon.json: { "features": { "buildkit": true } }
```

## BuildKit Secret Mounting

Use `--mount=type=secret` for build-time tokens. The secret is available during the `RUN` instruction only and is **never written to any image layer**.

```dockerfile
# syntax=docker/dockerfile:1

FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./

# Mount .npmrc as a secret — not baked into image
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci

COPY . .
RUN npm run build
```

Build command:
```bash
docker build --secret id=npmrc,src=.npmrc -t my-image .
```

**SSH key for private GitHub packages:**
```dockerfile
RUN --mount=type=ssh npm ci
```
```bash
eval $(ssh-agent) && ssh-add ~/.ssh/id_rsa
docker build --ssh default -t my-image .
```

## BuildKit Cache Mounts

Speed up repeated `npm ci` calls in CI by caching the npm cache directory across builds:

```dockerfile
RUN --mount=type=cache,target=/root/.npm \
    npm ci
```

This does NOT affect the image size — the cache mount is only available during the build, not in the final layer. Especially effective in CI environments with persistent build caches.

## Targeting Specific Stages

Build a specific stage (useful for running tests in CI without building the full image):

```bash
# Build only up to the builder stage for running tests
docker build --target builder -t my-image:test .
docker run my-image:test npm test

# Then build the full production image
docker build -t my-image:prod .
```

## What to Copy to Runtime — Checklist

Copy these from builder to runtime:
- ✅ Compiled output (`dist/`, `build/`, `.next/standalone/`)
- ✅ Production `node_modules` (after `npm prune --production`)
- ✅ `package.json` (needed for `npm start`, module resolution metadata)
- ✅ Static assets (`public/`, `.next/static/`) if not embedded in standalone output
- ✅ Any configuration files required at runtime (e.g., `prisma/schema.prisma` if using Prisma)

Never copy to runtime:
- ❌ `src/` or `*.ts` source files (already compiled)
- ❌ `devDependencies` in `node_modules`
- ❌ Build tool configs (`tsconfig.json`, `.eslintrc`, `jest.config.js`)
- ❌ `.npmrc`, `.env`, SSH keys, tokens
- ❌ Test files, coverage reports
- ❌ `.git` directory

## Next.js Standalone Output — Special Pattern

Next.js standalone mode (`output: 'standalone'` in `next.config.js`) traces and bundles only the imported modules. The `.next/standalone/` directory is self-contained and does NOT require copying `node_modules` manually.

```dockerfile
# next.config.js must have: output: 'standalone'

FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine AS runtime
RUN apk add --no-cache dumb-init
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

# Standalone server — no manual node_modules copy needed
COPY --from=builder --chown=node:node /app/.next/standalone ./
COPY --from=builder --chown=node:node /app/.next/static ./.next/static
COPY --from=builder --chown=node:node /app/public ./public

USER node
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
  CMD wget -qO- http://localhost:3000/api/health || exit 1
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]
```
