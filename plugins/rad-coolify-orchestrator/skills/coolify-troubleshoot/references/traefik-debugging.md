# Traefik Debugging in Coolify

## How Traefik Works in Coolify

Coolify runs Traefik as `coolify-proxy` — a Docker container that:
1. Listens on ports 80 (HTTP) and 443 (HTTPS)
2. Watches Docker container events for label changes
3. Routes requests to containers based on Traefik labels
4. Handles SSL termination via Let's Encrypt
5. Manages HTTP→HTTPS redirects

## Inspecting Traefik Configuration

### View Active Routers

```bash
# Traefik dashboard (if enabled)
# Access at http://<SERVER_IP>:8080/dashboard/ (usually disabled in production)

# View dynamic configuration from Docker labels
docker inspect <APP_CONTAINER> --format '{{json .Config.Labels}}' | python3 -m json.tool | grep traefik

# View Traefik logs
docker logs coolify-proxy --tail 100

# View Traefik logs filtered for errors
docker logs coolify-proxy 2>&1 | grep -i "error\|level=error\|no server"
```

### Common Traefik Labels Set by Coolify

```json
{
  "traefik.enable": "true",
  "traefik.http.routers.app-uuid.rule": "Host(`app.example.com`)",
  "traefik.http.routers.app-uuid.entrypoints": "https",
  "traefik.http.routers.app-uuid.tls": "true",
  "traefik.http.routers.app-uuid.tls.certresolver": "letsencrypt",
  "traefik.http.services.app-uuid.loadbalancer.server.port": "3000",
  "traefik.http.routers.app-uuid-http.rule": "Host(`app.example.com`)",
  "traefik.http.routers.app-uuid-http.entrypoints": "http",
  "traefik.http.routers.app-uuid-http.middlewares": "redirect-to-https"
}
```

### Verifying Correct Routing

```bash
# Step 1: Check that Traefik sees the container
docker exec coolify-proxy wget -qO- http://localhost:8080/api/http/routers 2>/dev/null | python3 -m json.tool

# Step 2: Check the container is on the right network
docker network inspect coolify | grep <APP_CONTAINER>

# Step 3: Test internal connectivity
docker exec coolify-proxy wget -qO- http://<APP_CONTAINER>:<PORT>/ 2>&1

# Step 4: Check entry points
docker exec coolify-proxy cat /etc/traefik/traefik.yml
```

## Common Traefik Issues

### "no server is available" Error

This means Traefik knows about the route but cannot reach any backend:

```
Causes:
├─ Container is not running
├─ Container is on a different Docker network than Traefik
├─ Container health check is failing (Traefik won't route to unhealthy containers)
├─ Port mismatch (label says 3000, app listens on 8080)
└─ Container just started and hasn't bound the port yet
```

**Diagnosis**:
```bash
# Is the container running?
docker ps | grep <APP_NAME>

# Is it on the coolify network?
docker inspect <CONTAINER> --format '{{json .NetworkSettings.Networks}}' | grep coolify

# Is the port correct?
docker exec <CONTAINER> ss -tlnp 2>/dev/null || docker exec <CONTAINER> netstat -tlnp

# Can Traefik reach it?
docker exec coolify-proxy wget -qO- http://<CONTAINER_NAME>:<PORT>/healthz
```

### Routing to Wrong Container

If multiple containers share a domain label:

```bash
# List all containers with traefik labels for a domain
docker ps -q | xargs docker inspect --format '{{.Name}} {{index .Config.Labels "traefik.http.routers"}}' 2>/dev/null | grep "example.com"
```

Fix: Ensure only one running container has the domain label. Old containers from failed deploys may still have the label — remove them.

### HTTPS Redirect Loop

Symptom: Browser shows "too many redirects" or ERR_TOO_MANY_REDIRECTS.

```
Causes:
├─ Cloudflare "Flexible" SSL mode + Coolify HTTPS redirect = infinite loop
│  └─ Fix: Set Cloudflare SSL mode to "Full (Strict)"
├─ Load balancer terminating SSL and re-sending as HTTP
│  └─ Fix: Configure Traefik to trust X-Forwarded-Proto header
└─ Multiple redirect middlewares applied
   └─ Fix: Check labels for duplicate redirect rules
```

### Custom Traefik Configuration

Coolify manages `traefik.yml` automatically. For custom middleware:

```bash
# View current Traefik config
docker exec coolify-proxy cat /etc/traefik/traefik.yml

# Coolify stores Traefik config in:
# /data/coolify/proxy/
ls -la /data/coolify/proxy/
```

**Warning**: Manually editing Traefik config may be overwritten by Coolify. Use Coolify's custom labels feature for application-specific Traefik configuration.

## Traefik Log Analysis

### Useful Log Patterns

```bash
# Successful routing
docker logs coolify-proxy 2>&1 | grep "200\|201\|301\|302"

# Failed routing (5xx errors)
docker logs coolify-proxy 2>&1 | grep "502\|503\|504"

# Certificate events
docker logs coolify-proxy 2>&1 | grep -i "certificate\|acme\|letsencrypt"

# Router registration
docker logs coolify-proxy 2>&1 | grep -i "router\|service"

# Configuration changes
docker logs coolify-proxy 2>&1 | grep -i "configuration\|provider"
```

### Access Logs

If access logs are enabled:
```bash
# Check if access logs are configured
docker exec coolify-proxy cat /etc/traefik/traefik.yml | grep -A5 "accessLog"

# View access logs
docker logs coolify-proxy 2>&1 | head -50
```

## Restarting Traefik

```bash
# Restart Traefik (minimal impact — requests queue briefly)
docker restart coolify-proxy

# Force recreate (loses in-memory state including ACME challenges in progress)
# Only if restart doesn't fix the issue
cd /data/coolify/source
docker compose up -d --force-recreate coolify-proxy
```

**Note**: Restarting Traefik does NOT cause downtime for apps. Requests queue for a few seconds during restart and are served once Traefik is back. Active WebSocket connections will be dropped.
