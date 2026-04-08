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

**As a Skill (recommended):** Go to **Settings > Customize > Skills** on Claude.ai. Upload the `.zip` from the skill's folder. It activates automatically in any conversation.

**As Project Knowledge:** Add `SKILL.md` and the `resources/` files to a Claude.ai Project.

**As a conversation attachment:** Attach `SKILL.md` to any conversation for one-off use.

**As an API system prompt:** Use the SKILL.md content as a system prompt when calling the Claude API.

## Available Skills

| Folder | ZIP Name | Description |
|--------|----------|-------------|
| `rad-seo-aeo-reviewer/` | `rad-seo-aeo-reviewer.zip` | SEO audit, competitor analysis, content strategy, AI visibility, schema markup |
| `rad-brainstormer/` | `rad-brainstormer.zip` | Facilitated ideation, evaluation frameworks, creative unblocking, design sprint |
| `rad-writer/` | `rad-writer.zip` | Domain-smart writing, AI pattern avoidance, voice profiling across 9 content types |

## Conventions

- Each skill gets its own folder: `skills/<skill-name>/`
- Each folder has `README.md`, `SKILL.md`, and `resources/`
