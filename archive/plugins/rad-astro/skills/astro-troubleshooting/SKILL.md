---
name: astro-troubleshooting
description: >
  This skill should be used when debugging Astro issues, identifying Astro anti-patterns, fixing common Astro mistakes, troubleshooting Astro errors, resolving "document is not defined" in Astro, resolving "window is not defined" in Astro, diagnosing a component not interactive, fixing content validation errors, investigating why an Astro build fails, debugging hydration issues, solving Astro 5 migration problems, fixing slug vs id errors, resolving render method not found, diagnosing Astro performance problems, reducing too much JavaScript in Astro, fixing Astro routing errors, or addressing form resubmission warnings.
---

# Astro Troubleshooting & Anti-Patterns

You are an expert Astro troubleshooter. When the user encounters an Astro issue, diagnose the root cause systematically using the patterns below. Do not guess -- match symptoms to known causes before recommending fixes.

## Architecture Anti-Patterns

### The Hydration Storm

When the user reports slow page load, large JS bundle, or poor LCP/INP scores, check for the Hydration Storm pattern.

- **Symptom:** Slow page load, large JS bundle, poor LCP/INP.
- **Cause:** Multiple components all using `client:load`, forcing simultaneous download, parse, and execute of framework runtimes.
- **Fix:** Audit every `client:*` directive in the project. Replace `client:load` with `client:visible` for below-the-fold components and `client:idle` for non-critical interactive elements. Break large interactive sections into small, granular islands so only the minimum JavaScript ships per component.

### The SSR Golden Hammer

When the user reports high server costs, slow TTFB, or unnecessary compute on every request, check for over-reliance on SSR.

- **Symptom:** High server costs, slow TTFB, unnecessary compute.
- **Cause:** Using `output: 'server'` for pages that could be static.
- **Fix:** Use the hybrid approach -- static by default, SSR only for truly dynamic routes. For pages that are "mostly static with one dynamic part," use a static page with `server:defer` for the dynamic fragment. This eliminates unnecessary server round-trips for content that rarely changes.

### The Stovepipe Data Architecture

When the user reports duplicated API calls or the same data fetched multiple times across components on a single page, check for stovepipe data fetching.

- **Symptom:** Same data fetched multiple times across different components on the same page.
- **Cause:** Each island independently fetching the same API or database data.
- **Fix:** Fetch data once in the page frontmatter and pass it as props to child components. For shared state across islands that need to communicate, use `nanostores` or a similar lightweight shared state library. Never let each island manage its own data fetching for shared resources.

### Layout Wrapper Anti-Pattern

When the user reports that an entire page hydrates as one massive JS bundle, check for the layout wrapper pattern.

- **Symptom:** Entire page hydrates as one massive JS bundle.
- **Cause:** Wrapping a layout-level component in a single React/Vue/Svelte component with `client:load`.
- **Fix:** Keep layouts as `.astro` components. Only hydrate specific small interactive widgets within the layout. The layout itself should never be a framework component -- it should be an Astro component that contains small, targeted islands.

## Client Directive Mistakes

### Component Not Interactive

When the user reports that a React, Vue, or Svelte component renders but buttons, inputs, or event handlers do not work, check for a missing client directive.

- **Symptom:** React/Vue/Svelte component renders but buttons and inputs do not work.
- **Cause:** Missing `client:*` directive. Without it, the component renders as static HTML only -- no JavaScript is sent to the browser.
- **Fix:** Add the appropriate `client:*` directive. Use `client:load` for immediately interactive components, `client:visible` for components that become interactive when scrolled into view, and `client:idle` for components that hydrate after the page is idle.

### Using client:only Inappropriately

When the user reports content flash, missing SSR, or poor SEO for a specific component, check for inappropriate use of `client:only`.

- **Symptom:** Content flash, no SSR, poor SEO for that component.
- **Cause:** Using `client:only` when the component does not strictly need browser APIs at render time.
- **Fix:** Only use `client:only` for components that MUST have `window` or `document` available at render time (e.g., canvas libraries, map widgets). Otherwise, use `client:load` or `client:visible` to get SSR benefits. The `client:only` directive skips server rendering entirely.

### Too Many Islands in Loops

When the user reports dozens of hydrated components or a massive JS payload from a list, check for islands spawned in loops.

- **Symptom:** Dozens of hydrated components, massive JS payload.
- **Cause:** Using `.map()` to spawn `client:*` components for each list item.
- **Fix:** Render list items as static HTML. Hydrate a single controller component (filter, sorter, paginator) that manages the list interaction. Each hydrated island carries overhead -- framework runtime, props serialization, hydration bootstrap -- so minimize the number of islands.

## Browser API Errors

### "document is not defined" / "window is not defined"

When the user encounters a build failure or runtime error about `document` or `window` not being defined, this is a server-side rendering boundary issue.

- **Symptom:** Build fails or runtime error referencing `document` or `window`.
- **Cause:** Using browser APIs (`window`, `document`, `localStorage`, `navigator`) in `.astro` frontmatter or server-side code. Astro runs this code on the server where no browser exists.
- **Fix:** Move browser-dependent code into `<script>` tags (which run client-side) or use `client:only="react"` (or the appropriate framework) for components that need browser APIs at render time. For conditional checks inside framework components, guard with `if (typeof window !== 'undefined')`. Never place browser API calls in `.astro` frontmatter.

## Content Layer / Collection Errors (Astro 5+)

### slug Property Not Found

When the user encounters a build error about `slug` being undefined or routing fails after upgrading to Astro 5, check for the slug-to-id migration issue.

- **Symptom:** Build error, routing fails, undefined property on `slug`.
- **Cause:** Using `entry.slug` which was removed in Astro 5. The property is now `entry.id`.
- **Fix:** Replace all `slug` references with `id`. Update dynamic routes accordingly: `params: { slug: post.id }`. Search the entire codebase for `.slug` usage on collection entries and replace every instance.

### entry.render() is Not a Function

When the user encounters a `TypeError` about `render()` not being a function on a content collection entry, this is an Astro 4 to 5 API change.

- **Symptom:** `TypeError` at build or request time saying `render` is not a function.
- **Cause:** Calling `render()` as a method on the entry object (the old Astro 4 API).
- **Fix:** Import the `render` utility from `astro:content` and call it as a standalone function:

```astro
---
import { render } from 'astro:content';
const { Content, headings } = await render(entry);
---
<Content />
```

Do not call `entry.render()` -- it no longer exists as a method on the entry object.

### Content Validation Fails

When the user encounters build errors with Zod validation messages from content collections, check the schema definition.

- **Symptom:** Build error with Zod validation messages.
- **Cause:** Schema too strict, missing `.optional()` on fields that may not exist in all entries, or date format mismatches.
- **Fix:** Use `.optional()` and `.default()` liberally on fields that are not guaranteed to exist. Use `z.coerce.date()` instead of `z.date()` for date fields -- raw frontmatter dates are strings, not Date objects. Audit external API data or markdown frontmatter against your schema to find mismatches.

### "type: 'content'" No Longer Works

When the user reports that a collection is not recognized or the legacy type syntax is failing, check for the old implicit loader syntax.

- **Symptom:** Collection not recognized, configuration errors.
- **Cause:** Using the legacy implicit loader syntax with `type: 'content'` or `type: 'data'`.
- **Fix:** Use explicit loaders. Use `glob()` for file directories, `file()` for single JSON or YAML files, and custom loaders for APIs. Example:

```ts
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({ /* ... */ }),
});
```

## Routing Errors

### output: 'hybrid' Warning/Error

When the user encounters a deprecation warning or unexpected behavior with `output: 'hybrid'`, this mode was removed in Astro 5.

- **Symptom:** Deprecation warning or unexpected behavior.
- **Cause:** Using `output: 'hybrid'` which was merged into `'static'` in Astro 5+.
- **Fix:** Use `output: 'static'` in `astro.config.mjs` and add `export const prerender = false` to individual pages that need SSR. This achieves the same hybrid behavior.

### Dynamic Prerender Flag Error

When the user encounters a build error about the prerender value, check for dynamic assignment.

- **Symptom:** Build error about prerender value.
- **Cause:** Using a dynamic value like `export const prerender = import.meta.env.SOME_VAR`.
- **Fix:** The `prerender` export MUST be a static boolean literal -- either `true` or `false`. No dynamic values, no environment variables, no computed expressions. Astro determines prerender status at build analysis time before runtime.

### Route Parameter Decoding Issues

When the user reports that special characters in URLs break routing, check the decoding method.

- **Symptom:** Special characters in URLs break routing.
- **Cause:** Using `decodeURIComponent` which incorrectly decodes `/`, `?`, and `#`.
- **Fix:** Use `decodeURI` instead of `decodeURIComponent` for route parameters. The `decodeURIComponent` function decodes characters that have special meaning in URLs, breaking the route structure.

### Astro.glob() Deprecated

When the user encounters a deprecation warning about `Astro.glob()`, migrate to the modern API.

- **Symptom:** Deprecation warning about `Astro.glob()`.
- **Cause:** Using the legacy `Astro.glob()` API.
- **Fix:** Use `getCollection()` from `astro:content` for content collections. Use `import.meta.glob()` for other file imports. The `Astro.glob()` function is removed in Astro 5.

## Form & Action Issues

### Form Resubmission Warning

When the user reports a "Confirm form resubmission?" dialog appearing on page refresh after a form submission, implement the POST/Redirect/GET pattern.

- **Symptom:** "Confirm form resubmission?" dialog on page refresh after form submit.
- **Cause:** Standard HTML form POST renders the result as a POST response. Refreshing replays the POST.
- **Fix:** Implement the POST/Redirect/GET pattern in middleware. Intercept the form action, process the data, persist the result to a session or cookie, then redirect to a GET request. The GET handler reads the persisted result and renders the page.

## TypeScript Issues

### Types Not Working / Autocomplete Missing

When the user reports no type inference for Astro APIs, collections, or components, check the TypeScript configuration.

- **Symptom:** No type inference for Astro APIs, collections, or components.
- **Cause:** Using the old `src/env.d.ts` reference. Astro 5 moved generated types to `.astro/types.d.ts`.
- **Fix:** Update `tsconfig.json` to include the `.astro` directory. Remove old `src/env.d.ts` references. Ensure the `include` array in `tsconfig.json` contains `".astro/types.d.ts"`.

## Layout Issues

### Non-ASCII Characters Broken (Astro 5+)

When the user reports garbled text or encoding issues on Markdown or MDX pages after upgrading to Astro 5, check for a missing charset meta tag.

- **Symptom:** Garbled text, encoding issues on Markdown/MDX pages.
- **Cause:** Missing charset meta tag in the layout component. Astro 5+ no longer auto-adds charset for pages using the `layout` frontmatter property.
- **Fix:** Add `<meta charset="utf-8">` manually in your layout's `<head>`. This must be present in every layout that renders Markdown or MDX content.

### layout Property in Content Collection Entries

When the user reports unexpected behavior or ignored layout settings in content collection entries, check where the layout property is being used.

- **Symptom:** Unexpected behavior or ignored layout.
- **Cause:** Using the `layout` frontmatter property in content collection Markdown files.
- **Fix:** The `layout` property is for standalone Markdown pages in `src/pages/` ONLY. For content collection entries, wrap with a layout in the rendering page -- the page that calls `render(entry)` should use an Astro layout component.

## Edge Cases

### Streaming Error Blind Spot

Be aware that if a component throws an error AFTER response headers are sent during HTML streaming, middleware CANNOT catch it. The response will show a 200 OK status but the page will be broken or incomplete. You cannot buffer the entire response to fix this without negating streaming benefits. Handle errors within components themselves and provide fallback content for error states.

### Async compiledContent()

In Astro 5+, `compiledContent()` on Markdown imports is now async. Forgetting to `await` it causes silent failures where the content appears empty or undefined. Always use: `const html = await post.compiledContent()`.

### context.locals Overwrite

Never overwrite the entire `context.locals` object. This destroys data set by other middleware.

- **Wrong:** `context.locals = { user }` (overwrites entire object)
- **Correct:** `context.locals.user = user` (appends to existing)

### astro:content on Client

Astro 5 blocks importing `astro:content` in client-side code because it would bloat the bundle with server logic. Query collections server-side in `.astro` frontmatter or API routes, then pass the results as props to client components.

## Quick Diagnosis Table

Use this table for rapid symptom-to-fix mapping:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| document/window not defined | Browser API in frontmatter | Move to `<script>` or `client:only` |
| Component not interactive | Missing `client:*` directive | Add appropriate directive |
| Slow page, large JS bundle | Hydration storm | Audit directives, use `client:visible` |
| entry.slug undefined | Astro 5 slug to id change | Use `entry.id` |
| entry.render() not a function | Old Astro 4 API | Import `render()` from `astro:content` |
| Content validation error | Schema mismatch | Add `.optional()`, use `z.coerce.date()` |
| Form resubmission warning | POST without redirect | POST/Redirect/GET in middleware |
| Non-ASCII chars broken | Missing charset in layout | Add `<meta charset="utf-8">` |
| Types not working | Old env.d.ts | Update to `.astro/types.d.ts` |
| output: 'hybrid' warning | Deprecated mode | Use `'static'` + `prerender = false` |
| Route decoding breaks | decodeURIComponent | Use `decodeURI` instead |
| Async content fails silently | Unawaited compiledContent | Always `await compiledContent()` |
| Locals data lost | Overwriting context.locals | Append, do not overwrite |
| astro:content import error | Client-side import | Query server-side, pass as props |
| Prerender build error | Dynamic prerender flag | Use static `true` or `false` only |
