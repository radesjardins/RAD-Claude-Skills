---
name: supabase-storage
description: >
  This skill should be used when working with Supabase Storage, managing buckets, uploading
  or downloading files, configuring storage policies, or handling file transformations.
  Trigger when: "Supabase storage", "storage bucket", "file upload", "file download",
  "storage policy", "image transformation", "create bucket", "storage RLS",
  "public bucket", "private bucket", "signed URL", "storage CDN",
  "supabase storage", "upload file to Supabase",
  or any file storage operation in a Supabase project.
---

# Supabase Storage

Guidance for managing file storage, buckets, access policies, and file operations in Supabase.

## Overview

Supabase Storage is an S3-compatible file storage system integrated with Supabase Auth and RLS. Files are organized into buckets and accessed through the Storage API or client libraries.

## Bucket Management

### Creating Buckets via SQL (MCP)

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
-- This is typically already enabled, but verify
alter table storage.objects enable row level security;
```

### Common Policy Patterns

#### Authenticated Users Upload to Own Folder

```sql
create policy "Users upload to own folder"
  on storage.objects for insert
  to authenticated
  with check (
    bucket_id = 'avatars'
    and (storage.foldername(name))[1] = auth.uid()::text
  );
```

#### Users Read Own Files

```sql
create policy "Users read own files"
  on storage.objects for select
  to authenticated
  using (
    bucket_id = 'documents'
    and (storage.foldername(name))[1] = auth.uid()::text
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
    and (storage.foldername(name))[1] = auth.uid()::text
  );
```

### Storage Helper Functions

Supabase provides built-in helper functions for storage policies:

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

## Image Transformations

Supabase Storage supports on-the-fly image transformations for public URLs:

```typescript
const { data } = supabase.storage
  .from("images")
  .getPublicUrl("photo.jpg", {
    transform: {
      width: 200,
      height: 200,
      resize: "cover",    // cover, contain, fill
      format: "origin",   // origin, avif, webp
      quality: 80,        // 1-100
    },
  });
```

Transformation parameters can also be passed as URL parameters:
```
/storage/v1/render/image/public/images/photo.jpg?width=200&height=200&resize=cover
```

## Storage in Edge Functions

Access storage from edge functions using the Supabase client:

```typescript
const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
);

// Upload from edge function
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
file_size_limit = "50MiB"         # Max file size
image_transformation.enabled = true # Enable image transforms
```

## Storage Logs (MCP)

```
mcp__supabase__get_logs(project_id: "<id>", service: "storage")
```

Returns storage-related logs from the last 24 hours.

## Best Practices

1. **Use private buckets by default** — only make buckets public when files should be world-readable
2. **Organize by user ID** — use `{user_id}/filename` path convention for per-user files
3. **Set file size limits** on buckets to prevent abuse
4. **Restrict MIME types** to prevent unexpected file uploads
5. **Use signed URLs** for temporary access to private files
6. **Enable image transformations** to serve optimized images
7. **Apply RLS policies** to `storage.objects` for fine-grained access control
