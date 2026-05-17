# Session Contract Template — embedded in `current.md`

This is the canonical format for the **Session contract** sub-section that rad-planner v4.8+ embeds inside `docs/planning/current.md` at M6. The contract is the build-readiness gate's per-milestone anchor; rad-session v5.5+ renders it at `/startup` as the first user-visible block.

## Why embedded, not a separate file

Decided in spec Q4 (2026-05-16): the contract lives **inside `current.md`** as a sub-section, not in a separate `docs/planning/contract.md`. Rationale:

- Single source of truth — when the milestone changes, the contract changes in one place
- No sync problem between two files
- One fewer file the user has to think about
- rad-session can read the contract from the same `current.md` it already reads

## Where in `current.md`

Place the Session contract sub-section **near the top of the active milestone**, after `## Objective` and before `## Acceptance criteria`. The level-3 heading `### Session contract` lives inside the milestone's section (or as a top-level `## Session contract` if `current.md` is single-milestone).

Recommended order:

```
## Objective
<one-sentence objective>

## Current milestone
<milestone id + theme>

### Session contract
<the 7-field block — see Format below>

## Acceptance criteria
<checkboxes>

## Validation commands
<commands>

## Guardrails
<what not to change>

## User-visible behavior
<observable outcome>

## Stop conditions
<bulleted list>

## Notes for the next session
<handoff notes>
```

## Format

```markdown
### Session contract

- **Current milestone:** <milestone id and short theme — derived from the "Current milestone" section>
- **Goal:** <one-sentence objective — derived from the "Objective" section, tightened to fit on one line>
- **In scope:** <2-5 bullets — derived from "Acceptance criteria" titles or "Planned changes"; what the agent IS implementing this milestone>
- **Out of scope:** <2-5 bullets — derived from milestone-specific exclusions + relevant entries from vision.md non-goals>
- **Files likely touched:** <2-7 bullets — derived from "Planned changes" section; paths or path patterns>
- **Acceptance criteria:** <reference to the "Acceptance criteria" section below + summary count, e.g., "5 ACs below — see § Acceptance criteria">
- **Stop and ask if:** <2-5 bullets — derived from "Stop conditions" section, shortened to one line each>
```

## Sizing

- Total: aim for 12-20 lines of contract content
- Each bullet: one line, under 100 characters
- The full contract should fit on one screen

If the contract exceeds 25 lines when rendered, rad-session's `/startup` truncates the rendered block at 25 lines and appends `… (full contract in docs/planning/current.md)`. So sizing the contract under that threshold keeps the briefing tight.

## Derivation rules

The contract is **derived** from the canonical sections, not authored separately. The intent is that updating `current.md` keeps the contract honest automatically. Specifically:

| Contract field | Source |
|---|---|
| Current milestone | `## Current milestone` section verbatim |
| Goal | `## Objective` section, tightened to one sentence |
| In scope | `## Acceptance criteria` titles (the "what" of each AC) + `## Planned changes` if more specific |
| Out of scope | Project-specific exclusions for this milestone + selected entries from `vision.md` non-goals |
| Files likely touched | `## Planned changes` paths/patterns |
| Acceptance criteria | Reference + count |
| Stop and ask if | `## Stop conditions` section, shortened |

At M6, rad-planner derives the contract from the M4 quality_gates_draft and the M2 scope_draft. The user reviews the contract during M5 (Doc-Set Recommendation) along with the rest of the plan, and confirms or adjusts before write.

## What does NOT belong in the contract

- New information not derivable from the other sections — if it's worth saying, it goes in the canonical section first
- Implementation details — those live in `## Planned changes` and `## Validation commands`
- Risk language — that's `## Stop conditions` and `## Risks`
- ADR rationale — that's `docs/decisions/`

The contract is a **render**, not a new source of truth.

## Idempotency on re-run

When `/plan --improve` or `/plan --pivot` regenerates `current.md`, the Session contract is regenerated from the updated canonical sections. The user's edits to the contract bullets are preserved per the standard rad-planner doc guard rail (overwrite/append/skip prompt for pre-existing strategic docs), but the derivation rules above are the canonical source — if the user wants permanent custom contract text, they should edit the underlying canonical section instead.

## Graceful degradation in rad-session

If `current.md` exists but has no `### Session contract` sub-section (e.g., older plan from before v4.8), rad-session skips the contract render silently. No warning, no placeholder — the user can run `/plan --improve` to add the contract to existing plans, or hand-write the section.
