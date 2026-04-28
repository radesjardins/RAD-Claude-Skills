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

### Step 3: Check for existing rad-session state

```
- CLAUDE.md present?
- HANDOFF.md present?
- .claude/session-log.md present?
- .claude/settings.json present?
```

Two scenarios:

**A. Greenfield (no existing rad-session files)** → scaffold from scratch.
**B. Existing project (CLAUDE.md exists)** → merge mode. Don't overwrite; offer additions.

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

### Step 6: Propose CLAUDE.md scaffold (or additions)

**A. Greenfield case** — generate a starter CLAUDE.md:

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

## Resources
- {each detected MCP server}: ...
- {each detected stack CLI}: ...

## Conventions
[user adds — placeholder for project-specific rules]
```

Show the proposed content. Ask: "Write this as your initial CLAUDE.md?" Wait for confirmation.

**B. Existing CLAUDE.md case** — propose ADDITIONS only:

- If `## Resources` section is missing → propose adding it with detected items.
- If `## Resources` exists → reconcile against detected. Show drift report (documented-but-missing, detected-but-undocumented). Offer to add the latter via `/add-resource` style edits.
- Do NOT touch the rest of the file.

Show the diff. Get confirmation before writing.

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

Resources registered: {N MCPs, N stack CLIs}
Drift detected:        {N items — see /add-resource if you want to add them}

Recommended rad-* plugins for your stack (not auto-installed):
  - rad-X — what it adds
  - rad-Y — what it adds
  ...

Next:
  - /startup at the start of each session
  - /wrapup at the end of each session
  - /add-resource any time to register new tools
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
- `scripts/README.md` — full script documentation

## Mode flags

- `--non-interactive` — Skip user-confirmation gates. Auto-write the CLAUDE.md scaffold (greenfield) or auto-merge the additions (existing). Useful for autonomous setup runs. In non-interactive mode, the skill emits a trailing JSON block summarizing what was created/modified.

```json
{
  "init_complete": true,
  "claude_md_action": "created | additions_merged | unchanged",
  "session_log_action": "created | unchanged",
  "stack_summary": {...},
  "resources_summary": {...},
  "recommended_plugins": ["rad-supabase", "rad-coolify-orchestrator", ...],
  "drift_items": N
}
```

- `--dry-run` — Run detection and show the proposed CLAUDE.md scaffold but write nothing. Same JSON output structure with `claude_md_action: "would_create"` / `"would_merge"`.
