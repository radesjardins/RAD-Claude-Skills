# RAD Claude Skills

## Tech Stack
- Standalone Claude Code skills and plugins (markdown-based, no build step)
- Git repository, Apache 2.0 license
- Cross-platform install scripts (bash + PowerShell)

## Conventions
- Plugins live in `plugins/`, standalone skills in `skills/`
- Each skill has a `SKILL.md` with frontmatter (name, description, argument-hint, allowed-tools)
- Reference docs go in `references/`, workflows in `workflows/`, templates in `templates/`
- Design specs go in `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
