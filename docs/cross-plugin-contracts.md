# Cross-Plugin Contracts — rad-planner 4.0 + rad-session 5.0

**Status:** Draft (Phase 0 spec, 2026-05-14)
**References:** `doc-conventions.md`, `entry-point-routing.md`, `status-md-schema.md`

How rad-planner 4.0 and rad-session 5.0 coordinate file writes, share configuration, and avoid stepping on each other. Soft-coupled — either plugin works without the other; both honor the contract.

## The single-writer rule

Every file in the canonical structure has exactly **one plugin writer** (with one structured exception — see "Sectioned-writer exception" below). Manual edits by the user are always welcome. The rule constrains automated plugin writes.

The rule's purpose is to prevent the failure modes that drove the v3.0/v4.0 era — HANDOFF.md collision, CLAUDE.md double-ownership, last-writer-wins drift.

## File ownership matrix

| File | Single writer | Notes |
|---|---|---|
| `docs/status.md` | rad-session | Evidence-based at `/wrapup`. rad-planner scaffolds at M6 with placeholders. |
| `docs/planning/archive/*.md` | rad-session | Moves `current.md` here at milestone-shipped confirmation. |
| `docs/vision.md` | rad-planner (creation); human (edits) | `/plan` M6 writes; subsequent runs check guard rail before rewriting. |
| `docs/architecture.md` | rad-planner (creation); human (edits) | Same handling as vision.md. |
| `docs/roadmap.md` | rad-planner (creation); human (edits) | Created if Phase 3 produced >1 milestone. |
| `docs/planning/current.md` | rad-planner (creation); human (edits during execution) | Acceptance criteria checkboxes flipped by human or by /wrapup with evidence. |
| `docs/decisions/README.md` | rad-planner (creation); human (edits) | Created when first ADR is needed. |
| `docs/decisions/NNNN-*.md` | Human; rad-planner creates initial ADRs during /plan if any; both plugins prompt for new ones | rad-session prompts at /wrapup when candidate decisions surface; rad-planner prompts at /plan if a decision is being locked. |
| `.claude/settings.json` | rad-session (creation); human (edits) | Created if Claude in scope. |
| `.codex/config.toml` | rad-session (creation); human (edits) | Created if Codex in scope. |
| `.rad/profile` | Either plugin creates if missing; either updates with user confirmation | Read freely by both. See `.rad/profile` protocol below. |

## Sectioned-writer exception: the operating manual

The operating manual (`CLAUDE.md` and/or `AGENTS.md`) is the one file with two automated writers. The single-writer rule is preserved at the **section level** — both plugins contribute, but to different sections.

### Operating manual section ownership

| Section | Writer |
|---|---|
| Project overview (one-sentence purpose) | rad-planner (Phase 1 Constitution) |
| Read order | rad-planner (Phase 1) |
| Hard boundaries | rad-planner (Phase 1); human edits |
| Engineering rules | rad-planner (Phase 1); human edits |
| Definition of done | rad-planner (Phase 1) |
| Escalate triggers | rad-planner (Phase 1) |
| Commands (install / test / lint / build) | rad-session (during `/startup` bootstrap path, first run only); human edits |
| Compact Instructions (CLAUDE.md only) | rad-session |
| Claude-specific behavior (CLAUDE.md only) | rad-session |
| `@AGENTS.md` import line (CLAUDE.md shim case) | rad-session |

### Section detection

Mechanical — section headers (`## Hard boundaries`, `## Commands`, etc.). Each plugin knows the section names it owns from a fixed list, parses the markdown, and modifies only those sections.

### User-added sections

Any section header in the operating manual that isn't in either plugin's owned-section list is treated as user-owned. Plugins do not modify these sections.

When a plugin processes the operating manual, it explicitly notes which sections it preserved as user-owned in its output:

> "Preserved user sections: `## Project gotchas`, `## Team notes`"

This surfaces the preservation explicitly so the user can verify nothing was missed.

### Conflict resolution

Plugins respect "don't touch the other's sections." If rad-session at `/wrapup` notices a section the other owns has drifted from its source (e.g., Hard Boundaries no longer matches architecture.md's invariants), it flags for user review rather than rewriting.

## Plugin handoff at /plan M6

When `/plan` completes its five-phase conversation and executes doc creation (Milestone 6):

**rad-planner writes:**
- Strategic docs: vision.md, architecture.md, planning/current.md, decisions/README.md (and initial ADRs if any), roadmap.md if recommended
- Operating manual Constitution sections (per the section ownership table above)
- status.md scaffold with placeholders
- `.rad/profile` with mode preference (if not already created)

**rad-session is not invoked during /plan M6.** rad-planner handles all writes directly. This keeps the handoff atomic — /plan produces a complete project state, and the next natural touch point is /wrapup.

**After /plan completes:**
- User can run `/rad-session:wrapup` which populates `status.md` from evidence collected since plan started
- User can run `/rad-session:startup` next session, which reads the complete project state

## Session safety: guard rails

Before any potentially-destructive or unexpected operation, the plugin surfaces the impact and asks for confirmation. The principle: not "should I run?" but "running this will do X — continue?"

Specific guard-rail moments:

### 1. Pre-existing strategic doc on /plan M6

If vision.md (or any other strategic doc rad-planner is about to write) already exists with non-trivial content, rad-planner prompts:

> "`vision.md` exists with your content. Overwrite, append, or skip?"

Three-option menu. User picks.

### 2. Operating manual exists during `/startup` bootstrap

If CLAUDE.md or AGENTS.md exists with substantial content (>500 bytes, more than residue from Claude Code's or Codex's built-in `/init`), rad-session prompts:

> "`CLAUDE.md` exists with N lines. Adding `## Commands` and `## Compact Instructions` sections. Preserved your existing sections: `## Project gotchas`. Continue?"

### 3. /wrapup with no work detected

If no commits, no changed files, and no plan-task changes since last status update:

> "No work detected since last wrapup. Nothing to wrap up — exit, or run anyway to refresh timestamps?"

Default is to exit. Forcing a noise update erodes status.md's evidence quality.

### 4. Mode preference change

If the user (or the plugin) is about to flip `.rad/profile`'s mode setting:

> "Switching mode from mentor to dev. This changes how /wrapup surfaces decisions. Confirm?"

### 5. Per-branch status opt-in

When the active-hybrid detection prompts for per-branch mode:

> "I see multiple active branches: [list]. Enabling per-branch status will rename `docs/status.md` to `docs/status-<current-branch>.md` and scaffold others at next /wrapup. Continue?"

### 6. Merged-branch status cleanup

When a merged branch still has a status file:

> "Branch `feature-x` was merged 2 days ago. Remove `docs/status-feature-x.md`? (Y/n/never-ask)"

The "never-ask" option sets `.rad/profile` to auto-clean merged-branch statuses silently in future runs.

### 7. Any `.rad/profile` write

Updates display a diff before applying:

> "Updating `.rad/profile`:
>   mode: mentor → dev
> Confirm?"

The pattern across all guard rails: surface the specific impact, not a generic "are you sure?" The user can always proceed, but they know what's happening.

## `.rad/profile` protocol

**Location:** `<project-root>/.rad/profile`

**Format:** TOML.

**Contents (minimum):**

```toml
# rad-planner / rad-session project profile
mode = "mentor"               # or "dev"
agent_scope = "claude_and_codex"  # or "claude_only", "codex_only"
multi_branch_status = false   # true when per-branch status is opted in
```

Additional keys allowed for future extensions; both plugins ignore unknown keys.

**Read behavior:** both plugins read on every skill invocation. No caching across invocations.

**Write behavior:** either plugin can write, with user confirmation per the guard-rail principle. Writes are atomic — read full file, modify, write full file. No partial updates.

**Conflict resolution:** not needed under normal use because plugins run sequentially. If concurrent invocations somehow happen, last-writer-wins for the file as a whole.

**First creation:** whichever plugin runs first creates the file. /plan M6 creates it with all known fields populated; `/startup`'s bootstrap path (first run) creates it with whatever fields it knows about and defaults the rest.

## Read coordination

Both plugins read freely from any file in the project. No locks needed because reads are non-mutating.

**Stale-read mitigation:**
- Plugins always read fresh from disk on each skill invocation
- Within a single skill invocation, file content is read once at start and treated as the snapshot for that invocation

## Plugin interaction edge cases

**No `status.md` scaffold exists when /plan runs.** rad-planner creates the scaffold during M6 directly. Doesn't depend on rad-session's `/startup` bootstrap having run first.

**rad-planner adds a new strategic doc during a re-run** (e.g., roadmap.md goes from absent to present). rad-session reads it on next /startup like any other doc. No special handoff needed.

**User pre-writes vision.md (or other strategic doc) before running /plan.** Per Phase 0 lock, /plan asks: overwrite, append, or skip. User picks.

**/plan running while /wrapup is in progress.** Undefined behavior — but realistic only by user accident. File-level single-writer rule prevents corruption. Plugin runs are sequential in practice.

**`/startup` bootstrap runs after /plan M6.** rad-session's bootstrap path (in `/startup` Phase 0.5, first run only) detects existing operating manual (with rad-planner's Constitution content) and only adds Operational sections (Commands, Compact Instructions) if those sections are empty. Honors the section-level single-writer rule.

**Project has non-standard operating manual filename** (e.g., `GUIDE.md` instead of `CLAUDE.md`). rad-session detects via heuristic — looks for the characteristic "Agent Operating Manual" header or `@AGENTS.md` imports — and treats it as the manual. Does not impose canonical naming on existing projects. Per Phase 0 lock: roll with what's there.

## Soft coupling

Either plugin can be installed without the other. The contract describes how they coordinate when both are present.

- **rad-planner alone:** writes strategic docs; doesn't expect rad-session to populate status.md. If status.md exists with scaffold content but no evidence-based updates, that's fine. User can populate manually or install rad-session later.
- **rad-session alone:** reads whatever exists; if no plan or strategic docs exist, surfaces the gap as a soft recommendation ("no project plan detected — recommend `/rad-planner:plan`"). Doesn't refuse to function; the doorman doesn't refuse to open the store just because some inventory is missing.

The contract above is honored by both plugins when both are present, and gracefully degraded by each plugin when run solo.
