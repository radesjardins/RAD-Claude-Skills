# MCP Server Configurations

Complete configuration blocks for each supported integration.

---

## GitHub (Official Remote Server — Recommended)

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PAT}"
      }
    }
  }
}
```

**CLI setup:**
```bash
claude mcp add-json github '{
  "type": "http",
  "url": "https://api.githubcopilot.com/mcp/",
  "headers": { "Authorization": "Bearer ${GITHUB_PAT}" }
}' --scope user
```

**PAT requirements (fine-grained):**
- Contents: Read & Write
- Pull requests: Read & Write
- Issues: Read & Write
- Actions: Read & Write
- Metadata: Read

**Toolset selection via env:**
```
GITHUB_TOOLSETS=repos,issues,pull_requests,actions,code_security
```

---

## GitHub (Docker-based Local Server — Alternative)

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "-e", "GITHUB_TOOLSETS=repos,issues,pull_requests,actions",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PAT}"
      }
    }
  }
}
```

---

## Coolify Deployment Control

```json
{
  "mcpServers": {
    "coolify": {
      "command": "npx",
      "args": ["-y", "@masonator/coolify-mcp"],
      "env": {
        "COOLIFY_ACCESS_TOKEN": "${COOLIFY_ACCESS_TOKEN}",
        "COOLIFY_BASE_URL": "${COOLIFY_BASE_URL}"
      }
    }
  }
}
```

**CLI setup:**
```bash
claude mcp add coolify -s user \
  -e COOLIFY_ACCESS_TOKEN=$COOLIFY_TOKEN \
  -e COOLIFY_BASE_URL=https://coolify.example.com \
  -- npx -y @masonator/coolify-mcp
```

**Token setup:** Coolify dashboard -> Keys & Tokens -> API Tokens -> Create New Token.

---

## PostgreSQL (Production — Read-Only)

```json
{
  "mcpServers": {
    "db-production": {
      "command": "uvx",
      "args": ["postgres-mcp", "--access-mode=restricted"],
      "env": {
        "DATABASE_URI": "${PRODUCTION_DATABASE_URI}"
      }
    }
  }
}
```

**With SSH tunnel (requires separate tunnel process):**
```bash
ssh -N -L 5433:localhost:5432 deploy@your-server-ip
```
Then use `postgresql://user:pass@localhost:5433/dbname` in DATABASE_URI.

**Alternative with built-in SSH tunneling:**
```json
{
  "mcpServers": {
    "db-production": {
      "command": "npx",
      "args": ["-y", "@zlash65/postgresql-ssh-mcp"],
      "env": {
        "DATABASE_URI": "${PRODUCTION_DATABASE_URI}",
        "SSH_ENABLED": "true",
        "SSH_HOST": "${SSH_HOST}",
        "SSH_USER": "${SSH_USER}",
        "SSH_PRIVATE_KEY_PATH": "~/.ssh/deploy_key"
      }
    }
  }
}
```

---

## PostgreSQL (Development — Read/Write)

```json
{
  "mcpServers": {
    "db-dev": {
      "command": "uvx",
      "args": ["postgres-mcp", "--access-mode=unrestricted"],
      "env": {
        "DATABASE_URI": "${DEV_DATABASE_URI}"
      }
    }
  }
}
```

---

## Prisma ORM

```json
{
  "mcpServers": {
    "prisma": {
      "command": "npx",
      "args": ["-y", "prisma", "mcp"]
    }
  }
}
```

Exposes: migrate-status, migrate-dev, migrate-reset, Prisma Postgres management.

---

## Google Workspace (Comprehensive)

```json
{
  "mcpServers": {
    "google-workspace": {
      "command": "uvx",
      "args": ["workspace-mcp", "--tools", "gmail", "drive", "calendar", "docs", "sheets"]
    }
  }
}
```

**CLI setup:**
```bash
claude mcp add google-workspace -- uvx workspace-mcp --tool-tier core
```

**OAuth2 setup required:**
1. Google Cloud Console -> Create project
2. Enable APIs: Drive, Gmail, Calendar, Docs, Sheets
3. OAuth consent screen -> Add test user
4. Create OAuth client (Desktop app) -> Download JSON
5. Save as `~/.config/google/gcp-oauth.keys.json`
6. First run opens browser for consent

---

## Google Calendar (Standalone)

```json
{
  "mcpServers": {
    "google-calendar": {
      "command": "npx",
      "args": ["@cocal/google-calendar-mcp"],
      "env": {
        "GOOGLE_OAUTH_CREDENTIALS": "${GOOGLE_OAUTH_CREDENTIALS_PATH}"
      }
    }
  }
}
```

---

## Docker (Local)

```json
{
  "mcpServers": {
    "docker": {
      "command": "uvx",
      "args": ["mcp-server-docker"]
    }
  }
}
```

---

## Docker (Remote via SSH)

```json
{
  "mcpServers": {
    "docker-remote": {
      "command": "uvx",
      "args": ["mcp-server-docker"],
      "env": {
        "DOCKER_HOST": "ssh://deploy@${VPS_IP}"
      }
    }
  }
}
```

---

## Playwright Browser Automation

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

---

## SSH Remote Access

```json
{
  "mcpServers": {
    "vps-ssh": {
      "command": "npx",
      "args": [
        "ssh-mcp", "-y", "--",
        "--host=${SSH_HOST}",
        "--port=22",
        "--user=${SSH_USER}",
        "--key=${SSH_KEY_PATH}",
        "--timeout=30000"
      ]
    }
  }
}
```

---

## Complete Unified Configuration Example

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PAT}"
      }
    },
    "coolify": {
      "command": "npx",
      "args": ["-y", "@masonator/coolify-mcp"],
      "env": {
        "COOLIFY_ACCESS_TOKEN": "${COOLIFY_ACCESS_TOKEN}",
        "COOLIFY_BASE_URL": "${COOLIFY_BASE_URL}"
      }
    },
    "db": {
      "command": "uvx",
      "args": ["postgres-mcp", "--access-mode=restricted"],
      "env": {
        "DATABASE_URI": "${DATABASE_URI}"
      }
    },
    "prisma": {
      "command": "npx",
      "args": ["-y", "prisma", "mcp"]
    },
    "google-workspace": {
      "command": "uvx",
      "args": ["workspace-mcp", "--tools", "gmail", "drive", "calendar"]
    },
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

**Critical:** Store all secrets in environment variables. Never hardcode in `.mcp.json`.

---

## Verification Prompts

After configuring, test each server:

| Integration | Test Prompt |
|-------------|-------------|
| GitHub | "List the 5 most recent commits in the repo" |
| Coolify | "Show all applications and their deployment status" |
| PostgreSQL | "List all tables and their row counts" |
| Prisma | "Check the current migration status" |
| Google Calendar | "Show my calendar events for today" |
| Gmail | "Search for the most recent 3 emails" |
| Playwright | "Navigate to the app URL and take a screenshot" |
| Docker | "List running containers" |
