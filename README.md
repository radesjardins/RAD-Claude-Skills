# RAD Claude Skills

A curated marketplace of plugins for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — Anthropic's agentic coding tool. 21 plugins, 210+ skills, and 15 autonomous agents covering developer frameworks, productivity, accessibility, SEO, writing, and more.

Install everything at once or cherry-pick individual plugins.

---

## What's Here

```
RAD-Claude-Skills/
├── plugins/                           # Full Claude Code plugins (multi-skill bundles)
│   ├── rad-a11y/                      # WCAG 2.2 AA accessibility toolkit
│   ├── rad-agentic-company-builder/   # AI-agent-driven company infrastructure
│   ├── rad-astro/                     # Astro 5/6 framework standards
│   ├── rad-brainstormer/              # Ideation methodologies & creative tools
│   ├── rad-chrome-extension/          # MV3 Chrome extension development
│   ├── rad-code-review/               # Diff-aware adversarial code review
│   ├── rad-fastify/                   # Fastify framework standards
│   ├── rad-google-workspace/          # Google Workspace integration (93 skills)
│   ├── rad-nextjs/                    # Next.js App Router standards
│   ├── rad-react/                     # Modern React best practices
│   ├── rad-seo-optimizer/             # Complete SEO & AEO toolkit
│   ├── rad-stack-guide/               # Stack detection, guidance & review orchestration
│   ├── rad-stripe-fastify-webhooks/   # Stripe webhook handling with Fastify
│   ├── rad-typescript/                # Production TypeScript standards
│   ├── rad-writer/                    # Domain-smart writing (9 domains, AI pattern avoidance)
│   └── rad-zod/                       # Zod v4 validation patterns
```

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

## Plugins

### Developer Frameworks

| Plugin | Skills | Agents | What It Does |
|--------|--------|--------|-------------|
| [rad-react](plugins/rad-react/) | 6 | 1 | Modern React — hooks, JSX, routing, forms, React 19 patterns, security (XSS, IDOR), performance, accessibility |
| [rad-nextjs](plugins/rad-nextjs/) | 4 | 1 | Next.js App Router — server/client boundaries, data fetching, caching, security, testing, troubleshooting |
| [rad-astro](plugins/rad-astro/) | 5 | 1 | Astro 5/6 — Islands architecture, Content Layer v2, Server Islands, performance, security, accessibility |
| [rad-fastify](plugins/rad-fastify/) | 8 | 1 | Fastify — encapsulation model, hook lifecycle, JSON Schema validation, Pino logging, TypeScript providers |
| [rad-typescript](plugins/rad-typescript/) | 6 | 1 | Production TypeScript — strict mode, type patterns, API boundary safety, error handling, AI codegen guardrails |
| [rad-zod](plugins/rad-zod/) | 6 | 1 | Zod v4 — schema design, validation patterns, security, framework integrations |
| [rad-chrome-extension](plugins/rad-chrome-extension/) | 9 | 1 | Chrome MV3 extensions — WXT, React, security, messaging, storage, service workers, CWS compliance |

### Quality & Testing

| Plugin | Skills | Agents | What It Does |
|--------|--------|--------|-------------|
| [rad-a11y](plugins/rad-a11y/) | 6 | 1 | WCAG 2.2 AA accessibility — semantic HTML, ARIA, keyboard, focus, forms, automated testing with axe-core |
| [rad-code-review](plugins/rad-code-review/) | 1 | 1 | Diff-aware adversarial code review — blame-aware scoping, framework-specific IDOR (6 frameworks), AI slop detection (14 patterns), performance heuristics, WCAG 2.2 ARIA state detection, 3 review roles, 8 project type modules |
| [rad-stack-guide](plugins/rad-stack-guide/) | 2 | 0 | Stack detection, guidance & review orchestration — auto-detects stack, configures CLAUDE.md, dispatches specialist reviewers + rad-code-review final gate |

### Productivity & Business

| Plugin | Skills | Agents | What It Does |
|--------|--------|--------|-------------|
| [rad-seo-optimizer](plugins/rad-seo-optimizer/) | 12 | 3 | Complete SEO toolkit — audits, AEO/AI visibility, keywords, competitors, link building, schema, reports |
| [rad-brainstormer](plugins/rad-brainstormer/) | 10 | 3 | Ideation methodologies — SCAMPER, Six Hats, Five Whys, reverse brainstorming, idea evaluation, design sprints |
| [rad-google-workspace](plugins/rad-google-workspace/) | 93 | 0 | Google Workspace — Gmail, Calendar, Drive, Docs, Sheets, Chat, Meet, Tasks, Forms, plus 41 recipes and 10 personas |
| [rad-agentic-company-builder](plugins/rad-agentic-company-builder/) | 7 | 1 | AI-agent company infrastructure — scaffolding, agent teams, hooks, MCP configs, operational patterns |
| [rad-writer](plugins/rad-writer/) | 4 | 2 | Domain-smart writing across 9 content types — email, blog, web copy, reports, research, presentations, prose, technical docs, social media. AI pattern avoidance, voice profiles, accept/reject suggestions |

### Specialized

| Plugin | Skills | Agents | What It Does |
|--------|--------|--------|-------------|
| [rad-stripe-fastify-webhooks](plugins/rad-stripe-fastify-webhooks/) | 7 | 1 | Stripe webhooks with Fastify — signature verification, subscription state machines, idempotent processing |

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
