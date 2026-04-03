# Technology → Plugin Map

This reference maps detectable technologies to rad-* plugins, their development skills, and review agents.

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

### rad-nextjs
- **Triggers when:** Next.js detected
- **Tier:** Core
- **Development skills:** nextjs-best-practices, nextjs-security, nextjs-testing, nextjs-troubleshooting
- **Review agent:** `nextjs-reviewer` (subagent_type: `rad-nextjs:nextjs-reviewer`)

### rad-react
- **Triggers when:** React detected (not Preact)
- **Tier:** Core when React is the primary UI library; Supporting when used inside Astro or Next.js
- **Development skills:** react-foundations, react-app-building, react-engineering, react-performance, react-accessibility, react-security
- **Review agent:** `react-reviewer` (subagent_type: `rad-react:react-reviewer`)

### rad-tailwind
- **Triggers when:** Tailwind CSS detected
- **Tier:** Supporting
- **Development skills:** tailwind-best-practices
- **Review agent:** (uses general code review)

### rad-typescript
- **Triggers when:** TypeScript detected
- **Tier:** Supporting (applies broadly to all TypeScript code)
- **Development skills:** typescript-strict-mode, typescript-type-patterns, typescript-api-safety, typescript-error-handling, typescript-modern-features, typescript-anti-patterns
- **Review agent:** `typescript-reviewer` (subagent_type: `rad-typescript:typescript-reviewer`)

### rad-fastify
- **Triggers when:** Fastify detected
- **Tier:** Core
- **Development skills:** fastify-best-practices, fastify-hooks-lifecycle, fastify-schemas-validation, fastify-logging, fastify-typescript, fastify-testing, fastify-production, fastify-troubleshooting
- **Review agent:** `fastify-reviewer` (subagent_type: `rad-fastify:fastify-reviewer`)

### rad-zod
- **Triggers when:** Zod detected
- **Tier:** Supporting
- **Development skills:** All rad-zod skills (schema composition, error handling, framework integrations, security review)
- **Review agent:** (covered by typescript-reviewer for type safety)

### rad-chrome-extension
- **Triggers when:** Chrome Extension manifest or WXT detected
- **Tier:** Core
- **Development skills:** chrome-ext-best-practices, chrome-ext-security, chrome-ext-messaging, chrome-ext-service-worker, chrome-ext-storage, chrome-ext-permissions, chrome-ext-testing, chrome-ext-ui-react, chrome-ext-troubleshooting
- **Review agent:** `chrome-ext-reviewer` (subagent_type: `rad-chrome-extension:chrome-ext-reviewer`)

### rad-stripe-fastify-webhooks
- **Triggers when:** Stripe detected AND Fastify detected
- **Tier:** Core (for webhook-related code)
- **Development skills:** All rad-stripe-fastify-webhooks skills
- **Review agent:** (manual review — no dedicated subagent type)

### rad-docker
- **Triggers when:** Dockerfile or docker-compose detected
- **Tier:** Supporting
- **Development skills:** docker, docker-review, docker-scaffold
- **Review agent:** (manual review via docker-review skill)

### rad-seo-optimizer
- **Triggers when:** Project type is Website or Web Application
- **Tier:** Pre-Ship
- **Review agent:** `seo-dominator` (subagent_type: `rad-seo-optimizer:seo-dominator`)

### rad-a11y
- **Triggers when:** Project has UI components (.tsx, .jsx, .astro files)
- **Tier:** Supporting (during development); Pre-Ship (for review)
- **Development skills:** a11y-review, a11y-semantic-html, a11y-aria-patterns, a11y-keyboard-focus, a11y-forms, a11y-testing
- **Review agent:** `a11y-reviewer` (subagent_type: `rad-a11y:a11y-reviewer`)

---

## Tier Definitions

| Tier | When to Use | Impact on Workflow |
|---|---|---|
| **Core** | Always consult during development in this project | Loaded when working on related code |
| **Supporting** | Consult when touching relevant code | Referenced as needed, not loaded by default |
| **Pre-Ship** | Run before deploying or merging | Dispatched by `/review-for-ship` command |
