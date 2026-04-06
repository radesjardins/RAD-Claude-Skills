# RAD Claude Skills — Repo Marketing & Discoverability Plan

**Date:** 2026-04-06
**Status:** Approved for implementation
**Approach:** B (Helpful Presence + Organic Discovery) with C (Content Anchor) as a long-game addition

---

## Context

RAD Claude Skills (`github.com/radesjardins/RAD-Claude-Skills`) is a personal open-source project — 20 plugins, 180+ skills, 13 autonomous agents for Claude Code. The immediate goal is organic discovery, community awareness, and gathering feedback. RadOrigin (the future brand connection) is intentionally not foregrounded at this stage.

**Constraints:**
- Limited time — can't sustain high-frequency posting or community management
- No promotional budget — organic only
- Personal social media presence exists (small, genuine audience)
- dev.to account already created with an honest intro post (no forced promotion, repo link in profile)
- Target audience: both coders and non-coders who use Claude Code

---

## Section 1: GitHub Foundation

All one-time work. Runs passively after setup.

### Repo Description
Set the GitHub repo description to:
> *180+ skills and plugins for Claude Code — code review, SEO, brainstorming, React, Next.js, TypeScript, accessibility, and more. Free, open source, Apache 2.0.*

### Topics
Add the following topics to the repo (GitHub Settings → Topics):
```
claude-code
claude
anthropic
ai-tools
developer-tools
claude-code-plugins
code-review
seo
react
nextjs
typescript
accessibility
productivity
open-source
```

### GitHub Profile README
Create `radesjardins/radesjardins/README.md` — a personal profile page visible at `github.com/radesjardins`. Content: 4-5 lines covering who you are, what you build, and a direct link to RAD Claude Skills. Keep it honest and understated — no corporate framing.

### Social Preview Image
Set a custom Open Graph image for the repo (GitHub Settings → Social Preview). When the repo URL is shared on Discord, Reddit, Twitter, or Slack, this card is what people see. A clean image with the repo name and tagline ("180+ skills for Claude Code") makes shared links look intentional.

### Pin the Repo
Pin `RAD-Claude-Skills` to your GitHub profile so it's the first thing any profile visitor sees.

---

## Section 2: README Polish

**Goal:** Every plugin README hooks both coders and non-coders in the first 3 seconds. Lead with the payoff, then the story, then the technical detail.

### Standard Formula
```
# Plugin Name — [one punchy line: what problem does it solve?]

[2-3 sentence story: what was hard before, what's easy now]

## What You Can Do With This
[2-3 concrete use cases, written for humans]

## How It Works
[skills/agents table — technical detail]

## Usage / Quick Start
[install + trigger phrases]
```

### Tier 1 — Priority Rewrites (flagship plugins, tell the full story)
- **rad-code-review** — most sophisticated plugin, deserves the strongest narrative. The "AI slop detection" and "blame-aware diff scoping" angles are genuinely unique.
- **rad-brainstormer** — 10 structured methodologies + 3 autonomous agents is unusually deep. The README undersells it.
- **rad-seo-optimizer** — 12 skills + AEO/AI visibility optimization is rare. The AEO angle specifically is something most SEO tools don't touch.
- **rad-stack-guide** — the orchestrator story. Must clearly explain: works alone, works better with all other rad-* plugins. The "workshop that organizes your tools" framing is the right one.

### Tier 2 — Same Formula, Lighter Lift
- rad-react, rad-typescript, rad-nextjs, rad-fastify, rad-a11y, rad-google-workspace, rad-agentic-company-builder, rad-session, rad-coolify-orchestrator, rad-chrome-extension, rad-astro

### Tier 3 — Quick Pass (opening line improvement only)
- rad-zod, rad-stripe-fastify-webhooks, rad-context-prompter, rad-para-second-brain, rad-supabase

### Root README
Already reads like a marketplace — that's correct. Add a short "Why these plugins?" narrative paragraph above the tables to tell a story, not just list entries.

---

## Section 3: Community Seeding

### Where to Be
| Community | Why |
|-----------|-----|
| Claude Code Discord | Direct audience — daily Claude Code users |
| r/ClaudeAI | Active, searchable, Google-indexed |
| r/ChatGPTCoding | Broader AI coding audience |
| dev.to | Already started — honest intro posted, repo in profile |
| GitHub Discussions (own repo) | Searchable Q&A, Google-indexed |

### Three-Phase Play

**Phase 1: Lurk and learn (1-2 weeks, ~30 min total)**
Read threads. Map recurring pain points with Claude Code. Note what questions come up that your plugins solve. Don't post anything yet.

**Phase 2: Be genuinely helpful (2-4 weeks, 2-3 interactions)**
Answer questions you actually know the answer to. No links to the repo yet. Build a small reputation before you need it.

**Phase 3: Natural introduction**
When someone asks a question your plugins directly solve, answer the question fully first — then mention the plugin as an optional next step. The sequence matters: help first, share second.

### One Launch Post
After README polish is complete, post once in r/ClaudeAI:
> *"I've been building Claude Code plugins for a few months — open sourced everything. 20 plugins, 180+ skills. Here's what's in it."*
Short, factual, no hype. Link to the repo. Let the work speak.

### Personal Social Media
Share the same post or a condensed version on existing personal accounts. Tags: `#ClaudeCode` `#AnthropicAI` `#OpenSource` `#DeveloperTools`. Once. Not repeated.

### GitHub Discussions — Enable Now
Turn on Discussions in repo settings. Seed with two threads:
- *"Which plugin are you using? What's working?"*
- *"Plugin requests and ideas"*

Makes the repo feel like a community, not just a download page.

---

## Section 4: Ongoing Rhythm

**Per new plugin shipped:**
1. Update root README (already standard practice)
2. One sentence on personal social: *"New plugin: rad-[x] — [one line]. Link in bio."*
3. If it solves a known community pain point — drop one comment in a relevant thread where it fits naturally. Not a new post.

That's the full cadence. No blog post required unless the plugin is a genuine standout.

---

## Section 5: Long Game — Content Anchor (Approach C, no deadline)

When bandwidth allows, write one high-quality dev.to post:
> *"How I built 20 Claude Code plugins and what I learned"*

This is the kind of piece that:
- Ranks in Google for "Claude Code plugins"
- Gets linked in newsletters and Discord threads by other people
- Compounds for years without ongoing maintenance

Not a priority now. A seed to plant when there's a quiet afternoon.

---

## Implementation Order

1. GitHub foundation (topics, description, profile README, social card, pin) — do first, one sitting
2. Tier 1 README rewrites (rad-code-review, rad-brainstormer, rad-seo-optimizer, rad-stack-guide)
3. Root README narrative paragraph
4. Enable GitHub Discussions + seed threads
5. Tier 2 README rewrites
6. Community Phase 1 (lurk)
7. Launch post (after README work is complete)
8. Tier 3 README quick passes
9. Community Phase 2 + 3 (organic, ongoing)
10. Content anchor post (future, no deadline)

---

## Success Criteria

- Repo has relevant GitHub topics applied
- Every plugin README hooks in the first 3 seconds
- GitHub Discussions enabled with seed threads
- At least one genuine launch post in r/ClaudeAI after README polish
- dev.to presence established (already done)
- Organic stars/forks begin without paid promotion
- First external contributor interaction (star, fork, Discussion reply, or issue) within 60 days of launch post
