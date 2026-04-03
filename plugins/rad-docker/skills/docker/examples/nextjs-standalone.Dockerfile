# syntax=docker/dockerfile:1
#
# Production Dockerfile — Next.js (standalone output mode)
#
# Prerequisites:
#   next.config.js must include: output: 'standalone'
#   This enables Next.js to trace only imported modules, creating a
#   self-contained .next/standalone/ directory without full node_modules.
#
# Usage:
#   docker build -t my-nextjs-app .
#   docker run -p 3000:3000 my-nextjs-app
#
# NEXT_PUBLIC_* variables:
#   These are baked in at build time (next build inlines them into JS bundles).
#   Pass them as build-time ARGs OR use next-runtime-env for runtime injection.
#   See: https://github.com/expatfile/next-runtime-env

# ─── Stage 1: Dependencies ────────────────────────────────────────────────────
FROM node:22-alpine AS deps
WORKDIR /app

# Lockfile copy first — maximizes cache for the costly npm ci step
COPY package.json package-lock.json ./

# Alpine musl compatibility: needed for some Next.js native modules
RUN apk add --no-cache libc6-compat

RUN npm ci

# ─── Stage 2: Builder ─────────────────────────────────────────────────────────
FROM node:22-alpine AS builder
WORKDIR /app

# Inherit dependencies from the deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Disable Next.js telemetry during build
ENV NEXT_TELEMETRY_DISABLED=1

# If you have NEXT_PUBLIC_* variables that must be baked in at build time:
# ARG NEXT_PUBLIC_API_URL
# ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

RUN npm run build

# ─── Stage 3: Runtime ─────────────────────────────────────────────────────────
FROM node:22-alpine AS runtime

RUN apk add --no-cache dumb-init

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
# Next.js standalone server must bind to 0.0.0.0 — not 127.0.0.1
ENV HOSTNAME=0.0.0.0

# standalone/ contains the self-contained Next.js server
# It does NOT require a separate node_modules directory
COPY --from=builder --chown=node:node /app/.next/standalone ./

# static/ contains CSS, JS chunks, and other hashed assets
# Must be served from the same path as the standalone server expects
COPY --from=builder --chown=node:node /app/.next/static ./.next/static

# public/ contains unprocessed static files (images, robots.txt, sitemap.xml, etc.)
COPY --from=builder --chown=node:node /app/public ./public

USER node

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=60s \
  CMD wget -qO- http://localhost:3000/api/health || exit 1

ENTRYPOINT ["dumb-init", "--"]
# Next.js standalone entry point is always server.js at the root of standalone/
CMD ["node", "server.js"]
