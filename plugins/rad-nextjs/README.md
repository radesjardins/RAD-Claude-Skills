# rad-nextjs

Comprehensive Next.js coding standards, security hardening, testing patterns, and troubleshooting guidance for Claude Code.

Built from 58 curated sources including official Next.js documentation, Vercel Academy, security guides, academic papers, Netflix engineering case studies, and web.dev performance research.

## Skills

### nextjs-best-practices
App Router architecture, Server/Client component boundaries, data fetching patterns, caching (`"use cache"`, ISR, revalidation), performance optimization (Core Web Vitals), layout patterns, Partial Prerendering, and deployment.

**Triggers:** Working on any Next.js project, creating components/pages/layouts, data fetching, caching, performance optimization, deployment.

### nextjs-security
Authentication with httpOnly cookies, 5-layer Server Action security checklist, CSP headers, CSRF/XSS prevention, environment variable management, Data Access Layer pattern, `server-only` package, React Taint APIs, and middleware security warnings (CVE-2025-29927).

**Triggers:** Implementing auth, writing Server Actions/API routes, configuring security headers, managing secrets, reviewing for OWASP vulnerabilities.

### nextjs-testing
Testing infrastructure with Vitest (unit), Cypress and Playwright (E2E), testing React Server Components, API route testing, resilient test patterns (`data-testid`, programmatic auth), and common anti-patterns.

**Triggers:** Writing tests, configuring test tools, testing Server Components, testing auth flows, CI/CD test integration.

### nextjs-troubleshooting
Diagnostic decision tree, serialization failures, hydration mismatches, stale auth in layouts, request waterfalls, memory leaks, Docker OOM crashes, middleware bypass, environment variable issues, and build/deploy debugging.

**Triggers:** Debugging errors, investigating performance issues, fixing build failures, diagnosing unexpected behavior.

## Installation

Add to your Claude Code plugins from the RAD-Claude-Skills marketplace, or install locally:

```bash
claude plugins add --dir /path/to/rad-nextjs
```

## Source Knowledge Base

All content derived from the "Next.js Guide" NotebookLM notebook containing 58 sources:
- Official Next.js documentation (App Router, Data Fetching, Caching, Security, Testing)
- Vercel Academy and Blog
- Security guides (TurboStarter, Vinta Software, Authgear, Arcjet)
- Academic papers (arXiv comparative analysis)
- Performance research (web.dev, DebugBear, Netflix Engineering)
- Community best practices (Reddit, dev.to)
- Framework comparisons and case studies
