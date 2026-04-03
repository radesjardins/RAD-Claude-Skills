---
name: react-performance
description: This skill should be used when the user is optimizing React performance, asking about "React re-renders", "useMemo", "useCallback", "React.memo", "code splitting", "lazy loading", "React.lazy", "bundle size", "rendering behavior", "React Compiler", "automatic memoization", "streaming", "Suspense performance", "prefetching", "parallel data fetching", "context performance", or debugging why a React component re-renders too often.
---

# React Performance

React rendering behavior, memoization strategies, code splitting, bundle optimization, and App Router-specific performance patterns. Focus on understanding when optimizations help vs. when they add unnecessary complexity.

## Rendering Behavior

React calculates the next UI, diffs against the previous version, and commits only minimum DOM changes. For this to work efficiently:

- Components must be **pure** — same inputs, same output
- State updates trigger re-renders of the component and all children
- React batches state updates within event handlers automatically

## Memoization — When and When Not

### useMemo

Cache expensive computations so they only re-run when dependencies change:

```tsx
const sorted = useMemo(() => expensiveSort(items), [items]);
```

**Use when:** The computation is measurably expensive (filtering thousands of items, complex calculations).
**Skip when:** Simple operations, cheap object creation — the overhead of memoization outweighs the savings.

### useCallback

Memoize function definitions to maintain reference equality:

```tsx
const handleClick = useCallback(() => { doThing(id); }, [id]);
```

**Use when:** Passing callbacks to children wrapped in `React.memo` — prevents child re-renders from new function references.
**Skip when:** Passing to native DOM elements or non-memoized children.

### React.memo

Skip re-rendering a component when its props haven't changed:

```tsx
const ExpensiveList = React.memo(function ExpensiveList({ items }: Props) {
  return items.map(item => <Item key={item.id} data={item} />);
});
```

**Use when:** Component renders are expensive and parent re-renders frequently with unchanged props.

### Do Not Over-Memoize

Wrapping everything in `useMemo`/`useCallback` adds memory overhead with no measurable benefit for cheap operations. Profile first, optimize second.

## React Compiler (Automatic Memoization)

The React Compiler uses static analysis to automatically memoize values derived from props or state. Significantly reduces the need for manual `useMemo` and `useCallback`.

- If the compiler detects code that breaks Rules of React, it safely skips those components
- Manual memoization still works alongside the compiler
- Gradually rolling out — check React docs for current status

## Code Splitting and Lazy Loading

### React.lazy + Suspense

Dynamically import components to split bundles by view:

```tsx
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Settings />
    </Suspense>
  );
}
```

### Server Components Reduce Bundle Size

Server Components execute on the server only — large dependencies (markdown parsers, date libraries, syntax highlighters) never enter the client bundle.

### Minimize Client Boundaries

Push `"use client"` as deep as possible. Keep large static layouts as Server Components; isolate interactivity into small Client Components.

### Development-Only Imports

Dynamically import dev tools to exclude from production:

```tsx
if (process.env.NODE_ENV !== 'production') {
  import('react-axe').then(axe => axe.default(React, ReactDOM, 1000));
}
```

## App Router Optimizations

### Streaming

Send static UI immediately, stream data-heavy components as they resolve:
- `loading.tsx` — route-level streaming fallback
- `<Suspense>` — per-component granular streaming

### Parallel Data Fetching

Avoid sequential waterfalls with `Promise.all()`:

```tsx
const [users, posts] = await Promise.all([fetchUsers(), fetchPosts()]);
```

### Prefetching

`<Link>` components auto-prefetch in production when entering the viewport. Navigations become near-instant.

### Caching

Next.js Data Cache stores `fetch` results automatically, avoiding redundant requests across renders.

## Anti-Patterns That Hurt Performance

| Anti-Pattern | Impact | Fix |
|---|---|---|
| Sequential fetches when independent | Multiplied load time | `Promise.all()` |
| Bloated Context providers | All consumers re-render on any change | Split contexts by concern |
| Missing/wrong dependency arrays | Stale closures or over-firing effects | Follow exhaustive-deps rule |
| Deep equality in React.memo | Unpredictable multi-second stalls | Restructure props, use stable references |
| Sync setState in useEffect | Extra render before paint | Restructure to avoid or use `useLayoutEffect` |
| Everything in `useMemo`/`useCallback` | Memory overhead, code noise | Profile first, memoize only when measured |

## Additional Resources

### Reference Files

- **`references/detailed-patterns.md`** — Profiling workflow, bundle analysis techniques, streaming architecture examples, and memoization decision tree
