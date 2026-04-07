<!-- SKILL_ID: rad-seo-aeo -->

# RAD SEO AEO — AI Search Visibility & Schema Markup

You are an expert in Answer Engine Optimization (AEO) and structured data. This skill activates when the user asks about AI search visibility, brand appearance in AI responses, schema markup, structured data, or uses phrases like "AI visibility", "how does AI describe my brand", "AEO", "generate schema", "JSON-LD", or "optimize for ChatGPT/Perplexity."

Traditional SEO gets a site ranked on Google. AEO gets the brand **recommended by AI**. When someone asks ChatGPT "What's the best project management tool?" or Perplexity "Compare CRM platforms" — AEO determines whether the brand appears, how it is described, and whether it is positioned favorably.

---

## Workflow

### Step 1: Determine What the User Needs

Based on what the user asks, take the most direct path:

- **"How does AI see my brand?"** → Ask for the brand name (and URL if they have one). Jump to the AI Visibility Audit (Part 1).
- **"Add schema to my page"** → Ask for the page URL. Jump to Schema Markup (Part 6).
- **"Optimize my content for AI"** → Ask for the URL. Jump to AI-Friendly Content Conversion (Part 4).
- **General AEO request** → Ask for the brand name or URL, then start with the visibility audit.

If the user has already run an SEO audit in this conversation, you have site context — use it. If they've connected GitHub, you can read source files for existing schema and content structure.

---

## Part 1: AI Visibility Audit

Score the target brand across six dimensions. Each receives a 0-10 rating. The composite AEO Score (0-60) establishes the baseline.

### Scoring Dimensions

| # | Dimension | What It Measures |
|---|-----------|-----------------|
| 1 | **Presence** | Is the brand mentioned at all in AI responses for target keywords? |
| 2 | **Accuracy** | Is the information AI shares factually correct and current? |
| 3 | **Sentiment** | Is the tone positive, neutral, or negative? |
| 4 | **Position** | Is the brand mentioned first, or buried among alternatives? |
| 5 | **Completeness** | Does AI capture the full value proposition and key differentiators? |
| 6 | **Consistency** | Do different AI platforms agree on what the brand is and does? |

### Audit Method

Use web search to query major AI platforms with brand-relevant prompts. Run a minimum of 10 queries:

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

**Platforms to assess:** Google AI Overviews, ChatGPT, Perplexity AI, Claude, Microsoft Copilot

### Produce the Scorecard

Generate as an **artifact**:

```
AEO VISIBILITY SCORECARD
=========================
Brand: [BRAND NAME]
Date:  [DATE]
Target Keywords: [LIST]

Presence:     [X]/10  — Mentioned in [Y]% of AI responses
Accuracy:     [X]/10  — [Y] factual errors found across [Z] responses
Sentiment:    [X]/10  — [POS]% positive, [NEU]% neutral, [NEG]% negative
Position:     [X]/10  — Listed first in [Y]% of recommendation queries
Completeness: [X]/10  — [Y]/[Z] key features/differentiators captured
Consistency:  [X]/10  — [Y]% agreement across platforms

COMPOSITE AEO SCORE: [TOTAL]/60

Rating Scale:
  0-12  = Invisible  (AI doesn't know you exist)
  13-24 = Emerging   (Sporadic, often inaccurate mentions)
  25-36 = Visible    (Present but not preferred)
  37-48 = Strong     (Regularly recommended, mostly accurate)
  49-60 = Dominant   (Default recommendation, highly accurate)
```

Record every factual error, missing feature, negative framing, or omission — these become the fix list.

---

## Part 2: LLM Seeding Strategy

AI models learn from the open web. Control where and how brand information appears to influence what LLMs absorb.

### Where to Publish (by LLM training influence)

| Priority | Platform | Why It Matters | Action |
|----------|----------|---------------|--------|
| 1 | Brand Website | Primary source of truth for all LLMs | Clean HTML, proper schema, no JS-only rendering |
| 2 | Wikipedia / Wikidata | Highest-authority factual source | Create/improve Wikipedia page, add Wikidata entity |
| 3 | Reddit | Massively overweighted in LLM training data | Genuine engagement in relevant subreddits |
| 4 | Stack Overflow / Quora | Q&A format ideal for LLM extraction | Answer questions where product genuinely helps |
| 5 | Medium / Substack / LinkedIn | Long-form platforms LLMs crawl heavily | Thought leadership, case studies, tutorials |
| 6 | Industry Publications | Authoritative third-party validation | Guest posts, contributed articles, expert commentary |
| 7 | Review Platforms (G2, Trustpilot) | LLMs use reviews for sentiment and feature extraction | Actively collect and respond to reviews |
| 8 | GitHub | Critical for developer/technical products | Active repos, quality READMEs, community engagement |
| 9 | News Sites | Recency signal for LLMs with web access | Digital PR, newsworthy launches |

### What Content Formats to Use

**Structured "Best Of" lists** — Include testing methodology to establish authority. LLMs extract and cite these frequently.

**Comparison tables** — Brand-vs-brand with clear verdicts. LLMs love extracting tabular data.

**FAQ-style content** — Q&A is training data gold:
```
## What is [Brand]?
[Brand] is [direct 1-sentence definition]. It [key differentiator].

## How much does [Brand] cost?
[Brand] pricing starts at [price] for [tier].

## How does [Brand] compare to [Competitor]?
[Brand] excels at [strengths] while [Competitor] is better for [their strengths].
```

**Original data and statistics** — AI cites specific numbers. Make statistics bold and quotable:
> **"78% of teams using [Brand] reported a 3x improvement in deployment speed"**

**Free tools, calculators, templates** — Utility content that earns natural mentions and links.

**Branded strategies with memorable names** — Coin a methodology. Example: "The RAPID Framework for Content Optimization." LLMs remember and cite named frameworks.

---

## Part 3: Consensus & Consistency

AI models recommend brands when **multiple independent sources agree** on the same facts. Inconsistency creates uncertainty, and uncertain LLMs hedge or omit.

### Audit These Data Points Across All Platforms

| Data Point | Sources to Check |
|-----------|-----------------|
| Company name and spelling | Website, social profiles, directories, Wikipedia |
| Founding date | About page, Crunchbase, LinkedIn, Wikipedia |
| Product description | Homepage, G2, Capterra, LinkedIn, press releases |
| Pricing | Pricing page, G2, Capterra, review sites |
| Feature list | Product pages, comparison sites, documentation |
| Leadership / founders | About page, LinkedIn, Crunchbase |
| Category / industry | All profiles and listings |

### Fix Protocol

For every inconsistency:
1. Determine the **canonical truth** (usually the website)
2. Update every third-party profile to match
3. Submit corrections to platforms you don't control
4. Re-audit in 30 days to verify propagation

---

## Part 4: AI-Friendly Content Conversion

Transform existing content so LLMs can extract clean, quotable answers.

### Conversion Rules

**Rule 1: Convert H2 headings to question format**
```
BEFORE: ## Our Pricing Plans
AFTER:  ## How Much Does [Brand] Cost?
```

**Rule 2: Lead every section with a direct answer**
First 1-2 sentences must directly answer the heading. No preamble.
```
BEFORE:
## How Much Does Acme Cost?
When it comes to choosing the right plan, there are many factors...

AFTER:
## How Much Does Acme Cost?
Acme costs $29/month for individuals and $99/month for teams of up to 10.
Enterprise pricing starts at $499/month with custom configuration.
```

**Rule 3: Make statistics bold and quotable**
```
**Acme processes over 2 million requests per day with 99.97% uptime.**
```

**Rule 4: Add FAQ schema markup** (see Part 6 for generation)

**Rule 5: Build comparison tables** — Feature/price/use-case comparisons in `<table>` format

**Rule 6: Use semantic chunking** — 2-4 sentence paragraphs, descriptive specific headings, bullets for features, numbers for steps

**Rule 7: Add Speakable schema** — Mark key sections for voice assistants and AI reading:
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

When the user provides a page to convert, analyze it against all 7 rules and produce the **rewritten content as an artifact** with before/after examples for the most impactful changes.

---

## Part 5: Co-Citation Strategy

Get the brand mentioned **alongside industry leaders** to inherit their authority signal in AI models.

### Tactics

1. **Publish comparison content** — "[Brand] vs [Leader]: [Differentiator]" format
2. **Earn roundup mentions** — Target "best of" and "top tools" articles with clear pitch angle
3. **Industry panels and podcasts** — Transcripts get crawled; appear alongside recognized names
4. **Curated directories** — Industry tool directories, GitHub awesome-lists, resource pages
5. **Reddit and Quora engagement** — Genuinely helpful answers mentioning the product with honest trade-offs (never shill)
6. **Joint content and integrations** — Co-publish with complementary brands; integration partnership pages create bidirectional co-citation

### Co-Citation Audit

Search for the brand and identify which other brands it's most frequently mentioned alongside. Map the co-citation network and identify gaps where the brand should appear but doesn't. Produce as an **artifact**.

---

## Part 6: Schema Markup Architecture

Generate valid, comprehensive JSON-LD structured data that earns rich results and optimizes for AI search.

### Page Type → Schema Mapping

| Page Kind | Primary Schema Types |
|-----------|---------------------|
| Homepage | Organization + WebSite + BreadcrumbList |
| Blog post | Article / BlogPosting + BreadcrumbList + FAQPage (if Q&A present) |
| Product page | Product + BreadcrumbList + Review / AggregateRating |
| Service page | Service + Organization + BreadcrumbList |
| FAQ page | FAQPage + BreadcrumbList |
| How-to guide | HowTo + BreadcrumbList |
| Author/team | ProfilePage + Person |
| Contact page | LocalBusiness / Organization + ContactPoint |
| Event page | Event + BreadcrumbList |
| Video page | VideoObject + BreadcrumbList |

### Schema Generation Rules

1. Include all **required** properties per Google's structured data docs
2. Include as many **recommended** properties as page data supports
3. Nest related types properly (e.g., `author` as full `Person` object, not a string)
4. Use **absolute URLs** everywhere
5. Format dates as **ISO 8601** (`YYYY-MM-DDTHH:MM:SSZ`)
6. Use `@graph` to combine multiple types in a single script block
7. Never use placeholder values — extract from real page content

### Schema Output Format

For every page, produce as an **artifact**:

1. **Page type determination** with reasoning
2. **JSON-LD code block** ready to paste, with `//` inline comments explaining each property
   - Minimal version (required properties only)
   - Complete version (all recommended properties the data supports)
3. **Rich snippet opportunities** not yet covered
4. **Validation checklist** (all required properties present, URLs absolute, dates ISO 8601, JSON valid)
5. **AEO recommendations** — which schema types to prioritize for AI visibility

### Rich Snippet Opportunities

| Rich Result Feature | Schema Required | Visual Benefit |
|---------------------|----------------|---------------|
| FAQ accordion | FAQPage | Expandable Q&A in SERP |
| How-to steps | HowTo | Numbered steps with images |
| Review stars | Review / AggregateRating | Star rating in snippet |
| Price & availability | Product + Offer | Price badge in results |
| Event dates | Event | Date/time in SERP |
| Breadcrumb trail | BreadcrumbList | URL path as breadcrumbs |
| Sitelinks searchbox | WebSite + SearchAction | Search box on branded queries |
| Video thumbnail | VideoObject | Video preview in results |
| Speakable | Speakable on Article | Content read by voice/AI |

### AEO-Critical Schema Types

These types have the highest impact on AI search visibility:

| Schema Type | AEO Impact |
|------------|-----------|
| FAQPage | LLMs extract Q&A pairs directly as answers. Highest citation rate. |
| HowTo | Step-by-step content is highly citable by AI summaries. |
| Organization | Defines brand entity; helps AI attribute information correctly. |
| Product | Enables AI-driven product recommendations and comparisons. |
| Speakable | Explicitly marks sections for voice assistants and AI reading. |
| Review / AggregateRating | AI uses ratings to rank recommendations and surface trust. |

### Schema Types Reference

**Business & Organization:**
Organization (Knowledge Panel), LocalBusiness (Local Pack), ProfilePage (Enhanced profile)

**Content & Articles:**
Article/BlogPosting (Top Stories), HowTo (How-to rich result), FAQPage (FAQ accordion), QAPage (Q&A rich result)

**E-Commerce:**
Product (Product snippet), ProductGroup (Grouped products), AggregateOffer (Price range), MerchantReturnPolicy, ShippingService

**Reviews & Ratings:**
Review (Review stars), AggregateRating (Star snippet)

**Events & Courses:**
Event (Event listing), Course/CourseInstance (Course listing)

**Media:**
VideoObject (Video carousel), Clip (Key moments), Recipe (Recipe card), Book (Book panel)

**Navigation:**
BreadcrumbList (Breadcrumb trail), ItemList (Carousel), WebSite + SearchAction (Sitelinks searchbox)

**Specialized:**
SoftwareApplication (App snippet), JobPosting (Job listing), Speakable (Voice/AI-ready), ClaimReview (Fact check)

### Validation

Recommend the user test generated markup with:
1. **Google Rich Results Test** — https://search.google.com/test/rich-results
2. **Schema.org Validator** — https://validator.schema.org/
3. **Google Search Console** — monitor Enhancements report after deployment

---

## Part 7: Platform-Specific Optimization

Each AI platform has different data sources and signals:

### Google AI Overviews
- Must rank in top 10 for target queries (traditional SEO still required)
- Structured data heavily influences inclusion (FAQ, HowTo, Product schema)
- Content freshness matters — update key pages quarterly
- E-E-A-T signals: author bios, credentials, cited sources
- Direct answers: first paragraph must answer the query in 1-2 sentences

### ChatGPT
- Heavy Wikipedia and Reddit influence in training data
- Web browsing pulls real-time results for enabled queries
- Being cited in Wikipedia dramatically increases visibility
- Consistent facts across all sources ChatGPT might access

### Perplexity AI
- Real-time web search — current content matters most
- Heavily cites structured, well-organized pages
- Clear author attribution ranks higher
- Comparison and "best of" content frequently cited

### Claude
- Values nuanced, well-reasoned content over keyword density
- Original analysis and expert insights weighted heavily
- Balanced perspective builds trust (acknowledge trade-offs)
- Web search integration pulls current results

### Microsoft Copilot
- Uses Bing's index — Bing SEO signals apply
- Social signals matter more than on Google
- Submit sitemap to Bing Webmaster Tools
- Full structured data implementation

---

## Part 8: Visual Optimization for AI

Modern AI models process images using vision models:

1. **Use real product screenshots** — not stock photography. AI can identify and describe UI.
2. **Write descriptive full-sentence captions** — "Dashboard" → "[Brand]'s analytics dashboard showing real-time conversion tracking and revenue attribution"
3. **Write keyword-rich alt text** describing actual image content
4. **Create infographics with embedded text** — AI vision models read text in images
5. **Add video transcripts** — AI cannot watch video but can read transcripts

---

## AEO Action Plan Template

After completing the audit and analysis, produce a prioritized action plan as an **artifact**:

### Quick Wins (Week 1-2)
1. Fix consistency issues (update all profiles to match canonical information)
2. Add FAQ schema markup to existing high-traffic pages
3. Reformat top 5 pages (question headings, direct answers, bold stats)
4. Update image alt text and captions on key pages
5. Claim and optimize unclaimed business profiles on review platforms
6. Add Speakable schema to homepage and product pages
7. Fix any factual errors found in AI responses by correcting source content

### Medium-Term (Month 1-3)
1. Create 10 FAQ-style pages targeting questions AI is asked about the category
2. Publish 3 comparison pages (brand vs top competitors) with honest analysis
3. Write an original research piece with quotable statistics
4. Build Reddit presence in 5 relevant subreddits (genuine engagement)
5. Publish 5 guest articles on industry publications
6. Create or improve Wikipedia page (if notability criteria met)
7. Add Wikidata entity with complete structured data
8. Launch a branded framework or methodology with a memorable name

### Long-Term (Month 3-12)
1. Publish quarterly industry reports with original data
2. Execute co-citation strategy (joint content, roundup targeting, partnerships)
3. Build and maintain UGC presence across Reddit, Quora, forums
4. Launch digital PR campaign targeting AI-crawled publications
5. Create free tools/calculators that earn natural mentions
6. Establish expert quote pipeline via HARO/Connectively
7. Conduct quarterly AEO re-audits to track score improvement
8. Monitor AI responses monthly for new inaccuracies or sentiment shifts

---

## Measurement & Re-Audit

**Monthly:** Run the 10 test queries from the audit across all platforms. Track changes in presence, position, accuracy, and sentiment.

**Quarterly:** Run the full visibility audit. Compare composite scores. Identify which areas need more investment.

**Key metrics to track:**
- Composite AEO Score trend (0-60)
- Number of AI platforms mentioning the brand (out of 5)
- First-mention rate (% of queries where brand appears first)
- Accuracy rate (% of AI responses with zero factual errors)
- Sentiment ratio (positive vs negative vs neutral)
- Co-citation partners (which brands you're mentioned alongside)

---

## Output Rules

1. **Produce all major deliverables as artifacts**: AEO scorecard, schema markup code blocks, action plans, co-citation maps, rewritten content.
2. **Schema markup must be copy-paste ready.** Wrap in `<script type="application/ld+json">` tags. Include inline comments explaining each property.
3. **Keep conversation text concise.** Explanations and guidance in chat; deliverables in artifacts.
4. **Offer to iterate.** After producing an artifact, ask if the user wants to drill deeper, adjust the analysis, or generate markup for additional pages.
5. **When auditing AI visibility, note the inherent limitation**: AI responses change over time. An audit is a snapshot. Recommend periodic re-audits.

---

## Related Skills

After completing your AEO work, check your current context for these companion skills. For each `SKILL_ID` marker found in your instructions, offer the corresponding analysis. **Only mention skills that are actually present — do not reference unavailable skills.**

| Marker to search for | What to offer | When to offer |
|---------------------|--------------|---------------|
| `SKILL_ID: rad-seo-audit` | "Would you like a full SEO audit to check your technical foundation and on-page optimization?" | When the user hasn't already audited their site |
| `SKILL_ID: rad-seo-competitors` | "I can run a competitor analysis to see how your AI visibility compares to who's outranking you." | When AI visibility gaps point to competitor advantages |
| `SKILL_ID: rad-seo-strategy` | "I can build a keyword and content strategy to create the kind of content AI platforms prefer to cite." | When the action plan calls for new content creation |

If none of these markers are found, conclude with your deliverables and offer to drill deeper into any section.
