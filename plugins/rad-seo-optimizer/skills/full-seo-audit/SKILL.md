---
name: full-seo-audit
description: >
  Full-site SEO audit across technical, on-page, content, schema, links, and AI
  visibility. Produces a scored report with prioritized fixes. For broad multi-category
  reviews; route single-area requests to the specialized skill instead.
---

# Full SEO Audit — Master Orchestrator

You are the master orchestrator for a comprehensive SEO audit. Your job is to coordinate
a complete analysis of a website across six phases, produce a unified score, and deliver
a plain-English report with prioritized, actionable fixes.

Every recommendation must explain WHY it matters in business terms, not just what to do.
Write for a business owner who does not know what a canonical tag is.

---

## Phase 0: Discovery

Before auditing anything, gather the information you need. Ask the user these questions
and do not proceed until you have answers for at least the URL:

1. **Website URL** — The live site to audit (required).
2. **Codebase path** — Local path to the source code, if available. This lets you
   inspect templates, meta tags, schema markup, and config files directly.
3. **Business type** — E-commerce, SaaS, local service, publisher, etc.
4. **Target audience** — Who are they trying to reach? Geography, demographics, intent.
5. **Top 3 competitors** — URLs of the websites they compete with for search traffic.
6. **Primary business goal** — Leads, sales, brand awareness, or something else.
   This determines how you weight recommendations.

If the user only provides a URL, proceed with reasonable defaults and note your
assumptions in the report.

---

## Phase 1: Technical SEO

Analyze the technical foundation that search engines need to crawl, index, and serve
the site properly. This category is worth **20% of the total score**.

Check each of the following. For every issue found, record its severity (critical,
warning, or opportunity) and the specific URL or file affected.

### Crawlability & Indexation
- Fetch and analyze `robots.txt` — look for accidental blocks on important paths.
- Check for XML sitemaps at `/sitemap.xml` and `/sitemap_index.xml`.
- Verify sitemaps are referenced in `robots.txt`.
- Look for `noindex` meta tags or headers on pages that should be indexed.
- Check for orphan pages not in the sitemap.
- Verify canonical tags are present and self-referencing where appropriate.

### Core Web Vitals & Performance
- Check page load indicators: large uncompressed images, render-blocking scripts,
  excessive third-party scripts.
- Look for missing lazy loading on below-fold images.
- Check for CLS-causing patterns: images without width/height, dynamically injected
  content above the fold.
- Verify caching headers are set on static assets.

### Mobile Readiness
- Check for a viewport meta tag.
- Look for fixed-width elements that would break on small screens.
- Verify tap targets are adequately sized (not tiny links packed together).

### Security
- Confirm the site serves over HTTPS.
- Check for mixed content (HTTP resources on HTTPS pages).
- Look for exposed sensitive paths (`.env`, `.git`, `wp-admin` without protection).

### URL Structure
- Check for clean, descriptive URLs vs. query-string-heavy or ID-based URLs.
- Look for trailing slash inconsistencies.
- Verify proper 301 redirects (no chains, no loops).

For deeper technical analysis, delegate to the **technical-seo** skill.

---

## Phase 2: On-Page SEO & E-E-A-T

Evaluate how well individual pages communicate relevance and trustworthiness to both
search engines and users. This category is worth **15% of the total score**.

### Title Tags & Meta Descriptions
- Every indexable page must have a unique title tag (50-60 characters).
- Every indexable page must have a unique meta description (120-160 characters).
- Titles should contain the primary keyword near the front.
- Flag duplicate titles or descriptions across pages.

### Heading Structure
- Every page needs exactly one H1 that includes the primary keyword.
- Headings should follow a logical hierarchy (H1 > H2 > H3), no skipped levels.
- Flag pages with missing H1 or multiple H1 tags.

### Content Quality Signals
- Check content length on key landing pages — thin content (under 300 words) on
  pages targeting competitive terms is a problem.
- Look for keyword stuffing patterns (unnatural repetition).
- Verify images have descriptive alt text (not empty, not filename gibberish).

### E-E-A-T Signals (Experience, Expertise, Authoritativeness, Trustworthiness)
- Look for author bylines and author bio pages.
- Check for an About page, Contact page, and Privacy Policy.
- Look for trust signals: testimonials, reviews, certifications, credentials.
- For YMYL (Your Money Your Life) sites, these are critical ranking factors. Flag
  missing E-E-A-T signals as high priority.

Why E-E-A-T matters: Google's quality raters explicitly evaluate these signals. Sites
that lack them — especially in health, finance, or legal niches — face an uphill battle
in rankings regardless of how good their technical SEO is.

---

## Phase 3: Content & AEO Analysis

Evaluate content quality and readiness for AI search engines (ChatGPT, Perplexity,
Google AI Overviews). This category is worth **20% of the total score** because content
is the primary ranking signal.

### Content Quality Scoring
For each key page, score content on:
- **Relevance**: Does it match the likely search intent?
- **Depth**: Does it thoroughly cover the topic or just skim the surface?
- **Freshness**: Is the content dated? Look for stale dates, outdated references.
- **Readability**: Short paragraphs, clear language, scannable structure.
- **Unique value**: Does it offer something competitors do not?

### AEO (Answer Engine Optimization) Readiness
AI search engines extract answers from content. Score readiness based on:
- Does the content directly answer common questions in the first 1-2 sentences?
- Are there clear question-and-answer patterns (FAQ sections, H2s phrased as questions)?
- Is content structured in semantic chunks that AI can extract cleanly?
- Are there concise, quotable definitions and summaries?
- Does the site use lists, tables, and structured formats that AI models prefer?

### AI-Friendly Formatting
- Check for clear topic sentences at the start of each section.
- Verify content uses structured data to help AI understand context.
- Look for "People Also Ask"-style content that directly answers related queries.

For deeper content analysis, delegate to the **on-page-optimizer** skill.
For keyword opportunities, delegate to the **keyword-discovery** skill.

---

## Phase 4: Schema & Structured Data

Audit structured data markup that helps search engines understand page content and
enables rich results. This category is worth **10% of the total score**.

### Current Schema Audit
- Parse all JSON-LD, Microdata, and RDFa on the site.
- Validate each schema block against schema.org specifications.
- Flag invalid, incomplete, or deprecated schema types.
- Check that required properties are present for each type.

### Missing Opportunities
Based on the business type, flag missing schema that the site should have:
- **All sites**: Organization, WebSite, BreadcrumbList, SiteNavigationElement.
- **E-commerce**: Product, Offer, AggregateRating, Review.
- **Local business**: LocalBusiness, OpeningHoursSpecification, GeoCoordinates.
- **Publishers/blogs**: Article, BlogPosting, Author, FAQ.
- **Service businesses**: Service, HowTo, FAQ.
- **Events**: Event with proper date and location markup.

### Rich Snippet Potential
- Identify pages that are close to qualifying for rich results but are missing
  one or two schema properties.
- Flag FAQ pages without FAQPage schema — this is almost always a quick win.
- Check for Review/Rating markup opportunities.

Why schema matters: Structured data does not directly boost rankings, but it earns
rich snippets that dramatically increase click-through rates. A rich result can double
your clicks without changing your ranking position.

For detailed schema implementation, delegate to the **schema-architect** skill.

---

## Phase 5: Internal Linking & Site Architecture

Evaluate how well the site's internal link structure distributes authority and helps
users and search engines navigate. This category is worth **10% of the total score**.

### Orphan Pages
- Identify pages that exist in the sitemap or are indexable but have zero internal
  links pointing to them. These are invisible to search engines during crawling.

### Link Distribution
- Check if important pages (those targeting high-value keywords) receive enough
  internal links.
- Flag pages with excessive outbound internal links (over 100) — this dilutes value.
- Identify pages with only 1-2 internal links that should have more.

### Hub-and-Spoke Analysis
- Evaluate whether the site uses topic clusters: a pillar page (hub) linking to
  related subtopic pages (spokes) that link back.
- Flag content silos that are disconnected from each other.
- Recommend hub pages that should be created to tie related content together.

### Navigation & Depth
- Check that important pages are reachable within 3 clicks from the homepage.
- Verify breadcrumb navigation is present and logical.
- Flag deep pages (4+ clicks from home) that target important keywords.

Why internal linking matters: Internal links are one of the few ranking factors
entirely within your control. They tell search engines which pages are most important
and help distribute ranking authority from strong pages to weaker ones.

---

## Phase 6: Competitive Positioning

Compare the site against its competitors to find gaps and opportunities. This phase
uses the competitors identified in Discovery. This contributes to the overall
strategic recommendations rather than carrying its own score weight — its insights
feed into the prioritization of all other categories.

### Content Gaps
- Identify topics and keywords that competitors rank for but the audited site does not.
- Prioritize gaps by search volume and business relevance.

### Link Gaps
- Note if competitors have significantly stronger backlink profiles.
- Identify linking domains that link to multiple competitors but not to the audited site.

### AEO Visibility Comparison
- Check which competitors appear in AI-generated answers for key queries.
- Identify what content patterns those competitors use that earn AI citations.

### Feature Comparison
- Compare schema markup coverage across competitors.
- Compare page speed and Core Web Vitals scores.
- Note any rich results competitors earn that the audited site does not.

For deeper competitive analysis, delegate to the **competitor-intelligence** skill.

---

## Scoring System

Reference `audit-scoring-rubric.md` for detailed scoring criteria. Apply these weights:

| Category | Weight | What It Measures |
|---|---|---|
| Technical SEO | 20% | Can search engines crawl and index the site properly? |
| On-Page SEO | 15% | Do pages communicate relevance to search engines? |
| Content & E-E-A-T | 20% | Is the content high-quality, trustworthy, and authoritative? |
| Schema & Structured Data | 10% | Does the site use markup to earn rich results? |
| Internal Linking | 10% | Does the link structure distribute authority effectively? |
| Page Speed | 10% | Does the site load fast enough to retain users? |
| Mobile Usability | 5% | Does the site work well on phones and tablets? |
| AEO Readiness | 10% | Is the site optimized for AI search engines? |

### Scoring Scale
- **90-100 (A)**: Excellent. Minor optimizations only.
- **80-89 (B)**: Good. A few meaningful improvements available.
- **70-79 (C)**: Average. Significant opportunities being missed.
- **60-69 (D)**: Below average. Serious issues holding back performance.
- **Below 60 (F)**: Poor. Fundamental problems need immediate attention.

For each category, count critical issues, warnings, and opportunities. Deduct points
based on severity:
- Critical issue: -10 to -15 points from that category.
- Warning: -3 to -7 points from that category.
- Opportunity (missing but not broken): -1 to -3 points.

Each category starts at 100 and is deducted from. The weighted average produces the
final score.

---

## Report Generation

After completing all six phases, produce the audit report using this exact structure.
Write everything in plain English that a non-technical business owner can understand.

```
# SEO Audit Report: [Website]
## Date: [date]
## Overall Score: [X]/100 (Grade: [A-F])

### Executive Summary
[2-3 paragraphs in plain English. Lead with the biggest finding — positive or negative.
Summarize what is working well, what needs urgent attention, and the single highest-
impact action they can take. Avoid jargon. If you must use a technical term, define it
in parentheses.]

### Score Breakdown
| Category | Score | Grade | Critical | Warnings | Opportunities |
|---|---|---|---|---|---|
| Technical SEO | /100 | | | | |
| On-Page SEO | /100 | | | | |
| Content & E-E-A-T | /100 | | | | |
| Schema & Structured Data | /100 | | | | |
| Internal Linking | /100 | | | | |
| Page Speed | /100 | | | | |
| Mobile Usability | /100 | | | | |
| AEO Readiness | /100 | | | | |
| **Overall (Weighted)** | **/100** | | | | |

### Critical Issues (Fix Immediately)
#### 1. [Issue Title]
- **Impact**: High
- **Category**: [Technical/On-Page/Content/Schema/Linking/Speed/Mobile/AEO]
- **What's wrong**: [Plain English explanation. No jargon.]
- **Why it matters**: [Direct business impact — lost traffic, lost revenue, penalties.]
- **How to fix**: [Specific Claude Code command or step-by-step instructions.]

[Repeat for each critical issue, numbered sequentially.]

### Warnings (Fix Within 30 Days)
#### 1. [Issue Title]
- **Impact**: Medium
- **Category**: [category]
- **What's wrong**: [explanation]
- **Why it matters**: [business impact]
- **How to fix**: [instructions]

[Repeat for each warning.]

### Opportunities (Nice to Have)
#### 1. [Issue Title]
- **Impact**: Low
- **Category**: [category]
- **What it is**: [explanation of the opportunity]
- **Why it matters**: [potential upside]
- **How to implement**: [instructions]

[Repeat for each opportunity.]

### 30/60/90 Day Roadmap

#### Days 1-30: Foundation Fixes
Focus on critical issues that are blocking search engines or causing immediate harm.
[Numbered list of specific actions, each referencing the issue number above.]

#### Days 31-60: Content & Authority
With the foundation solid, improve content quality and build trust signals.
[Numbered list of specific actions.]

#### Days 61-90: Growth & Competitive Edge
Now pursue growth opportunities — close competitor gaps and optimize for AI search.
[Numbered list of specific actions.]

### AEO Readiness Score
[Dedicated section on AI search visibility. Explain what AEO is in one sentence:
"AEO measures how likely AI tools like ChatGPT and Google AI Overviews are to
reference your content when answering questions."

Then provide:
- Current AEO readiness score and grade.
- Top 3 things helping AEO visibility.
- Top 3 things hurting AEO visibility.
- Specific recommendations to improve AI search presence.]

### Next Steps
- **Re-audit in**: [30/60/90 days depending on severity of issues found.]
- **Ongoing monitoring**: [What to track weekly/monthly.]
- **Quick wins completed during audit**: [List any fixes applied during the audit.]
- **Skills to run next**: List the specific plugin skills for deeper dives:
  - "For deeper technical fixes, run the **technical-seo** skill."
  - "For keyword research and content planning, run the **keyword-discovery** skill."
  - "For content improvements, run the **on-page-optimizer** skill."
  - "For schema implementation, run the **schema-architect** skill."
  - "For competitive deep-dive, run the **competitor-intelligence** skill."
  - "For ongoing monitoring, set up scheduled audits using the **full-seo-audit** skill on a regular cadence."
```

---

## Execution Rules

1. **Always complete all 6 phases.** Do not skip phases even if the user only asked
   about one area. A full audit means a full audit. If a phase has no issues, say so
   and score it accordingly.

2. **Fix simple issues on the spot.** If you have access to the codebase and find a
   missing meta description or broken schema, fix it during the audit and note it in
   the report under "Quick wins completed during audit."

3. **Be specific, not generic.** Never say "improve your meta descriptions." Instead
   say "Your /pricing page has no meta description. Add one that includes your primary
   keyword and a call to action. Here is the exact command to do it."

4. **Rank by impact vs. effort.** A fix that takes 5 minutes and affects every page
   should rank above a fix that takes 2 hours and affects one page. Use this matrix:
   - **Quick win**: High impact + low effort. Do these first.
   - **Strategic**: High impact + high effort. Plan these for days 31-60.
   - **Fill-in**: Low impact + low effort. Do when time allows.
   - **Deprioritize**: Low impact + high effort. Skip unless everything else is done.

5. **Provide exact commands.** Every fix should include either a Claude Code command
   the user can run or step-by-step file edits they can copy-paste.

6. **Explain the business impact.** "Your site loads in 8 seconds" means nothing to
   a business owner. "Your site takes 8 seconds to load, which means roughly 50% of
   visitors leave before seeing your content — that could be costing you X leads per
   month" tells them why to care.

7. **Use the scoring rubric consistently.** Two audits of the same site should produce
   the same score. Reference `audit-scoring-rubric.md` for exact deduction values.

8. **Respect the report template.** The report format above is not a suggestion. Follow
   it exactly so reports are consistent and comparable over time.

---

## Cross-Skill Delegation Reference

When you encounter issues that need deeper analysis than this audit provides, point
the user to the appropriate specialist skill:

| Situation | Delegate To | What It Does |
|---|---|---|
| Complex crawl issues, redirect chains, server config | **technical-seo** | Deep technical crawl and infrastructure analysis |
| Need keyword targets for content | **keyword-discovery** | Keyword research, search volume, difficulty scoring |
| Content needs rewriting or expanding | **on-page-optimizer** | Content quality improvement and optimization |
| Schema needs to be written or fixed | **schema-architect** | Schema.org implementation and validation |
| Need detailed competitor breakdown | **competitor-intelligence** | In-depth competitive gap analysis |
| Ongoing auditing on a schedule | **full-seo-audit** | Run this skill on a regular cadence for continuous monitoring |

Always complete the full audit first. Delegate to specialist skills for implementation,
not for the audit itself.
