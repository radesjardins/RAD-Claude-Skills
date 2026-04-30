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

**JSON output structure** — see the script's docstring for the full schema. Used by `/init` and optionally by `/startup` Phase 2.5.

**Exit codes:** `0` always (this is a measurement, not pass/fail), `2` script error.

## detect-resources.py

Scans for MCP servers and stack CLIs. Compares detected against documented (in CLAUDE.md `## Resources`) and reports drift.

```bash
python3 scripts/detect-resources.py <project-root>
python3 scripts/detect-resources.py <project-root> --json
python3 scripts/detect-resources.py <project-root> --check-clis           # verify CLIs in PATH
python3 scripts/detect-resources.py <project-root> --include-env-names    # also list .env.example var names
```

**Detects:**
- MCP servers from `.mcp.json` and `.claude/settings.json` (`enabledMcpjsonServers`)
- Stack CLIs inferred from marker files (supabase/config.toml → supabase, fly.toml → flyctl, etc. — same table as `/startup` Phase 2.5.2)
- CLI presence in PATH (with `--check-clis`) — useful at `/init` time to flag CLIs the project assumes but aren't installed
- Documented resources from CLAUDE.md `## Resources` section
- `.env.example` variable names (with `--include-env-names`) — names only, never values

**Drift detection:**
- `documented_but_missing` — listed in CLAUDE.md but not detected (config moved, tool uninstalled?)
- `detected_but_undocumented` — detected but not in CLAUDE.md (signals user may want to `/add-resource`)

**Exit codes:** `0` always, `2` script error.

## audit-plugin-bloat.py (3.6)

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
| `/init` | `detect-stack.py --json` + `detect-resources.py --check-clis --json` + `audit-plugin-bloat.py --json --installed-plugins-stdin` | Once on project bootstrap. Drives the CLAUDE.md scaffold, rad-* plugin recommendations, and per-project `enabledPlugins` disables in `.claude/settings.local.json`. Safe to re-run for refresh. |
| `/startup` | `detect-resources.py --json --cache` | Every session, Phase 2.5. Cache-keyed by input mtimes (3.5). |

## What these scripts deliberately do NOT do

- **Do not exec stack binaries** by default. File-presence inference only. `--check-clis` does run `which` (or Windows `where`) to verify PATH availability — that's the only exception, and it's opt-in.
- **Do not read `.env`** (only `.env.example`, and only variable names).
- **Do not modify any files.**
- **Do not call out to the network.** No registry lookups, no version checks. (For framework version verification, that's the LLM's job with WebSearch / Context7.)
- **Do not prescribe** which rad-* plugins to install. They surface what's there; `/init` decides what to recommend based on the data.
