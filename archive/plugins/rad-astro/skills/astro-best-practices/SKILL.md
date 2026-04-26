---
name: astro-best-practices
description: >
  This skill should be used when working on any Astro project or when the user asks about
  Astro best practices, conventions, or patterns. Trigger when: working on an Astro project,
  creating Astro components/pages/layouts, configuring astro.config, setting up Content
  Collections, using Content Layer API, choosing client directives (client:load/idle/visible/media/only),
  using server:defer or server islands, deciding between SSR and SSG, working with Astro Actions
  for forms, configuring middleware, using Zod schemas for content, building with TypeScript in
  Astro, creating API endpoints, using @astro/autoload, working with .astro files, Astro 5 or
  Astro 6 development.
---

# Astro: Core Architecture & Best Practices

## Core Philosophy

Astro is content-first and ships ZERO JavaScript by default. Internalize this before writing any code. Assume every component renders as plain HTML unless interactivity is strictly necessary — only opt in to JavaScript through explicit client directives when state or event handling is required. Astro uses a Multi-Page Application (MPA) mindset, not a Single-Page Application (SPA) mindset. Do not attempt to replicate SPA patterns like global client-side state stores or full-page client-side routing unless explicitly asked.

Understand the strict separation of environments: build-time (Content Layer fetches and transforms data), server-time (SSR endpoints, Server Islands, middleware), and browser-time (Client Islands, `<script>` tags). Never mix these boundaries. Data flows downward: build-time or server-time code produces HTML and passes serializable props to client components. The browser never calls `getCollection()` or accesses `Astro.locals`.

## Component Model

Every `.astro` file has two regions: the frontmatter fence (`---`) and the template below it. The frontmatter is SERVER-ONLY code that runs at build time or request time. Use it to import components, fetch data, define variables, and destructure props. Never access `window`, `document`, `localStorage`, or any browser API in frontmatter — doing so causes `document is not defined` or `window is not defined` errors.

Client-side JavaScript belongs in `<script>` tags in the template section, not in frontmatter. Astro processes `<script>` tags and bundles them automatically. Use `<script>` for DOM manipulation, event listeners, and browser API access.

For props, always destructure `Astro.props` with sensible defaults so components work without every prop being passed. Collect remaining attributes with `...attrs` and spread them on the root element to allow consumers to pass `id`, `aria-*`, `data-*`, and `class` attributes freely. Use `class:list` for dynamic class composition — it accepts strings, arrays, objects, and variables. Import `HTMLAttributes` from `astro/types` and extend your `Props` interface for full editor autocompletion:

```astro
---
import type { HTMLAttributes } from 'astro/types';
interface Props extends HTMLAttributes<'section'> {
  title: string;
  size?: 'sm' | 'md' | 'lg';
}
const { title, size = 'md', class: className, ...attrs } = Astro.props;
---
<section class:list={['card', size, className]} {...attrs}>
  <h2>{title}</h2>
  <slot />
</section>
```

Use named slots (`slot="name"`) for multi-region layouts and `<slot />` for default content injection. Prefer composition over inheritance — layouts wrap content via slots, not by extending base classes. For dynamic HTML tags, accept an `as` prop and capitalize it before rendering: `const As = as;` then `<As>`.

## Islands Architecture & Client Directives

The fundamental rule: no directive means no JavaScript. An Astro component or framework component rendered without a `client:*` directive outputs static HTML with zero JS. This is the default and the desired state for most of your page.

When interactivity is required, choose the correct directive:

- **`client:load`** — Hydrates immediately on page load. Use ONLY for above-the-fold critical interactive UI: navigation menus, hero carousels, "Add to Cart" buttons. Never use this as a default.
- **`client:idle`** — Hydrates when the browser main thread is free. Use for secondary interactive UI: newsletter signup forms, non-urgent widgets, chat popups.
- **`client:visible`** — Hydrates when the component scrolls into the viewport. Use for below-the-fold content: charts, image carousels, infinite scroll loaders, comment sections.
- **`client:media`** — Hydrates when a CSS media query matches. Use for responsive-only UI: mobile hamburger menus that should not load JS on desktop.
- **`client:only="framework"`** — Renders entirely on the client with no SSR pass. Use only when the component depends on browser APIs that cannot run server-side, or for third-party embeds that require a DOM to initialize.

Audit every `client:*` directive in code review. If you see `client:load` on something below the fold, change it to `client:visible`. If you see it on a non-critical widget, change it to `client:idle`.

Keep islands granular. Do NOT wrap entire page layouts or large sections in a framework component. Hydrate small, specific widgets (a search bar, a cart button, a form) while leaving surrounding content as static Astro HTML. Do NOT use `map()` over arrays to spawn dozens of individual `client:*` islands — render list items statically and hydrate a single controller component that manages the interactive behavior.

For **Server Islands** (`server:defer`), use them when data is dynamic but the UI does not need client-side interactivity. User avatars, stock levels, cart summaries, and personalized greetings are ideal candidates. Server Islands stream completed HTML independently after the static shell loads, adding zero JavaScript payload. Always provide a `slot="fallback"` for the loading state:

```astro
<CartSummary server:defer>
  <LoadingSkeleton slot="fallback" />
</CartSummary>
```

## Project Structure

Follow this layout. Only `src/pages/` is strictly required by Astro; the rest are strong conventions you must follow:

```
src/
  pages/              # REQUIRED — file-based routing
  components/         # Reusable .astro, .tsx, .vue, .svelte components
  layouts/            # Page layout wrappers (shared head, nav, footer)
  content/            # RESERVED — Content Collections source files only
  content.config.ts   # Collection definitions — at src/ root, NOT inside content/
  live.config.ts      # Live Content Collections config (Astro 6)
  actions/
    index.ts          # Astro Actions definitions
  middleware.ts       # Request interceptor for cross-cutting concerns
  assets/             # Images for optimization (NOT public/)
public/               # Static assets copied verbatim (robots.txt, favicons, fonts)
```

Place `content.config.ts` at `src/content.config.ts`, never inside `src/content/`. The `src/content/` directory is reserved exclusively for Content Collection source files. Store optimizable images in `src/assets/` so the `<Image />` component can process them — never put images you want optimized in `public/`. Dynamic routes use `[param].astro` syntax; catch-all routes use `[...param].astro`.

## Content Layer API (Astro 5+)

The Content Layer is an ETL pipeline: loaders fetch raw data, Zod schemas validate and transform it, and the result is a type-safe data store you query at build time. You MUST use explicit loaders — `glob()` for local Markdown/MDX files, `file()` for single-file JSON/YAML arrays, and custom loader functions for remote APIs. Do not rely on implicit behavior.

Critical Astro 5+ changes: the `slug` property has been removed and replaced by a mandatory `id` primary key. The `entry.render()` method is gone — import the `render()` utility from `astro:content` and pass the entry to it:

```ts
import { getEntry, render } from 'astro:content';
const entry = await getEntry('blog', 'my-post');
const { Content } = await render(entry);
```

In your schema definitions, always use `z.coerce.date()` instead of `z.date()` because frontmatter dates arrive as strings. Use `.optional()` and `.default()` liberally to prevent validation errors as content grows. Use `reference()` to link collections (author references, related posts) rather than nesting objects. Use the `image()` helper for local image validation in schemas.

Never use `astro:content` APIs on the client. Always query collections in server-side code (frontmatter, endpoints, middleware) and pass the data as serializable props to client components.

**Live Content Collections (Astro 6):** Define `src/live.config.ts` for data that must be fetched at request time rather than build time — stock prices, live inventory, real-time feeds. This replaces the pattern of making every page SSR just for one dynamic data source.

## Rendering Modes

Static (SSG) is the default and the best choice for most content: blogs, docs, marketing pages, product catalogs. It offers the best performance, security, and hosting cost.

In Astro 5+, `output: 'hybrid'` is DEPRECATED and merged into `output: 'static'`. To opt individual pages into server rendering within a static site, add `export const prerender = false` to that page's frontmatter. This is the replacement for hybrid mode.

In `output: 'server'` mode, all pages render on the server by default. Opt specific pages into static generation with `export const prerender = true`. The `prerender` flag MUST be a static `true` or `false` boolean literal — you cannot use `import.meta.env` or any dynamic expression.

Any SSR requires an adapter. Install the adapter matching your deployment target: `@astrojs/node`, `@astrojs/vercel`, `@astrojs/cloudflare`, `@astrojs/netlify`, or `@astrojs/deno`. Without an adapter, SSR pages will fail to build.

**Astro 6** introduces the Vite Environment API, which runs the exact production runtime locally during development. For example, if deploying to Cloudflare, the dev server runs the `workerd` runtime so you catch runtime incompatibilities before deployment.

Combine static pages with Server Islands when you need personalized fragments (user greeting, cart count) on otherwise cacheable static pages. This avoids making the entire page SSR for one dynamic element.

## Astro Actions (Form Handling)

Astro Actions replace manual API endpoint boilerplate for mutations. Define them in `src/actions/index.ts` using `defineAction()`:

```ts
import { defineAction, z } from 'astro:actions';

export const server = {
  subscribe: defineAction({
    accept: 'form',
    input: z.object({
      email: z.string().email(),
    }),
    handler: async ({ email }) => {
      await addSubscriber(email);
      return { success: true };
    },
  }),
};
```

Use `accept: 'form'` with a Zod input validator for type-safe form data. Throw `ActionError` with standard codes (`"UNAUTHORIZED"`, `"NOT_FOUND"`, `"BAD_REQUEST"`) for backend failures. Use `isInputError()` on the client to display field-specific validation messages.

For progressive enhancement, use `<form action={actions.subscribe} method="POST">` — this works without JavaScript. Read results server-side with `Astro.getActionResult()`. Implement the POST/Redirect/GET pattern after successful form submissions to prevent resubmission warnings on page refresh.

Prefer Astro Actions over raw API endpoints for all form and mutation handling. Reserve raw endpoints for external-facing APIs, webhooks, and dynamic asset generation.

## Middleware (src/middleware.ts)

Middleware intercepts every request and is the architectural backbone for cross-cutting concerns. Use it for:

- **Authentication:** Read session cookies, validate tokens, redirect unauthenticated users with `return context.redirect('/login')`.
- **Data passing:** Attach validated user data to `context.locals`. MUST append properties to the existing `locals` object — never overwrite or reassign `context.locals` entirely, as this destroys data set by other middleware in the chain.
- **Action gating:** Use `getActionContext()` to block actions that require a valid session before the handler runs.
- **Security headers:** Inject CSP, CORS, and rate-limiting headers on every response.
- **Session management:** Use `Astro.cookies` with `httpOnly`, `secure`, and `sameSite` options for cookie-based sessions.

## API Endpoints

Place endpoints in `src/pages/api/` with `.ts` or `.js` extensions. Export named HTTP method handlers (`GET`, `POST`, `PUT`, `DELETE`). Return standard `Response` objects:

```ts
export const GET: APIRoute = async ({ params, request }) => {
  const query = new URL(request.url).searchParams.get('q');
  const results = await search(query);
  return new Response(JSON.stringify(results), {
    headers: { 'Content-Type': 'application/json' },
  });
};
```

Use API endpoints for external-facing APIs, webhook receivers, and dynamic asset generation (OG images, sitemaps). For internal form handling and mutations, prefer Astro Actions.

## TypeScript

Astro 5+ uses `.astro/types.d.ts` for type inference, not `src/env.d.ts`. Ensure your `tsconfig.json` includes the correct directories and references `.astro/types.d.ts`. Use the `astro:env` module for type-safe environment variables — define your schema in `astro.config` under `env.schema` and import validated variables from `astro:env/server` or `astro:env/client`.

`Astro.glob()` is DEPRECATED. Use `getCollection()` from `astro:content` for content files or `import.meta.glob()` for arbitrary file imports.

## View Transitions

Add `<ClientRouter />` from `astro:transitions` to your shared layout `<head>` for SPA-like client-side navigation between pages:

```astro
---
import { ClientRouter } from 'astro:transitions';
---
<head>
  <ClientRouter />
</head>
```

Use `transition:persist` on components that must maintain state across page navigations — video players, audio elements, interactive islands with user input. Use `data-astro-reload` on links that should bypass the client-side router and trigger a full page load (login portals, external applications). Use `transition:animate` to control enter/exit animations per element.

## Image Handling

Always use `<Image />` from `astro:assets` instead of raw `<img>` tags for local images. The component auto-infers dimensions to prevent Cumulative Layout Shift, generates optimized formats, and produces responsive `srcset` attributes.

Store all optimizable images in `src/assets/`, never in `public/`. Images in `public/` are copied verbatim without processing. Use `layout="responsive"` to generate `srcset` and `sizes` for optimal device-specific loading.

Always provide the `alt` attribute — the `<Image />` component requires it. Use `alt=""` only for purely decorative images that convey no information.

For remote images, authorize domains in `astro.config` under `image.domains` for exact domain matching or `image.remotePatterns` for pattern-based matching. Without authorization, remote image optimization will fail.

```astro
---
import { Image } from 'astro:assets';
import heroImg from '../assets/hero.jpg';
---
<Image src={heroImg} alt="Mountain landscape at sunrise" layout="responsive" />
```

## Quick Reference: Common Mistakes

| Mistake | Fix |
|---------|-----|
| `document is not defined` | Move browser API calls from frontmatter to `<script>` tag or `client:only` component |
| `window is not defined` | Same — server code cannot access `window` |
| Component not interactive | Add the appropriate `client:*` directive |
| Content validation error | Check Zod schema in `content.config.ts`, verify frontmatter fields match |
| Using `entry.render()` | Import `render()` from `astro:content` and pass the entry to it |
| Using `slug` property | Use `id` instead — `slug` was removed in Astro 5 |
| `output: 'hybrid'` | Deprecated in Astro 5+ — use `output: 'static'` with per-page `prerender = false` |
| `Astro.glob()` calls | Deprecated — use `getCollection()` or `import.meta.glob()` |
| Images in `public/` not optimizing | Move to `src/assets/` for `<Image />` processing |
| `console.log` not showing | Frontmatter logs go to terminal; use `<script>` for browser console |
