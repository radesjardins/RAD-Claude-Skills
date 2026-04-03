# rad-astro

Comprehensive Astro framework coding standards, security hardening, accessibility compliance, performance optimization, and troubleshooting for Claude Code.

Built from curated sources including official Astro documentation, performance guides, security best practices, and WCAG 2.2 accessibility standards. Updated for Astro 5/6.

## Skills

| Skill | Purpose |
|-------|---------|
| `astro-best-practices` | Core architecture: Islands, Content Layer v2, Actions, middleware, rendering modes, TypeScript |
| `astro-performance` | Core Web Vitals, hydration strategies, streaming, Fonts API, CSS, prefetching, CDN |
| `astro-security` | CSP, XSS/set:html, secrets, Session API, CSRF, cookies, middleware security |
| `astro-accessibility` | WCAG 2.2 AA, semantic HTML, ARIA, keyboard nav, focus management, axe-core CI |
| `astro-troubleshooting` | Anti-patterns, Astro 5/6 migration pitfalls, edge cases, diagnosis table |

## Agents

| Agent | Purpose |
|-------|---------|
| `astro-reviewer` | Autonomous code review for performance, security, accessibility, and stale patterns |

## What This Plugin Enforces

### Hard Rules (Never Violate)

- No client directive = no JavaScript (the fundamental rule)
- Never default to client:load without justification
- Never wrap layouts in framework components with client:load
- Never use set:html with unsanitized user content
- Never put secrets in import.meta.env (inlined at build time in Astro 6)
- Never use astro:content on the client
- Never overwrite context.locals (append only)
- Always use explicit loaders in content.config.ts (Astro 5+)
- entry.id replaces entry.slug (Astro 5+)
- render() is a utility import, not a method (Astro 5+)
- prerender flags must be static booleans (no dynamic values)

### Architecture Principles

- Static First: every component is HTML unless interactivity is explicitly needed
- Content-first MPA mindset, not SPA
- Separation of environments: build-time / server / browser
- Security by default: CSP, CSRF, origin checking
- Accessibility as a requirement, not an afterthought

## Installation

```bash
claude plugins install rad-astro@rad-claude-skills
```

## Usage

Skills activate automatically when working on Astro projects. The agent can be invoked with:

- "Review my Astro code"
- "Check Astro performance"
- "Audit my Astro site for accessibility"
- "Is my Astro app production ready?"

## Author

RAD
