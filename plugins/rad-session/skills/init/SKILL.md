---
name: init
description: >
  One-time per project. Bootstraps rad-session machinery: detects the tech stack
  deterministically (via scripts/detect-stack.py), discovers MCP servers and CLIs
  (via scripts/detect-resources.py with PATH verification), scaffolds or merges
  CLAUDE.md with a baseline + ## Resources section, and recommends which rad-*
  plugins are worth installing for the detected stack. Trigger when the user says
  "/init", "init project", "set up rad-session here", "bootstrap session", "new
  project setup", "configure for this project", "set up CLAUDE.md".
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Project Init — One-Time Bootstrap

Set up a project for rad-session: detect what's there, scaffold the baseline files, register the resources Claude will need every session.

**This skill runs ONCE per project.** Re-running is safe (it merges rather than overwrites), but the value is at the start. Per-session orientation is `/startup`. Per-session capture is `/wrapup`.

## Honest framing

This skill does NOT:
- Install rad-* plugins for you (it recommends; you decide)
- Add MCP servers (it detects what's already configured)
- Generate framework-specific code
- Decide your tech stack (it observes what's already there)

This skill DOES:
- Run two Python scripts that deterministically scan the project
- Generate or merge a CLAUDE.md baseline (you confirm before writing)
- Surface gaps: "you have a Supabase project but the supabase CLI isn't in PATH"
- Suggest which rad-* plugins fit the detected stack

## Cross-model note

Works identically across Opus 4.7, Sonnet 4.6, and Haiku 4.5. The two detection scripts handle the heavy lifting deterministically; the LLM only synthesizes the report and proposes the CLAUDE.md scaffold for user confirmation.

## Workflow

### Step 1: Verify Python is available

```bash
python3 --version 2>/dev/null || python --version 2>/dev/null
```

If neither is available, fall back to LLM-based detection (manual marker scan + package.json read) and warn the user that without Python they're getting a less reliable bootstrap.

### Step 2: Run detection scripts in parallel

```bash
python3 ${plugin_root}/scripts/detect-stack.py "$PWD" --json > /tmp/rad-stack.json
python3 ${plugin_root}/scripts/detect-resources.py "$PWD" --check-clis --include-env-names --json > /tmp/rad-resources.json
```

Both should complete in well under a second. Read both JSON outputs.

### Step 3: Check for existing rad-session and rad-planner state

```
- CLAUDE.md present?
- HANDOFF.md present?
- .claude/session-log.md present?
- .claude/settings.json present?
- CLAUDE-FRAGMENT.md present?            (handoff from rad-planner /plan — consumed and deleted by this step)
- Strategic docs at project root?        (PRD.md, ARCHITECTURE.md, ASSUMPTIONS.md, DECISIONS.md, PLAN.md)
```

Two scenarios for CLAUDE.md:

**A. Greenfield (no existing rad-session files)** → scaffold from scratch.
**B. Existing project (CLAUDE.md exists)** → merge mode. Don't overwrite; offer additions.

The FRAGMENT and strategic-doc state determines the `@-import` block that gets inserted into the CLAUDE.md scaffold (Step 6).

### Step 4: Synthesize a stack summary for the user

Present the detection results as a brief, scannable summary:

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

⚠ CLIs the project assumes but NOT in PATH: [list, if any — install these]

Existing rad-session state:
  CLAUDE.md:       [present (N lines) | missing]
  HANDOFF.md:      [present | missing]
  session-log:     [present (N entries) | missing]
```

### Step 5: Recommend rad-* plugins for the detected stack

Match detected stack to currently-shipping rad-* plugins. **Be honest about which actually exist** — earlier-version recommendations referenced now-archived plugins (rad-react, rad-zod, rad-typescript, rad-nextjs, rad-fastify, rad-astro, rad-stripe-fastify-webhooks). Don't recommend those.

The currently-shipping plugins worth recommending by stack signal:

| Detected signal | Recommended plugin | What it adds |
|---|---|---|
| `supabase` (deploy_target or framework) | `rad-supabase` | RLS audit, MCP integration for live ops, migration patterns |
| `coolify` (deploy_target) or Dockerfile + Traefik patterns | `rad-coolify-orchestrator` | Coolify-specific deploy patterns + MCP for live operations |
| `manifest.json` + `wxt.config` or extension-shaped project | `rad-chrome-extension` | MV3 conventions, CWS compliance, manifest validation |
| Any frontend framework + accessibility concerns mentioned | `rad-a11y` | WCAG 2.2 AA review, axe-core integration |
| Coding project of any kind | `rad-code-review` | Diff-aware adversarial code review |
| Project planning needed | `rad-planner` | Dependency-aware implementation plans with DAG validation |
| Brainstorming / design needed | `rad-brainstormer` | Pre-planning ideation + design specs |
| Writing / content work | `rad-writer` | Domain-aware writing assistance |
| Multi-platform agentic company work | `rad-agentic-company-builder` | Workspace scaffolding + opt-in business-function agents |

**For each recommendation, surface what's installed vs. not.** Use Bash to check `~/.claude/plugins/` (or wherever Claude Code's plugin install path lives — varies by environment). If you can't determine install state, just present the recommendation and let the user decide.

### Step 5.5: Plugin / MCP bloat audit (3.6)

Claude Code's user-scope plugin set carries a real per-turn token cost — every plugin's skill descriptions land in the model's context every turn, and plugins shipping MCP servers add their tool registry on top. For projects that don't use a given plugin's stack, those tokens are pure noise.

This step proposes a `enabledPlugins` map in `.claude/settings.local.json` (gitignored, personal) that disables irrelevant plugins for **this** project specifically. User-scope plugins stay intact in other projects.

#### 5.5.1 Get the installed plugin list

```bash
claude plugin list 2>/dev/null | grep -E '^\s*>\s*[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+' > /tmp/rad-installed-plugins.txt || true
```

If `claude plugin list` is unavailable or returns nothing parseable, ask the user to paste the output. The script accepts loose text — it greps `name@marketplace` patterns.

#### 5.5.2 Run the audit script

```bash
python3 ${plugin_root}/scripts/audit-plugin-bloat.py "$PWD" --json --installed-plugins-stdin < /tmp/rad-installed-plugins.txt > /tmp/rad-plugin-audit.json
```

The script:
- Detects 10 stack signals (supabase, stripe, coolify, chrome_extension, frontend_web, python, anthropic_sdk, 1password_secrets, claude_plugin_repo, content_site)
- Applies a built-in catalog of plugin-relevance rules
- Filters to only INSTALLED plugins (passed via stdin)
- Outputs per-plugin recommendation (`keep` | `disable`) with reason

#### 5.5.3 Present the audit to the user

Group recommendations by recommendation + category:

```
Plugin / MCP audit ({total} installed):

Will keep ({N}):
  Core: rad-session, claude-md-management, code-simplifier, ...
  Stack-matched: pyright-lsp (python), rad-supabase (supabase), ...

Recommend disable for this project ({N}):
  No matching signal:
    - chrome-devtools-mcp [MCP] — no frontend_web signal
    - rad-coolify-orchestrator [MCP] — no coolify signal
    - rad-supabase — no supabase signal
    - ...
  Productivity (re-enable per project where you actively use it):
    - rad-gws-core, rad-para-second-brain, rad-agentic-company-builder

Estimated savings: ~{N} tool names cut from registry per turn,
plus ~{N} skill descriptions from skill listing.
```

Compute the estimate by counting plugins shipping MCPs (×~10-20 tools each) plus the skill-only disables (×~5-10 skill descriptions each). Order of magnitude only — the goal is to give the user a sense of scale, not a precise number.

#### 5.5.4 Get user confirmation

Default behavior: prompt the user.

```
Apply these disables to .claude/settings.local.json? [Y/n/edit]
```

- **Y** — write the `enabledPlugins` map merging with any existing settings.
- **n** — skip; record the proposed disables in the final report so the user can apply manually later.
- **edit** — let the user override individual disables (e.g., "keep rad-1password even though no op:// signal — I use it broadly").

In `--non-interactive` mode, auto-apply the disables and record them in the trailing JSON output (`plugins_disabled: ["...", ...]`).

#### 5.5.5 Write the settings

Read existing `.claude/settings.local.json` if present. **Merge — do not replace** the existing content; preserve `permissions`, any other fields. Add or update the `enabledPlugins` map:

```json
{
  "...existing fields...": "...",
  "enabledPlugins": {
    "chrome-devtools-mcp@claude-plugins-official": false,
    "stripe@claude-plugins-official": false,
    "...": false
  }
}
```

If the user already had an `enabledPlugins` map, merge: existing `true` values stay (user explicit overrides), audit's `false` values are added/updated.

#### 5.5.6 Write to settings.json (committed) instead?

Ask once if the project is single-author or the user wants the disables shared with collaborators:

```
Write to .claude/settings.local.json (gitignored, personal) or
        .claude/settings.json (committed, team-shared)?
```

Default: `.claude/settings.local.json`. Most projects benefit from per-user override; the disables encode personal preference, not team policy.

#### 5.5.7 Note for activation

Plugin enable/disable changes do NOT take effect mid-session. Tell the user:

```
⚠ Plugin disables take effect on next session start. The current session continues with the full set already loaded.
```

#### 5.5.8 Re-running the audit

`/init` is safe to re-run. On subsequent invocations, this step compares current settings against fresh audit recommendations and surfaces a diff:

```
Audit refresh:
  - Newly recommend disable: X (signal lost or new plugin installed)
  - Newly recommend keep: Y (signal added since last audit)
  - Already disabled and still recommended: Z (no change)
```

The user can apply the deltas, ignore them, or re-edit settings manually.

---

### Step 6: Propose CLAUDE.md scaffold (or additions)

#### Step 6.0: Compute the Strategic Docs `@-import` block (4.0)

Before generating the scaffold or proposing additions, determine what `@-import` block (if any) lands inside CLAUDE.md. Three cases, evaluated in order:

**Case 1 — `CLAUDE-FRAGMENT.md` exists at project root.** This is the canonical handoff from `/rad-planner:plan`:

1. Read its content. It should contain an `@-import` block listing `@PRD.md`, `@ARCHITECTURE.md`, etc.
2. Extract the `@-import` lines (ignore comments and the header).
3. Wrap them in a `## Strategic Docs` section to be inserted in CLAUDE.md (Step 6 branches use this block).
4. **Delete `CLAUDE-FRAGMENT.md`** after a successful CLAUDE.md write in Step 6. Absence at next `/init` is fine — Cases 2 and 3 below cover regeneration.

**Case 2 — No FRAGMENT, but ≥1 strategic doc exists at project root.** Auto-generate the import block from detected filenames:

```bash
# Glob the project root for the 5 strategic docs
for f in PRD.md ARCHITECTURE.md ASSUMPTIONS.md DECISIONS.md PLAN.md; do
  [ -f "$f" ] && echo "@$f"
done
```

Wrap the resulting lines in a `## Strategic Docs` section. This handles projects where the user ran `/plan` and merged the FRAGMENT manually (deleting the FRAGMENT), or projects on a different machine where the FRAGMENT never landed in this clone.

**Case 3 — No FRAGMENT and no strategic docs.** Scaffold with placeholder pointers so the user knows the slots exist and how to fill them:

```markdown
## Strategic Docs (pending — run /rad-planner:plan to create)

<!-- @PRD.md           — what we're building and why -->
<!-- @ARCHITECTURE.md  — how it fits together -->
<!-- @ASSUMPTIONS.md   — non-obvious truths about the project's reality -->
<!-- @DECISIONS.md     — architecture decisions, sequence-numbered, append-only -->
<!-- @PLAN.md          — milestones, steps, checkpoints -->
```

(HTML comments so the imports don't resolve until the user uncomments them or runs `/rad-planner:plan` to generate the actual files. Avoids broken-import warnings during `/startup` Phase 1.1.)

In all three cases, this block becomes the `{strategic_docs_block}` substitution used in Step 6.A and Step 6.B below.

#### Step 6.A: Greenfield case — generate a starter CLAUDE.md

```markdown
# {project-name}

## Project Type
{coding-project | non-coding-project}

## Tech Stack
- Languages: {languages}
- Frameworks: {frameworks}
- Package manager: {package_manager}
- Deploy: {deploy_targets}

## Build Commands
{from package.json scripts}

{strategic_docs_block}

## Resources
- {each detected MCP server}: ...
- {each detected stack CLI}: ...

## Conventions
[user adds — placeholder for project-specific rules]
```

Show the proposed content. Ask: "Write this as your initial CLAUDE.md?" Wait for confirmation.

#### Step 6.B: Existing CLAUDE.md case — propose ADDITIONS only

- If `## Resources` section is missing → propose adding it with detected items.
- If `## Resources` exists → reconcile against detected. Show drift report (documented-but-missing, detected-but-undocumented). Offer to add the latter via `/add-resource` style edits.
- **If `## Strategic Docs` section is missing AND Case 1 or Case 2 from Step 6.0 applies** → propose inserting `{strategic_docs_block}` near the top of CLAUDE.md, after the project header / tech stack / build commands but before the Resources section. If CLAUDE.md already contains any of the `@PRD.md` / `@ARCHITECTURE.md` / etc. lines, treat as "already merged" — skip the insertion silently and (Case 1 only) still delete CLAUDE-FRAGMENT.md.
- Do NOT touch the rest of the file.

Show the diff. Get confirmation before writing.

#### Step 6.C: After a successful CLAUDE.md write

If Case 1 applied (FRAGMENT was consumed):

```bash
rm CLAUDE-FRAGMENT.md
```

Note the deletion in the Step 8 final report (`CLAUDE-FRAGMENT.md: consumed and removed`).

If the user declined the CLAUDE.md write in Step 6.A/6.B, **do not delete the FRAGMENT** — leave it on disk so a later re-run of `/init` can pick it up.

### Step 7: Set up `.claude/` baseline (if missing)

If `.claude/` doesn't exist:

```bash
mkdir -p .claude
```

If `.claude/session-log.md` is missing, create it with a header line so the file format is established:

```
# Session Log
Newest first. Each entry: `## YYYY-MM-DD — short title`.
```

Do NOT generate `.claude/settings.json` automatically — that's a separate decision (some users want team-shared settings, some don't). Mention it as an optional next step.

### Step 7.5: Ensure session files are tracked by git

The cross-machine sync in `/wrapup` Phase 6 and `/startup` Phase 0 depends on `HANDOFF.md` and `.claude/session-log.md` being committed. If `.claude/` is gitignored at the project root or a parent, the session log gets stranded on whatever machine wrote it.

Skip this step silently if the project is not a git repo.

Otherwise:

1. Read `.gitignore` at the project root (if it exists). Look for any rule that would match `.claude/` or `.claude/session-log.md` (e.g., `.claude/`, `.claude/*`, `**/.claude/`, `.claude`).

2. If a matching rule exists and there is no exception (`!.claude/session-log.md`), propose appending to `.gitignore`:

   ```
   # rad-session: keep session continuity files tracked across machines
   !.claude/session-log.md
   ```

   Show the diff. Wait for confirmation before writing. If the user declines, note in the final report: `⚠ .claude/session-log.md is gitignored — cross-machine sync will not transfer the log file.`

3. Also check that `HANDOFF.md` is not gitignored (rare, but check). If it is, propose `!HANDOFF.md`.

4. If `.gitignore` doesn't exist, do nothing — session files at their current paths are tracked by default.

In `--non-interactive` mode, auto-append the exceptions when needed and record the change in the trailing JSON output (`gitignore_action: "exception_added" | "unchanged"`).

### Step 8: Final report and next steps

```
Init complete.

Created/updated:
  - CLAUDE.md   ({new | additions made | already complete})
  - .claude/session-log.md  ({new | already present})
  - .claude/settings.local.json  ({plugin disables added: N | unchanged})

Strategic docs (rad-planner output):
  - {emit one line per case}
    - Case 1 (FRAGMENT merged): "CLAUDE-FRAGMENT.md: consumed and removed; @-imports merged into CLAUDE.md"
    - Case 2 (auto-generated):  "Strategic docs detected ({N} of 5): @-imports auto-generated into CLAUDE.md"
    - Case 3 (placeholders):    "No strategic docs yet — placeholder @-import comments inserted. Run /rad-planner:plan when ready."

Resources registered: {N MCPs, N stack CLIs}
Drift detected:        {N items — see /add-resource if you want to add them}
Plugin audit:          {N kept, N disabled — saves ~{N} tool names + ~{N} skills/turn}

Recommended rad-* plugins for your stack (not auto-installed):
  - rad-X — what it adds
  - rad-Y — what it adds
  ...

Next:
  - /startup at the start of each session (start fresh — plugin disables take effect on restart)
  - /wrapup at the end of each session
  - /add-resource any time to register new tools
  {Case 3 only:} - /rad-planner:plan to generate the strategic docs (PRD / ARCH / ASSUMPTIONS / DECISIONS / PLAN)
```

### Step 9: Optional follow-ups (only if user asks)

- "How do I install rad-X?" → `claude plugins add ./RAD-Claude-Skills/plugins/rad-X` or via marketplace
- "Generate `.claude/settings.json` for the team?" → propose minimal permissions allow/deny + enabled MCPs
- "Run /startup now?" → hand off to /startup

## What this skill does NOT do (recap)

- Does not install plugins (recommends only)
- Does not add MCP servers to .mcp.json (detects existing only — adding is `/configure-mcp` in rad-agentic-company-builder)
- Does not generate framework-specific scaffolding (that's the framework's own CLI: `npx create-next-app`, `cargo init`, etc.)
- Does not run tests, builds, or any side-effect commands beyond the two read-only Python scripts and `mkdir .claude/`
- Does not decide your tech stack — observation only

## Key references

- `scripts/detect-stack.py` — the deterministic stack scanner
- `scripts/detect-resources.py` — the MCP + CLI scanner with drift detection
- `scripts/audit-plugin-bloat.py` — per-project plugin relevance audit (3.6)
- `scripts/README.md` — full script documentation

## Mode flags

- `--non-interactive` — Skip user-confirmation gates. Auto-write the CLAUDE.md scaffold (greenfield) or auto-merge the additions (existing). Useful for autonomous setup runs. In non-interactive mode, the skill emits a trailing JSON block summarizing what was created/modified.

```json
{
  "init_complete": true,
  "claude_md_action": "created | additions_merged | unchanged",
  "session_log_action": "created | unchanged",
  "settings_local_action": "created | merged | unchanged",
  "fragment_action": "consumed | absent_auto_generated | absent_placeholder | absent_unchanged",
  "strategic_docs_detected": ["PRD.md", "ARCHITECTURE.md"],
  "stack_summary": {...},
  "resources_summary": {...},
  "recommended_plugins": ["rad-supabase", "rad-coolify-orchestrator", ...],
  "drift_items": N,
  "plugins_disabled": ["chrome-devtools-mcp@claude-plugins-official", "..."],
  "plugin_audit_summary": {"total": N, "keep": N, "disable": N}
}
```

- `--dry-run` — Run detection and show the proposed CLAUDE.md scaffold but write nothing. Same JSON output structure with `claude_md_action: "would_create"` / `"would_merge"`.
