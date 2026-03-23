---
name: aeo-optimizer
description: >
  Optimizes a brand's visibility and reputation across AI search engines — ChatGPT,
  Perplexity, Claude, Google AI Overviews, and agentic search. Produces an AI
  visibility score, LLM seeding strategy, co-citation plan, and platform-specific
  tactics. Use when the user wants their brand recommended by AI, asks about AEO,
  GEO, generative engine optimization, answer engine optimization, or AI search
  optimization. Triggers on questions like "how do I show up in ChatGPT results,"
  "Perplexity doesn't mention us," "competitors appear in AI Overviews but we
  don't," "how do I get cited by LLMs," or "optimize for AI-powered search." Also
  triggers when users mention AI visibility scoring, LLM seeding, or want to
  influence what AI says about their brand. This is NOT for: building chatbots or
  AI integrations, using the Claude/OpenAI API, writing content without an AI
  search context, traditional Google SEO (use other skills), Google Ads, social
  media marketing, or general content writing. The key differentiator is the user
  wants to appear in AI-generated answers, not just traditional search results.
---

# AEO Optimizer — AI Engine Optimization Skill

Make brands discoverable, recommended, and accurately represented by AI search engines.

Traditional SEO gets you ranked on Google. AEO gets you **recommended by AI**. When a user asks ChatGPT "What's the best project management tool?" or Perplexity "Compare CRM platforms" — AEO determines whether your brand appears, how it's described, and whether it's positioned favorably.

---

## Phase 1: AI Visibility Audit

Score the brand across six dimensions. Each dimension receives a 0-10 rating. The composite AEO Score (0-60) establishes the baseline.

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

Publish brand-relevant content on these platforms, ordered by LLM training influence:

| Priority | Platform | Why It Matters | Action |
|----------|----------|---------------|--------|
| 1 | **Your Website** | Primary source of truth. Must be crawlable, well-structured, fast. | Ensure clean HTML, proper schema markup, no JS-only rendering. |
| 2 | **Wikipedia / Wikidata** | Highest-authority factual source for all LLMs. | Create or improve your Wikipedia page. Add Wikidata entity. |
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

LLMs associate brands that appear together frequently. Get mentioned **alongside industry leaders** to inherit their authority signal.

### Tactics

**1. Publish Comparison Content**
Create honest comparisons between your brand and established players. Title format: "[Your Brand] vs [Leader]: [Specific Differentiator]"

**2. Earn Roundup Mentions**
Target "best of" and "top tools" articles. Pitch to authors with a clear angle on what makes your product worth including.

**3. Participate in Industry Panels and Podcasts**
Transcripts get crawled. Appear alongside recognized names in recorded discussions.

**4. Get Listed in Curated Directories**
Industry-specific tool directories, awesome-lists on GitHub, and curated resource pages.

**5. Engage on Reddit and Quora**
When someone asks "What's the best alternative to [Leader]?" provide a genuinely helpful answer mentioning your product **with context and honest trade-offs**. Never shill.

**6. Joint Content and Integrations**
Co-publish content with complementary (non-competing) established brands. Integration partnership pages create bidirectional co-citation.

### Co-Citation Audit Command

```bash
claude "Search for '[BRAND]' and identify which other brands it is most
        frequently mentioned alongside in AI responses, review sites, and
        comparison articles. Map the co-citation network and identify gaps
        where [BRAND] should appear but doesn't."
```

---

## Phase 6: Platform-Specific Optimization

Each AI platform has different data sources and ranking signals. Optimize for each individually.

### Google AI Overviews

Google AI Overviews pull from top-ranking search results and structured data.

| Signal | Action |
|--------|--------|
| Search ranking | Must rank in top 10 for target queries (traditional SEO still matters) |
| Structured data | Implement FAQ, HowTo, Product, Review, and Organization schema |
| Content freshness | Update key pages quarterly with current data |
| E-E-A-T signals | Author bios, credentials, cited sources, methodology |
| Direct answers | First paragraph must answer the query in 1-2 sentences |

```bash
claude "Audit [URL] for Google AI Overview eligibility. Check:
        search ranking for [KEYWORDS], structured data implementation,
        content freshness date, author attribution, and direct-answer
        formatting in the first paragraph."
```

### ChatGPT

ChatGPT relies on training data (with a knowledge cutoff) plus web browsing. Heavy Wikipedia and Reddit influence.

| Signal | Action |
|--------|--------|
| Wikipedia presence | Create or improve Wikipedia article with citations |
| Reddit mentions | Genuine engagement in relevant subreddits |
| Structured content | Clean HTML, clear headings, extractable facts |
| Consistent facts | Same information across all sources ChatGPT might access |
| Recency (browsing) | Fresh content on crawlable pages for browsing-enabled queries |

```bash
claude "Check if [BRAND] has a Wikipedia page. If yes, audit it for
        accuracy and completeness. If no, assess notability criteria and
        draft a neutral, well-sourced article outline."
```

### Perplexity AI

Perplexity performs real-time web search and cites sources directly. Quality and structure matter most.

| Signal | Action |
|--------|--------|
| Content quality | Well-written, factual, comprehensive content |
| Author attribution | Clear author names, bios, and credentials on content |
| Page structure | Clean headings, short paragraphs, extractable answers |
| Source diversity | Multiple authoritative pages about your brand |
| Recency | Recently published or updated content ranks higher |

```bash
claude "Search Perplexity for '[TARGET QUERY]' and analyze: Is [BRAND]
        cited? Which sources are used? What content format do cited pages
        use? Identify what [BRAND] content needs to match."
```

### Claude

Claude values nuanced, well-reasoned content over keyword density.

| Signal | Action |
|--------|--------|
| Depth of analysis | Publish genuinely insightful, non-obvious content |
| Original research | Unique data, case studies, and first-party findings |
| Balanced perspective | Acknowledge trade-offs honestly (builds trust signal) |
| Technical accuracy | Precise, verifiable claims with methodology |
| Clean writing | Well-structured prose, not keyword-stuffed SEO content |

### Microsoft Copilot / Bing Chat

Copilot uses Bing's index. Bing SEO signals apply.

| Signal | Action |
|--------|--------|
| Bing ranking | Optimize for Bing (social signals matter more than on Google) |
| Social proof | Active social media profiles linked from your site |
| Schema markup | Full structured data implementation |
| Bing Webmaster Tools | Submit sitemap, monitor indexing |

---

## Phase 7: Visual Optimization for AI

Modern AI models process images using vision models (CLIP and similar). Optimize visuals for AI interpretation.

### Image Optimization Rules

**1. Use Real Product Screenshots**
AI models can identify and describe UI screenshots. Use actual in-product images rather than stock photography.

**2. Write Descriptive Full-Sentence Captions**
```html
<!-- BEFORE -->
<figcaption>Dashboard</figcaption>

<!-- AFTER -->
<figcaption>[Brand]'s analytics dashboard showing real-time conversion
tracking, revenue attribution, and campaign performance metrics.</figcaption>
```

**3. Write Keyword-Rich Alt Text**
```html
<img src="dashboard.png"
     alt="[Brand] analytics dashboard displaying conversion rates,
          revenue by channel, and A/B test results for e-commerce campaigns">
```

**4. Create Infographics with Embedded Text**
AI vision models read text in images. Infographics with statistics, process flows, and branded data are extractable by multimodal LLMs.

**5. Add Video Transcripts**
Every video should have an accurate, timestamped transcript. AI cannot watch video but can read transcripts.

```bash
claude "Audit all images on [URL/DIRECTORY] for AI optimization.
        Check: alt text quality, caption descriptiveness, image relevance,
        and whether real product screenshots are used vs stock photos.
        Generate improved alt text and captions for each image."
```

---

## Phase 8: Distribution and Seeding Plan

Systematic content distribution to maximize AI training data coverage.

### UGC Hub Strategy

Build organic brand mentions in user-generated content platforms:

- **Reddit**: Identify 5-10 relevant subreddits. Contribute value for 30+ days before any brand mentions. Answer questions where your product genuinely helps. Never create fake accounts or astroturf.
- **Quora**: Answer high-traffic questions in your category. Provide detailed, expert answers. Mention your product only when directly relevant.
- **Industry Forums**: Identify niche forums in your vertical. Become a recognized contributor.
- **Discord/Slack Communities**: Join relevant communities. Be helpful first. Product mentions come naturally.

### Digital PR for AI Citation Earning

Traditional PR now serves double duty: human readers and AI training data.

- Publish data-driven press releases with quotable statistics
- Create annual industry reports that journalists and AI will reference
- Pitch stories to publications that AI platforms crawl (major news, tech press, industry publications)
- Distribute via newswires that feed into multiple databases

### Affiliate and Review Coverage

- Launch or optimize an affiliate program to incentivize honest review content
- Send product access to review creators on YouTube, blogs, and podcasts
- Make reviewer onboarding frictionless (dedicated landing pages, press kits)
- Respond publicly to all reviews (positive and negative)

### Expert Quote Placement

- Use HARO (Help a Reporter Out) / Connectively / Quoted to place expert quotes in articles
- Offer expert commentary to journalists covering your industry
- Create a spokesperson page on your site with ready-to-use quotes and bios

### Content Syndication

Republish and syndicate content to AI-crawled platforms:
- Syndicate blog posts to Medium, LinkedIn, and industry publications (with canonical tags)
- Repurpose long-form content into Twitter/X threads, LinkedIn carousels, and short-form video transcripts
- Submit content to aggregators and newsletters in your vertical

---

## Output: AEO Action Plan

After completing all phases, generate a prioritized action plan organized by time horizon.

### Quick Wins (Week 1-2)

These require no new content creation and have immediate impact:

1. **Fix consistency issues** found in Phase 3 (update all profiles to match canonical information)
2. **Add FAQ schema markup** to existing high-traffic pages
3. **Reformat top 5 pages** using Phase 4 conversion rules (question headings, direct answers, bold stats)
4. **Update image alt text and captions** on key pages per Phase 7
5. **Claim and optimize** all unclaimed business profiles on review platforms
6. **Add Speakable schema** to homepage and product pages
7. **Fix any factual errors** found in AI responses by correcting source content

### Medium-Term (Month 1-3)

Content creation and platform presence building:

1. **Create 10 FAQ-style pages** targeting questions AI is asked about your category
2. **Publish 3 comparison pages** (brand vs top competitors) with honest, detailed analysis
3. **Write an original research piece** with quotable statistics about your industry
4. **Build Reddit presence** in 5 relevant subreddits (genuine engagement, no shilling)
5. **Publish 5 guest articles** on industry publications and high-authority platforms
6. **Create or improve Wikipedia page** (if notability criteria are met)
7. **Add Wikidata entity** with complete structured data
8. **Launch a branded framework or methodology** with a memorable name
9. **Build comparison tables** for all product/pricing pages

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
- Co-citation partners (which brands you're mentioned alongside)

```bash
claude "Run a monthly AEO check for [BRAND]. Query all 5 AI platforms
        with our 10 standard queries. Compare results to last month's
        baseline. Flag any new inaccuracies, sentiment shifts, or
        position changes. Output a trend report."
```
