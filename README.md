# RAD Claude Skills

A curated marketplace of plugins for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — Anthropic's agentic coding tool. 23 plugins, 234+ skills, and 27 autonomous agents covering developer frameworks, productivity, accessibility, SEO, writing, and more.

Install everything at once or cherry-pick individual plugins.

---

## What's Here

```
RAD-Claude-Skills/
├── packages/                          # Standalone npm packages
│   └── coolify-mcp/                   # @radoriginllc/coolify-mcp — MCP server for Coolify API
├── plugins/                           # Claude Code CLI & Desktop plugins (multi-skill bundles)
│   ├── rad-a11y/                      # WCAG 2.2 AA accessibility toolkit
│   ├── rad-agentic-company-builder/   # AI-agent-driven company infrastructure
│   ├── rad-astro/                     # Astro 5/6 framework standards
│   ├── rad-brainstormer/              # Ideation methodologies & creative tools
│   ├── rad-chrome-extension/          # MV3 Chrome extension development
│   ├── rad-code-review/               # Diff-aware adversarial code review
│   ├── rad-context-prompter/          # Prompt engineering for 30+ AI platforms
│   ├── rad-coolify-orchestrator/      # Coolify self-hosted PaaS management
│   ├── rad-fastify/                   # Fastify framework standards
│   ├── rad-google-workspace/          # Google Workspace integration (93 skills)
│   ├── rad-gws-core/                  # Google Workspace core (14 essential skills)
│   ├── rad-nextjs/                    # Next.js App Router standards
│   ├── rad-para-second-brain/         # PARA second brain — organize, review, distill
│   ├── rad-planner/                   # Structured project planning & risk assessment
│   ├── rad-react/                     # Modern React best practices
│   ├── rad-seo-optimizer/             # Complete SEO & AEO toolkit
│   ├── rad-session/                   # Resource-aware session briefings + disciplined wrapup
│   ├── rad-stack-guide/               # Stack detection, guidance & review orchestration
│   ├── rad-stripe-fastify-webhooks/   # Stripe webhook handling with Fastify
│   ├── rad-supabase/                  # Full-stack Supabase development
│   ├── rad-typescript/                # Production TypeScript standards
│   ├── rad-writer/                    # Domain-aware writing (9 domains, AI pattern removal)
│   └── rad-zod/                       # Zod v4 validation patterns
└── skills/                            # Claude.ai skills (ZIP upload / Project Knowledge)
    ├── rad-brainstormer/              # Ideation — Claude.ai adaptation of rad-brainstormer
    ├── rad-seo-aeo-reviewer/          # SEO/AEO — Claude.ai adaptation of rad-seo-optimizer
    └── rad-writer/                    # Writing — Claude.ai adaptation of rad-writer
```

---

## Plugins vs Skills — Two Formats, Two Environments

You'll notice that some names appear in both `plugins/` and `skills/` (rad-writer, rad-brainstormer). They cover the same knowledge, but they're built for different environments:

**`plugins/` — Claude Code CLI & Claude Desktop**
Full plugin bundles with multiple skills, autonomous agents, reference files, and automatic routing. They activate when you're working in a Claude Code session — they can read your filesystem, spawn subagents, and chain tools together. Install with `claude plugins add`.

**`skills/` — Claude.ai (the web app)**
Single-file skills designed for [claude.ai](https://claude.ai). They work as uploadable ZIP files via **Settings > Customize > Skills**, as Project Knowledge, or as conversation attachments. They consolidate plugin knowledge into one skill, use web search and URL fetching instead of filesystem tools, and output deliverables as artifacts. No CLI needed.

Three plugins have Claude.ai counterparts: `rad-writer`, `rad-brainstormer`, and `rad-seo-optimizer` (as `rad-seo-aeo-reviewer`). The table column **Works with** shows which environments each plugin supports.

---

## Why These Plugins?

Claude Code is powerful out of the box — but it doesn't know your framework's security model, your accessibility requirements, or which code review patterns catch AI-generated mistakes. These plugins fill that gap.

Each one installs in a single command and activates automatically when you ask Claude about relevant topics. No configuration, no manual invocation — just better answers for the specific tools and problems you're working with. Use any plugin on its own, or use `rad-stack-guide` to detect your full stack and connect them all.

---

## Quick Install

### Option 1: Add as a Marketplace (recommended)

Add the entire marketplace to Claude Code or Claude Desktop — browse and install any plugin, with automatic updates on sync.

```bash
# Add the marketplace
claude plugin marketplace add https://github.com/radesjardins/RAD-Claude-Skills

# Install any plugin from the marketplace
claude plugin install rad-react@rad-claude-skills
claude plugin install rad-typescript@rad-claude-skills
claude plugin install rad-code-review@rad-claude-skills
# ... any plugin from the list below

# Update all installed plugins
claude plugin marketplace update
```

### Option 2: Install Directly from Git

```bash
# Clone the repo
git clone https://github.com/radesjardins/RAD-Claude-Skills.git

# Install any plugin
claude plugins add ./RAD-Claude-Skills/plugins/rad-react
claude plugins add ./RAD-Claude-Skills/plugins/rad-typescript
claude plugins add ./RAD-Claude-Skills/plugins/rad-code-review
# ... any plugin from the list below
```

### Verify Installation

Start a new Claude Code session and run:
```
/skills
```

---

## Where to Start

Not sure which plugins to install first? These five deliver the most value across the widest range of projects:

| Plugin | Why install it | Works with |
|--------|---------------|-----------|
| [rad-code-review](plugins/rad-code-review/) | Catches bugs, AI anti-patterns, and security issues in your current diff — regardless of language or framework | CLI, Desktop |
| [rad-session](plugins/rad-session/) | Resource-aware `/startup` briefings (auto-detects MCPs, CLIs, stack), disciplined `/wrapup` with prune protection, PreCompact safety net | CLI, Desktop |
| [rad-typescript](plugins/rad-typescript/) | Enforces strict mode and catches the 14 most common AI-generated TypeScript mistakes | CLI, Desktop |
| [rad-writer](plugins/rad-writer/) | Domain-aware writing across 9 content types, with structured review and AI pattern removal | CLI, Desktop, Claude.ai |
| [rad-stack-guide](plugins/rad-stack-guide/) | Detects your full stack, recommends which rad-* plugins to install, and orchestrates pre-ship reviews | CLI, Desktop |

Install all five in one pass, or pick the ones that match your current work.

---

## Plugin Pipelines

Some plugins are designed to chain. The most common pipeline for a new project:

1. **[rad-brainstormer](plugins/rad-brainstormer/)** — explore the problem space, converge on an idea, produce a design spec (`/rad-brainstormer:brainstorm-session` → `/rad-brainstormer:design-sprint`)
2. **[rad-planner](plugins/rad-planner/)** — turn the spec into a dependency-aware implementation plan with risk review (`/rad-planner:plan-project`)
3. **[rad-code-review](plugins/rad-code-review/)** — review the code you generate from the plan (`/rad-code-review`)

Each plugin stands alone — the pipeline is a suggestion, not a requirement. The boundary between `design-sprint` and `plan-project` is: design-sprint produces a *spec* (architecture, components, APIs), plan-project produces an *ordered implementation plan* (DAG, tasks, complexity, risk).

---

## Plugins

### Developer Frameworks

| Plugin | Skills | Agents | What It Does | Works with |
|--------|--------|--------|-------------|-----------|
| [rad-react](plugins/rad-react/) | 6 | 1 | Modern React — hooks, JSX, routing, forms, React 19 patterns, security (XSS, IDOR), performance, accessibility | CLI, Desktop |
| [rad-nextjs](plugins/rad-nextjs/) | 4 | 1 | Next.js App Router — server/client boundaries, data fetching, caching, security, testing, troubleshooting | CLI, Desktop |
| [rad-astro](plugins/rad-astro/) | 5 | 1 | Astro 5/6 — Islands architecture, Content Layer v2, Server Islands, performance, security, accessibility | CLI, Desktop |
| [rad-fastify](plugins/rad-fastify/) | 8 | 1 | Fastify — encapsulation model, hook lifecycle, JSON Schema validation, Pino logging, TypeScript providers | CLI, Desktop |
| [rad-typescript](plugins/rad-typescript/) | 6 | 1 | Production TypeScript — strict mode, type patterns, API boundary safety, error handling, AI codegen guardrails | CLI, Desktop |
| [rad-zod](plugins/rad-zod/) | 6 | 1 | Zod v4 — schema design, validation patterns, security, framework integrations | CLI, Desktop |
| [rad-chrome-extension](plugins/rad-chrome-extension/) | 9 | 1 | Chrome MV3 extensions — WXT, React, security, messaging, storage, service workers, CWS compliance | CLI, Desktop |

### Code Quality & Developer Workflow

| Plugin | Skills | Agents | What It Does | Works with |
|--------|--------|--------|-------------|-----------|
| [rad-a11y](plugins/rad-a11y/) | 6 | 1 | WCAG 2.2 AA accessibility — semantic HTML, ARIA, keyboard, focus, forms, automated testing with axe-core | CLI, Desktop |
| [rad-code-review](plugins/rad-code-review/) | 1 | 1 | Diff-aware adversarial code review — blame-aware scoping, framework-specific IDOR (6 frameworks), AI slop detection (14 patterns), performance heuristics, 3 review roles | CLI, Desktop |
| [rad-stack-guide](plugins/rad-stack-guide/) | 2 | 0 | Stack detection & review orchestration — detects your stack, configures CLAUDE.md, dispatches specialist reviewers + rad-code-review final gate | CLI, Desktop |
| [rad-session](plugins/rad-session/) | 3 | 0 | Resource-aware session briefings + disciplined wrapup. `/startup` auto-detects MCPs/CLIs/stack (Phase 2.5 Resource Discovery), `/wrapup` captures "what NOT to do" and prunes CLAUDE.md with diff confirmation (Resources section protected), `/add-resource` registers new tools. PreCompact hook prevents silent context loss on compaction. | CLI, Desktop |
| [rad-planner](plugins/rad-planner/) | 5 | 3 | Structured project planning — dependency-aware implementation plans, stack evaluation, risk assessment (14 anti-patterns), failure state mapping, context management | CLI, Desktop |

### Productivity & Content

| Plugin | Skills | Agents | What It Does | Works with |
|--------|--------|--------|-------------|-----------|
| [rad-seo-optimizer](plugins/rad-seo-optimizer/) | 12 | 3 | Full SEO toolkit — site audits, AEO/AI visibility, keyword research, competitor analysis, link building, schema, technical SEO | CLI, Desktop, Claude.ai |
| [rad-brainstormer](plugins/rad-brainstormer/) | 10 | 3 | Structured ideation — SCAMPER, Six Hats, Five Whys, reverse brainstorming, design sprints, pre-mortem analysis | CLI, Desktop, Claude.ai |
| [rad-writer](plugins/rad-writer/) | 4 | 2 | Domain-aware writing across 9 content types — email, blog, web copy, reports, technical docs, social media. Structured review, AI pattern removal, voice profiles | CLI, Desktop, Claude.ai |
| [rad-para-second-brain](plugins/rad-para-second-brain/) | 5 | 2 | PARA second brain — organize notes, run weekly reviews, progressive summarization, session handoffs, 12 favorite problems | CLI, Desktop |
| [rad-context-prompter](plugins/rad-context-prompter/) | 2 | 1 | Prompt engineering — write, debug, and optimize prompts for 30+ AI platforms. Includes decompiler for reverse-engineering existing prompts | CLI, Desktop |

### Backend & Infrastructure

| Plugin | Skills | Agents | What It Does | Works with |
|--------|--------|--------|-------------|-----------|
| [rad-supabase](plugins/rad-supabase/) | 11 | 1 | Full-stack Supabase — local CLI workflows, MCP remote operations, RLS, migrations, auth, storage, edge functions, branching | CLI, Desktop |
| [rad-coolify-orchestrator](plugins/rad-coolify-orchestrator/) | 8 | 1 | Coolify self-hosted PaaS — deployments (Nixpacks/Dockerfile/Compose), databases, security, CI/CD, troubleshooting, observability, infrastructure. Bundles [`@radoriginllc/coolify-mcp`](packages/coolify-mcp/) | CLI, Desktop |
| [rad-stripe-fastify-webhooks](plugins/rad-stripe-fastify-webhooks/) | 7 | 1 | Stripe webhooks with Fastify — signature verification, subscription state machines, idempotent processing | CLI, Desktop |

### Google Workspace

| Plugin | Skills | Agents | What It Does | Works with |
|--------|--------|--------|-------------|-----------|
| [rad-gws-core](plugins/rad-gws-core/) | 14 | 0 | Google Workspace essentials — Gmail send/read/reply/triage, Docs, Sheets, Slides, Drive, Calendar. Lightweight starting point | CLI, Desktop |
| [rad-google-workspace](plugins/rad-google-workspace/) | 93 | 0 | Full Google Workspace — 44 service skills, 41 workflow recipes, 10 role-based personas. Requires `gws` CLI | CLI, Desktop |

### Agentic Systems

| Plugin | Skills | Agents | What It Does | Works with |
|--------|--------|--------|-------------|-----------|
| [rad-agentic-company-builder](plugins/rad-agentic-company-builder/) | 7 | 1 | AI-agent company infrastructure — company scaffolding, agent team generation, hooks, MCP configs, operational patterns | CLI, Desktop |

---

## Claude.ai Skills

Three plugins have been adapted as standalone Claude.ai skills. Import as a ZIP via **Settings > Customize > Skills**, add to a Project, or attach to any conversation.

| Skill | Based on | ZIP | What It Does |
|-------|----------|-----|-------------|
| [rad-writer](skills/rad-writer/) | rad-writer | `rad-writer.zip` | Domain-aware writing and editorial review across 9 content types, AI pattern avoidance, voice profiling |
| [rad-brainstormer](skills/rad-brainstormer/) | rad-brainstormer | `rad-brainstormer.zip` | Facilitated ideation, SCAMPER/Six Hats/Five Whys, pre-mortem analysis, design sprint |
| [rad-seo-aeo-reviewer](skills/rad-seo-aeo-reviewer/) | rad-seo-optimizer | `rad-seo-aeo-reviewer.zip` | SEO audit (URL or GitHub mode), competitor research, content strategy, AI search visibility |

See [`skills/README.md`](skills/README.md) for import instructions and how these differ from the plugin versions.

---

## How It Works

Once installed, skills activate automatically when you ask Claude about relevant topics. Each skill has specific **trigger phrases** — natural language patterns that tell Claude when to use that skill.

For example, with `rad-react` installed:
```
You: "Is this component accessible?"
Claude: [activates react-accessibility skill, reviews your component]

You: "Review my React code for security issues"
Claude: [activates react-security skill, checks for XSS, IDOR, etc.]
```

With `rad-seo-optimizer` installed:
```
You: /seo-audit https://mysite.com
Claude: [runs 6-phase SEO audit with scored report]

You: "How do I get recommended by ChatGPT?"
Claude: [activates aeo-optimizer skill, analyzes AI search visibility]
```

See each plugin's README for its full list of trigger phrases.

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed and authenticated
- Internet access (for skills that fetch web content)
- Some plugins have additional requirements noted in their READMEs

---

## Contributing

Found a bug? Have an idea for a new skill? See:

- [Contributing Guide](CONTRIBUTING.md) — how to submit changes
- [Code of Conduct](CODE_OF_CONDUCT.md) — community standards
- [Security Policy](SECURITY.md) — reporting vulnerabilities
- [Discussions](https://github.com/radesjardins/RAD-Claude-Skills/discussions) — questions & ideas

---

## License

[Apache License 2.0](LICENSE) — free to use, modify, and distribute. Includes patent protection and requires noting modifications.

---

Built with Claude Code by [RAD](https://github.com/radesjardins)
