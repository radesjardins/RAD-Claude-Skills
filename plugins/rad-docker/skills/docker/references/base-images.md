# Base Image Selection: Deep Dive

## The Four Tiers

### Tier 1: Full Debian (`node:22`, `node:22-bullseye`)
- **Size:** ~1.1 GB
- **Base OS:** Full Debian with dev tools, compilers (Python, G++), package managers
- **Security:** Lowest — hundreds of system libraries, many with CVEs
- **Use:** Builder stage ONLY. Never use as a production runtime image.

### Tier 2: Slim (`node:22-slim`, `node:22-bullseye-slim`)
- **Size:** ~230 MB
- **Base OS:** Stripped Debian — only what Node.js needs to run
- **Security:** Medium — no compilers, but has shell and package manager
- **libc:** `glibc` — full compatibility with native Node.js C++ modules
- **Use:** Production runtime when native C++ modules are required (`bcrypt`, `sharp`, `canvas`, `argon2`, `node-gyp` built packages)

### Tier 3: Alpine (`node:22-alpine`)
- **Size:** ~55 MB
- **Base OS:** Alpine Linux with `musl` libc and `busybox`
- **Security:** High — minimal attack surface, few preinstalled packages
- **libc:** `musl` — may cause issues with native C++ modules compiled for `glibc`
- **Use:** Production runtime for pure JavaScript applications or apps with no native module dependencies

### Tier 4: Distroless (`gcr.io/distroless/nodejs22-debian12`)
- **Size:** ~110 MB
- **Base OS:** Google-maintained; contains only the application runtime, no shell, no package manager, no utilities
- **Security:** Highest — no shell means no interactive attacker session; no `apt`, `sh`, `ls`, `cat` available
- **libc:** `glibc` (Debian-based) — full native module compatibility
- **Use:** Production runtime with maximum security requirements

## Decision Matrix

```
Does your app use native C++ modules (bcrypt, sharp, canvas, argon2)?
├── YES → Use node:22-slim (glibc compatible)
└── NO  → Does your org require maximum security hardening?
          ├── YES → Use gcr.io/distroless/nodejs22-debian12
          └── NO  → Use node:22-alpine (smallest footprint)
```

## Alpine and Native Modules: The musl Problem

Alpine Linux uses `musl` libc instead of the GNU C Library (`glibc`) used by Debian/Ubuntu. Many native Node.js addons are compiled against `glibc` and will fail on Alpine with errors like:

```
Error: /lib/x86_64-linux-musl/libc.so.6: invalid ELF header
```

**Affected packages (partial list):**
- `bcrypt` / `bcryptjs` — use `bcryptjs` (pure JS) to avoid this
- `sharp` — image processing; Alpine support possible but needs `libc6-compat`
- `canvas` — requires `glibc`
- `node-gyp` built packages in general

**Workarounds for Alpine with native modules:**

Option A — Install `libc6-compat`:
```dockerfile
FROM node:22-alpine
RUN apk add --no-cache libc6-compat
```
Works for many packages but not all; test explicitly.

Option B — Switch to slim:
```dockerfile
FROM node:22-slim AS runtime
```
Clean solution; larger image but no compatibility risk.

## Distroless: Setup and Debugging

Since Distroless has no package manager, dependencies must be installed in the builder stage and copied across:

```dockerfile
FROM node:22 AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY . .
RUN npm run build

FROM gcr.io/distroless/nodejs22-debian12 AS runtime
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./package.json
USER nonroot
EXPOSE 3000
CMD ["dist/server.js"]
# Note: Distroless runs node directly, so CMD takes the script path, not "node" + path
```

**Debugging Distroless:** The standard image has no shell. Use the `:debug` tag which adds `busybox` for emergency access:
```bash
docker run --rm -it --entrypoint /busybox/sh gcr.io/distroless/nodejs22-debian12:debug
```

## Version Pinning Strategies

### Strategy 1: Specific version tag (recommended default)
```dockerfile
FROM node:22.11.0-alpine3.20
```
- Deterministic: same image every pull
- Still benefits from OS security patches if Alpine patch version is updated
- Easy to read and audit

### Strategy 2: SHA256 digest (maximum immutability)
```dockerfile
FROM node:22-alpine@sha256:a1b2c3d4e5f6...
```
- Absolutely immutable — guarantees the exact same image bytes on every pull
- Opt-out of all upstream security patches (must update digest manually)
- Combine with Docker Scout / Snyk to be alerted when patched digests are available

### Strategy 3: Major version tag with `--pull` (not recommended for production)
```dockerfile
FROM node:22-alpine  # Will pull latest patch for node:22-alpine
```
- Build with `docker build --pull` to force the latest patch
- Non-deterministic without `--pull`; inconsistent between developers

## How to Find a SHA256 Digest

```bash
# Get the digest for a specific tag
docker pull node:22.11.0-alpine3.20
docker inspect node:22.11.0-alpine3.20 --format='{{index .RepoDigests 0}}'
# Output: node@sha256:abc123...

# Or use docker buildx imagetools
docker buildx imagetools inspect node:22-alpine
```

## Automated Security Monitoring

**Docker Scout** (built into Docker Desktop and Docker CLI):
```bash
docker scout cves my-image:latest
docker scout recommendations my-image:latest
```

**Snyk:**
```bash
snyk container test my-image:latest
```

Use these tools in CI pipelines to catch newly discovered CVEs in your pinned base images without requiring manual monitoring.
