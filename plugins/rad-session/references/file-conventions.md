# File Conventions

Shared rules that both `/wrapup` and `/startup` follow. These conventions ensure consistency across every project that uses the rad-session plugin.

## File Locations

| File | Location | Created by |
|------|----------|------------|
| `CLAUDE.md` | Project root | User or `/wrapup` (scaffold only) |
| `HANDOFF.md` | Project root | `/wrapup` (overwritten each session) |
| `.claude/session-log.md` | `.claude/` directory | `/wrapup` (prepend per session) |

## CLAUDE.md Standards

- **Max target:** ~150 lines. Prune aggressively — every line should earn its place.
- **Content:** Permanent rules, conventions, tech stack, build commands, non-obvious architectural constraints.
- **NOT for:** Session state, current work in progress, TODOs, temporary workarounds that have been resolved.
- **Test each line:** "Would removing this cause Claude to make mistakes in the next session?" If no, it can go.
- **Ephemeral state migrates to HANDOFF.md.** This is the primary pruning heuristic.

## HANDOFF.md Standards

- **Lifecycle:** Overwritten on each `/wrapup`. Always reflects the latest session only.
- **Content:** Session state, current work, decisions made, failed approaches, modified files, key insights.
- **Target length:** 30-80 lines depending on session complexity.
- **Read by:** `/startup` at the beginning of the next session.

## Session Log Standards

- **Lifecycle:** Append-only (newest first), capped at 20 entries.
- **Content:** Compact per-session entries — status, changes, decisions, traps.
- **Target per entry:** 15-25 lines.
- **Maintenance:** Oldest entries trimmed on `/wrapup`. Recurring traps promoted to CLAUDE.md.
- **Read by:** `/startup` (last 3-5 entries for pattern context).

## First-Run Behavior

When `/wrapup` runs on a project for the first time:

1. Create `.claude/` directory if it doesn't exist
2. Create `HANDOFF.md` from the handoff template
3. Create `.claude/session-log.md` with the first entry
4. If no `CLAUDE.md` exists, create a minimal scaffold:
   ```markdown
   # [Project Name]

   ## Tech Stack
   [Auto-detected or "TBD"]

   ## Conventions
   [To be established]
   ```
5. Do NOT over-generate CLAUDE.md — keep it skeletal so the user fills in what matters

## The Three-Tier Model

```
CLAUDE.md (permanent)     →  Always loaded. Rules that apply to every session.
HANDOFF.md (current)      →  Latest session state. Overwritten each /wrapup.
session-log.md (history)  →  Institutional memory. Grows over time, capped at 20.
```

Information flows upward: recurring traps in the session log get promoted to CLAUDE.md. Ephemeral state in CLAUDE.md gets pushed down to HANDOFF.md. The system self-maintains through regular `/wrapup` usage.
