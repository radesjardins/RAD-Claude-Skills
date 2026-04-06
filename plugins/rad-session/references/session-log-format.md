# Session Log Format

The session log (`.claude/session-log.md`) is an append-only history of session summaries. It builds institutional memory across many sessions.

## Entry Format

```markdown
## YYYY-MM-DD — [Brief title of what was done]
**Status:** [one-line project state]
**Changes:** [file list or high-level summary]
**Decisions:** [key choices made, if any]
**Traps:** [what to avoid — only if something failed or a gotcha was discovered]
---
```

## Rules

1. **Newest first.** New entries prepend to the top of the file.
2. **15-25 lines per entry.** This is a log, not a narrative.
3. **No file contents.** Reference paths only — never embed code or full file contents.
4. **Separator required.** Each entry ends with `---` for parseability.
5. **Traps only when real.** Only include "Traps" if something actually failed or a non-obvious gotcha was discovered. Don't fabricate traps.
6. **Titles should be meaningful.** "Implemented JWT auth and fixed CORS" beats "Worked on the project."

## Maintenance

The `/wrapup` skill manages log size:

- **Cap:** 20 entries maximum
- **Trimming:** Oldest entries (bottom of file) are removed when cap is exceeded
- **Trap promotion:** Before trimming, recurring traps (appeared 3+ times) are promoted to CLAUDE.md as permanent rules
- **Notification:** User is told what was trimmed and what was promoted

## Example

```markdown
## 2026-04-05 — Implemented DataProvider abstraction
**Status:** Phase 2 in progress — MapboxProvider working, EBirdProvider started
**Changes:** `src/providers/data-provider.ts` (new), `src/providers/mapbox-provider.ts` (new), `src/types/index.ts` (updated)
**Decisions:** Used abstract class over interface for DataProvider — shared caching logic justified it
**Traps:** eBird API rate limits at 100 req/hr — must throttle; don't use fetch directly, go through DataProvider.query()
---

## 2026-04-04 — Set up project scaffolding and design system
**Status:** Phase 1 complete — scaffolding, routing, and design tokens in place
**Changes:** Initial project setup — 14 files created
**Decisions:** Chose Next.js App Router over Pages — server components needed for map data
---
```
