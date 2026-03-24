# Technical SEO — Platform-Specific Fix Commands

This reference contains framework-specific fix commands for Core Web Vitals, mobile compliance, and JavaScript SEO issues. Consult this when the technical-seo skill identifies issues that need platform-tailored remediation.

---

## Core Web Vitals: LCP Fix Commands

| Framework | Command |
|-----------|---------|
| Next.js | `claude "Use next/image with priority prop on the hero image. Enable next/font to eliminate font-swap delay. Move non-critical CSS to dynamic imports."` |
| React | `claude "Preload the hero image in index.html. Code-split below-the-fold components with React.lazy. Inline critical CSS with critters."` |
| WordPress | `claude "Install and configure a caching plugin. Add preload tags for hero images in header.php. Defer non-critical plugins."` |
| Static HTML | `claude "Convert hero images to WebP. Add preload link tags. Inline above-the-fold CSS. Defer all JS with the defer attribute."` |

---

## Core Web Vitals: INP Fix Commands

| Framework | Command |
|-----------|---------|
| Next.js | `claude "Wrap expensive event handlers in startTransition. Move analytics to a web worker. Add the Interaction to Next Paint diagnostic to next.config.js."` |
| React | `claude "Use useTransition for non-urgent state updates. Debounce search input handlers to 150 ms. Lazy-load modal content."` |
| WordPress | `claude "Defer third-party scripts. Replace jQuery event handlers with vanilla JS. Add async to non-critical enqueued scripts."` |
| Static HTML | `claude "Move analytics scripts to defer. Break long tasks into chunks using scheduler.yield(). Remove unused JS."` |

---

## Core Web Vitals: CLS Fix Commands

| Framework | Command |
|-----------|---------|
| Next.js | `claude "Add width and height to all next/image components. Configure next/font with adjustFontFallback. Reserve ad slot space with min-height in CSS modules."` |
| React | `claude "Set explicit dimensions on every img and iframe. Use Skeleton components for async content. Apply will-change: transform to animated elements."` |
| WordPress | `claude "Add missing width/height attributes to all img tags in theme templates. Preload the primary web font. Set min-height on ad containers in style.css."` |
| Static HTML | `claude "Add width and height attributes to every img tag. Add aspect-ratio CSS for responsive images. Reserve space for ad containers."` |

---

## Mobile-First Fix Commands

### Viewport Meta Tag
```
claude "Add the viewport meta tag to every HTML template. Remove maximum-scale and user-scalable=no restrictions."
```

### Mobile Content Parity
```
claude "Find all CSS rules that hide content on mobile. Replace display:none with responsive layout that preserves content. Ensure structured data is in the server-rendered HTML."
```

### Touch Target Sizing
```
claude "Set min-height: 48px and min-width: 48px on all buttons and link areas. Add padding to inline links in body text. Ensure 8px gap between adjacent tap targets."
```

### Font Sizes
```
claude "Set base font-size to 16px on the body element. Ensure all text containers use max-width: 100% and overflow-wrap: break-word."
```

### Horizontal Scrolling
```
claude "Add max-width: 100% to all images. Wrap wide tables in a div with overflow-x: auto. Replace fixed-width elements with responsive equivalents."
```

---

## JavaScript SEO: Server-Side Rendering Fix Commands

| Framework | Command |
|-----------|---------|
| Next.js | `claude "Convert client-side pages to use getStaticProps or getServerSideProps. Ensure all pages export server-rendered HTML with full content."` |
| React | `claude "Set up server-side rendering with ReactDOMServer or migrate to a framework like Next.js. As a quick fix, add react-snap for static pre-rendering."` |
| WordPress | `claude "Verify that theme content is in PHP templates, not injected by JavaScript. Deactivate plugins that replace server-rendered content with JS widgets."` |

### Dynamic Rendering Detection
```
claude "Audit the dynamic rendering layer. Compare Googlebot-rendered output to browser-rendered output. Flag any content discrepancies. Plan migration to native SSR."
```

### JavaScript-Dependent Content
```
claude "Move critical content (prices, reviews, article text) to the server-rendered HTML. Use progressive enhancement: load the HTML first, then hydrate interactivity."
```

### Lazy-Loading Implementation
```
claude "Remove loading=lazy from the first 2 images (above the fold). Add loading=lazy to all other images. Ensure lazy-loaded images have width and height attributes."
```

---

## Security Fix Commands

### HTTPS Everywhere
```
claude "Find all HTTP resource references (images, scripts, stylesheets). Rewrite them to HTTPS or protocol-relative URLs. Verify the 301 redirect from HTTP to HTTPS in the server config."
```

### HSTS Header
```
claude "Add Strict-Transport-Security: max-age=31536000; includeSubDomains; preload to the server configuration. For Next.js, add it to next.config.js headers. For WordPress, add it to .htaccess."
```

### Content-Security-Policy
```
claude "Generate a Content-Security-Policy header based on the site's actual resource origins. Start with a report-only policy, then enforce after verifying no breakage."
```

### Sensitive File Exposure
```
claude "Add deny rules to the server config for .env, .git, and backup files. Remove any sensitive files from the public directory. Add them to .gitignore."
```

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
