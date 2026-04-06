# Repo Discoverability & README Polish — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make RAD-Claude-Skills organically discoverable by improving GitHub metadata, rewriting all plugin READMEs to hook both coders and non-coders in the first 3 seconds, and setting up community infrastructure.

**Architecture:** README-first approach — every plugin README follows the same formula (hook → story → use cases → how it works → quick start). GitHub metadata runs passively. Community steps are user-executed checkpoints.

**Tech Stack:** Markdown, GitHub, gws CLI (email), git

---

## README Formula (used in every task below)

```markdown
# Plugin Name — [one punchy hook line]

[2-3 sentence story: what was painful before, what's easy now]

## What You Can Do With This

- [concrete use case 1]
- [concrete use case 2]
- [concrete use case 3]

## How It Works

[skills/agents table — keep existing table, just ensure it's accurate]

## Quick Start

[install command + 2-3 trigger phrases]

## License
Apache-2.0
```

**The 3-second test:** Read the opening line aloud. If a non-coder can't understand the value, rewrite it.

---

## Files Modified

| File | Action |
|------|--------|
| `plugins/rad-code-review/README.md` | Full rewrite |
| `plugins/rad-brainstormer/README.md` | Full rewrite |
| `plugins/rad-seo-optimizer/README.md` | Full rewrite |
| `plugins/rad-stack-guide/README.md` | Full rewrite |
| `README.md` | Add narrative paragraph |
| `plugins/rad-react/README.md` | Formula rewrite |
| `plugins/rad-typescript/README.md` | Formula rewrite |
| `plugins/rad-nextjs/README.md` | Formula rewrite |
| `plugins/rad-fastify/README.md` | Formula rewrite |
| `plugins/rad-a11y/README.md` | Formula rewrite |
| `plugins/rad-google-workspace/README.md` | Formula rewrite |
| `plugins/rad-agentic-company-builder/README.md` | Formula rewrite |
| `plugins/rad-session/README.md` | Formula rewrite |
| `plugins/rad-coolify-orchestrator/README.md` | Formula rewrite |
| `plugins/rad-chrome-extension/README.md` | Formula rewrite |
| `plugins/rad-astro/README.md` | Formula rewrite |
| `plugins/rad-zod/README.md` | Opening line + story |
| `plugins/rad-stripe-fastify-webhooks/README.md` | Opening line + story |
| `plugins/rad-context-prompter/README.md` | Opening line + story |
| `plugins/rad-para-second-brain/README.md` | Opening line + story |
| `plugins/rad-supabase/README.md` | Opening line + story |

---

## Task 1: GitHub Foundation (Manual Steps)

> **Note:** These steps are executed by the user directly in the GitHub web UI and terminal. No code changes required in this task. Check each off as you complete it.

**GitHub.com UI steps:**

- [ ] **Step 1: Set repo description**
  Go to `github.com/radesjardins/RAD-Claude-Skills` → Settings (gear icon next to About) → paste:
  ```
  180+ skills and plugins for Claude Code — code review, SEO, brainstorming, React, Next.js, TypeScript, accessibility, and more. Free, open source, Apache 2.0.
  ```

- [ ] **Step 2: Add topics**
  In the same About settings, add these topics one by one:
  ```
  claude-code  claude  anthropic  ai-tools  developer-tools
  claude-code-plugins  code-review  seo  react  nextjs
  typescript  accessibility  productivity  open-source
  ```

- [ ] **Step 3: Enable GitHub Discussions**
  Go to repo Settings → Features → check "Discussions" → Save.

- [ ] **Step 4: Create seed Discussion threads**
  Go to the Discussions tab → New discussion → create these two threads:
  - Title: `Which plugin are you using? What's working?` (category: General)
  - Title: `Plugin requests and ideas` (category: Ideas)

- [ ] **Step 5: Pin the repo to your profile**
  Go to `github.com/radesjardins` → Customize your profile → Pin repositories → add RAD-Claude-Skills.

- [ ] **Step 6: Social preview image**
  Go to repo Settings → Social preview → Upload an image.
  Content spec: dark background, white text "RAD Claude Skills", subtitle "180+ skills for Claude Code", bottom-right "github.com/radesjardins/RAD-Claude-Skills". Use Canva or any design tool. 1280×640px.

- [ ] **Step 7: Create GitHub Profile README repo**
  Go to github.com/new → name it exactly `radesjardins` (must match your username exactly) → initialize with a README → the content of that README will be written in Task 2.

---

## Task 2: GitHub Profile README

> Executor: Write this file. The user will copy-paste it into their `radesjardins/radesjardins/README.md` repo, OR you can commit it to a local clone of that repo if one exists.

**Files:**
- Create: `../radesjardins-profile/README.md` (or provide as text for copy-paste)

- [ ] **Step 1: Write the profile README**

  > The GitHub Profile README lives in a separate repo named exactly `radesjardins` (same as your username). Create it at github.com/new, name it `radesjardins`, initialize with a README, then paste the content below into the README file via the GitHub web editor and commit.

  Content:

  ```markdown
  # Hi, I'm RAD

  I build open-source plugins for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — Anthropic's agentic coding CLI.

  ## What I'm Building

  **[RAD Claude Skills](https://github.com/radesjardins/RAD-Claude-Skills)** — 20 plugins, 180+ skills, 13 autonomous agents covering code review, SEO, React, TypeScript, accessibility, brainstorming, Google Workspace automation, and more. Free and open source.

  Each plugin installs in one command and activates automatically when you ask Claude about relevant topics — no manual invocation needed.

  ## Featured

  - **rad-code-review** — adversarial code review that catches AI slop and only flags what you changed
  - **rad-seo-optimizer** — full-site SEO audits + AI search visibility from your editor
  - **rad-brainstormer** — structured ideation with 10 proven methodologies
  - **rad-stack-guide** — detects your stack, installs the right plugins, orchestrates your reviewers

  ## Links

  - [RAD Claude Skills repo](https://github.com/radesjardins/RAD-Claude-Skills) — browse all plugins
  - [dev.to](https://dev.to/radesjardins) — writing about Claude Code and open source

  Apache 2.0 — free to use, fork, and improve.
  ```

- [ ] **Step 2: Verify the 3-second test**
  Read the first two lines aloud. A non-coder should understand what this person builds and why it matters.

- [ ] **Step 3: Commit**
  The GitHub web editor has a "Commit changes" button — use that directly. No local clone needed.

---

## Task 3: rad-code-review README (Tier 1 Flagship)

**Files:**
- Modify: `plugins/rad-code-review/README.md`

- [ ] **Step 1: Rewrite the README**

  ```markdown
  # rad-code-review — Catch what AI wrote wrong before it ships.

  When you build with Claude, you move fast. Fast enough that subtle bugs, fake error handling, and hardcoded accessibility states slip through — and they look fine at a glance. rad-code-review is the adversarial reviewer that knows exactly which mistakes AI code generators make. It only flags what *you* changed, not the whole codebase. And it understands your framework well enough to catch the security holes that generic linters miss.

  ## What You Can Do With This

  - Review your current diff for bugs and security issues before committing — only the code you wrote gets flagged
  - Check a new API endpoint for IDOR vulnerabilities across 6 supported frameworks (Next.js, Express, Fastify, Django, Rails, Go)
  - Run a pre-ship audit across the full repo with a clear ship/no-ship verdict
  - Detect AI-generated code anti-patterns: hallucinated imports, fake error handling, placeholder stubs, silent failures

  ## How It Works

  rad-code-review runs three review roles in sequence — bug finder, architecture reviewer, release gate — then produces severity-ranked findings with optional fix application.

  | Skill | Purpose |
  |-------|---------|
  | `rad-code-review` | Full orchestrated review — blame-aware scoping, 3 review roles, 12 dimensions, adversarial pass, fix application, report generation |

  | Agent | Purpose |
  |-------|---------|
  | `code-reviewer` | Autonomous reviewer — scans codebase for bugs, security vulnerabilities, AI slop, performance anti-patterns, accessibility violations, and release blockers |

  ## Key Capabilities

  - **Blame-aware diff scoping** — only flag issues you introduced, not pre-existing noise
  - **14-pattern AI slop detection** — hallucinated imports, fake error handling, placeholder stubs, silent failures, and 10 more
  - **Framework-specific IDOR detection** — Next.js, Express, Fastify, Django, Rails, Go
  - **Dynamic ARIA state detection** — catches hardcoded `aria-expanded`, `aria-selected`, `aria-checked`, `aria-pressed`
  - **Performance heuristics** — N+1 queries, unbounded lists, sync blocking, bundle bloat, re-renders
  - **8 project-type modules** — web app, API, Chrome extension, CLI, library, Electron, mobile, SaaS
  - **Fix application with validation** — applies fixes, runs tests, verifies

  ## Quick Start

  ```bash
  claude plugins add ./RAD-Claude-Skills/plugins/rad-code-review
  ```

  Then just ask naturally:

  ```
  Review my code
  Is this ready to ship?
  Check what I changed for security issues
  Review changes since last release
  ```

  Or use slash commands:

  ```bash
  /rad-code-review diff          # Review current diff (blame-aware)
  /rad-code-review --since abc123  # Review since a specific commit
  /rad-code-review repo --strictness public  # Full repo, public release standard
  ```

  ## License
  Apache-2.0
  ```

- [ ] **Step 2: 3-second test**
  Read: *"Catch what AI wrote wrong before it ships."* — passes for both audiences.

- [ ] **Step 3: Commit**
  ```bash
  git add plugins/rad-code-review/README.md
  git commit -m "docs: rewrite rad-code-review README with hook-first structure"
  ```

---

## Task 4: rad-brainstormer README (Tier 1)

**Files:**
- Modify: `plugins/rad-brainstormer/README.md`

- [ ] **Step 1: Rewrite the README**

  ```markdown
  # rad-brainstormer — A thinking partner that knows when to diverge and when to decide.

  Brainstorming alone loops back to the same ideas. rad-brainstormer brings 10 proven methodologies — SCAMPER, Six Thinking Hats, Five Whys, reverse brainstorming, design sprints — into a structured session with autonomous agents that research your domain, stress-test your assumptions, and review your specs for completeness. Works for software features, business strategy, product decisions, content, and anything else you need to think through clearly.

  ## What You Can Do With This

  - Run a guided brainstorm on a new feature — diverge broadly, then converge to a decision
  - Use Five Whys to find the real root cause of a recurring problem
  - Do a design sprint to go from vague idea to reviewable spec in one session
  - Stress-test your plan with a pre-mortem before you build

  ## How It Works

  | Skill | Purpose |
  |-------|---------|
  | `brainstorm-session` | Facilitated session with structured divergent/convergent phases |
  | `idea-generation` | Generate diverse ideas using multiple creative techniques |
  | `idea-evaluation` | Evaluate and prioritize ideas with structured criteria |
  | `creative-unblock` | Break through blocks with lateral thinking techniques |
  | `scamper` | SCAMPER — Substitute, Combine, Adapt, Modify, Put to other uses, Eliminate, Reverse |
  | `six-hats` | Six Thinking Hats — explore all perspectives systematically |
  | `reverse-brainstorm` | Make the problem worse to find what's actually causing it |
  | `five-whys` | Root cause analysis — ask why until you hit the real issue |
  | `how-might-we` | Reframe problems as opportunity statements |
  | `design-sprint` | Structured spec creation and architecture design |

  | Agent | Purpose |
  |-------|---------|
  | `domain-researcher` | Research any topic — landscape, approaches, constraints, recent innovations |
  | `idea-challenger` | Pre-mortem analysis — feasibility, desirability, viability stress-test |
  | `spec-reviewer` | Review design specs for completeness, consistency, and implementation readiness |

  ## Quick Start

  ```bash
  claude plugins add ./RAD-Claude-Skills/plugins/rad-brainstormer
  ```

  Then just say:

  ```
  Let's brainstorm
  I need ideas for X
  Run a design sprint for this feature
  Do a Five Whys on why this keeps happening
  Help me evaluate these three options
  ```

  ## License
  Apache-2.0
  ```

- [ ] **Step 2: 3-second test**
  Read: *"A thinking partner that knows when to diverge and when to decide."* — passes.

- [ ] **Step 3: Commit**
  ```bash
  git add plugins/rad-brainstormer/README.md
  git commit -m "docs: rewrite rad-brainstormer README with hook-first structure"
  ```

---

## Task 5: rad-seo-optimizer README (Tier 1)

**Files:**
- Modify: `plugins/rad-seo-optimizer/README.md`

- [ ] **Step 1: Rewrite the README**

  ```markdown
  # rad-seo-optimizer — Full-site SEO audit, keyword strategy, and AI search visibility — without leaving your editor.

  SEO has always meant switching tools, switching contexts, and waiting for separate reports. rad-seo-optimizer brings the whole workflow into Claude Code — crawl your site for technical issues, find keyword gaps, fix structured data, and optimize for AI search engines like ChatGPT and Perplexity that increasingly control discovery. Twelve skills, three autonomous agents, one place.

  ## What You Can Do With This

  - Run a complete site-wide SEO audit with a scored report and prioritized fix list
  - Find out how your brand appears in AI-generated answers (ChatGPT, Perplexity, Gemini) and improve it
  - Research keywords, map search intent, and identify content gaps your competitors are filling
  - Fix specific issues: broken links, missing schema, slow Core Web Vitals, bad meta descriptions

  ## How It Works

  | Skill | Purpose |
  |-------|---------|
  | `full-seo-audit` | Complete site-wide SEO audit with prioritized findings |
  | `on-page-optimizer` | Title tags, meta descriptions, headings, internal linking |
  | `keyword-discovery` | Keyword research, search intent analysis, opportunity mapping |
  | `competitor-intelligence` | Competitor content, ranking, and strategy analysis |
  | `content-strategist` | Content gaps, topic clusters, editorial calendar planning |
  | `link-building-strategy` | Backlink opportunities, outreach templates, domain authority |
  | `schema-architect` | JSON-LD structured data, rich snippets, schema.org markup |
  | `technical-seo` | Core Web Vitals, crawlability, robots.txt, sitemaps, site speed |
  | `aeo-optimizer` | AI search visibility, GEO optimization, brand presence in AI answers |
  | `fix-seo` | Step-by-step fix guidance for specific SEO issues |
  | `broken-link-fixer` | Find and fix 404 errors, dead links, redirect chains |
  | `seo-report-generator` | Generate formatted audit reports with scores and recommendations |

  | Agent | Purpose |
  |-------|---------|
  | `seo-dominator` | Full-site autonomous SEO audit with scored report and prioritized fixes |
  | `competitor-spy` | Autonomous competitor research — content, links, SERP features, AI visibility |
  | `content-auditor` | Content quality and AEO readiness audit with refresh/rewrite recommendations |

  ## Quick Start

  ```bash
  claude plugins add ./RAD-Claude-Skills/plugins/rad-seo-optimizer
  ```

  Then just ask:

  ```
  Audit my SEO
  How do I get recommended by ChatGPT?
  Find keyword opportunities I'm missing
  Check my competitor's SEO strategy
  Fix my missing meta descriptions
  ```

  ## License
  Apache-2.0
  ```

- [ ] **Step 2: 3-second test**
  Read: *"Full-site SEO audit, keyword strategy, and AI search visibility — without leaving your editor."* — passes for both audiences.

- [ ] **Step 3: Commit**
  ```bash
  git add plugins/rad-seo-optimizer/README.md
  git commit -m "docs: rewrite rad-seo-optimizer README with hook-first structure"
  ```

---

## Task 6: rad-stack-guide README (Tier 1 — Orchestrator Story)

**Files:**
- Modify: `plugins/rad-stack-guide/README.md`

- [ ] **Step 1: Rewrite the README**

  ```markdown
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
  ```

- [ ] **Step 2: 3-second test**
  Read: *"Install one plugin. It figures out what else you need — and connects everything."* — passes.

- [ ] **Step 3: Commit**
  ```bash
  git add plugins/rad-stack-guide/README.md
  git commit -m "docs: rewrite rad-stack-guide README — orchestrator story, solo vs combined use"
  ```

---

## Task 7: Root README — Add Narrative Paragraph

**Files:**
- Modify: `README.md` (add a short paragraph above the plugin tables)

- [ ] **Step 1: Read the current README**
  Read `README.md`. Find the line `## What's Here` and the directory tree block. Insert the new paragraph *after* the directory tree block and the `---` divider, but *before* `## Quick Install`.

- [ ] **Step 2: Insert the paragraph**

  After the closing ` ``` ` of the directory tree and the `---` divider, insert:

  ```markdown
  ## Why These Plugins?

  Claude Code is powerful out of the box — but it doesn't know your framework's security model, your accessibility requirements, or which code review patterns catch AI-generated mistakes. These plugins fill that gap.

  Each one installs in a single command and activates automatically when you ask Claude about relevant topics. No configuration, no manual invocation — just better answers for the specific tools and problems you're working with. Use any plugin on its own, or use `rad-stack-guide` to detect your full stack and connect them all.

  ---
  ```

- [ ] **Step 3: Commit**
  ```bash
  git add README.md
  git commit -m "docs: add Why These Plugins narrative to root README"
  ```

---

## Task 8: Tier 2 README Rewrites — Developer Frameworks (rad-react, rad-typescript, rad-nextjs)

**Files:**
- Modify: `plugins/rad-react/README.md`
- Modify: `plugins/rad-typescript/README.md`
- Modify: `plugins/rad-nextjs/README.md`

- [ ] **Step 1: Rewrite rad-react README**

  ```markdown
  # rad-react — Modern React patterns for Claude Code. Hooks, performance, security, and React 19.

  React moves fast, and so does the list of ways to write it badly. rad-react keeps Claude aligned with current patterns — functional components, React 19 forms, secure data handling, and performance optimization — so you're not discovering anti-patterns or security gaps during code review.

  ## What You Can Do With This

  - Get hooks-compliant component code that follows current React patterns
  - Review a component for XSS vulnerabilities and insecure direct object references (IDOR)
  - Optimize re-renders with the right memoization strategy for your use case
  - Check that your forms, modals, and dynamic content meet WCAG 2.2 AA standards

  ## How It Works

  | Skill | Purpose |
  |-------|---------|
  | `react-foundations` | Components, hooks, JSX, props, state management, context |
  | `react-app-building` | Routing, layouts, forms, data fetching, server/client boundaries |
  | `react-engineering` | Project tooling, testing, code organization, TypeScript integration |
  | `react-performance` | Re-render optimization, memoization, lazy loading, profiling |
  | `react-accessibility` | ARIA patterns, keyboard navigation, screen reader support |
  | `react-security` | XSS prevention, IDOR checks, input sanitization, secure data handling |

  | Agent | Purpose |
  |-------|---------|
  | `react-reviewer` | Reviews React code for anti-patterns, accessibility, performance, and security |

  ## Quick Start

  ```bash
  claude plugins add ./RAD-Claude-Skills/plugins/rad-react
  ```

  Claude activates these skills automatically when you work on React code. Or ask directly:

  ```
  Review my React code for security issues
  Is this component accessible?
  Why is this re-rendering too much?
  ```

  ## License
  Apache-2.0
  ```

- [ ] **Step 2: Rewrite rad-typescript README**

  ```markdown
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
  ```

- [ ] **Step 3: Rewrite rad-nextjs README**

  ```markdown
  # rad-nextjs — Next.js App Router done right. Server/client boundaries, auth, caching, and security.

  The App Router changed how Next.js works at a fundamental level — and Claude's training data includes a lot of Pages Router patterns that silently break things. rad-nextjs keeps Claude aligned with App Router conventions: correct server/client component boundaries, safe Server Actions, data fetching that doesn't over-cache or under-secure, and IDOR prevention built into every route handler.

  ## What You Can Do With This

  - Write Server Actions that verify auth before mutating data (not after)
  - Get route handlers and API endpoints with IDOR protection built in
  - Fix hydration errors and client/server boundary mistakes
  - Set up testing for App Router components with the correct Vitest/Cypress patterns

  ## How It Works

  | Skill | Purpose |
  |-------|---------|
  | `nextjs-best-practices` | App Router conventions, server/client boundaries, data fetching, caching |
  | `nextjs-security` | IDOR prevention, Server Action auth, CSP, input validation |
  | `nextjs-testing` | Vitest, Cypress, Testing Library for App Router |
  | `nextjs-troubleshooting` | Hydration errors, boundary mistakes, caching bugs |

  | Agent | Purpose |
  |-------|---------|
  | `nextjs-reviewer` | Reviews Next.js code for App Router violations, security issues, and performance anti-patterns |

  ## Quick Start

  ```bash
  claude plugins add ./RAD-Claude-Skills/plugins/rad-nextjs
  ```

  ```
  Review my Next.js code
  Is my Server Action secure?
  Fix this hydration error
  Check my route handlers for IDOR
  ```

  ## License
  Apache-2.0
  ```

- [ ] **Step 4: Commit all three**
  ```bash
  git add plugins/rad-react/README.md plugins/rad-typescript/README.md plugins/rad-nextjs/README.md
  git commit -m "docs: rewrite rad-react, rad-typescript, rad-nextjs READMEs with hook-first structure"
  ```

---

## Task 9: Tier 2 README Rewrites — Backend & Infrastructure (rad-fastify, rad-coolify-orchestrator, rad-chrome-extension)

**Files:**
- Modify: `plugins/rad-fastify/README.md`
- Modify: `plugins/rad-coolify-orchestrator/README.md`
- Modify: `plugins/rad-chrome-extension/README.md`

- [ ] **Step 1: Rewrite rad-fastify README**

  ```markdown
  # rad-fastify — Fastify the way Fastify was designed. Encapsulation, schemas, hooks, and production patterns.

  Fastify's power comes from its encapsulation model and hook lifecycle — but they're also where most mistakes happen. rad-fastify keeps Claude aligned with Fastify's actual design philosophy: proper plugin encapsulation, JSON Schema validation on every route, Pino logging configured correctly, and TypeScript type providers that don't leak types across scope boundaries.

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
  ```

- [ ] **Step 2: Rewrite rad-coolify-orchestrator README**

  ```markdown
  # rad-coolify-orchestrator — Deploy, manage, and troubleshoot self-hosted apps on Coolify — from Claude Code.

  Coolify is a self-hosted Heroku/Netlify alternative, and it has its own patterns for Dockerfiles, environment variables, Traefik routing, and zero-downtime deployments. rad-coolify-orchestrator teaches Claude those patterns so you're not guessing at configuration or debugging 502s without a clear mental model of what Traefik is doing.

  ## What You Can Do With This

  - Deploy an application to Coolify with the right build pack and health check configuration
  - Diagnose 502/504 errors, failed deployments, and Traefik routing issues with a structured approach
  - Set up environment variables and secrets without exposing them in Dockerfiles or build logs
  - Configure CI/CD pipelines that trigger Coolify deployments from GitHub Actions

  ## How It Works

  | Skill | Purpose |
  |-------|---------|
  | `coolify-deploy` | Build packs, Dockerfile patterns, Docker Compose, deployment configuration |
  | `coolify-databases` | Database provisioning, backups, restore, connection strings |
  | `coolify-security` | Secrets management, environment variables, Docker BuildKit secrets |
  | `coolify-cicd` | GitHub Actions integration, webhook triggers, Coolify REST API |
  | `coolify-infrastructure` | Multi-server, Docker Swarm, server configuration |
  | `coolify-observability` | Sentinel monitoring, notification channels, log configuration |
  | `coolify-troubleshoot` | 502/504 diagnosis, Traefik routing, container failures, deployment errors |
  | `coolify-actions` | MCP-based operational actions against a live Coolify instance |

  | Agent | Purpose |
  |-------|---------|
  | `coolify-reviewer` | Reviews Coolify configs, Dockerfiles, and environment setups for anti-patterns and security issues |

  ## Quick Start

  ```bash
  claude plugins add ./RAD-Claude-Skills/plugins/rad-coolify-orchestrator
  ```

  ```
  Review my Coolify deployment config
  Why is my deployment failing?
  Set up CI/CD for Coolify
  Is my Dockerfile ready for Coolify?
  ```

  ## License
  Apache-2.0
  ```

- [ ] **Step 3: Rewrite rad-chrome-extension README**

  ```markdown
  # rad-chrome-extension — Build production-ready Chrome MV3 extensions. Security, messaging, storage, and Chrome Web Store compliance handled.

  Chrome's Manifest V3 changed how extensions are built — service workers instead of background pages, stricter CSP, new permission patterns. rad-chrome-extension keeps Claude aligned with MV3 conventions and the WXT framework, with security and Chrome Web Store compliance built into every component it helps you write.

  ## What You Can Do With This

  - Build an extension popup, content script, or service worker with correct MV3 patterns
  - Set up messaging between your background service worker, content scripts, and popup — without the common race conditions
  - Request only the permissions you actually need (and understand why the Store rejects over-permissioned extensions)
  - Review an extension for security issues before submitting to the Chrome Web Store

  ## How It Works

  | Skill | Purpose |
  |-------|---------|
  | `chrome-ext-best-practices` | MV3 conventions, WXT framework, project structure |
  | `chrome-ext-service-worker` | Service worker lifecycle, persistence patterns, background tasks |
  | `chrome-ext-messaging` | Inter-component messaging, ports, connection patterns |
  | `chrome-ext-storage` | chrome.storage.local/sync, data patterns, migration |
  | `chrome-ext-permissions` | Permission minimization, optional permissions, CWS compliance |
  | `chrome-ext-security` | CSP, eval usage, content script trust boundaries, XSS prevention |
  | `chrome-ext-ui-react` | React UI in popups and side panels, WXT + React patterns |
  | `chrome-ext-testing` | Unit tests, integration tests for extension components |
  | `chrome-ext-troubleshooting` | CWS rejections, service worker issues, messaging bugs |

  | Agent | Purpose |
  |-------|---------|
  | `chrome-ext-reviewer` | Reviews extension code for security, messaging patterns, permission over-requesting, and CWS compliance |

  ## Quick Start

  ```bash
  claude plugins add ./RAD-Claude-Skills/plugins/rad-chrome-extension
  ```

  ```
  Review my Chrome extension
  Is my extension ready for the Chrome Web Store?
  Check my extension for security issues
  ```

  ## License
  Apache-2.0
  ```

- [ ] **Step 4: Commit all three**
  ```bash
  git add plugins/rad-fastify/README.md plugins/rad-coolify-orchestrator/README.md plugins/rad-chrome-extension/README.md
  git commit -m "docs: rewrite rad-fastify, rad-coolify, rad-chrome-extension READMEs"
  ```

---

## Task 10: Tier 2 README Rewrites — Quality & Productivity (rad-a11y, rad-astro, rad-agentic-company-builder)

**Files:**
- Modify: `plugins/rad-a11y/README.md`
- Modify: `plugins/rad-astro/README.md`
- Modify: `plugins/rad-agentic-company-builder/README.md`

- [ ] **Step 1: Rewrite rad-a11y README**

  ```markdown
  # rad-a11y — WCAG 2.2 AA accessibility built in, not bolted on.

  Accessibility is easiest when it's part of how you build, not an audit you run afterward. rad-a11y brings WCAG 2.2 AA standards into your development workflow — semantic HTML, ARIA patterns, keyboard navigation, focus management, and automated testing with axe-core — so compliance isn't a separate phase.

  ## What You Can Do With This

  - Review a component for accessibility violations before it ships — with specific WCAG criteria referenced
  - Get correct ARIA roles and attributes for custom interactive elements (accordions, dialogs, tabs, comboboxes)
  - Set up axe-core or jest-axe for automated a11y testing in your CI pipeline
  - Fix keyboard navigation and focus management issues that screen readers expose

  ## How It Works

  | Skill | Purpose |
  |-------|---------|
  | `a11y-semantic-html` | Semantic structure, heading hierarchy, landmark regions |
  | `a11y-aria-patterns` | ARIA roles, attributes, live regions — when to use and when not to |
  | `a11y-keyboard-focus` | Keyboard navigation, focus rings, focus trapping, skip links |
  | `a11y-forms` | Accessible form labels, error messages, required fields |
  | `a11y-testing` | axe-core, jest-axe, @testing-library, Playwright a11y testing |
  | `a11y-review` | Full WCAG 2.2 AA audit of a component or page |

  | Agent | Purpose |
  |-------|---------|
  | `a11y-reviewer` | Autonomous accessibility audit — WCAG failures, ARIA misuse, keyboard navigation, focus management |

  ## Quick Start

  ```bash
  claude plugins add ./RAD-Claude-Skills/plugins/rad-a11y
  ```

  ```
  Review my accessibility
  Is this component keyboard accessible?
  Check for WCAG violations
  Set up axe-core testing
  ```

  ## License
  Apache-2.0
  ```

- [ ] **Step 2: Rewrite rad-astro README**

  ```markdown
  # rad-astro — Astro 5/6 best practices. Islands, Content Layer, Server Islands, and performance.

  Astro's Islands architecture and Content Layer are powerful but specific — and the patterns from React or Next.js don't always apply. rad-astro keeps Claude aligned with current Astro conventions: correct component boundaries, Content Layer v2 collections, Server Islands, and the performance optimizations that make Astro sites fast by default.

  ## What You Can Do With This

  - Structure an Astro project with correct island boundaries — interactive only where needed
  - Set up Content Layer v2 collections for type-safe content management
  - Debug hydration, build, and SSR issues with a structured approach
  - Audit your Astro site for Core Web Vitals issues and LCP optimization

  ## How It Works

  | Skill | Purpose |
  |-------|---------|
  | `astro-best-practices` | Project structure, Islands architecture, component patterns, conventions |
  | `astro-performance` | Core Web Vitals, LCP/CLS/INP, image optimization, bundle analysis |
  | `astro-security` | CSP configuration, XSS prevention, input validation |
  | `astro-accessibility` | ARIA patterns, WCAG compliance in Astro components |
  | `astro-troubleshooting` | Hydration errors, build issues, SSR debugging, common anti-patterns |

  | Agent | Purpose |
  |-------|---------|
  | `astro-reviewer` | Reviews Astro code for anti-patterns, performance issues, security, and accessibility |

  ## Quick Start

  ```bash
  claude plugins add ./RAD-Claude-Skills/plugins/rad-astro
  ```

  ```
  Review my Astro code
  Is my Astro site production ready?
  Check Astro performance
  Fix this Astro hydration error
  ```

  ## License
  Apache-2.0
  ```

- [ ] **Step 3: Rewrite rad-agentic-company-builder README**

  ```markdown
  # rad-agentic-company-builder — Scaffold an AI-agent-driven company structure in a single session.

  Running a company with AI agents requires a specific infrastructure: folder hierarchies that agents can navigate, CLAUDE.md files that give each agent its context, hooks that enforce quality gates, and MCP configs that connect agents to the tools they need. rad-agentic-company-builder creates all of that from scratch — based on *The Agentic Bible 2026* — so you can start operating with a full agent team instead of building scaffolding by hand.

  ## What You Can Do With This

  - Scaffold a full company folder hierarchy with CLAUDE.md files for each function
  - Generate a standard 6-agent team: architect, implementer, reviewer, tester, deployer, docs-writer
  - Configure quality gate hooks and MCP connections (GitHub, Coolify, PostgreSQL, Google Workspace, and more)
  - Audit your existing agentic structure for gaps against Agentic Bible best practices

  ## How It Works

  | Skill | Trigger Phrases | What It Does |
  |-------|----------------|--------------|
  | `scaffold-company` | "scaffold a company", "create agentic company" | Creates company folder hierarchy with CLAUDE.md files and shared infrastructure |
  | `scaffold-project` | "scaffold a project", "add a project" | Adds a new application project within the company structure |
  | `generate-agents` | "generate agents", "set up agent team" | Generates 6 standard agent types |
  | `generate-skills` | "generate skills", "add skills to project" | Generates 4 standard skills: sprint-cycle, api-design, release-prep, daily-standup |
  | `configure-hooks` | "configure hooks", "set up quality gates" | Sets up enforcement hooks and quality gates |
  | `configure-mcp` | "configure MCP", "add MCP integrations" | Configures MCP server connections |
  | `agentic-operations` | "daily operating rhythm", "token optimization" | Reference guide for daily ops, cost optimization, credential rotation |

  | Agent | Purpose |
  |-------|---------|
  | `company-auditor` | Audits company structure for completeness against Agentic Bible best practices |

  ## Quick Start

  ```bash
  claude plugins add ./RAD-Claude-Skills/plugins/rad-agentic-company-builder
  ```

  ```
  Scaffold a company
  Generate agents for my project
  Configure MCP for my setup
  Audit my agentic company structure
  ```

  ## Requirements

  - Claude Code CLI installed and authenticated
  - Familiarity with the Agentic Bible 2026 patterns (recommended)

  ## License
  Apache-2.0
  ```

- [ ] **Step 4: Commit all three**
  ```bash
  git add plugins/rad-a11y/README.md plugins/rad-astro/README.md plugins/rad-agentic-company-builder/README.md
  git commit -m "docs: rewrite rad-a11y, rad-astro, rad-agentic-company-builder READMEs"
  ```

---

## Task 11: Tier 2 README Rewrites — Productivity (rad-session, rad-google-workspace)

**Files:**
- Modify: `plugins/rad-session/README.md`
- Modify: `plugins/rad-google-workspace/README.md`

- [ ] **Step 1: Rewrite rad-session README**

  ```markdown
  # rad-session — Never lose context between Claude Code sessions again.

  Every time you start a new Claude Code session, you start fresh. rad-session fixes that with two commands: `/wrapup` captures exactly where you left off — decisions made, traps to avoid, open work — and `/startup` reads it back at the start of the next session so you're oriented in seconds instead of minutes.

  ## What You Can Do With This

  - End a session with a structured handoff that captures status, key decisions, known traps, and next steps
  - Start the next session with a concise briefing — git state, branch info, and where you left off
  - Keep CLAUDE.md clean over time — `/wrapup` prunes stale content automatically (shows you the diff first)

  ## How It Works

  | Skill | Trigger | What It Does |
  |-------|---------|-------------|
  | `/wrapup` | End of session | Writes HANDOFF.md, appends session log, prunes CLAUDE.md, prompts for memory updates |
  | `/startup` | Start of session | Reads HANDOFF.md + session log, detects project state, presents briefing |

  The plugin maintains three files per project:

  | File | Purpose |
  |------|---------|
  | `CLAUDE.md` | Permanent rules, conventions, tech stack |
  | `HANDOFF.md` | Current session state (overwritten each `/wrapup`) |
  | `.claude/session-log.md` | Session history (append-only, capped at 20 entries) |

  ## Quick Start

  ```bash
  claude plugins add ./RAD-Claude-Skills/plugins/rad-session
  ```

  At the end of any session:
  ```
  /wrapup
  ```

  At the start of the next:
  ```
  /startup
  ```

  Works with coding projects (captures git state) and non-coding projects (scans recently modified files).

  ## License
  Apache-2.0
  ```

- [ ] **Step 2: Rewrite rad-google-workspace README**

  ```markdown
  # rad-google-workspace — Your entire Google Workspace, accessible from Claude Code.

  Gmail, Calendar, Drive, Docs, Sheets, Chat, Meet, Tasks, Forms, Classroom, and more — all accessible through natural language or commands. rad-google-workspace provides 93 skills covering direct service access, 41 cross-service workflow recipes, and 10 role-based personas for common job functions. Requires the `gws` CLI.

  ## What You Can Do With This

  - Send emails, schedule meetings, and manage Drive files without leaving your editor
  - Run cross-service workflows: convert a Gmail thread to a task, prepare for your next meeting, post-mortem setup, weekly digest
  - Automate repetitive Workspace operations: bulk Drive organization, sheet data exports, form response collection
  - Operate as a role-based persona — Executive Assistant, Project Manager, IT Admin, and more

  ## Skill Categories

  ### Service Skills (44)
  Direct API access: Gmail · Calendar · Drive · Docs · Sheets · Slides · Chat · Meet · Tasks · Forms · Keep · Classroom · Admin · People · Events · Model Armor · Apps Script

  ### Workflow Recipes (41)
  Cross-service workflows including: email-to-task, meeting prep, weekly digest, standup report, file announce, expense tracker setup, post-mortem setup, bulk invitations, and more.

  ### Role-Based Personas (10)
  Pre-configured behavioral profiles: Executive Assistant, Team Lead, Project Manager, Sales Ops, IT Admin, HR Coordinator, Content Creator, Event Coordinator, Customer Support, Researcher.

  ## Quick Start

  ```bash
  claude plugins add ./RAD-Claude-Skills/plugins/rad-google-workspace
  ```

  Requires the `gws` CLI — see [gws installation](https://github.com/googleworkspace/cli).

  ```
  Send an email to alice@example.com
  What's on my calendar today?
  Prepare me for my next meeting
  Run my weekly digest
  ```

  ## Attribution

  Derivative work based on the [Google Workspace CLI](https://github.com/googleworkspace/cli), Apache License 2.0. Not an officially supported Google product.

  ## License
  Apache-2.0
  ```

- [ ] **Step 3: Commit both**
  ```bash
  git add plugins/rad-session/README.md plugins/rad-google-workspace/README.md
  git commit -m "docs: rewrite rad-session, rad-google-workspace READMEs"
  ```

---

## Task 12: Tier 3 README Quick Passes (rad-zod, rad-stripe-fastify-webhooks, rad-context-prompter, rad-para-second-brain, rad-supabase)

> Tier 3 is opening line + short story only. Keep the existing skills/agents tables. Just replace the header and add a 2-sentence story paragraph.

**Files:**
- Modify: `plugins/rad-zod/README.md`
- Modify: `plugins/rad-stripe-fastify-webhooks/README.md`
- Modify: `plugins/rad-context-prompter/README.md`
- Modify: `plugins/rad-para-second-brain/README.md`
- Modify: `plugins/rad-supabase/README.md`

- [ ] **Step 1: Update rad-zod — replace opening**

  Read `plugins/rad-zod/README.md`. Replace everything before the first `##` heading with:
  ```markdown
  # rad-zod — Zod v4 schemas that are secure, composable, and framework-ready.

  Zod is the standard for TypeScript runtime validation — but it's easy to write schemas that look safe and aren't. rad-zod covers coercion attacks, schema composition patterns, and integrations with Fastify, Next.js, and React Hook Form so your validation layer is actually a security layer.
  ```
  Keep the rest of the file unchanged.

- [ ] **Step 2: Update rad-stripe-fastify-webhooks — replace opening**

  Read `plugins/rad-stripe-fastify-webhooks/README.md`. Replace everything before the first `##` heading with:
  ```markdown
  # rad-stripe-fastify-webhooks — Stripe webhooks with Fastify. Signature verification, subscription state machines, and idempotent processing done right.

  Stripe webhooks fail in specific, hard-to-debug ways — signature verification races, duplicate event processing, subscription state inconsistencies. rad-stripe-fastify-webhooks covers all of it: the correct verification flow, idempotency patterns, and state machine logic for subscription lifecycle events.
  ```
  Keep the rest of the file unchanged.

- [ ] **Step 3: Update rad-context-prompter — replace opening**

  Read `plugins/rad-context-prompter/README.md`. Replace everything before the first `##` heading with:
  ```markdown
  # rad-context-prompter — Write, debug, and optimize prompts for 30+ AI platforms. No guessing.

  Different AI models need different prompting strategies — what works for Claude degrades output on o3, and vice versa. rad-context-prompter maps your task type to the right technique for the right model, diagnoses why a prompt is failing with a coded taxonomy, and can reverse-engineer existing prompts to translate them across platforms.
  ```
  Keep the rest of the file unchanged.

- [ ] **Step 4: Update rad-para-second-brain — replace opening**

  Read `plugins/rad-para-second-brain/README.md`. Replace everything before the first `##` heading with:
  ```markdown
  # rad-para-second-brain — An AI that actively manages your PARA second brain. Not just knowledge about it.

  Most PARA tools tell you about the methodology. rad-para-second-brain implements it for you — organizing notes, running weekly reviews, distilling raw captures into usable knowledge, and maintaining continuity between sessions via the Hemingway Bridge pattern. Based on Tiago Forte's Building a Second Brain.
  ```
  Keep the rest of the file unchanged.

- [ ] **Step 5: Update rad-supabase — replace opening**

  Read `plugins/rad-supabase/README.md`. Replace everything before the first `##` heading with:
  ```markdown
  # rad-supabase — Full-stack Supabase development. Local CLI workflows, remote MCP operations, and production patterns.

  Supabase has two interfaces — the CLI for local development and migrations, and the MCP server for remote project operations — and knowing when to use which is half the battle. rad-supabase covers both, plus the non-negotiables: RLS on every public table, service role keys never on the client, and cost confirmation before creating branches or projects.
  ```
  Keep the rest of the file unchanged.

- [ ] **Step 6: Commit all five**
  ```bash
  git add plugins/rad-zod/README.md plugins/rad-stripe-fastify-webhooks/README.md plugins/rad-context-prompter/README.md plugins/rad-para-second-brain/README.md plugins/rad-supabase/README.md
  git commit -m "docs: tier 3 README quick passes — hook lines and story paragraphs"
  ```

---

## Task 13: Final Verification Pass

- [ ] **Step 1: Spot-check the 3-second test across all plugins**
  Read the opening line of each plugin README. Verify each passes:
  - Is the value clear to a non-coder?
  - Does a coder immediately know what problem it solves?

- [ ] **Step 2: Verify root README plugin table links still work**
  Each row in the root README links to `plugins/<name>/`. Confirm the links resolve correctly after the README rewrites (filenames didn't change, just content).

- [ ] **Step 3: Push to remote**
  ```bash
  git push origin main
  ```

- [ ] **Step 4: Post-push checklist (user-executed)**
  - Confirm GitHub topics are visible on the repo page
  - Confirm the repo description shows correctly
  - Check that the social preview card looks right by sharing the URL in a test Discord message

---

## Community Steps (User-Executed, No Code)

These happen after the README work is complete.

- [ ] Join Claude Code Discord (link in Anthropic docs) — lurk for 1-2 weeks, map pain points
- [ ] Browse r/ClaudeAI and r/ChatGPTCoding — same pattern, observe before posting
- [ ] After completing Tasks 3-12, post once in r/ClaudeAI: *"I've been building Claude Code plugins for a few months — open sourced everything. 20 plugins, 180+ skills. Here's what's in it."* + repo link
- [ ] Share on personal social media with tags: `#ClaudeCode #AnthropicAI #OpenSource #DeveloperTools`
- [ ] Begin Phase 2: answer questions helpfully in communities, mention plugins only when directly relevant

---

## Implementation Order Summary

1. Task 1 — GitHub Foundation (manual, do first)
2. Task 2 — GitHub Profile README
3. Task 3 — rad-code-review (flagship)
4. Task 4 — rad-brainstormer
5. Task 5 — rad-seo-optimizer
6. Task 6 — rad-stack-guide
7. Task 7 — Root README narrative
8. Task 8 — React, TypeScript, Next.js
9. Task 9 — Fastify, Coolify, Chrome Extension
10. Task 10 — a11y, Astro, Agentic Company Builder
11. Task 11 — Session, Google Workspace
12. Task 12 — Tier 3 quick passes
13. Task 13 — Final verification + push
14. Community steps (after all README work is done)
