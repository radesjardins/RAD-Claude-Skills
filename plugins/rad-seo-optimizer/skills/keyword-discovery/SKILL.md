---
name: keyword-discovery
description: >
  Keyword research, find keywords, what keywords should I target, keyword analysis, search
  volume, keyword difficulty. Covers seed discovery, expansion, intent classification,
  difficulty, and topic clustering. Produces 150-300 prioritized keywords.
argument-hint: "[topic or seed keyword]"
---

# Keyword Discovery Skill

Walk the user through a complete keyword research pipeline, producing a
prioritized keyword plan they can act on immediately. Assume the user has
never done keyword research before -- explain every concept in plain
language, but keep the process moving.

---

## Overview

This skill executes six phases in order:

1. **Seed Keyword Discovery** -- gather raw inputs
2. **Keyword Expansion** -- broaden the list
3. **Search Intent Classification** -- tag every keyword
4. **Difficulty Assessment** -- gauge competition
5. **Topic Cluster Mapping** -- organize into a hierarchy
6. **Prioritization** -- produce a ranked action plan

Work through each phase sequentially. Present findings after each phase
before moving on. Ask clarifying questions only in Phase 1; after that,
execute without unnecessary interruptions.

---

## Phase 1: Seed Keyword Discovery

### Gather Context

Before generating a single keyword, ask the user these questions. Do not
skip any. Wait for answers before proceeding.

1. **Business basics**: What does the business do? What products or
   services does it offer?
2. **Target audience**: Who are the ideal customers? What language or
   jargon do they use when talking about this space?
3. **Top 3 competitors**: Name up to three competitors (websites or
   brands) considered the main rivals.
4. **Existing keywords**: Are there any keywords already being targeted?
   If so, list them. If not, say "none" and start fresh.

### Seed Sources

Once you have the answers, mine seeds from every source below. For each
source, explain briefly what it is and why it matters.

| Source | What to extract |
|---|---|
| **Business context** | Industry terms, product names, service categories, brand modifiers |
| **Competitor analysis** | Terms competitors rank for on page 1; recurring themes in their title tags, H1s, and meta descriptions |
| **Customer language** | Phrases from support tickets, reviews, forum posts, and testimonials -- the words *customers* use, not marketing copy |
| **Question mining** | Questions from Reddit, Quora, and AnswerThePublic-style tools (autocomplete expansions, "People Also Ask" boxes) |
| **Google autocomplete** | Type each seed into Google and capture the suggested completions; do the same for YouTube and Amazon if relevant |
| **Internal site search** | If the user has site-search data, pull the top queries visitors type on-site -- these reveal unmet content needs |

Deliver the seed list as a simple numbered table:

```
#  | Seed Keyword            | Source
1  | project management tool | Business context
2  | how to manage remote teams | Question mining
...
```

Aim for **30-50 seed keywords** before moving on.

---

## Phase 2: Keyword Expansion

Take every seed and expand it using the four strategies below. The goal
is to go from ~40 seeds to **150-300 candidate keywords**.

### 2a. Long-Tail Variations (3-5 word phrases)

Add specificity to each seed. Long-tail keywords convert better because
they match a precise need.

> Seed: "project management"
> Long-tail: "project management for startups", "free project management
> software for small teams"

### 2b. Question-Based Keywords

Prepend question words: **who, what, when, where, why, how**.

> "how to choose project management software"
> "what is agile project management"
> "why do projects fail"

### 2c. Modifier Keywords

Append common modifiers to seeds:

- **Best / Top / Review / Comparison / vs** -- commercial intent
- **Alternative / Cheap / Free** -- budget-conscious buyers
- **Near me / [City]** -- local intent
- **Template / Example / Checklist** -- resource seekers
- **For beginners / For enterprises / For [audience]** -- audience fit

### 2d. LSI / Semantic Keywords

List related terms and concepts that are not exact synonyms but appear
alongside the seed in top-ranking content. These help search engines
understand topical depth.

> Seed: "project management"
> LSI: "Gantt chart", "sprint planning", "work breakdown structure",
> "resource allocation"

### 2e. Medium-Tail Keywords

Identify the "sweet spot" keywords -- 2-3 words, moderate search volume,
and moderate competition. These are often the fastest wins.

> "agile project management", "project scheduling tools"

Present the expanded list grouped by strategy so the user can see where
each keyword came from.

---

## Phase 3: Search Intent Classification

Every keyword must be tagged with exactly one intent. Explain each
intent type, then classify the full list.

### Intent Types

| Intent | Signal words | What Google shows |
|---|---|---|
| **Informational** | how to, what is, guide, tutorial, why, tips | Blog posts, Wikipedia, knowledge panels, videos |
| **Commercial** | best, top, review, comparison, vs, alternative | Listicles, review sites, comparison tables |
| **Transactional** | buy, price, discount, coupon, sign up, download, order | Shopping results, product pages, pricing pages, CTAs |
| **Navigational** | [brand name], login, support, contact, app | Official site, login pages, app store links |

### How to Classify

The definitive method is to look at the actual search results page:

- **Shopping carousel or product ads?** Transactional.
- **Video pack or "People Also Ask" boxes?** Likely informational.
- **Comparison articles dominate?** Commercial.
- **Single brand dominates positions 1-3?** Navigational.

If a keyword shows mixed intent, label it with the *dominant* intent and
note the secondary one.

### Output Format

Add an "Intent" column to the keyword table:

```
#  | Keyword                              | Intent        | Notes
1  | how to manage remote teams           | Informational |
2  | best project management software     | Commercial    |
3  | buy Asana subscription               | Transactional |
4  | Trello login                         | Navigational  |
```

---

## Phase 4: Difficulty Assessment

For each keyword (or at minimum the top 50), assess ranking difficulty.
You do not need paid tools to make a useful estimate.

### Factors to Evaluate

| Factor | What to look for | Easy signal | Hard signal |
|---|---|---|---|
| **Who ranks now** | Domain authority of page-1 sites | Forums, small blogs, thin content | Major brands, .gov, Wikipedia |
| **Content format** | Type of content on page 1 | Short articles, outdated posts | In-depth guides, interactive tools |
| **SERP features** | Featured snippets, PAA, video | Featured snippet = chance to leapfrog | Knowledge panel from Wikipedia = hard to displace |
| **Commercial value** | Ad spend on this term | No ads = lower commercial value | Heavy ads = lucrative but competitive |

### Difficulty Scale

Assign one of three levels:

- **Easy**: Thin or outdated content ranks; few strong domains; featured
  snippet available. A well-written article can rank in weeks.
- **Moderate**: Mix of strong and weak pages; requires comprehensive
  content and some backlinks. Expect 2-6 months.
- **Hard**: Page 1 is all high-authority domains with deep content.
  Requires significant authority, backlinks, and time (6-12+ months).

Add "Difficulty" and "Opportunity" columns to the table:

```
#  | Keyword                          | Intent       | Difficulty | Opportunity
1  | project management for nonprofits| Commercial   | Easy       | Featured snippet available
2  | project management software      | Commercial   | Hard       | Heavy ad spend, high value
```

---

## Phase 5: Topic Cluster Mapping

Organize the keyword list into a content hierarchy. This is how modern
SEO works: you do not target keywords in isolation; you build *clusters*
of related content that reinforce each other through internal links.

### Hierarchy

```
Pillar Topic (broad, 1-2 words, high volume)
  |
  +-- Subtopic A (medium-tail, 2-3 words)
  |     +-- Long-tail query 1
  |     +-- Long-tail query 2
  |
  +-- Subtopic B
        +-- Long-tail query 3
        +-- Long-tail query 4
```

### How to Build Clusters

1. **Identify pillars**: Pick the broadest, highest-volume terms. Each
   pillar becomes a comprehensive "pillar page" (2,000-4,000 words).
2. **Group subtopics**: Assign medium-tail keywords as subtopics. Each
   gets its own supporting article (1,000-2,000 words).
3. **Attach long-tail queries**: These become sections within subtopic
   articles, standalone FAQ entries, or short blog posts.
4. **Map internal links**: Every subtopic article links up to the pillar
   page. The pillar page links down to every subtopic. Subtopics in the
   same cluster link to each other where relevant.

### Example Cluster

```
PILLAR: Project Management
  |
  +-- Subtopic: Agile Project Management
  |     +-- what is a sprint in agile
  |     +-- agile vs waterfall comparison
  |
  +-- Subtopic: Project Management Tools
  |     +-- best free project management software
  |     +-- Asana vs Monday.com
  |
  +-- Subtopic: Remote Project Management
        +-- how to manage remote teams effectively
        +-- remote team communication best practices
```

Present the full cluster map and confirm it with the user before
moving to prioritization.

---

## Phase 6: Prioritization

This is the final deliverable. Score every keyword cluster and produce
three ranked lists the user can act on immediately.

### Scoring Criteria

Rate each keyword on these dimensions:

| Criterion | Scale | Description |
|---|---|---|
| **Business relevance** | 1-10 | How closely does this keyword relate to the product or service? |
| **Search volume indicator** | High / Medium / Low | Estimated relative search volume based on autocomplete prominence and SERP competition |
| **Competition level** | Easy / Moderate / Hard | From Phase 4 |
| **Content gap** | Yes / No | Does the site already have content targeting this keyword? |
| **Estimated effort** | Low / Medium / High | Time and resources needed to create ranking content |

### The Three Lists

#### 1. Top 10 Quick Wins

Keywords where content already exists (or is easy to create), competition
is low, and you can rank within weeks.

```
#  | Keyword                           | Intent       | Difficulty | Action
1  | project management for nonprofits | Commercial   | Easy       | Optimize existing /nonprofits page
2  | free Gantt chart template         | Transactional| Easy       | Create downloadable template
...
```

#### 2. Top 10 Strategic Targets

High-value keywords with moderate competition. These require dedicated
content creation and some link building. Expect results in 2-6 months.

```
#  | Keyword                           | Intent       | Difficulty | Action
1  | best project management software  | Commercial   | Moderate   | Write 3,000-word comparison guide
2  | agile project management guide    | Informational| Moderate   | Create pillar page with video
...
```

#### 3. Top 10 Long-Term Plays

High-competition, high-reward keywords. Build toward these by first
ranking for related easier keywords, then consolidating authority.

```
#  | Keyword                           | Intent       | Difficulty | Action
1  | project management software       | Commercial   | Hard       | Build cluster, earn backlinks
2  | project management                | Informational| Hard       | Pillar page + 10 subtopics
...
```

### Content Type Recommendations

For each keyword, recommend the best content format:

| Content Type | When to use |
|---|---|
| **Blog post** | Informational long-tail queries, how-tos |
| **Landing page** | Transactional keywords, product comparisons |
| **Comprehensive guide** | Pillar topics, informational medium-tail |
| **Tool or calculator** | "Calculator", "template", "generator" queries |
| **Video** | "How to" queries where Google shows video results |
| **FAQ section** | Question-based long-tail keywords |
| **Case study** | "[Industry] + results/example" queries |

### The 70/20/10 Content Mix

Apply this framework to the content calendar:

- **70% Foundation** (safe, proven formats): How-to guides, tutorials,
  listicles, FAQ content. These reliably attract traffic and build
  topical authority. Start here.
- **20% Growth** (builds on the foundation, moderate risk): Original
  research, data-driven posts, expert roundups, detailed comparisons.
  Higher effort but differentiates the site from competitors.
- **10% Moonshots** (innovative, high risk): Interactive tools,
  contrarian opinion pieces, original frameworks, viral-potential
  content. Most will underperform but the wins are outsized.

When building the content calendar, tag each piece with its mix
category to maintain the balance over time.

---

## Delivery Checklist

Before finishing, confirm you have delivered:

- [ ] 30-50 seed keywords with sources
- [ ] 150-300 expanded keywords grouped by strategy
- [ ] Every keyword tagged with search intent
- [ ] Top 50+ keywords assessed for difficulty
- [ ] Complete topic cluster map with pillar-subtopic hierarchy
- [ ] Internal linking plan between cluster pages
- [ ] Top 10 Quick Wins with specific actions
- [ ] Top 10 Strategic Targets with content recommendations
- [ ] Top 10 Long-Term Plays with cluster-building roadmap
- [ ] Content type recommendation for each priority keyword
- [ ] 70/20/10 mix labels on all recommended content

If any item is incomplete, go back and finish it before presenting the
final plan to the user.

---

## Tone and Style

- Use plain language. Define jargon the first time you use it.
- Be specific. "Write a blog post" is not actionable. "Write a
  2,000-word comparison of X vs Y targeting commercial intent" is.
- Use tables for any list longer than five items.
- After each phase, give a brief summary of what was found and what
  comes next, so the user always knows where they are in the process.
- When you lack real search volume data, say so honestly and use
  relative estimates (high/medium/low) based on observable signals
  like autocomplete prominence and SERP competition density.
