# rad-session — Resource-aware session briefings and disciplined wrapup for Claude Code.

Claude Code has built-in memory (CLAUDE.md + native Auto Memory since v2.1.59). **rad-session doesn't replace it — it fills the gaps it doesn't cover:**

1. **Resource Discovery at `/startup`** — parses `.mcp.json`, infers stack CLIs from marker files, extracts `package.json` scripts, and surfaces everything your project has available so you stop reminding Claude about the Supabase MCP, the Coolify CLI, and the `pnpm dev` script every single session.
2. **Disciplined `/wrapup`** — structured HANDOFF.md with a "**What NOT to do**" field for captured failed approaches, active **CLAUDE.md pruning with diff confirmation** (the only tool in the ecosystem that *shrinks* CLAUDE.md instead of growing it), and a protected `## Resources` section that can't be accidentally pruned.
3. **PreCompact safety net** — a hook that fires when Claude Code compacts context, reminding Claude to run `/wrapup` so session state isn't silently lost mid-session.

If you want "write a note so next session can read it," built-in auto-memory already does that. **rad-session is for projects where the *stack* and the *discipline* matter** — where you want Claude to walk into the project already knowing what tools it has, what failed last time, and what's in-flight.

## What's in the plugin

| Skill | Trigger | What It Does |
|-------|---------|-------------|
| `/startup` | Start of session | Reads HANDOFF.md + session log, detects git state, **runs Phase 2.5 Resource Discovery (MCPs, CLIs, scripts, env)**, presents briefing |
| `/wrapup` | End of session | Writes HANDOFF.md with "What NOT to do" field, appends session log (20-entry cap), prunes CLAUDE.md with diff confirmation (**Resources section protected**), surfaces insights for native Auto Memory |
| `/add-resource` | Any time | Appends an MCP, CLI, script, or note to CLAUDE.md's `## Resources` section so `/startup` picks it up next session |

Plus one hook:

| Hook | Event | What It Does |
|------|-------|-------------|
| `precompact` | `PreCompact` | Fires automatically when context compaction begins. Injects a systemMessage telling Claude to run `/wrapup` before the compacted context loses session state. |

## Files the plugin maintains

| File | Purpose | Who writes it |
|------|---------|---------------|
| `CLAUDE.md` | Permanent project rules + **`## Resources` section** (MCPs, CLIs, scripts, notes) | You and `/add-resource`; pruned by `/wrapup` (Resources protected) |
| `HANDOFF.md` | Current session state — status, decisions, **what NOT to do**, open work, insights | `/wrapup` (overwrites each session) |
| `.claude/session-log.md` | Session history, newest first, capped at 20 entries | `/wrapup` (prepends one entry per session) |

Notably **not** managed: `~/.claude/projects/<project>/memory/` — that's owned by Claude Code's native Auto Memory (v2.1.59+). rad-session surfaces insights in the final summary so native auto-memory can pick them up, but never writes to that path.

## Phase 2.5 Resource Discovery (the headline feature)

`/startup` runs a read-only resource-detection pass that parses:

- **`.mcp.json`** and `.claude/settings.json` → MCP servers available to the project
- **Stack marker files** — each implies a CLI you probably use:

  | Marker file(s) | Implied CLI |
  |----------------|-------------|
  | `supabase/config.toml` | `supabase` |
  | `wrangler.toml`, `wrangler.jsonc` | `wrangler` |
  | `netlify.toml` | `netlify` |
  | `vercel.json` | `vercel` |
  | `fly.toml` | `flyctl` |
  | `firebase.json` | `firebase` |
  | `.github/workflows/` | `gh` |
  | `Dockerfile`, `docker-compose.yml`, `compose.yaml` | `docker` |
  | `coolify.json`, `.coolify/` | Coolify deploy target |
  | `terraform/`, `*.tf` | `terraform` |
  | `pulumi.yaml` | `pulumi` |

- **`package.json`** → `packageManager` field + top scripts (`dev`, `build`, `test`, `typecheck`, `lint`, ...)
- **`.env.example`** → variable **names** only (never values)
- **CLAUDE.md `## Resources` section** → the documented source of truth, reconciled against what's actually detected

### Example briefing output

```
Project: my-app
Type: Coding (Next.js + Supabase)
Branch: main (up to date)
Last session: 2026-04-10 — Auth flow complete, billing next

Where we left off:
  - Stripe checkout endpoint wired, webhook handler still TODO
  - Supabase RLS policies applied for users table

Watch out for:
  - Do not mock the Stripe webhook in integration tests — signature verify must hit real code path

Resources available:
  MCPs: supabase, stripe, coolify
  Stack CLIs: supabase, gh, docker
  Scripts (pnpm): dev, build, test, typecheck, lint
  Env template: DATABASE_URL, STRIPE_SECRET_KEY, SUPABASE_ANON_KEY (.env.example)

Ready to continue. What would you like to work on?
```

## Disciplined `/wrapup`

`/wrapup` writes a **structured HANDOFF.md** with sections most handoff tools skip:

- **What NOT to do** — failed approaches and *why they failed*. Prevents the next session from retrying a dead end.
- **Key Decisions** — the *why* behind architecture/approach choices, not just the what.
- **Open Work** — state-of-play as descriptions, never as instructions ("EBirdProvider started, API auth not wired" — not "Next, wire up the eBird API auth").
- **Key Insights** — API quirks, environment gotchas, architectural constraints not in CLAUDE.md.

Then it prunes CLAUDE.md with **diff confirmation** (you see what's about to be removed and can say "undo item X" before anything is saved), **protecting the `## Resources` section** from removal. Nothing else in the Claude Code ecosystem actively shrinks CLAUDE.md — this is the antidote to the "CLAUDE.md keeps growing forever" problem.

## PreCompact safety net (new in 2.1)

When Claude Code's context compaction fires, the `PreCompact` hook injects a systemMessage instructing Claude to run `/wrapup` before anything else. This closes the biggest gap in 2.0: silent context loss when compaction happens mid-session. No config required — the hook ships with the plugin.

## Registering resources manually

When Claude doesn't know about a tool you want it to use, just say:

```
remember this MCP for the project: stripe
```

Or:

```
/add-resource add the supabase CLI to project resources
```

The skill writes to `## Resources` in CLAUDE.md, deduplicates, confirms overwrites, and shows you a diff before saving. Next `/startup` will surface it automatically.

## How this compares to alternatives

| | **rad-session** | Native CC Auto Memory | claude-plugins-official/remember | claude-mem | thepushkarp/handoff |
|---|---|---|---|---|---|
| Resource discovery (MCPs/CLIs/stack) | ✅ **unique** | ❌ | ❌ | ❌ | ❌ |
| Active CLAUDE.md prune w/ diff | ✅ **unique** | ❌ (grows) | compression | ❌ | ❌ |
| "What NOT to do" field | ✅ | ❌ | ❌ | ❌ | partial |
| PreCompact safety net | ✅ (new in 2.1) | ✅ (built in) | ✅ | ✅ | ✅ |
| Zero dependencies / no daemon / no vector DB | ✅ | ✅ | ❌ (Haiku) | ❌ (Chroma) | ✅ |
| Setup cost | plugin install | **zero — built in** | plugin install | plugin install | plugin install |

**When to use rad-session:** you want structured, disciplined session handoffs *and* you want Claude to walk into your project already knowing the available tools and stack resources.

**When you don't need it:** simple single-language projects where CLAUDE.md + native Auto Memory is enough. Don't install what you won't use.

**Complementary:** rad-session pairs well with `basic-memory` MCP if you want semantic recall *across* projects — they're not competing.

## Quick Start

Install via the rad-claude-skills marketplace:
```
/plugin marketplace update rad-claude-skills
/plugin install rad-session@rad-claude-skills
```

At the start of any session:
```
/startup
```

Register resources as you discover them:
```
remember we have the coolify MCP available for this project
```

At the end of the session:
```
/wrapup
```

Works with coding projects (captures git state + stack resources) and non-coding projects (scans recently modified files; still surfaces documented resources).

## Version

**2.1.0** — PreCompact hook for silent-context-loss prevention; Phase 5 stops writing to `~/.claude/projects/<project>/memory/` to avoid collision with native Auto Memory (v2.1.59+); repositioned pitch around Resource Discovery and wrapup discipline.

**2.0.0** — Added `/add-resource` skill, `/startup` Phase 2.5 Resource Discovery, `/wrapup` prune protection for the Resources section.

**1.0.0** — Initial release: `/wrapup` and `/startup` skills.

## License
Apache-2.0
