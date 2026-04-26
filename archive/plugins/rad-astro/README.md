# rad-astro — Astro 5/6 best practices. Islands, Content Layer, Server Islands, and performance.

Astro's Islands architecture and Content Layer are powerful but specific — and the patterns from React or Next.js don't always apply. rad-astro keeps Claude aligned with current Astro conventions: correct component boundaries, Content Layer v2 collections, Server Islands, and the performance optimizations that make Astro sites fast by default.

## What You Can Do With This

- Structure an Astro project with correct island boundaries — interactive only where needed
- Set up Content Layer v2 collections for type-safe content management
- Debug hydration, build, and SSR issues with a structured approach
- Audit your Astro site for Core Web Vitals issues and LCP optimization

## How It Works

| Skill | Purpose |
|-------|---------|
| `astro-best-practices` | Project structure, Islands architecture, component patterns, conventions |
| `astro-performance` | Core Web Vitals, LCP/CLS/INP, image optimization, bundle analysis |
| `astro-security` | CSP configuration, XSS prevention, input validation |
| `astro-accessibility` | ARIA patterns, WCAG compliance in Astro components |
| `astro-troubleshooting` | Hydration errors, build issues, SSR debugging, common anti-patterns |

| Agent | Purpose |
|-------|---------|
| `astro-reviewer` | Reviews Astro code for anti-patterns, performance issues, security, and accessibility |

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-astro
```

```
Review my Astro code
Is my Astro site production ready?
Check Astro performance
Fix this Astro hydration error
```

## License
Apache-2.0
