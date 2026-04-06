# rad-a11y — WCAG 2.2 AA accessibility built in, not bolted on.

Accessibility is easiest when it's part of how you build, not an audit you run afterward. rad-a11y brings WCAG 2.2 AA standards into your development workflow — semantic HTML, ARIA patterns, keyboard navigation, focus management, and automated testing with axe-core — so compliance isn't a separate phase.

## What You Can Do With This

- Review a component for accessibility violations before it ships — with specific WCAG criteria referenced
- Get correct ARIA roles and attributes for custom interactive elements (accordions, dialogs, tabs, comboboxes)
- Set up axe-core or jest-axe for automated a11y testing in your CI pipeline
- Fix keyboard navigation and focus management issues that screen readers expose

## How It Works

| Skill | Purpose |
|-------|---------|
| `a11y-semantic-html` | Semantic structure, heading hierarchy, landmark regions |
| `a11y-aria-patterns` | ARIA roles, attributes, live regions — when to use and when not to |
| `a11y-keyboard-focus` | Keyboard navigation, focus rings, focus trapping, skip links |
| `a11y-forms` | Accessible form labels, error messages, required fields |
| `a11y-testing` | axe-core, jest-axe, @testing-library, Playwright a11y testing |
| `a11y-review` | Full WCAG 2.2 AA audit of a component or page |

| Agent | Purpose |
|-------|---------|
| `a11y-reviewer` | Autonomous accessibility audit — WCAG failures, ARIA misuse, keyboard navigation, focus management |

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-a11y
```

```
Review my accessibility
Is this component keyboard accessible?
Check for WCAG violations
Set up axe-core testing
```

## License
Apache-2.0
