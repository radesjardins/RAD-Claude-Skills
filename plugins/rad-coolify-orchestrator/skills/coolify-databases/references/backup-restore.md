# Database Backup and Restore — Detailed Reference

## PostgreSQL Backup and Restore

### Automated Backup (via Coolify)

Coolify runs `pg_dump` inside the container and compresses the output:

```bash
# What Coolify executes internally:
docker exec <CONTAINER> pg_dump -U <USER> <DATABASE> | gzip > backup_<TIMESTAMP>.sql.gz
```

The compressed dump is then uploaded to the configured S3 storage.

### Manual Backup

```bash
# Dump a specific database
docker exec <PG_CONTAINER> pg_dump -U postgres -d mydb -Fc > mydb.dump

# Dump all databases
docker exec <PG_CONTAINER> pg_dumpall -U postgres > all_databases.sql

# Dump with compression
docker exec <PG_CONTAINER> pg_dump -U postgres -d mydb | gzip > mydb.sql.gz
```

### Restore

```bash
# Restore from custom format dump
docker exec -i <PG_CONTAINER> pg_restore -U postgres -d mydb < mydb.dump

# Restore from SQL dump
docker exec -i <PG_CONTAINER> psql -U postgres -d mydb < mydb.sql

# Restore from compressed dump
gunzip -c mydb.sql.gz | docker exec -i <PG_CONTAINER> psql -U postgres -d mydb

# Restore to a new database (avoid overwriting production)
docker exec <PG_CONTAINER> createdb -U postgres mydb_restored
gunzip -c mydb.sql.gz | docker exec -i <PG_CONTAINER> psql -U postgres -d mydb_restored
```

### Point-in-Time Recovery (PITR)

Coolify's built-in backup uses `pg_dump` (logical backups), which does **not** support point-in-time recovery. For PITR:

1. Enable WAL archiving in PostgreSQL configuration
2. Configure continuous archiving to S3
3. This requires custom PostgreSQL configuration — not managed by Coolify's UI

**Recommendation**: For critical production databases needing PITR, manage PostgreSQL outside Coolify or use a managed service (Supabase, Neon, RDS).

## MySQL / MariaDB Backup and Restore

### Automated Backup (via Coolify)

```bash
# What Coolify executes internally:
docker exec <CONTAINER> mysqldump -u root -p<PASSWORD> <DATABASE> | gzip > backup.sql.gz
```

### Manual Backup

```bash
# Single database
docker exec <MYSQL_CONTAINER> mysqldump -u root -p<PASSWORD> mydb > mydb.sql

# All databases
docker exec <MYSQL_CONTAINER> mysqldump -u root -p<PASSWORD> --all-databases > all.sql

# With compression
docker exec <MYSQL_CONTAINER> mysqldump -u root -p<PASSWORD> mydb | gzip > mydb.sql.gz

# Consistent backup with single transaction (InnoDB)
docker exec <MYSQL_CONTAINER> mysqldump -u root -p<PASSWORD> --single-transaction mydb > mydb.sql
```

### Restore

```bash
# Restore from SQL dump
docker exec -i <MYSQL_CONTAINER> mysql -u root -p<PASSWORD> mydb < mydb.sql

# Restore from compressed dump
gunzip -c mydb.sql.gz | docker exec -i <MYSQL_CONTAINER> mysql -u root -p<PASSWORD> mydb
```

### Binary Log Recovery

MySQL binary log recovery is not managed by Coolify. For point-in-time recovery:
- Enable binary logging in MySQL configuration
- Use `mysqlbinlog` tool to replay events
- Requires manual configuration outside Coolify's UI

## MongoDB Backup and Restore

### Automated Backup (via Coolify)

```bash
# What Coolify executes internally:
docker exec <CONTAINER> mongodump --archive | gzip > backup.archive.gz
```

### Manual Backup

```bash
# All databases
docker exec <MONGO_CONTAINER> mongodump --archive > backup.archive

# Specific database
docker exec <MONGO_CONTAINER> mongodump --db mydb --archive > mydb.archive

# With compression
docker exec <MONGO_CONTAINER> mongodump --archive --gzip > backup.archive.gz
```

### Restore

```bash
# Restore all databases
docker exec -i <MONGO_CONTAINER> mongorestore --archive < backup.archive

# Restore specific database
docker exec -i <MONGO_CONTAINER> mongorestore --db mydb --archive < mydb.archive

# Restore from compressed archive
docker exec -i <MONGO_CONTAINER> mongorestore --archive --gzip < backup.archive.gz

# Drop existing collections before restore
docker exec -i <MONGO_CONTAINER> mongorestore --drop --archive < backup.archive
```

## Redis Persistence Configuration

Coolify does not provide built-in backup for Redis. Configure persistence manually:

### RDB Snapshots

Add to Redis configuration (via environment variable or custom config):

```
# Save snapshot every 60 seconds if at least 1000 keys changed
save 60 1000

# Save snapshot every 300 seconds if at least 100 keys changed
save 300 100
```

### AOF (Append Only File)

```
appendonly yes
appendfsync everysec
```

### Backup Redis Data

```bash
# RDB file is at /data/dump.rdb inside the container
docker cp <REDIS_CONTAINER>:/data/dump.rdb ./redis-backup.rdb

# Restore by copying back
docker cp ./redis-backup.rdb <REDIS_CONTAINER>:/data/dump.rdb
docker restart <REDIS_CONTAINER>
```

## S3 Storage Configuration Details

### AWS S3

```
Endpoint: s3.amazonaws.com (or s3.<REGION>.amazonaws.com)
Region: us-east-1 (or your bucket's region)
Bucket: coolify-backups
Access Key: AKIA...
Secret Key: ...
```

### DigitalOcean Spaces

```
Endpoint: <REGION>.digitaloceanspaces.com (e.g., nyc3.digitaloceanspaces.com)
Region: nyc3
Bucket: coolify-backups
Access Key: (from DO Spaces keys)
Secret Key: (from DO Spaces keys)
```

### MinIO (Self-Hosted)

```
Endpoint: https://minio.example.com (or http://minio-host:9000)
Region: us-east-1 (MinIO default)
Bucket: coolify-backups
Access Key: minioadmin (or custom)
Secret Key: minioadmin (or custom)
```

### Backblaze B2

```
Endpoint: s3.us-west-002.backblazeb2.com (varies by region)
Region: us-west-002
Bucket: coolify-backups
Access Key: (B2 application key ID)
Secret Key: (B2 application key)
```

### Hetzner Object Storage

```
Endpoint: fsn1.your-objectstorage.com (varies by location)
Region: fsn1
Bucket: coolify-backups
Access Key: (from Hetzner console)
Secret Key: (from Hetzner console)
```

## Backup Verification Strategy

### Automated Verification

Set up a cron job or scheduled task to periodically:

1. Download the latest backup from S3
2. Restore it to a temporary database container
3. Run a sanity check query
4. Report success/failure

```bash
#!/bin/bash
# backup-verify.sh — run weekly to verify backup integrity

LATEST=$(aws s3 ls s3://coolify-backups/postgres/ --recursive | sort | tail -1 | awk '{print $4}')
aws s3 cp "s3://coolify-backups/$LATEST" /tmp/latest-backup.sql.gz

# Start temp postgres container
docker run -d --name pg-verify -e POSTGRES_PASSWORD=verify postgres:16-alpine
sleep 5

gunzip -c /tmp/latest-backup.sql.gz | docker exec -i pg-verify psql -U postgres

# Run sanity check
RESULT=$(docker exec pg-verify psql -U postgres -t -c "SELECT count(*) FROM users;")
echo "Backup verification: $RESULT users found"

# Cleanup
docker rm -f pg-verify
rm /tmp/latest-backup.sql.gz
```
