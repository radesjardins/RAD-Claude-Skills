# rad-tailwind

Comprehensive Tailwind CSS coding standards, architectural guidance, and anti-pattern enforcement for Claude Code.

Built from curated sources including official Tailwind CSS v4 documentation, the Tailwind CSS v4.0 release blog, Steve Kinney's Tailwind course (anti-patterns, CVA), official migration guides, tailwind-merge documentation, and MDN accessibility references. Updated for Tailwind CSS v4 / Oxide engine.

## Skills

| Skill | Purpose |
|-------|---------|
| `tailwind-best-practices` | Core standards: utility-first model, class ordering, @theme tokens, quick rules checklist |
| `tailwind-responsive-design` | Mobile-first patterns, container queries (@container), named containers, viewport vs container breakpoints |
| `tailwind-component-patterns` | CVA (Class Variance Authority), tailwind-merge, cn() utility, abstraction decision tree |
| `tailwind-dark-mode-theming` | Dark mode strategies (media/class), @theme directive, design tokens, multi-theme patterns |
| `tailwind-v4-migration` | v3 to v4 migration guide, Oxide engine, breaking changes, upgrade tool, browser requirements |
| `tailwind-accessibility` | Focus management (focus-visible:), sr-only, ARIA variants, forced-colors, color contrast |

## Agents

| Agent | Purpose |
|-------|---------|
| `tailwind-reviewer` | Reviews Tailwind code for anti-patterns, accessibility issues, and v4 best practice violations |

## Reference Files

| File | Content |
|------|---------|
| `references/v4-config-theming.md` | @theme syntax, design token namespaces, dark mode strategies, multi-theme patterns, v3 to v4 breaking changes, production optimization |
| `references/component-patterns.md` | CVA compound variants, tailwind-merge configuration, cn() patterns, container queries, framework integration (Astro/React/Vue) |
| `references/anti-patterns-edge-cases.md` | Full anti-pattern catalog, dynamic class safety, edge cases, accessibility implementation guide, browser support matrix |

## Key Principles Enforced

1. **Outside-In class ordering** — enforced by `prettier-plugin-tailwindcss`
2. **CSS-first configuration** — `@theme {}` replaces `tailwind.config.js`
3. **Component abstraction > CSS abstraction** — CVA over `@apply`
4. **Deterministic overrides** — `cn()` = `clsx` + `tailwind-merge`
5. **Mobile-first always** — no desktop-first overrides
6. **Container queries for components** — `@container` over viewport breakpoints for portable UI
7. **`focus-visible:` always** — never suppress focus rings without replacement
