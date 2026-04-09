---
name: aeo-optimizer
description: >
  AEO, AI visibility, AI search optimization, generative engine optimization, "how does my
  brand appear in AI", LLM seeding, AI citations, answer engine optimization, brand presence
  in ChatGPT/Perplexity/Google AI Overviews.
argument-hint: "[brand name or URL]"
---

# AEO Optimizer — AI Engine Optimization Skill

Make the target brand discoverable, recommended, and accurately represented by AI search engines.

Traditional SEO gets a site ranked on Google. AEO gets the brand **recommended by AI**. When a user asks ChatGPT "What's the best project management tool?" or Perplexity "Compare CRM platforms" — AEO determines whether the brand appears, how it is described, and whether it is positioned favorably.

---

## Phase 1: AI Visibility Audit

Score the target brand across six dimensions. Each dimension receives a 0-10 rating. The composite AEO Score (0-60) establishes the baseline.

### Scoring Dimensions

| # | Dimension | What It Measures | Score Range |
|---|-----------|-----------------|-------------|
| 1 | **Presence** | Is the brand mentioned at all in AI responses for target keywords? | 0-10 |
| 2 | **Accuracy** | Is the information AI shares factually correct and current? | 0-10 |
| 3 | **Sentiment** | Is the tone positive, neutral, or negative when discussing the brand? | 0-10 |
| 4 | **Position** | Is the brand mentioned first, or buried among alternatives? | 0-10 |
| 5 | **Completeness** | Does the AI capture the full value proposition and key differentiators? | 0-10 |
| 6 | **Consistency** | Do different AI platforms agree on what the brand is and does? | 0-10 |

### Audit Method

Use `WebSearch` to query each major AI platform with brand-relevant prompts. Run a minimum of 10 queries per platform.

**Query templates to test:**

```
"What is [BRAND]?"
"Best [CATEGORY] tools in 2026"
"[BRAND] vs [COMPETITOR]"
"Is [BRAND] worth it?"
"[BRAND] pricing and features"
"What are the pros and cons of [BRAND]?"
"Alternatives to [COMPETITOR] for [USE CASE]"
"[BRAND] review"
"How does [BRAND] compare to [COMPETITOR]?"
"What [CATEGORY] tool should I use for [SPECIFIC NEED]?"
```

**Platforms to query:**
- Google AI Overviews (search with AI mode)
- ChatGPT (web browsing enabled)
- Perplexity AI
- Claude (with web search)
- Microsoft Copilot / Bing Chat

### Generating the Scorecard

After collecting responses, produce a scorecard:

```
============================
  AEO VISIBILITY SCORECARD
============================
Brand: [BRAND NAME]
Date:  [DATE]
Target Keywords: [LIST]

Presence:    [X]/10  — Mentioned in [Y]% of AI responses
Accuracy:    [X]/10  — [Y] factual errors found across [Z] responses
Sentiment:   [X]/10  — [POS]% positive, [NEU]% neutral, [NEG]% negative
Position:    [X]/10  — Listed first in [Y]% of recommendation queries
Completeness:[X]/10  — [Y]/[Z] key features/differentiators captured
Consistency: [X]/10  — [Y]% agreement across platforms

COMPOSITE AEO SCORE: [TOTAL]/60
Rating: [Invisible|Emerging|Visible|Strong|Dominant]

  0-12  = Invisible  (AI doesn't know you exist)
  13-24 = Emerging   (Sporadic, often inaccurate mentions)
  25-36 = Visible    (Present but not preferred)
  37-48 = Strong     (Regularly recommended, mostly accurate)
  49-60 = Dominant   (Default recommendation, highly accurate)
```

Record every factual error, missing feature, negative framing, or omission. These become the fix list for subsequent phases.

---

## Phase 2: LLM Seeding Strategy

AI models learn from the open web. Control where and how brand information appears to influence what LLMs absorb.

### WHERE to Publish (Source Priority)

Publish brand-relevant content on these platforms, ordered by LLM training influence. Replace [BRAND] with the target brand name throughout:

| Priority | Platform | Why It Matters | Action |
|----------|----------|---------------|--------|
| 1 | **The Brand Website** | Primary source of truth. Must be crawlable, well-structured, fast. | Ensure clean HTML, proper schema markup, no JS-only rendering. |
| 2 | **Wikipedia / Wikidata** | Highest-authority factual source for all LLMs. | Create or improve the Wikipedia page. Add Wikidata entity. |
| 3 | **Reddit** | Massively overweighted in LLM training data. Authentic discussions. | Engage genuinely in relevant subreddits. Never astroturf. |
| 4 | **Stack Overflow / Quora** | Q&A format is ideal for LLM extraction. | Answer questions where your product is genuinely the solution. |
| 5 | **Medium / Substack / LinkedIn** | Long-form platforms LLMs crawl heavily. | Publish thought leadership, case studies, tutorials. |
| 6 | **Industry Publications** | Authoritative third-party validation. | Guest posts, contributed articles, expert commentary. |
| 7 | **Review Platforms** (G2, Trustpilot, Capterra) | LLMs use reviews for sentiment and feature extraction. | Actively collect reviews. Respond to all reviews. |
| 8 | **GitHub** | Critical for developer/technical products. | Maintain active repos, quality READMEs, community engagement. |
| 9 | **News Sites** | Recency signal. LLMs with web access pull recent news. | Digital PR, press releases, newsworthy launches. |

### WHAT Content Format to Use

These content formats are disproportionately extracted and cited by LLMs:

**1. Structured "Best Of" Lists**
```markdown
## Best [Category] Tools in 2026
### 1. [Your Brand] — Best for [Specific Use Case]
**Why we chose it:** [2-sentence verdict]
**Key features:** [Bullet list]
**Pricing:** [Clear pricing info]
**Best for:** [Target audience]
```
Always include testing methodology to establish authority.

**2. Comparison Tables**
Create brand-vs-brand comparison content with clear verdicts. LLMs love extracting tabular data.

**3. FAQ-Style Content**
Q&A is training data gold. Structure content as:
```markdown
## What is [Brand]?
[Brand] is [direct 1-sentence definition]. It [key differentiator].

## How much does [Brand] cost?
[Brand] pricing starts at [price] for [tier]. [Additional detail].

## How does [Brand] compare to [Competitor]?
[Brand] excels at [strengths] while [Competitor] is better for [their strengths].
```

**4. Original Data and Statistics**
Publish original research, benchmarks, surveys. AI cites specific numbers. Make statistics bold and quotable:
> **"78% of teams using [Brand] reported a 3x improvement in deployment speed"**

**5. Free Tools, Calculators, Templates**
Create utility content that earns natural mentions and links. Examples: ROI calculators, assessment tools, framework templates.

**6. Branded Strategies with Memorable Names**
Coin a methodology. Give it a name. Example: "The RAPID Framework for Content Optimization." LLMs remember and cite named frameworks.

---

## Phase 3: Consensus and Consistency Audit

AI models recommend brands when **multiple independent sources agree** on the same facts. Inconsistency creates uncertainty, and uncertain LLMs hedge or omit.

### Sources to Audit

Check that the following information is identical across all platforms:

| Data Point | Sources to Check |
|-----------|-----------------|
| Company name and spelling | Website, social profiles, directories, Wikipedia |
| Founding date | About page, Crunchbase, LinkedIn, Wikipedia |
| Product description | Homepage, G2, Capterra, LinkedIn, press releases |
| Pricing | Pricing page, G2, Capterra, review sites |
| Feature list | Product pages, comparison sites, documentation |
| Leadership / founders | About page, LinkedIn, Crunchbase, press mentions |
| Company size / metrics | About page, LinkedIn, Crunchbase, press releases |
| Contact information | Website, Google Business, directories |
| Category / industry | All profiles and listings |

### Audit Commands

```bash
# Search for brand mentions across platforms to compare
claude "Search for [BRAND] on G2, Capterra, Crunchbase, and LinkedIn.
        Compare the company description, founding date, pricing, and
        feature list across all sources. Flag any inconsistencies."
```

### Fix Protocol

For every inconsistency found:
1. Determine the **canonical truth** (usually your website)
2. Update every third-party profile to match
3. Submit corrections to platforms you don't control
4. Re-audit in 30 days to verify propagation

---

## Phase 4: AI-Friendly Content Conversion

Transform existing content so LLMs can extract clean, quotable answers.

### Conversion Rules

**Rule 1: Convert H2 Headings to Question Format**

```
BEFORE: ## Our Pricing Plans
AFTER:  ## How Much Does [Brand] Cost?
```

**Rule 2: Lead Every Section with a Direct Answer**

The first 1-2 sentences after any heading must directly answer the implied question. No preamble.

```
BEFORE:
## How Much Does Acme Cost?
When it comes to choosing the right plan, there are many factors to consider.
Our flexible pricing is designed to scale with your needs...

AFTER:
## How Much Does Acme Cost?
Acme costs $29/month for individuals and $99/month for teams of up to 10.
Enterprise pricing starts at $499/month with custom configuration.
```

**Rule 3: Make Statistics Bold and Quotable**

```
**Acme processes over 2 million requests per day with 99.97% uptime.**
```

**Rule 4: Add FAQ Schema Markup**

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "How much does [Brand] cost?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "[Direct answer with pricing details]"
    }
  }]
}
```

**Rule 5: Build Comparison Tables**

```html
<table>
  <thead>
    <tr><th>Feature</th><th>[Brand]</th><th>[Competitor A]</th><th>[Competitor B]</th></tr>
  </thead>
  <tbody>
    <tr><td>Price</td><td>$29/mo</td><td>$49/mo</td><td>$39/mo</td></tr>
    <tr><td>Free Tier</td><td>Yes</td><td>No</td><td>Yes (limited)</td></tr>
  </tbody>
</table>
```

**Rule 6: Use Semantic Chunking**

- Paragraphs: 2-4 sentences max
- Headings: descriptive and specific (not "Overview" but "What [Brand] Does Differently")
- Lists: use bullets for features, numbers for steps
- Definitions: use `<dfn>` tags or bold the term being defined

**Rule 7: Add Speakable Schema**

For content you want AI voice assistants to read aloud:

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".summary", ".key-answer", ".product-description"]
  }
}
```

### Conversion Commands

```bash
# Audit a page for AI-friendliness
claude "Read [URL/FILE] and score it for AI extractability. Check:
        heading format, answer directness, quotable stats, schema markup,
        paragraph length, and semantic structure. Provide specific rewrites."

# Bulk convert headings to question format
claude "Scan all content files in [DIRECTORY]. Convert every H2 that
        isn't a question into question format. Preserve meaning."

# Add FAQ schema to existing content
claude "Read [FILE] and generate FAQPage schema markup based on
        the existing Q&A content. Output the JSON-LD script tag."

# Rewrite for AI extractability
claude "Rewrite [FILE] following AEO content rules: question headings,
        direct first-sentence answers, bold statistics, short paragraphs,
        and comparison tables where relevant."
```

---

## Phase 5: Co-Citation Strategy

LLMs associate brands that appear together frequently. Get the target brand mentioned **alongside industry leaders** to inherit their authority signal.

### Tactics

**1. Publish Comparison Content**
Create honest comparisons between the target brand and established players. Title format: "[Brand] vs [Leader]: [Specific Differentiator]"

**2. Earn Roundup Mentions**
Target "best of" and "top tools" articles. Pitch to authors with a clear angle on what makes the product worth including.

**3. Participate in Industry Panels and Podcasts**
Transcripts get crawled. Appear alongside recognized names in recorded discussions.

**4. Get Listed in Curated Directories**
Industry-specific tool directories, awesome-lists on GitHub, and curated resource pages.

**5. Engage on Reddit and Quora**
When someone asks "What's the best alternative to [Leader]?" provide a genuinely helpful answer mentioning the product **with context and honest trade-offs**. Never shill.

**6. Joint Content and Integrations**
Co-publish content with complementary (non-competing) established brands. Integration partnership pages create bidirectional co-citation.

For detailed phase-by-phase execution steps for Phases 6-8, consult `references/aeo-phases.md`.

### Co-Citation Audit Command

```bash
claude "Search for '[BRAND]' and identify which other brands it is most
        frequently mentioned alongside in AI responses, review sites, and
        comparison articles. Map the co-citation network and identify gaps
        where [BRAND] should appear but doesn't."
```

---

## Phase 6: Platform-Specific Optimization

Each AI platform has different data sources and ranking signals. Optimize for Google AI Overviews (structured data + top-10 rankings), ChatGPT (Wikipedia + Reddit + training data), Perplexity (real-time web search + citations), Claude (depth + original research), and Microsoft Copilot (Bing index + social signals).

For detailed platform-by-platform signal tables and audit commands, consult `references/aeo-phases.md`.

---

## Phase 7: Visual Optimization for AI

Optimize visuals for AI interpretation: use real product screenshots, write descriptive full-sentence captions, add keyword-rich alt text, create infographics with embedded text, and add video transcripts.

For detailed image optimization rules and code examples, consult `references/aeo-phases.md`.

---

## Phase 8: Distribution and Seeding Plan

Systematic content distribution to maximize AI training data coverage across UGC platforms (Reddit, Quora, forums), digital PR, affiliate/review coverage, expert quote placement, and content syndication.

For detailed distribution tactics and platform-specific strategies, consult `references/aeo-phases.md`.

---

## Output: AEO Action Plan

After completing all phases, generate a prioritized action plan organized by time horizon.

### Quick Wins (Week 1-2)

These require no new content creation and have immediate impact:

1. **Fix consistency issues** found in Phase 3 (update all profiles to match canonical information).
2. **Add FAQ schema markup** to existing high-traffic pages.
3. **Reformat top 5 pages** using Phase 4 conversion rules (question headings, direct answers, bold stats).
4. **Update image alt text and captions** on key pages per Phase 7.
5. **Claim and optimize** all unclaimed business profiles on review platforms.
6. **Add Speakable schema** to homepage and product pages.
7. **Fix any factual errors** found in AI responses by correcting source content.

### Medium-Term (Month 1-3)

Content creation and platform presence building:

1. **Create 10 FAQ-style pages** targeting questions AI is asked about the target category.
2. **Publish 3 comparison pages** (brand vs top competitors) with honest, detailed analysis.
3. **Write an original research piece** with quotable statistics about the industry.
4. **Build Reddit presence** in 5 relevant subreddits (genuine engagement, no shilling).
5. **Publish 5 guest articles** on industry publications and high-authority platforms.
6. **Create or improve Wikipedia page** (if notability criteria are met).
7. **Add Wikidata entity** with complete structured data.
8. **Launch a branded framework or methodology** with a memorable name.
9. **Build comparison tables** for all product/pricing pages.

### Long-Term (Month 3-12)

Authority building, co-citation, and sustained digital PR:

1. **Publish quarterly industry reports** with original data
2. **Execute co-citation strategy** (joint content, roundup targeting, integration partnerships)
3. **Build and maintain UGC presence** across Reddit, Quora, and forums
4. **Launch digital PR campaign** targeting AI-crawled publications
5. **Create free tools/calculators** that earn natural mentions and links
6. **Establish expert quote pipeline** via HARO/Connectively
7. **Build affiliate program** to incentivize review coverage
8. **Conduct quarterly AEO re-audits** to track score improvement
9. **Monitor AI responses monthly** for new inaccuracies or sentiment shifts
10. **Expand to emerging AI platforms** as new search interfaces launch

### Action Plan Command

```bash
claude "Generate a complete AEO action plan for [BRAND] in the [CATEGORY]
        space. Competitors: [LIST]. Run the full 8-phase AEO audit and
        produce a prioritized action plan with quick wins, medium-term
        projects, and long-term strategy. Include specific content briefs
        for the top 5 highest-impact pieces to create."
```

---

## Measurement and Re-Audit

Track AEO progress with monthly check-ins and quarterly full audits.

**Monthly**: Run the 10 test queries from Phase 1 across all platforms. Track changes in presence, position, accuracy, and sentiment. Log in a tracking spreadsheet.

**Quarterly**: Run the full Phase 1 audit. Compare composite scores. Identify which phases need more investment.

**Key metrics to track:**
- Composite AEO Score trend (0-60)
- Number of AI platforms mentioning the brand (out of 5)
- First-mention rate (% of queries where brand appears first)
- Accuracy rate (% of AI responses with zero factual errors)
- Sentiment ratio (positive vs negative vs neutral mentions)
- Co-citation partners (which brands the target is mentioned alongside)

```bash
claude "Run a monthly AEO check for [BRAND]. Query all 5 AI platforms
        with our 10 standard queries. Compare results to last month's
        baseline. Flag any new inaccuracies, sentiment shifts, or
        position changes. Output a trend report."
```
