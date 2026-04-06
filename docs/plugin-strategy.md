# Plugin Strategy & Portfolio Assessment

> Last reviewed: 2026-04-03

## The Test Every Plugin Must Pass

> **"Does Claude give meaningfully worse advice without this plugin than with it, at the moment it fires?"**

Strong plugins share three traits:
1. Claude behaves **noticeably** worse without them — not marginally
2. The domain is **specific enough** that training data is thin or inconsistent
3. There is a **clear, natural trigger moment** — you're in a specific file type, using a specific tool, or starting a specific workflow

Weak plugins tend to cover broad domains where Claude already has dense training data, or fire on keyword matches that don't correspond to a moment where guidance actually changes what gets written.

---

## Ranked Plugin Assessment

### Tier 1 — Keep, High Confidence

These pass the test clearly. Claude behaves meaningfully differently with them.

| Plugin | Why it earns its place |
|---|---|
| `rad-code-review` | Orchestrated multi-phase review with severity ranking, fix application, and history comparison. Structurally better than asking Claude to "review my code." One of the strongest tools in the library. |
| `rad-stripe-fastify-webhooks` | Best example in the library. Extremely niche, Claude has no training depth on this specific combination. Subscription state machines, idempotent event processing — genuinely changes what gets produced. |
| `rad-google-workspace` | Different category: enables capability that doesn't exist without it. Claude cannot use the `gws` CLI at all without these skills. Operational, not educational. |
| `rad-typescript` | Claude defaults to `any`, inconsistent strict patterns. Plugin enforces zero-any, discriminated unions, parse-don't-validate. Real, measurable behavior change. |
| `rad-react` | React 19 patterns, IDOR in Server Actions, hooks rules — Claude is inconsistent without it. The security content alone justifies it. |
| `rad-fastify` | Encapsulation model and plugin DAG are misapplied constantly without guidance. Claude writes Fastify like Express without this. |
| `rad-a11y` | Claude produces inaccessible code at a high rate. This genuinely changes output quality. WCAG 2.2 AA content is specific enough that training is inconsistent. |
| `rad-chrome-extension` | Claude writes MV2 patterns for MV3 projects without guidance. Very recent spec changes, complex CSP requirements. Clear niche. |
| `rad-brainstormer` | Process scaffolding, not knowledge. Claude brainstorms without structure; this enforces methodology (SCAMPER, Six Hats, etc.). The value is workflow. |
| `rad-context-prompter` | Prompt engineering is genuinely specialized and Claude writes mediocre prompts without guidance. Meta-value — helps Claude help you better. |

### Tier 2 — Keep, Conditional

The differentiator is specific and recent. Value fades as model training catches up, or depends on a subset of the plugin's content.

| Plugin | Keep because | Watch for |
|---|---|---|
| `rad-nextjs` | App Router patterns are recent enough that training is thin. Server/Client boundaries, caching behavior, auth patterns. | Value fades as Claude's Next.js training improves. Revisit annually. |
| `rad-astro` | Specialized enough framework (Islands architecture, Content Layer v2, Astro Actions) to earn its place, similar to rad-fastify. | Smaller audience than React/Next.js. |
| `rad-zod` | v4 is recent, training data is thin for the new API. Integration patterns with Fastify and react-hook-form are specific. | Without v4 differentiator, Claude knows Zod adequately. Keep updated. |
| `rad-seo-optimizer` | AEO/GEO optimization angle is genuinely recent and not well-covered in training. | Standard SEO content Claude already knows well. Value lives in the AEO/AI-search layer only. |
| `rad-agentic-company-builder` | Very niche, tuned to a specific workflow and "Agentic Bible" content that isn't general knowledge. | Audience is narrow — primarily useful to you personally. |

### Tier 3 — Marginal, Monitor

| Plugin | Honest assessment | Status |
|---|---|---|
| `rad-para-second-brain` | Retained as a personal workflow utility for managing PARA folder structure within specific projects, not a general marketplace skill. | **Keep as personal tool** |
| `rad-stack-detect` | Meta-value only — as good as the plugins it routes to. | **Monitor** — if it reliably fires the right plugins it earns its place; if noisy, remove it. |

### Tier 4 — Retired (2026-04-03)

Removed from repo and marketplace. Claude gives equivalent or better advice without them, content well-covered in training data, or marginal improvement over direct prompting.

| Plugin | Why retired |
|---|---|
| `rad-tailwind` | General Tailwind advice well-covered in Claude's training. Only differentiator was v4 migration content — too thin to justify a full plugin. |
| `rad-docker` | Multi-stage builds, non-root execution, BuildKit secrets — Claude knows this adequately. Superseded by `rad-coolify` when built. |
| `rad-gem-creator` | Niche use case, marginal execution improvement over asking Claude directly. |
| `rad-gpt-creator` | Same as gem-creator — convenience tool, not a quality multiplier. |

### Tier 5 — Do Not Build

| Plugin | Why |
|---|---|
| `rad-testing` *(proposed)* | JS/TS testing ecosystem is well-documented. Claude knows Vitest and Playwright adequately. The genuinely unique insight (test strategy evaluation) doesn't fit the skill format. The reviewer agent would be outclassed by `rad-code-review`. Testing questions arrive embedded in framework context, so the wrong skill loads or none does. **Skip.** |

---

## What Makes a Plugin Worth Building

Based on the patterns in Tier 1:

```
High value = Specific domain + Thin training data + Clear trigger moment
           + Claude's default behavior is noticeably wrong without it
```

The sweet spot is **niche + operational + recent**:
- **Niche**: Not broad "best practices" — a specific tool, stack combination, or workflow
- **Operational**: Enables something (like gws CLI) rather than just improving something
- **Recent**: Post-training-cutoff APIs, frameworks, or patterns where Claude's defaults are stale

---

## New Plugin Suggestions

Ranked by estimated value / likelihood of passing the test:

### 1. `rad-coolify` — Highest Priority

**Why it would pass the test:** Claude has essentially no training on Coolify. It's a self-hosted deployment platform with its own conventions, service types, environment management, and Traefik configuration. Without a plugin, Claude gives generic Docker Compose advice that doesn't map to how Coolify actually works.

**Profile:** Same value category as `rad-google-workspace` — operational, enables capability that doesn't exist without it.

**Notebook available:** Yes — "Coolify Deployment and Orchestration Guide" (2026-03-29)

**Trigger:** Clear — whenever working with Coolify deployments, `coolify.yaml`, service configs

**Scope:** Service creation, environment variables, persistent storage, custom domains, Traefik config, GitHub Actions integration, database services, one-click apps

---

### 2. `rad-local-ai` — High Priority

**Why it would pass the test:** MCP server configuration, Ollama integration, local model routing, tool definitions for local inference — Claude knows this in fragments but not coherently. The space is evolving fast enough that training data is spotty. This is recent, specific, and Claude's defaults are inconsistent.

**Profile:** Similar to rad-context-prompter — meta value, helps you build better AI-powered tooling.

**Notebook available:** Yes — "Integrating Local AI Tools for Software Development" (2026-03-31)

**Trigger:** Working with Ollama, building MCP servers, configuring local model inference, setting up AI-assisted dev tooling

**Scope:** Ollama setup and model selection, MCP server patterns, local vs. API model routing, tool definitions, prompt caching for local inference, dev workflow integration

---

### 3. `rad-offline-first` — Medium-High Priority

**Why it would pass the test:** Offline-first architecture patterns (sync engines, conflict resolution, CRDT basics, local-first data) are specialized enough that Claude gives generic advice without guidance. The combination of Electron + SQLite + sync is exactly the kind of specific stack where training data is thin.

**Profile:** Similar to rad-fastify — specialized architectural patterns that Claude routinely gets wrong without guidance.

**Notebook available:** Yes — "Architecting Offline-First Desktop and Mobile Applications" (2026-03-31)

**Trigger:** Working with Electron, Tauri, React Native with offline requirements, sync engines, conflict resolution, local-first architecture

**Scope:** Sync architecture patterns, conflict resolution strategies, CRDT basics, SQLite in Electron, background sync, network state management, optimistic UI patterns

---

### 4. `rad-saas` — Medium Priority

**Why it might pass the test:** Multi-tenancy patterns, billing integration, trial/subscription state machines, entitlement logic — generic advice is common but opinionated patterns that prevent real mistakes are not.

**Profile:** Overlaps with rad-stripe-fastify-webhooks. Could extend that plugin rather than creating a new one, or scope to the patterns that plugin doesn't cover (tenant isolation, feature flags, usage metering).

**Notebook available:** Yes — "Modern SaaS Applications" (2026-03-29)

**Caution:** Risk of being too broad. Only worth building if scoped to patterns Claude genuinely gets wrong — tenant data isolation, subscription state edge cases, usage-based billing architecture.

---

## Plugins to Retire or Collapse

| Action | Plugin | Replacement |
|---|---|---|
| Collapse to 1 skill | `rad-tailwind` | Keep only `tailwind-v4-migration` skill; remove or consolidate the rest |
| Replace | `rad-docker` | If Docker guidance is needed, incorporate into `rad-coolify` as deployment context |
| Keep as personal utility only | `rad-para-second-brain` | Not marketplace-worthy; fine as a personal tool |
| Evaluate usage before deciding | `rad-gem-creator`, `rad-gpt-creator` | If used less than once a month, not worth maintaining |

---

## Summary

**Active — keep as-is (10):** rad-code-review, rad-stripe-fastify-webhooks, rad-google-workspace, rad-typescript, rad-react, rad-fastify, rad-a11y, rad-chrome-extension, rad-brainstormer, rad-context-prompter

**Active — monitor/update (5):** rad-nextjs, rad-astro, rad-zod, rad-seo-optimizer, rad-agentic-company-builder

**Active — personal tool only (1):** rad-para-second-brain

**Monitor (1):** rad-stack-detect

**Retired (4):** ~~rad-tailwind~~, ~~rad-docker~~, ~~rad-gem-creator~~, ~~rad-gpt-creator~~

**Do not build (1):** rad-testing

**Build next, in priority order (4):** rad-coolify → rad-local-ai → rad-offline-first → rad-saas
