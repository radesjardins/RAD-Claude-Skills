---
name: astro-performance
description: >
  This skill should be used when optimizing Astro performance, improving Core Web Vitals in Astro, fixing LCP/CLS/INP issues, auditing client directives, reducing JavaScript bundle size, configuring Astro prefetching, using server:defer for performance, optimizing Astro images, configuring Astro fonts, CSS optimization in Astro, HTML streaming, Astro build optimization, Astro CDN configuration, Route Caching API, Lighthouse audit for Astro, hydration performance, client:visible vs client:load, or Astro asset pipeline.
---

# Astro Performance Optimization

## Core Mental Model: HTML First, JavaScript Only When Necessary

Astro ships ZERO JavaScript by default. This is the primary performance advantage of the framework. Treat every `client:*` directive as a conscious decision to add JavaScript payload to the page. Your goal is to maintain the zero-JS baseline and add interactivity only where it is surgically necessary.

Target these Core Web Vitals thresholds on every page:
- **LCP** (Largest Contentful Paint): under 2.5 seconds
- **CLS** (Cumulative Layout Shift): under 0.1
- **INP** (Interaction to Next Paint): under 200 milliseconds

When reviewing or building Astro pages, start from the assumption that zero client-side JavaScript is correct, then justify each addition.

## The Hydration Storm Anti-Pattern (CRITICAL)

A "hydration storm" occurs when multiple `client:load` directives cause the browser to download, parse, and execute multiple framework runtimes simultaneously on page load. This is the single most common performance mistake in Astro projects. Watch for these patterns and flag them immediately:

- NEVER use `client:load` on multiple components without explicit justification for each one. Every `client:load` fires on page load and competes for the main thread.
- NEVER wrap entire page layouts or large sections in a single framework component (React, Vue, Svelte) with `client:load`. This hydrates EVERYTHING inside that component, defeating Astro's island architecture entirely.
- NEVER use `.map()` to spawn dozens of `client:*` islands in a loop. If you have a list of items that each get a `client:visible` or `client:load` directive, you are creating N separate island instances. Instead, render list items as static HTML and hydrate a single controller or filter component that manages the entire list.

When you find hydration storms, apply these fixes:

1. Audit every `client:*` directive in the project. For each one, ask: does this component need interactivity on page load, or can it wait?
2. Replace `client:load` with `client:visible` for components below the fold. Replace with `client:idle` for components that need interactivity but not immediately.
3. Break large interactive sections into small, granular islands. Extract the interactive parts (buttons, forms, toggles) into their own island components, and leave surrounding content as static Astro markup.

## Server Islands vs Client Islands Decision Framework

Use this decision framework every time you create or review an interactive component:

**Use Client Islands when** the component needs browser APIs (`window`, `document`, `navigator`), event handlers (`onClick`, `onSubmit`), or client-side state (`useState`, reactive stores, local component state that changes based on user input).

**Use Server Islands (`server:defer`) when** the component renders dynamic data that does not need click handlers. Examples: user avatars, personalized greetings, stock levels, cart item counts, "last updated" timestamps, recommended products, and any content that varies per request but is read-only on the client.

Server Islands stream completed HTML to the browser without any JavaScript payload. This is a massive performance advantage. The static HTML shell of the page can be CDN-cached while the dynamic Server Island parts render per-request on the server and stream in.

Always provide a `slot="fallback"` with a loading skeleton for Server Islands so the user sees a placeholder while the dynamic content loads:

```astro
<ServerIsland server:defer>
  <div slot="fallback" class="skeleton animate-pulse h-8 w-24"></div>
</ServerIsland>
```

Apply this rule: if the component does not need `addEventListener`, try `server:defer` first.

## HTML Streaming

Astro streams static HTML to the browser as it generates it. This means the browser can start painting the page layout before all data has loaded. Streaming is critical for LCP because the largest content element often appears in the static shell.

NEVER use top-level `await` in page frontmatter. A top-level `await` blocks the entire page from streaming because Astro must resolve the promise before it can emit any HTML.

```astro
---
// BAD: blocks streaming of the entire page
const data = await fetch('https://api.example.com/slow-endpoint').then(r => r.json());
---
```

Fix this by extracting async data fetching into child components. Astro streams the static shell immediately while the async child components resolve independently:

```astro
---
// GOOD: page streams immediately, DataSection fetches its own data
import DataSection from '../components/DataSection.astro';
---
<html>
  <body>
    <h1>Page Title</h1>  <!-- Streams immediately -->
    <DataSection />       <!-- Fetches data independently -->
  </body>
</html>
```

This pattern ensures the browser paints the layout before all data loads, dramatically improving LCP.

## Image Optimization

ALWAYS use `<Image />` from `astro:assets` for local images. Never use raw `<img>` tags for images stored in the project.

```astro
---
import { Image } from 'astro:assets';
import heroImage from '../assets/hero.webp';
---
<Image src={heroImage} alt="Hero banner" />
```

`<Image />` automatically infers width and height from the source file, preventing CLS. It also generates optimized formats and sizes.

Store all optimizable images in `src/assets/` so Astro processes them at build time. NEVER put images that should be optimized in `public/`. Files in `public/` bypass the entire optimization pipeline and are served as-is.

For responsive images, use `layout="responsive"` to generate `srcset` and `sizes` attributes for device-specific loading.

For hero images or any image likely to be the LCP element, add explicit loading and priority attributes:

```astro
<Image src={heroImage} alt="Hero" loading="eager" fetchpriority="high" />
```

For below-fold images, `loading="lazy"` is the default behavior and does not need to be specified.

For remote images, authorize the domains in `astro.config`:

```javascript
image: {
  domains: ['cdn.example.com'],
  // or use remotePatterns for more granular control
  remotePatterns: [{ protocol: 'https', hostname: '**.example.com' }]
}
```

## Astro 6 Fonts API

Use the built-in Fonts API for zero-CLS font loading. The Fonts API automatically handles `font-display: swap`, eliminates render-blocking font requests, and self-hosts fonts for both performance and privacy. This avoids both flash of unstyled text (FOUT) and flash of invisible text (FOIT).

The Fonts API replaces manual `@font-face` declarations and Google Fonts `<link>` tags. If you encounter a project using Google Fonts links in the `<head>`, migrate them to the Fonts API to eliminate the render-blocking external request.

## CSS Optimization

Astro scopes `<style>` blocks to their parent component automatically, preventing global CSS pollution. Leverage this by co-locating styles with components rather than maintaining large global stylesheets.

Configure critical CSS extraction in `astro.config`:

```javascript
build: {
  inlineStylesheets: 'auto'
}
```

The `'auto'` setting inlines small stylesheets directly into the HTML (eliminating a render-blocking request) and links larger stylesheets as external files. This is the optimal setting for first paint performance. Astro minifies all CSS in production builds automatically.

When working with Tailwind 4, be aware that specificity changes in the migration may require `!important` adjustments. Test thoroughly after upgrading.

Avoid importing large CSS libraries globally. Import them per-component where possible to keep each page's CSS payload minimal.

## Prefetching

Astro prefetches linked pages for near-instant navigation between routes. Configure prefetching in `astro.config`:

```javascript
prefetch: {
  defaultStrategy: 'viewport',  // prefetch links when they become visible
  prefetchAll: false             // don't prefetch everything indiscriminately
}
```

Available strategies:
- `'hover'` (default when using `<ClientRouter />`): prefetches when the user hovers over a link
- `'viewport'`: prefetches when the link scrolls into the viewport
- `'load'`: prefetches all links on page load
- `'tap'`: prefetches on mousedown/touchstart (minimal prefetching)

Use `data-astro-prefetch="false"` on links that should not be prefetched: external links, large file downloads, or links to pages with expensive server-side rendering.

When using `<ClientRouter />` for SPA-like transitions, hover prefetching is enabled automatically.

## Asset Pipeline and Build Optimization

Vite handles code splitting, tree shaking, and minification automatically during `astro build`. You do not need to configure these manually.

For CDN configuration, use `build.assetsPrefix` to serve hashed static assets from a CDN while keeping HTML on the origin server:

```javascript
build: {
  assetsPrefix: 'https://cdn.example.com'
}
```

All hashed static assets (JS, CSS, images processed by the pipeline) will reference the CDN URL, while HTML documents are served from the origin.

## Route Caching API (Experimental, Astro 6)

The Route Caching API allows you to cache entire route responses at the edge. Configure cache control headers per-route to dramatically reduce server load for semi-dynamic pages.

Combine Route Caching with Server Islands for the optimal pattern: cache the static HTML shell at the CDN edge, and stream dynamic Server Island parts per-request. This gives you CDN-speed page loads with personalized dynamic content.

## The SSR Golden Hammer Anti-Pattern

Do NOT default every page to server-side rendering. SSR is the most expensive rendering mode: every request requires server compute, cannot be cached at the CDN edge (without Route Caching), and adds latency.

Static pages served from a CDN are the fastest, cheapest, and most reliable option. Use a hybrid rendering approach:
- **Static by default**: prerender pages at build time whenever possible
- **SSR only for truly dynamic routes**: authentication-gated pages, real-time data dashboards, pages that vary per user

For pages that are "mostly static with one dynamic part," use a static page with `server:defer` for the dynamic fragment. This keeps the page on the CDN while streaming the personalized content.

## Performance Monitoring

Run Lighthouse audits in CI against the production build (`astro build` followed by `astro preview`), never against the dev server. The dev server does NOT reflect production performance: it skips minification, code splitting, and asset optimization.

Monitor Core Web Vitals targets continuously:
- LCP under 2.5 seconds
- CLS under 0.1
- INP under 200 milliseconds

Use the Astro Dev Toolbar Audit app during local development for quick performance checks, but always validate against the production build before shipping.

Set up Real User Monitoring (RUM) for production using the `web-vitals` library or your analytics platform. Lab data (Lighthouse) shows potential; field data (RUM) shows actual user experience.

## Performance Checklist

Before shipping any Astro page or completing a performance audit, verify every item:

1. Zero unnecessary `client:load` directives. Each one has explicit justification.
2. Islands are granular. No framework components wrapping entire layouts.
3. No hydration storms from `.map()` loops spawning dozens of islands.
4. Server Islands used for dynamic-but-non-interactive content.
5. No top-level `await` in page frontmatter blocking HTML streaming.
6. All local images use `<Image />` from `astro:assets` and live in `src/assets/`.
7. LCP image has `loading="eager"` and `fetchpriority="high"`.
8. Fonts loaded via Astro 6 Fonts API or properly self-hosted.
9. `build.inlineStylesheets: 'auto'` configured in `astro.config`.
10. Prefetching configured with an appropriate strategy.
11. Static rendering used where possible. SSR only when genuinely needed.
12. Lighthouse audit run against the production build, not the dev server.
