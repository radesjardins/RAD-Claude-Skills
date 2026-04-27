---
name: supabase-storage
description: >
  This skill should be used when working with Supabase Storage, managing buckets, uploading
  or downloading files, configuring storage policies, or handling file transformations.
  Trigger when: "Supabase storage", "storage bucket", "file upload", "file download",
  "S3 protocol", "S3-compatible", "TUS upload", "resumable upload",
  "storage policy", "image transformation", "create bucket", "storage RLS",
  "public bucket", "private bucket", "signed URL", "storage CDN", "Smart CDN",
  "supabase storage", "upload file to Supabase", "list_storage_buckets",
  "get_storage_config", "update_storage_config",
  or any file storage operation in a Supabase project.
---

# Supabase Storage

Guidance for managing file storage, buckets, access policies, and file operations in Supabase. Pinned to April 2026.

## Overview

Supabase Storage is an S3-compatible file storage system integrated with Supabase Auth and RLS. It exposes **three interoperable upload protocols** that operate on the same objects:

| Protocol | Endpoint | Best for |
|----------|----------|----------|
| **REST** | `/storage/v1/object/...` | Default supabase-js client; small uploads |
| **TUS** (resumable) | `/storage/v1/upload/resumable` | Large file uploads, unreliable networks |
| **S3-compatible** | `/storage/v1/s3` | Existing S3 tooling (aws-cli, boto3, multipart uploads) |

S3 protocol shipped GA April 2024 — full multipart upload support; works with `aws s3 cp`, `boto3`, `rclone`, etc.

## Bucket Management

### Via MCP (v0.7+, off by default — enable with `--features=...,storage`)

The MCP server exposes three storage tools when the storage feature is enabled:

```
mcp__supabase__list_storage_buckets(project_id: "<id>")
mcp__supabase__get_storage_config(project_id: "<id>")
mcp__supabase__update_storage_config(project_id: "<id>", config: { ... })
```

`update_storage_config` is a mutating call — disabled when the server is in `--read-only` mode.

### Creating Buckets via SQL

Use `apply_migration` or `execute_sql` to manage buckets:

```sql
-- Create a private bucket
insert into storage.buckets (id, name, public)
values ('avatars', 'avatars', false);

-- Create a public bucket (files accessible without auth)
insert into storage.buckets (id, name, public)
values ('public-assets', 'public-assets', true);

-- Create bucket with file size limit (in bytes)
insert into storage.buckets (id, name, public, file_size_limit)
values ('documents', 'documents', false, 10485760); -- 10MB

-- Create bucket with allowed MIME types
insert into storage.buckets (id, name, public, allowed_mime_types)
values ('images', 'images', false, array['image/png', 'image/jpeg', 'image/webp']);
```

### Listing Buckets

```sql
select * from storage.buckets;
```

Or via MCP: `mcp__supabase__list_storage_buckets(project_id: "<id>")`.

### Deleting a Bucket

```sql
-- Must empty the bucket first
delete from storage.objects where bucket_id = 'old-bucket';
delete from storage.buckets where id = 'old-bucket';
```

## Storage Policies (RLS)

Storage uses RLS on the `storage.objects` table. Policies control who can upload, download, update, and delete files.

### Enable RLS on Storage

```sql
-- Typically already enabled, but verify
alter table storage.objects enable row level security;
```

### Common Policy Patterns

All examples use the `(select auth.uid())` initPlan-cached form (Splinter lint 0003).

#### Authenticated Users Upload to Own Folder

```sql
create policy "Users upload to own folder"
  on storage.objects for insert
  to authenticated
  with check (
    bucket_id = 'avatars'
    and (storage.foldername(name))[1] = (select auth.uid())::text
  );
```

#### Users Read Own Files

```sql
create policy "Users read own files"
  on storage.objects for select
  to authenticated
  using (
    bucket_id = 'documents'
    and (storage.foldername(name))[1] = (select auth.uid())::text
  );
```

#### Public Read on Public Bucket

```sql
create policy "Public read on public assets"
  on storage.objects for select
  using (bucket_id = 'public-assets');
```

#### Users Delete Own Files

```sql
create policy "Users delete own files"
  on storage.objects for delete
  to authenticated
  using (
    bucket_id = 'avatars'
    and (storage.foldername(name))[1] = (select auth.uid())::text
  );
```

### Storage Helper Functions

| Function | Description | Example |
|----------|-------------|---------|
| `storage.foldername(name)` | Returns folder path segments as array | `(storage.foldername(name))[1]` = first folder |
| `storage.filename(name)` | Returns the file name | `storage.filename(name) = 'avatar.png'` |
| `storage.extension(name)` | Returns the file extension | `storage.extension(name) = 'png'` |

## Client-Side File Operations

### Upload a File

```typescript
const { data, error } = await supabase.storage
  .from("avatars")
  .upload(`${userId}/avatar.png`, file, {
    cacheControl: "3600",
    upsert: true,
  });
```

### Resumable Upload (TUS — for large files)

```typescript
import { Upload } from "tus-js-client";

const upload = new Upload(file, {
  endpoint: `${SUPABASE_URL}/storage/v1/upload/resumable`,
  retryDelays: [0, 3000, 5000, 10000, 20000],
  headers: {
    authorization: `Bearer ${session.access_token}`,
    "x-upsert": "true",
  },
  metadata: {
    bucketName: "videos",
    objectName: `${userId}/recording.mp4`,
    contentType: "video/mp4",
  },
});
upload.start();
```

### S3-Compatible Upload (boto3)

```python
import boto3
client = boto3.client(
    "s3",
    endpoint_url="https://<project>.supabase.co/storage/v1/s3",
    aws_access_key_id="<storage_access_key>",
    aws_secret_access_key="<storage_secret_key>",
    region_name="auto",
)
client.upload_file("local.mp4", "videos", "userid/recording.mp4")
```

S3 access keys are managed in the dashboard under Storage → S3 Connection.

### Download a File

```typescript
const { data, error } = await supabase.storage
  .from("avatars")
  .download(`${userId}/avatar.png`);
```

### Get Public URL (Public Buckets)

```typescript
const { data } = supabase.storage
  .from("public-assets")
  .getPublicUrl("hero-image.png");
// data.publicUrl = https://<project>.supabase.co/storage/v1/object/public/public-assets/hero-image.png
```

### Create Signed URL (Private Buckets)

```typescript
const { data, error } = await supabase.storage
  .from("documents")
  .createSignedUrl("report.pdf", 3600); // Expires in 1 hour
```

### List Files in a Folder

```typescript
const { data, error } = await supabase.storage
  .from("avatars")
  .list(userId, {
    limit: 100,
    offset: 0,
    sortBy: { column: "created_at", order: "desc" },
  });
```

### Delete Files

```typescript
const { data, error } = await supabase.storage
  .from("avatars")
  .remove([`${userId}/avatar.png`]);
```

### Move/Copy Files

```typescript
// Move
await supabase.storage.from("avatars").move("old-path.png", "new-path.png");

// Copy
await supabase.storage.from("avatars").copy("source.png", "destination.png");
```

## Image Transformations (Pro+)

On-the-fly image transformations served through Smart CDN. **Pro plan and above only**; billed at $5 per 1,000 distinct origin images transformed (cached transforms are free).

```typescript
const { data } = supabase.storage
  .from("images")
  .getPublicUrl("photo.jpg", {
    transform: {
      width: 200,
      height: 200,
      resize: "cover",    // cover, contain, fill
      format: "origin",   // origin, avif, webp (auto-selects best for browser if "origin")
      quality: 80,        // 20-100
    },
  });
```

URL parameter form:
```
/storage/v1/render/image/public/images/photo.jpg?width=200&height=200&resize=cover
```

Smart CDN auto-invalidates on object update/delete and on new transform variants.

## Storage in Edge Functions

```typescript
const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
);

const { data, error } = await supabase.storage
  .from("generated")
  .upload("output.pdf", pdfBuffer, {
    contentType: "application/pdf",
  });
```

## Storage Configuration (config.toml)

```toml
[storage]
enabled = true
file_size_limit = "50MiB"             # Max file size
image_transformation.enabled = true   # Enable image transforms (Pro+)
```

## Storage Logs (MCP)

```
mcp__supabase__get_logs(project_id: "<id>", service: "storage")
```

Returns storage-related logs from the last 24 hours.

## Best Practices

1. **Use private buckets by default** — only make buckets public when files should be world-readable.
2. **Organize by user ID** — use `{user_id}/filename` path convention for per-user files.
3. **Set file size limits** on buckets to prevent abuse.
4. **Restrict MIME types** on user-upload buckets to prevent unexpected content.
5. **Use signed URLs** for temporary access to private files.
6. **Pick the right protocol** — REST for small uploads, TUS for large files / unreliable networks, S3 for existing tooling.
7. **Enable image transformations** on Pro+ to serve optimized images via Smart CDN.
8. **Apply RLS policies** to `storage.objects` for fine-grained access control — wrap `auth.uid()` in `(select ...)` for performance.
