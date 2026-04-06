---
name: supabase-projects
description: >
  This skill should be used when managing Supabase projects or organizations, creating new projects,
  listing projects, checking project status, retrieving API keys, pausing or restoring projects,
  or working with project costs and billing.
  Trigger when: "create Supabase project", "list Supabase projects", "Supabase API keys",
  "pause project", "restore project", "Supabase organization", "project cost",
  "get project URL", "publishable keys", "anon key", "service role key",
  "supabase link", "project settings", or managing Supabase project lifecycle.
---

# Supabase Project Management

Guidance for managing Supabase projects and organizations using both the MCP tools and CLI.

## Project Lifecycle

### Creating a Project (MCP)

Creating a project via MCP requires a cost confirmation flow:

1. **List organizations** to find the target org:
   ```
   mcp__supabase__list_organizations
   ```

2. **Get cost estimate** — always ask the user which organization:
   ```
   mcp__supabase__get_cost(type: "project", organization_id: "<org_id>")
   ```

3. **Confirm cost** with the user — repeat the cost and get explicit confirmation:
   ```
   mcp__supabase__confirm_cost(type: "project", recurrence: "monthly", amount: <amount>)
   ```

4. **Create the project** — returns a project that takes minutes to initialize:
   ```
   mcp__supabase__create_project(
     name: "my-project",
     region: "us-east-1",
     organization_id: "<org_id>",
     confirm_cost_id: "<cost_id>"
   )
   ```

5. **Check initialization status** by polling:
   ```
   mcp__supabase__get_project(id: "<project_id>")
   ```

### Available Regions

`us-west-1`, `us-east-1`, `us-east-2`, `ca-central-1`, `eu-west-1`, `eu-west-2`, `eu-west-3`, `eu-central-1`, `eu-central-2`, `eu-north-1`, `ap-south-1`, `ap-southeast-1`, `ap-northeast-1`, `ap-northeast-2`, `ap-southeast-2`, `sa-east-1`

Choose the region closest to the application's primary user base.

## Listing and Inspecting Projects

### Via MCP
```
mcp__supabase__list_projects          # All projects
mcp__supabase__get_project(id: "...")  # Single project details
```

### Via CLI
```bash
supabase projects list                # List all projects
supabase link --project-ref <id>      # Link local to remote project
```

## API Keys and URLs

### Retrieving Keys (MCP)

```
mcp__supabase__get_publishable_keys(project_id: "...")
```

Returns both **legacy anon keys** (JWT-based) and **modern publishable keys** (format: `sb_publishable_...`). Modern publishable keys are recommended for new applications due to better security and independent rotation.

**Important:** Only use keys where `disabled` is `false` or undefined.

### Retrieving Project URL (MCP)

```
mcp__supabase__get_project_url(project_id: "...")
```

Returns the API URL: `https://<project-ref>.supabase.co`

### Via CLI

After linking a project, keys and URLs are available via:
```bash
supabase status   # Shows local URLs and keys
```

For remote keys, use the Dashboard or MCP tools.

## Organization Management

### List Organizations (MCP)
```
mcp__supabase__list_organizations
```

### Get Organization Details (MCP)
```
mcp__supabase__get_organization(id: "...")
```
Returns organization details including the subscription plan (Free, Pro, Team, Enterprise).

### Via CLI
```bash
supabase orgs list
```

## Pausing and Restoring Projects

Free-tier projects automatically pause after inactivity. Pro/Team/Enterprise projects can be manually paused.

### Pause (MCP)
```
mcp__supabase__pause_project(project_id: "...")
```

### Restore (MCP)
```
mcp__supabase__restore_project(project_id: "...")
```

Restoring a paused project takes a few minutes. Poll `get_project` to check status.

## Linking Local to Remote

The CLI uses `link` to associate a local project with a remote Supabase project:

```bash
supabase link --project-ref <project-id>
```

The project ID is found in the Dashboard URL: `https://supabase.com/dashboard/project/<project-id>`

After linking:
- `supabase db push` pushes migrations to the linked project
- `supabase db pull` pulls the remote schema
- `supabase functions deploy` deploys to the linked project

## Cost Awareness

Always follow this protocol when creating projects or branches:

1. Call `get_cost` first — never assume costs across organizations
2. Present the cost clearly to the user
3. Wait for explicit confirmation
4. Pass the `confirm_cost_id` to the create operation

This applies to both `create_project` and `create_branch` operations.

## CLI vs MCP Decision Matrix

| Task | Use CLI | Use MCP |
|------|---------|---------|
| Create project | When scripting CI/CD | Interactive Claude Code session |
| List projects | Quick terminal check | When operating on results programmatically |
| Get API keys | `supabase status` (local) | Remote project keys |
| Pause/restore | Not available in CLI | Always use MCP |
| Link project | Always CLI | Not applicable |
| Organization info | `supabase orgs list` | When need subscription details |
