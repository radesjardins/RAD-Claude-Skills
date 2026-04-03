# Next.js Performance Optimization Checklist

Complete Core Web Vitals optimization reference with specific techniques and metrics.

---

## Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | 2.5s – 4.0s | > 4.0s |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | 0.1 – 0.25 | > 0.25 |
| **INP** (Interaction to Next Paint) | ≤ 200ms | 200ms – 500ms | > 500ms |

---

## LCP Optimization

### Image LCP (Most Common)

```tsx
// CORRECT: Hero image with priority
import Image from 'next/image';

export function Hero() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero banner"
      width={1200}
      height={600}
      priority              // Adds fetchpriority="high", disables lazy loading
      quality={75}          // Reduce file size with negligible visual difference
    />
  );
}
```

**Checklist:**
- [ ] LCP image uses `next/image` with `priority` prop
- [ ] LCP image does NOT have `loading="lazy"`
- [ ] Image is served in modern format (WebP/AVIF — automatic with next/image)
- [ ] Image is appropriately sized (not 4000px wide for a 800px container)
- [ ] `quality` reduced to 75 for large hero images
- [ ] No redirect chains before the LCP resource loads

### Text LCP

- [ ] Fonts loaded with `next/font` (eliminates external requests)
- [ ] Font uses `display: swap` or `display: optional`
- [ ] Critical CSS is inlined (automatic with Next.js)

### Server Response Time (TTFB)

- [ ] Database queries parallelized with `Promise.all()`
- [ ] Edge/CDN caching configured for static content
- [ ] Consider Partial Prerendering (PPR) for mixed static/dynamic pages

---

## CLS Optimization

### Images and Media

- [ ] All `<img>` tags have explicit `width` and `height` (enforced by `next/image`)
- [ ] Video/iframe elements have `aspect-ratio` CSS or explicit dimensions
- [ ] Placeholder images or blur-up used during loading

### Fonts

- [ ] Using `next/font` with `size-adjust` (automatic)
- [ ] No Flash of Unstyled Text (FOUT) causing layout shifts
- [ ] Fallback font metrics match web font metrics

### Dynamic Content

- [ ] Content injected after load has reserved space (min-height, aspect-ratio)
- [ ] Ads/banners have fixed dimensions
- [ ] No elements inserted above existing content after initial render

### Animations

```css
/* BAD: Triggers layout recalculation */
.animate-bad {
  transition: top 0.3s, margin-left 0.3s;
}

/* GOOD: Composited on GPU, no layout impact */
.animate-good {
  transition: transform 0.3s, opacity 0.3s;
}
```

- [ ] Animations use `transform` and `opacity` only
- [ ] No animations on `top`, `left`, `right`, `bottom`, `margin`, `padding`, `width`, `height`
- [ ] `will-change` used sparingly for known animation targets

---

## INP Optimization

### Long Task Prevention

```typescript
// Break up heavy computations
async function processLargeDataset(items: Item[]) {
  for (let i = 0; i < items.length; i++) {
    processItem(items[i]);

    // Yield to main thread every 50 items
    if (i % 50 === 0) {
      await scheduler.yield();  // Modern API
      // Fallback: await new Promise(resolve => setTimeout(resolve, 0));
    }
  }
}
```

- [ ] No single JavaScript task exceeds 50ms on the main thread
- [ ] Heavy computations use `scheduler.yield()` to yield to main thread
- [ ] Event handlers are lightweight — offload heavy work to Web Workers or Server Actions
- [ ] Third-party scripts don't block interaction

### Minimize Client-Side JavaScript

- [ ] Non-interactive UI uses Server Components (zero JS)
- [ ] `'use client'` only on leaf components that need state/effects/browser APIs
- [ ] Heavy libraries lazy-loaded with `next/dynamic`
- [ ] Tree-shaking working (no barrel file imports pulling entire libraries)

---

## Asset Optimization Checklist

### Images

- [ ] All images use `next/image` component
- [ ] Above-the-fold images have `priority` prop
- [ ] Below-the-fold images use default lazy loading
- [ ] `quality` set to 75 for large images (default is 75, verify not overridden to 100)
- [ ] `sizes` prop configured when image doesn't fill viewport width
- [ ] External image domains configured in `next.config.ts` `images.remotePatterns`
- [ ] No images served from `public/` without processing (use `next/image`)

### Fonts

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',         // Prevents FOUT-related CLS
  variable: '--font-inter', // CSS variable for Tailwind
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
```

- [ ] All fonts loaded via `next/font` (Google or local)
- [ ] No external font CDN requests (`<link href="fonts.googleapis.com">`)
- [ ] Font subsets specified (e.g., `latin`) to reduce download size
- [ ] CSS variable used for Tailwind integration

### Third-Party Scripts

```tsx
import Script from 'next/script';

// Analytics — load after page is interactive
<Script src="https://analytics.example.com/script.js" strategy="afterInteractive" />

// Chat widget — load when browser is idle
<Script src="https://chat.example.com/widget.js" strategy="lazyOnload" />
```

- [ ] All third-party scripts use `next/script`
- [ ] Analytics scripts use `strategy="afterInteractive"`
- [ ] Non-critical scripts (chat, ads) use `strategy="lazyOnload"`
- [ ] No `<script>` tags in `<head>` blocking render

### Code Splitting

```tsx
import dynamic from 'next/dynamic';

// Lazy-load a heavy modal
const HeavyModal = dynamic(() => import('./HeavyModal'), {
  loading: () => <ModalSkeleton />,
  ssr: false,  // Skip server rendering for client-only components
});

// Lazy-load a chart library
const Chart = dynamic(() => import('./Chart'), {
  loading: () => <ChartSkeleton />,
});
```

- [ ] Below-the-fold interactive components use `next/dynamic`
- [ ] Modals and dialogs are dynamically imported
- [ ] Heavy charting/visualization libraries are code-split
- [ ] `@next/bundle-analyzer` used to identify bloated chunks

---

## Build Output Analysis

After `next build`, review the output:

```
Route (app)                    Size     First Load JS
┌ ○ /                          5.2 kB   89 kB
├ ○ /about                     1.8 kB   85 kB
├ λ /api/products              0 B      0 B
├ ● /products/[id]             3.1 kB   87 kB
└ ○ /contact                   2.4 kB   86 kB

○  Static   ●  SSG   λ  Dynamic
First Load JS shared by all: 83.5 kB
```

**Red flags:**
- First Load JS > 100 kB for any route → investigate with bundle analyzer
- Many `λ` (dynamic) routes that could be static → add caching or ISR
- Shared bundle > 100 kB → check for unnecessary global imports

---

## Partial Prerendering (PPR)

For pages mixing static and dynamic content:

```tsx
// app/product/[id]/page.tsx
import { Suspense } from 'react';
import { ProductInfo } from './ProductInfo';       // Static — cached
import { PersonalizedRecs } from './PersonalizedRecs'; // Dynamic — user-specific

export default function ProductPage({ params }: { params: { id: string } }) {
  return (
    <main>
      {/* Static shell served instantly from edge */}
      <ProductInfo id={params.id} />

      {/* Dynamic hole — streams in when ready */}
      <Suspense fallback={<RecsSkeleton />}>
        <PersonalizedRecs userId={getCurrentUserId()} />
      </Suspense>
    </main>
  );
}
```

**Enable PPR** in `next.config.ts`:
```typescript
const nextConfig = {
  experimental: {
    ppr: true,
  },
};
```

---

## Monitoring in Production

### Real User Monitoring (RUM)

Track actual user Core Web Vitals with:
- **Vercel Analytics** (built-in with Vercel deployment)
- **Google Chrome UX Report (CrUX)** via PageSpeed Insights
- **Custom reporting** via `web-vitals` library:

```tsx
// app/layout.tsx or a Client Component
'use client';
import { useReportWebVitals } from 'next/web-vitals';

export function WebVitalsReporter() {
  useReportWebVitals((metric) => {
    // Send to your analytics endpoint
    fetch('/api/vitals', {
      method: 'POST',
      body: JSON.stringify(metric),
    });
  });
  return null;
}
```

### instrumentation.ts

Initialize monitoring at server startup:

```typescript
// instrumentation.ts
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    // Initialize server-side monitoring
    const { init } = await import('@sentry/nextjs');
    init({ dsn: process.env.SENTRY_DSN });
  }
}
```
