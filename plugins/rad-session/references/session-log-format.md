# Session Log Format

The session log (`.claude/session-log.md`) is an append-only history of session summaries. It builds institutional memory across many sessions.

**Entries are derived mechanically from HANDOFF.md, not re-synthesized.** `/wrapup` Phase 3 compresses the structured HANDOFF.md it just wrote into log format — Status comes through verbatim, Changes/Decisions/Traps are the corresponding HANDOFF sections compressed to one line each. This avoids a second LLM synthesis pass and keeps the log consistent with the handoff that produced it.

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
2. **15–25 lines per entry, hard cap 30 lines / 1.5 KB.** This is a log, not a narrative. If your entry is over the cap, you're not compressing enough — drop secondary bullets, drop file-by-file descriptions, drop multi-clause rationales.
3. **One sentence per bullet (~150 chars max).** Each Decision is ONE line: name + single-clause WHY. Each Trap is ONE line in compact form `TRIED: X — FAILED BECAUSE: Y` (drop CORRECT APPROACH for the log — that lives in HANDOFF). Each Change is a comma-separated path list with no per-file descriptions.
4. **No file contents.** Reference paths only — never embed code or full file contents.
5. **Separator required.** Each entry ends with `---` for parseability.
6. **Traps only when real.** Only include "Traps" if something actually failed or a non-obvious gotcha was discovered. Don't fabricate traps.
7. **Titles should be meaningful.** "Implemented JWT auth and fixed CORS" beats "Worked on the project."

### Why the per-bullet cap is strict

The session-log is read across many sessions for trend detection (recurring traps, ongoing work threads). At 20 entries × 1 KB target, the whole log fits comfortably in a single read. At 20 entries × 5 KB (what happens without the cap), the log balloons to 100 KB and `/startup` can only read the most recent 3–5 entries — losing the cross-session trend signal entirely. The cap is what makes the log useful at scale.

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
