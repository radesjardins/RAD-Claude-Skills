# React App Building — Detailed Patterns

## Server Actions with Form Validation

```tsx
// app/actions.ts
'use server'

import { z } from 'zod';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

const CreatePostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(10),
  categoryId: z.string().uuid(),
});

export async function createPost(formData: FormData) {
  const parsed = CreatePostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
    categoryId: formData.get('categoryId'),
  });

  if (!parsed.success) {
    return { errors: parsed.error.flatten().fieldErrors };
  }

  await db.post.create({ data: parsed.data });
  revalidatePath('/posts');
  redirect('/posts');
}
```

```tsx
// app/posts/new/page.tsx
import { createPost } from '@/app/actions';

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <label htmlFor="title">Title</label>
      <input id="title" name="title" required />

      <label htmlFor="content">Content</label>
      <textarea id="content" name="content" required />

      <button type="submit">Create Post</button>
    </form>
  );
}
```

## Binding IDs to Server Actions

```tsx
// Pass ID securely without hidden inputs
import { updatePost } from '@/app/actions';

export default function EditButton({ postId }: { postId: string }) {
  const updateWithId = updatePost.bind(null, postId);
  return (
    <form action={updateWithId}>
      <input name="title" />
      <button type="submit">Update</button>
    </form>
  );
}
```

## Parallel Data Fetching

```tsx
// BAD: Sequential waterfall
async function Dashboard() {
  const user = await fetchUser();       // 200ms
  const posts = await fetchPosts();     // 300ms → total: 500ms
  const stats = await fetchStats();     // 150ms → total: 650ms
}

// GOOD: Parallel fetching
async function Dashboard() {
  const [user, posts, stats] = await Promise.all([
    fetchUser(),    // 200ms
    fetchPosts(),   // 300ms
    fetchStats(),   // 150ms
  ]);              // total: 300ms (slowest wins)
}
```

## Streaming with Suspense

```tsx
// Route-level streaming with loading.tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <DashboardSkeleton />;
}

// Granular streaming with Suspense
import { Suspense } from 'react';

async function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      {/* Instant — static content */}
      <WelcomeBanner />

      {/* Streams when ready */}
      <Suspense fallback={<ChartSkeleton />}>
        <SlowChart />
      </Suspense>

      <Suspense fallback={<TableSkeleton />}>
        <DataTable />
      </Suspense>
    </div>
  );
}
```

## Server/Client Composition

```tsx
// Push "use client" deep — only the interactive part
// components/SearchBar.tsx
'use client';
export function SearchBar() {
  const [query, setQuery] = useState('');
  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}

// page.tsx (Server Component)
import { SearchBar } from './components/SearchBar';

export default async function Page() {
  const data = await fetchData(); // Server-only
  return (
    <main>
      <SearchBar />           {/* Client island */}
      <DataDisplay data={data} /> {/* Server Component */}
    </main>
  );
}
```

## Slot Pattern: Server Components Inside Client Components

```tsx
// ClientModal.tsx
'use client';
export function ClientModal({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button onClick={() => setOpen(true)}>Open</button>
      {open && <dialog open>{children}</dialog>}
    </>
  );
}

// page.tsx (Server Component)
import { ClientModal } from './ClientModal';
import { ServerContent } from './ServerContent'; // async server component

export default function Page() {
  return (
    <ClientModal>
      <ServerContent />  {/* Stays on server, passed as children */}
    </ClientModal>
  );
}
```

## Context Provider Wrapper Pattern

```tsx
// providers/ThemeProvider.tsx
'use client';
import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext<'light' | 'dark'>('light');

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
```

```tsx
// app/layout.tsx (Server Component)
import { ThemeProvider } from './providers/ThemeProvider';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <ThemeProvider>  {/* Client boundary as deep as possible */}
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
```

## Preventing Server Code Leaks

```tsx
// lib/db.ts
import 'server-only'; // Build-time error if imported in Client Component

import { PrismaClient } from '@prisma/client';
export const db = new PrismaClient();
```
