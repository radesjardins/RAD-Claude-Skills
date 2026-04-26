# React Foundations — Detailed Patterns

## Component Purity Examples

```tsx
// GOOD: Local mutation during render
function FruitList({ items }) {
  const sorted = [...items].sort(); // copy, then mutate the copy
  return <ul>{sorted.map(i => <li key={i}>{i}</li>)}</ul>;
}

// BAD: Mutating external variable during render
let count = 0;
function Counter() {
  count++; // Side effect in render — breaks purity
  return <p>{count}</p>;
}
```

## JSX Gotchas

```tsx
// Fragment avoids breaking semantic HTML
function TableRow({ cells }) {
  return (
    <>
      {cells.map(c => <td key={c.id}>{c.value}</td>)}
    </>
  );
}

// ARIA stays hyphen-cased, DOM props use camelCase
<input
  tabIndex={0}
  aria-label="Search"
  aria-required="true"
  htmlFor="search-input"
/>
```

## Props Patterns

```tsx
// Modern default props — standard JS defaults
interface ButtonProps {
  variant?: "primary" | "secondary";
  size?: "sm" | "md" | "lg";
  children: React.ReactNode;
}

function Button({ variant = "primary", size = "md", children }: ButtonProps) {
  return <button className={`btn-${variant} btn-${size}`}>{children}</button>;
}

// Composition via children (avoids prop drilling)
// Server Component passed into Client Component
<ClientModal>
  <ServerDataFetcher />  {/* Stays on server */}
</ClientModal>
```

## State Management Patterns

```tsx
// Immutable object updates
const [user, setUser] = useState({ name: "", email: "" });
setUser(prev => ({ ...prev, name: "Alice" })); // Spread existing, override one field

// Immutable array updates
const [items, setItems] = useState<string[]>([]);
setItems(prev => [...prev, "new item"]);           // Add
setItems(prev => prev.filter(i => i !== "remove")); // Remove
setItems(prev => prev.map(i => i === "old" ? "new" : i)); // Update

// Functional update — safe in async and batched updates
setCount(prev => prev + 1);

// Lazy initialization — expensive computation runs once
const [data] = useState(() => parseExpensiveCSV(rawData));
```

## Hook Patterns

### useEffect Cleanup

```tsx
// Subscription with cleanup
useEffect(() => {
  const ws = new WebSocket(url);
  ws.onmessage = (e) => setMessages(prev => [...prev, e.data]);
  return () => ws.close(); // Cleanup on unmount or dependency change
}, [url]);

// Timer with cleanup
useEffect(() => {
  const id = setInterval(() => tick(), 1000);
  return () => clearInterval(id);
}, []);
```

### useRef for DOM and Mutable Values

```tsx
// DOM ref
const inputRef = useRef<HTMLInputElement>(null);
const focusInput = () => inputRef.current?.focus();

// Mutable value that persists without causing re-render
const prevValue = useRef(value);
useEffect(() => {
  prevValue.current = value;
});
```

### useReducer with Discriminated Unions

```tsx
type Action =
  | { type: "increment" }
  | { type: "decrement" }
  | { type: "set"; payload: number };

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case "increment": return state + 1;
    case "decrement": return state - 1;
    case "set": return action.payload;
  }
}

const [count, dispatch] = useReducer(reducer, 0);
dispatch({ type: "set", payload: 42 });
```

## Custom Hook Patterns

```tsx
// Reusable data fetching hook
function useData<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    fetch(url)
      .then(r => r.json())
      .then(d => { if (!cancelled) setData(d); })
      .catch(e => { if (!cancelled) setError(e); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [url]);

  return { data, error, loading } as const;
}

// Online status hook
function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  useEffect(() => {
    const onOnline = () => setIsOnline(true);
    const onOffline = () => setIsOnline(false);
    window.addEventListener("online", onOnline);
    window.addEventListener("offline", onOffline);
    return () => {
      window.removeEventListener("online", onOnline);
      window.removeEventListener("offline", onOffline);
    };
  }, []);
  return isOnline;
}
```

## Common Anti-Patterns

| Anti-Pattern | Why It's Wrong | Fix |
|---|---|---|
| Mutating state directly (`state.x = 1`) | No re-render triggered | Use setter with spread |
| Hooks inside conditions | Breaks call order between renders | Move condition inside the hook |
| Missing deps in useEffect | Stale closures — uses outdated values | Add all reactive values to deps array |
| `useMount(fn)` wrapper | Bypasses exhaustive-deps linting | Use `useEffect` directly |
| `React.FC` for typing | Deprecated pattern, implicit children | Type props interface directly |
| Creating functions in render without memo | New reference every render breaks child memo | `useCallback` when passing to memoized children |

---

## 15 Common useEffect Mistakes (With Fixes)

### 1. Missing Dependency Array → Infinite Loop

```tsx
// BAD: runs on every render, likely causes infinite loop
useEffect(() => { setCount(count + 1); });

// GOOD: dependency array controls when it runs
useEffect(() => { /* side effect */ }, []);
```

### 2. Stale Props (Missing Dependency)

```tsx
// BAD: uses stale userId — effect never updates
useEffect(() => { fetchUser(userId); }, []);

// GOOD: re-runs when userId changes
useEffect(() => { fetchUser(userId); }, [userId]);
```

### 3. Derived State in useEffect → Double Render

```tsx
// BAD: forces extra render with stale value, then correct value
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);

// GOOD: calculate during render, zero extra renders
const fullName = `${firstName} ${lastName}`;
```

### 4. Resetting State on Prop Change → Complex and Slow

```tsx
// BAD: effect fires after render with old state visible
useEffect(() => {
  if (userId !== prevUserId.current) {
    setProfile(null);
    prevUserId.current = userId;
  }
}, [userId]);

// GOOD: pass key prop — React resets automatically
<UserProfile key={userId} userId={userId} />
```

### 5. Data Fetch Without Cancellation → Race Condition

```tsx
// BAD: stale response overwrites current data if user clicks fast
useEffect(() => {
  fetchProduct(productId).then(setProduct);
}, [productId]);

// GOOD: AbortController cancels stale requests
useEffect(() => {
  const controller = new AbortController();
  fetchProduct(productId, { signal: controller.signal })
    .then(setProduct)
    .catch(err => { if (err.name !== 'AbortError') setError(err); });
  return () => controller.abort();
}, [productId]);
```

### 6. Boolean Flag Pattern (Alternative to AbortController)

```tsx
useEffect(() => {
  let isCancelled = false;
  async function load() {
    const data = await fetchData(id);
    if (!isCancelled) setData(data);
  }
  load();
  return () => { isCancelled = true; };
}, [id]);
```

### 7. Async Function Passed Directly to useEffect

```tsx
// BAD: useEffect callback returns a Promise, not a cleanup function
useEffect(async () => {
  const data = await fetchData();
  setData(data);
}, []);

// GOOD: define inner async function, call it
useEffect(() => {
  async function load() {
    const data = await fetchData();
    setData(data);
  }
  load();
}, []);
```

### 8. Missing Cleanup for Event Listeners → Memory Leak

```tsx
// BAD: adds listener on every render, never removes
useEffect(() => {
  window.addEventListener('resize', handleResize);
});

// GOOD: cleanup removes listener on unmount
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, [handleResize]);
```

### 9. Unstable Object/Function Dependencies → Infinite Re-runs

```tsx
// BAD: new object reference every render triggers effect infinitely
useEffect(() => {
  initLibrary(options);
}, [options]); // options is { theme: 'dark' } created inline

// GOOD: pass stable primitives
useEffect(() => {
  initLibrary({ theme });
}, [theme]);

// OR: memoize with useMemo/useCallback
const stableOptions = useMemo(() => ({ theme }), [theme]);
```

### 10. Chained Effects → Cascading Re-renders

```tsx
// BAD: multiple re-renders, brittle cascade
useEffect(() => { setStep(step + 1); }, [cart]);
useEffect(() => { validateStep(step); }, [step]);

// GOOD: single event handler handles the whole flow
function handleCartUpdate(newCart) {
  setCart(newCart);
  validateStep(currentStep + 1);
}
```

### 11. Event-Specific Logic in useEffect

```tsx
// BAD: useEffect can't distinguish HOW the state changed
useEffect(() => {
  if (submitted) {
    toast('Order placed!');
    trackAnalytics('order_submit');
  }
}, [submitted]);

// GOOD: handle it in the event handler where it belongs
async function handleSubmit() {
  await submitOrder(cart);
  setSubmitted(true);
  toast('Order placed!');
  trackAnalytics('order_submit');
}
```

### 12. Using useEffect When useLayoutEffect Is Needed

```tsx
// BAD: useEffect fires after browser paints — causes flash
useEffect(() => {
  const { height } = element.current.getBoundingClientRect();
  setTooltipTop(height);
}, []);

// GOOD: useLayoutEffect fires before browser paints
useLayoutEffect(() => {
  const { height } = element.current.getBoundingClientRect();
  setTooltipTop(height);
}, []);
```

### 13. External Store Subscription via useEffect

```tsx
// BAD: useEffect + useState for external stores has tearing risks
useEffect(() => {
  const unsubscribe = store.subscribe(() => setState(store.getState()));
  return unsubscribe;
}, []);

// GOOD: useSyncExternalStore is purpose-built for this
const state = useSyncExternalStore(store.subscribe, store.getState);
```

### 14. Non-Reactive Logic in Dependencies (React 19+)

```tsx
// BAD: analytics callback doesn't need to be reactive,
// but adding it to deps causes unnecessary re-runs
useEffect(() => {
  connectToRoom(roomId);
  onConnect(user); // shouldn't be a dependency
}, [roomId, onConnect, user]);

// GOOD: useEffectEvent extracts non-reactive logic (React 19+)
const onConnectEvent = useEffectEvent(() => onConnect(user));
useEffect(() => {
  connectToRoom(roomId);
  onConnectEvent();
}, [roomId]);
```

### 15. Setting State After Unmount → Warning and Memory Leak

```tsx
// BAD: async callback may fire after component unmounts
useEffect(() => {
  fetch('/api/data').then(r => r.json()).then(setData); // setData after unmount
}, []);

// GOOD: isMounted flag prevents stale setState
useEffect(() => {
  let mounted = true;
  fetch('/api/data')
    .then(r => r.json())
    .then(data => { if (mounted) setData(data); });
  return () => { mounted = false; };
}, []);
```

---

## AI-Generated React Code: Common Mistakes to Watch For

AI coding assistants frequently introduce these patterns because they were trained on older or misguided examples. Flag immediately in code review:

| AI Pattern | Problem | Fix |
|---|---|---|
| `useEffect(async () => {...}, [])` | Returns Promise, not cleanup | Inner async function pattern |
| Derived state via `useState` + `useEffect` | Double render, stale flash | Calculate directly during render |
| `useCallback(() => fn(), [])` with empty deps | Stale closure — captures initial props/state only | Add all referenced values to deps |
| `key={index}` on dynamic lists | Breaks reconciliation on reorder/insert | Use stable unique IDs |
| Uncontrolled input with `onChange` that does nothing | Controlled/uncontrolled mismatch | Pick one pattern |
| `useEffect` inside conditional | Rules of Hooks violation — runtime crash | Move condition inside the hook |
| Missing `AbortController` on fetch in effect | Race conditions on rapid dependency changes | Always add cleanup |
| Global Context for frequently-changing data | Every consumer re-renders | Split contexts; use Zustand for hot state |
| `dangerouslySetInnerHTML` without sanitization | XSS vulnerability | DOMPurify before rendering |
| Third-party library initialized in every component's `useEffect` | Runs multiple times | Initialize once in root `App.tsx` |
| `console.log(user)` logging full objects in production | Sensitive data in browser console | Remove before commit; guard with NODE_ENV |
