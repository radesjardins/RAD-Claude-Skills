---
name: supabase-edge-functions
description: >
  This skill should be used when developing, deploying, or managing Supabase Edge Functions,
  working with Deno in Supabase, or building serverless endpoints.
  Trigger when: "edge function", "deploy function", "supabase functions", "Deno function",
  "serverless endpoint", "functions serve", "functions deploy", "create function",
  "webhook handler", "Supabase function secrets", "function logs",
  "supabase functions new", "invoke function", "edge runtime",
  or building any server-side TypeScript function for Supabase.
---

# Supabase Edge Functions

Guidance for developing, deploying, and managing Edge Functions using both MCP tools and CLI.

## Overview

Edge Functions are globally distributed TypeScript functions running on Deno. They serve as server-side endpoints for webhooks, API routes, scheduled tasks, and third-party integrations.

## Creating Edge Functions

### Via CLI (Recommended for Local Development)

```bash
supabase functions new my-function
```

Creates `supabase/functions/my-function/index.ts` with a starter template.

### Function Structure

```
supabase/functions/
├── _shared/              # Shared modules across functions
│   └── cors.ts
├── my-function/
│   ├── index.ts          # Entry point (required)
│   └── deno.json         # Deno config (optional)
└── another-function/
    └── index.ts
```

### Basic Function Template

```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

Deno.serve(async (req: Request) => {
  const { name } = await req.json();

  return new Response(
    JSON.stringify({ message: `Hello ${name}!` }),
    { headers: { "Content-Type": "application/json" } }
  );
});
```

### Function with Supabase Client

```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

Deno.serve(async (req: Request) => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );

  const { data, error } = await supabase
    .from("profiles")
    .select("*")
    .limit(10);

  return new Response(JSON.stringify({ data, error }), {
    headers: { "Content-Type": "application/json" },
  });
});
```

### CORS Headers (Shared Module)

```typescript
// supabase/functions/_shared/cors.ts
export const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};
```

## Deploying Edge Functions

### Via MCP

```
mcp__supabase__deploy_edge_function(
  project_id: "<project_id>",
  name: "my-function",
  entrypoint_path: "index.ts",
  verify_jwt: true,
  files: [
    { "name": "index.ts", "content": "<function code>" },
    { "name": "deno.json", "content": "<deno config if exists>" }
  ]
)
```

**JWT Verification (`verify_jwt`):**
- **Always enable** (`true`) for authorized access
- Only disable if: the function previously had it disabled, the function body implements custom auth (API keys, webhooks), or the user explicitly requests it

**Include supporting files:** Pass `deno.json`, `deno.jsonc`, and any relative dependencies in the `files` array.

### Via CLI

```bash
# Deploy single function
supabase functions deploy my-function

# Deploy all functions
supabase functions deploy

# Deploy without JWT verification (webhooks, public endpoints)
supabase functions deploy my-function --no-verify-jwt
```

### Listing Functions

```
# MCP
mcp__supabase__list_edge_functions(project_id: "<id>")

# CLI
supabase functions list
```

### Getting Function Code (MCP)

```
mcp__supabase__get_edge_function(
  project_id: "<id>",
  function_slug: "my-function"
)
```

Returns the function's file contents. Use this to inspect deployed function code.

## Local Development

### Serve Functions Locally

```bash
supabase functions serve
```

Starts a local edge runtime. Functions are available at:
```
http://localhost:54321/functions/v1/<function-name>
```

### Test Locally with curl

```bash
curl -i --location --request POST \
  'http://localhost:54321/functions/v1/my-function' \
  --header 'Authorization: Bearer <anon-key>' \
  --header 'Content-Type: application/json' \
  --data '{"name": "World"}'
```

### Environment Variables

Edge Functions access environment variables via `Deno.env.get()`. Built-in variables available in deployed functions:

| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Project API URL |
| `SUPABASE_ANON_KEY` | Anon/public key |
| `SUPABASE_SERVICE_ROLE_KEY` | Service role key (bypasses RLS) |
| `SUPABASE_DB_URL` | Direct Postgres connection string |

### Managing Secrets

```bash
supabase secrets set MY_API_KEY=sk-xxx ANOTHER_SECRET=value
supabase secrets list
supabase secrets unset MY_API_KEY
```

Secrets are available as environment variables in deployed edge functions.

## Common Patterns

### Webhook Handler (Stripe)

```typescript
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import Stripe from "npm:stripe@17";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY")!);
const webhookSecret = Deno.env.get("STRIPE_WEBHOOK_SECRET")!;

Deno.serve(async (req: Request) => {
  const body = await req.text();
  const signature = req.headers.get("stripe-signature")!;

  const event = await stripe.webhooks.constructEventAsync(
    body, signature, webhookSecret
  );

  switch (event.type) {
    case "checkout.session.completed":
      // Handle completed checkout
      break;
  }

  return new Response(JSON.stringify({ received: true }), {
    headers: { "Content-Type": "application/json" },
  });
});
```

### Scheduled Function (pg_cron)

Edge Functions can be triggered by `pg_cron` via `pg_net`:

```sql
select cron.schedule(
  'daily-cleanup',
  '0 3 * * *',
  $$
  select net.http_post(
    url := 'https://<project>.supabase.co/functions/v1/cleanup',
    headers := '{"Authorization": "Bearer <service_role_key>"}'::jsonb
  );
  $$
);
```

## Function Logs

### Via MCP

```
mcp__supabase__get_logs(
  project_id: "<id>",
  service: "edge-function"
)
```

Returns logs from the last 24 hours for all edge functions.

## CLI vs MCP Decision Matrix

| Task | Use CLI | Use MCP |
|------|---------|---------|
| Create function scaffold | `functions new` | Not available |
| Deploy function | `functions deploy` | `deploy_edge_function` |
| List functions | `functions list` | `list_edge_functions` |
| Get function code | `functions download` | `get_edge_function` |
| Serve locally | `functions serve` | Not available |
| Manage secrets | `secrets set/list/unset` | Not available |
| View logs | Dashboard | `get_logs` (service: edge-function) |
| Delete function | `functions delete` | Not available |
