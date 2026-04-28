# rad-stack-guide — Install one plugin. It figures out what else you need — and connects everything.

Every rad-* plugin works great on its own. But when your stack is React + TypeScript + Next.js + Supabase, the right plugins need to work together in a specific way — and manually deciding which ones to install, when to invoke which skills, and which reviewers to run is friction you don't need. rad-stack-guide detects your stack, shows you the gaps, configures Claude automatically, and orchestrates all your specialist reviewers before you ship. It's the difference between a toolbox and a workshop.

The individual plugins are the tools. rad-stack-guide is the workshop that organizes them for you.

## What You Can Do With This

- Set up a new project in one command — rad-stack-guide detects your tech, recommends what to install, and configures Claude to use it
- Develop with stack-aware guidance that routes Claude to the right skills automatically (no manual invocation)
- Run a pre-ship review that dispatches all relevant specialist reviewers in parallel, then gates on rad-code-review as a final pass

## How It Works

### Phase 1: Detect & Equip (`/detect-stack`)

Scans your `package.json`, config files, and file types. Then:
- Creates a stack profile at `.claude/stack-profile.local.md`
- Runs a gap analysis — checks which rad-* plugins are installed vs. recommended
- Injects CLAUDE.md guidance so Claude routes to the right skills during development
- Generates `.claude/settings.json` so teammates get the same plugins automatically

### Phase 2: Guide During Development

With stack guidance in CLAUDE.md, Claude knows which skills to consult automatically:

- Writing a React component? Claude consults `rad-react` for hooks rules, performance, security
- Adding a Server Action? Claude consults `rad-nextjs` for auth verification, IDOR prevention
- Defining a Zod schema? Claude consults `rad-zod` for coercion attacks, validation patterns

No manual skill invocation needed.

### Phase 3: Review Before Shipping (`/review-for-ship`)

```
Phase 1: Specialist Reviewers (parallel)       Phase 2: Final Gate
────────────────────────────────────────       ──────────────────────
rad-react:react-reviewer                       rad-code-review
rad-nextjs:nextjs-reviewer                     ├── AI slop detection
rad-typescript:typescript-reviewer              ├── Architecture review
rad-a11y:a11y-reviewer                         ├── Release readiness
rad-seo-optimizer:seo-dominator                └── Ship / No Ship verdict
  ...whatever your stack needs
```

## Supported Stacks

| Technology | Plugin | Reviewer |
|---|---|---|
| Astro | rad-astro | astro-reviewer |
| Next.js | rad-nextjs | nextjs-reviewer |
| React | rad-react | react-reviewer |
| TypeScript | rad-typescript | typescript-reviewer |
| Fastify | rad-fastify | fastify-reviewer |
| Zod | rad-zod | zod-reviewer |
| Chrome Extension | rad-chrome-extension | chrome-ext-reviewer |
| Accessibility | rad-a11y | a11y-reviewer |
| Supabase | rad-supabase | supabase-reviewer |
| Coolify/Docker | rad-coolify-orchestrator | coolify-reviewer |
| SEO | rad-seo-optimizer | seo-dominator |
| Stripe + Fastify | rad-stripe-fastify-webhooks | (manual) |
| **Any project** | **rad-code-review** | **final gate** |

## Quick Start

```bash
# 1. Install
claude plugins add ./RAD-Claude-Skills/plugins/rad-stack-guide

# 2. Detect your stack and get recommendations
/detect-stack

# 3. Install recommended plugins
# 4. Develop — Claude routes to the right skills automatically
# 5. Ship with confidence
/review-for-ship
```

## What's Inside

| Component | Count |
|-----------|-------|
| Skills | 2 (`detect-stack`, `review-for-ship`) |
| Agents | 0 — dispatches agents from other rad-* plugins dynamically |
| References | 1 — technology detection rules and plugin mapping |

## Requirements

- Claude Code CLI installed and authenticated
- Other rad-* plugins installed for specialist reviewers (rad-stack-guide tells you which ones)
- rad-code-review for the final gate

## License
Apache-2.0
