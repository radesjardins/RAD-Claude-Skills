# syntax=docker/dockerfile:1
#
# Production Dockerfile — Node.js / Express API
# Multi-stage: builder (full tools) → runtime (Alpine minimal)
#
# Usage:
#   docker build -t my-api .
#   docker build --secret id=npmrc,src=.npmrc -t my-api .  (for private packages)
#   docker run -p 3000:3000 -e DATABASE_URL="..." my-api

# ─── Stage 1: Builder ─────────────────────────────────────────────────────────
FROM node:22-alpine AS builder
WORKDIR /app

# 1. Copy lockfiles FIRST — maximizes npm ci layer cache
#    This layer only rebuilds when dependencies actually change.
COPY package.json package-lock.json ./

# 2. Install ALL dependencies (including devDependencies for build tools)
#    Use npm ci — strictly honors lockfile, reproducible installs.
#
#    For private npm packages, use BuildKit secret mounting:
#    RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
RUN npm ci

# 3. Copy source code AFTER dependency install
COPY . .

# 4. Compile TypeScript and prune dev dependencies
RUN npm run build

# 5. Remove devDependencies — only production deps go to runtime
RUN npm prune --production

# ─── Stage 2: Runtime ─────────────────────────────────────────────────────────
FROM node:22-alpine AS runtime

# dumb-init: runs as PID 1, correctly proxies signals (SIGTERM) to Node.js
# Without this, Docker sends SIGTERM → Node.js ignores it → forced SIGKILL after 10s
RUN apk add --no-cache dumb-init

WORKDIR /app

# Enable production mode for Express and all Node.js libraries
ENV NODE_ENV=production
# Document default port; override at runtime with -e PORT=8080
ENV PORT=3000

# Copy ONLY the compiled output and production dependencies
# --chown ensures the node user owns these files (required for USER node below)
COPY --from=builder --chown=node:node /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/dist ./dist
COPY --from=builder --chown=node:node /app/package.json ./package.json

# Drop to non-root user — principle of least privilege
# The 'node' user is pre-created in official Node.js images
USER node

# EXPOSE is documentation only — it does NOT publish the port.
# Use -p 3000:3000 at docker run time.
EXPOSE 3000

# Health check: verify the /health endpoint responds
# --start-period: 40s grace period for startup (migrations, warmup, JIT)
# --retries 3: require 3 consecutive failures before marking unhealthy
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
  CMD wget -qO- http://localhost:3000/health || exit 1

# ENTRYPOINT + CMD pattern:
# - ENTRYPOINT: always dumb-init (fixed, not overridable without --entrypoint)
# - CMD: the application command (overridable with docker run arguments)
# Both MUST use exec (JSON array) form — shell form swallows signals
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
