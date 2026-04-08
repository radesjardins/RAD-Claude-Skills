# Claude.ai Skills

Skills in this folder are designed for **Claude.ai** (claude.ai). They give Claude specialized capabilities when provided as context — whether through Project Knowledge, conversation attachments, or API system prompts.

## How This Differs from Plugins

The `plugins/` folder contains skills built for **Claude Code CLI**, **Claude Desktop**, and **Claude Cowork** — environments with filesystem access, subagents, and automatic skill routing via SKILL.md frontmatter.

Claude.ai has different strengths:
- **Web search and URL fetching** — analyze live websites directly
- **GitHub connector** — read repository files when connected
- **Artifacts** — produce downloadable reports, code blocks, and structured documents
- **Project Knowledge** — uploaded files stay in context across all conversations in a project

These skills are rewritten to maximize those capabilities and work without filesystem tools or subagents.

## How to Use

Each skill is packaged as a `.zip` in its folder's `dist/` directory.

**As a Skill (recommended):** Go to **Settings > Customize > Skills** on Claude.ai. Upload the `.zip`. It activates automatically in any conversation.

**As Project Knowledge:** Add the `.md` files from the `*-complete/` folder to a Claude.ai Project.

**As a conversation attachment:** Attach `SKILL.md` to any conversation for one-off use.

**As an API system prompt:** Use the SKILL.md content as a system prompt when calling the Claude API.

## Available Skills

| Folder | Source Plugin | Skills |
|--------|-------------|--------|
| `rad-seo/` | rad-seo-optimizer | SEO audit, competitor analysis, strategy, and AI visibility optimization |
| `rad-brainstorm/` | rad-brainstormer | Facilitated ideation, evaluation frameworks, creative unblocking, and design sprint |
| `rad-writer/` | rad-writer | Domain-smart writing, AI pattern avoidance, voice profiling across 9 content types |

## Conventions

- Each adapted plugin gets its own folder: `skills/<plugin-name>/`
- Each folder has a `README.md` with setup instructions and example prompts
- The complete skill lives in `<plugin-name>-complete/` with `SKILL.md` + `resources/`
- Importable ZIP is in `dist/` (gitignored — regenerable from source)
