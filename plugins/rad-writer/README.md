# rad-writer — Domain-smart writing that doesn't read like AI.

Most AI writing assistance defaults to grammar checking or generic tone adjustments. rad-writer goes further: it knows what good email writing looks like versus good research writing versus good web copy — nine domains, each with their own conventions, anti-patterns, and quality criteria. And it knows the 50+ lexical tells, structural patterns, and rhetorical crutches that mark text as AI-generated, fixing them not by disguising them but by replacing them with genuinely better writing. Four skills, two agents, thirteen reference files built from curated research.

## What You Can Do With This

- Write a follow-up email, a blog post, an executive summary, or a LinkedIn post — with domain-specific context gathering and zero AI tells in the output
- Paste in a document and get numbered suggestions you accept or reject one at a time, with the option to explain the reasoning behind each change
- Get a structured diagnostic review of any piece of writing — scored categories, specific findings, and a prioritized fix list
- Run a deep AI pattern audit that measures burstiness, lexical tells, hedging density, and specificity — with a pattern-by-pattern breakdown and fixes
- Build a voice profile from your own writing samples so Claude writes like you, not like a template

## How It Works

| Skill | Purpose |
|-------|---------|
| `write` | Context-aware drafting across 9 domains — gathers context before writing, avoids AI patterns during generation, writes in your voice profile if available |
| `improve` | Numbered accept/reject suggestions on existing text — preserves your voice while fixing clarity, structure, word choice, and AI patterns |
| `review` | Structured diagnostic with scored categories (clarity, structure, voice, domain conventions, AI patterns) and prioritized findings |
| `ai-audit` | Deep AI pattern analysis — burstiness scores, lexical tell counts, em dash density, hedging density, specificity ratios, rhetorical pattern scan |

| Agent | Purpose |
|-------|---------|
| `writing-reviewer` | Three-pass adversarial review (structure & flow, sentence & word craft, AI pattern scan) for longer or high-stakes documents — dispatched by the review skill or invocable directly |
| `voice-analyst` | Analyzes 3-5 writing samples to generate a structured voice profile capturing your sentence rhythm, vocabulary, tone, structural habits, and personality markers |

## Writing Domains

Every skill adapts to the type of writing. Specify a domain or let the plugin infer it from context:

| Domain | What the plugin knows |
|--------|----------------------|
| Email | Tone calibration across 6+ contexts (cold outreach, colleague, executive, customer, bad news, requests), subject line patterns, the 50-125 word sweet spot, F-pattern scanning, passive-aggressive anti-patterns |
| Blog | 4-Part Hook Formula, In Media Res openings, bucket brigades, voice development ("selfish writing"), STEPPS virality framework, Full Circle endings |
| Web copy | 4U headline formula, Eugene Schwartz awareness levels, PAS framework, FAB product descriptions, first-person CTAs, risk reversal microcopy |
| Business report | Pyramid Principle (MECE), executive summary formula, Action Titles for data, "What-So What-Now What" framework, zombie noun elimination, trade-off framing |
| Research | IMRaD abstract scaffold, literature review synthesis (not summary), "Future Self" methodology test, hedging calibration, discipline-specific conventions (STEM, humanities, social sciences, applied) |
| Presentation | Billboard test, 6x6 rule, SCR framework, Action Titles on data slides, "Measure Twice Cut Once" rehearsal, context-specific expectations (board, sales, training, technical) |
| Prose | Right-branching sentences, Given-Before-New principle, "Burrito Paragraph," Classic Style, show vs. tell, Pull-a-Sentence test, zombie noun elimination |
| Technical | Diataxis framework (tutorial vs. how-to vs. reference vs. explanation), README adoption patterns, "Time to First Call" for API docs, Single Concept Rule for code examples, progressive disclosure |
| Social | LinkedIn hook-story-insight, 10-Tweet Architecture, "No Link" Rule, Zoom-In Ladder, Two-Second Test, 3-2-1 newsletter format, platform-specific conventions (LinkedIn, X, Instagram, Facebook, TikTok) |

## Key Capabilities

- **AI pattern avoidance is structural, not cosmetic** — the write skill never produces AI tells in the first place. The improve and review skills flag them as part of genuine quality improvement, not as a separate "humanizer" pass. 50+ lexical tells, 15+ structural patterns, 10+ rhetorical crutches tracked across the blocklist and pattern references.
- **Chunked long document processing** — rolling context summaries (~200 words) carry forward between sections, preventing the "lost in the middle" problem where AI misses issues in the center of long documents. Every section gets full attention while maintaining document-level coherence.
- **Numbered accept/reject workflow** — every suggestion in the improve skill gets a unique ID. Accept all, reject all, or walk through individually. Accept by number, by section, or in bulk. Explanations are opt-in (coach mode).
- **Platform-agnostic with graceful adaptation** — works on Claude Code CLI, Claude Desktop, and claude.ai. Voice profiles persist on CLI/Desktop (`~/.rad-writer/profiles/`), or export as artifacts for claude.ai Project Knowledge.
- **Editor mode by default, coach mode on demand** — concise suggestions that show the problem and the fix. Toggle coach mode for 1-2 sentence explanations of the underlying writing principle behind each change.
- **Voice profiles** — the voice-analyst agent studies your writing samples and generates a persistent profile of your distinctive patterns. On CLI/Desktop, profiles load automatically. On claude.ai, add the profile to Project Knowledge for persistence across conversations.

## Voice Profiles

The voice-analyst agent studies 3-5 writing samples to build a profile of your distinctive style — sentence length distribution, vocabulary preferences, tone markers, structural habits, and personality quirks.

**On CLI and Desktop:**
```
Analyze my writing voice. Here are some samples: [paste or provide file paths]
```
Profiles save to `~/.rad-writer/profiles/` and load automatically via `@import` in `~/.claude/CLAUDE.md`. Create multiple named profiles for different contexts (professional-email, blog-voice, academic).

**On claude.ai:**
Profiles output as artifacts with instructions to add to Project Knowledge. Every conversation in that Project writes in your voice. The profile includes a header explaining exactly how to set it up.

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-writer
```

Then just ask naturally:

```
Write me a follow-up email to the client about the delayed launch
Draft a blog post about why we redesigned our onboarding
Improve this [paste text]
Review this writing
Does this sound like AI?
```

Or with flags:

```
Write me an email --coach          # Explains writing decisions
Review this report --thorough      # Dispatches writing-reviewer agent for deep 3-pass analysis
AI audit this document             # Full pattern diagnostic with scores
```

## Philosophy

This plugin is not anti-AI. It's anti-*bad*-AI-writing.

The patterns that make AI text detectable — uniform sentence lengths, hollow hedging, mechanical transitions, overused filler words like "delve" and "leverage" — are the same patterns that make any text worse. Fix the writing quality, and the detection problem solves itself.

Using AI to draft is legitimate. Producing drafts full of AI tells, uniform sentence structures, and empty qualifiers is not. This plugin fixes the output quality, which is valuable regardless of who wrote the first draft.

## Platform Support

| Feature | CLI | Desktop | claude.ai |
|---------|-----|---------|-----------|
| All 4 skills | Yes | Yes | Yes |
| File input/output | Yes | Yes | Upload/paste, artifacts |
| Voice profiles | Persistent (`~/.rad-writer/`) | Persistent (`~/.rad-writer/`) | Project Knowledge |
| Long doc chunking | Yes | Yes | Yes |
| Accept/reject workflow | Yes | Yes | Yes |
| Coach mode | Yes | Yes | Yes |

## License

[Apache License 2.0](../../LICENSE)
