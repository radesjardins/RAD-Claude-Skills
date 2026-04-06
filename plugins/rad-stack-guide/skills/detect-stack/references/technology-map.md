# Technology → Plugin Map

This reference maps detectable technologies to rad-* plugins, their development skills, review agents, and CLAUDE.md skill routing patterns.

## Detection Rules

### File-Based Detection

| File Pattern | Technology | Notes |
|---|---|---|
| `astro.config.*` | Astro | .mjs, .ts, .js variants |
| `next.config.*` | Next.js | .mjs, .ts, .js variants |
| `tailwind.config.*` | Tailwind CSS | Also check for `@tailwind` in CSS or `tailwindcss` in deps |
| `tsconfig.json` | TypeScript | Also check `typescript` in devDependencies |
| `wxt.config.*` | WXT | Chrome Extension framework (implies Chrome Extension) |
| `manifest.json` with `manifest_version` | Chrome Extension | Must contain `manifest_version` field to distinguish from other manifest.json files |
| `Dockerfile` or `docker-compose.*` | Docker | Any Dockerfile variant or compose file |

### Dependency-Based Detection (package.json)

Check both `dependencies` and `devDependencies`:

| Dependency Key | Technology |
|---|---|
| `astro` | Astro |
| `next` | Next.js |
| `react` or `react-dom` | React |
| `preact` | Preact |
| `tailwindcss` | Tailwind CSS |
| `fastify` | Fastify |
| `zod` | Zod |
| `stripe` | Stripe |
| `typescript` | TypeScript |
| `electron` | Electron |
| `@supabase/supabase-js` | Supabase |

### Project Type Classification

| Pattern | Project Type |
|---|---|
| Astro + no API server | Website |
| Next.js detected | Web Application |
| React + Vite (no Astro/Next) | Single Page Application |
| Fastify detected (no frontend framework) | API Server |
| Fastify + frontend framework | Full-Stack Application |
| Chrome Extension manifest or WXT | Browser Extension |
| Electron detected | Desktop Application |

**Website** and **Web Application** project types automatically get `rad-seo-optimizer` as a pre-ship plugin and `rad-a11y` as a supporting plugin.

**Any project with UI components** (.tsx, .jsx, .astro files) gets `rad-a11y` as a supporting plugin.

---

## Plugin Mapping

### rad-astro
- **Triggers when:** Astro detected
- **Tier:** Core
- **Development skills:** astro-best-practices, astro-security, astro-performance, astro-accessibility, astro-troubleshooting
- **Review agent:** `astro-reviewer` (subagent_type: `rad-astro:astro-reviewer`)
- **Skill routing pattern:** `*.astro` files, `src/pages/`, `src/layouts/`, `src/components/*.astro`

### rad-nextjs
- **Triggers when:** Next.js detected
- **Tier:** Core
- **Development skills:** nextjs-best-practices, nextjs-security, nextjs-testing, nextjs-troubleshooting
- **Review agent:** `nextjs-reviewer` (subagent_type: `rad-nextjs:nextjs-reviewer`)
- **Skill routing pattern:** `app/` directory, Server Actions, Route Handlers, `middleware.ts`

### rad-react
- **Triggers when:** React detected (not Preact)
- **Tier:** Core when React is the primary UI library; Supporting when used inside Astro or Next.js
- **Development skills:** react-foundations, react-app-building, react-engineering, react-performance, react-accessibility, react-security
- **Review agent:** `react-reviewer` (subagent_type: `rad-react:react-reviewer`)
- **Skill routing pattern:** `*.tsx`, `*.jsx` files containing JSX/React components

### rad-typescript
- **Triggers when:** TypeScript detected
- **Tier:** Supporting (applies broadly to all TypeScript code)
- **Development skills:** typescript-strict-mode, typescript-type-patterns, typescript-api-safety, typescript-error-handling, typescript-modern-features, typescript-anti-patterns
- **Review agent:** `typescript-reviewer` (subagent_type: `rad-typescript:typescript-reviewer`)
- **Skill routing pattern:** `*.ts`, `*.tsx` files, `tsconfig.json`

### rad-fastify
- **Triggers when:** Fastify detected
- **Tier:** Core
- **Development skills:** fastify-best-practices, fastify-hooks-lifecycle, fastify-schemas-validation, fastify-logging, fastify-typescript, fastify-testing, fastify-production, fastify-troubleshooting
- **Review agent:** `fastify-reviewer` (subagent_type: `rad-fastify:fastify-reviewer`)
- **Skill routing pattern:** Route files, plugin files, Fastify hooks, server setup

### rad-zod
- **Triggers when:** Zod detected
- **Tier:** Supporting
- **Development skills:** zod-schema-design, zod-best-practices, zod-error-handling, zod-security, zod-v4-migration, zod-integrations
- **Review agent:** `zod-reviewer` (subagent_type: `rad-zod:zod-reviewer`)
- **Skill routing pattern:** Zod schema files, validation code, API boundary parsing

### rad-chrome-extension
- **Triggers when:** Chrome Extension manifest or WXT detected
- **Tier:** Core
- **Development skills:** chrome-ext-best-practices, chrome-ext-security, chrome-ext-messaging, chrome-ext-service-worker, chrome-ext-storage, chrome-ext-permissions, chrome-ext-testing, chrome-ext-ui-react, chrome-ext-troubleshooting
- **Review agent:** `chrome-ext-reviewer` (subagent_type: `rad-chrome-extension:chrome-ext-reviewer`)
- **Skill routing pattern:** `manifest.json`, content scripts, service worker, messaging, popup/options UI

### rad-a11y
- **Triggers when:** Project has UI components (.tsx, .jsx, .astro files)
- **Tier:** Supporting (during development); Pre-Ship (for review)
- **Development skills:** a11y-review, a11y-semantic-html, a11y-aria-patterns, a11y-keyboard-focus, a11y-forms, a11y-testing
- **Review agent:** `a11y-reviewer` (subagent_type: `rad-a11y:a11y-reviewer`)
- **Skill routing pattern:** Any UI components, ARIA attributes, forms, keyboard/focus code

### rad-stripe-fastify-webhooks
- **Triggers when:** Stripe detected AND Fastify detected
- **Tier:** Core (for webhook-related code)
- **Development skills:** All rad-stripe-fastify-webhooks skills
- **Review agent:** (manual review — no dedicated subagent type)
- **Skill routing pattern:** Stripe webhook handlers, subscription management, billing code

### rad-seo-optimizer
- **Triggers when:** Project type is Website or Web Application
- **Tier:** Pre-Ship
- **Review agent:** `seo-dominator` (subagent_type: `rad-seo-optimizer:seo-dominator`)
- **Skill routing pattern:** N/A (pre-ship review only)

### rad-coolify-orchestrator
- **Triggers when:** Dockerfile or docker-compose detected AND Coolify configuration present
- **Tier:** Supporting
- **Development skills:** coolify-deploy, coolify-databases, coolify-security, coolify-cicd, coolify-troubleshoot, coolify-observability, coolify-infrastructure
- **Review agent:** `coolify-reviewer` (subagent_type: `rad-coolify-orchestrator:coolify-reviewer`)
- **Skill routing pattern:** Dockerfile, docker-compose.yml, CI/CD pipelines, deployment config

### rad-supabase
- **Triggers when:** `@supabase/supabase-js` detected in dependencies
- **Tier:** Supporting
- **Development skills:** supabase-best-practices, supabase-database, supabase-migrations, supabase-edge-functions, supabase-auth, supabase-security, supabase-storage, supabase-realtime, supabase-troubleshooting
- **Review agent:** `supabase-reviewer` (subagent_type: `rad-supabase:supabase-reviewer`)
- **Skill routing pattern:** Supabase client code, RLS policies, edge functions, migration files

### rad-code-review (Final Gate)
- **Triggers when:** Always included in review-for-ship as final gate
- **Tier:** Final Gate (runs after all specialist reviewers)
- **Scope:** AI slop detection, architecture, release readiness, general security, documentation, dependency audit
- **Invocation:** Skill tool (not Agent subagent_type) — invoke `rad-code-review`
- **Note:** This is a standalone skill, not a plugin agent. It runs as the generalist complement to the specialist reviewer agents.

---

## Skill Routing Patterns for CLAUDE.md

When generating the CLAUDE.md `## Stack Guidance` section, use these templates to create routing rules. Only include rules for detected technologies:

| Technology | CLAUDE.md Routing Rule |
|---|---|
| React | `**React components** (*.tsx, *.jsx with JSX): use rad-react skills (react-foundations, react-performance, react-security)` |
| Next.js | `**Next.js patterns** (app/ directory, Server Actions, Route Handlers): use rad-nextjs skills (nextjs-best-practices, nextjs-security)` |
| TypeScript | `**TypeScript code** (*.ts, *.tsx): use rad-typescript skills (typescript-strict-mode, typescript-api-safety)` |
| Fastify | `**Fastify server code** (routes, plugins, hooks): use rad-fastify skills (fastify-best-practices, fastify-schemas-validation)` |
| Astro | `**Astro pages and components** (*.astro, src/pages/): use rad-astro skills (astro-best-practices, astro-performance)` |
| Accessibility | `**Accessibility** (any UI components, ARIA, forms, keyboard): use rad-a11y skills (a11y-semantic-html, a11y-aria-patterns)` |
| Chrome Extension | `**Chrome Extension** (manifest, content scripts, service worker): use rad-chrome-extension skills (chrome-ext-best-practices, chrome-ext-security)` |
| Zod | `**Zod schemas** (validation, parsing, type inference): use rad-zod skills (zod-schema-design, zod-security)` |
| Supabase | `**Supabase** (database, auth, RLS, edge functions, storage): use rad-supabase skills (supabase-best-practices, supabase-security)` |
| Coolify | `**Deployment** (Dockerfile, compose, CI/CD): use rad-coolify-orchestrator skills (coolify-deploy, coolify-security)` |

---

## Tier Definitions

| Tier | When to Use | Impact on Workflow |
|---|---|---|
| **Core** | Always consult during development in this project | Loaded when working on related code |
| **Supporting** | Consult when touching relevant code | Referenced as needed |
| **Pre-Ship** | Run before deploying or merging | Dispatched by `/review-for-ship` |
| **Final Gate** | Always runs last in `/review-for-ship` | rad-code-review provides the ship/no-ship verdict |
