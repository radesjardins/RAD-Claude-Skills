# rad-typescript — Production TypeScript. Not the TypeScript Claude defaults to.

Claude writes TypeScript. Without guardrails, it defaults to loose patterns — `any` types, unsafe casts, missing null checks, and API boundaries that trust external data too much. rad-typescript enforces strict mode, catches the 14 anti-patterns that AI code generators introduce most often, and ensures your API endpoints safely handle data from the outside world.

## What You Can Do With This

- Write TypeScript that passes strict mode without fighting the compiler
- Catch AI-generated anti-patterns before they reach production: `as any`, non-null assertions, missing discriminated unions
- Design API boundaries that safely validate and type external data (HTTP requests, webhooks, third-party APIs)
- Handle errors with typed Result patterns instead of untyped catch blocks

## How It Works

| Skill | Purpose |
|-------|---------|
| `typescript-strict-mode` | tsconfig.json, strict flags, compiler options |
| `typescript-type-patterns` | Union types, type guards, discriminated unions, mapped types |
| `typescript-api-safety` | API boundary safety, external data validation, HTTP request typing |
| `typescript-error-handling` | Result types, typed errors, try/catch patterns |
| `typescript-anti-patterns` | 14 AI codegen anti-patterns — detection and fixes |
| `typescript-modern-features` | TypeScript 4.9–5.7 features: `satisfies`, const type params, `using` |

| Agent | Purpose |
|-------|---------|
| `typescript-reviewer` | Audits TypeScript against strict-mode standards and AI anti-pattern checklist |

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-typescript
```

```
Review my TypeScript for production readiness
Check this for TypeScript anti-patterns
Is my API boundary safe?
```

## License
Apache-2.0
