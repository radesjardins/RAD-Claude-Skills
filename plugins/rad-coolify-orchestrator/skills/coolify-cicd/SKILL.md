---
name: coolify-cicd
description: >
  This skill should be used when setting up CI/CD pipelines for Coolify, using the Coolify REST
  API, triggering deployments from GitHub Actions, configuring webhooks, deploying from GHCR or
  other registries, setting up PR preview environments, configuring branch-specific deployments,
  using the Coolify deploy webhook, integrating GitLab CI with Coolify, or managing API tokens.
  Trigger when: "Coolify CI/CD", "Coolify API", "deploy to Coolify from GitHub Actions",
  "Coolify webhook", "Coolify deploy trigger", "Coolify API token", "GHCR deploy Coolify",
  "Coolify PR preview", "Coolify branch deploy", "action-coolify", "GitLab CI Coolify",
  "Coolify REST API", "automate Coolify deployment".
---

# Coolify CI/CD

Covers the Coolify REST API, GitHub Actions integration, GHCR workflows, webhooks, and PR preview environments for Coolify v4 self-hosted.

> **Self-Hosted Only**: All content assumes self-hosted Coolify v4.x. API endpoints and webhook behavior may differ on Coolify Cloud.

## Deployment Trigger Methods

| Method | Best For | Complexity |
|--------|----------|------------|
| **Git Push (Auto-deploy)** | Simple projects, Coolify builds from source | Lowest |
| **Deploy Webhook URL** | Quick integration, no API token needed | Low |
| **REST API** | Full control, multi-step pipelines | Medium |
| **GitHub Actions + API** | Enterprise CI/CD with tests before deploy | Medium |
| **GHCR + API** | Build externally, deploy pre-built images | Higher |

Choose based on your build pipeline: if Coolify builds from source, use Git Push or Webhook. If CI builds the image, use GHCR + API. If neither fits, use the REST API directly for full control.

## REST API

### Authentication

All API requests require a Bearer token:
```bash
curl -H "Authorization: Bearer <YOUR_API_TOKEN>" \
     "https://<COOLIFY_FQDN>/api/v1/..."
```

Generate tokens in **Coolify UI → Security → API Tokens**. Tokens are team-scoped — they grant access to all resources within the team.

### Core Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/v1/applications` | List all applications |
| `GET` | `/api/v1/applications/{uuid}` | Get application details |
| `PATCH` | `/api/v1/applications/{uuid}` | Update application settings |
| `POST` | `/api/v1/applications/{uuid}/deploy` | Trigger deployment |
| `POST` | `/api/v1/applications/{uuid}/restart` | Restart application |
| `POST` | `/api/v1/applications/{uuid}/stop` | Stop application |
| `GET` | `/api/v1/applications/{uuid}/deployments` | List deployments |
| `GET` | `/api/v1/servers` | List servers |
| `GET` | `/api/v1/teams` | List teams |
| `GET` | `/api/v1/projects` | List projects |

### Trigger a Deployment

```bash
# Basic deploy (note: GET method, not POST)
curl "https://<COOLIFY_FQDN>/api/v1/deploy?uuid=<APP_UUID>" \
  -H "Authorization: Bearer <YOUR_API_TOKEN>"

# With optional parameters
curl "https://<COOLIFY_FQDN>/api/v1/deploy?uuid=<APP_UUID>&force=true" \
  -H "Authorization: Bearer <YOUR_API_TOKEN>"

# Response (async — returns deployment job)
{
  "deployments": [
    {
      "message": "Deployment request queued.",
      "resource_uuid": "app-xxxx",
      "deployment_uuid": "dep-xxxx-xxxx"
    }
  ]
}
```

**Parameters**: `uuid` (resource UUID, comma-separated for batch), `tag` (tag name), `force` (boolean, skip cache), `pr` (PR number for preview deploys).

### Check Deployment Status

```bash
curl -s "https://<COOLIFY_FQDN>/api/v1/deployments/<DEPLOYMENT_UUID>" \
  -H "Authorization: Bearer <TOKEN>" | jq '.status'

# Status values: queued, in_progress, finished, failed, cancelled
```

### Get Application Logs

```bash
curl -s "https://<COOLIFY_FQDN>/api/v1/applications/<APP_UUID>/logs?lines=100" \
  -H "Authorization: Bearer <TOKEN>"
```

### Update Application Settings

```bash
# Update image tag for pre-built image deployments
curl -X PATCH "https://<COOLIFY_FQDN>/api/v1/applications/<APP_UUID>" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "docker_registry_image_tag": "v1.2.3"
  }'
```

## Deploy Webhook URL

Each application has a unique webhook URL (found in **Application → Webhooks** tab):

```
https://<COOLIFY_FQDN>/api/v1/deploy?uuid=<APP_UUID>&token=<WEBHOOK_TOKEN>
```

Trigger with a simple GET (auth via Bearer token or webhook-specific token):
```bash
curl "https://<COOLIFY_FQDN>/api/v1/deploy?uuid=<APP_UUID>" \
  -H "Authorization: Bearer <YOUR_API_TOKEN>"
```

**Webhook vs API**: The webhook URL is simpler (no auth header), but offers less control. Use the API for updating settings before deploy, checking status, or complex workflows.

## GitHub Actions Integration

### Basic Deploy on Push

```yaml
name: Deploy to Coolify
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Coolify Deployment
        run: |
          curl --request GET \
            "${{ secrets.COOLIFY_WEBHOOK }}" \
            -H "Authorization: Bearer ${{ secrets.COOLIFY_API_TOKEN }}" \
            --fail --silent --show-error
```

### Required GitHub Secrets

| Secret | Value | Example |
|--------|-------|---------|
| `COOLIFY_WEBHOOK` | Deploy webhook URL from app's Webhook page | `https://coolify.example.com/api/v1/deploy?uuid=app-xxxx` |
| `COOLIFY_API_TOKEN` | API token from Keys & Tokens → API Tokens | `token with "Deploy" permission` |
| `COOLIFY_URL` | Coolify instance URL (for API calls) | `https://coolify.example.com` |

### Deploy After Tests Pass

```yaml
name: Test and Deploy
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm test

  deploy:
    needs: test    # Only runs if tests pass
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Coolify
        run: |
          curl -X POST \
            "${{ secrets.COOLIFY_URL }}/api/v1/applications/${{ secrets.COOLIFY_APP_UUID }}/deploy" \
            -H "Authorization: Bearer ${{ secrets.COOLIFY_API_TOKEN }}" \
            --fail --silent --show-error
```

### Multi-Environment (Staging + Production)

```yaml
name: Deploy Pipeline
on:
  push:
    branches: [main, develop]

jobs:
  deploy-staging:
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Staging
        run: |
          curl -X POST \
            "${{ secrets.COOLIFY_URL }}/api/v1/applications/${{ secrets.COOLIFY_STAGING_UUID }}/deploy" \
            -H "Authorization: Bearer ${{ secrets.COOLIFY_API_TOKEN }}" --fail

  deploy-production:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production    # Requires approval if configured
    steps:
      - name: Deploy to Production
        run: |
          curl -X POST \
            "${{ secrets.COOLIFY_URL }}/api/v1/applications/${{ secrets.COOLIFY_PROD_UUID }}/deploy" \
            -H "Authorization: Bearer ${{ secrets.COOLIFY_API_TOKEN }}" --fail
```

## GHCR Pattern (Full Pipeline)

Build in GitHub Actions → push to GHCR → trigger Coolify to deploy the image:

```yaml
name: Build, Push, Deploy
on:
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-push-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

      - name: Update image tag in Coolify
        run: |
          curl -X PATCH \
            "${{ secrets.COOLIFY_URL }}/api/v1/applications/${{ secrets.COOLIFY_APP_UUID }}" \
            -H "Authorization: Bearer ${{ secrets.COOLIFY_API_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d '{"docker_registry_image_tag": "${{ github.sha }}"}'

      - name: Trigger deployment
        run: |
          curl -X POST \
            "${{ secrets.COOLIFY_URL }}/api/v1/applications/${{ secrets.COOLIFY_APP_UUID }}/deploy" \
            -H "Authorization: Bearer ${{ secrets.COOLIFY_API_TOKEN }}" --fail
```

## Webhooks and Auto-Deploy

### Git Provider Webhooks

Coolify can auto-deploy when it detects a push to the configured branch:

1. **Application → General → Git Repository** — configure the repo and branch
2. Enable **Auto Deploy** — Coolify registers a webhook with the git provider
3. On push to the configured branch, Coolify triggers a build and deploy automatically

### Branch-Specific Rules

- Each Coolify application is configured for one branch
- For multiple branches (staging, production), create separate Coolify applications pointing to different branches
- Use the same repo, different branch configuration per application

### PR Preview Environments

Coolify supports preview deployments for pull requests:

1. Enable **Preview Deployments** in the application settings
2. When a PR is opened against the configured branch, Coolify creates a temporary deployment
3. The preview gets its own subdomain (e.g., `pr-123.preview.example.com`)
4. When the PR is merged or closed, the preview environment is automatically destroyed

**Limitations**:
- Preview environments share the server resources with production
- Each preview creates a new container (resource-heavy for many concurrent PRs)
- Database-dependent apps need a strategy for preview databases
- Environment variables are inherited from the main application

## Anti-Patterns

| Anti-Pattern | Consequence |
|-------------|-------------|
| Using the same API token for all environments | Staging pipeline can accidentally deploy to production |
| Not using `--fail` flag in curl deploy commands | CI/CD pipeline reports success even when deploy fails |
| Hardcoding Coolify URL or UUID in workflow files | Breaks when migrating Coolify or recreating apps |
| Polling deployment status in a tight loop | Wastes API rate limits; use reasonable intervals (10-15s) |
| Deploying without running tests first | Broken code reaches production |
| Using webhook URL in public repos | Anyone can trigger your deployments |
| Not pinning image tags in production | `latest` tag means non-deterministic deployments |
| Skipping the PATCH step in GHCR workflows | Coolify deploys the old image tag, not the new one |

## Related Skills

- **coolify-deploy** — Build pack selection, deployment configuration, rollbacks
- **coolify-security** — API token management, webhook security
- **coolify-troubleshoot** — Debugging failed deployments

## Additional Resources

### Reference Files

- **`references/api-reference.md`** — Full Coolify API v1 endpoint reference with request/response shapes
- **`references/gitlab-ci-pattern.md`** — GitLab CI integration pattern for Coolify
