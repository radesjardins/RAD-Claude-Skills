# rad-code-review — Catch what AI wrote wrong before it ships.

> **v4.0 — Naming pass.** The `UCR-` heritage prefix on config / finding IDs / state dirs renamed to `RADCR-` for naming consistency. **Existing users:** rename `.ucrconfig.yml` → `.radcrconfig.yml` and `.ucr/` → `.radcr/` before running this version (no content changes). See the Naming section below.
>
> **v3.0 — Optimized for Claude Opus 4.7.** Opus 4.7 is now the default primary-review model. Parallel tool calls across discovery/stack-detection/automated-checks. JSON-first subagent output (robust across models). Compaction-safe checkpointing with `--resume <run-id>`. `--non-interactive` mode for agents and CI. Externalized subagent prompt templates. `.radcrconfig.yml` accepted-risk expiry is now enforced. Sonnet 4.6 is a first-class fallback; Haiku 4.5 works for narrow blame-aware diffs.

When you build with Claude, you move fast. Fast enough that subtle bugs, fake error handling, and hardcoded accessibility states slip through — and they look fine at a glance. rad-code-review is the adversarial reviewer that knows exactly which mistakes AI code generators make. It only flags what *you* changed, not the whole codebase. And it understands your framework well enough to catch the security holes that generic linters miss.

## What You Can Do With This

- Review your current diff for bugs and security issues before committing — only the code you wrote gets flagged
- Check a new API endpoint for IDOR vulnerabilities across 6 supported frameworks (Next.js, Express, Fastify, Django, Rails, Go)
- Run a pre-ship audit across the full repo with a clear ship/no-ship verdict
- Detect AI-generated code anti-patterns: hallucinated imports, fake error handling, placeholder stubs, silent failures

## How It Works

rad-code-review runs three review roles in sequence — bug finder, architecture reviewer, release gate — then produces severity-ranked findings with optional fix application.

| Skill | Purpose |
|-------|---------|
| `rad-code-review` | Full orchestrated review — blame-aware scoping, 3 review roles, 12 dimensions, adversarial pass, fix application, report generation |

| Agent | Purpose |
|-------|---------|
| `code-reviewer` | Autonomous reviewer — scans codebase for bugs, security vulnerabilities, AI slop, performance anti-patterns, accessibility violations, and release blockers |

## Key Capabilities

- **Opus 4.7 default, Sonnet/Haiku compatible** — set `--model` per run or pin via `.radcrconfig.yml`'s `review_model`
- **Parallel tool-call pipeline** — Steps 1–5 batch reads, greps, and shell checks; `run_in_background` for automated scans
- **JSON-first subagent output** — authoritative findings schema; markdown fallback only on parse failure
- **Checkpoint + `--resume`** — state written after Steps 5/7/9 so compaction mid-review is recoverable
- **`--non-interactive`** — structured return path for `code-reviewer` agent, `/loop`, CI
- **Blame-aware diff scoping** — only flag issues you introduced, not pre-existing noise
- **14-pattern AI slop detection** — hallucinated imports, fake error handling, placeholder stubs, silent failures, and 10 more
- **Framework-specific IDOR detection** — Next.js, Express, Fastify, Django, Rails, Go
- **Dynamic ARIA state detection** — catches hardcoded `aria-expanded`, `aria-selected`, `aria-checked`, `aria-pressed`
- **Performance heuristics** — N+1 queries, unbounded lists, sync blocking, bundle bloat, re-renders
- **8 project-type modules** — web app, API, Chrome extension, CLI, library, Electron, mobile, SaaS
- **Fix application with validation** — applies fixes, runs tests, verifies
- **Accepted-risk expiry enforcement** — stale `.radcrconfig.yml` entries are re-evaluated, not silently suppressed

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-code-review
```

Then just ask naturally:

```
Review my code
Is this ready to ship?
Check what I changed for security issues
Review changes since last release
```

Or use slash commands:

```bash
/rad-code-review diff                               # Review current diff (blame-aware, Opus 4.7)
/rad-code-review --since abc123                     # Review since a specific commit
/rad-code-review repo --strictness public           # Full repo, public release standard
/rad-code-review diff --model sonnet                # Cost-sensitive scan on Sonnet 4.6
/rad-code-review diff --non-interactive             # Agent/CI mode (no findings menu)
/rad-code-review --resume 2026-04-16-143022         # Resume an interrupted review
```

## Agent vs. Skill

- **Skill (`/rad-code-review`)** — full orchestrated workflow with interactive findings menu, fix application, `.radcrconfig.yml` acceptance flow. Default mode when a human triggers a review.
- **`code-reviewer` agent** — autonomous reviewer invoked by another Claude (or automatically after significant feature work). Returns findings directly without menu prompts. Use `subagent_type: "code-reviewer"` when spawning from other agents; use the skill when a human is driving.

The agent always runs in non-interactive mode. The skill supports `--non-interactive` to match that behavior for CI/loop contexts.

## Naming

Config file (`.radcrconfig.yml`), finding IDs (`RADCR-NNN`), and the state/history directories (`.radcr/state/`, `.radcr/history/`) use the RADCR prefix matching the plugin name.

**If you have an existing `.ucrconfig.yml`** from a prior version of this plugin: rename it to `.radcrconfig.yml`, and rename `.ucr/` (if present) to `.radcr/`. Earlier versions used a `UCR` prefix as a heritage from this plugin's "Universal Code Review" predecessor; that prefix was retired for consistency with the plugin name. Existing history files under `.ucr/history/` are still readable after the directory rename — no content changes required.

## Version

**3.0.0** — **Optimized for Claude Opus 4.7** while retaining Sonnet 4.6 and Haiku 4.5 compatibility.

- **Opus 4.7 default** — agent and skill primary-review model switched from Sonnet to Opus; `--model` flag + `.radcrconfig.yml` `review_model` override.
- **Parallel tool calls everywhere** — agent Phase 1 (entry points, auth, DB, APIs, config), orchestrator Steps 3a–3e (metadata, stack, trust, file list), Step 5 (automated checks via `run_in_background`). Deep reviews complete ~3–5× faster on Opus/Sonnet.
- **JSON-first subagent output** — primary and adversarial subagents emit JSON per schema in `references/subagent-prompts/*.md`. Markdown parsing retained as fallback.
- **Checkpoint + `--resume <run-id>`** — state written to `.radcr/state/<run-id>.json` after Steps 5/7/9. Compaction-safe.
- **`--non-interactive`** — skips the Step 10 findings menu; returns structured findings + verdict + report path. Used by the `code-reviewer` agent, `/loop`, CI.
- **Externalized subagent prompts** — moved from inline in `orchestrate-review.md` to `references/subagent-prompts/{primary,adversarial,self-adversarial}-review.md`. Easier to audit, version, and reuse.
- **`.radcrconfig.yml` expiry enforcement** — accepted risks with `expires < today` are surfaced as stale and re-evaluated rather than silently suppressed.
- **History filename unified** — `{YYYY-MM-DD}-{HHmmss}-{scope}-{strictness}.md` across both orchestrator Step 12 and report-generation.md. Multiple same-day reviews no longer overwrite each other.
- **Cleanup** — removed vestigial `install.sh`/`install.ps1` (plugin manifest handles install) and unused `scripts/*.sh` that no workflow referenced.

**2.2.0 and earlier** — see git log for history; v2.0 introduced blame-aware scoping, framework IDOR, performance heuristics, dynamic ARIA detection.

## License
Apache-2.0
