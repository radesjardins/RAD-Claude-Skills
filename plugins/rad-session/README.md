# rad-session — Never lose context between Claude Code sessions again.

Every time you start a new Claude Code session, you start fresh. rad-session fixes that with three commands: `/wrapup` captures exactly where you left off — decisions made, traps to avoid, open work — `/startup` reads it back at the start of the next session **and detects what resources your project has**, and `/add-resource` lets you register MCPs, CLIs, and tools so Claude never forgets they're available.

## What You Can Do With This

- End a session with a structured handoff that captures status, key decisions, known traps, and next steps
- Start the next session with a concise briefing — git state, branch info, where you left off, **and an active inventory of MCPs, CLIs, and scripts the project uses**
- Register new resources as you go — tell Claude once, and it will remember them on every future `/startup`
- Keep CLAUDE.md clean over time — `/wrapup` prunes stale content automatically (shows you the diff first) while **protecting your Resources section from deletion**

## How It Works

| Skill | Trigger | What It Does |
|-------|---------|-------------|
| `/startup` | Start of session | Reads HANDOFF.md + session log, detects project state **and project resources** (MCPs, CLIs, scripts, env), presents briefing |
| `/wrapup` | End of session | Writes HANDOFF.md, appends session log, prunes CLAUDE.md (**Resources section protected**), prompts for memory updates |
| `/add-resource` | Any time | Appends an MCP, CLI, script, or note to CLAUDE.md's `## Resources` section so `/startup` picks it up next session |

The plugin maintains three files per project:

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Permanent rules, conventions, tech stack, **and `## Resources` section (MCPs, CLIs, scripts, notes)** |
| `HANDOFF.md` | Current session state (overwritten each `/wrapup`) |
| `.claude/session-log.md` | Session history (append-only, capped at 20 entries) |

## Resource Discovery (new in 2.0)

`/startup` now runs a read-only **Phase 2.5 Resource Discovery** pass that detects:

- **MCP servers** — parsed from `.mcp.json` and `.claude/settings.json`
- **Stack CLIs** — inferred from marker files (`supabase/config.toml` → supabase CLI, `wrangler.toml` → wrangler, `fly.toml` → flyctl, `.github/workflows/` → gh, `Dockerfile` → docker, and more)
- **Package manager + scripts** — top scripts from `package.json` plus the correct `pnpm` / `yarn` / `npm` / `bun` invocation
- **Environment template** — variable **names** (never values) from `.env.example`
- **Documented resources** — extracts the `## Resources` section from CLAUDE.md as the authoritative source

Detected and documented resources are reconciled — if you've documented a resource that is no longer present, `/startup` flags it as drift; if a new resource is detected that isn't in CLAUDE.md, it suggests running `/add-resource` to register it.

### Example briefing output

```
Project: my-app
Type: Coding (Next.js + Supabase)
Branch: main (up to date)
Last session: 2026-04-10 — Auth flow complete, billing next

Where we left off:
  - Stripe checkout endpoint wired, webhook handler still TODO
  - Supabase RLS policies applied for users table

Resources available:
  MCPs: supabase, stripe, coolify
  Stack CLIs: supabase, gh, docker
  Scripts (pnpm): dev, build, test, typecheck, lint
  Env template: DATABASE_URL, STRIPE_SECRET_KEY, SUPABASE_ANON_KEY (.env.example)

Ready to continue. What would you like to work on?
```

## Registering Resources

When Claude doesn't know about a tool you want it to use, just tell it:

```
/add-resource remember we have the stripe MCP and the supabase CLI here
```

Or use natural phrasing — the skill triggers on:
- "remember this MCP for the project"
- "add the X CLI to project resources"
- "save this tool to CLAUDE.md"
- "register this resource"

The skill writes to the `## Resources` section in CLAUDE.md (creating it if missing), deduplicates, confirms overwrites, and shows you a diff before saving.

## Prune Protection

`/wrapup`'s CLAUDE.md pruning step has always removed ephemeral state (current work, TODOs, stale references). As of 2.0, it **never touches your `## Resources` section** (or the aliases `## MCP`, `## Tools`, `## CLI Tools`). Individual entries may only be removed if they reference a path or binary that clearly no longer exists — and even then, you're asked to confirm before anything is deleted.

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-session
```

At the start of any session:
```
/startup
```

Add resources as you discover them:
```
/add-resource remember we have the coolify MCP available
```

At the end of the session:
```
/wrapup
```

Works with coding projects (captures git state + stack resources) and non-coding projects (scans recently modified files; still surfaces documented resources).

## Version

**2.0.0** — Added `/add-resource` skill, `/startup` Phase 2.5 resource discovery, and `/wrapup` prune protection for the Resources section.

## License
Apache-2.0
