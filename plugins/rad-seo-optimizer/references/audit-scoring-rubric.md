# SEO Audit Scoring Rubric

This rubric defines how the Ultimate SEO Optimizer calculates scores across all audit categories. The unified score (0-100) is a weighted composite of category scores.

## Category Weights

| Category | Weight | Rationale |
|----------|--------|-----------|
| Technical SEO | 20% | Foundation — if crawling/indexing fails, nothing else matters |
| On-Page SEO | 15% | Direct ranking signals — title, meta, headings, content |
| Content Quality & E-E-A-T | 20% | Google's helpful content system makes this critical |
| Schema & Structured Data | 10% | Rich snippets and AI-parseable content |
| Internal Linking | 10% | Authority distribution and crawl efficiency |
| Page Speed & Core Web Vitals | 10% | Page experience signal |
| Mobile & Accessibility | 5% | Mobile-first indexing compliance |
| AEO/GEO Readiness | 10% | AI search visibility — increasingly important |

## Severity Levels

Each issue found is classified by severity:

### Critical (blocks ranking)
- Site not indexable (robots.txt blocking, noindex on key pages)
- HTTPS not configured or mixed content
- Core Web Vitals failing (LCP > 4s, CLS > 0.25)
- Duplicate content without canonicalization
- No H1 tag or multiple H1s
- Missing title tags or meta descriptions on key pages
- Broken internal links to important pages
- Site penalized by Google (manual action)

### Warning (hurts ranking)
- Slow page speed (LCP 2.5-4s)
- Missing alt text on images
- Thin content (< 300 words on informational pages)
- No schema markup implemented
- Orphan pages with no internal links
- Redirect chains (3+ hops)
- Missing author bios on YMYL content
- No XML sitemap or incomplete sitemap
- Keyword cannibalization detected

### Opportunity (could improve ranking)
- Schema types not yet implemented that could trigger rich snippets
- Internal linking opportunities not exploited
- Content gaps vs. competitors
- Long-tail keywords not targeted
- AEO-unfriendly content formatting
- Missing FAQ schema on question-answering pages
- No breadcrumb navigation/markup
- Images not optimized (format, compression, dimensions)

### Passing (no action needed)
- Check passes all criteria — note what's working well

## Scoring Formula

### Per-Category Score (0-100)
```
category_score = 100 - (critical_count * 15) - (warning_count * 5) - (opportunity_count * 2)
minimum: 0
```

### Unified Score
```
unified_score = sum(category_score * category_weight for each category)
```

### Grade Mapping
| Score | Grade | Status |
|-------|-------|--------|
| 90-100 | A+ | Excellent — maintain and optimize |
| 80-89 | A | Strong — minor improvements available |
| 70-79 | B | Good — targeted fixes will yield gains |
| 60-69 | C | Average — significant optimization opportunity |
| 50-59 | D | Below average — systematic improvements needed |
| 0-49 | F | Critical — fundamental issues blocking performance |

## Priority Matrix

Each fix recommendation is scored on two dimensions:

### Impact (1-10)
How much will fixing this improve rankings?
- **9-10**: Direct ranking factor with immediate effect (e.g., fixing noindex, adding title tags)
- **7-8**: Strong ranking signal (e.g., Core Web Vitals, internal linking overhaul)
- **5-6**: Moderate signal (e.g., schema markup, image optimization)
- **3-4**: Indirect benefit (e.g., better UX, breadcrumbs)
- **1-2**: Minor polish (e.g., favicon, cosmetic improvements)

### Effort (Quick Fix / Moderate / Project)
- **Quick Fix** (< 30 minutes): Meta tag updates, alt text, robots.txt fix, single redirect
- **Moderate** (1-4 hours): Schema implementation, content optimization, internal linking pass
- **Project** (1+ days): Content creation, site architecture overhaul, Core Web Vitals fixes, link building campaign

### Priority Ranking
```
priority = impact_score / effort_multiplier
where effort_multiplier: quick_fix=1, moderate=2, project=4
```

Always present fixes in priority order: highest impact, lowest effort first.

## Comparison Benchmarks

When comparing against competitors, use these benchmarks:
- **Page speed**: Compare LCP, INP, CLS against top 3 ranking competitors
- **Content depth**: Word count, topic coverage, unique insights vs. competitors
- **Backlink profile**: Domain authority, referring domains, link quality vs. competitors
- **Schema coverage**: Schema types implemented vs. competitors
- **AEO readiness**: AI citation frequency vs. competitors
