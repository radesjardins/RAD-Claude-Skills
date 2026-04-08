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

There are several ways to use these skills on Claude.ai:

### Option 1: Project Knowledge (recommended for repeated use)
1. Go to [claude.ai](https://claude.ai) and create a new **Project**
2. Open the Project settings and add **Project Knowledge** files
3. Upload the skill `.md` file(s) — they persist across all conversations in that project

### Option 2: Conversation attachment (one-off use)
1. Start a new conversation on claude.ai
2. Attach the skill `.md` file(s) to your message
3. Claude will follow the skill instructions for that conversation

### Option 3: API system prompt
Use the skill content as a system prompt when calling the Claude API directly.

Each skill is self-contained. Upload or provide one, two, or all skills from a folder — no dependencies between files.

## Available Skills

| Folder | Source Plugin | Skills |
|--------|-------------|--------|
| `rad-seo/` | rad-seo-optimizer | SEO audit, competitor analysis, strategy, and AI visibility optimization |
| `rad-brainstorm/` | rad-brainstormer | Facilitated ideation, evaluation frameworks, creative unblocking, and design sprint |
| `rad-writer/` | rad-writer | Domain-smart writing, AI pattern avoidance, voice profiling across 9 content types |

## Conventions

- Each adapted plugin gets its own folder: `skills/<plugin-name>/`
- Each folder has a `README.md` with setup instructions and example prompts
- Skill files are named `<plugin-name>-<focus>.md`
- Optional extras (templates, reference docs) go in `optional/`
- Skills are fully self-contained — no cross-file dependencies
