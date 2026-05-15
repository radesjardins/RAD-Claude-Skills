---
name: init
description: >
  One-time per project. Bootstraps rad-session machinery for v5.0: detects the tech
  stack deterministically (via scripts/detect-stack.py), discovers MCP servers and
  CLIs (via scripts/detect-resources.py), determines agent scope (Claude / Codex /
  both / not sure), scaffolds the operating manual's Operational sections (Commands,
  Compact Instructions, Claude-specific behavior) per the cross-plugin sectioned-
  writer rule, scaffolds docs/status.md for /wrapup to populate from evidence,
  sets .rad/profile, and recommends which rad-* plugins fit the detected stack.
  Trigger when the user says "/init", "init project", "set up rad-session here",
  "bootstrap session", "new project setup", "configure for this project", "set up
  CLAUDE.md or AGENTS.md".

  Strategic docs (vision.md, architecture.md, planning/current.md, decisions/) are
  rad-planner's responsibility per docs/cross-plugin-contracts.md — /init does NOT
  write them, and surfaces a recommendation to run /rad-planner:plan if they're
  missing. Per the sectioned-writer rule for the operating manual, /init writes
  ONLY the Operational sections; Constitution sections (Project, Read order, Hard
  boundaries, Engineering rules, Definition of done, Escalate triggers) are rad-
  planner's at /plan M6.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Project Init — One-Time Bootstrap (v5.0)

Set up a project for rad-session: detect what's there, determine the agent scope, scaffold the operating manual's Operational sections, scaffold docs/status.md, set .rad/profile, and recommend which rad-* plugins fit the detected stack.

**This skill runs ONCE per project.** Re-running is safe (it merges rather than overwrites). The value is at the start.

> **Status:** rad-session 5.0 — released. plugin.json is at 5.0.0; the marketplace ships this workflow. See [`fixtures/`](../../fixtures/) for worked examples across all four agent_scope / mode combinations.

## v5.0 scope reduction

`/init` no longer writes strategic docs. Per the single-writer rule in [`docs/cross-plugin-contracts.md`](../../../../docs/cross-plugin-contracts.md), strategic docs (vision.md, architecture.md, planning/current.md, decisions/) are owned by rad-planner.

The operating manual is a **sectioned-writer exception**:

- **rad-planner** writes the Constitution sections at `/plan` M6 — Project, Read order, Hard boundaries, Engineering rules, Definition of done, Escalate triggers
- **rad-session** (this skill) writes only the **Operational sections** — Commands, Compact Instructions (CLAUDE.md only), Claude-specific behavior (CLAUDE.md only), `@AGENTS.md` shim line (CLAUDE.md shim case)

If Constitution sections are missing, `/init` does not fill them — it surfaces a recommendation to run `/rad-planner:plan`.

## Honest framing

This skill does NOT:
- Install rad-* plugins (recommends; you decide)
- Add MCP servers (detects what's configured)
- Generate framework-specific code
- Decide your tech stack (observes what's there)
- Write strategic docs (rad-planner's job)
- Write Constitution sections of the operating manual (rad-planner's job at `/plan` M6)
- Touch HANDOFF.md (retired in v5.0 — replaced by docs/status.md)
- Create `.claude/session-log.md` (retired in v5.0 — planning/archive/ serves the journal role)

This skill DOES:
- Run two Python scripts deterministically scanning the project
- Determine agent scope (which agents will work in this project)
- Scaffold operating manual Operational sections per agent scope
- Scaffold `docs/status.md` so `/wrapup` can populate from evidence
- Set `.rad/profile` (mode preference, agent scope)
- Run the per-project plugin / MCP bloat audit
- Surface gaps and recommend follow-ups

## Cross-model note

Works identically across Opus 4.7, Sonnet 4.6, and Haiku 4.5. Detection scripts handle the heavy lifting deterministically; the LLM synthesizes the report and proposes scaffolds for user confirmation.

## Workflow

### Step 1: Verify Python is available

```bash
python3 --version 2>/dev/null || python --version 2>/dev/null
```

If neither, fall back to LLM-based detection (manual marker scan + package.json read) and warn the user.

### Step 2: Run detection scripts in parallel

```bash
python3 ${plugin_root}/scripts/detect-stack.py "$PWD" --json > /tmp/rad-stack.json
python3 ${plugin_root}/scripts/detect-resources.py "$PWD" --check-clis --include-env-names --json > /tmp/rad-resources.json
```

Both complete in well under a second. Read both JSON outputs.

### Step 3: Pre-flight discovery

Determine three things before any writes (same shape as rad-planner M0):

#### 3a — Project directory

Default to `$PWD`. If the user invoked `/init` with an explicit path argument, validate it exists and is writable, then use that. **Never write outside the project directory** — hard rule for all downstream steps.

#### 3b — Agent scope

Determine which coding agents will use this project.

**Detection order:**

1. If `.rad/profile` exists at project root and has `agent_scope` set → use it, skip prompt
2. If `/init` was invoked with `--agents <scope>` → use that
3. Otherwise → ASK:

> "Which coding agents will use this project?
> 1. Claude only (CLAUDE.md canonical)
> 2. Codex only (AGENTS.md canonical)
> 3. Both Claude and Codex (AGENTS.md canonical + CLAUDE.md `@AGENTS.md` shim)
> 4. Not sure yet — defaults to Claude only (this is a Claude plugin); can change later"

Save `agent_scope`. Defaults to `claude_only` if user is unsure — rad-session is a Claude plugin, Claude-native is the right default.

#### 3c — Existing state detection

Mechanical read-only inspection of the project directory. Compute a feature vector:

| Field | Source |
|---|---|
| `has_git` | `.git/` exists with at least 1 commit |
| `has_claude_md` | `CLAUDE.md` exists |
| `claude_init_residue` | `CLAUDE.md` <500 bytes AND no `@AGENTS.md` line AND no `## Compact Instructions` section |
| `has_agents_md` | `AGENTS.md` exists |
| `codex_init_residue` | `AGENTS.md` <500 bytes AND matches Codex `/init` default scaffold pattern |
| `has_vision` | `docs/vision.md` exists with non-trivial content |
| `has_architecture` | `docs/architecture.md` exists with non-trivial content |
| `has_planning_current` | `docs/planning/current.md` exists with non-trivial content |
| `has_status` | `docs/status.md` exists with non-trivial content |
| `has_decisions` | `docs/decisions/` directory exists with at least `README.md` |
| `has_rad_profile` | `.rad/profile` exists |
| `has_v3_strategic_docs` | any of `PRD.md`, `ARCHITECTURE.md`, `ASSUMPTIONS.md`, `DECISIONS.md`, `PLAN.md` exists at project root (legacy detection) |

If `has_v3_strategic_docs == true`, surface to the user:

> "⚠ v3.0-style strategic docs detected at project root (PRD.md / ARCHITECTURE.md / etc.). rad-planner 4.0's canonical structure is at `docs/`. Consider running `/rad-planner:plan --pivot` to migrate, or keep the v3.0 layout for now — rad-session 5.0 reads what's there. The v4.0 doc set is the canonical structure going forward."

Save the full feature vector for use in subsequent steps.

### Step 4: Synthesize a stack summary for the user

Present detection results as a brief, scannable summary:

```
Detected stack:
  Languages:       [from detect-stack]
  Frameworks:      [from detect-stack]
  Package manager: [from detect-stack]
  Deploy targets:  [from detect-stack]
  Infrastructure:  [from detect-stack]

Detected resources:
  MCP servers:     [from detect-resources]
  Stack CLIs:      [from detect-resources, with installed/missing flags]

⚠ CLIs the project assumes but NOT in PATH: [list, if any]

Existing rad-session state (v4.0 canonical):
  Operating manual: {agent_scope-specific state — see Step 6}
  docs/vision.md:           [present | missing]
  docs/architecture.md:     [present | missing]
  docs/planning/current.md: [present | missing]
  docs/status.md:           [present | missing]
  docs/decisions/:          [present (N ADRs) | missing]
  .rad/profile:             [present | missing]

⚠ Legacy v3.0 state (if detected): [PRD.md, etc. — listed; user advised on migration]
```

### Step 5: Recommend rad-* plugins for the detected stack

Match detected stack to currently-shipping rad-* plugins. **Be honest about which actually exist.**

| Detected signal | Recommended plugin | What it adds |
|---|---|---|
| `supabase` (deploy_target or framework) | `rad-supabase` | RLS audit, MCP integration for live ops, migration patterns |
| `coolify` (deploy_target) or Dockerfile + Traefik patterns | `rad-coolify-orchestrator` | Coolify-specific deploy patterns + MCP for live operations |
| `manifest.json` + `wxt.config` or extension-shaped project | `rad-chrome-extension` | MV3 conventions, CWS compliance, manifest validation |
| Any frontend framework + accessibility concerns mentioned | `rad-a11y` | WCAG 2.2 AA review, axe-core integration |
| Coding project of any kind | `rad-code-review` | Diff-aware adversarial code review |
| Project planning needed | `rad-planner` | Plan-first workflow, four entry points, four mechanical validators (4.0) |
| Brainstorming / design needed | `rad-brainstormer` | Pre-planning ideation + design specs |
| Writing / content work | `rad-writer` | Domain-aware writing assistance |
| Multi-platform agentic company work | `rad-agentic-company-builder` | Workspace scaffolding + opt-in business-function agents |

For each recommendation, surface what's installed vs. not. If you can't determine install state, present the recommendation and let the user decide.

### Step 5.5: Plugin / MCP bloat audit

Claude Code's user-scope plugin set carries a real per-turn token cost — every plugin's skill descriptions land in the model's context every turn, and plugins shipping MCP servers add their tool registry on top. For projects that don't use a given plugin's stack, those tokens are pure noise.

This step proposes an `enabledPlugins` map in `.claude/settings.local.json` (gitignored, personal) that disables irrelevant plugins for **this** project specifically. User-scope plugins stay intact in other projects.

#### 5.5.1 Get the installed plugin list

```bash
claude plugin list 2>/dev/null | grep -E '^\s*>\s*[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+' > /tmp/rad-installed-plugins.txt || true
```

If `claude plugin list` is unavailable, ask the user to paste the output.

#### 5.5.2 Run the audit script

```bash
python3 ${plugin_root}/scripts/audit-plugin-bloat.py "$PWD" --json --installed-plugins-stdin < /tmp/rad-installed-plugins.txt > /tmp/rad-plugin-audit.json
```

The script detects ~10 stack signals, applies plugin-relevance rules, filters to only INSTALLED plugins, and outputs per-plugin recommendation (`keep` | `disable`) with reason.

#### 5.5.3 Present the audit to the user

```
Plugin / MCP audit ({total} installed):

Will keep ({N}):
  Core: rad-session, code-simplifier, ...
  Stack-matched: pyright-lsp (python), rad-supabase (supabase), ...

Recommend disable for this project ({N}):
  No matching signal:
    - chrome-devtools-mcp [MCP] — no frontend_web signal
    - rad-coolify-orchestrator [MCP] — no coolify signal
    - ...

Estimated savings: ~{N} tool names cut per turn, plus ~{N} skill descriptions.
```

#### 5.5.4 Get user confirmation

Default behavior: prompt the user.

```
Apply these disables to .claude/settings.local.json? [Y/n/edit]
```

In `--non-interactive` mode, auto-apply.

#### 5.5.5 Write the settings

Read existing `.claude/settings.local.json` if present. **Merge — do not replace**. Preserve `permissions`, any other fields. Add or update the `enabledPlugins` map.

#### 5.5.6 settings.json (committed) vs settings.local.json (gitignored)?

Default: `.claude/settings.local.json`. Ask once if the project is single-author or the user wants the disables shared.

#### 5.5.7 Note for activation

```
⚠ Plugin disables take effect on next session start. The current session continues with the full set already loaded.
```

#### 5.5.8 Re-running the audit

On subsequent invocations, compare current settings against fresh audit recommendations and surface a diff.

### Step 6: Operating manual scaffolding

Determine paths per `agent_scope`:

| Scope | Files written by `/init` |
|---|---|
| `claude_only` | `CLAUDE.md` (canonical) |
| `codex_only` | `AGENTS.md` (canonical) |
| `claude_and_codex` | `AGENTS.md` (canonical) + `CLAUDE.md` (`@AGENTS.md` shim) |

**Critical: `/init` writes Operational sections only.** Per the sectioned-writer rule:

- **Operational sections (`/init` writes):** Commands, Compact Instructions (CLAUDE.md only), Claude-specific behavior (CLAUDE.md only), `@AGENTS.md` import line (CLAUDE.md shim case)
- **Constitution sections (rad-planner `/plan` M6 writes):** Project, Read order, Hard boundaries, Engineering rules, Definition of done, Escalate triggers

If Constitution sections are missing, leave them missing — surface in Step 10 final report: "run `/rad-planner:plan` to populate Constitution sections."

#### 6.1 Detect existing state per file

For each target file (per agent_scope table above):

- **Case A: file doesn't exist.** Scaffold from template (see 6.2).
- **Case B: file exists with `/init` residue** (per Step 3c `claude_init_residue` or `codex_init_residue`). Enrich — insert Operational sections; preserve everything else. Surface "Preserved existing content above."
- **Case C: file exists with substantial content.** Guard rail — three-option prompt:
  > "`{filename}` exists with N lines. Three options:
  > 1. Overwrite — replace existing content with rad-session scaffold (loses user content; backup made)
  > 2. Append Operational sections — preserve all existing content; insert Commands / Compact Instructions / Claude-specific behavior sections in their proper place
  > 3. Skip — leave file untouched"

  Default: append. Show diff before writing.

#### 6.2 Operating manual template (Operational sections only)

```markdown
## Commands

- Install: {from detected stack or placeholder}
- Dev server: {placeholder}
- Unit tests: {from package.json scripts or placeholder}
- Lint: {from package.json scripts or placeholder}
- Typecheck: {from package.json scripts or placeholder}
- Build: {from package.json scripts or placeholder}

{CLAUDE.md only:}

## Claude-specific behavior

- Use `/plan` for ambiguous, multi-file, or architectural work.
- Use subagents for broad codebase investigation, log triage, and post-change review so the main session stays focused.
- If the session drifts after repeated corrections, stop, update `docs/status.md`, and restart with a fresh session.

## Compact Instructions

When using compact:
- preserve the current objective
- preserve non-goals and hard boundaries
- preserve acceptance criteria
- preserve the current list of changed files
- preserve latest validation commands and results
- preserve blockers, open questions, and next step
- drop superseded exploration paths and abandoned ideas
```

For the CLAUDE.md shim case (claude_and_codex), the CLAUDE.md scaffold opens with:

```markdown
@AGENTS.md

## Claude-specific behavior
{...}

## Compact Instructions
{...}
```

(No Operational `## Commands` section in the shim — `AGENTS.md` carries Commands. The shim only adds Claude-specific Operational content.)

#### 6.3 Surface what was preserved

If user-added sections exist in the file (sections not in either rad-planner's owned list or rad-session's owned list), explicitly note in output:

> "Preserved user sections: `## Project gotchas`, `## Team notes`"

This makes preservation visible so the user can verify nothing was missed.

### Step 7: docs/status.md scaffold

If `docs/status.md` doesn't exist:

```bash
mkdir -p docs
```

Create `docs/status.md` with the 8-section template per [`docs/status-md-schema.md`](../../../../docs/status-md-schema.md):

```markdown
# Status

## Current state
- Branch / worktree: (unknown — populated at first /wrapup)
- Current milestone: (unknown — populated from docs/planning/current.md)
- Overall status: No data yet — populated by rad-session /wrapup from evidence

## Last completed

No data yet — populated by rad-session /wrapup from evidence.

## Files changed recently

No data yet — populated by rad-session /wrapup from git evidence.

## Latest validation results

No data yet — populated by rad-session /wrapup from session evidence.

## Decisions made during execution

No data yet — populated by rad-session /wrapup when candidate decisions surface.

## Known issues or blockers

No data yet — populated by rad-session /wrapup.

## Next recommended step

No data yet — populated by rad-session /wrapup from planning/current.md and session context.

## If restarting from scratch

- Read {CLAUDE.md or AGENTS.md per agent_scope}
- Read docs/planning/current.md (if it exists — otherwise run /rad-planner:plan)
- Read docs/architecture.md (if it exists)
- Resume with: (populated at first /wrapup)
```

If `docs/status.md` already exists, leave it alone — user (or prior /wrapup) owns it.

### Step 8: Tool-specific config scaffolding

Per [`docs/cross-plugin-contracts.md`](../../../../docs/cross-plugin-contracts.md), `.claude/settings.json` and `.codex/config.toml` are both rad-session-owned at creation; the human owns subsequent edits. Each is scaffolded only when its respective tool is in scope.

#### 8.1 `.claude/settings.json` (if Claude in scope)

If `agent_scope` includes Claude (`claude_only` or `claude_and_codex`) and `.claude/settings.json` is missing, scaffold with sensible defaults:

```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep", "WebSearch", "WebFetch"],
    "ask": ["Write", "Edit", "Bash"]
  }
}
```

Default to ask-permissions for write operations. User can customize.

If `.claude/settings.json` already exists, leave it alone. (Settings.local.json may have been added by Step 5.5 — that's separate and gitignored.)

Skip 8.1 entirely if `agent_scope == codex_only`.

#### 8.2 `.codex/config.toml` (if Codex in scope)

If `agent_scope` includes Codex (`codex_only` or `claude_and_codex`) and `.codex/config.toml` is missing, scaffold with sensible defaults:

```toml
# Codex project configuration
# rad-session scaffolds this file on /init; rad-planner adds hook entries on /plan M6.
# See https://github.com/openai/codex for full schema.

# Default approvals — adjust per project trust level.
approval_policy = "on-request"   # on-request | unless-allow-listed | never
sandbox_mode    = "workspace-write"  # read-only | workspace-write | danger-full-access

# [shell.env]
# Project-scoped environment variables Codex agents should inherit.

# [hooks]
# rad-planner /plan M6 adds approved hooks here based on the doc_set_draft.
# Manual hook authoring: see docs/cross-plugin-contracts.md and the Codex docs.
```

Match the rad-planner contract: leave the `[hooks]` table commented until rad-planner populates it via `/plan`. The defaults above mirror what most Codex projects start with — agents may write to the workspace but must request approval for destructive shell actions.

If `.codex/config.toml` already exists, leave it alone.

Skip 8.2 entirely if `agent_scope == claude_only`.

### Step 9: .rad/profile

If `.rad/profile` doesn't exist:

```bash
mkdir -p .rad
```

Create with TOML content:

```toml
# rad-planner / rad-session project profile
mode = "mentor"               # mentor (teaching prompts in /wrapup) or dev (quick skip)
agent_scope = "{from Step 3b}"   # claude_only | codex_only | claude_and_codex
multi_branch_status = false   # true when per-branch status is opted in (active hybrid)
```

If `.rad/profile` exists, leave it alone — user owns it.

### Step 10: Final report and next steps

```
Init complete.

Created/updated:
  - {operating manual file(s)}    ({new | enriched | additions made | unchanged})
  - docs/status.md                ({new | unchanged})
  - .claude/settings.json         ({new | unchanged | not applicable for codex_only scope})
  - .claude/settings.local.json   ({plugin disables added: N | unchanged | not applicable for codex_only scope})
  - .codex/config.toml            ({new | unchanged | not applicable for claude_only scope})
  - .rad/profile                  ({new | unchanged})

Strategic doc state (rad-planner output):
  - {one of:}
    - "All v4.0 strategic docs present (vision, architecture, planning/current, status, decisions). Project is fully set up."
    - "Some strategic docs missing: {list}. Recommend /rad-planner:plan --improve to complete."
    - "No strategic docs detected. Recommend /rad-planner:plan --full to create the plan and complete the operating manual's Constitution sections."

Operating manual Constitution sections (rad-planner /plan M6 writes these):
  - {one of:}
    - "Constitution sections present (Project, Read order, Hard boundaries, etc.). /plan has already run."
    - "Constitution sections missing. Run /rad-planner:plan to populate."

Legacy state (if detected):
  - {if has_v3_strategic_docs:} "⚠ v3.0 strategic docs at project root (PRD.md, etc.). rad-session 5.0 reads what's there but the canonical v4.0 structure is at docs/. Consider /rad-planner:plan --pivot to migrate."

Resources registered: {N MCPs, N stack CLIs}
Drift detected:        {N items}
Plugin audit:          {N kept, N disabled — saves ~{N} tool names + ~{N} skills/turn}

Recommended rad-* plugins for your stack (not auto-installed):
  - rad-X — what it adds
  ...

Next:
  - {if no plan:} /rad-planner:plan to create the plan and populate Constitution sections
  - /startup at the start of each session
  - /wrapup at the end of each session
```

### Step 11: Optional follow-ups (only if user asks)

- "How do I install rad-X?" → `claude plugins add ./RAD-Claude-Skills/plugins/rad-X` or via marketplace
- "Run /startup now?" → hand off to `/startup`
- "Why doesn't `/init` write the Constitution sections?" → explain single-writer rule; point at `docs/cross-plugin-contracts.md`

## What this skill does NOT do (recap)

- Does not install plugins (recommends only)
- Does not add MCP servers to .mcp.json (detects existing only)
- Does not generate framework-specific scaffolding
- Does not write strategic docs (rad-planner's job)
- Does not write Constitution sections of the operating manual (rad-planner's job at `/plan` M6)
- Does not write HANDOFF.md (retired in v5.0 — `docs/status.md` replaces it)
- Does not create `.claude/session-log.md` (retired in v5.0 — `docs/planning/archive/` serves the journal role)
- Does not run tests, builds, or side-effect commands beyond detection scripts and `mkdir`
- Does not decide your tech stack — observation only

## Key references

**Canonical spec docs (top-level):**

- [`docs/doc-conventions.md`](../../../../docs/doc-conventions.md) — canonical file structure
- [`docs/cross-plugin-contracts.md`](../../../../docs/cross-plugin-contracts.md) — single-writer rule, sectioned-writer exception for operating manual
- [`docs/status-md-schema.md`](../../../../docs/status-md-schema.md) — status.md schema

**Plugin internals:**

- `scripts/detect-stack.py` — deterministic stack scanner
- `scripts/detect-resources.py` — MCP + CLI scanner with drift detection
- `scripts/audit-plugin-bloat.py` — per-project plugin relevance audit
- `scripts/README.md` — full script documentation

## Mode flags

- `--non-interactive` — Skip user-confirmation gates. Auto-write scaffolds (greenfield) or auto-merge additions (existing). In non-interactive mode, emits trailing JSON.
- `--agents <scope>` — Set agent scope without prompting (`claude_only` | `codex_only` | `claude_and_codex`).
- `--dry-run` — Run detection and show proposed scaffolds, write nothing.

```json
{
  "init_complete": true,
  "agent_scope": "claude_only | codex_only | claude_and_codex",
  "operating_manual_action": {
    "CLAUDE.md": "created | enriched | additions_merged | unchanged | skipped | not_applicable",
    "AGENTS.md": "created | enriched | additions_merged | unchanged | skipped | not_applicable"
  },
  "status_md_action": "created | unchanged",
  "settings_json_action": "created | unchanged | not_applicable",
  "settings_local_action": "created | merged | unchanged",
  "codex_config_action": "created | unchanged | not_applicable",
  "rad_profile_action": "created | unchanged",
  "strategic_docs_present": ["docs/vision.md", "docs/architecture.md"],
  "strategic_docs_missing": ["docs/planning/current.md", "docs/status.md", "docs/decisions/"],
  "constitution_sections_present": true,
  "legacy_v3_docs_detected": false,
  "stack_summary": {},
  "resources_summary": {},
  "recommended_plugins": ["rad-supabase"],
  "drift_items": 0,
  "plugins_disabled": [],
  "plugin_audit_summary": {"total": 0, "keep": 0, "disable": 0}
}
```
