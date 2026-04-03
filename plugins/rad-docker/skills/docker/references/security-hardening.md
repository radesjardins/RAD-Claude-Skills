# Security Hardening: Deep Dive

## The Hardening Checklist

Apply these in order — each adds an independent layer of defense.

### 1. Non-Root User (Critical)

Docker runs as `root` by default. Root inside a container maps to root on the host in many configurations, enabling container escape attacks.

```dockerfile
# For Node.js official images (node user pre-exists)
COPY --from=builder --chown=node:node /app/dist ./dist
COPY --from=builder --chown=node:node /app/node_modules ./node_modules
USER node

# For Debian/Ubuntu base images — create a dedicated user
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/false --no-create-home appuser
USER appuser

# For Alpine base images
RUN addgroup -S -g 1001 appgroup && \
    adduser -S -u 1001 -G appgroup -H -D appuser
USER appuser
```

**The `--no-log-init` edge case:** On Debian/Ubuntu, `useradd` writes to `/var/log/faillog` and `/var/log/lastlog`. For very large UIDs (>65536), a bug in the Go `archive/tar` package can cause these files to balloon into GBs of null bytes, filling the layer. Add `--no-log-init` to `useradd`:
```dockerfile
RUN useradd --no-log-init --uid 1001 --gid appgroup appuser
```

**Never install `sudo`:** It causes unpredictable TTY and signal-forwarding behavior inside containers. If a daemon requires root initialization before dropping privileges, use `gosu` instead.

### 2. Minimal Base Images

Each additional package is a potential CVE entry point.

- Prefer Alpine over slim; prefer Distroless over Alpine for highest security
- Install only the exact packages needed: `apk add --no-cache dumb-init curl`
- Do not install text editors, compilers, or "nice to have" utilities in runtime images

### 3. Multi-Stage Builds

Multi-stage builds are themselves a security control, not just an optimization:
- Build-time tools (TypeScript, Webpack, test frameworks) never reach production
- Build-time secrets (`.npmrc` tokens, SSH keys) are discarded with the builder stage
- Source code is compiled and discarded; only binary artifacts ship

### 4. Secret Management (BuildKit)

Never place secrets in `ENV`, `ARG`, or `COPY`. They are permanently recorded in image layer history.

```bash
# Inspect a compromised image
docker history --no-trunc my-leaked-image
# Shows every ENV and COPY command — secrets are fully visible
```

**Build-time secrets via BuildKit:**
```dockerfile
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci
```
```bash
docker build --secret id=npmrc,src=.npmrc .
```

**Runtime secrets:** Inject via orchestrator at container start. Never bake into the image.
- Kubernetes: `env.valueFrom.secretKeyRef` or mounted `Secret` volumes
- AWS ECS: Secrets Manager integration via task definition
- Docker Compose: `secrets:` block with `external: true`

### 5. COPY vs ADD

Use `COPY` for all local file operations. `ADD` has implicit behavior that introduces risk:

| Operation | `COPY` | `ADD` |
|-----------|--------|-------|
| Local file copy | ✓ | ✓ |
| Remote URL fetch | ✗ | ✓ — no TLS validation, MITM risk |
| Auto-extract archives | ✗ | ✓ — zip bomb / Zip Slip risk |

**Only exception:** `ADD` has checksums for remote resources — acceptable if you need deterministic remote file downloads and can verify the checksum.

### 6. Read-Only Filesystem (Runtime Flag)

Run the container with a read-only root filesystem — applications should not be writing to their own image layers:

```bash
docker run --read-only --tmpfs /tmp --tmpfs /var/run my-image
```

```yaml
# docker-compose.yml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
```

Directories that legitimately need writes (temp files, PID files) get `tmpfs` mounts. This ensures that even if an attacker achieves code execution, they cannot modify application binaries.

### 7. Drop Linux Capabilities (Runtime Flag)

Docker grants a default set of Linux capabilities that most applications never need. Drop all, add back only what is required:

```bash
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE my-image
```

```yaml
# docker-compose.yml
services:
  app:
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if binding port < 1024
```

Common capabilities most applications don't need: `SYS_ADMIN`, `SYS_PTRACE`, `NET_ADMIN`, `CHOWN`, `SETUID`, `SETGID`.

### 8. Image Signing and Verification

**Docker Content Trust (Notary):**
```bash
export DOCKER_CONTENT_TRUST=1
docker push my-registry/my-image:latest
docker pull my-registry/my-image:latest
```

**Sigstore/cosign (modern approach):**
```bash
cosign sign my-registry/my-image@sha256:abc123
cosign verify my-registry/my-image@sha256:abc123
```

### 9. Security Scanning in CI

Integrate vulnerability scanning into every image build:

```yaml
# GitHub Actions example
- name: Scan image with Docker Scout
  run: docker scout cves $IMAGE_TAG --exit-code

- name: Scan with Trivy
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.IMAGE_TAG }}
    exit-code: '1'
    severity: CRITICAL,HIGH
```

## Security Review Checklist

When reviewing a Dockerfile for security:

- [ ] No `USER root` or missing `USER` instruction in runtime stage
- [ ] No `ENV` or `ARG` containing passwords, tokens, or keys
- [ ] No `COPY .npmrc`, `COPY .env`, `COPY *.pem`, or similar
- [ ] `.dockerignore` exists and excludes secrets
- [ ] `ADD` only used where `COPY` cannot suffice (remote resources with checksum)
- [ ] Base image is pinned (not `:latest`)
- [ ] Base image is minimal (slim/Alpine/Distroless for runtime, not full Debian)
- [ ] Multi-stage build separates build tools from runtime
- [ ] No `sudo` or `su` in Dockerfile
- [ ] No unnecessary packages installed in runtime stage
- [ ] For Distroless: `USER nonroot` or equivalent UID
