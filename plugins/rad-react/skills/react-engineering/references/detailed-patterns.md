# React Engineering — Detailed Patterns

## ESLint Configuration

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "plugin:jsx-a11y/recommended"
  ],
  "plugins": ["react", "react-hooks", "jsx-a11y"],
  "rules": {
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "warn",
    "jsx-a11y/alt-text": "error",
    "jsx-a11y/anchor-is-valid": "error",
    "jsx-a11y/click-events-have-key-events": "error",
    "jsx-a11y/no-noninteractive-element-interactions": "warn"
  },
  "settings": {
    "react": { "version": "detect" }
  }
}
```

## Component Testing

```tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SearchBar } from './SearchBar';

test('filters results as user types', async () => {
  const user = userEvent.setup();
  const onSearch = vi.fn();

  render(<SearchBar onSearch={onSearch} />);

  // Find by role — accessible query
  const input = screen.getByRole('searchbox', { name: /search/i });
  await user.type(input, 'react hooks');

  await waitFor(() => {
    expect(onSearch).toHaveBeenCalledWith('react hooks');
  });
});

test('shows error state when search fails', async () => {
  const user = userEvent.setup();
  render(<SearchBar onSearch={() => { throw new Error('fail'); }} />);

  const input = screen.getByRole('searchbox');
  await user.type(input, 'test');
  await user.keyboard('{Enter}');

  expect(screen.getByRole('alert')).toHaveTextContent(/search failed/i);
});
```

## Testing Async Components

```tsx
test('displays user data after loading', async () => {
  render(<UserProfile userId="123" />);

  // Initially shows loading state
  expect(screen.getByText(/loading/i)).toBeInTheDocument();

  // Wait for data to appear
  const heading = await screen.findByRole('heading', { name: /alice/i });
  expect(heading).toBeInTheDocument();

  // Loading state gone
  expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
});
```

## Testing Custom Hooks

```tsx
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

test('increments and decrements', () => {
  const { result } = renderHook(() => useCounter(0));

  expect(result.current.count).toBe(0);

  act(() => result.current.increment());
  expect(result.current.count).toBe(1);

  act(() => result.current.decrement());
  expect(result.current.count).toBe(0);
});

test('respects min/max bounds', () => {
  const { result } = renderHook(() => useCounter(0, { min: 0, max: 5 }));

  act(() => result.current.decrement());
  expect(result.current.count).toBe(0); // Does not go below min

  for (let i = 0; i < 10; i++) act(() => result.current.increment());
  expect(result.current.count).toBe(5); // Does not exceed max
});
```

## TypeScript Patterns

### Props with Children

```tsx
// Explicit children typing (React.FC no longer recommended)
interface LayoutProps {
  children: React.ReactNode;
  sidebar?: React.ReactNode;
}

function Layout({ children, sidebar }: LayoutProps) {
  return (
    <div className="layout">
      {sidebar && <aside>{sidebar}</aside>}
      <main>{children}</main>
    </div>
  );
}
```

### Discriminated Union for useReducer

```tsx
type State = { status: "idle" } | { status: "loading" } | { status: "success"; data: User[] } | { status: "error"; error: string };

type Action =
  | { type: "FETCH_START" }
  | { type: "FETCH_SUCCESS"; payload: User[] }
  | { type: "FETCH_ERROR"; error: string };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "FETCH_START":
      return { status: "loading" };
    case "FETCH_SUCCESS":
      return { status: "success", data: action.payload };
    case "FETCH_ERROR":
      return { status: "error", error: action.error };
  }
}
```

### Generic Reusable Components

```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
  emptyMessage?: string;
}

function List<T>({ items, renderItem, keyExtractor, emptyMessage }: ListProps<T>) {
  if (items.length === 0) return <p>{emptyMessage ?? "No items"}</p>;
  return (
    <ul>
      {items.map((item, i) => (
        <li key={keyExtractor(item)}>{renderItem(item, i)}</li>
      ))}
    </ul>
  );
}

// Usage — T is inferred
<List
  items={users}
  keyExtractor={u => u.id}
  renderItem={u => <span>{u.name}</span>}
/>
```

### Typing Events

```tsx
// Inline — types inferred automatically
<button onClick={(e) => { /* e is React.MouseEvent<HTMLButtonElement> */ }}>

// Extracted handler — must type explicitly
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  const data = new FormData(e.currentTarget);
};

// Generic event for multiple element types
const handleInput = (e: React.SyntheticEvent<HTMLElement>) => {
  console.log(e.currentTarget.id);
};
```

### Custom Hook Return Types

```tsx
// Use `as const` for tuple returns
function useToggle(initial = false) {
  const [value, setValue] = useState(initial);
  const toggle = useCallback(() => setValue(v => !v), []);
  return [value, toggle] as const;
  // Returns: readonly [boolean, () => void]
  // Without `as const`: (boolean | (() => void))[] — loses type specificity
}
```

## Reusable Custom Hooks

### useDebounce

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}

// Usage
const debouncedQuery = useDebounce(searchQuery, 300);
useEffect(() => {
  fetchResults(debouncedQuery);
}, [debouncedQuery]);
```

### useLocalStorage

```tsx
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((prev: T) => T)) => {
    setStoredValue(prev => {
      const next = value instanceof Function ? value(prev) : value;
      window.localStorage.setItem(key, JSON.stringify(next));
      return next;
    });
  }, [key]);

  return [storedValue, setValue] as const;
}
```
