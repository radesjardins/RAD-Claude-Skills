---
name: react-foundations
description: This skill should be used when the user is writing React components, working with JSX, managing props, using useState or other hooks, asking about "React component patterns", "hooks rules", "props destructuring", "state management", "useState", "useEffect", "useRef", "custom hooks basics", "JSX gotchas", "React rendering rules", "derived state", "useEffect anti-patterns", "useEffect vs event handler", "stale closure", "race condition in React", "React purity", or building any React UI with functional components. Covers modern React only — no class components.
---

# React Foundations

Modern React development patterns for functional components, JSX, props, state, and hooks. All guidance targets current React practices — no class components or legacy lifecycle methods.

## Component Purity

Components must be **pure and idempotent** — same inputs (props, state, context) always produce the same output. Side effects belong in event handlers or hooks like `useEffect`, never in the render path.

**Allowed:** Local mutation during rendering (creating and modifying arrays within the render function).
**Forbidden:** Mutating external variables, DOM manipulation, or network requests during render.

## JSX Rules

- Standard HTML attributes use camelCase: `htmlFor`, `tabIndex`, `className`
- ARIA and data attributes stay hyphen-cased: `aria-label`, `data-testid`
- Return a single root element — use Fragments (`<>...</>`) to avoid wrapper divs that break semantic layout
- Values passed into JSX are immutable — never mutate after passing

## Props Patterns

Props are **immutable snapshots** for a single render. Never mutate them directly.

- **Destructure in the signature:** `function Card({ title, children }) {}`
- **Default values via JS defaults:** `function Button({ variant = "primary" }) {}` — do not use `defaultProps` or `React.FC`
- **Composition via children:** Pass components as children to avoid prop drilling. This pattern enables passing Server Components into Client Components.

## State with useState

- **Immutable updates:** Use spread operator for objects/arrays — `useState` does not auto-merge
- **Functional updates:** When new state depends on previous: `setCount(prev => prev + 1)`
- **Lazy initialization:** Pass a function for expensive initial values: `useState(() => computeExpensive())`
- **Never mutate directly:** `state.value = 2` does not trigger re-render — always use the setter

## Rules of Hooks

Hooks must follow strict rules so React can track state between renders:

1. **Top level only** — never inside loops, conditions, nested functions, after early returns, or in try/catch
2. **React functions only** — call from functional components or custom hooks, nowhere else
3. **Dependency arrays must be exhaustive** — include all reactive values referenced inside the hook. Omitting dependencies causes stale closures.

Enforce with `eslint-plugin-react-hooks` — the `rules-of-hooks` and `exhaustive-deps` rules catch violations at build time.

## useEffect — Mental Model and Rules

**`useEffect` is an escape hatch to synchronize with systems outside of React** — not a lifecycle method and not a way to orchestrate data flow inside the component tree.

### The Key Question: Effect or Event Handler?

Ask *why* the code needs to run:

| Situation | Solution |
|-----------|----------|
| Triggered by a specific user action (click, submit, type) | **Event handler** |
| Runs because the component was displayed on screen | **`useEffect`** |
| Syncing with external system (WebSocket, DOM, 3rd-party library) | **`useEffect`** |
| Updating state Y when state X changes | **Calculate during render** — never `useEffect` |

### useEffect Anti-Patterns — Critical Rules

1. **Never use useEffect to compute derived state.** If you can calculate it from existing props/state, do it during render: `const fullName = firstName + ' ' + lastName;` — no effect needed.
2. **Always return a cleanup function** when subscribing, adding event listeners, or starting timers. Failure causes memory leaks and stale handlers.
3. **Never pass an async function directly** to useEffect. Define an inner async function and call it.
4. **Race conditions in data fetching:** Use `AbortController` + cleanup to cancel stale requests. Every `fetch` inside `useEffect` needs cancellation handling.
5. **Never chain Effects** to update state based on other state — this causes cascading re-renders and brittle code.
6. **Object/function dependencies:** Pass primitive values (e.g., `user.id`) or memoize with `useCallback`/`useMemo` to prevent unnecessary re-runs.

```tsx
// CORRECT: cleanup + AbortController
useEffect(() => {
  const controller = new AbortController();
  async function load() {
    const data = await fetchUser(id, { signal: controller.signal });
    setUser(data);
  }
  load();
  return () => controller.abort();
}, [id]);

// WRONG: async directly as effect, no cleanup
useEffect(async () => { setUser(await fetchUser(id)); }, [id]);
```

See `references/detailed-patterns.md` for the complete list of 15 useEffect mistakes with fixes.

## Derived State — Core Rule

**If a value can be computed from existing props or state, it is NOT state.** Never store it in `useState` and never sync it with `useEffect`.

```tsx
// BAD: double render, brittle synchronization
const [fullName, setFullName] = useState('');
useEffect(() => setFullName(`${firstName} ${lastName}`), [firstName, lastName]);

// GOOD: calculated during render
const fullName = `${firstName} ${lastName}`;
```

Use `useMemo` only if the calculation is provably expensive.

## Core Hooks Quick Reference

| Hook | Purpose | Key Pattern |
|------|---------|-------------|
| `useState` | Component memory | Functional updates: `set(prev => ...)` |
| `useEffect` | Sync with external systems only | Always cleanup; use event handlers for user actions |
| `useRef` | Mutable value that persists across renders | DOM refs, timers, previous values |
| `useMemo` | Cache expensive computations | Only when measurably expensive; React Compiler handles the rest |
| `useCallback` | Stable function references | When passing to `React.memo`-wrapped children |
| `useReducer` | Complex state logic | Discriminated union actions with TypeScript |
| `useContext` | Read context without nesting | Keep providers as deep in the tree as possible |

## Custom Hooks

Extract reusable stateful logic into functions starting with `use`. Each call gets independent state.

- Keep hooks focused on concrete use cases: `useOnlineStatus()`, `useChatRoom(options)`
- **Anti-pattern:** Abstract lifecycle wrappers like `useMount(fn)` — these bypass linting and break the React paradigm
- Return tuples with `as const` for correct TypeScript inference

## Additional Resources

### Reference Files

- **`references/detailed-patterns.md`** — Complete code examples for all hook patterns, prop patterns, JSX edge cases, and common anti-patterns with fixes
