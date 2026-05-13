# File Conventions — RAD 8-Doc Standard

Canonical specification for the documents that rad-session and rad-planner read, write, and prune. This file is the single source of truth — both plugins reference it; neither plugin is required to be installed for the convention to apply.

The standard defines **eight project documents** organized in three tiers (strategic, operational, session), plus two machine-readable artifacts (`tasks.md`, `.planner/state/*.json`) and one transient handoff artifact (`CLAUDE-FRAGMENT.md`). Every file has exactly one plugin owner — the **single-writer rule** prevents collision.

## The Three-Tier Model

```
Strategic   (set at project genesis, rarely change)
  PRD.md             — what we're building and why
  ARCHITECTURE.md    — how it fits together
  ASSUMPTIONS.md     — what's true about reality that isn't obvious in code

Operational (evolve with the work)
  DECISIONS.md       — choices made, why, and what they superseded
  PLAN.md            — milestones, steps, checkpoints

Session     (continuity across sessions)
  CLAUDE.md          — permanent rules + @-imports of strategic docs
  HANDOFF.md         — latest session state, overwritten each /wrapup
  .claude/session-log.md — capped history of recent sessions
```

Information flows between tiers: recurring traps in the session log get promoted into CLAUDE.md; ephemeral state in CLAUDE.md gets pushed down to HANDOFF.md; durable choices surfaced during sessions get appended to DECISIONS.md.

## Document Index

| File | Tier | Owner | Target length | Lifecycle | Git |
|---|---|---|---|---|---|
| `PRD.md` | Strategic | rad-planner `/plan` | 50–150 lines | Revised, not appended | Yes |
| `ARCHITECTURE.md` | Strategic | rad-planner `/plan` | 100–300 lines | Revised in place | Yes |
| `ASSUMPTIONS.md` | Strategic | rad-planner `/plan` + rad-session `/wrapup` (prompt) | 20–80 lines | Append + invalidate-mark | Yes |
| `DECISIONS.md` | Operational | rad-planner `/plan` + rad-session `/wrapup` (prompt) + manual | 50–500 lines | Append-only with supersession | Yes |
| `PLAN.md` | Operational | rad-planner `/plan`, `/status` | 100–400 lines | Updated as work progresses | Yes |
| `CLAUDE.md` | Session | rad-session `/init`, `/add-resource`, `/wrapup` | ≤150 lines | Pruned each wrapup | Yes |
| `HANDOFF.md` | Session | rad-session `/wrapup` only | 30–80 lines | Overwritten each session | Yes |
| `.claude/session-log.md` | Session | rad-session `/wrapup` | 30 lines / 1.5 KB per entry, 20-entry cap | Append (newest first), trim oldest | Yes |
| `tasks.md` | Machine | rad-planner `/plan`, `/status` | Unbounded | Updated per task state change | Yes |
| `.planner/state/*.json` | Machine | rad-planner (run-internal) | Unbounded | Per-run, resumable | Optional |
| `CLAUDE-FRAGMENT.md` | Transient | rad-planner `/plan` (writer) → rad-session `/init` (consumer) | 10–30 lines | Deleted by `/init` after merge | No |

**Location:** all eight project documents and `tasks.md` live at the **project root**, alongside `README.md` / `LICENSE`. Machine state lives under `.claude/` and `.planner/`. The split heuristic: if a human visiting the repo would want to read it to understand the project, it's at root; if it's plugin state, it's hidden.

## Strategic Tier

### PRD.md

- **Created by:** rad-planner `/plan` Phase 6 (from Phase 1 Discovery output).
- **Maintained by:** rad-planner `/plan` (regenerated on `/plan --reboot`), or manually edited between planning sessions.
- **Target length:** 50–150 lines.
- **Update triggers:** scope change, success-criteria change, new constraint discovered that reshapes the product. `/plan --reboot` archives the prior PRD to `PRD.md.pre-reboot` before overwriting.
- **Pruning rules:** revise sections in place; do not append a changelog tail. Historical versions are recoverable via git history (and `*.pre-reboot` archives for reboot events).

### ARCHITECTURE.md

- **Created by:** rad-planner `/plan` Phase 6 (from Phase 2 stack-advisor output + Phase 5 architecture decisions).
- **Maintained by:** rad-planner `/plan` (regenerated on `/plan --reboot`), or manually edited as the architecture evolves.
- **Target length:** 100–300 lines. Component diagrams count toward the budget; if they push past 300, move them to `ARCHITECTURE-DIAGRAMS.md`.
- **Update triggers:** new component, removed component, integration boundary changed, deprecation of an existing pattern.
- **Pruning rules:** revise in place. When a major restructuring lands, the prior version is captured via git history; `/plan --reboot` produces an `ARCHITECTURE.md.pre-reboot` archive.

### ASSUMPTIONS.md

- **Created by:** rad-planner `/plan` Phase 1 (interview question explicitly asks for non-obvious truths about the project's reality).
- **Maintained by:** rad-planner `/plan` (`/plan --reboot` re-prompts), rad-session `/wrapup` Phase 3.5 (when a new assumption is tagged during a session), and manual edits.
- **Target length:** 20–80 lines. Aim for tight one-line entries.
- **Update triggers:** discovering a new latent assumption, an existing assumption becoming false, switching project mode (e.g., "no users yet" → "production users").
- **Pruning rules:** when an assumption invalidates, mark it `~~Invalidated YYYY-MM-DD — <reason>~~` rather than deleting. Keeps an audit trail of what was once true. Annual review is reasonable; not automated.

## Operational Tier

### DECISIONS.md

- **Created by:** rad-planner `/plan` Phase 6 (initial entries from Phase 2 stack rationale + Phase 4 risk-assessor verdicts).
- **Maintained by:** rad-planner `/plan` (adds entries on `/plan --reboot`), rad-session `/wrapup` Phase 3.5 (prompts to append decisions tagged during a session), and manual edits.
- **Target length:** 50–500 lines while in index-style. Above ~500 lines, prompt to convert to ADR layout under `/decisions/NNNN-slug.md`.
- **Update triggers:** any architecture, tooling, scope, or interface choice with non-trivial downstream impact.
- **Pruning rules:** **append-only**. Entries are numbered sequentially (`0001`, `0002`, …). Superseded decisions stay in the file with their status updated to `**Status:** Superseded by 0042 (reboot 2026-05-13)` or similar — the new entry's sequence number is the cross-reference. Never delete a decision; supersession preserves the history.

**Entry format:**

```markdown
## 0007 — 2026-04-25 — Switched ingress from Traefik to Caddy

**Status:** Active

**Context:** [why this came up]

**Decision:** [what was chosen]

**Consequences:** [what we accept / give up]
```

**ADR threshold escalation:** when DECISIONS.md crosses ~500 lines, plugins prompt independently to convert. The conversion moves each entry to `decisions/NNNN-slug.md` and replaces the body with an index. Supersession references remain numeric — `Superseded by 0042` resolves to `decisions/0042-*.md` after conversion.

### PLAN.md

- **Created by:** rad-planner `/plan` Phase 6 (from Phase 3 milestones + Phase 5 implementation steps + checkpoints).
- **Maintained by:** rad-planner `/plan`, `/status` (task-state updates), an executor walking the plan, and manual edits at milestone boundaries.
- **Target length:** 100–400 lines. If a single project's PLAN exceeds 400 lines, that's a signal to split by milestone (`PLAN.md` index + `plans/M1.md`, `plans/M2.md`, …).
- **Update triggers:** task state change (`[ ]` → `[IN PROGRESS]` → `[DONE]`), milestone boundary, scope adjustment, new task added.
- **Pruning rules:** completed tasks stay marked `[DONE]` in place. Completed milestones can be moved to a "Completed milestones" section at the bottom for readability. Don't delete — the plan-vs-actual record is useful.

## Session Tier

### CLAUDE.md

- **Created by:** rad-session `/init` (scaffolded with detected stack + Resources section; merges `CLAUDE-FRAGMENT.md` if present).
- **Maintained by:** rad-session `/init` (additive merges on re-run), `/add-resource` (Resources section appends), `/wrapup` (prune phase, with Resources section protected).
- **Target length:** ≤150 lines. Every line should earn its place — test each with *"Would removing this cause Claude to make a mistake in the next session?"* If no, prune.
- **Content:** permanent rules, conventions, tech stack, build commands, non-obvious architectural constraints, `## Resources` section (MCPs/CLIs/scripts/notes), `@-import` block linking to the strategic docs.
- **NOT for:** session state, current work-in-progress, TODOs, decisions still being deliberated, temporary workarounds since resolved.
- **Pruning rules:** `/wrapup` auto-prunes when CLAUDE.md has changed since the last wrapup. The Resources section is **protected** — never removed automatically. Ephemeral state migrates down to `HANDOFF.md`; recurring traps (3+ sessions) get promoted into CLAUDE.md itself.

### HANDOFF.md

- **Created by:** rad-session `/wrapup` (overwrites each session).
- **Maintained by:** rad-session `/wrapup` only. No other plugin writes here. `/checkpoint` does **not** write HANDOFF.md (single-writer rule).
- **Target length:** 30–80 lines depending on session complexity; bullets ≤ 3 sentences (~300 chars); total ≤ 100 lines / 8 KB hard cap.
- **Update triggers:** every `/wrapup`. Always reflects the latest session only.
- **Pruning rules:** overwritten in full each wrapup. No history kept here — that's the session log's job.
- **Read by:** `/startup` at the beginning of the next session.

### .claude/session-log.md

- **Created by:** rad-session `/init` (header line) or `/wrapup` (first run if `/init` skipped).
- **Maintained by:** rad-session `/wrapup` (prepend one entry per session).
- **Target length per entry:** 15–25 lines preferred; bullets ≤ 1 sentence (~150 chars); hard cap 30 lines / 1.5 KB per entry.
- **Update triggers:** every `/wrapup`. Entry derived mechanically from the HANDOFF.md just written (no second LLM synthesis pass).
- **Pruning rules:** append-only (newest first), capped at 20 entries. Oldest trimmed automatically by `/wrapup` Phase 3.B (mandatory, Bash-gated). Recurring traps (same FAILED line in 3+ entries) get promoted to CLAUDE.md.
- **Read by:** `/startup` (last 3–5 entries for pattern context).

## Machine-Readable Artifacts

### tasks.md

- **Created by:** rad-planner `/plan` Phase 6.
- **Maintained by:** rad-planner `/plan`, `/status`, or an executor as task states change.
- **Format:** DAG-based — hierarchical task IDs (`S01`, `S01.1`, …), dependency arrays, complexity scores, validation criteria, rollback notes. Validated by `scripts/plan-lint.py`.
- **Update triggers:** task state change, new task added, dependency added/removed.
- **Pruning rules:** completed tasks stay in place with `[DONE]` state. The DAG must always validate clean (no cycles, no phantom deps).

### .planner/state/*.json

- **Created by:** rad-planner skills (`plan`, `review-plan`, `evaluate-stack`) during a run.
- **Maintained by:** the same skill, resumed via `--resume <run-id>`.
- **Format:** shared schema documented in `plugins/rad-planner/references/context-management.md`.
- **Git:** optional. Most projects gitignore `.planner/state/`; commit only if collaborative resume is needed.

## Transient Artifacts

### CLAUDE-FRAGMENT.md

- **Created by:** rad-planner `/plan` Phase 6 (emits an `@-import` block listing PRD / ARCHITECTURE / ASSUMPTIONS / DECISIONS / PLAN).
- **Consumed by:** rad-session `/init` — merges the imports into CLAUDE.md, then **deletes the FRAGMENT**.
- **Target length:** 10–30 lines.
- **Lifecycle:** ephemeral. If absent at `/init` time, `/init` falls through to auto-generating the import block from detected strategic docs, or to placeholder pointers if no strategic docs exist.
- **Git:** no. Treat as build-output. Gitignore optional but encouraged.

## Single-Writer Rule

Every file in this standard has exactly **one plugin writer**. Manual edits are always welcome — the rule only constrains automated plugin writes.

| File | Single writer |
|---|---|
| `PRD.md` / `ARCHITECTURE.md` / `ASSUMPTIONS.md` / `DECISIONS.md` / `PLAN.md` | rad-planner `/plan` |
| `tasks.md` | rad-planner `/plan` (state updates via `/status` count as same writer) |
| `CLAUDE.md` | rad-session (`/init`, `/add-resource`, `/wrapup`) |
| `HANDOFF.md` | rad-session `/wrapup` |
| `.claude/session-log.md` | rad-session `/wrapup` |
| `CLAUDE-FRAGMENT.md` | rad-planner `/plan` (writer) → consumed-and-deleted by rad-session `/init` |

`/wrapup` may **prompt** the user to append to DECISIONS.md or ASSUMPTIONS.md when in-session tagging surfaces relevant content, but the user's `y`-confirm is what authorizes the write — those entries are user-authored, not plugin-authored.

## Cross-Machine Sync

Cross-machine continuity (PC ↔ GitHub ↔ Laptop) depends on the session-tier files being committed to git:

- `/init` Step 7.5 detects `.claude/` gitignore rules and proposes a `!.claude/session-log.md` exception so the log gets committed.
- `/wrapup` Phase 6 auto-commits HANDOFF.md, session-log.md, and CLAUDE.md (only if Phase 4 modified it). Prompts for push; `--push` skips the prompt, `--no-push` commits locally only.
- `/startup` Phase 0 fetches origin and prompts to pull when behind, *before* reading any handoff file. `--auto-pull` skips the prompt, `--no-pull` skips the sync entirely.

Strategic-tier docs (PRD / ARCHITECTURE / ASSUMPTIONS / DECISIONS / PLAN) are also git-tracked. They sync via the same mechanism but aren't part of the auto-commit set — they're either committed during a planning session or by hand. `tasks.md` is part of the planning session commit.

## First-Run Behavior

When rad-session `/init` runs on a project for the first time:

1. Create `.claude/` directory if missing.
2. Look for `CLAUDE-FRAGMENT.md`. If present, merge its `@-imports` into the generated CLAUDE.md and delete the FRAGMENT.
3. If absent, auto-generate the import block from detected strategic docs (PRD.md, ARCHITECTURE.md, etc.) at project root.
4. If no strategic docs exist, scaffold CLAUDE.md with placeholder pointers: `@PRD.md — run /rad-planner:plan to create`.
5. Create `.claude/session-log.md` with a header line.
6. Do **not** create HANDOFF.md — that's `/wrapup`'s job.

When rad-planner `/plan` runs on a project for the first time:

1. Phase 1 Discovery interview explicitly captures ASSUMPTIONS material.
2. Phase 6 writes PRD.md / ARCHITECTURE.md / ASSUMPTIONS.md / DECISIONS.md / PLAN.md / tasks.md at project root.
3. Phase 6 also writes CLAUDE-FRAGMENT.md for the next `/init` run to consume.
4. Does **not** write CLAUDE.md, HANDOFF.md, or `.claude/session-log.md` — those belong to rad-session.

## Why this standard exists

Three failure modes drove the design:

- **HANDOFF.md collision** (pre-4.0): both `/wrapup` and `/checkpoint` wrote HANDOFF.md with different templates. Single-writer rule eliminates this.
- **CLAUDE.md double-ownership** (pre-4.0): rad-session's `/init` and rad-planner's `/generate-project-config` produced different structures at the same path. `/generate-project-config` is retired in rad-planner 3.0; `/plan` emits the FRAGMENT instead.
- **Mega-doc opacity** (pre-3.0 rad-planner): a single `implementation_plan.md` with 7 sections was harder to query selectively than five focused files with clear ownership.

The 8-doc split makes each concern individually addressable — and lets agents load only what they need per task.
