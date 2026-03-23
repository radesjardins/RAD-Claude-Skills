---
name: technical-seo
description: >
  Audits the technical SEO foundation of a website — crawlability, indexation,
  Core Web Vitals, page speed, mobile-first compliance, robots.txt, sitemaps,
  canonical tags, redirects, HTTPS, JavaScript rendering, and security headers.
  Produces a scored report with fix commands for every issue. Use when the user
  asks about crawl errors, indexing problems, pages not showing in Google,
  Core Web Vitals failures (LCP, CLS, INP, TTFB), robots.txt or sitemap issues,
  redirect chains, noindex problems, canonical conflicts, JavaScript SEO, SSR
  concerns, mobile PageSpeed scores, crawl budget, mixed content, or site
  migration technical checks. Also triggers on "why aren't my pages indexed" or
  "Google Search Console shows errors." This is NOT for: writing Python scrapers,
  CDN/infrastructure setup, database query optimization, adding GTM/analytics
  tags, general code performance profiling, or simple one-off fixes like
  "compress this image." If the user wants a broad audit across all SEO
  categories, use full-seo-audit instead.
---

# Technical SEO Skill

Run a comprehensive technical SEO audit. Report every issue with a why-it-matters explanation, an exact fix command, and an expected ranking impact.

---

## 1. Crawlability & Indexation

### 1.1 robots.txt Validation

Read `robots.txt` at the site root. Check for these problems:

- **Missing robots.txt.** Search engines treat a missing file as "allow all," but it signals neglect and prevents crawl-budget directives.
- **Blocking important paths.** Flag any `Disallow` rule that covers pages meant to rank (e.g., `/blog/`, `/products/`).
- **Missing sitemap directive.** `robots.txt` should contain a `Sitemap:` line pointing to the XML sitemap.
- **Wildcard overreach.** Rules like `Disallow: /*?` can inadvertently block faceted navigation or parameterized pages that should be indexed.

**Why it matters:** A misconfigured robots.txt can deindex entire site sections overnight.

**Fix command:**
```
# See claude-code-fix-recipes.md — recipe: robots-txt-repair
claude "Read robots.txt, remove rules blocking /blog and /products, add Sitemap: https://example.com/sitemap.xml, and write the corrected file."
```

**Expected impact:** High. Blocked pages cannot rank at all.

### 1.2 XML Sitemap

Fetch the sitemap from the `Sitemap:` directive in robots.txt, or try `/sitemap.xml` and `/sitemap_index.xml`. Validate:

- Sitemap exists and returns HTTP 200.
- All URLs return 200 (no 404s, no redirects).
- Sitemap contains fewer than 50,000 URLs per file (protocol limit).
- `<lastmod>` dates are present and accurate.
- No URLs blocked by robots.txt appear in the sitemap.
- Sitemap is referenced in robots.txt.

**Why it matters:** Sitemaps guide crawlers to new and updated content. Broken entries waste crawl budget.

**Fix command:**
```
# See claude-code-fix-recipes.md — recipe: sitemap-generate
claude "Crawl all public pages, generate a valid XML sitemap with accurate lastmod dates, exclude noindexed URLs, and write sitemap.xml to the public root."
```

**Expected impact:** Medium. Accelerates discovery of new pages; critical for large sites (1,000+ pages).

### 1.3 Canonical Tag Audit

For every indexable page, inspect the `<link rel="canonical">` tag:

- **Missing canonical.** Every indexable page needs one.
- **Conflicting canonical.** The canonical must not point to a page that itself canonicalizes elsewhere (chain).
- **Self-referencing canonical.** Acceptable and recommended, but flag if the URL differs by trailing slash, protocol, or www.
- **Cross-domain canonical.** Flag unless intentional (syndication).
- **Canonical on paginated pages.** Paginated pages should canonicalize to themselves, not page 1.

**Why it matters:** Incorrect canonicals consolidate ranking signals to the wrong URL or cause deindexation.

**Fix command:**
```
# See claude-code-fix-recipes.md — recipe: canonical-fix
claude "Audit every page's canonical tag. Add self-referencing canonicals where missing. Fix any canonical that points to a redirected or noindexed URL."
```

**Expected impact:** High. Duplicate content confusion directly suppresses rankings.

### 1.4 Noindex / Nofollow Audit

Scan every page for `<meta name="robots" content="noindex">` and `X-Robots-Tag` headers:

- Flag pages with `noindex` that appear in the sitemap.
- Flag pages with `noindex` that receive internal links as if they are indexable.
- Flag `nofollow` on internal links (leaks PageRank).
- Flag conflicting directives between meta tag and HTTP header.

**Why it matters:** Accidental noindex removes pages from search entirely. Internal nofollow wastes link equity.

**Fix command:**
```
# See claude-code-fix-recipes.md — recipe: meta-robots-cleanup
claude "Find all pages with noindex that should be indexed. Remove the noindex directive and ensure they are in the sitemap."
```

**Expected impact:** High for affected pages.

### 1.5 Orphan Page Detection

Compare the set of URLs in the sitemap against the set of URLs reachable by following internal links from the homepage:

- Pages in the sitemap but not linked internally are orphans.
- Pages linked internally but missing from the sitemap are sitemap gaps.

**Why it matters:** Orphan pages receive no internal link equity and are rarely crawled. Sitemap gaps slow discovery.

**Fix command:**
```
# See claude-code-fix-recipes.md — recipe: internal-link-orphans
claude "Identify orphan pages. For each, suggest the most relevant existing page to add an internal link from. Generate the link markup."
```

**Expected impact:** Medium. Orphan pages often see a ranking boost once internally linked.

### 1.6 Crawl Budget Optimization

Check for crawl-budget drains:

- Infinite-scroll or faceted navigation generating unbounded URL permutations.
- Session IDs or tracking parameters in URLs.
- Soft-404 pages (return 200 but display "not found" content).
- Duplicate content accessible at multiple URL paths.

**Why it matters:** On large sites, wasted crawl budget means new content takes weeks to appear in search.

**Fix command:**
```
# See claude-code-fix-recipes.md — recipe: crawl-budget-optimize
claude "Add parameter handling rules to robots.txt. Implement rel=canonical on parameterized variants. Return proper 404 status codes for dead pages."
```

**Expected impact:** Medium-High on sites with 10,000+ pages. Negligible on small sites.

---

## 2. Core Web Vitals

### 2.1 Largest Contentful Paint (LCP) — Target < 2.5 s

Identify the LCP element (usually hero image, heading, or video poster). Check:

- Image is served in next-gen format (WebP/AVIF).
- Image has explicit `width` and `height` attributes.
- Image is preloaded with `<link rel="preload">`.
- No render-blocking CSS or JS delays the LCP element.
- Server response time (TTFB) is under 800 ms.
- Critical CSS is inlined; non-critical CSS is deferred.

**Why it matters:** LCP is a direct Google ranking signal. Pages above 2.5 s lose ranking eligibility for Top Stories and some SERP features.

**Fix commands:**

| Framework | Command |
|-----------|---------|
| Next.js | `claude "Use next/image with priority prop on the hero image. Enable next/font to eliminate font-swap delay. Move non-critical CSS to dynamic imports."` |
| React | `claude "Preload the hero image in index.html. Code-split below-the-fold components with React.lazy. Inline critical CSS with critters."` |
| WordPress | `claude "Install and configure a caching plugin. Add preload tags for hero images in header.php. Defer non-critical plugins."` |
| Static HTML | `claude "Convert hero images to WebP. Add preload link tags. Inline above-the-fold CSS. Defer all JS with the defer attribute."` |

**Expected impact:** High. LCP improvement from 4 s to 2 s can move pages up 2-5 positions.

### 2.2 Interaction to Next Paint (INP) — Target < 200 ms

Identify long-running event handlers (click, keydown, pointerdown). Check:

- No synchronous `localStorage` or `sessionStorage` reads in event handlers.
- Heavy computation is offloaded to Web Workers or `requestIdleCallback`.
- Input handlers are debounced where appropriate.
- Third-party scripts do not block the main thread for > 50 ms.
- React hydration does not block interactivity (check for `hydrateRoot` usage).

**Why it matters:** INP replaced FID as a Core Web Vital in March 2024. Poor INP directly reduces rankings.

**Fix commands:**

| Framework | Command |
|-----------|---------|
| Next.js | `claude "Wrap expensive event handlers in startTransition. Move analytics to a web worker. Add the Interaction to Next Paint diagnostic to next.config.js."` |
| React | `claude "Use useTransition for non-urgent state updates. Debounce search input handlers to 150 ms. Lazy-load modal content."` |
| WordPress | `claude "Defer third-party scripts. Replace jQuery event handlers with vanilla JS. Add async to non-critical enqueued scripts."` |
| Static HTML | `claude "Move analytics scripts to defer. Break long tasks into chunks using scheduler.yield(). Remove unused JS."` |

**Expected impact:** High. INP violations correlate with higher bounce rates and lower rankings.

### 2.3 Cumulative Layout Shift (CLS) — Target < 0.1

Detect layout-shifting elements. Check:

- All images and videos have explicit `width` and `height` (or `aspect-ratio` in CSS).
- Web fonts use `font-display: swap` with a size-adjusted fallback.
- Ads and embeds have reserved space via `min-height`.
- No content is injected above the fold after initial paint.
- Dynamic banners (cookie consent, promos) use CSS `transform` instead of pushing content.

**Why it matters:** CLS is a Core Web Vital. Layout shifts frustrate users and depress rankings.

**Fix commands:**

| Framework | Command |
|-----------|---------|
| Next.js | `claude "Add width and height to all next/image components. Configure next/font with adjustFontFallback. Reserve ad slot space with min-height in CSS modules."` |
| React | `claude "Set explicit dimensions on every img and iframe. Use Skeleton components for async content. Apply will-change: transform to animated elements."` |
| WordPress | `claude "Add missing width/height attributes to all img tags in theme templates. Preload the primary web font. Set min-height on ad containers in style.css."` |
| Static HTML | `claude "Add width and height attributes to every img tag. Add aspect-ratio CSS for responsive images. Reserve space for ad containers."` |

**Expected impact:** Medium-High. CLS fixes produce immediate ranking improvements on mobile.

---

## 3. Mobile-First

### 3.1 Viewport Meta Tag

Verify `<meta name="viewport" content="width=device-width, initial-scale=1">` is present in `<head>`:

- Flag if missing entirely.
- Flag if `maximum-scale=1` or `user-scalable=no` is set (accessibility violation).

**Fix command:**
```
claude "Add the viewport meta tag to every HTML template. Remove maximum-scale and user-scalable=no restrictions."
```

**Expected impact:** Critical. Without the viewport tag, Google treats the page as non-mobile-friendly.

### 3.2 Mobile Content Parity

Compare rendered content between mobile and desktop user agents:

- Flag text visible on desktop but hidden on mobile (display:none on small screens).
- Flag images present on desktop but absent on mobile.
- Flag structured data present on desktop but missing from mobile markup.

**Fix command:**
```
claude "Find all CSS rules that hide content on mobile. Replace display:none with responsive layout that preserves content. Ensure structured data is in the server-rendered HTML."
```

**Expected impact:** High. Google uses mobile-first indexing; hidden mobile content is invisible to the index.

### 3.3 Touch Target Sizing

Scan interactive elements (links, buttons, inputs) for:

- Minimum size of 48x48 CSS pixels.
- Minimum spacing of 8px between adjacent targets.

**Fix command:**
```
claude "Set min-height: 48px and min-width: 48px on all buttons and link areas. Add padding to inline links in body text. Ensure 8px gap between adjacent tap targets."
```

**Expected impact:** Low-Medium. Affects mobile usability score and can trigger manual demotion.

### 3.4 Font Sizes

Check that body text is at least 16px and that no text block requires zooming to read:

- Flag body font-size below 16px.
- Flag text containers narrower than viewport causing overflow.

**Fix command:**
```
claude "Set base font-size to 16px on the body element. Ensure all text containers use max-width: 100% and overflow-wrap: break-word."
```

**Expected impact:** Low-Medium. Improves mobile usability score.

### 3.5 Horizontal Scrolling

Detect viewport overflow on mobile widths (360px-414px):

- Flag elements with fixed widths exceeding viewport.
- Flag tables without horizontal scroll wrappers.
- Flag images without `max-width: 100%`.

**Fix command:**
```
claude "Add max-width: 100% to all images. Wrap wide tables in a div with overflow-x: auto. Replace fixed-width elements with responsive equivalents."
```

**Expected impact:** Low-Medium. Horizontal scrolling triggers mobile usability failures in Search Console.

---

## 4. Security

### 4.1 HTTPS Everywhere

Check every page and resource:

- All pages load over HTTPS.
- No mixed content (HTTP resources on HTTPS pages).
- HTTP-to-HTTPS redirect is in place (301, not 302).
- SSL certificate is valid and not expiring within 30 days.

**Why it matters:** HTTPS is a confirmed ranking signal. Mixed content triggers browser warnings that destroy trust.

**Fix command:**
```
claude "Find all HTTP resource references (images, scripts, stylesheets). Rewrite them to HTTPS or protocol-relative URLs. Verify the 301 redirect from HTTP to HTTPS in the server config."
```

**Expected impact:** Medium. HTTPS is a lightweight signal, but mixed content warnings devastate click-through rates.

### 4.2 HSTS Header

Check for `Strict-Transport-Security` header:

- Present with `max-age` of at least 31536000 (one year).
- `includeSubDomains` directive present.
- `preload` directive present if the site is on the HSTS preload list.

**Fix command:**
```
claude "Add Strict-Transport-Security: max-age=31536000; includeSubDomains; preload to the server configuration. For Next.js, add it to next.config.js headers. For WordPress, add it to .htaccess."
```

**Expected impact:** Low direct ranking impact. Prevents SSL-stripping attacks and builds user trust.

### 4.3 Content-Security-Policy

Check for a `Content-Security-Policy` header:

- Flag if entirely missing.
- Flag overly permissive directives (`unsafe-inline`, `unsafe-eval`, `*`).
- Verify `frame-ancestors` is set to prevent clickjacking.

**Fix command:**
```
claude "Generate a Content-Security-Policy header based on the site's actual resource origins. Start with a report-only policy, then enforce after verifying no breakage."
```

**Expected impact:** Low direct ranking impact. Protects against XSS; compromised sites get deindexed.

### 4.4 Sensitive File Exposure

Check for publicly accessible files that should not be exposed:

- `.env`, `.git/`, `wp-config.php`, `config.yml`, `package.json` (with private keys).
- Database dumps (`.sql`).
- Backup files (`.bak`, `.old`).
- `phpinfo.php`.

**Fix command:**
```
claude "Add deny rules to the server config for .env, .git, and backup files. Remove any sensitive files from the public directory. Add them to .gitignore."
```

**Expected impact:** Low ranking impact but critical for site safety. Hacked sites get deindexed.

---

## 5. URL Structure

### 5.1 Clean, Descriptive URLs

Evaluate URL patterns across the site:

- URLs contain readable words, not IDs or hashes (bad: `/p/12345`; good: `/products/blue-widget`).
- URLs reflect site hierarchy (`/category/subcategory/page`).
- URLs are not excessively deep (4+ path segments).

**Fix command:**
```
claude "Identify URLs that use numeric IDs or hashes. Propose slug-based alternatives. Generate 301 redirect rules from old to new URLs."
```

**Expected impact:** Medium. Descriptive URLs improve click-through rates in SERPs and provide keyword signals.

### 5.2 Lowercase, Hyphen-Separated

Check all internal URLs:

- Flag uppercase characters in paths.
- Flag underscores (use hyphens instead).
- Flag spaces or encoded characters (%20).

**Fix command:**
```
claude "Add a server-side middleware that lowercases all URL paths and 301-redirects uppercase variants. Replace underscores with hyphens in all route definitions."
```

**Expected impact:** Low. Prevents duplicate content from case variants.

### 5.3 Query Parameters on Important Pages

Identify pages that rank or should rank and check whether their canonical URL uses query parameters:

- Flag important content accessible only via query strings (`?id=123`).
- Flag sorting/filtering parameters that generate indexable duplicate pages.

**Fix command:**
```
claude "Convert query-parameter-based routes to path-based routes. Add canonical tags to parameterized variants pointing to the clean URL. Update internal links."
```

**Expected impact:** Medium. Clean URLs outperform parameterized URLs in CTR and perceived relevance.

### 5.4 Pagination Handling

Check paginated content (blog listings, product categories):

- Each paginated page is self-canonicalized (not to page 1).
- `rel="next"` and `rel="prev"` are present (still used by some engines).
- Paginated pages are in the sitemap.
- No infinite scroll without progressive-enhancement URLs.

**Fix command:**
```
claude "Add self-referencing canonicals to each paginated page. Add rel=next/prev link tags. Ensure all paginated URLs appear in the sitemap."
```

**Expected impact:** Medium for content-heavy sites with deep pagination.

---

## 6. JavaScript SEO

### 6.1 Server-Side Rendering Check

Fetch each key page with JavaScript disabled (or inspect the raw HTML source):

- Flag pages where the `<body>` contains only a root `<div>` and a `<script>` tag (client-side-only rendering).
- Verify that title, meta description, headings, and body text are in the initial HTML.
- Verify that internal links are `<a href="...">` elements, not JavaScript-triggered navigation.

**Why it matters:** Googlebot can render JavaScript, but it queues pages for rendering, delaying indexation by hours to weeks. Content in the initial HTML is indexed immediately.

**Fix commands:**

| Framework | Command |
|-----------|---------|
| Next.js | `claude "Convert client-side pages to use getStaticProps or getServerSideProps. Ensure all pages export server-rendered HTML with full content."` |
| React | `claude "Set up server-side rendering with ReactDOMServer or migrate to a framework like Next.js. As a quick fix, add react-snap for static pre-rendering."` |
| WordPress | `claude "Verify that theme content is in PHP templates, not injected by JavaScript. Deactivate plugins that replace server-rendered content with JS widgets."` |

**Expected impact:** Critical. Client-side-only rendering can delay indexation by days and lose content from the index entirely.

### 6.2 Dynamic Rendering Detection

Check whether the server returns different content to Googlebot vs. regular users:

- Detect dynamic rendering setups (Rendertron, Puppeteer, prerender.io).
- Verify that the rendered output matches the client-side version.
- Flag if dynamic rendering is used as a permanent solution instead of SSR.

**Fix command:**
```
claude "Audit the dynamic rendering layer. Compare Googlebot-rendered output to browser-rendered output. Flag any content discrepancies. Plan migration to native SSR."
```

**Expected impact:** Medium. Dynamic rendering works but adds fragility. SSR is the long-term solution.

### 6.3 JavaScript-Dependent Content

Identify critical content loaded asynchronously:

- Product prices, reviews, and availability loaded via API calls.
- Article body text fetched after initial render.
- Internal links rendered by JavaScript frameworks.

**Fix command:**
```
claude "Move critical content (prices, reviews, article text) to the server-rendered HTML. Use progressive enhancement: load the HTML first, then hydrate interactivity."
```

**Expected impact:** High for e-commerce and content sites. Search engines may miss JS-dependent content.

### 6.4 Lazy-Loading Implementation

Check image and iframe lazy-loading:

- Above-the-fold images must NOT be lazy-loaded (harms LCP).
- Below-the-fold images should use `loading="lazy"`.
- Verify that lazy-loaded images have `<noscript>` fallbacks or are in the HTML source.

**Fix command:**
```
claude "Remove loading=lazy from the first 2 images (above the fold). Add loading=lazy to all other images. Ensure lazy-loaded images have width and height attributes."
```

**Expected impact:** Medium. Correct lazy-loading improves LCP while reducing bandwidth.

---

## 7. Redirects

### 7.1 Redirect Chain Detection

Follow every redirect path to its final destination. Flag:

- Chains of 2+ redirects (A -> B -> C). Flatten to A -> C.
- Chains exceeding 3 hops (Googlebot may stop following after 5).
- Internal links pointing to URLs that redirect (update the link target instead).

**Why it matters:** Each redirect hop adds latency (100-300 ms) and leaks a small amount of PageRank.

**Fix command:**
```
claude "Map all redirect chains. Generate updated redirect rules that point directly to the final destination. Update all internal links to use the final URL."
```

**Expected impact:** Medium. Flattening chains improves crawl efficiency and preserves link equity.

### 7.2 Mixed Redirect Types (301 vs. 302)

Audit every redirect for the correct status code:

- Permanent moves must be 301 or 308 (passes full link equity).
- Temporary redirects (302, 307) must only be used for genuinely temporary situations.
- Flag 302 redirects that have been in place for more than 30 days (likely should be 301).

**Fix command:**
```
claude "Find all 302 redirects. For each, determine if the move is permanent. Convert permanent moves to 301. Document any that should remain 302 with a comment explaining why."
```

**Expected impact:** Medium. 302 redirects may not pass full link equity, diluting rankings over time.

### 7.3 Redirect Loops

Detect circular redirects where URL A redirects to B and B redirects back to A (or longer cycles):

- Flag any redirect that does not terminate in a 200 response within 10 hops.
- Check for conditional redirect loops triggered by user-agent, cookies, or geo-location.

**Fix command:**
```
claude "Trace all redirect paths. Identify loops. Break each loop by removing the offending rule and pointing to the correct final destination."
```

**Expected impact:** Critical. Redirect loops make pages completely inaccessible to both users and search engines.

---

## Output Format

Present results as a scorecard followed by categorized issues.

### Summary Scorecard

| Category | Score | Critical | Warnings | Passed |
|----------|-------|----------|----------|--------|
| Crawlability & Indexation | A-F | count | count | count |
| Core Web Vitals | A-F | count | count | count |
| Mobile-First | A-F | count | count | count |
| Security | A-F | count | count | count |
| URL Structure | A-F | count | count | count |
| JavaScript SEO | A-F | count | count | count |
| Redirects | A-F | count | count | count |
| **Overall** | **A-F** | **total** | **total** | **total** |

### Issue Format

For every issue found, output:

```
### [CRITICAL|WARNING] Issue Title

**Category:** Category Name > Sub-check
**Why it matters:** One-sentence explanation of the SEO impact.
**Affected URLs:** List of URLs or "site-wide"
**Fix command:**
  claude "Exact command to fix the issue — see claude-code-fix-recipes.md"
**Expected impact:** High | Medium | Low — brief explanation.
```

### Priority Order

Sort issues by expected impact:

1. Critical issues blocking indexation (noindex on key pages, redirect loops, missing SSR).
2. Core Web Vitals failures.
3. Mobile-first violations.
4. Redirect problems.
5. URL structure issues.
6. Security hardening.

---

## Framework Detection

Auto-detect the framework before running checks:

| Signal | Framework |
|--------|-----------|
| `next.config.js` or `next.config.mjs` in project root | Next.js |
| `package.json` with `react-scripts` or `vite` + `react` | React (SPA) |
| `wp-config.php` or `wp-content/` directory | WordPress |
| Only `.html` files, no build tooling | Static HTML |

Tailor fix commands to the detected framework. When the framework is ambiguous, ask before proceeding.
