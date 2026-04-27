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

## When the skills run these

| Skill | Script | When |
|---|---|---|
| `/init` | `detect-stack.py --json` + `detect-resources.py --check-clis --json` | Once, on project bootstrap. Drives the CLAUDE.md scaffold and rad-* plugin recommendations. |
| `/startup` | `detect-resources.py --json` (optionally `detect-stack.py`) | Every session, Phase 2.5. Replaces LLM-based marker-file scanning. |

## What these scripts deliberately do NOT do

- **Do not exec stack binaries** by default. File-presence inference only. `--check-clis` does run `which` (or Windows `where`) to verify PATH availability — that's the only exception, and it's opt-in.
- **Do not read `.env`** (only `.env.example`, and only variable names).
- **Do not modify any files.**
- **Do not call out to the network.** No registry lookups, no version checks. (For framework version verification, that's the LLM's job with WebSearch / Context7.)
- **Do not prescribe** which rad-* plugins to install. They surface what's there; `/init` decides what to recommend based on the data.
