# Archived Plugins

These plugins are paused — they remain in the repository for reference and potential revival, but are **not** listed in the marketplace and will not be installed by anyone browsing `radesjardins/RAD-Claude-Skills`.

## Why archived

Modern frontier coding models (Opus 4.7+) have strong baseline knowledge of these frameworks and languages. The skills here mostly duplicated that baseline knowledge without adding meaningful uplift, and contributed noise to skill selection. Generic "best practices" and "anti-pattern" skills for popular frameworks were the lowest-leverage portion of the toolkit.

The reviewer agents in these plugins were partially redundant with [`rad-code-review`](../plugins/rad-code-review) and [`rad-stack-guide`](../plugins/rad-stack-guide), which orchestrate ship-readiness reviews using a stack-aware approach.

## Archived plugins

| Plugin | Notes |
| --- | --- |
| `rad-astro` | Astro 5/6 standards, a11y, perf, security |
| `rad-fastify` | Fastify encapsulation, hooks, schemas, testing |
| `rad-nextjs` | App Router, RSC, security, testing |
| `rad-react` | React 19 patterns, hooks, security, perf |
| `rad-stripe-fastify-webhooks` | Stripe webhook handling, idempotency, Zod contracts |
| `rad-typescript` | Strict mode, type narrowing, API safety |
| `rad-zod` | Zod v4 schemas, error handling, integrations |

## How to restore one

```bash
# 1. Move it back
git mv archive/plugins/rad-zod plugins/rad-zod

# 2. Re-add its entry to .claude-plugin/marketplace.json
#    (copy the shape of an existing entry — name, source, description, category, homepage, license)

# 3. Bump marketplace version, commit, push.
```

If reviving multiple, consider whether the underlying premise — that frontier models cover this baseline — has changed. If a specific skill turned out to provide unique uplift (e.g., a version-specific migration guide), prefer extracting that single skill rather than reviving the whole plugin.
