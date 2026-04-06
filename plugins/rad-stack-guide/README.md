# rad-stack-guide

Install one plugin. It detects your stack, tells you what else to install, configures Claude to use framework-specific best practices during development, and runs every relevant reviewer before you ship.

## Quick Start

```bash
# 1. Install the orchestrator
claude plugins install rad-stack-guide@rad-claude-skills

# 2. Detect your stack
/detect-stack

# 3. Install any recommended plugins it finds
# 4. Develop with stack-aware guidance (CLAUDE.md auto-configured)
# 5. Ship with confidence
/review-for-ship
```

## What It Does

### Phase 1: Detect & Equip (`/detect-stack`)

Scans your project's `package.json`, config files, and file types to identify your tech stack. Then:

- **Creates a stack profile** at `.claude/stack-profile.local.md` with detected technologies, plugin mappings, and review agent assignments
- **Runs gap analysis** — checks which rad-* plugins are installed vs. recommended, shows install commands for missing ones
- **Injects CLAUDE.md guidance** — adds skill routing rules so Claude proactively consults the right skills for your stack during development
- **Generates team settings** — creates `.claude/settings.json` with `enabledPlugins` so teammates get the same plugins when they trust the project folder

### Phase 2: Guide During Development

With stack guidance in your CLAUDE.md, Claude knows which skills to consult when you're working on different parts of your codebase:

- Writing a React component? Claude consults `rad-react` for hooks rules, performance, security
- Adding a Server Action? Claude consults `rad-nextjs` for auth verification, IDOR prevention
- Defining a Zod schema? Claude consults `rad-zod` for coercion attacks, validation patterns

No manual skill invocation needed — the routing rules guide Claude automatically.

### Phase 3: Review Before Shipping (`/review-for-ship`)

Dispatches all relevant specialist reviewers in parallel, then runs `rad-code-review` as the final gate:

```
Phase 1: Specialist Reviewers (parallel)          Phase 2: Final Gate
────────────────────────────────────────          ──────────────────────
rad-react:react-reviewer                          rad-code-review
rad-nextjs:nextjs-reviewer                        ├── AI slop detection
rad-typescript:typescript-reviewer                 ├── Architecture review
rad-a11y:a11y-reviewer                            ├── Release readiness
rad-seo-optimizer:seo-dominator                   ├── General security
  ...whatever your stack needs                    └── Ship / No Ship verdict
```

Produces a unified report with findings from all sources, priority-ordered fix recommendations, and a clear ship/no-ship verdict.

## Supported Stacks

| Technology | Plugin | Tier | Reviewer Agent |
|---|---|---|---|
| Astro | rad-astro | Core | astro-reviewer |
| Next.js | rad-nextjs | Core | nextjs-reviewer |
| React | rad-react | Core/Supporting | react-reviewer |
| TypeScript | rad-typescript | Supporting | typescript-reviewer |
| Fastify | rad-fastify | Core | fastify-reviewer |
| Zod | rad-zod | Supporting | zod-reviewer |
| Chrome Extension | rad-chrome-extension | Core | chrome-ext-reviewer |
| Accessibility | rad-a11y | Supporting/Pre-Ship | a11y-reviewer |
| Supabase | rad-supabase | Supporting | supabase-reviewer |
| Coolify/Docker | rad-coolify-orchestrator | Supporting | coolify-reviewer |
| SEO | rad-seo-optimizer | Pre-Ship | seo-dominator |
| Stripe + Fastify | rad-stripe-fastify-webhooks | Core | (manual) |
| **Any project** | **rad-code-review** | **Final Gate** | **generalist review** |

## Bundle Philosophy

Every rad-* plugin works independently. `rad-react` doesn't need `rad-stack-guide` to function. `rad-code-review` doesn't need any other plugin.

`rad-stack-guide` makes the *combination* seamless:
- **Without it:** You manually decide which plugins to install, when to invoke which skills, and which reviewers to run
- **With it:** Auto-detection, auto-configuration, and orchestrated multi-reviewer pre-ship checks

Think of it as the difference between buying tools individually and having a workshop that organizes them for you.

## What's Inside

| Component | Count |
|-----------|-------|
| Skills | 2 (`detect-stack`, `review-for-ship`) |
| Agents | 0 (dispatches agents from other rad-* plugins dynamically) |
| References | 1 (technology detection rules and plugin mapping) |

## Skills

| Skill | What It Does |
|-------|-------------|
| `detect-stack` | Scans project, detects stack, writes profile, runs gap analysis, injects CLAUDE.md guidance, generates team settings |
| `review-for-ship` | Reads profile, dispatches specialist reviewers in parallel, runs rad-code-review as final gate, compiles unified report |

## Installation

```bash
claude plugins install rad-stack-guide@rad-claude-skills
```

## Requirements

- Claude Code CLI installed and authenticated
- Other rad-* plugins installed for specialist reviewers (rad-stack-guide will tell you which ones you need)
- rad-code-review plugin for the final gate

## License

Apache-2.0
