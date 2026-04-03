# Process Management: Deep Dive

## The PID 1 Problem

In Linux, every process has a Process ID (PID). The kernel assigns PID 1 special treatment:

1. **PID 1 does NOT receive default signal behaviors.** For all other PIDs, an unhandled SIGTERM causes the process to exit. PID 1 ignores SIGTERM unless it explicitly registers a handler.
2. **PID 1 is the init process.** It adopts orphaned child processes. If PID 1 exits without reaping its children, zombie processes accumulate.

When Docker stops a container (`docker stop`, scale-down, deployment rollout), it sends SIGTERM to PID 1. If PID 1 ignores SIGTERM, Docker waits 10 seconds and then sends SIGKILL — a forced kill that:
- Drops all in-flight HTTP requests immediately
- Leaves database connections unreleased
- Causes data corruption for operations mid-write

**Three ways Node.js becomes PID 1 in a container:**
1. `CMD ["node", "server.js"]` — Node.js is directly PID 1 ✓ (receives signals, must handle them)
2. `CMD ["npm", "start"]` — npm is PID 1 and does NOT forward signals to Node.js ✗
3. `CMD node server.js` (shell form) — `/bin/sh` is PID 1 and swallows signals ✗

## dumb-init: The Standard Solution

`dumb-init` is a minimal init process (< 200KB) that:
1. Runs as PID 1
2. Spawns your application as its child process
3. Proxies all signals to the child process group
4. Reaps zombie processes

```dockerfile
# Alpine
RUN apk add --no-cache dumb-init

# Debian/Ubuntu
RUN apt-get update && apt-get install -y --no-install-recommends dumb-init && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
```

How it works: dumb-init takes PID 1, spawns `node dist/server.js` as a child, and when Docker sends SIGTERM to PID 1 (dumb-init), dumb-init forwards SIGTERM to the Node.js process. Node.js then runs its SIGTERM handler.

## tini: The Alternative

`tini` is functionally similar to `dumb-init`. Docker Desktop and Docker Engine v1.13+ include tini — use `docker run --init` to activate it without modifying the Dockerfile.

```bash
# Use Docker's built-in init — no Dockerfile change needed
docker run --init my-image
```

```yaml
# docker-compose.yml
services:
  app:
    init: true
```

## CMD vs ENTRYPOINT: Definitive Guide

Both `CMD` and `ENTRYPOINT` define what runs when the container starts. Their interaction is subtle.

### ENTRYPOINT: The Fixed Executable

`ENTRYPOINT` defines the command that always runs. It can only be overridden with `docker run --entrypoint`.

```dockerfile
ENTRYPOINT ["dumb-init", "--"]
# Always runs dumb-init, regardless of docker run arguments
```

### CMD: Default Arguments

`CMD` provides default arguments to `ENTRYPOINT`, or the default command if no `ENTRYPOINT` is set. Override by passing arguments to `docker run`.

```dockerfile
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
# Default: dumb-init -- node dist/server.js
# Override: docker run my-image node dist/worker.js
#           Runs: dumb-init -- node dist/worker.js
```

### Forms: Exec vs Shell

Both instructions support two forms:

**Exec form (JSON array) — always prefer:**
```dockerfile
CMD ["node", "server.js"]           # Process receives signals directly
ENTRYPOINT ["dumb-init", "--"]
```
- Spawns the process directly; no shell involved
- Process receives signals from Docker/OS
- Arguments are passed literally, no shell expansion

**Shell form (string) — avoid:**
```dockerfile
CMD node server.js                  # Runs: /bin/sh -c "node server.js"
```
- Wraps in `/bin/sh -c`; shell becomes PID 1
- Shell does NOT forward signals to child processes
- `$VAR` expansion works but at the cost of signal handling

### Interaction Table

| Dockerfile | `docker run my-image` | `docker run my-image arg` |
|-----------|----------------------|--------------------------|
| Only `CMD ["a","b"]` | Runs `a b` | Runs `arg` (CMD replaced) |
| Only `ENTRYPOINT ["a"]` | Runs `a` | Runs `a arg` (arg appended) |
| `ENTRYPOINT ["a"]` + `CMD ["b"]` | Runs `a b` | Runs `a arg` (CMD replaced by arg) |

## Graceful Shutdown in Node.js

Node.js must explicitly register signal handlers. Default behavior is:
- `SIGTERM`: ignored if Node.js is PID 1; otherwise causes process to exit immediately
- `SIGINT`: causes process to exit immediately (Ctrl+C)

With `dumb-init`, Node.js receives the signal. It still needs to handle it gracefully:

### Express/Node.js HTTP Server

```js
const app = express()
const server = app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server listening on port ${PORT}`)
})

let isShuttingDown = false

const shutdown = async (signal) => {
  if (isShuttingDown) return
  isShuttingDown = true
  console.log(`Received ${signal}. Starting graceful shutdown...`)

  // 1. Stop accepting new connections
  server.close(async () => {
    console.log('HTTP server closed.')

    try {
      // 2. Clean up resources
      await db.pool.end()
      await redis.quit()
      console.log('All connections closed. Exiting.')
      process.exit(0)
    } catch (err) {
      console.error('Error during shutdown:', err)
      process.exit(1)
    }
  })

  // 3. Force exit after timeout (if connections don't drain)
  setTimeout(() => {
    console.error('Graceful shutdown timed out. Forcing exit.')
    process.exit(1)
  }, 30_000)
}

process.on('SIGTERM', () => shutdown('SIGTERM'))
process.on('SIGINT',  () => shutdown('SIGINT'))
```

### Fastify Graceful Shutdown

```js
const fastify = require('fastify')({ logger: true })

const shutdown = async (signal) => {
  fastify.log.info({ signal }, 'Received signal, closing server')
  await fastify.close()  // Fastify handles connection draining
  process.exit(0)
}

process.on('SIGTERM', () => shutdown('SIGTERM'))
process.on('SIGINT',  () => shutdown('SIGINT'))
```

### NestJS Graceful Shutdown

```ts
// main.ts
const app = await NestFactory.create(AppModule)
app.enableShutdownHooks()  // NestJS handles SIGTERM/SIGINT automatically
await app.listen(3000)
```

## npm start vs Direct node Invocation

**Avoid `npm start` as PID 1:**
```dockerfile
# WRONG — npm is PID 1, does not forward signals
CMD ["npm", "start"]
```

`npm` is a process manager, not an init system. It does not forward SIGTERM to Node.js. Docker sends SIGTERM → npm (PID 1) → npm ignores → Docker waits 10s → Docker sends SIGKILL → Node.js hard-killed.

**Use direct invocation:**
```dockerfile
# CORRECT — dumb-init handles PID 1, node receives signals
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
```

## Zombie Process Reaping

When a process exits and its parent hasn't waited for it, it becomes a "zombie" (defunct process). Zombie processes consume a PID slot and clutter `ps` output.

If your Node.js application spawns child processes (via `child_process.spawn`, cluster workers, etc.), those children can become zombies if they outlive their parent without being reaped.

`dumb-init` automatically reaps orphaned zombie processes as the init process — another reason to always use it.

## Summary: Process Management Checklist

- [ ] Use exec form for CMD: `CMD ["node", "server.js"]`, not `CMD node server.js`
- [ ] Install and use `dumb-init` or `tini` as ENTRYPOINT for PID 1 handling
- [ ] Register `process.on('SIGTERM')` and `process.on('SIGINT')` handlers in app code
- [ ] Graceful shutdown: stop accepting new connections, drain existing, close DB connections, then exit
- [ ] Set a shutdown timeout to force exit if connections don't drain within 30s
- [ ] Never use `CMD ["npm", "start"]` — npm doesn't forward signals
- [ ] Set `HOSTNAME=0.0.0.0` for Next.js standalone to bind to all interfaces
