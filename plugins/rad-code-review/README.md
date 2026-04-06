# rad-code-review — Catch what AI wrote wrong before it ships.

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

- **Blame-aware diff scoping** — only flag issues you introduced, not pre-existing noise
- **14-pattern AI slop detection** — hallucinated imports, fake error handling, placeholder stubs, silent failures, and 10 more
- **Framework-specific IDOR detection** — Next.js, Express, Fastify, Django, Rails, Go
- **Dynamic ARIA state detection** — catches hardcoded `aria-expanded`, `aria-selected`, `aria-checked`, `aria-pressed`
- **Performance heuristics** — N+1 queries, unbounded lists, sync blocking, bundle bloat, re-renders
- **8 project-type modules** — web app, API, Chrome extension, CLI, library, Electron, mobile, SaaS
- **Fix application with validation** — applies fixes, runs tests, verifies

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
/rad-code-review diff          # Review current diff (blame-aware)
/rad-code-review --since abc123  # Review since a specific commit
/rad-code-review repo --strictness public  # Full repo, public release standard
```

## License
Apache-2.0
