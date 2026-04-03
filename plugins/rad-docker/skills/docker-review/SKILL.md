---
name: docker-review
description: >
  User-invoked skill to perform a comprehensive Dockerfile review. Trigger when the user
  explicitly invokes /rad-docker:docker-review, or says: "review my Dockerfile",
  "check my Dockerfile", "audit my Dockerfile", "is my Dockerfile production ready",
  "what's wrong with my Dockerfile", "review my Docker setup", "check my Docker config",
  "Dockerfile best practices review", "Docker security review".
argument-hint: "[path/to/Dockerfile — defaults to Dockerfile in current directory]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Dockerfile Review

Perform a comprehensive, autonomous review of the specified Dockerfile (or all Dockerfiles in the project if no path is given). Do NOT ask the user what to check — scan first, report findings.

---

## Phase 1: Locate and Read Files

1. If a path argument was provided, read that file. Otherwise:
   - Use Glob to find all Dockerfiles: `Dockerfile`, `Dockerfile.*`, `*.Dockerfile`, `docker/Dockerfile*`
   - Also find `docker-compose*.yml` and `compose.yaml`
   - Also find `.dockerignore`

2. Read every Dockerfile found. Build a complete picture before reporting.

3. If a `package.json` exists in the same directory, read it to understand the project type (Node.js, Next.js, NestJS, etc.) and what scripts (`build`, `start`) are defined.

---

## Phase 2: Critical Issues — Must Fix

These cause security vulnerabilities, silent failures, or broken deployments. Flag every match as **CRITICAL**.

### C1: No Multi-Stage Build
Flag if the Dockerfile has only one `FROM` instruction and appears to be a production image. Single-stage images bake dev tools, compilers, and devDependencies into production. Skip this check if the Dockerfile is explicitly labeled as a dev/test image.

### C2: Running as Root
Flag if there is no `USER` instruction in the final stage. Docker runs as root by default. Any compromised process has unrestricted filesystem access and a path to host escape.

### C3: Shell Form CMD or ENTRYPOINT
Flag any CMD or ENTRYPOINT using shell form (string, not JSON array):
- Bad: `CMD npm start`, `CMD node server.js`, `ENTRYPOINT /docker-entrypoint.sh`
- Good: `CMD ["node", "server.js"]`, `ENTRYPOINT ["dumb-init", "--"]`
Shell form wraps the process in `/bin/sh -c`, which swallows SIGTERM and prevents graceful shutdown.

### C4: Using `:latest` or Unpinned Tags
Flag any `FROM` instruction that:
- Uses `:latest` explicitly
- Omits a tag entirely (e.g., `FROM node`)
- Uses only a major version (e.g., `FROM node:22` with no minor/patch or distro)

### C5: Secrets in Image Layers
Flag any of:
- `COPY .npmrc` or `COPY .env` or `COPY *.pem` — copies credentials into the image
- `ENV *_TOKEN=`, `ENV *_KEY=`, `ENV *_SECRET=`, `ENV *_PASSWORD=` with hardcoded values
- `ARG` followed immediately by `ENV` for sensitive variable names
- `RUN npm install` or `npm ci` without `--mount=type=secret` but evidence of needing private packages (`.npmrc` exists, or `@org/` scoped packages in `package.json`)

### C6: Source Code Copied Before Dependency Install
Flag if `COPY . .` or any broad `COPY` appears before `RUN npm ci` / `RUN yarn install` / `RUN pnpm install`. This busts the dependency cache on every commit.

### C7: `npm install` Instead of `npm ci`
Flag any `RUN npm install` in a Dockerfile. `npm install` is non-deterministic and modifies the lockfile. Use `npm ci` for reproducible, lockfile-adherent installs.

### C8: Using `ADD` for Local Files
Flag `ADD` instructions where the source is a local file or directory (not a URL). `ADD` auto-extracts archives (zip bomb risk) and fetches remote URLs without TLS validation. Use `COPY` for local files.

### C9: Missing `.dockerignore`
If `.dockerignore` does not exist in the project root, flag it. Without it, `COPY . .` sends `node_modules`, `.git`, `.env`, and secrets to the Docker daemon.

---

## Phase 3: Warnings — Should Fix

Flag each as **WARNING**. These degrade security, performance, or reliability.

### W1: No HEALTHCHECK
Every production service container should have a `HEALTHCHECK` instruction. Without it, orchestrators cannot detect unhealthy containers and route traffic away from them.

### W2: Cleaning Caches in a Separate RUN Layer
If `apt-get update` or package installation is in one `RUN` and cleanup (`rm -rf /var/lib/apt/lists/*`) is in a separate `RUN`, the cache is permanently stored in the first layer. Chain them: `RUN apt-get update && apt-get install -y ... && rm -rf /var/lib/apt/lists/*`.

### W3: `apt-get update` Without `apt-get install` in the Same RUN
If `apt-get update` is in its own `RUN` instruction, subsequent builds will reuse the stale cache and may install outdated packages. Always chain: `RUN apt-get update && apt-get install -y --no-install-recommends ...`.

### W4: Full Debian Base Image in Runtime Stage
If the final (runtime) stage uses `FROM node:XX` (full Debian, not `slim` or `alpine`) without a clear justification, flag it. Full images ship hundreds of unnecessary packages and compilers.

### W5: No EXPOSE Instruction
`EXPOSE` is documentation. Its absence makes it unclear what port the application uses. Add it even though it does not publish the port.

### W6: No `dumb-init` or `--init` for Signal Handling
If Node.js is launched without a proper init system (no `dumb-init`, `tini`, or `--init`), PID 1 signal handling is unreliable. Check for `RUN apk add dumb-init` or equivalent and `ENTRYPOINT ["dumb-init", "--"]`.

### W7: `NODE_ENV` Not Set to `production`
`ENV NODE_ENV=production` must be set in the runtime stage. Without it, many frameworks (Express, NestJS, etc.) enable development behaviors (verbose error stacks, slower template rendering) in production.

### W8: devDependencies Not Pruned
If the runtime stage copies `node_modules` without evidence of `npm prune --production` or `npm ci --omit=dev`, devDependencies are included in the final image. They bloat size and expand CVE surface.

### W9: `--no-install-recommends` Missing
When installing system packages with `apt-get install`, missing `--no-install-recommends` causes many extra packages to be installed beyond the direct dependency. Always: `apt-get install -y --no-install-recommends <package>`.

---

## Phase 4: Informational — Consider Improving

Flag as **INFO**.

### I1: Consider BuildKit Cache Mounts
`RUN --mount=type=cache,target=/root/.npm npm ci` can dramatically speed up CI builds by caching the npm cache across builds without affecting the final image.

### I2: Consider SHA256 Digest Pinning
For maximum build immutability, pin base images to SHA256 digest (`node:22-alpine@sha256:...`) rather than version tags. Combine with Docker Scout for automated security monitoring.

### I3: `start-period` May Be Too Short
If `HEALTHCHECK --start-period` is less than 30s for an application that runs database migrations or has a slow startup, it may incorrectly fail early health checks.

### I4: Consider Distroless for Maximum Security
If the application has no native C++ module dependencies, `gcr.io/distroless/nodejs22-debian12` provides a harder security profile than Alpine (no shell, no package manager, no utilities for an attacker to use).

---

## Phase 5: Output the Report

After completing all checks, produce a report in this exact format:

```
## Dockerfile Review Report

**Files reviewed:** [list all Dockerfiles and docker-compose files found]
**Project type:** [Node.js Express / Next.js / NestJS / Generic Node.js / Unknown]
**Build stages:** [count — single-stage or multi-stage]

---

### CRITICAL — Must Fix

> Security vulnerabilities, broken deployments, and architectural anti-patterns.

- [ ] **[Issue title]** — `Dockerfile:lineNumber`
  [Explanation of what is wrong and the specific risk]
  **Fix:** [Concrete, copy-pasteable fix]

(If none: "No critical issues found.")

---

### WARNING — Should Fix

> Performance degradation, best practice violations, production readiness gaps.

- [ ] **[Issue title]** — `Dockerfile:lineNumber`
  [Explanation]
  **Fix:** [Concrete fix instruction]

(If none: "No warnings.")

---

### INFO — Consider Improving

> Suggestions that improve performance, security posture, or maintainability.

- [ ] **[Suggestion]** — `Dockerfile:lineNumber`
  [Recommendation]

(If none: "No additional suggestions.")

---

### PASSED — Correctly Implemented

> Patterns correctly implemented. Acknowledge good work.

- [x] **[What was done correctly]**
  [Brief note on why this is good practice]

---

### Verdict

**[PRODUCTION READY / NOT PRODUCTION READY]** — [1–2 sentence summary of the most important issues to fix]
```

---

## Rules

1. **Be autonomous.** Never ask the user what to check. Read the files yourself.
2. **Be specific.** Always include file path and line number for every finding.
3. **Be actionable.** Every CRITICAL and WARNING must include a concrete, copy-pasteable fix.
4. **Be fair.** Always populate the PASSED section. Find and acknowledge what is done well.
5. **Be accurate.** Only report issues you have confirmed by reading the actual Dockerfile. Do not hallucinate issues.
6. **Open with verdict.** End the report with a clear PRODUCTION READY or NOT PRODUCTION READY verdict.
