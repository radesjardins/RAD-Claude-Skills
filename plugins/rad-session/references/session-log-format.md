# session-log.md format (retired in v5.0)

`.claude/session-log.md` is retired as of rad-session 5.0. Its journal role is replaced by `docs/planning/archive/YYYY-MM-DD-MN-slug.md` — one file per shipped milestone, written by `/wrapup` Phase 6 when all acceptance criteria in `docs/planning/current.md` are checked.

The canonical convention lives at:

→ **[`docs/doc-conventions.md`](../../../docs/doc-conventions.md)** — section on `docs/planning/archive/` (canonical source)

## Why the change

v4.0's session-log.md was a flat append-only file capped at 20 entries. Two structural problems:

1. **Per-session granularity was too fine.** Sessions don't map cleanly to milestones — one milestone often spans 5–20 sessions; one session sometimes spans multiple milestones. Per-session entries fragmented the timeline.
2. **20-entry hard cap forced premature trim.** Real projects have more than 20 milestones; the cap was a workaround for fixed-size flat files, not a meaningful boundary.

`planning/archive/` solves both: one file per **shipped milestone** (the right granularity), unlimited count (one file per archive entry), and the filename's date+milestone-number prefix sorts chronologically without scanning content.

## Migrating a v3/v4 project

Run `scripts/migrate-to-v5.py` from the rad-session plugin directory. It archives the old `.claude/session-log.md` to `.rad-archive/<UTC-timestamp>/` for reference. The historical entries are preserved but not migrated into the new archive structure (per-session entries don't map 1:1 to milestones).

## If you're following an old link

The v4.0 session-log format (newest-first, structured per-entry blocks) is preserved in `.rad-archive/<UTC-timestamp>/` of any project that ran the v5.0 migration.
