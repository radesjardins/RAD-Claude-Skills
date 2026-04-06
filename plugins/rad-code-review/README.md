# rad-code-review

3-role adversarial code review with diff-aware scoping and AI slop detection — the only code reviewer that catches what AI wrote badly and only flags what you changed.

Covers security (OWASP + framework-specific IDOR), architecture, 14-pattern AI slop detection, performance profiling heuristics, UX/accessibility (WCAG 2.2 + dynamic ARIA state), and release readiness with severity-ranked findings and optional fix application.

## Skills

| Skill | Purpose |
|-------|---------|
| `rad-code-review` | Full orchestrated review — blame-aware scoping, 3 review roles, 12 dimensions, adversarial pass, fix application, report generation |

## Agents

| Agent | Purpose |
|-------|---------|
| `code-reviewer` | Autonomous code reviewer — scans codebase for bugs, security vulnerabilities, AI slop, performance anti-patterns, accessibility violations, and release blockers |

## Usage

```bash
# Review your current diff (blame-aware — only flags your changes)
/rad-code-review diff

# Review changes since a specific commit
/rad-code-review --since abc123

# Review last commit before merging
/rad-code-review commit

# Full repository audit (no blame filtering)
/rad-code-review repo

# Override blame-aware default — flag everything in the diff
/rad-code-review diff --full-scan

# Strict mode for public release
/rad-code-review repo --strictness public
```

Or just say it naturally:

```
Review my code
Is this ready to ship?
Check what I changed for security issues
Review changes since last release
```

## Key Features

- **Blame-aware diff scoping** — only flag issues you introduced, with dependency chain detection
- **Incremental `--since` review** — review changes across multiple commits
- **Framework-specific IDOR detection** — Next.js, Express, Fastify, Django, Rails, Go
- **Performance profiling heuristics** — N+1, re-renders, unbounded lists, sync blocking, bundle bloat
- **Dynamic ARIA state detection** — hardcoded `aria-expanded`, `aria-selected`, `aria-checked`, `aria-pressed`
- **14-pattern AI slop detection** — hallucinated imports, fake error handling, placeholder stubs, silent failures
- **3-role adversarial review** — bug finder, architecture reviewer, release gate
- **8 project-type modules** — web-app, API, Chrome extension, CLI, library, Electron, mobile, SaaS
- **Fix application with validation** — apply fixes, run tests, verify
- **Report history and comparison** — track findings over time
