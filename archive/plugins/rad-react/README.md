# rad-react — Modern React patterns for Claude Code. Hooks, performance, security, and React 19.

React moves fast, and so does the list of ways to write it badly. rad-react keeps Claude aligned with current patterns — functional components, React 19 forms, secure data handling, and performance optimization — so you're not discovering anti-patterns or security gaps during code review.

## What You Can Do With This

- Get hooks-compliant component code that follows current React patterns
- Review a component for XSS vulnerabilities and insecure direct object references (IDOR)
- Optimize re-renders with the right memoization strategy for your use case
- Check that your forms, modals, and dynamic content meet WCAG 2.2 AA standards

## How It Works

| Skill | Purpose |
|-------|---------|
| `react-foundations` | Components, hooks, JSX, props, state management, context |
| `react-app-building` | Routing, layouts, forms, data fetching, server/client boundaries |
| `react-engineering` | Project tooling, testing, code organization, TypeScript integration |
| `react-performance` | Re-render optimization, memoization, lazy loading, profiling |
| `react-accessibility` | ARIA patterns, keyboard navigation, screen reader support |
| `react-security` | XSS prevention, IDOR checks, input sanitization, secure data handling |

| Agent | Purpose |
|-------|---------|
| `react-reviewer` | Reviews React code for anti-patterns, accessibility, performance, and security |

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-react
```

Claude activates these skills automatically when you work on React code. Or ask directly:

```
Review my React code for security issues
Is this component accessible?
Why is this re-rendering too much?
```

## License
Apache-2.0
