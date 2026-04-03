# rad-zod

Expert Zod v4 guidance for TypeScript projects — schema design, validation patterns, security, error handling, and framework integrations.

## Overview

The `rad-zod` plugin provides Claude Code with deep expertise in Zod schema validation. It covers the full lifecycle of Zod usage: architectural placement, schema composition, error handling, security review, Zod v4 migration, and integration with major frameworks (Fastify, Next.js, React Hook Form, tRPC).

## Features

- **6 specialized skills** covering all aspects of Zod development
- **1 autonomous review agent** that audits Zod usage for security issues and anti-patterns
- **Zod v4 focused** — covers breaking changes, new APIs (registries, ZodMini, z.file()), and behavioral changes
- **Security-first** — catches over-posting vulnerabilities, PATCH data-loss bugs, coercion attacks, and PII exposure
- **Framework integration guides** — Fastify type providers, Next.js Server Actions, React Hook Form, monorepo shared schemas

## Skills

| Skill | Triggers On |
|---|---|
| `zod-best-practices` | "how to use Zod", "where should I put Zod", "parse don't validate", "overvalidation" |
| `zod-schema-design` | "composing schemas", "extend pick omit", "transforms", "refinements", "discriminatedUnion" |
| `zod-error-handling` | "parse vs safeParse", "ZodError", "treeifyError", "flattenError", "custom error messages" |
| `zod-security` | "Zod security", "over-posting", "strictObject", "PATCH bug", "z.custom security" |
| `zod-v4-migration` | "Zod 4", "upgrading to Zod 4", "breaking changes", "ZodMini", "z.config", "registries" |
| `zod-integrations` | "Zod with Fastify", "Next.js server actions", "zodResolver", "shared Zod schemas", "monorepo" |

## Agent

**`zod-reviewer`** — Autonomously reviews TypeScript code for Zod anti-patterns, security vulnerabilities, and v4 compatibility issues. Triggers proactively after Zod implementation work is completed, or when explicitly requested.

Checks for:
- `z.object()` vs `z.strictObject()` at API boundaries (over-posting prevention)
- `.default()` + `.partial()` on PATCH schemas (data loss in Zod 4)
- `z.custom()` without validators (validation bypass)
- Raw ZodError exposure to API clients
- Deprecated v4 APIs (`.merge()`, `.email()` chains, `error.format()`)
- Schema definitions inside functions (performance)
- Missing validation at system entry points

## Installation

Install from the marketplace or copy this plugin directory to your `.claude-plugin/` directory.

## Prerequisites

- Zod v4 (`npm install zod`) — this plugin is v4-focused; v3 patterns are covered in the migration skill

## Usage

Skills activate automatically when you discuss Zod-related topics. The `zod-reviewer` agent triggers after completing Zod implementation or when you ask for a review.

To explicitly invoke the reviewer:
> "Review my Zod schemas for security issues"
> "Check my Zod validation before I deploy"
> "I've finished migrating to Zod 4, can you audit it?"

## Key Zod v4 Gotchas This Plugin Helps With

1. **`.default()` + `.partial()` data loss** — In Zod 4, defaults are applied even when fields are absent, corrupting PATCH endpoint logic
2. **Transform runs after failed refine** — Requires `{ abort: true }` to prevent runtime crashes
3. **Registry ID collisions in monorepos** — `.meta({ id })` inside dynamic functions causes crashes in v4.1.13+
4. **`.merge()` deprecation** — Silent in most codebases; should be migrated to `.extend()` or shape spreading
5. **`z.strictObject()` at boundaries** — Default `z.object()` strips unknown keys but doesn't reject them
