---
name: react-app-building
description: This skill should be used when the user is building a React application with routing, layouts, forms, data fetching, mutations, or working with server/client component boundaries. Triggers on "React routing", "App Router pages", "React forms", "server actions", "data fetching in React", "server component", "client component", "use client directive", "Suspense boundary", "streaming", "React layouts", "nested routes", "form validation", "mutations in React", "server vs client component", "useActionState", "useFormStatus", "useOptimistic", "React 19 forms", "optimistic UI", "form pending state".
---

# React App Building

Patterns for building complete React applications: routing, layouts, forms, data fetching, mutations, and the server/client boundary. Aligned with the React Server Components (RSC) model and App Router conventions.

## Routing and Layouts

### File-System Routing

Routes map to folders with `page.tsx` files. Colocate UI components, tests, and utilities directly within route folders.

```
app/
├── layout.tsx          # Root layout (required) — wraps <html> and <body>
├── page.tsx            # Home route (/)
├── dashboard/
│   ├── layout.tsx      # Dashboard layout — persists across child navigation
│   └── page.tsx        # /dashboard
└── settings/
    └── page.tsx        # /settings
```

### Layouts and Partial Rendering

Layouts wrap nested pages via `children` prop. On navigation, **only the page re-renders** — the layout preserves client-side React state (partial rendering).

### Navigation

Use the `<Link>` component for client-side transitions without full page refresh. In production, routes are **automatically prefetched** when `<Link>` enters the viewport.

## Forms and Mutations

### Server Actions

Declare server-side async functions with `'use server'` directive. Pass directly to `<form action={...}>` — receives native `FormData` automatically.

**Progressive enhancement:** Forms work even before JavaScript loads on the client.
**Security:** Server Actions are public POST endpoints. Always verify authentication AND authorization inside every action. Never trust client-side validation alone.

### Validation Pattern

Validate `FormData` with Zod before database operations:

1. Define Zod schema for expected shape
2. Parse FormData through schema
3. Return structured errors if validation fails
4. Proceed with mutation only on valid data

### After Mutation

- `revalidatePath(path)` — purge client cache, fetch fresh server data
- `redirect(path)` — navigate to updated page
- Use `bind` to attach IDs to actions (not hidden inputs)

## React 19 Form Hooks

React 19 introduces first-class form state management via three companion hooks. These replace the manual `useState` + `useEffect` fetch pattern for mutations.

### `useActionState` — Action State Manager

Wraps a Server Action and manages its pending state, result, and error automatically:

```tsx
'use client';
import { useActionState } from 'react';
import { createPost } from './actions';

const initialState = { errors: {}, message: null };

export function CreatePostForm() {
  const [state, formAction, isPending] = useActionState(createPost, initialState);

  return (
    <form action={formAction}>
      <input name="title" aria-describedby="title-error" />
      {state.errors?.title && (
        <span id="title-error" aria-live="polite">{state.errors.title}</span>
      )}
      <button type="submit" disabled={isPending}>
        {isPending ? 'Saving…' : 'Save'}
      </button>
    </form>
  );
}
```

### `useFormStatus` — Parent Form Pending State

Reads the pending state of the **nearest parent `<form>`** — no prop drilling required:

```tsx
'use client';
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Saving…' : 'Save'}
    </button>
  );
}

// Must be rendered inside a <form> — works with Server or Client Actions
```

### `useOptimistic` — Instant UI Updates

Updates UI immediately on user interaction and rolls back if the server action fails:

```tsx
'use client';
import { useOptimistic } from 'react';

function TodoList({ todos, addTodoAction }) {
  const [optimisticTodos, addOptimistic] = useOptimistic(
    todos,
    (state, newTodo) => [...state, { ...newTodo, pending: true }]
  );

  async function formAction(formData) {
    const title = formData.get('title') as string;
    addOptimistic({ id: crypto.randomUUID(), title }); // instant UI update
    await addTodoAction(formData);                      // actual server call
  }

  return (
    <>
      {optimisticTodos.map(t => (
        <li key={t.id} style={{ opacity: t.pending ? 0.5 : 1 }}>{t.title}</li>
      ))}
      <form action={formAction}>
        <input name="title" />
        <SubmitButton />
      </form>
    </>
  );
}
```

See `references/detailed-patterns.md` for full form examples with Zod validation, error handling, and redirect patterns.

## Data Fetching

### Server Components (Default)

Use `async/await` directly — no `useEffect` or `useState` needed. Keeps secrets on the server, reduces client bundle.

### Parallel vs Sequential

Avoid unintentional **request waterfalls** where requests block each other. Use `Promise.all()` for independent requests:

```tsx
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts()
]);
```

### Streaming with Suspense

Prevent slow queries from blocking the entire page:

- `loading.tsx` — streams entire route segment with a fallback
- `<Suspense fallback={<Skeleton />}>` — granular streaming per component

### Client Fetching

When client-side fetching is necessary:
- Route Handlers for API endpoints
- SWR or React Query for caching, revalidation, and streaming
- React `use` API to resolve server-passed promises in `<Suspense>`

## Server/Client Component Boundary

### When to Use Server Components (Default)

- Fetch data close to the database
- Keep large dependencies off the client bundle
- Protect API keys and secrets
- Improve First Contentful Paint

### When to Use Client Components (`"use client"`)

- Interactivity: `onClick`, `onChange`, event handlers
- React state: `useState`, `useReducer`
- Lifecycle: `useEffect`
- Browser APIs: `localStorage`, `window`, `IntersectionObserver`

### Boundary Rules

- `"use client"` makes the file AND all its imports part of the client bundle
- Push `"use client"` as deep in the tree as possible to minimize bundle
- Nest Server Components inside Client Components via children props (slot pattern)
- Context providers must be Client Components — render as deep as possible
- Third-party packages without `"use client"` need a wrapper Client Component
- Use `server-only` package to prevent server code from leaking to client

## Additional Resources

### Reference Files

- **`references/detailed-patterns.md`** — Complete code examples for routing, form actions with Zod validation, streaming patterns, and server/client composition
