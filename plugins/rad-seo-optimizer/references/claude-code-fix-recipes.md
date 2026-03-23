# Claude Code Fix Recipes

Exact commands and approaches for fixing common SEO issues using Claude Code. These are referenced by all skills in the plugin to provide actionable remediation steps.

## Technical SEO Fixes

### robots.txt Issues
```
# Fix: Create or repair robots.txt
claude "Read the current robots.txt file and fix it to allow Googlebot access to all important pages while blocking admin, API, and private paths. Add a Sitemap directive pointing to /sitemap.xml"

# Fix: Unblock accidentally blocked resources
claude "Check robots.txt and ensure CSS, JS, and image files are not blocked from crawling"
```

### XML Sitemap
```
# Fix: Generate sitemap
claude "Generate an XML sitemap for this project that includes all public pages with proper lastmod dates, changefreq, and priority values. Exclude admin routes, API endpoints, and duplicate pages"

# Fix: Add sitemap to robots.txt
claude "Add 'Sitemap: https://example.com/sitemap.xml' to the robots.txt file"
```

### Canonical Tags
```
# Fix: Add missing canonicals
claude "Add rel=canonical tags to all pages in this project. Each page should point to its own canonical URL. For paginated content, point to the first page"

# Fix: Fix self-referencing canonicals
claude "Ensure every page has a self-referencing canonical tag with the full absolute URL including protocol"
```

### HTTPS / Security
```
# Fix: Force HTTPS redirects
claude "Add server-side redirect rules to force all HTTP traffic to HTTPS. Ensure no mixed content issues exist"

# Fix: Add security headers
claude "Add these security headers to the server config: Strict-Transport-Security, X-Content-Type-Options, X-Frame-Options, Content-Security-Policy"
```

### Redirect Chains
```
# Fix: Flatten redirect chains
claude "Find all redirect chains in the codebase (301/302 redirects that point to other redirects) and update them to point directly to the final destination"
```

## On-Page SEO Fixes

### Title Tags
```
# Fix: Add/optimize title tags
claude "Review all page title tags. Each should be 50-60 characters, include the primary keyword near the front, be unique across all pages, and include the brand name at the end"

# Fix: Dynamic title generation
claude "Create a utility function that generates SEO-optimized title tags from page data, ensuring proper length and keyword placement"
```

### Meta Descriptions
```
# Fix: Add/optimize meta descriptions
claude "Review all meta descriptions. Each should be 150-160 characters, include the target keyword, contain a call-to-action, and be unique. Generate missing ones from page content"
```

### Heading Structure
```
# Fix: Heading hierarchy
claude "Audit the heading structure on all pages. Ensure exactly one H1 per page containing the primary keyword, logical H2-H6 hierarchy with no skipped levels, and descriptive headings that read as section summaries"
```

### Image Optimization
```
# Fix: Missing alt text
claude "Find all images missing alt text and add descriptive, keyword-relevant alt attributes. Also add width and height attributes to prevent CLS"

# Fix: Image compression
claude "Convert all images to WebP format with appropriate quality settings. Add srcset for responsive images. Implement lazy loading for below-the-fold images"
```

## Schema Markup Fixes

### Add Schema
```
# Fix: Add Organization schema to homepage
claude "Add JSON-LD Organization schema to the homepage with name, url, logo, sameAs (social profiles), and contactPoint"

# Fix: Add Article schema to blog posts
claude "Add JSON-LD Article schema to all blog post templates with headline, author (Person), datePublished, dateModified, image, and publisher"

# Fix: Add FAQ schema
claude "Convert the FAQ section on this page into proper FAQPage JSON-LD schema markup"

# Fix: Add BreadcrumbList schema
claude "Add BreadcrumbList JSON-LD schema to all pages based on the URL hierarchy"

# Fix: Add Product schema
claude "Add Product JSON-LD schema to product pages including name, description, image, offers (price, currency, availability), and aggregateRating if reviews exist"
```

### Validate Schema
```
# Fix: Fix invalid schema
claude "Read the JSON-LD schema on this page and fix any validation errors: ensure all required properties exist, URLs are absolute, dates are ISO 8601, and the schema type matches the page content"
```

## Core Web Vitals Fixes

### LCP (Largest Contentful Paint)
```
# Fix: Optimize LCP
claude "Identify the LCP element on the main pages and optimize loading: preload critical images, inline critical CSS, defer non-critical JS, add fetchpriority='high' to hero images, and implement font-display: swap"
```

### CLS (Cumulative Layout Shift)
```
# Fix: Prevent layout shifts
claude "Fix CLS issues: add explicit width/height to all images and videos, reserve space for dynamic content and ads, avoid inserting content above existing content, and use CSS contain where appropriate"
```

### INP (Interaction to Next Paint)
```
# Fix: Improve responsiveness
claude "Optimize INP: break up long JavaScript tasks, use requestIdleCallback for non-critical work, debounce input handlers, and move heavy computation to Web Workers"
```

## Internal Linking Fixes

```
# Fix: Add internal links
claude "Analyze the site structure and add contextual internal links between related pages. Each important page should have at least 3 internal links pointing to it. Use descriptive anchor text"

# Fix: Fix orphan pages
claude "Find pages with no internal links pointing to them and add appropriate links from related content pages"

# Fix: Add breadcrumb navigation
claude "Add breadcrumb navigation to all pages based on the site hierarchy, with BreadcrumbList schema markup"
```

## Content Quality Fixes

```
# Fix: Add author bios
claude "Add an author bio section to all blog/article pages with the author's name, credentials, photo placeholder, and link to author page. Include Person schema markup"

# Fix: Add publish/update dates
claude "Add visible 'Published on' and 'Last updated' dates to all content pages with proper datePublished and dateModified schema"

# Fix: Add table of contents
claude "Add an auto-generated table of contents to long-form content pages (>1500 words) based on H2/H3 headings, with anchor links"
```

## AEO-Specific Fixes

```
# Fix: Convert to AEO-friendly format
claude "Reformat this content for AI search optimization: convert H2 headings to question format, add a direct 1-2 sentence answer at the start of each section, add FAQ schema, include quotable statistics in bold, and add comparison tables where relevant"

# Fix: Add Speakable schema
claude "Add Speakable schema markup to the key summary sections of this page to mark them as suitable for voice assistant and AI reading"
```

## Mobile Fixes

```
# Fix: Viewport configuration
claude "Ensure the viewport meta tag is set to 'width=device-width, initial-scale=1' on all pages"

# Fix: Touch targets
claude "Audit all clickable elements and ensure touch targets are at least 48x48px with adequate spacing between them"

# Fix: Font sizes
claude "Ensure all body text is at least 16px and no text requires zooming to read on mobile"
```

## Broken Link Fixes

```
# Fix: Find and fix broken internal links
claude "Scan all internal links in the codebase, identify any pointing to non-existent routes or pages, and either update the URL or remove the link"

# Fix: Add 404 page
claude "Create a custom 404 page that includes: a friendly error message, search functionality, links to popular pages, and proper HTTP 404 status code"
```

## Bulk Operations

```
# Fix: Site-wide meta tag audit and fix
claude "Audit every page in this project for SEO issues: missing/duplicate titles, missing meta descriptions, missing canonicals, missing alt text, heading hierarchy problems. Fix all issues found"

# Fix: Full schema implementation
claude "Implement comprehensive schema markup across the entire site: Organization on homepage, Article on blog posts, Product on product pages, BreadcrumbList on all pages, FAQ where applicable"
```
