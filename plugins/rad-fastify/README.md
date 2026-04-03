# rad-fastify

Comprehensive Fastify framework coding standards, architectural guidance, and anti-pattern enforcement for Claude Code.

Built from curated sources including official Fastify documentation, Node.js production best practices, and real-world case studies.

## Skills

| Skill | Purpose |
|-------|---------|
| `fastify-best-practices` | Core architecture: encapsulation model, plugin DAG, decorators, project organization |
| `fastify-hooks-lifecycle` | Complete hook lifecycle reference with execution order, constraints, and rules |
| `fastify-schemas-validation` | JSON Schema validation (Ajv), response serialization (fast-json-stringify), shared schemas |
| `fastify-logging` | Pino configuration, child loggers, redaction, async transports, crash handling |
| `fastify-typescript` | Type providers, declaration merging, typing plugins and routes |
| `fastify-testing` | In-process testing with .inject(), app/server separation, plugin isolation |
| `fastify-production` | Security hardening, graceful shutdown, reverse proxy, deployment checklist |
| `fastify-troubleshooting` | Anti-patterns, common mistakes, diagnosis table, debugging patterns |

## Agents

| Agent | Purpose |
|-------|---------|
| `fastify-reviewer` | Autonomous code review for Fastify anti-patterns, encapsulation violations, and production readiness |

## What This Plugin Enforces

### Hard Rules (Never Violate)

- Never use reference types in `decorateRequest`/`decorateReply`
- Never mix async/await with done callbacks in hooks
- Never use arrow functions for decorators or hooks
- Never expose Fastify directly to the internet (use reverse proxy)
- Never pass user-provided schemas (code execution vulnerability)
- Never use `allErrors: true` in production Ajv config
- Always define response schemas for serialization performance
- Always separate app registration from server listening
- Always use `return reply` after `reply.send()` in async hooks

### Architecture Principles

- Everything is a plugin — the app is a tree of encapsulated contexts
- Schema-first: define explicit JSON Schema contracts for all routes
- Fail fast: reject invalid data before business logic executes
- Deterministic lifecycle: plugins load in registration order via avvio

## Installation

```bash
claude /install-plugin C:/Dev/rad-skills-repo/plugins/rad-fastify
```

Or add to your project's `.claude/settings.json`:

```json
{
  "plugins": ["C:/Dev/rad-skills-repo/plugins/rad-fastify"]
}
```

## Usage

Skills activate automatically when working on Fastify projects. The agent can be invoked with:

- "Review my Fastify code"
- "Check for Fastify anti-patterns"
- "Is my Fastify app production ready?"

## Author

RAD
