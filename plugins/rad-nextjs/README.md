# rad-nextjs — Next.js App Router done right. Server/client boundaries, auth, caching, and security.

The App Router changed how Next.js works at a fundamental level — and Claude's training data includes a lot of Pages Router patterns that silently break things. rad-nextjs keeps Claude aligned with App Router conventions: correct server/client component boundaries, safe Server Actions, data fetching that doesn't over-cache or under-secure, and IDOR prevention built into every route handler.

## What You Can Do With This

- Write Server Actions that verify auth before mutating data (not after)
- Get route handlers and API endpoints with IDOR protection built in
- Fix hydration errors and client/server boundary mistakes
- Set up testing for App Router components with the correct Vitest/Cypress patterns

## How It Works

| Skill | Purpose |
|-------|---------|
| `nextjs-best-practices` | App Router conventions, server/client boundaries, data fetching, caching |
| `nextjs-security` | IDOR prevention, Server Action auth, CSP, input validation |
| `nextjs-testing` | Vitest, Cypress, Testing Library for App Router |
| `nextjs-troubleshooting` | Hydration errors, boundary mistakes, caching bugs |

| Agent | Purpose |
|-------|---------|
| `nextjs-reviewer` | Reviews Next.js code for App Router violations, security issues, and performance anti-patterns |

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-nextjs
```

```
Review my Next.js code
Is my Server Action secure?
Fix this hydration error
Check my route handlers for IDOR
```

## License
Apache-2.0
