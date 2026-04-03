# React Performance — Detailed Patterns

## Memoization Decision Tree

```
Should I memoize this?

1. Is it a VALUE (computed during render)?
   → Is the computation measurably expensive? (>1ms, runs frequently)
     → YES: useMemo(() => compute(deps), [deps])
     → NO: Skip it. Recalculation is cheaper than memoization overhead.

2. Is it a FUNCTION (passed as prop)?
   → Is the child wrapped in React.memo?
     → YES: useCallback(() => fn(deps), [deps])
     → NO: Skip it. The child re-renders anyway.

3. Is it a COMPONENT (re-renders with unchanged props)?
   → Is the render expensive? (large list, complex layout)
     → YES: React.memo(Component)
     → NO: Skip it. React's diffing is already fast.

When in doubt: Profile with React DevTools Profiler first.
```

## Profiling Workflow

### React DevTools Profiler

1. Open React DevTools → Profiler tab
2. Click Record → interact with the app → Stop
3. Look for:
   - Components that render when they shouldn't (highlighted in flame graph)
   - Render duration per component
   - "Why did this render?" annotations

### Identifying Unnecessary Re-Renders

```tsx
// Debug: Log renders in development
function ExpensiveComponent({ data }: Props) {
  console.count('ExpensiveComponent render');
  // If this logs more than expected, investigate the parent's state changes
}
```

## Bundle Analysis

```bash
# Next.js built-in analyzer
ANALYZE=true npm run build

# Or use webpack-bundle-analyzer
npm install --save-dev @next/bundle-analyzer
```

```js
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});
module.exports = withBundleAnalyzer(nextConfig);
```

Key things to look for:
- Large packages that could be lazy-loaded or replaced
- Duplicate packages (different versions of the same library)
- Server-only code appearing in client bundles

## Streaming Architecture

```tsx
// Full streaming example with multiple Suspense boundaries
import { Suspense } from 'react';

export default async function DashboardPage() {
  // This data is fast — fetch immediately
  const user = await fetchUser();

  return (
    <div className="dashboard">
      {/* Instant render — no data dependency */}
      <Header user={user} />

      <div className="grid">
        {/* Streams independently — slow chart doesn't block metrics */}
        <Suspense fallback={<MetricsSkeleton />}>
          <MetricsPanel />
        </Suspense>

        <Suspense fallback={<ChartSkeleton />}>
          <RevenueChart />  {/* Slow query, streams when ready */}
        </Suspense>

        <Suspense fallback={<ActivitySkeleton />}>
          <RecentActivity />
        </Suspense>
      </div>
    </div>
  );
}
```

## Context Performance Optimization

```tsx
// BAD: One giant context with everything
const AppContext = createContext({
  user: null,
  theme: 'light',
  notifications: [],
  cart: [],
  // Every consumer re-renders when ANY of these change
});

// GOOD: Split by concern
const UserContext = createContext<User | null>(null);
const ThemeContext = createContext<'light' | 'dark'>('light');
const NotificationContext = createContext<Notification[]>([]);

// Each consumer only re-renders when its specific context changes
```

## Lazy Loading Patterns

### Route-Based Code Splitting

```tsx
import { lazy, Suspense } from 'react';

// Each route loads its own bundle
const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

### Component-Level Lazy Loading

```tsx
// Heavy component loaded only when needed
const MarkdownEditor = lazy(() => import('./MarkdownEditor'));

function PostForm({ showEditor }: { showEditor: boolean }) {
  return (
    <form>
      <input name="title" />
      {showEditor && (
        <Suspense fallback={<textarea placeholder="Loading editor..." />}>
          <MarkdownEditor />
        </Suspense>
      )}
    </form>
  );
}
```

## Parallel vs Sequential Data Fetching

```tsx
// BAD: Sequential waterfall — each waits for previous
async function Page() {
  const user = await fetchUser();          // 200ms
  const posts = await fetchPosts(user.id); // 300ms (depends on user)
  const comments = await fetchComments();  // 150ms (independent!)
  // Total: 650ms — comments waited unnecessarily
}

// GOOD: Parallel where possible, sequential where necessary
async function Page() {
  const user = await fetchUser();                    // 200ms
  const [posts, comments] = await Promise.all([
    fetchPosts(user.id),  // 300ms (needs user)
    fetchComments(),      // 150ms (independent)
  ]);
  // Total: 500ms — comments fetched in parallel with posts
}

// BEST: Use Suspense for independent sections
async function Page() {
  return (
    <>
      <Suspense fallback={<UserSkeleton />}>
        <UserSection />     {/* Fetches its own data */}
      </Suspense>
      <Suspense fallback={<PostsSkeleton />}>
        <PostsSection />    {/* Fetches independently, streams when ready */}
      </Suspense>
      <Suspense fallback={<CommentsSkeleton />}>
        <CommentsSection /> {/* Fetches independently, streams when ready */}
      </Suspense>
    </>
  );
}
```

## Keys and Reconciliation

```tsx
// BAD: Index as key — causes bugs with reordering, filtering, inserting
{items.map((item, index) => <Item key={index} data={item} />)}

// GOOD: Stable, unique ID as key
{items.map(item => <Item key={item.id} data={item} />)}

// Use key to force remount (reset state) when entity changes
<ProfileForm key={selectedUserId} userId={selectedUserId} />
```
