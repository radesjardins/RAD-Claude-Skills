# Astro Client Directives Cheatsheet

Quick decision tree for choosing the right hydration strategy.

## Decision Flow

```
Does this component need JavaScript?
  NO  → Don't add any client directive (default static HTML)
  YES → Does it need to work immediately on page load?
    YES → Is it above the fold and critical?
      YES → client:load
      NO  → client:idle
    NO  → Is it below the fold?
      YES → client:visible
      NO  → Does it only apply to certain screen sizes?
        YES → client:media="(max-width: 768px)"
        NO  → Does it rely on browser-only APIs (window, document)?
          YES → client:only="react" (specify framework)
          NO  → client:idle
```

## Performance Impact (least to most JS)

1. No directive (zero JS)
2. `server:defer` (zero client JS, streams HTML)
3. `client:visible` (deferred, may never load)
4. `client:media` (conditional on viewport)
5. `client:idle` (deferred until idle)
6. `client:load` (immediate — use sparingly)
7. `client:only` (no SSR, full client render)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `client:load` on everything | Audit: most components can use `client:idle` or `client:visible` |
| Wrapping layout in React component with `client:load` | Break into granular islands — hydrate only interactive parts |
| Mapping array into many `client:*` islands | Render list statically, hydrate one sorter/paginator |
| Using `client:only` when SSR works fine | Only use `client:only` for browser-API-dependent code |
| No fallback on `server:defer` | Always provide `<slot name="fallback">` content |
