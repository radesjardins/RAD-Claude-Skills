# rad-session — Never lose context between Claude Code sessions again.

Every time you start a new Claude Code session, you start fresh. rad-session fixes that with two commands: `/wrapup` captures exactly where you left off — decisions made, traps to avoid, open work — and `/startup` reads it back at the start of the next session so you're oriented in seconds instead of minutes.

## What You Can Do With This

- End a session with a structured handoff that captures status, key decisions, known traps, and next steps
- Start the next session with a concise briefing — git state, branch info, and where you left off
- Keep CLAUDE.md clean over time — `/wrapup` prunes stale content automatically (shows you the diff first)

## How It Works

| Skill | Trigger | What It Does |
|-------|---------|-------------|
| `/wrapup` | End of session | Writes HANDOFF.md, appends session log, prunes CLAUDE.md, prompts for memory updates |
| `/startup` | Start of session | Reads HANDOFF.md + session log, detects project state, presents briefing |

The plugin maintains three files per project:

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Permanent rules, conventions, tech stack |
| `HANDOFF.md` | Current session state (overwritten each `/wrapup`) |
| `.claude/session-log.md` | Session history (append-only, capped at 20 entries) |

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-session
```

At the end of any session:
```
/wrapup
```

At the start of the next:
```
/startup
```

Works with coding projects (captures git state) and non-coding projects (scans recently modified files).

## License
Apache-2.0
