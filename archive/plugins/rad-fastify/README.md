# rad-fastify — Fastify the way Fastify was designed. Encapsulation, schemas, hooks, and production patterns.

Fastify's power comes from its encapsulation model and hook lifecycle — but they're also where most mistakes happen. rad-fastify keeps Claude aligned with Fastify's actual design philosophy: proper plugin scoping, JSON Schema validation on every route, Pino logging configured correctly, and TypeScript type providers that don't leak types across scope boundaries.

## What You Can Do With This

- Structure a Fastify app with correct plugin scoping — no accidental decoration leaks
- Add JSON Schema validation to route inputs and outputs for both safety and serialization speed
- Configure structured logging with Pino redaction so sensitive fields never appear in logs
- Review a Fastify codebase for anti-patterns before shipping

## How It Works

| Skill | Purpose |
|-------|---------|
| `fastify-best-practices` | Architecture, plugin encapsulation, project structure |
| `fastify-hooks-lifecycle` | Hook execution order, onRequest/preParsing/preValidation/onSend |
| `fastify-schemas-validation` | JSON Schema, Ajv, fast-json-stringify serialization |
| `fastify-logging` | Pino configuration, child loggers, log redaction |
| `fastify-typescript` | Type providers, @fastify/type-provider-typebox |
| `fastify-production` | Security headers, reverse proxy config, graceful shutdown |
| `fastify-testing` | .inject() HTTP testing, unit tests, integration patterns |
| `fastify-troubleshooting` | Anti-patterns, common mistakes, diagnostic patterns |

| Agent | Purpose |
|-------|---------|
| `fastify-reviewer` | Reviews Fastify code for encapsulation violations, anti-patterns, and production readiness |

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-fastify
```

```
Review my Fastify code
Is my Fastify app production ready?
Check for Fastify anti-patterns
```

## License
Apache-2.0
