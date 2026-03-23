---
name: seo-report-generator
description: >
  Aggregates findings from all completed SEO audit skills into a single prioritized
  report with scores, executive summary, category dashboards, and a 30/60/90 day
  roadmap with fix commands. Use when the user wants to compile or export SEO audit
  results into a report, needs a prioritized implementation plan from audit findings,
  asks for an SEO scorecard or summary document, wants to know "what should I fix
  first," or needs a formatted report for stakeholders or a board presentation.
  Triggers on "generate an SEO report," "summarize the audit findings," "create an
  action plan," "export recommendations," or "give me a 30/60/90 day SEO roadmap."
  This skill should run AFTER other audit skills have produced findings — it
  aggregates, it does not perform the audits itself. This is NOT for: running the
  actual audits (use specific skills first), building analytics dashboards, creating
  Google Data Studio reports, or writing general business reports.
---

# SEO Report Generator

Aggregates findings from every other skill in the RAD SEO Optimizer plugin and
produces a single, prioritized, actionable report a business owner or developer can
follow step-by-step.

---

## Phase 1: Data Collection

Gather results from all completed audit skills. For each source below, pull the
raw findings, individual scores, and issue lists.

### Required Data Sources

| Source Skill | Data Collected |
|---|---|
| Technical SEO Audit | Crawlability, indexing, robots.txt, sitemap, HTTPS, canonical tags, redirects, status codes |
| On-Page SEO Audit | Title tags, meta descriptions, headings, keyword usage, image alt text, URL structure |
| Content & E-E-A-T Assessment | Content quality scores, expertise signals, author authority, trust indicators |
| Schema Markup Audit | Structured data types present, validation errors, coverage gaps |
| Internal Linking Analysis | Link graph depth, orphan pages, anchor text distribution, link equity flow |
| Core Web Vitals | LCP, INP, CLS, TTFB, FCP scores per page and site-wide aggregates |
| AEO Readiness Audit | AI-engine visibility across Presence, Accuracy, Sentiment, Position, Completeness, Consistency |
| Competitor Analysis | Competitor domain scores, content gaps, backlink gaps, keyword overlaps |
| Keyword Research | Target keywords, search intent, difficulty, current rankings |
| Link Building Recon | Prospect lists, broken-link targets, resource page targets, expected DA |

If a skill has not yet been run, note it as **"Not audited -- run [skill name] first"**
in the report and exclude its category from the overall score calculation.

---

## Phase 2: Priority Ranking

Score every individual finding using three dimensions.

### Scoring Model

**Impact (1-10):** Estimated ranking improvement if the issue is resolved.

| Impact Range | Meaning |
|---|---|
| 9-10 | Blocking indexing or causing major ranking loss |
| 7-8 | Significant ranking drag; fixing yields visible improvement within weeks |
| 4-6 | Moderate effect; contributes to cumulative ranking gains |
| 1-3 | Minor polish; unlikely to move rankings alone |

**Effort:**

| Label | Time Estimate | Multiplier |
|---|---|---|
| Quick Fix | < 30 minutes | 1 |
| Moderate | 1-4 hours | 2 |
| Project | 1+ days | 4 |

**Priority Score** = Impact / Effort Multiplier

Sort all findings by priority score descending. Group into three tiers:

- **Critical Issues** -- Priority >= 5 or Impact >= 9
- **Warnings** -- Priority >= 2.5 and Impact >= 4
- **Opportunities** -- Everything else worth acting on

---

## Phase 3: Report Generation

Output the report in the exact template below. Replace every `[placeholder]` with
real data. Remove any section whose source skill was not run, but keep the section
heading with a note that the audit is pending.

````markdown
# SEO Domination Report: [Website Name]
**Generated**: [Date]
**Overall Score**: [X]/100 (Grade: [A-F])
**AEO Readiness**: [X]/60

---

## Executive Summary

[3-4 paragraphs in plain English explaining:
- Current state of the website's SEO health
- Biggest opportunities for improvement
- Expected impact of implementing recommendations
- How the site compares to competitors]

---

## Score Dashboard

### Category Scores

| Category | Score | Grade | Critical | Warnings | Opportunities |
|----------|-------|-------|----------|----------|---------------|
| Technical SEO | X/100 | X | X | X | X |
| On-Page SEO | X/100 | X | X | X | X |
| Content & E-E-A-T | X/100 | X | X | X | X |
| Schema Markup | X/100 | X | X | X | X |
| Internal Linking | X/100 | X | X | X | X |
| Page Speed | X/100 | X | X | X | X |
| Mobile & Accessibility | X/100 | X | X | X | X |
| AEO Readiness | X/100 | X | X | X | X |

**Grading Scale**: A = 90-100, B = 80-89, C = 70-79, D = 60-69, F = below 60

### AEO Visibility Scores

| Dimension | Score | Assessment |
|-----------|-------|------------|
| Presence | X/10 | [Brief assessment] |
| Accuracy | X/10 | [Brief assessment] |
| Sentiment | X/10 | [Brief assessment] |
| Position | X/10 | [Brief assessment] |
| Completeness | X/10 | [Brief assessment] |
| Consistency | X/10 | [Brief assessment] |

---

## Critical Issues (Fix Immediately)

### 1. [Issue Title]
- **Category**: [Technical/On-Page/Content/Schema/Linking/Speed/AEO]
- **Impact**: [X]/10 | **Effort**: [Quick Fix/Moderate/Project] | **Priority**: [X]
- **What's wrong**: [Plain English explanation a business owner can understand]
- **Why it matters**: [How this affects rankings and revenue]
- **How to fix with Claude Code**:
  ```
  claude "[exact command to fix this issue]"
  ```
- **Manual fix steps**: [Step-by-step for issues Claude Code cannot fully automate]

[Repeat for every critical issue, numbered sequentially]

---

## Warnings (Fix Within 30 Days)

### [N]. [Issue Title]
- **Category**: [category]
- **Impact**: [X]/10 | **Effort**: [level] | **Priority**: [X]
- **What's wrong**: [explanation]
- **Why it matters**: [ranking/revenue impact]
- **How to fix with Claude Code**:
  ```
  claude "[command]"
  ```
- **Manual fix steps**: [if needed]

[Repeat for every warning, numbered sequentially continuing from Critical Issues]

---

## Opportunities (Implement for Growth)

### [N]. [Issue Title]
- **Category**: [category]
- **Impact**: [X]/10 | **Effort**: [level] | **Priority**: [X]
- **What's wrong**: [explanation]
- **Why it matters**: [ranking/revenue impact]
- **How to fix with Claude Code**:
  ```
  claude "[command]"
  ```
- **Manual fix steps**: [if needed]

[Repeat for every opportunity]

---

## Competitive Analysis Summary

| Metric | Your Site | [Competitor 1] | [Competitor 2] | [Competitor 3] |
|--------|-----------|----------------|----------------|----------------|
| Domain Authority | X | X | X | X |
| Organic Keywords | X | X | X | X |
| Monthly Traffic Est. | X | X | X | X |
| Backlink Count | X | X | X | X |
| Content Pages | X | X | X | X |
| Schema Coverage | X% | X% | X% | X% |
| Core Web Vitals Pass | Y/N | Y/N | Y/N | Y/N |
| AEO Readiness | X/60 | X/60 | X/60 | X/60 |

---

## 30/60/90 Day Implementation Roadmap

### Days 1-30: Foundation Fixes
**Goal**: Fix all critical issues and quick wins

1. [Specific action] -- `claude "[command]"`
2. [Specific action] -- `claude "[command]"`
3. [Continue for all Day-1-30 tasks]

**Expected outcome**: [Measurable improvement prediction]

### Days 31-60: Content & Authority Building
**Goal**: Create new content, implement schema, begin link building

1. [Specific action] -- `claude "[command]"`
2. [Specific action] -- `claude "[command]"`
3. [Continue for all Day-31-60 tasks]

**Expected outcome**: [Measurable improvement prediction]

### Days 61-90: Growth & Competitive Edge
**Goal**: Scale content production, active outreach, AEO optimization

1. [Specific action] -- `claude "[command]"`
2. [Specific action] -- `claude "[command]"`
3. [Continue for all Day-61-90 tasks]

**Expected outcome**: [Measurable improvement prediction]

---

## Keyword Opportunities

| Keyword | Intent | Difficulty | Volume | Current Rank | Target Rank | Action |
|---------|--------|------------|--------|--------------|-------------|--------|
| [kw] | [informational/transactional/navigational] | [1-100] | [monthly] | [pos or --] | [pos] | [Create/Optimize/Build links] |

---

## Link Building Opportunities

| Tactic | Target | Expected DA | Effort | Priority | Status |
|--------|--------|-------------|--------|----------|--------|
| [Broken link / Resource page / Guest post / etc.] | [URL or domain] | [DA] | [Quick/Moderate/Project] | [High/Medium/Low] | [Pending] |

---

## Content Recommendations

| Content Piece | Type | Target Keyword | Word Count | Priority | Status |
|---------------|------|----------------|------------|----------|--------|
| [Title] | [Blog/Landing/Pillar/FAQ] | [keyword] | [est.] | [High/Medium/Low] | [To create/To update] |

---

## AEO Action Plan

1. **Structured Data Expansion** -- Add FAQ, HowTo, and Article schema to all key pages
   ```
   claude "Add FAQ schema markup to [page] based on the top questions people ask about [topic]"
   ```
2. **Direct Answer Optimization** -- Restructure content to lead with concise answers
3. **Entity Clarity** -- Ensure the site's primary entities are unambiguously defined
4. **Source Authority** -- Build citations and mentions on authoritative third-party sites
5. **Freshness Signals** -- Establish a content update cadence for high-value pages
6. **Multi-Engine Consistency** -- Verify information parity across Google, Bing, ChatGPT, Perplexity

---

## Re-Audit Recommendation

- **Next full audit**: [Date -- typically 90 days from report generation]
- **Interim check (critical items only)**: [Date -- typically 30 days out]
- **Focus areas for next audit**: [Top 3 areas that need re-evaluation]
- **KPIs to track between audits**:
  - Organic traffic trend (weekly)
  - Core Web Vitals pass rate
  - Indexed page count
  - AEO readiness score delta
  - Keyword ranking movement for top 20 targets

---
*Generated by RAD SEO Optimizer -- Claude Code Plugin*
````

---

## Phase 4: Export Options

After generating the report, offer the user three choices:

1. **Display in conversation** (default) -- Output the full markdown report directly.
2. **Save to file** -- Write the report to a file in the project:
   ```
   claude "Save this SEO report to ./seo-reports/[domain]-[YYYY-MM-DD].md"
   ```
3. **Create task lists** -- Break the report into separate actionable files:
   - `critical-fixes.md` -- Only the Critical Issues section with checkboxes
   - `30-day-plan.md` -- Days 1-30 roadmap as a checklist
   - `60-day-plan.md` -- Days 31-60 roadmap as a checklist
   - `90-day-plan.md` -- Days 61-90 roadmap as a checklist
   - `content-calendar.md` -- Content recommendations as a production schedule
   - `link-building-tracker.md` -- Link prospects with status tracking columns

---

## Scoring Reference

### Overall Score Calculation

The overall score is the weighted average of all audited category scores:

| Category | Weight |
|----------|--------|
| Technical SEO | 20% |
| On-Page SEO | 15% |
| Content & E-E-A-T | 20% |
| Schema Markup | 10% |
| Internal Linking | 10% |
| Page Speed | 10% |
| Mobile & Accessibility | 5% |
| AEO Readiness | 10% |

If a category was not audited, redistribute its weight proportionally across the
remaining categories.

### Grade Thresholds

| Grade | Score Range | Interpretation |
|-------|------------|----------------|
| A | 90-100 | Excellent -- maintain and iterate |
| B | 80-89 | Strong -- a few targeted improvements needed |
| C | 70-79 | Average -- meaningful gains available |
| D | 60-69 | Below average -- significant work required |
| F | 0-59 | Poor -- critical intervention needed |
