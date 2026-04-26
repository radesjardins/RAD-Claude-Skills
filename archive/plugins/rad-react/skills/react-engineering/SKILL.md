---
name: react-engineering
description: This skill should be used when the user is setting up React project tooling, writing tests, organizing code, typing React with TypeScript, or creating reusable hooks. Triggers on "React testing", "React Testing Library", "component tests", "ESLint React", "eslint-plugin-react-hooks", "TypeScript React props", "typing hooks", "typing events", "custom hooks", "code organization", "feature-based folders", "React file structure", "getByRole", or "test React component".
---

# React Engineering Workflow

Linting, testing, code organization, TypeScript patterns, and reusable custom hooks for production React applications.

## ESLint Configuration

### Essential Plugins

**eslint-plugin-react-hooks** — enforces two critical rules:
- `rules-of-hooks` — hooks only at top level of components/custom hooks
- `exhaustive-deps` — dependency arrays include all reactive values

**eslint-plugin-jsx-a11y** — flags accessibility violations in JSX at build time (missing alt text, incorrect ARIA roles, missing keyboard handlers).

## Testing Strategy

### Core Principle

**Tests should resemble the way software is actually used.** Test behavior from the user's perspective, not implementation details.

### What to Test vs. Not Test

| Test | Do Not Test |
|------|-------------|
| User-visible behavior | Internal state values |
| DOM output and interactions | Component instance methods |
| Accessibility (roles, labels) | Implementation details |
| Error states and edge cases | Snapshot of non-visual code |

### React Testing Library Query Priority

Use queries that reflect how users and assistive technology find elements:

1. **`getByRole`** — primary selector (buttons, links, headings, form fields by ARIA role)
2. **`getByLabelText`** — form elements by their label
3. **`getByText`** — non-interactive elements by visible text
4. **`getByDisplayValue`** — inputs by current value
5. **`getByTestId`** — last resort only

If RTL cannot find the element by role, assistive technology cannot either — that is an accessibility bug.

### Testing Custom Hooks

Use React Testing Library with `renderHook` to test hooks in isolation. Test async operations, state changes, and cleanup behavior.

## Code Organization

### Feature-Based Structure

Group related code by feature, not by type:

```
src/
├── features/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   ├── LoginForm.test.tsx
│   │   ├── useAuth.ts
│   │   └── auth-api.ts
│   └── dashboard/
│       ├── Dashboard.tsx
│       ├── Dashboard.test.tsx
│       ├── widgets/
│       └── useDashboardData.ts
├── components/          # Shared/generic components
├── hooks/               # Shared hooks
├── lib/                 # Utilities
└── types/               # Shared TypeScript types
```

### Co-location

Keep tests, styles, and utilities next to the components that use them. App Router naturally supports this — route folders can contain components, tests, and utilities alongside `page.tsx`.

## TypeScript with React

### Typing Props

Use `interface` or `type`. Do not use `React.FC` — it is no longer recommended:

```tsx
interface CardProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
}

function Card({ title, subtitle, children }: CardProps) { ... }
```

### Typing Hooks

- `useState` infers from initial value — use generics for complex types: `useState<"idle" | "loading">("idle")`
- `useReducer` — type actions as discriminated unions for exhaustive checking
- `useRef` — `useRef<HTMLInputElement>(null)` for DOM refs

### Typing Events

Event types infer from inline handlers. For extracted functions, type explicitly:

```tsx
function handleClick(e: React.MouseEvent<HTMLButtonElement>) { ... }
function handleChange(e: React.ChangeEvent<HTMLInputElement>) { ... }
```

### Generics for Reusable Components

```tsx
interface SelectProps<T> {
  items: T[];
  selected: T;
  onSelect: (item: T) => void;
  getLabel: (item: T) => string;
}

function Select<T>({ items, selected, onSelect, getLabel }: SelectProps<T>) { ... }
```

## Custom Hooks Best Practices

- Name starts with `use` — required for ESLint and React to recognize hooks
- Share **stateful logic**, not state — each call gets independent state
- Keep focused on concrete use cases: `useOnlineStatus()`, `useDebounce(value, ms)`
- Return tuples with `as const` for correct type inference
- **Anti-pattern:** `useMount(fn)` lifecycle wrappers — bypass linting, break React paradigm

## Additional Resources

### Reference Files

- **`references/detailed-patterns.md`** — Complete code examples for testing patterns, TypeScript typing, custom hook templates, and ESLint configuration
