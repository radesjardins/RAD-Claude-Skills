# RAD Claude Skills

A curated marketplace of plugins for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — Anthropic's agentic coding tool. The lineup focuses on capabilities that add value beyond Opus 4.7's baseline competence: workflow lifecycle, MCP-backed live operations, structured planning, honest AI-pattern auditing, and domain-specific tools where they earn their place.

Install everything at once or cherry-pick individual plugins.

> **May 2026 — RAD 8-doc standardization (marketplace v1.5.0, rad-planner 3.0 + rad-session 4.0).** rad-planner and rad-session are now **soft-coupled** through the RAD 8-doc standard at [`docs/file-conventions.md`](docs/file-conventions.md). The old v2.x single `implementation_plan.md` mega-doc is replaced by five focused files at project root — `PRD.md`, `ARCHITECTURE.md`, `ASSUMPTIONS.md`, `DECISIONS.md`, `PLAN.md` — plus `tasks.md` and a transient `CLAUDE-FRAGMENT.md` that rad-session's `/init` consumes. Each file has exactly one plugin owner (single-writer rule). The `generate-project-config` skill is retired; its role splits between `/rad-planner:plan` (writes ARCHITECTURE) and `/rad-session:init` (writes CLAUDE.md after merging the FRAGMENT). New `/plan --reboot` audits an existing codebase and regenerates strategic docs anchored to current reality; `/plan --validate` is a cheap 8-doc gap-check. `/rad-session:wrapup` Phase 3.5 prompts to append tagged decisions to `DECISIONS.md` with sequence-numbered entries. **A migration helper at [`plugins/rad-session/scripts/migrate-to-v4.py`](plugins/rad-session/scripts/migrate-to-v4.py)** handles upgrades from 2.x / 3.x projects. See [`docs/file-conventions.md`](docs/file-conventions.md) for the full standard and the "why" behind it.
>
> **April 2026 — Marketplace tightened.** The single-framework reviewer plugins (rad-react, rad-zod, rad-typescript, rad-nextjs, rad-fastify, rad-astro, rad-stripe-fastify-webhooks) have been archived — Opus 4.7 handles those framework-specific reviews well enough on its own. **rad-stack-guide is also archived**, with its stack-detection value absorbed into rad-session 3.0's new `/init` skill. **rad-google-workspace (93 skills) is also archived** — superseded by the focused [`rad-gws-core`](plugins/rad-gws-core/) (14 essential skills). All archived plugins are preserved in [`archive/`](archive/) for reference. The remaining 15 plugins are the ones that demonstrably add value Opus doesn't already provide.

---

## What's Here

```
RAD-Claude-Skills/
├── packages/                          # Standalone npm packages
│   └── coolify-mcp/                   # @radoriginllc/coolify-mcp — MCP server for Coolify API
├── plugins/                           # Claude Code CLI & Desktop plugins (multi-skill bundles)
│   ├── rad-a11y/                      # WCAG 2.2 AA accessibility toolkit
│   ├── rad-agentic-company-builder/   # Workspace scaffolding + opt-in business-function agents (where MCPs exist)
│   ├── rad-brainstormer/              # Ideation methodologies & creative tools
│   ├── rad-chrome-extension/          # MV3 Chrome extension development
│   ├── rad-code-review/               # Diff-aware adversarial code review
│   ├── rad-context-prompter/          # Prompt engineering for 30+ AI platforms
│   ├── rad-coolify-orchestrator/      # Coolify self-hosted PaaS management (MCP-backed)
│   ├── rad-gws-core/                  # Google Workspace core (14 essential skills)
│   ├── rad-para-second-brain/         # PARA second brain — organize, review, distill
│   ├── rad-planner/                   # Structured project planning + Python DAG validators
│   ├── rad-seo-optimizer/             # Complete SEO & AEO toolkit
│   ├── rad-session/                   # Three-phase workflow lifecycle: /init + /startup + /wrapup
│   ├── rad-supabase/                  # Full-stack Supabase development (MCP-backed)
│   └── rad-writer/                    # Domain-aware writing (9 domains) + Python validators for measured AI patterns
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

Claude Code is powerful out of the box — but it doesn't know which MCP servers your project has wired up, which review patterns catch AI-generated mistakes in your specific framework, or how to deterministically validate the implementation plan it just generated. These plugins add value Opus 4.7 doesn't provide on its own: deterministic validators (Python scripts), MCP-backed live operations, structured workflow lifecycle, and domain-specific tools.

Each one installs in a single command and activates automatically when you ask Claude about relevant topics. No configuration, no manual invocation — just better answers for the specific problems they were built for. Use any plugin on its own, or run **`/rad-session:init`** in a new project to detect your stack and get a recommendation list of which plugins fit.

---

## Quick Install

### Option 1: Add as a Marketplace (recommended)

Add the entire marketplace to Claude Code or Claude Desktop — browse and install any plugin, with automatic updates on sync.

```bash
# Add the marketplace
claude plugin marketplace add https://github.com/radesjardins/RAD-Claude-Skills

# Install any plugin from the marketplace
claude plugin install rad-session@rad-claude-skills
claude plugin install rad-code-review@rad-claude-skills
claude plugin install rad-planner@rad-claude-skills
# ... any plugin from the list below

# Update all installed plugins
claude plugin marketplace update
```

### Option 2: Install Directly from Git

```bash
# Clone the repo
git clone https://github.com/radesjardins/RAD-Claude-Skills.git

# Install any plugin
claude plugins add ./RAD-Claude-Skills/plugins/rad-session
claude plugins add ./RAD-Claude-Skills/plugins/rad-code-review
claude plugins add ./RAD-Claude-Skills/plugins/rad-planner
# ... any plugin from the list below
```

### Verify Installation

Start a new Claude Code session and run:
```
/skills
```

---

## Where to Start

Not sure which plugins to install first? These four deliver the most value across the widest range of projects:

| Plugin | Why install it | Works with |
|--------|---------------|-----------|
| [rad-session](plugins/rad-session/) | **4.0** — Three-phase workflow lifecycle with cross-machine continuity AND soft-coupling to rad-planner via the [RAD 8-doc standard](docs/file-conventions.md). `/init` bootstraps (deterministic stack detection, plugin recommendations, CLAUDE.md scaffold, **merges `CLAUDE-FRAGMENT.md` from rad-planner's `/plan` and deletes it**), `/startup` orients each session (verifies sync with origin before reading any handoff file, **gap-checks the 5 strategic docs and soft-warns when missing**), `/wrapup` captures state (**prompts to append tagged decisions to `DECISIONS.md`** as sequence-numbered entries, prune protection, auto-commits + prompts to push). PreCompact safety net included. | CLI, Desktop |
| [rad-code-review](plugins/rad-code-review/) | Catches bugs, AI anti-patterns, and security issues in your current diff — regardless of language or framework | CLI, Desktop |
| [rad-planner](plugins/rad-planner/) | **3.0** — Structured implementation planning with the [RAD 8-doc output standard](docs/file-conventions.md): `/plan` emits PRD / ARCHITECTURE / ASSUMPTIONS / DECISIONS / PLAN + tasks.md + transient CLAUDE-FRAGMENT.md. Python DAG validators back the parts templates can't enforce. New `--reboot` mode regenerates after pivots; `--validate` does a cheap 8-doc gap-check. | CLI, Desktop |
| [rad-writer](plugins/rad-writer/) | Domain-aware writing across 9 content types with measured AI-pattern auditing (Python validators), honest about what detection can/can't claim in 2026 | CLI, Desktop, Claude.ai |

After installing rad-session, run `/rad-session:init` in your project — it detects your stack and recommends which other rad-* plugins fit (no auto-install, just informed recommendations).

---

## Plugin Pipelines

Some plugins are designed to chain. The most common pipeline for a new project:

1. **[rad-brainstormer](plugins/rad-brainstormer/)** — explore the problem space, converge on an idea, produce a design spec (`/rad-brainstormer:brainstorm-session` → `/rad-brainstormer:design-sprint`)
2. **[rad-planner](plugins/rad-planner/)** — turn the spec into a dependency-aware implementation plan with risk review and mechanical DAG/checklist validation (`/rad-planner:plan`, or `--lite` for small work, or `--reboot` to regenerate after a pivot). Emits the [RAD 8-doc standard](docs/file-conventions.md): PRD + ARCHITECTURE + ASSUMPTIONS + DECISIONS + PLAN + tasks.md + a transient CLAUDE-FRAGMENT.md.
3. **[rad-session](plugins/rad-session/)** — `/init` merges the CLAUDE-FRAGMENT into CLAUDE.md so the strategic docs are imported every session. `/startup` orients the execution session, `/wrapup` captures state.
4. **[rad-code-review](plugins/rad-code-review/)** — review the code you generate from the plan (`/rad-code-review`)

Each plugin stands alone — the pipeline is a suggestion, not a requirement. The boundary between `design-sprint` and `plan` is: design-sprint produces a *spec* (architecture, components, APIs), plan produces an *ordered implementation plan* (DAG, tasks, complexity, risk) plus the 8-doc strategic/operational set.

---

## Plugins

### Workflow & Code Quality

| Plugin | Skills | Agents | What It Does | Works with |
|--------|--------|--------|-------------|-----------|
| [rad-session](plugins/rad-session/) | 4 | 0 | **4.0** — Three-phase workflow lifecycle, **soft-coupled with rad-planner 3.0 via the [RAD 8-doc standard](docs/file-conventions.md)**. `/init` bootstraps once (stack detection, plugin recommendations, **CLAUDE.md scaffold with FRAGMENT-merge / auto-generated / placeholder `@-imports`** for the 5 strategic docs). `/startup` orients each session (Phase 0 fetches origin and prompts to pull when behind; **Phase 1.5 gap-checks the strategic docs and soft-warns**). `/wrapup` captures each session (structured HANDOFF.md, mechanical session-log derivation, **Phase 3.5 prompts to append tagged decisions to `DECISIONS.md`** as sequence-numbered multi-line entries — skipped in `--quick` / non-interactive; CLAUDE.md prune-with-diff auto-skipped when unchanged; auto-commit + prompted push). `/add-resource`. Four Python scripts (`detect-stack.py`, `detect-resources.py`, `audit-plugin-bloat.py`, `migrate-to-v4.py`). PreCompact safety net. Single-writer rule: this plugin owns CLAUDE.md / HANDOFF.md / session-log; rad-planner owns the strategic and operational tier. | CLI, Desktop |
| [rad-code-review](plugins/rad-code-review/) | 1 | 1 | Diff-aware adversarial code review — blame-aware scoping, framework-specific IDOR (6 frameworks), AI slop detection (14 patterns), performance heuristics, 3 review roles | CLI, Desktop |
| [rad-planner](plugins/rad-planner/) | 5 | 3 | **3.0** — Structured implementation-planning scaffolding with the [RAD 8-doc output standard](docs/file-conventions.md). `/plan` emits 5 strategic/operational files at project root (PRD, ARCHITECTURE, ASSUMPTIONS, DECISIONS, PLAN) plus tasks.md plus a transient `CLAUDE-FRAGMENT.md` consumed by rad-session's `/init`. The old `implementation_plan.md` mega-doc and `EXECUTION-PROMPT.md` are retired (PLAN.md replaces the former; `/rad-session:startup` briefing replaces the latter). The `generate-project-config` skill is removed — its role is absorbed by `/plan` Phase 6 + rad-session's FRAGMENT merge. New mode flags: `--reboot` (audit current code, archive prior strategic docs to `*.pre-reboot`, regenerate anchored to reality, append sequence-number-superseded entries to DECISIONS); `--validate` (cheap 8-doc gap-check + plan-lint, no agents, no writes). Python DAG / field-presence / JSON Schema validators unchanged. `/checkpoint` no longer writes HANDOFF.md per the single-writer rule. | CLI, Desktop |
| [rad-a11y](plugins/rad-a11y/) | 6 | 1 | WCAG 2.2 AA accessibility — 4 reference skills (semantic HTML, ARIA, keyboard/focus, forms), 1 setup skill (a11y-testing wires up real axe via jest-axe + Playwright), 1 static-analysis skill (a11y-review) + autonomous reviewer agent. **2.0 honesty pass:** every finding tagged `[STATIC]` / `[HEURISTIC]` / `[NEEDS-MANUAL]`; no Pass/Fail compliance verdict. **2.1 mechanical validators:** 4 pure-stdlib Python scripts (scan-jsx-patterns, check-tailwind-contrast with real WCAG sRGB math, check-target-size for WCAG 2.5.8, lint-aria wrapping eslint-plugin-jsx-a11y) run in Phase 0 before LLM judgment. **2.2 cross-model + stack-aware:** Phase 0 + Phase 1 issued as a single parallel tool-call burst on Opus 4.7/Sonnet 4.6 (Haiku falls back gracefully); Phase 8 stack slices only execute when detected stack matches (React/Next/Astro/Tailwind/Radix/Headless UI), plain HTML projects skip Phase 8 entirely. | CLI, Desktop |
| [rad-chrome-extension](plugins/rad-chrome-extension/) | 9 | 1 | Chrome MV3 extensions — WXT, React, security, messaging, storage, service workers, CWS compliance | CLI, Desktop |

### Productivity & Content

| Plugin | Skills | Agents | What It Does | Works with |
|--------|--------|--------|-------------|-----------|
| [rad-seo-optimizer](plugins/rad-seo-optimizer/) | 12 | 3 | Full SEO toolkit — site audits, AEO/AI visibility, keyword research, competitor analysis, link building, schema, technical SEO | CLI, Desktop, Claude.ai |
| [rad-brainstormer](plugins/rad-brainstormer/) | 10 | 3 | Structured ideation — SCAMPER, Six Hats, Five Whys, reverse brainstorming, design sprints, pre-mortem analysis | CLI, Desktop, Claude.ai |
| [rad-writer](plugins/rad-writer/) | 4 | 2 | Domain-aware writing across 9 content types — email, blog, web copy, reports, technical docs, social media. Python validators (`text-stats.py` for burstiness/em-dash/hedging/transitions, `check-blocklist.py` for word-list scans). AI patterns reorganized by durability tier. Honest about detection (impossible) and voice cloning (informal-genre limits). 2.0 honesty pass. | CLI, Desktop, Claude.ai |
| [rad-para-second-brain](plugins/rad-para-second-brain/) | 5 | 2 | PARA second brain — organize notes, run weekly reviews, progressive summarization, session handoffs, 12 favorite problems | CLI, Desktop |
| [rad-context-prompter](plugins/rad-context-prompter/) | 2 | 1 | Prompt engineering — write, debug, and optimize prompts for 30+ AI platforms. Includes decompiler for reverse-engineering existing prompts | CLI, Desktop |

### Backend & Infrastructure (MCP-backed live operations)

| Plugin | Skills | Agents | What It Does | Works with |
|--------|--------|--------|-------------|-----------|
| [rad-supabase](plugins/rad-supabase/) | 11 | 1 | Full-stack Supabase — local CLI workflows, MCP remote operations, RLS, migrations, auth, storage, edge functions, branching | CLI, Desktop |
| [rad-coolify-orchestrator](plugins/rad-coolify-orchestrator/) | 8 | 1 | Coolify self-hosted PaaS — deployments, databases, security, CI/CD, troubleshooting, observability, infrastructure. **2.0 ships 4 Python validators** (lint-dockerfile, lint-compose, check-coolify-env, audit-cicd) the coolify-reviewer agent runs before LLM judgment. Honest about what's experimental (Sentinel scope, Swarm, Caddy proxy, Railpack-NOT-yet-shipped). Bundles [`@radoriginllc/coolify-mcp`](packages/coolify-mcp/) (27 verified tools). | CLI, Desktop |

### Google Workspace

| Plugin | Skills | Agents | What It Does | Works with |
|--------|--------|--------|-------------|-----------|
| [rad-gws-core](plugins/rad-gws-core/) | 14 | 0 | Google Workspace essentials — Gmail send/read/reply/triage, Docs write, Sheets read/append, Slides, Drive, Calendar. Requires `gws` CLI. The wider 93-skill `rad-google-workspace` was archived in April 2026 (see [archive/](archive/)). | CLI, Desktop |

### Agentic Systems

| Plugin | Skills | Agents | What It Does | Works with |
|--------|--------|--------|-------------|-----------|
| [rad-agentic-company-builder](plugins/rad-agentic-company-builder/) | 8 | 1 | Claude Code workspace scaffolding + opt-in business-function agents for verified write-capable MCPs (Stripe, HubSpot, QuickBooks, Intercom, Vanta, DocuSign, etc.). Ships Python validators (`audit-structure`, `validate-hooks`, `check-mcp-config`) that catch fictional hook events, hardcoded secrets, structural gaps. Honest about what AI agents can/can't do in 2026. | CLI, Desktop |

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

For example, with `rad-a11y` installed:
```
You: "Is this component accessible?"
Claude: [activates a11y-review skill, runs WCAG 2.2 AA review]

You: "Set up axe-core testing for my project"
Claude: [activates a11y-testing skill, scaffolds CI integration]
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
