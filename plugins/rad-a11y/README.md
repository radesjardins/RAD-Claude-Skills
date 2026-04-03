# rad-a11y — Digital Accessibility Plugin

A comprehensive WCAG 2.2 AA accessibility toolkit for Claude Code. Built from 56 curated sources covering the W3C ARIA Authoring Practices Guide, axe-core/Deque testing tools, MDN Web Docs, and framework-specific patterns for React, Astro, and Tailwind CSS.

## Coverage

- **Standard**: WCAG 2.2 AA (includes new 2.2 criteria: Target Size, Focus Not Obscured, Accessible Authentication)
- **Stacks**: React / Next.js, Astro, Tailwind CSS, Radix UI, Headless UI
- **Testing**: axe-core, jest-axe, @axe-core/playwright, eslint-plugin-jsx-a11y

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `a11y-review` | `/rad-a11y:a11y-review` or "accessibility review" | Full 8-phase WCAG 2.2 AA audit with severity-ranked findings |
| `a11y-semantic-html` | "semantic HTML", "heading hierarchy", "landmark" | Heading hierarchy, landmark regions, div-vs-semantic, tables, lists |
| `a11y-aria-patterns` | "ARIA pattern", "aria-expanded", "APG pattern" | ARIA roles/states/properties, APG widget patterns (tabs, dialogs, comboboxes, menus, accordions), live regions, roving tabindex |
| `a11y-keyboard-focus` | "keyboard navigation", "focus management", "skip link" | Focus indicators, `:focus-visible`, skip links, modal focus trapping, React focus drift, keyboard patterns per component type |
| `a11y-forms` | "accessible form", "form label", "aria-invalid" | Label association, error messages, fieldset/legend, required fields, autocomplete, file uploads, password fields |
| `a11y-testing` | "accessibility test", "jest-axe", "axe-core" | eslint-plugin-jsx-a11y, jest-axe, @axe-core/playwright, CI/CD integration, axe result structure |

## Agent

**`a11y-reviewer`** — A proactive accessibility code reviewer that performs a 7-phase autonomous audit:
1. Codebase orientation (stack detection)
2. Semantic structure (headings, landmarks, element selection)
3. ARIA usage (aria-hidden, accessible names, state sync, live regions)
4. Keyboard and focus (focus indicators, traps, skip links, focus drift)
5. Visual and motion (contrast suspects, color-only meaning, animations)
6. Forms (labels, errors, required, fieldset/legend, autocomplete)
7. SVG and icons (decorative vs informative, Astro hydration issues)

Reports findings grouped by severity: **Critical** (blocks PR) → **Serious** → **Moderate** → **Minor**.

## Installation

```bash
# From this repo
claude --plugin-dir ./plugins/rad-a11y
```

Or copy to your project's `.claude-plugin/` directory.

## Quick Start

```
# Full page audit (slash command)
/rad-a11y:a11y-review src/pages/Home.tsx

# Full codebase audit
/rad-a11y:a11y-review all

# Ask Claude directly
"Review the accessibility of my LoginForm component"
"Check my navigation for WCAG compliance"
"Is this dialog accessible?"
"Set up axe-core testing for my React app"
```

## What's Covered

### WCAG Success Criteria Enforced
- **1.1.1** Non-text Content (alt text, aria-hidden)
- **1.3.1** Info and Relationships (semantic HTML, form labels)
- **1.3.5** Identify Input Purpose (autocomplete attributes)
- **1.4.1** Use of Color (not color-only meaning)
- **1.4.3** Contrast Minimum (4.5:1 text, 3:1 large text)
- **1.4.11** Non-text Contrast (UI components, focus rings)
- **2.1.1** Keyboard (all interactive elements operable)
- **2.1.2** No Keyboard Trap
- **2.3.3** Animation from Interactions (prefers-reduced-motion)
- **2.4.1** Bypass Blocks (skip links)
- **2.4.3** Focus Order (DOM order = reading order)
- **2.4.7** Focus Visible
- **2.4.11** Focus Not Obscured (WCAG 2.2)
- **2.5.8** Target Size Minimum (WCAG 2.2, 24×24px)
- **3.3.1** Error Identification
- **3.3.2** Labels or Instructions
- **4.1.2** Name, Role, Value

### Stack-Specific Patterns

**React**: JSX boolean ARIA states, useRef focus management, Fragment semantic preservation, key-prop focus loss, Radix UI asChild prop forwarding

**Astro**: Islands architecture hydration dead zones, client:visible keyboard risks, pre-hydration ARIA state via data-* attributes, accessible-astro-starter patterns

**Tailwind CSS**: `sr-only`/`not-sr-only`, `focus-visible:ring-*` vs `outline-none`, `motion-safe:`/`motion-reduce:` modifiers, `list-none` role restoration

## Sources

Built from 56 curated sources including:
- W3C WAI ARIA Authoring Practices Guide (APG)
- MDN Web Docs — Semantic HTML, ARIA, focus-visible, prefers-reduced-motion
- Deque / axe-core documentation
- Radix UI and Headless UI accessibility documentation
- Accessible Astro documentation
- WCAG 2.2 success criteria
- Tailwind CSS accessibility utilities documentation
