# RAD Claude Skills

A curated marketplace of plugins and standalone skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — Anthropic's agentic coding tool. 16 plugins, 190+ skills, and 14 autonomous agents covering developer frameworks, productivity, accessibility, SEO, and more.

Install everything at once or cherry-pick individual plugins and skills.

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
│   ├── rad-docker/                    # Dockerfile best practices & optimization
│   ├── rad-fastify/                   # Fastify framework standards
│   ├── rad-google-workspace/          # Google Workspace integration (93 skills)
│   ├── rad-nextjs/                    # Next.js App Router standards
│   ├── rad-react/                     # Modern React best practices
│   ├── rad-seo-optimizer/             # Complete SEO & AEO toolkit
│   ├── rad-stack-detect/              # Tech stack detection & review dispatch
│   ├── rad-stripe-fastify-webhooks/   # Stripe webhook handling with Fastify
│   ├── rad-tailwind/                  # Tailwind CSS v4 standards
│   ├── rad-typescript/                # Production TypeScript standards
│   └── rad-zod/                       # Zod v4 validation patterns
│
└── skills/                            # Standalone skills (copy & use individually)
    ├── rad-brainstorming/             # Collaborative ideation & design specs
    ├── rad-code-review/               # Professional code review with AI slop detection
    ├── rad-context-prompter/          # Prompt engineering for any AI platform
    ├── rad-gem-creator/               # Google Gemini Gem builder
    ├── rad-gpt-creator/               # OpenAI Custom GPT builder
    └── rad-para-second-brain/         # PARA method knowledge management
```

### Plugins vs. Skills

- **Plugins** bundle multiple skills, agents, and reference docs into one installable unit. Install the whole thing with one command.
- **Skills** are standalone — one SKILL.md plus supporting files. Copy a single folder and you're done.

---

## Quick Install

### Install a Plugin

```bash
# Clone the repo
git clone https://github.com/radesjardins/RAD-Claude-Skills.git

# Install any plugin
claude plugins add ./RAD-Claude-Skills/plugins/rad-react
claude plugins add ./RAD-Claude-Skills/plugins/rad-typescript
claude plugins add ./RAD-Claude-Skills/plugins/rad-seo-optimizer
# ... any plugin from the list below
```

### Install a Standalone Skill

```bash
mkdir -p ~/.claude/skills
cp -r RAD-Claude-Skills/skills/rad-code-review ~/.claude/skills/
```

### Verify Installation

Start a new Claude Code session and run:
```
/skills
```

> **Note:** Some skills reference shared files. If you get file-not-found errors, also copy the `references/` directory from the same component.

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
| [rad-tailwind](plugins/rad-tailwind/) | 6 | 1 | Tailwind CSS v4 — utility-first patterns, CVA components, dark mode, responsive design, v3-to-v4 migration |
| [rad-chrome-extension](plugins/rad-chrome-extension/) | 9 | 1 | Chrome MV3 extensions — WXT, React, security, messaging, storage, service workers, CWS compliance |
| [rad-docker](plugins/rad-docker/) | 3 | 1 | Docker — multi-stage builds, image optimization, security hardening, Node.js/Next.js patterns |

### Quality & Testing

| Plugin | Skills | Agents | What It Does |
|--------|--------|--------|-------------|
| [rad-a11y](plugins/rad-a11y/) | 6 | 1 | WCAG 2.2 AA accessibility — semantic HTML, ARIA, keyboard, focus, forms, automated testing with axe-core |
| [rad-stack-detect](plugins/rad-stack-detect/) | 2 | 0 | Tech stack detection — scans your project and dispatches the right review agents before shipping |

### Productivity & Business

| Plugin | Skills | Agents | What It Does |
|--------|--------|--------|-------------|
| [rad-seo-optimizer](plugins/rad-seo-optimizer/) | 12 | 3 | Complete SEO toolkit — audits, AEO/AI visibility, keywords, competitors, link building, schema, reports |
| [rad-brainstormer](plugins/rad-brainstormer/) | 10 | 3 | Ideation methodologies — SCAMPER, Six Hats, Five Whys, reverse brainstorming, idea evaluation, design sprints |
| [rad-google-workspace](plugins/rad-google-workspace/) | 93 | 0 | Google Workspace — Gmail, Calendar, Drive, Docs, Sheets, Chat, Meet, Tasks, Forms, plus 41 recipes and 10 personas |
| [rad-agentic-company-builder](plugins/rad-agentic-company-builder/) | 7 | 1 | AI-agent company infrastructure — scaffolding, agent teams, hooks, MCP configs, operational patterns |

### Specialized

| Plugin | Skills | Agents | What It Does |
|--------|--------|--------|-------------|
| [rad-stripe-fastify-webhooks](plugins/rad-stripe-fastify-webhooks/) | 7 | 1 | Stripe webhooks with Fastify — signature verification, subscription state machines, idempotent processing |

---

## Standalone Skills

| Skill | What It Does |
|-------|-------------|
| [rad-code-review](skills/rad-code-review/) | Professional code review — AI slop detection, security (OWASP), architecture, release readiness. 3 review roles, 8 project type modules. |
| [rad-brainstorming](skills/rad-brainstorming/) | Collaborative ideation — transforms ideas into design specs before implementation. Enforces design-first discipline. |
| [rad-context-prompter](skills/rad-context-prompter/) | Prompt engineering for any AI platform — system prompts, tool descriptions, anti-hallucination, cross-model migration. |
| [rad-gem-creator](skills/rad-gem-creator/) | Google Gemini Gem builder — guided interview, knowledge base design, anti-hallucination patterns. |
| [rad-gpt-creator](skills/rad-gpt-creator/) | OpenAI Custom GPT builder — guided interview, 8K instruction limit management, Actions configuration. |
| [rad-para-second-brain](skills/rad-para-second-brain/) | PARA method knowledge management — folder setup, progressive summarization, weekly reviews, creative techniques. |

---

## How Skills Work

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
