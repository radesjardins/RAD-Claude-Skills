---
name: supabase-auth
description: >
  This skill should be used when configuring Supabase authentication, setting up auth providers,
  managing users, working with JWTs, or implementing auth flows in applications.
  Trigger when: "Supabase auth", "authentication", "sign up", "sign in", "OAuth provider",
  "auth configuration", "JWT", "auth.users", "auth.uid()", "service role key",
  "anon key", "user management", "auth hooks", "email templates",
  "social login", "magic link", "password reset", "auth middleware",
  or implementing any authentication with Supabase.
---

# Supabase Authentication

Guidance for configuring and implementing Supabase Auth, managing users, and integrating auth providers.

## Overview

Supabase Auth provides a complete authentication system with support for email/password, magic links, OAuth providers, phone auth, and SSO. It manages the `auth.users` table and issues JWTs for API authorization.

## Auth Architecture

```
Client App → Supabase Auth API → auth.users table
                ↓
            JWT issued → Used in API requests
                ↓
            RLS policies check auth.uid() against table data
```

**Key concept:** Authentication (who is the user) is handled by Supabase Auth. Authorization (what can the user do) is handled by RLS policies referencing `auth.uid()`.

## Client-Side Auth (supabase-js)

### Sign Up

```typescript
const { data, error } = await supabase.auth.signUp({
  email: "user@example.com",
  password: "<your-password>",
});
```

### Sign In (Email/Password)

```typescript
const { data, error } = await supabase.auth.signInWithPassword({
  email: "user@example.com",
  password: "<your-password>",
});
```

### Sign In (OAuth)

```typescript
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: "google",
  options: {
    redirectTo: "https://myapp.com/auth/callback",
  },
});
```

### Sign In (Magic Link)

```typescript
const { data, error } = await supabase.auth.signInWithOtp({
  email: "user@example.com",
});
```

### Sign Out

```typescript
const { error } = await supabase.auth.signOut();
```

### Get Current User

```typescript
const { data: { user } } = await supabase.auth.getUser();
```

### Listen for Auth Changes

```typescript
supabase.auth.onAuthStateChange((event, session) => {
  if (event === "SIGNED_IN") {
    // Handle sign in
  }
});
```

## Server-Side Auth

### Verifying Users in Edge Functions

```typescript
import { createClient } from "jsr:@supabase/supabase-js@2";

Deno.serve(async (req: Request) => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_ANON_KEY")!,
    {
      global: {
        headers: { Authorization: req.headers.get("Authorization")! },
      },
    }
  );

  const { data: { user }, error } = await supabase.auth.getUser();
  if (error || !user) {
    return new Response("Unauthorized", { status: 401 });
  }

  // User is authenticated, proceed...
});
```

### Service Role Key (Admin Operations)

The service role key bypasses RLS. Use it only server-side for admin operations:

```typescript
const supabaseAdmin = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
);

// Admin: list all users
const { data: { users } } = await supabaseAdmin.auth.admin.listUsers();
```

**Never expose the service role key to the client.**

## Auth Configuration (config.toml)

Configure auth for local development in `supabase/config.toml`:

```toml
[auth]
enabled = true
site_url = "http://localhost:3000"
additional_redirect_urls = ["http://localhost:3000/auth/callback"]
jwt_expiry = 3600
enable_signup = true

[auth.email]
enable_signup = true
double_confirm_changes = true
enable_confirmations = false  # Set true for production

[auth.external.google]
enabled = true
client_id = "env(GOOGLE_CLIENT_ID)"
secret = "env(GOOGLE_CLIENT_SECRET)"
redirect_uri = ""  # Uses default
```

## Supported Providers

| Provider | Config Key | Notes |
|----------|-----------|-------|
| Email/Password | `[auth.email]` | Built-in, always available |
| Phone/SMS | `[auth.sms]` | Requires Twilio or other provider |
| Google | `[auth.external.google]` | OAuth 2.0 |
| GitHub | `[auth.external.github]` | OAuth 2.0 |
| Apple | `[auth.external.apple]` | OAuth 2.0 |
| Discord | `[auth.external.discord]` | OAuth 2.0 |
| Twitter/X | `[auth.external.twitter]` | OAuth 2.0 |
| Azure AD | `[auth.external.azure]` | OAuth 2.0 / OIDC |
| SAML SSO | Dashboard config | Enterprise feature |

## User Management via SQL

Query and manage users using MCP `execute_sql`:

```sql
-- List recent signups
SELECT id, email, created_at, last_sign_in_at
FROM auth.users
ORDER BY created_at DESC
LIMIT 20;

-- Count users by provider
SELECT raw_app_meta_data->>'provider' as provider, count(*)
FROM auth.users
GROUP BY provider;

-- Check user metadata
SELECT id, email, raw_user_meta_data
FROM auth.users
WHERE email = 'user@example.com';
```

## Auth + RLS Integration

The core pattern: RLS policies use `auth.uid()` to reference the current authenticated user.

```sql
-- Users can only read their own profile
create policy "Users read own profile"
  on public.profiles for select
  using (auth.uid() = id);

-- Users can only insert their own profile
create policy "Users insert own profile"
  on public.profiles for insert
  with check (auth.uid() = id);

-- Service role bypasses all RLS
-- Anon key respects RLS (uses JWT claims)
```

## Auth Logs (MCP)

```
mcp__supabase__get_logs(project_id: "<id>", service: "auth")
```

Returns auth-related logs from the last 24 hours. Useful for debugging sign-in failures, provider issues, and JWT problems.

## Common Auth Patterns

### Profile Creation on Sign-Up (Database Trigger)

Automatically create a profile when a user signs up:

```sql
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, display_name, email)
  values (new.id, new.raw_user_meta_data->>'full_name', new.email);
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
```

### Protected API Route Pattern

```typescript
// Middleware pattern for edge functions
function requireAuth(handler: (req: Request, user: User) => Promise<Response>) {
  return async (req: Request) => {
    const supabase = createClient(/* ... with auth header */);
    const { data: { user }, error } = await supabase.auth.getUser();
    if (!user) return new Response("Unauthorized", { status: 401 });
    return handler(req, user);
  };
}
```

## Searching Supabase Auth Docs (MCP)

For the latest auth documentation, use:
```
mcp__supabase__search_docs(query: "auth <specific topic>")
```
