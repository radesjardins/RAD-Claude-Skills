# Server & Client Component Patterns

Detailed patterns and code examples for Next.js App Router component architecture.

---

## Server Component Patterns

### Direct Data Fetching

Server Components support `async/await` natively — no `useEffect` or client-side libraries needed:

```tsx
// app/products/[id]/page.tsx (Server Component)
import { getProduct, getReviews } from '@/lib/dal';

export default async function ProductPage({ params }: { params: { id: string } }) {
  // Parallel fetching — both queries start simultaneously
  const [product, reviews] = await Promise.all([
    getProduct(params.id),
    getReviews(params.id),
  ]);

  return (
    <main>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <ReviewList reviews={reviews} />
    </main>
  );
}
```

### Data Access Layer (DAL) Pattern

Centralize all data access in a server-only module:

```typescript
// lib/dal.ts
import 'server-only';
import { cache } from 'react';
import { verifyAuth } from './auth';
import { db } from './db';

// Wrap with React.cache for request deduplication
export const getUser = cache(async (userId: string) => {
  const session = await verifyAuth();
  if (!session) throw new Error('Unauthorized');

  const user = await db.user.findUnique({ where: { id: userId } });
  if (!user) return null;

  // Return a DTO, never the raw database record
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    // Exclude: passwordHash, internalFlags, etc.
  };
});

export const getProducts = cache(async () => {
  // No auth required for public data
  return db.product.findMany({
    select: { id: true, name: true, price: true, imageUrl: true },
    orderBy: { createdAt: 'desc' },
  });
});
```

### Streaming with Suspense

Wrap slow data-fetching components in Suspense for progressive loading:

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';
import { DashboardStats } from './DashboardStats';
import { RecentOrders } from './RecentOrders';
import { Skeleton } from '@/components/ui/skeleton';

export default function DashboardPage() {
  return (
    <main>
      <h1>Dashboard</h1>
      {/* Fast — renders immediately */}
      <Suspense fallback={<Skeleton className="h-32" />}>
        <DashboardStats />
      </Suspense>
      {/* Slow — streams in when ready */}
      <Suspense fallback={<Skeleton className="h-64" />}>
        <RecentOrders />
      </Suspense>
    </main>
  );
}
```

---

## Client Component Patterns

### Minimal Client Boundary

Push `'use client'` to the deepest leaf:

```tsx
// components/ui/LikeButton.tsx
'use client';
import { useState } from 'react';

export function LikeButton({ productId }: { productId: string }) {
  const [liked, setLiked] = useState(false);

  return (
    <button onClick={() => setLiked(!liked)}>
      {liked ? '❤️' : '🤍'}
    </button>
  );
}
```

```tsx
// app/products/[id]/page.tsx (Server Component)
import { getProduct } from '@/lib/dal';
import { LikeButton } from '@/components/ui/LikeButton';

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);
  return (
    <main>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <LikeButton productId={product.id} />  {/* Only this ships JS */}
    </main>
  );
}
```

---

## The Composition Pattern

### Problem: Server Component Inside Client Component

A Client Component cannot `import` a Server Component — doing so would force the server code into the client bundle.

### Solution: Pass as Children Props

```tsx
// components/ui/Sidebar.tsx (Client Component)
'use client';
import { useState, type ReactNode } from 'react';

export function Sidebar({ children }: { children: ReactNode }) {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <aside className={isOpen ? 'w-64' : 'w-0'}>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {isOpen && children}
    </aside>
  );
}
```

```tsx
// app/dashboard/layout.tsx (Server Component)
import { Sidebar } from '@/components/ui/Sidebar';
import { NavigationLinks } from '@/components/server/NavigationLinks';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex">
      <Sidebar>
        <NavigationLinks />  {/* Server Component passed as children */}
      </Sidebar>
      <main>{children}</main>
    </div>
  );
}
```

**How it works:** React resolves `NavigationLinks` on the server first, then passes the serialized RSC Payload into the `Sidebar` Client Component as a prop.

---

## Serialization Rules

### Safe to Pass (Server → Client)

| Type | Example |
|------|---------|
| Strings | `"hello"` |
| Numbers | `42`, `3.14` |
| Booleans | `true`, `false` |
| `null` | `null` |
| Plain objects | `{ name: "John", age: 30 }` |
| Arrays | `[1, 2, 3]` |
| JSX (ReactNode) | `<ServerComponent />` (via children) |

### Not Serializable (Will Error or Silently Strip)

| Type | Fix |
|------|-----|
| `Date` | Pass `.toISOString()`, reconstruct on client |
| `Map` / `Set` | Convert to array/object |
| Functions | Move to Client Component |
| Class instances | Extract plain data |
| `Symbol` | Use string keys |
| Circular references | Flatten the structure |

---

## Server Action Patterns

### Form Submission

```tsx
// app/contact/page.tsx
import { submitContact } from './actions';

export default function ContactPage() {
  return (
    <form action={submitContact}>
      <input name="email" type="email" required />
      <textarea name="message" required />
      <button type="submit">Send</button>
    </form>
  );
}
```

```typescript
// app/contact/actions.ts
'use server';
import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const contactSchema = z.object({
  email: z.string().email(),
  message: z.string().min(10).max(1000),
});

export async function submitContact(formData: FormData) {
  const parsed = contactSchema.safeParse({
    email: formData.get('email'),
    message: formData.get('message'),
  });

  if (!parsed.success) {
    return { error: 'Invalid input' };
  }

  await db.contact.create({ data: parsed.data });
  revalidatePath('/contact');
  return { success: true };
}
```

### Streaming Promise to Client Component

```tsx
// app/dashboard/page.tsx (Server Component)
import { getAnalytics } from '@/lib/dal';
import { AnalyticsChart } from './AnalyticsChart';

export default function DashboardPage() {
  // Do NOT await — pass the promise directly
  const analyticsPromise = getAnalytics();
  return <AnalyticsChart dataPromise={analyticsPromise} />;
}
```

```tsx
// app/dashboard/AnalyticsChart.tsx (Client Component)
'use client';
import { use, Suspense } from 'react';

function ChartInner({ dataPromise }: { dataPromise: Promise<AnalyticsData> }) {
  const data = use(dataPromise);  // Unwrap the promise
  return <Chart data={data} />;
}

export function AnalyticsChart({ dataPromise }: { dataPromise: Promise<AnalyticsData> }) {
  return (
    <Suspense fallback={<ChartSkeleton />}>
      <ChartInner dataPromise={dataPromise} />
    </Suspense>
  );
}
```

---

## Client-Side Fetching (When Needed)

For highly interactive, frequently updating data (dashboards, live feeds), use client-side fetching libraries:

```tsx
'use client';
import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then(res => res.json());

export function LiveDashboard() {
  const { data, error, isLoading } = useSWR('/api/metrics', fetcher, {
    refreshInterval: 5000,  // Poll every 5 seconds
  });

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorDisplay error={error} />;
  return <MetricsGrid data={data} />;
}
```

Use SWR or React Query only when data must update on the client without page navigation. For initial page data, always prefer Server Components.
