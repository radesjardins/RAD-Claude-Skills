# Database Connection Patterns — Detailed Reference

## Connection String Formats

### PostgreSQL

```
# Standard
postgresql://user:password@hostname:5432/database

# With SSL
postgresql://user:password@hostname:5432/database?sslmode=require

# With connection pool settings
postgresql://user:password@hostname:5432/database?sslmode=require&connection_limit=20

# Internal Coolify connection (same server)
postgresql://postgres:<GENERATED_PASSWORD>@<DB_CONTAINER_NAME>:5432/mydb
```

### MySQL / MariaDB

```
# Standard
mysql://user:password@hostname:3306/database

# With SSL
mysql://user:password@hostname:3306/database?ssl=true

# Internal Coolify connection
mysql://root:<GENERATED_PASSWORD>@<DB_CONTAINER_NAME>:3306/mydb
```

### MongoDB

```
# Standard
mongodb://user:password@hostname:27017/database

# With auth database
mongodb://user:password@hostname:27017/database?authSource=admin

# With SSL
mongodb://user:password@hostname:27017/database?ssl=true&authSource=admin

# Internal Coolify connection
mongodb://root:<GENERATED_PASSWORD>@<DB_CONTAINER_NAME>:27017/mydb?authSource=admin
```

### Redis

```
# Standard
redis://hostname:6379

# With password
redis://:password@hostname:6379

# With database number
redis://:password@hostname:6379/0

# Internal Coolify connection
redis://:<GENERATED_PASSWORD>@<DB_CONTAINER_NAME>:6379
```

## Finding the Container Name

Coolify assigns container names based on the resource UUID. Find it via:

1. **Coolify UI**: Database resource page shows the container name in the "General" tab
2. **CLI on server**:
   ```bash
   docker ps --filter "label=coolify.managed=true" --format "{{.Names}} {{.Image}}"
   ```
3. **Environment variable**: Coolify sets the connection URL as an environment variable on linked applications

## Connection Pooling

### Why Pool Connections?

Database connections are expensive. Without pooling:
- Each request opens a new TCP connection + auth handshake
- Connection limits are hit quickly under load
- PostgreSQL: default `max_connections = 100`

### PgBouncer (PostgreSQL)

Deploy PgBouncer as a separate service in Coolify:

```yaml
# docker-compose.yml
services:
  pgbouncer:
    image: edoburu/pgbouncer
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres-container:5432/mydb
      - POOL_MODE=transaction
      - MAX_CLIENT_CONN=200
      - DEFAULT_POOL_SIZE=25
    ports:
      - "6432"
```

Apps connect to PgBouncer instead of directly to PostgreSQL:
```
postgresql://postgres:password@pgbouncer:6432/mydb
```

### Application-Level Pooling

Most ORMs support connection pooling:

```javascript
// Prisma (Node.js)
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  // Connection pool managed by Prisma
}

// connection_limit in URL
// postgresql://user:pass@host:5432/db?connection_limit=10
```

```python
# SQLAlchemy (Python)
engine = create_engine(
    "postgresql://user:pass@host:5432/db",
    pool_size=10,
    max_overflow=20
)
```

## Secure External Access Patterns

### SSH Tunnel (Recommended for Development)

Instead of exposing the database port:

```bash
# Create SSH tunnel to Coolify server
ssh -L 5432:<DB_CONTAINER_NAME>:5432 user@coolify-server

# Connect local client to localhost:5432
psql -h localhost -p 5432 -U postgres -d mydb
```

This avoids exposing the database port to the internet.

### TablePlus / DBeaver Configuration

If port is exposed (temporary access only):

```
Host: <COOLIFY_SERVER_IP>
Port: <EXPOSED_PORT> (e.g., 5432 or custom)
User: postgres (or configured user)
Password: <FROM_COOLIFY_UI>
Database: mydb
SSL: Optional for same-network; required for internet access
```

### WireGuard / Tailscale VPN

For persistent, secure access without exposing ports:

1. Install Tailscale on the Coolify server and your local machine
2. Connect via Tailscale IP: `psql -h 100.x.x.x -p 5432 -U postgres`
3. No port exposure needed — traffic is encrypted and private

## Resource Limit Configuration

### Setting Limits in Coolify

In the database resource settings:

| Setting | Recommendation | Notes |
|---------|---------------|-------|
| **Memory Limit** | 80% of available RAM (for dedicated DB) | Leave headroom for OS and Docker |
| **Memory Reservation** | 50% of limit | Soft limit; container can burst |
| **CPU Limit** | Number of cores (e.g., `2.0`) | Prevents CPU monopolization |
| **CPU Reservation** | 50% of limit | Guaranteed minimum CPU |

### Per-Database Tuning

**PostgreSQL**:
```
# shared_buffers: 25% of container memory limit
shared_buffers = 512MB

# effective_cache_size: 50-75% of container memory
effective_cache_size = 1536MB

# work_mem: (memory_limit - shared_buffers) / (max_connections * 3)
work_mem = 16MB

# maintenance_work_mem: 5-10% of memory
maintenance_work_mem = 128MB
```

Set these via environment variables in Coolify:
```
POSTGRES_SHARED_BUFFERS=512MB
POSTGRES_EFFECTIVE_CACHE_SIZE=1536MB
```

Or mount a custom `postgresql.conf` via volumes.

**MySQL / MariaDB**:
```
# innodb_buffer_pool_size: 50-80% of container memory
innodb_buffer_pool_size = 1G

# max_connections
max_connections = 100
```

**Redis**:
```
# maxmemory: Set to container memory limit minus ~100MB for overhead
maxmemory 900mb
maxmemory-policy allkeys-lru
```

## Common OOM Scenarios

| Scenario | Cause | Fix |
|----------|-------|-----|
| PostgreSQL OOM during vacuum | `maintenance_work_mem` too high | Reduce to 256MB or less |
| MongoDB OOM with large collections | WiredTiger cache consumes all RAM | Set `wiredTigerCacheSizeGB` to 50% of container memory |
| Redis OOM | No `maxmemory` set; grows unbounded | Set `maxmemory` with an eviction policy |
| MySQL OOM during sort | `sort_buffer_size * connections` exceeds memory | Reduce `sort_buffer_size` or `max_connections` |
| Any DB OOM during backup | `pg_dump`/`mysqldump` buffers entire result in memory | Use `--no-synchronized-snapshots` or streaming backup |
