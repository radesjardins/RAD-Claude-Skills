# RAD Claude Skills

Custom plugins and skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — Anthropic's CLI for Claude. Install everything at once or cherry-pick individual tools.

## What's Here

```
RAD-Claude-Skills/
├── plugins/                           # Full Claude Code plugins (multi-skill bundles)
│   └── rad-seo-optimizer/             # 11 skills, 3 agents, 6 commands, 7 reference docs
│
└── skills/                            # Standalone skills (copy & use individually)
    ├── rad-code-review/               # Professional-grade code review with AI slop detection
    └── rad-context-prompter/          # Context-aware prompt engineering (coming soon)
```

### Plugins vs. Skills

- **Plugins** bundle multiple skills, agents, commands, and reference docs into one installable unit. Install the whole thing.
- **Skills** are standalone — one SKILL.md plus supporting files. Copy a single folder and you're done.

---

## Quick Install

### Option 1: Install Everything

```bash
git clone https://github.com/radesjardins/RAD-Claude-Skills.git
```

Then install whichever components you want:
```bash
# Install the SEO plugin
claude plugins add ./RAD-Claude-Skills/plugins/rad-seo-optimizer

# Install the code review skill
cp -r ./RAD-Claude-Skills/skills/rad-code-review/skill ~/.claude/skills/rad-code-review
cp -r ./RAD-Claude-Skills/skills/rad-code-review/references ~/.ai-shared/ucr/references
cp -r ./RAD-Claude-Skills/skills/rad-code-review/workflows ~/.ai-shared/ucr/workflows
cp -r ./RAD-Claude-Skills/skills/rad-code-review/project-types ~/.ai-shared/ucr/project-types
cp -r ./RAD-Claude-Skills/skills/rad-code-review/templates ~/.ai-shared/ucr/templates
cp -r ./RAD-Claude-Skills/skills/rad-code-review/scripts ~/.ai-shared/ucr/scripts
```

### Option 2: Cherry-Pick Individual Skills

```bash
# Example: install just one SEO skill (AEO optimizer)
mkdir -p ~/.claude/skills
cp -r RAD-Claude-Skills/plugins/rad-seo-optimizer/skills/aeo-optimizer ~/.claude/skills/

# Example: install just the code review skill
cp -r RAD-Claude-Skills/skills/rad-code-review/skill ~/.claude/skills/rad-code-review
```

> **Note:** Some skills reference shared files. If you get file-not-found errors, also copy the `references/` directory from the same component.

### Verify Installation

Start a new Claude Code session and check:
```
> /skills
```

---

# Available Components

## Plugins

| Plugin | Skills | Agents | Commands | What It Does |
|--------|--------|--------|----------|-------------|
| [RAD SEO Optimizer](#rad-seo-optimizer) | 11 | 3 | 6 | Full SEO toolkit — audits, AEO, keywords, competitors, link building, schema, reports |

## Standalone Skills

| Skill | What It Does |
|-------|-------------|
| [RAD Code Review](#rad-code-review) | Professional-grade code review — AI slop detection, security, architecture, release readiness |
| RAD Context Prompter | Context-aware prompt engineering and optimization (coming soon) |

---

# RAD Code Review

Professional-grade code review skill that catches AI-generated code issues, security vulnerabilities, architecture problems, and release blockers.

## What It Does

UCR performs **three review roles** on every run:

1. **Bug Finder** — Functional defects, logic errors, race conditions, edge cases, and AI-specific failures (hallucinated imports, fake error handling, placeholder stubs, silent failures)
2. **Architecture Reviewer** — Structure, coupling, naming, abstraction quality, test coverage gaps, performance issues, and maintainability
3. **Release Gate** — Security (OWASP), accessibility, license compliance, dependency vulnerabilities, secret exposure, and documentation completeness

Each finding includes severity, category, file location, code evidence, and a concrete fix suggestion.

## Usage

```
/review                              # Review current diff (default)
/review --scope repo                 # Review entire repository
/review --scope commit               # Review last commit
/review --scope tree                 # Review working tree changes
/review --strictness production      # Strict review for production
/review --strictness public          # Strictest — for public/open-source release
```

Or just ask naturally:
```
Review this codebase for release readiness.
Run a security-focused review on the src/ directory.
Check this PR for AI slop and architecture issues.
```

## Review Scopes

| Scope | What It Reviews | When To Use |
|-------|----------------|-------------|
| `diff` | Staged/unstaged changes or PR diff | Default for PRs and quick checks |
| `commit` | Specific commit(s) | Post-merge review |
| `tree` | All modified files in working tree | Before committing |
| `repo` | Entire repository | First-time audit or major releases |

## Strictness Levels

| Level | What It Means |
|-------|-------------|
| `mvp` | Lenient — focus on blockers only (early development) |
| `production` | Balanced — catches issues that would cause production incidents |
| `public` | Strictest — everything a public/open-source release needs (security, licensing, docs) |

## Review Categories

| Category | What It Checks |
|----------|---------------|
| Functional Correctness | Logic errors, edge cases, race conditions, state corruption |
| Security (OWASP) | Injection, XSS, CSRF, auth issues, secrets exposure |
| AI Slop Detection | Hallucinated APIs, shallow error handling, copy-paste divergence, placeholder code |
| Architecture | Coupling, boundaries, patterns, naming, extensibility |
| Tests | Coverage gaps, flaky tests, missing edge case tests |
| Performance | N+1 queries, memory leaks, unnecessary re-renders, algorithmic complexity |
| UI/UX | Usability issues, accessibility (WCAG), responsive design |
| Dependencies | Vulnerable packages, license conflicts, outdated dependencies |
| Documentation | Missing or misleading docs, API contract issues |
| Release Readiness | Migration safety, rollback plan, monitoring, feature flags |

## Project Type Modules

UCR adapts its review focus based on your project type:

| Module | Focus Areas |
|--------|------------|
| Web App | SSR/CSR, routing, state management, SEO, performance |
| API | REST/GraphQL conventions, auth, rate limiting, versioning |
| Chrome Extension | Manifest v3, permissions, content scripts, CSP |
| CLI Tool | Argument parsing, exit codes, signals, output formatting |
| Library | API design, semver, tree-shaking, type exports |
| Electron App | IPC security, native modules, auto-update, packaging |
| Mobile App | Platform conventions, offline support, permissions, deep linking |
| SaaS | Multi-tenancy, billing, onboarding, data isolation |

## What You Get

A structured report with:
- **Severity-ranked findings** (Blocker, Critical, Major, Minor, Nit)
- **Release verdict** (Ship / Ship-with-caveats / Block)
- **Code evidence** for every finding (file, line, snippet)
- **Fix suggestions** with concrete code changes
- **Optional auto-fix** — UCR can apply fixes for blockers and critical issues

## Installation

**Using the install script:**
```bash
cd RAD-Claude-Skills/skills/rad-code-review

# Unix / macOS / Git Bash
./install.sh

# Windows PowerShell
.\install.ps1
```

**Manual:**
```bash
mkdir -p ~/.claude/skills/rad-code-review
cp skill/SKILL.md ~/.claude/skills/rad-code-review/

mkdir -p ~/.ai-shared/ucr
cp -r references workflows project-types templates scripts ~/.ai-shared/ucr/
chmod +x ~/.ai-shared/ucr/scripts/*.sh
```

For full details, see the [RAD Code Review README](skills/rad-code-review/README.md).

---

# RAD SEO Optimizer

## What It Does

The RAD SEO Optimizer is a complete SEO toolkit that turns Claude Code into your personal SEO consultant. It covers:

| Capability | What You Get |
|-----------|-------------|
| **Full Site Audit** | Comprehensive 6-phase audit with a 0-100 score and prioritized fix list |
| **Technical SEO** | Crawlability, Core Web Vitals, mobile, security, redirects — with auto-fix commands |
| **On-Page Optimization** | Title tags, meta descriptions, headings, content quality, E-E-A-T scoring |
| **AI Search Optimization (AEO)** | Get your brand recommended by ChatGPT, Perplexity, Claude, and Google AI Overviews |
| **Keyword Research** | Full pipeline from seed discovery to prioritized keyword plan with topic clusters |
| **Competitor Analysis** | Content gaps, link gaps, SERP features, and AI visibility comparison |
| **Link Building Strategy** | 12-week outreach plan with tactics, templates, and weekly targets |
| **Content Strategy** | Topic authority mapping, content briefs, 12-week editorial calendar |
| **Schema Markup** | JSON-LD generation for 20+ schema types with validation |
| **Broken Link Repair** | Site-wide scanning with redirect chain detection and link reclamation |
| **SEO Report Generation** | Executive report with 30/60/90 day roadmap and Claude Code fix commands |

## Plugin Architecture

```
rad-seo-optimizer/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── skills/                      # 11 interactive skills
│   ├── full-seo-audit/          # Master orchestrator
│   ├── technical-seo/           # Technical audit + auto-fix
│   ├── on-page-optimizer/       # On-page SEO + E-E-A-T
│   ├── aeo-optimizer/           # AI search visibility
│   ├── keyword-discovery/       # Keyword research pipeline
│   ├── competitor-intelligence/ # Competitor analysis
│   ├── link-building-strategy/  # Link acquisition planning
│   ├── content-strategist/      # Content strategy + briefs
│   ├── schema-architect/        # JSON-LD generation
│   ├── broken-link-fixer/       # Broken link scanning
│   └── seo-report-generator/    # Report compilation
├── agents/                      # 3 autonomous agents
│   ├── seo-dominator/           # Full autonomous audit
│   ├── competitor-spy/          # Autonomous competitor research
│   └── content-auditor/         # Content quality assessment
├── commands/                    # 6 slash commands
│   ├── seo-audit.md
│   ├── fix-seo.md
│   ├── keyword-research.md
│   ├── schema-gen.md
│   ├── competitor-check.md
│   └── aeo-check.md
└── references/                  # 7 knowledge base documents
    ├── google-ranking-systems.md
    ├── eeat-checklist.md
    ├── aeo-playbook.md
    ├── link-building-tactics.md
    ├── schema-types-guide.md
    ├── audit-scoring-rubric.md
    └── claude-code-fix-recipes.md
```

---

## Quick Start Commands

These slash commands are the fastest way to use the plugin:

| Command | What It Does | Example |
|---------|-------------|---------|
| `/seo-audit [url]` | Run a comprehensive SEO audit | `/seo-audit https://mysite.com` |
| `/fix-seo [issue]` | Fix a specific SEO issue | `/fix-seo missing meta descriptions` |
| `/keyword-research [topic]` | Discover and prioritize keywords | `/keyword-research organic skincare` |
| `/schema-gen [type]` | Generate JSON-LD schema markup | `/schema-gen FAQ` |
| `/competitor-check [url]` | Quick competitor comparison | `/competitor-check https://competitor.com` |
| `/aeo-check [brand]` | Check AI search visibility | `/aeo-check "My Brand Name"` |

---

## Detailed Skill Guide

### 1. Full SEO Audit (Master Orchestrator)

**What it does:** Runs all 6 audit phases and produces a unified report.

**How to trigger it:**
- "Audit my site for SEO"
- "Run a full SEO audit on mysite.com"
- "Check my SEO health"
- "Grade my website's SEO"
- "I'm getting zero organic traffic — what's wrong?"

**What Claude will ask you:**
1. Your website URL (required)
2. Whether you also have the codebase available locally
3. Your business type and target audience
4. Your top 2-3 competitors
5. Your primary business goal (leads, sales, brand awareness)

**What you'll get back:**
- Overall score (0-100) with letter grade
- Category-by-category breakdown with individual scores
- Critical issues (fix immediately) with exact Claude Code commands
- Warnings (fix within 30 days)
- Opportunities (nice to have)
- 30/60/90 day implementation roadmap
- AEO readiness assessment

**Example interaction:**
```
You: Can you audit my website's SEO? It's a Next.js app in this directory
     and the live site is at https://mybakery.com

Claude: I'll run a comprehensive 6-phase SEO audit. Let me ask a few questions first:
        1. What type of business is this? (bakery, I see from the site)
        2. Who are your top 2-3 competitors?
        3. What's your primary goal — local foot traffic, online orders, or brand awareness?

You: It's a local bakery in Portland. Competitors are Ken's Artisan Bakery
     and Grand Central Baking. Goal is more online orders.

Claude: [Runs 6-phase audit and produces scored report with findings like:]

        # SEO Audit Report: My Bakery
        Overall Score: 47/100 (Grade: F)

        ## Critical Issues
        ### 1. No LocalBusiness Schema Markup
        - Impact: High | Effort: Quick Fix
        - What's wrong: Your site has no structured data telling Google
          you're a local bakery with an address, hours, and menu.
        - Why it matters: Without this, you won't appear in Google's
          local pack (the map results) for "bakery near me" searches.
        - Fix with Claude Code:
          claude "Add LocalBusiness JSON-LD schema to the homepage..."
```

---

### 2. Technical SEO

**What it does:** Deep dive into your site's technical foundation.

**How to trigger it:**
- "Check my Core Web Vitals"
- "Why aren't my pages showing up in Google?"
- "Audit my robots.txt and sitemap"
- "I have crawl errors in Search Console"
- "My site is slow on mobile"

**What it checks:**
- robots.txt (blocking important pages?)
- XML sitemap (exists? complete? valid?)
- Canonical tags (missing? conflicting?)
- Core Web Vitals (LCP < 2.5s, INP < 200ms, CLS < 0.1)
- Mobile-first compliance
- HTTPS and security headers
- URL structure
- JavaScript rendering / SSR
- Redirect chains

**What you'll get:**
Every finding includes three things:
1. **Plain English explanation** of what's wrong and why it matters
2. **Exact Claude Code command** to fix it
3. **Expected ranking impact** of making the fix

---

### 3. On-Page Optimizer + E-E-A-T

**What it does:** Optimizes individual pages for maximum search visibility.

**How to trigger it:**
- "Optimize this page for SEO"
- "Why isn't this page ranking for [keyword]?"
- "Check the E-E-A-T signals on my blog posts"
- "How do I improve this page's search rankings?"

**What it analyzes per page:**
- Title tag (length, keyword placement, uniqueness)
- Meta description (length, keyword, call-to-action)
- Heading hierarchy (H1-H6 structure)
- Content quality score (depth, originality, readability, intent match)
- E-E-A-T signals (author bios, credentials, citations, dates, trust markers)
- Image optimization (alt text, dimensions, format, lazy loading)
- Internal linking (contextual links, anchor text quality)
- AEO-ready formatting (question headings, direct answers, quotable stats)

**E-E-A-T Scoring:** Each page gets scored on Google's Experience, Expertise, Authoritativeness, and Trustworthiness framework. This is especially important for YMYL (Your Money or Your Life) topics like health, finance, and legal content.

---

### 4. AEO Optimizer (AI Search Visibility)

**What it does:** Makes your brand visible and recommended by AI search engines.

**How to trigger it:**
- "How do I get recommended by ChatGPT?"
- "Our competitors show up in Perplexity but we don't"
- "Optimize for AI search"
- "What is AEO / GEO?"
- "How do I appear in Google AI Overviews?"

**The 8-Phase AEO Process:**

| Phase | What Happens |
|-------|-------------|
| 1. AI Visibility Audit | Score your brand across 6 dimensions on 5 AI platforms |
| 2. LLM Seeding Strategy | Optimize what and where you publish for AI citation |
| 3. Consensus & Consistency | Ensure brand info matches across the web |
| 4. Content Conversion | Reformat content to be AI-extractable |
| 5. Co-Citation Strategy | Get mentioned alongside industry leaders |
| 6. Platform Optimization | Tactics for ChatGPT, Perplexity, Claude, Google AI |
| 7. Visual Optimization | Optimize images for AI image processing (CLIP) |
| 8. Distribution Plan | UGC hubs, digital PR, syndication strategy |

**AI Visibility Score:** Your brand is scored 0-60 across 6 dimensions:
- **Presence** (0-10): Are you mentioned at all?
- **Accuracy** (0-10): Is the info correct?
- **Sentiment** (0-10): Is the tone positive?
- **Position** (0-10): Are you first mentioned or buried?
- **Completeness** (0-10): Does AI capture your full value?
- **Consistency** (0-10): Do all AI platforms agree?

---

### 5. Keyword Discovery

**What it does:** Complete keyword research pipeline from zero to prioritized plan.

**How to trigger it:**
- "What keywords should I target?"
- "Do keyword research for [my business/niche]"
- "Find keyword opportunities in [industry]"
- "What are people searching for in [topic]?"
- "Build a keyword strategy for my site"

**The 6-Phase Pipeline:**

1. **Seed Discovery** — Claude asks about your business, audience, and competitors, then generates initial keyword seeds
2. **Expansion** — Expands seeds into long-tail, question-based, and modifier keywords (150-300 total)
3. **Intent Classification** — Classifies every keyword: Informational, Commercial, Transactional, or Navigational
4. **Difficulty Assessment** — Evaluates competition level and rankability
5. **Topic Clustering** — Organizes into pillar topics, subtopics, and supporting content
6. **Prioritization** — Produces three lists:
   - **Quick Wins** — Low competition, high relevance (rank fast)
   - **Strategic Targets** — High value, moderate competition (medium-term)
   - **Long-Term Plays** — High competition, high reward (worth the investment)

**What you'll get:**
A complete keyword plan with content type recommendations (blog post, landing page, guide, tool, FAQ, case study) for each keyword.

---

### 6. Competitor Intelligence

**What it does:** Deep competitive SEO analysis with actionable gap identification.

**How to trigger it:**
- "Analyze my competitors' SEO"
- "Why does [competitor] rank higher than me?"
- "What are my competitors doing differently?"
- "Do a competitive SEO audit"
- "Find content gaps vs my competitors"

**What it analyzes:**
- **Content Gaps** — Topics competitors cover that you don't
- **Technical Comparison** — Speed, schema, mobile, URL structure
- **Link Gap Analysis** — Who links to them but not you
- **SERP Feature Mapping** — Who owns featured snippets, FAQ results, People Also Ask
- **AI Visibility Comparison** — Who gets recommended by ChatGPT/Perplexity/Claude

**Output:** Ranked opportunity list with effort estimates and specific tactics for each gap.

---

### 7. Link Building Strategy

**What it does:** Creates a comprehensive backlink acquisition plan.

**How to trigger it:**
- "How do I get more backlinks?"
- "Create a link building strategy"
- "Improve my domain authority"
- "Analyze my backlink profile"

**Tactics covered:**
Skyscraper Technique, Broken Link Building, Moving Man Method, Resource Page Building, Digital PR, HARO/Media Requests, Strategic Guest Posting, Link Reclamation, Competitor Link Gap Outreach, Link Roundups, Podcasting, Testimonials, Content Transformation, Local Community Links, Affiliate Programs, and LLM Co-Citation Strategy.

**What you'll get:**
- Current link profile assessment
- Link gap analysis vs competitors
- Recommended tactics based on your business type and resources
- 6 customizable outreach email templates
- 12-week link building plan with weekly targets

---

### 8. Content Strategist

**What it does:** Builds a data-driven content strategy with editorial calendar.

**How to trigger it:**
- "What should I write about?"
- "Create a content strategy"
- "Build an editorial calendar"
- "Audit my existing content"
- "Plan my blog strategy for SEO"

**What it produces:**
- Topical authority map (what topics you should own)
- Content audit scorecard (rate existing content: keep, update, consolidate, create, remove)
- Content gap analysis vs competitors
- Detailed content briefs with outlines, keyword mapping, and schema recommendations
- 12-week editorial calendar using the 70/20/10 content mix
- Content relaunch recommendations for underperforming pages

---

### 9. Schema Architect

**What it does:** Generates comprehensive JSON-LD structured data.

**How to trigger it:**
- "Add schema markup to my site"
- "Generate JSON-LD for my pages"
- "What structured data do I need?"
- "Audit my schema markup"

**Supported schema types (20+):**
Organization, LocalBusiness, Article, BlogPosting, Product, FAQPage, HowTo, BreadcrumbList, Review, AggregateRating, Event, Course, VideoObject, JobPosting, Recipe, SoftwareApplication, WebSite, ProfilePage, Speakable, and more.

**What you'll get:**
- Auto-detection of which schema types each page needs
- Ready-to-paste JSON-LD code with inline comments
- Rich snippet opportunity analysis
- Validation checklist
- Framework-specific integration guidance (Next.js, React, WordPress, static HTML)

---

### 10. Broken Link Fixer

**What it does:** Scans your entire site for broken links and fixes them.

**How to trigger it:**
- "Find all broken links on my site"
- "Do a link audit"
- "Check for 404 errors"
- "Clean up redirect chains"

**What it scans:**
- Internal links (within your site)
- External links (to other sites)
- Resource links (images, CSS, JS, downloads)
- Redirect chains (3+ hops)
- Mixed content (HTTP resources on HTTPS pages)

**Bonus:** Also finds link reclamation opportunities — unlinked brand mentions and competitor broken links you can capture.

---

### 11. SEO Report Generator

**What it does:** Compiles findings from all audit skills into one executive report.

**How to trigger it:**
- "Generate an SEO report"
- "Summarize the audit findings"
- "Create a 30/60/90 day SEO roadmap"
- "I need a report for my board meeting"

**Report structure:**
1. Executive Summary (plain English for business owners)
2. Score Dashboard with category breakdown
3. AEO Visibility Scores
4. Critical Issues with fix commands
5. Warnings and Opportunities
6. Competitive Analysis Summary
7. 30/60/90 Day Implementation Roadmap
8. Keyword Opportunities
9. Link Building Opportunities
10. Content Recommendations
11. Re-audit Recommendation

> **Important:** Run this AFTER other audit skills. It aggregates findings — it doesn't perform the audits itself.

---

## Autonomous Agents

Agents run independently without step-by-step interaction. Just give them a task and they work autonomously.

### SEO Dominator Agent

**Trigger:** "Run a full SEO audit on my site" or "Audit this codebase for SEO"

Autonomously crawls your codebase or fetches your live site, runs all 6 audit phases, and produces a comprehensive scored report saved as `seo-audit-report.md`.

### Competitor Spy Agent

**Trigger:** "Analyze my competitors' SEO strategy" or "Who are my SEO competitors?"

Autonomously researches competitors, analyzes their content and SEO strategies, and delivers an actionable opportunity report saved as `competitor-intelligence-report.md`.

### Content Auditor Agent

**Trigger:** "Audit my content quality" or "Score my existing content for SEO"

Crawls all content pages, scores each on quality/E-E-A-T/AEO readiness, and recommends keep/update/consolidate/create/remove for each page. Saves as `content-audit-report.md`.

---

## Reference Documents

The plugin includes 7 reference documents that skills consult as needed:

| Document | Contents |
|----------|----------|
| `google-ranking-systems.md` | All known Google ranking systems and how to optimize for each |
| `eeat-checklist.md` | Complete E-E-A-T scoring criteria and audit checklist |
| `aeo-playbook.md` | LLM seeding strategies, co-citation tactics, platform-specific optimization |
| `link-building-tactics.md` | 20+ link building methods with step-by-step execution guides |
| `schema-types-guide.md` | All Google-supported schema types with properties and rich result triggers |
| `audit-scoring-rubric.md` | How scores are calculated, severity levels, and priority matrix |
| `claude-code-fix-recipes.md` | Exact Claude Code commands for fixing every common SEO issue |

These are loaded on-demand — they don't consume context unless a skill explicitly references them.

---

## Scoring System

### Unified Score (0-100)

The audit produces a weighted composite score:

| Category | Weight |
|----------|--------|
| Technical SEO | 20% |
| On-Page SEO | 15% |
| Content Quality & E-E-A-T | 20% |
| Schema & Structured Data | 10% |
| Internal Linking | 10% |
| Page Speed & Core Web Vitals | 10% |
| Mobile & Accessibility | 5% |
| AEO Readiness | 10% |

### Grade Scale

| Score | Grade | What It Means |
|-------|-------|--------------|
| 90-100 | A+ | Excellent — maintain and optimize for growth |
| 80-89 | A | Strong — minor improvements available |
| 70-79 | B | Good — targeted fixes will yield ranking gains |
| 60-69 | C | Average — significant optimization opportunity |
| 50-59 | D | Below average — systematic improvements needed |
| 0-49 | F | Critical — fundamental issues blocking performance |

### Priority Ranking

Every fix recommendation is scored:
- **Impact** (1-10): How much will this improve rankings?
- **Effort**: Quick Fix (< 30 min) / Moderate (1-4 hrs) / Project (1+ days)
- **Priority** = Impact / Effort — highest priority fixes come first

---

## Tips for Best Results

1. **Start with `/seo-audit`** — Get the full picture before diving into specifics
2. **Have your codebase open** — Claude can read and fix your actual code, not just give advice
3. **Provide competitor URLs** — Better competitor data = better recommendations
4. **Be specific about your business** — "Local bakery in Portland" gets better results than just a URL
5. **Use the fix commands** — Every issue includes an exact Claude Code command you can run
6. **Re-audit after fixes** — Run the audit again after implementing changes to track improvement
7. **AEO is the differentiator** — Most SEO tools ignore AI search. This one doesn't.

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed and authenticated
- A website URL and/or local codebase to audit
- Internet access (for live site fetching and competitor research)

---

# Coming Soon

| Skill/Plugin | Status | Description |
|-------------|--------|-------------|
| RAD Context Prompter | In Progress | Context-aware prompt engineering and optimization |
| RAD Gem Creator | Planned | Create polished Google Gemini gems with optimized prompts |
| RAD GPT Creator | Planned | Build custom OpenAI GPTs with structured configuration |
| RAD PARA Second Brain | Planned | Implement the PARA method (Projects, Areas, Resources, Archives) for knowledge management |

---

## Requirements (All Components)

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed and authenticated
- Internet access (for skills that fetch web content)

---

## License

MIT License — free to use, modify, and distribute.

---

## Contributing

Found a bug? Have an idea for a new skill? Open an issue or PR at [github.com/radesjardins/RAD-Claude-Skills](https://github.com/radesjardins/RAD-Claude-Skills).

---

Built with Claude Code by RAD
