---
name: competitor-intelligence
description: >
  This skill should be used when the user says "competitor analysis", "who ranks for",
  "what are competitors doing", "competitive audit", "compare my SEO", "competitor gap",
  or wants to understand how they stack up against competitors in search. Covers content gaps,
  technical comparison, backlink profiles, SERP features, and AI search visibility.
argument-hint: "[competitor URL or domain]"
---

# Competitor Intelligence Skill

Perform a comprehensive competitor SEO analysis that covers traditional ranking factors
and AI/LLM search visibility. Every finding includes a concrete, prioritized action.

---

## Pre-Flight: Gather Inputs

Before starting, collect the following from the user. Do not proceed until you have all three.

1. **Target site URL** — the domain to benchmark.
2. **2-3 known competitors** — direct business competitors the user already knows about.
3. **5-10 target keywords** — the queries they most want to win.

If the user provides only a URL, ask:
> "Provide 2-3 competitors already known, plus 5-10 keywords to rank for.
> The analysis will also discover *digital* competitors — the sites actually beating the
> target site in search, which are often different from direct business competitors."

---

## Phase 1: Competitor Identification

### 1A — Confirm Known Competitors

Accept the 2-3 competitors the user provides. Validate each URL loads correctly using
WebFetch (head request only; do not parse full pages yet).

### 1B — Discover Digital Competitors

Digital competitors are sites that rank in the top 10 for the user's target keywords,
regardless of whether they are direct business rivals. Blogs, aggregators, and tool sites
often fall into this category.

For each target keyword:

```
WebSearch("[keyword]")
```

Collect every domain that appears in the top 10 across all keyword searches.
Rank domains by how many target keywords they appear for. The top 3-5 recurring domains
(excluding the user's own site) are the digital competitors.

Present a combined list:

| # | Competitor | Type | Overlapping Keywords |
|---|-----------|------|---------------------|
| 1 | example.com | Business + Digital | 8 of 10 |
| 2 | blog-rival.com | Digital only | 6 of 10 |
| 3 | toolsite.io | Digital only | 5 of 10 |

Ask the user to confirm which competitors to include in the full analysis (recommend 3).

---

## Phase 2: Content Gap Analysis

For each confirmed competitor, discover what content they publish that the user does not.

### 2A — Map Competitor Top Pages

Use WebSearch to find each competitor's most visible pages:

```
WebSearch("site:competitor.com [keyword]")
```

Run this for every target keyword. Also run a broad search:

```
WebSearch("site:competitor.com")
```

Build a list of each competitor's top-performing URLs and the topics they cover.

### 2B — Identify Content Gaps

Compare the competitor topic lists against the user's site. A content gap exists when
a competitor covers a topic that the user does not.

For each gap, classify it:

- **Missing entirely** — user has no page on this topic.
- **Thin coverage** — user has a page but it is significantly less comprehensive.
- **Format gap** — competitor uses a superior format (calculator, interactive tool, video,
  infographic) while user has only text.

### 2C — Assess Content Depth

For the top 5 content gaps, fetch the competitor's page:

```
WebFetch("https://competitor.com/their-page")
```

Evaluate:
- Word count (approximate from fetched content)
- Heading structure (H2/H3 depth)
- Use of images, tables, or embedded media
- Presence of original data, quotes, or case studies
- Internal linking density

### 2D — Identify 10x Content Opportunities

A "10x opportunity" is a topic where:
1. Competitors rank but their content is mediocre (thin, outdated, or poorly structured).
2. The user has domain expertise or data that could produce something significantly better.
3. Search volume justifies the investment.

Flag the top 3 10x opportunities with a brief rationale for each.

---

## Phase 3: Technical Comparison

Fetch the homepage and one key landing page from each competitor to benchmark technical SEO.

### 3A — Page Speed

Use WebFetch to load each page. Record approximate load behavior. Note any indicators of
performance optimization (minified assets, lazy-loaded images, CDN usage).

Recommend specific improvements if the user's site is slower.

### 3B — Mobile Experience

Check the fetched HTML for:
- Viewport meta tag presence
- Responsive CSS indicators (media queries, flexible grids)
- Touch-friendly element sizing
- Mobile-specific structured data

### 3C — Schema Markup

Search each page's HTML for JSON-LD or microdata:

```
Look for: <script type="application/ld+json">
```

Catalog which schema types each competitor implements:
- Organization / LocalBusiness
- Article / BlogPosting
- Product / Review
- FAQ / HowTo
- BreadcrumbList
- VideoObject

Flag any schema types competitors use that the user does not.

### 3D — URL Structure

Compare URL patterns across competitors:

| Site | URL Pattern | Hierarchy Depth | Keyword in URL |
|------|------------|-----------------|----------------|
| user.com | /blog/post-title | 2 levels | Sometimes |
| comp1.com | /guides/category/topic | 3 levels | Always |

Note best practices the user should adopt.

---

## Phase 4: Link Gap Analysis

Identify who links to competitors but not the user, and how to earn those links.

### 4A — Discover Competitor Backlink Sources

For each competitor, search for pages that reference them:

```
WebSearch('"competitor.com" -site:competitor.com')
WebSearch('"competitor brand name" recommendation OR review OR resource')
```

Collect referring domains. Cross-reference across competitors to find sites that link to
multiple competitors but not the user — these are the highest-value targets.

### 4B — Classify Link Opportunities

For each opportunity, assign:

- **Source type**: editorial, resource page, directory, guest post, mention
- **Relevance**: how topically related the linking site is (High / Medium / Low)
- **Feasibility**: how likely the user can earn a link (High / Medium / Low)
- **Suggested tactic**: the specific approach to earn the link

Refer to `link-building-tactics.md` in the plugin knowledge base for detailed playbooks
on each tactic.

### 4C — Prioritize

Sort opportunities by a combined score of (relevance x feasibility). Present the top 10.

---

## Phase 5: SERP Feature Ownership

Map who currently owns SERP features for each target keyword.

### 5A — Featured Snippets

For each target keyword, run:

```
WebSearch("[keyword]")
```

Note whether a featured snippet appears and who holds it. Record the snippet format
(paragraph, list, table) and approximate content.

### 5B — Rich Results

Check search results for:
- FAQ accordions
- HowTo step displays
- Review stars
- Product cards
- Video carousels
- Image packs

Map which competitors own each type for which keywords.

### 5C — People Also Ask (PAA)

Collect PAA questions that appear for target keywords. Note which competitors' pages
are surfaced as answers. These questions are direct content brief opportunities.

### 5D — Knowledge Panel Presence

Check whether any competitor has a knowledge panel. If the user does not have one,
note the steps to establish one (Google Business Profile, Wikidata, structured data).

### 5E — Opportunity Map

Build a table:

| Keyword | Feature | Current Owner | User Eligible? | Action to Win |
|---------|---------|--------------|----------------|---------------|
| best crm | Featured snippet (list) | comp1.com | Yes | Add H2 list format |
| crm pricing | FAQ rich result | comp2.com | Yes | Add FAQPage schema |

---

## Phase 6: LLM / AEO Visibility Comparison

This is the highest-value differentiator. AI-powered search surfaces are growing fast
and most competitors are not optimizing for them yet.

### 6A — Query AI Platforms

For each target keyword, run queries against available AI search surfaces using WebSearch
with platform-specific searches where possible:

- **Google AI Overviews**: Check if an AI Overview appears in Google results and who is cited.
- **Perplexity**: Search for mentions of competitors vs. the user in Perplexity-style results.
- **ChatGPT / Claude**: Note general brand awareness — which brands are commonly associated
  with the target keywords in LLM training data.

Use searches like:

```
WebSearch("[keyword] site:perplexity.ai")
WebSearch("[keyword] AI overview")
WebSearch("[competitor brand] vs [user brand] [keyword]")
```

### 6B — Track Citations and Recommendations

For each platform and keyword, record:

| Platform | Keyword | Your Brand | Comp 1 | Comp 2 | Comp 3 |
|----------|---------|-----------|--------|--------|--------|
| Google AI Overview | best crm | Not cited | Cited | Cited | Not cited |
| Perplexity | crm software | Not mentioned | Recommended | Mentioned | Not mentioned |

### 6C — Analyze Why Competitors Get Cited

When a competitor is cited by an AI platform, investigate the likely reasons:

- **Authoritative source**: high domain authority, well-known brand
- **Consensus content**: says what most other sources agree on
- **Structured format**: clear definitions, lists, or tables that are easy for LLMs to extract
- **Unique data**: original research, statistics, or benchmarks that no one else publishes
- **Freshness**: recently updated content on a fast-moving topic

### 6D — Identify AI Search Gaps

Find keywords where no competitor is well-cited by AI platforms. These are low-competition
AEO opportunities. Also find keywords where the user could displace a weakly-cited
competitor by producing better-structured, more authoritative content.

### 6E — Build AEO Action Plan

For each AI search gap, recommend a specific action. Reference `aeo-playbook.md` in the
plugin knowledge base for detailed strategies on:

- Structuring content for LLM extraction
- Building entity authority for knowledge graphs
- Creating "consensus-plus" content that LLMs prefer to cite
- Earning mentions on platforms that LLMs use as training data

---

## Output Format

Compile all findings into a single report. Every finding must include a recommended action.

```
# Competitor Intelligence Report: [Your Site] vs. [Competitors]
# Generated: [Date]

## Executive Summary
[3-5 sentence overview of competitive position, biggest threats, and biggest opportunities]

## Competitor Overview
| Metric              | Your Site | Competitor 1 | Competitor 2 | Competitor 3 |
|---------------------|-----------|-------------|-------------|-------------|
| Type                |    —      | Business    | Digital     | Digital     |
| Keyword Overlap     |    —      | 8/10        | 6/10        | 5/10        |
| Content Depth       | [score]   | [score]     | [score]     | [score]     |
| Schema Types Used   | [count]   | [count]     | [count]     | [count]     |
| Est. Backlink Sources | [count] | [count]     | [count]     | [count]     |
| SERP Features Owned | [count]   | [count]     | [count]     | [count]     |
| AI Search Visibility | [level]  | [level]     | [level]     | [level]     |

## Content Gaps (Biggest Opportunities)
1. **[Topic]** — Competitor X has [content type/URL], you have nothing.
   Estimated traffic potential: [X visits/mo]. **Action**: [specific content to create].
2. ...
3. ...

## 10x Content Opportunities
1. **[Topic]** — Existing competitor content is [weakness]. You can win by [strategy].
2. ...
3. ...

## Technical SEO Comparison
| Factor          | Your Site | Comp 1 | Comp 2 | Comp 3 | Your Action           |
|-----------------|-----------|--------|--------|--------|-----------------------|
| Page Speed      | [rating]  | [rating]| [rating]| [rating]| [specific fix]       |
| Mobile UX       | [rating]  | [rating]| [rating]| [rating]| [specific fix]       |
| Schema Markup   | [types]   | [types] | [types] | [types] | [schemas to add]     |
| URL Structure   | [pattern] | [pattern]| [pattern]| [pattern]| [improvements]     |

## Link Opportunities
1. **[Referring Site]** — Links to Competitors A and B but not you.
   Type: [resource page]. **Tactic**: [specific outreach approach].
2. ...
(Top 10, sorted by feasibility x relevance)

## SERP Feature Opportunities
1. **[Keyword]** — Featured snippet held by [competitor]. Format: [list/table/paragraph].
   **Strategy**: [restructure content with H2 + list to win snippet].
2. **[Keyword]** — FAQ rich result held by [competitor].
   **Strategy**: [add FAQPage schema to existing page].
3. ...

## AI Search Visibility
| Platform          | Your Brand   | Comp 1      | Comp 2       | Comp 3      |
|-------------------|-------------|-------------|--------------|-------------|
| Google AI Overview | Not cited   | Cited       | Cited        | Not cited   |
| Perplexity        | Not mentioned| Recommended | Mentioned    | Not mentioned|
| General LLM Awareness | Low     | High        | Medium       | Low         |

### Why Competitors Win in AI Search
- Competitor 1: [reason — e.g., publishes original benchmarks that LLMs cite as data]
- Competitor 2: [reason — e.g., clear structured definitions that match consensus]

### Your AI Search Action Plan
1. **[Action]** — Target: [platform/keyword]. Expected impact: [rationale].
   See aeo-playbook.md section: [relevant section].
2. ...

## Prioritized Action Plan
Sorted by (Impact / Effort) ratio. Execute in this order.

| # | Action | Category | Impact | Effort | Timeline |
|---|--------|----------|--------|--------|----------|
| 1 | [action] | Content Gap | High | Low | 1 week |
| 2 | [action] | SERP Feature | High | Low | 2 days |
| 3 | [action] | AEO | High | Medium | 2 weeks |
| 4 | [action] | Link Gap | Medium | Medium | 3 weeks |
| 5 | [action] | Technical | Medium | Low | 1 day |
| ... | ... | ... | ... | ... | ... |
```

---

## Execution Notes

- **Be specific**: Never say "improve the content." Say "add a comparison table with
  pricing columns to the /crm-guide page, matching the format comp1.com uses at /pricing."
- **Cite sources**: When referencing a competitor's page, include the URL.
- **Quantify when possible**: Estimated traffic, word counts, number of backlinks.
- **Cross-reference plugin resources**: Point the user to `aeo-playbook.md` for AI search
  strategies and `link-building-tactics.md` for link acquisition playbooks.
- **Prioritize ruthlessly**: The action plan should have no more than 15 items. Rank them
  by the ratio of expected impact to required effort. Quick wins first.
- **Flag time-sensitive opportunities**: If a competitor's content is outdated or a SERP
  feature is weakly held, mark it as urgent.
- **Re-run quarterly**: Recommend the user re-run this analysis every 90 days to track
  progress and catch new competitor moves.
