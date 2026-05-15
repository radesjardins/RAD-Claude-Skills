# rad-session scripts

Deterministic detection layer for the rad-session skills. Replaces "ask the LLM to eyeball package.json" with structured Python scans. Saves tokens and gives reproducible results.

All scripts are pure Python 3.8+ stdlib. No `pip install` required.

## detect-stack.py

Scans a project directory and identifies its tech stack from lockfiles, config files, package.json dependencies, and source-file extensions.

```bash
python3 scripts/detect-stack.py <project-root>            # default: cwd
python3 scripts/detect-stack.py <project-root> --json
python3 scripts/detect-stack.py <project-root> --plain    # text only, no decorations
```

**Detects:**
- Languages (typescript, python, go, rust, ruby, etc. — via marker files + file-extension scan)
- Frameworks (next, react, vue, svelte, fastify, prisma, drizzle, zod, vitest, playwright, etc.)
- Package manager (pnpm, npm, yarn, bun, poetry, pipenv, cargo, go) via lockfile + `packageManager` field
- Top scripts from package.json (prioritized: dev, build, test, typecheck, lint)
- Deploy targets (vercel, netlify, fly, cloudflare, supabase, coolify, etc.)
- Infrastructure (docker, github-actions, terraform, etc.)
- Toolchain (mise, asdf, nix, devbox)
- Whether it's a coding project at all

**JSON output structure** — see the script's docstring for the full schema. Used by `/startup` (Phase 0.5 bootstrap path on first run, and read by the steady-state briefing for the project-type line).

**Exit codes:** `0` always (this is a measurement, not pass/fail), `2` script error.

## detect-resources.py

Scans for MCP servers and stack CLIs. Compares detected against documented (in the operating manual or `docs/architecture.md`) and reports drift.

```bash
python3 scripts/detect-resources.py <project-root>
python3 scripts/detect-resources.py <project-root> --json
python3 scripts/detect-resources.py <project-root> --check-clis           # verify CLIs in PATH
python3 scripts/detect-resources.py <project-root> --include-env-names    # also list .env.example var names
```

**Detects:**
- MCP servers from `.mcp.json` and `.claude/settings.json` (`enabledMcpjsonServers`)
- Stack CLIs inferred from marker files (supabase/config.toml → supabase, fly.toml → flyctl, etc. — same table referenced in `/startup`)
- CLI presence in PATH (with `--check-clis`) — useful during `/startup`'s bootstrap path to flag CLIs the project assumes but aren't installed
- Documented resources from the operating manual (if a `## Resources` section is present) — backward-compatible with v4.0 layouts
- `.env.example` variable names (with `--include-env-names`) — names only, never values

**Drift detection:**
- `documented_but_missing` — listed in the operating manual but not detected (config moved, tool uninstalled?)
- `detected_but_undocumented` — detected but not in the manual (signals user may want to `/add-resource`)

**Exit codes:** `0` always, `2` script error.

## migrate-to-v5.py (5.0)

One-shot migration helper for projects upgrading from rad-session 3.x / 4.x to the v5.0 canonical doc structure. Read the script's module docstring for the full contract.

```bash
python3 scripts/migrate-to-v5.py <project-root>                    # interactive
python3 scripts/migrate-to-v5.py <project-root> --dry-run          # show plan, write nothing
python3 scripts/migrate-to-v5.py <project-root> --non-interactive  # apply safe transforms only
python3 scripts/migrate-to-v5.py <project-root> --json             # trailing JSON summary; implies --non-interactive
```

**Transforms applied:**

| Detected | Action |
|---|---|
| `HANDOFF.md` at project root | Archived to `.rad-archive/<UTC-timestamp>/HANDOFF.md.orig`. Prompts whether to seed `docs/status.md` from the archived content's "Where we left off" / "What NOT to do" / "Next" sections. |
| `.claude/session-log.md` | Archived to `.rad-archive/<UTC-timestamp>/.claude-session-log.md.orig`. Historical entries are preserved but not migrated into `planning/archive/` (per-session entries don't map 1:1 to milestones). |
| `PRD.md` / `ARCHITECTURE.md` / `ASSUMPTIONS.md` / `DECISIONS.md` / `PLAN.md` at project root (v4.0 8-doc layout) | Moved to `docs/` per the v5.0 canonical structure: `PRD.md` → `docs/vision.md`, `ARCHITECTURE.md` → `docs/architecture.md`, `PLAN.md` → `docs/planning/current.md`, `DECISIONS.md` → split into `docs/decisions/NNNN-*.md` ADRs (sequence-numbered from the DECISIONS.md entries). `ASSUMPTIONS.md` is archived (its content is folded into vision.md non-goals + architecture.md invariants as the user chooses). |
| `CLAUDE-FRAGMENT.md` (v4.0 transient) | Archived. Its role is replaced by `/rad-planner:plan` M6 writing directly to the operating manual's Constitution sections. |
| Operating manual without sectioned-writer markers | Parsed to detect sections rad-session owns; preserved as-is unless the user opts to add the v5.0 Operational scaffolds (`## Commands`, `## Compact Instructions`, `## Claude-specific behavior`). |

**Safety:**
- Archive-before-edit: every transformed original is copied to `.rad-archive/<UTC-timestamp>/` before any in-place change.
- `manifest.json` in the archive records what was archived, where it came from, and what was applied.
- `.rad-archive/` is added to `.gitignore` by default (override with `--no-gitignore`).
- Dry-run mode (`--dry-run`) shows the full plan without writing.
- Re-running on an already-migrated project is a no-op (exits clean with "nothing to migrate").

**Ambiguous transformations** require explicit confirmation in interactive mode and are skipped (with a note in the manifest) in `--non-interactive`. Cases:
- Both `PRD.md` at root AND `docs/vision.md` already present (would overwrite — user picks).
- `DECISIONS.md` contains free-form prose rather than sequence-numbered entries (script can't safely split).

**Rollback:** manual. The archive directory contains every original with the suffix `.orig` (path separators flattened to `-`). Restore by copying back from the archive timestamp directory, then deleting the new v5 files.

**Exit codes:** `0` migration applied (or dry-run completed), `1` nothing to migrate / all declined, `2` script error.

> **Status (v5.0 release):** `migrate-to-v5.py` is the planned migration tool. The v4.0 `migrate-to-v4.py` remains in the repo at `scripts/migrate-to-v4.py` for projects still on the 2.x/3.x layout that want to land on v4.0 before stepping up to v5.0. Projects can also go straight from 3.x to v5.0 by running both migrators in sequence, or directly via `migrate-to-v5.py` once it ships.

## audit-plugin-bloat.py

Recommends which Claude Code plugins to disable per-project for token efficiency. Plugins shipping MCP servers add their tool registry to every turn's context; plugins shipping skills add their skill descriptions to the listing. For projects that don't use a given plugin's stack, those tokens are pure noise.

```bash
python3 scripts/audit-plugin-bloat.py <project-root>
python3 scripts/audit-plugin-bloat.py <project-root> --json
python3 scripts/audit-plugin-bloat.py <project-root> --json --installed-plugins-stdin < <plugin-list>
```

**How it works:**
- Detects 10 stack signals (supabase, stripe, coolify, chrome_extension, frontend_web, python, anthropic_sdk, 1password_secrets, claude_plugin_repo, content_site)
- Applies a built-in catalog of plugin-relevance rules (in `PLUGIN_RULES` at top of script — edit there to add/adjust)
- Categories: `core` (always keep), `stack-conditional` (keep iff signals match), `productivity` (default disable), `meta-authoring` (keep only in plugin-authoring repos)
- With `--installed-plugins-stdin`: reads `name@marketplace` IDs from stdin (tolerant of `claude plugin list` raw output) and filters audit to only installed plugins

**Output (JSON):** `stack_signals` map, `audit` list (per-plugin recommendation + reason + ships_mcp flag), `summary` counts. See script docstring for the full schema.

**The script is OPINIONATED.** It encodes "this plugin is worth its token cost only when these signals are present." Edit `PLUGIN_RULES` in the script to override or extend.

**Exit codes:** `0` always, `2` script error.

## When the skills run these

| Skill | Script | When |
|---|---|---|
| `/startup` (Phase 0.5 bootstrap) | `detect-stack.py --json` + `detect-resources.py --check-clis --json` + `audit-plugin-bloat.py --json --installed-plugins-stdin` | First run for a project. Drives operating manual `## Commands` scaffold, rad-* plugin recommendations, and per-project `enabledPlugins` disables in `.claude/settings.local.json`. Skipped silently on subsequent runs. Re-runnable via `/startup --bootstrap`. |
| `/startup` | `detect-resources.py --json --cache` | Optional. Phase 2.5 (drift surfacing only). Cache-keyed by input mtimes. Skipped silently if no drift. |
| (user-invoked) | `migrate-to-v5.py` | One-shot during upgrade from 3.x/4.x. Not called from any skill — the user runs it manually. |
| (user-invoked) | `migrate-to-v4.py` | Legacy. One-shot during upgrade from 2.x/3.x to v4.0. Kept in-repo for projects that want a staged migration. |

## What these scripts deliberately do NOT do

- **Do not exec stack binaries** by default. File-presence inference only. `--check-clis` does run `which` (or Windows `where`) to verify PATH availability — that's the only exception, and it's opt-in.
- **Do not read `.env`** (only `.env.example`, and only variable names).
- **Do not modify any files.** (Migration scripts are the exception — they're explicitly destructive but always archive first.)
- **Do not call out to the network.** No registry lookups, no version checks. (For framework version verification, that's the LLM's job with WebSearch / Context7.)
- **Do not prescribe** which rad-* plugins to install. They surface what's there; `/startup`'s bootstrap path decides what to recommend based on the data.
