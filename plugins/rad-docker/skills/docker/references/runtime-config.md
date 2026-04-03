# Runtime Configuration: Deep Dive

## HEALTHCHECK

The `HEALTHCHECK` instruction tells Docker how to verify that a container is healthy — not just running, but capable of serving traffic.

### Anatomy of a Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
  CMD wget -qO- http://localhost:3000/health || exit 1
```

| Option | Default | Recommended | Purpose |
|--------|---------|-------------|---------|
| `--interval` | 30s | 30s | How often to run the check |
| `--timeout` | 30s | 5–10s | Max time before marking as failed |
| `--retries` | 3 | 3 | Consecutive failures before "unhealthy" |
| `--start-period` | 0s | 40s–120s | Grace period before failures count |

### What the Health Endpoint Should Check

A `/health` endpoint should be fast (<100ms) and verify internal readiness:

```js
// Minimal health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', uptime: process.uptime() })
})

// Production health check — check dependencies
app.get('/health', async (req, res) => {
  try {
    await db.query('SELECT 1')          // DB connectivity
    const memUsage = process.memoryUsage()
    const memMB = memUsage.rss / 1024 / 1024
    if (memMB > 500) throw new Error('Memory pressure')
    res.status(200).json({ status: 'ok' })
  } catch (err) {
    res.status(503).json({ status: 'degraded', error: err.message })
  }
})
```

### Health Check Command Options

**wget (preferred for Alpine — pre-installed):**
```dockerfile
HEALTHCHECK CMD wget -qO- http://localhost:3000/health || exit 1
```

**curl (install explicitly):**
```dockerfile
RUN apk add --no-cache curl
HEALTHCHECK CMD curl -f http://localhost:3000/health || exit 1
```

**Node.js script (no external tools needed):**
```dockerfile
HEALTHCHECK CMD node -e "require('http').get('http://localhost:3000/health', r => process.exit(r.statusCode === 200 ? 0 : 1)).on('error', () => process.exit(1))"
```

### Liveness vs. Readiness (Kubernetes)

In Kubernetes, `HEALTHCHECK` maps to **readiness probes** (stop routing traffic) and **liveness probes** (restart the container) — these have different requirements:

| Probe | Purpose | Should check |
|-------|---------|--------------|
| Liveness | Should container be restarted? | App-internal only (memory, deadlocks) |
| Readiness | Should traffic be routed here? | App + dependencies (DB, cache) |

**Critical mistake:** Including external dependency checks (database, Redis) in a **liveness** probe. If the database goes down, liveness fails, and Kubernetes endlessly restarts your application — which cannot fix the database and creates a restart cascade.

```yaml
# Kubernetes example — separate liveness and readiness
livenessProbe:
  httpGet:
    path: /health/live   # Only checks: process alive, no OOM
    port: 3000
  initialDelaySeconds: 40
  periodSeconds: 30

readinessProbe:
  httpGet:
    path: /health/ready  # Checks: DB connected, cache available
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 10
```

### start-period — Why It Matters

Services that run database migrations, JIT compile, or warm up caches need time before they can pass health checks. Without `--start-period`, Docker starts counting failures immediately — triggering unnecessary restarts during normal startup.

Rule of thumb:
- Lightweight APIs: `--start-period=30s`
- Apps with migrations or warmup: `--start-period=60s`
- Heavy JVM or ML model loading: `--start-period=120s`

---

## Port Configuration

### EXPOSE vs -p

`EXPOSE` is metadata — it records which port the application listens on for documentation and inter-container communication, but does NOT publish the port to the host.

```dockerfile
EXPOSE 3000    # Documents intent; does not open port
```

Actual port binding happens at runtime:
```bash
docker run -p 3000:3000 my-image           # host:container
docker run -p 8080:3000 my-image           # Map container 3000 → host 8080
docker run -P my-image                     # Auto-map all EXPOSE'd ports to random host ports
```

### Port Best Practices

- Always include `EXPOSE` for documentation and Docker network discovery
- Bind to `0.0.0.0` not `127.0.0.1` inside the container (otherwise the port is unreachable from outside)
- Let operators control the host port mapping — don't hardcode it in the image

```js
// Correct: bind to all interfaces
app.listen(PORT, '0.0.0.0', () => { ... })

// Wrong: only accessible from inside the container
app.listen(PORT, '127.0.0.1', () => { ... })
```

---

## Environment Variables

### In the Dockerfile: Non-Sensitive Defaults Only

```dockerfile
ENV NODE_ENV=production      # Enable framework production optimizations
ENV PORT=3000                # Overridable default
ENV LOG_LEVEL=info           # Overridable default
```

### At Runtime: Configuration and Secrets

```bash
# Single variable
docker run -e DATABASE_URL="postgres://..." my-image

# From .env file (not for production secrets)
docker run --env-file .env.production my-image
```

### What Belongs Where

| Type | Mechanism | Where |
|------|-----------|-------|
| App defaults (non-secret) | `ENV` in Dockerfile | Dockerfile |
| Runtime config | `-e` flag or platform config | Runtime |
| Sensitive secrets | Platform secret store | Never in image |
| Build-time tokens | `--mount=type=secret` | BuildKit only |

### Next.js Runtime Injection

`NEXT_PUBLIC_*` variables are inlined at `next build` time into the client-side JavaScript bundle. They **cannot** be changed without rebuilding the image, breaking the "build once, deploy anywhere" principle.

**Solutions:**

1. **`next-runtime-env` library:** Reads values from `window.__ENV` injected server-side
2. **`export const dynamic = 'force-dynamic'`:** Forces server-side rendering, accessing `process.env` fresh on each request
3. **Entrypoint `sed` substitution** (escape hatch): Replace placeholder values in the built bundle at container start
4. **Server-side proxy pattern:** Expose config via an API endpoint (`/api/config`) that reads `process.env` at request time

---

## Docker Compose: Health Conditions

`depends_on` with no condition only waits for container start — not readiness. Use `condition: service_healthy` to ensure dependent services wait for actual readiness.

```yaml
services:
  app:
    build: .
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: postgres://postgres:secret@db:5432/mydb

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: secret
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### Circular Dependency Edge Case

If Service A needs Service B healthy before starting, but Service B needs Service A for bootstrap configuration, Docker Compose has no native solution. Workaround: start services in a degraded mode via environment variable and have them retry dependencies on a backoff loop rather than failing fast.
