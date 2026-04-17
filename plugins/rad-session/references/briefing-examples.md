# Briefing Examples

Canonical output formats for `/startup` Phase 3. The startup skill picks one of these three shapes based on what it detected. Follow the structure verbatim — the formatting is load-bearing for scanability.

---

## Full Briefing (HANDOFF.md exists + coding project)

```
Project: [name]
Type: [Coding (stack) | Non-coding]
Branch: [name] ([N ahead, M behind] or [up to date])
Last session: [date] — [status line from HANDOFF.md]

Where we left off:
  - [item from HANDOFF.md]
  - [item from HANDOFF.md]

Watch out for:
  - [trap from HANDOFF.md "What NOT To Do" — preserve TRIED/FAILED BECAUSE/CORRECT APPROACH wording]
  - [recurring trap from session log, if any]

Open work:
  - [item from HANDOFF.md]

[If any resources detected or documented:]
Resources available:
  MCPs: [list from .mcp.json + settings]
  Stack CLIs: [list inferred from marker files]
  Scripts ([pm]): [top scripts from package.json]
  Env template: [names from .env.example]
  [⚠ documented but not found: <items>]
  [Also detected (not in CLAUDE.md): <items>  →  run /add-resource to register]

[If imports resolved non-trivial content:]
Imports: [<path1>, <path2>]

[If uncommitted changes exist:]
Uncommitted changes from last session:
  - [file list from git status]

[If commits made outside last session:]
Changes since last session (not from Claude Code):
  - [commit list]

Ready to continue. What would you like to work on?
```

### Concrete example

```
Project: my-app
Type: Coding (Next.js + Supabase)
Branch: main (up to date)
Last session: 2026-04-10 — Auth flow complete, billing next

Where we left off:
  - Stripe checkout endpoint wired, webhook handler still TODO
  - Supabase RLS policies applied for users table

Watch out for:
  - TRIED: mocking the Stripe webhook in integration tests
    FAILED BECAUSE: signature verification ran against the mock, not real code path
    CORRECT APPROACH: use Stripe CLI `stripe listen` against a real test-mode endpoint

Open work:
  - Stripe webhook handler: scaffolded at src/app/api/webhook/route.ts, signature verify done, event routing pending

Resources available:
  MCPs: supabase, stripe, coolify
  Stack CLIs: supabase, gh, docker
  Scripts (pnpm): dev, build, test, typecheck, lint
  Env template: DATABASE_URL, STRIPE_SECRET_KEY, SUPABASE_ANON_KEY (.env.example)

Ready to continue. What would you like to work on?
```

---

## Stale-handoff auto-refresh variant

When HANDOFF.md is 7+ days old, lead with a staleness note and include the auto-synthesized git-log summary.

```
⚠ Handoff is 12 days old — auto-refreshed from git log.

Project: [name]
Type: [Coding (stack)]
Branch: [name] ([ahead/behind])
Last session (per HANDOFF.md): [date] — [status]

Changes since last session (outside Claude Code):
  - abc1234 fix: resolve billing webhook timeout (2 days ago)
  - def5678 chore: bump deps (5 days ago)
  - [summarize 3–8 commits; collapse runs of trivial commits]

Where we left off:
  - [from HANDOFF.md]

Watch out for:
  - [from HANDOFF.md]

Ready to continue. What would you like to work on?
```

---

## Minimal Briefing (No HANDOFF.md)

```
Project: [name from directory or CLAUDE.md]
Type: [Coding (stack) | Non-coding]
[Branch: [name] — if git project]

No session handoff found — this is either a new project or one that hasn't used /wrapup yet.

[If CLAUDE.md exists:]
From CLAUDE.md: [brief summary of project rules/conventions]

[If any resources detected:]
Resources available:
  MCPs: [list]
  Stack CLIs: [list]
  Scripts ([pm]): [list]

[If git history exists:]
Recent activity:
  - [last 5 commits]

What would you like to work on?
```

---

## Non-Coding Briefing

```
Project: [name]
Type: Non-coding
Last session: [date] — [status from HANDOFF.md]

Where we left off:
  - [items]

Watch out for:
  - [traps]

[If any resources documented/detected:]
Resources available:
  MCPs: [list]
  Tools: [list]

Recently modified files:
  - [file list]

Ready to continue. What would you like to work on?
```
