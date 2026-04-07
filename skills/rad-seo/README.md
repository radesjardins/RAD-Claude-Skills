# RAD SEO — Claude.ai Skills

Comprehensive SEO auditing, strategy, and AI visibility optimization, adapted from the [rad-seo-optimizer plugin](../../plugins/rad-seo-optimizer/) for Claude.ai.

## Two Options

### Option A: Complete Suite (recommended)

One skill with everything. Import `dist/rad-seo-complete.zip` into Claude.ai via **Settings > Customize > Skills**.

Includes the full SKILL.md orchestrator (audit, competitors, strategy, AEO) plus 8 resource files (scoring rubrics, E-E-A-T checklist, schema guide, AEO playbook, link building tactics, outreach templates, and more).

### Option B: Modular Skills

Import only the skills you need. Each is a separate ZIP in `dist/`:

| ZIP File | What It Does | Use When You Want To... |
|----------|-------------|------------------------|
| `rad-seo-audit.zip` | Site evaluation and scoring | Audit a website's SEO health |
| `rad-seo-competitors.zip` | Deep competitor intelligence | Find who's outranking you and why |
| `rad-seo-strategy.zip` | Keywords, content planning, link building | Plan what to do next |
| `rad-seo-aeo.zip` | AI search visibility and schema markup | Get recommended by AI search engines |

Each modular skill is self-contained with no cross-file dependencies. When multiple are imported, they automatically detect each other and offer related analyses after completing their workflow.

## How to Import

**As a Skill (recommended):** Go to **Settings > Customize > Skills** on Claude.ai. Upload the `.zip` file(s). The skill activates automatically in any conversation.

**As Project Knowledge:** Create a Claude.ai Project, add the `.md` file(s) directly as Project Knowledge for project-scoped use.

**As a conversation attachment:** Attach the `.md` file to any conversation for one-off use.

**API system prompt:** Use the SKILL.md content as a system prompt when calling the Claude API directly.

## Example Prompts

### With rad-seo-audit.md
- "I need to analyze my website for SEO"
- "Check the SEO of https://example.com"
- "Score my site's SEO health"
- "What's wrong with my website's SEO?"

### With rad-seo-competitors.md
- "Who are my competitors in search?"
- "Do a competitor analysis for my site"
- "Who's outranking me and why?"
- "Compare my SEO to my competitors"

### With rad-seo-strategy.md
- "Do keyword research for [my topic/industry]"
- "Build me a 12-week content calendar"
- "What should I write about to rank higher?"
- "Help me plan a link building strategy"

### With rad-seo-aeo.md
- "How does my brand appear in AI search results?"
- "Generate schema markup for my homepage"
- "Optimize my site for ChatGPT and Perplexity"
- "Score my AI visibility"

## Input Modes

Each skill automatically adapts to how you provide your site:

- **URL mode** (default): Give a website URL — Claude searches the web and fetches pages to analyze
- **GitHub mode**: If you've connected your GitHub repo, Claude can read source code directly to inspect templates, meta tags, schema, and config files
- **Strategy mode**: No site needed — Claude helps with keyword research, competitor analysis, and content planning using web search

## What's Different from the Plugin

The plugin version (in `plugins/rad-seo-optimizer/`) is built for Claude Code CLI with filesystem tools, subagents, and automatic routing across 12 specialized skills. These Claude.ai skills:

- Consolidate 12 skills + 3 agents into 4 focused workflows
- Replace filesystem operations with web search, URL fetching, and GitHub connector
- Output deliverables as **artifacts** (downloadable reports, schema code, calendars)
- Include all reference material inline (no separate reference file dependencies)
- Use a proactive workflow — Claude analyzes first, asks questions later
- Skills are aware of each other — after completing an analysis, they offer related skills if available
