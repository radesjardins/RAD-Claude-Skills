# rad-session

Session handoff management for Claude Code. Two skills that make moving between chat sessions seamless.

## Skills

| Skill | Trigger | What It Does |
|-------|---------|-------------|
| `/wrapup` | End of session | Captures state to HANDOFF.md, appends session log, prunes CLAUDE.md, prompts for global memory updates |
| `/startup` | Start of session | Reads HANDOFF.md and session log, detects project type, presents a concise briefing |

## How It Works

The plugin maintains three files per project:

| File | Location | Purpose |
|------|----------|---------|
| `CLAUDE.md` | Project root | Permanent rules, conventions, tech stack |
| `HANDOFF.md` | Project root | Current session state (overwritten each `/wrapup`) |
| `.claude/session-log.md` | `.claude/` dir | Session history (append-only, capped at 20 entries) |

**At the end of a session**, run `/wrapup` to:
- Write a structured HANDOFF.md with status, decisions, traps, and open work
- Append a compact entry to the session log
- Prune stale or ephemeral content from CLAUDE.md (with diff shown for review)
- Optionally save insights to global memory

**At the start of the next session**, run `/startup` to:
- Read HANDOFF.md, session log, and CLAUDE.md
- Detect project type and gather live state (git status, branch info)
- Present a concise briefing of where things stand

## Installation

This plugin is part of the [RAD Claude Skills](https://github.com/radesjardins/RAD-Claude-Skills) repo. Enable it in Claude Code settings:

```json
{
  "enabledPlugins": {
    "rad-session@rad-claude-skills": true
  }
}
```

## Works With Any Project

- **Coding projects:** Captures git state, branch info, uncommitted changes
- **Non-coding projects:** Uses filesystem scan for recently modified files
- **New projects:** Creates minimal scaffolding on first `/wrapup`
