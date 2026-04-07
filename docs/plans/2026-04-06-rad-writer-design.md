# rad-writer Design Spec

**Date:** 2026-04-06
**Status:** Approved
**Plugin:** rad-writer
**Tagline:** Domain-smart writing that doesn't read like AI.

---

## 1. Plugin Identity & Positioning

### What it is

A multi-skill writing plugin that helps users write better across 9 domains — or takes AI-assisted drafts and makes them genuinely good. Every skill is informed by deep domain-specific conventions and cross-cutting AI pattern awareness. It doesn't detect AI or evade detectors. It produces better writing.

### What it is NOT

- Not a "humanizer" or detection bypasser
- Not a grammar checker (Grammarly exists)
- Not a creative fiction tool
- Not a coding/development writing tool (other plugins handle that)

### Philosophy

The best way to not sound like AI is to actually write better. The patterns that make AI text detectable are the same patterns that make any text worse — uniform sentence lengths, hollow hedging, mechanical transitions, overused filler words. Fix the writing quality, and the detection problem solves itself.

This plugin is not anti-AI. It's anti-*bad*-AI-writing. Using AI to draft is legitimate. Producing drafts full of "delve," uniform sentence structures, and empty qualifiers is not. The plugin fixes the output quality, which is valuable regardless of who wrote the first draft.

### Form factor

- 4 skills (write, improve, review, ai-audit)
- 2 agents (writing-reviewer, voice-analyst)
- 13 reference files (4 cross-cutting, 9 domain-specific)
- No orchestrator — clean, direct skill routing
- Platform-agnostic: works on Claude Code CLI, Claude Desktop, and claude.ai

---

## 2. Skills

### 2.1 `write`

**Trigger:** "write me a...", "draft a...", "create a...", "I need a...", "compose a..."

**Behavior:** Infers or asks which domain. Runs domain-specific context-gathering questions before writing. Generates a draft following the domain reference conventions with AI pattern avoidance active throughout — not as a post-processing step, but as a constraint during generation.

**Context gathering by domain:**

| Domain | Key questions |
|--------|--------------|
| Email | Who's the recipient? What's the relationship? What's the ask/purpose? Tone? |
| Research | Target publication/audience? Section (abstract, lit review, discussion)? Discipline? |
| Web copy | Product/service? Target customer? Awareness level? Desired action? |
| Business report | Audience (board, team, external)? Purpose (inform, recommend, persuade)? Key data points? |
| Blog | Topic? Target reader? What should they take away? Your angle/thesis? |
| Presentation | Context (keynote, team update, pitch)? Audience expertise? Time constraint? |
| Prose | Topic? Publication/context? What's the argument or story? |
| Technical | What are you documenting? Who's the reader? What should they be able to do after? |
| Social | Platform? Goal (authority, engagement, announcement)? Audience? |

If the user provides rich context upfront (or attachments), the skill skips questions it can already answer. Never asks more than 3-4 questions.

**Long document handling:** For substantial drafts, produces section by section with the user able to review and redirect between sections. Single framing note on first large draft request (non-repeating): "I'll generate a full draft based on your context. This works best as a starting point for your own revision — not a final product."

**Platform adaptation:** On CLI/Desktop with a voice profile active, writes in the user's voice. On claude.ai without one, writes clean domain-appropriate prose. If file system is available, offers to save output to a file.

### 2.2 `improve`

**Trigger:** "improve this", "make this better", "clean this up", "rewrite this", "fix this writing", "polish this"

**Behavior:** Takes pasted text or a file. Infers domain from content (or asks). Produces an improved version with numbered changes. Presents the suggestion workflow:

1. Accept all — show clean output
2. Review individually — accept/reject each change
3. Explain changes — show reasoning for each (coach mode)
4. Revise further — additional pass

**Long document handling:** Chunks by section. Processes each with full attention. Carries forward a rolling context summary (~200 words) so later sections stay coherent with earlier ones. Reassembles complete output.

**AI pattern awareness:** Flags AI tells it finds as part of the improvements — woven into the suggestions, not a separate report. Light touch.

### 2.3 `review`

**Trigger:** "review this writing", "give me feedback on", "critique this", "what can I improve", "how's my writing"

**Behavior:** Diagnostic mode — the user wants feedback, not a rewrite. Reads the text, produces a structured assessment:

- Overall impression (2-3 sentences)
- Scored categories: clarity, structure, voice, domain conventions, AI patterns (each on a simple scale with 1-2 sentence justification)
- Specific findings (numbered, with location, issue, and suggested fix)
- Top 3 priorities to address

**Long document handling:** Same chunked processing with rolling context summary. Section-by-section findings, then a rolled-up summary. The user can drill into any section.

**Distinction from improve:** Review tells you *what's wrong and why*. Improve *does the fixing*. A user might review first, then selectively improve sections they agree need work.

### 2.4 `ai-audit`

**Trigger:** "check for AI patterns", "does this sound like AI", "AI audit", "ai-audit", "check if this reads as human", "humanize check"

**Behavior:** Deep dedicated pass focused exclusively on AI writing patterns. Analyzes:

- Lexical tells (flagged words/phrases from the blocklist with counts and locations)
- Structural tells (sentence length variance, paragraph uniformity, transition patterns)
- Burstiness score (measured sentence length standard deviation, compared to human-typical ranges)
- Hedging density (qualifying language frequency)
- Specificity score (concrete details vs. vague abstractions)

**Output:** A diagnostic report with severity-ranked findings. Not a binary "AI or human" judgment — a pattern-by-pattern breakdown with specific locations and fixes. Explicitly does NOT claim to be an AI detector.

**Relationship to other skills:** The write, improve, and review skills all have light AI pattern awareness baked in. The ai-audit skill is the deep, dedicated pass for when it matters — before publishing, submitting, or sending something where AI patterns would undermine credibility.

---

## 3. Agents

### 3.1 `writing-reviewer`

**Purpose:** Adversarial multi-pass review for longer or higher-stakes documents.

**When invoked:** The `review` skill dispatches this agent when the user explicitly asks for a thorough/deep review, or when the document is long enough to benefit from multi-pass analysis (roughly 3+ pages). For shorter documents or quick feedback requests, the review skill handles it directly without the agent. Also invocable directly by the user.

**Three sequential passes:**

1. **Pass 1: Structure & Flow** — document-level architecture. Does the argument build logically? Are sections in the right order? Is there a clear through-line? Are transitions earned or mechanical?
2. **Pass 2: Sentence & Word** — line-level craft. Sentence variety, word choice, passive voice, hedging, cliches, domain-specific anti-patterns. Loads the relevant domain reference.
3. **Pass 3: AI Pattern Scan** — the ai-audit lens applied to the full document. Lexical tells, structural uniformity, burstiness. Only flags patterns not already caught in Pass 2.

**Output:** Consolidated findings across all three passes, deduplicated, severity-ranked. Each finding has a location, the issue, and a suggested fix. Feeds back into the review skill's numbered accept/reject workflow.

**Long document handling:** Processes chunks but maintains a running document-level context so structural feedback (Pass 1) spans the whole piece.

**Model:** Sonnet

### 3.2 `voice-analyst`

**Purpose:** Analyzes samples of the user's writing to generate a structured voice profile.

**Availability:** CLI and Desktop (persistent profiles). On claude.ai, generates a downloadable artifact the user can add to Project Knowledge.

**Process:**

1. User provides 3-5 writing samples (pasted or as files). More is better, 3 is minimum.
2. Agent analyzes across samples for consistent patterns:
   - Sentence length distribution (mean, variance, range)
   - Vocabulary level and preferences (plain vs. technical, industry-specific terms)
   - Tone markers (formal/informal, warm/clinical, direct/diplomatic)
   - Structural habits (paragraph length, opening patterns, transition style)
   - Distinctive patterns (fragments, rhetorical questions, parentheticals, em dashes)
   - What they *don't* do (anti-patterns specific to this writer)
3. Generates a structured profile in markdown with YAML frontmatter

**Output format:**

```yaml
---
name: [user-chosen name]
created: [date]
samples: [count]
---
```

Followed by sections: Sentence Patterns, Vocabulary, Tone, Structure, Distinctive Markers, Anti-patterns.

**Storage by platform:**

| Platform | Storage | Loading |
|----------|---------|---------|
| CLI | `~/.rad-writer/profiles/[name].md` | Auto-loaded via `@import` in `~/.claude/CLAUDE.md` |
| Desktop | `~/.rad-writer/profiles/[name].md` | Auto-loaded via `@import` in `~/.claude/CLAUDE.md` |
| claude.ai | Artifact output with instructions | User adds to Project Knowledge manually |

**claude.ai guidance:** When on claude.ai, the voice profile artifact includes a header block:

> **How to use this voice profile:**
> 1. Download this artifact or copy its contents
> 2. Open your Claude.ai Project settings
> 3. Add this file to Project Knowledge
> 4. Every conversation in this Project will now use your voice
>
> To use across multiple Projects, add the same file to each Project's Knowledge.

**Profile management:** Can update an existing profile with new samples, tweak specific attributes on request ("make it less formal"), or create multiple named profiles for different contexts.

**Model:** Sonnet

---

## 4. Reference Files

### 4.1 Cross-cutting references (loaded by all skills)

**`ai-writing-patterns.md`**
- Lexical tells: overused verbs (delve, leverage, utilize, harness, streamline), adjectives (pivotal, robust, innovative, seamless), nouns (landscape, realm, tapestry, synergy)
- Phrase tells: "It's important to note that...", "In today's [X] landscape...", "Generally speaking...", "From a broader perspective..."
- Structural tells: uniform sentence length (low standard deviation), balanced paragraph lengths, excessive hedging, formulaic transitions, participial phrase overuse (2-5x human rate), emotional flatness, triple/quintuple list patterns
- Burstiness and perplexity explained as craft concepts, not detection metrics
- Primary source: AI Writing Accountability notebook

**`word-blocklist.md`**
- Words/phrases organized by severity:
  - **Always avoid:** delve, utilize, tapestry, synergy, paradigm, "it's important to note," "in today's [X] landscape"
  - **Context-dependent:** leverage (ok in finance), robust (ok in engineering), comprehensive (ok in research methodology)
- Each entry has: the word/phrase, why it's flagged, 2-3 suggested replacements, frequency data where available
- Primary source: AI Writing Accountability notebook + web research

**`sentence-craft.md`**
- Burstiness as a craft tool: how sentence length variation creates rhythm and momentum
- Techniques: the short punch after a long build-up, fragment use, varying syntactic structure
- Paragraph as unit of thought: development vs. information dumping
- Natural transitions vs. mechanical connectors (Furthermore, Additionally, Moreover)
- Primary source: Effective Writing notebook

**`voice-profile-schema.md`**
- Template definition for voice profiles
- Attribute definitions: what each field means, how to interpret it, valid ranges
- Example profiles at different formality levels
- Instructions for the voice-analyst agent on how to generate profiles
- Instructions for mode skills on how to consume profiles
- Created during plugin development

### 4.2 Domain references (loaded based on writing type)

Each domain reference file follows a consistent structure:

1. **What good [domain] writing looks like** — positive patterns, conventions, structural expectations
2. **Common mistakes** — anti-patterns specific to this domain
3. **Context-gathering questions** — what the write skill should ask
4. **Quality criteria** — what the review skill evaluates against
5. **AI pattern considerations** — domain-specific AI tells (e.g., AI research writing has different tells than AI email writing)

| File | Covers | Key differentiator |
|------|--------|-------------------|
| `domain-email.md` | Tone calibration by context (6+ email types), subject lines, structure, the ask, length guidelines, cultural considerations | Tone shifts across cold outreach, colleague, executive, customer, bad news, requests |
| `domain-blog.md` | Hooks, scanability, voice development, transitions, endings, engagement patterns | What makes readers share vs. just read |
| `domain-web-copy.md` | Headlines, CTAs, conversion patterns, awareness levels (Schwartz framework), microcopy, brand voice | Awareness-level framework for matching copy to buyer stage |
| `domain-business-report.md` | Pyramid principle, exec summaries, data presentation, recommendation framing, Amazon/McKinsey patterns | Writing for decision-makers, not just informing |
| `domain-research.md` | Abstracts, lit review synthesis, methodology, results vs. discussion, hedging calibration, peer review expectations | Discipline-specific conventions across STEM, social sciences, humanities |
| `domain-presentation.md` | Slide text rules, speaker notes, narrative arc, data slides, the billboard test | Writing for spoken delivery, not silent reading |
| `domain-prose.md` | Sentence-level craft, show vs. tell, voice, essay structures (braided, lyric, hermit crab), editing techniques | Craft-level patterns from published writers |
| `domain-technical.md` | Diataxis framework, READMEs, API docs, tutorials vs. how-tos, progressive disclosure | Writing to enable, not just explain |
| `domain-social.md` | LinkedIn, threads, bios, taglines, newsletters, platform conventions, compression techniques | Platform-specific patterns, not generic social media tips |

---

## 5. Workflows & Interactions

### 5.1 Suggestion Workflow

Unified across improve and review skills, scaled by document length.

**Short documents (~1 page or less):**

```
1. Plugin shows improved version with numbered inline changes
2. Menu:
   1. Accept all — show clean version
   2. Review individually — accept/reject each
   3. Explain changes — show reasoning for each
   4. Revise further — additional pass
3. User accepts/rejects by number or in bulk
4. Plugin outputs clean final version for copy/paste
```

**Long documents (multi-page):**

```
1. Plugin detects section breaks (headings, chapters, natural divisions)
2. Processes each section with full attention
3. Carries forward a rolling context summary (~200 words)
4. Presents section-by-section summary with finding counts
5. Menu:
   1. Accept all — write clean version
   2. Walk through all — one at a time
   3. Walk through by section — pick a section
   4. Show annotated version — inline comments at each suggestion
   5. Explain changes — show reasoning for all
6. User accepts/rejects by number, by section, or in bulk
7. Plugin outputs clean final version
```

### 5.2 Rolling Context Summary

The rolling context summary prevents the "lost in the middle" problem when processing long documents. It carries forward between chunks:

- Key terminology established in earlier sections
- Structural decisions (argument flow, narrative arc)
- Issues already flagged (to avoid redundant findings)
- Tone and voice baseline detected in opening sections
- Approximately 200 words, updated after each chunk

### 5.3 Coach Mode

Off by default (editor mode). Activated per-session or per-interaction:

- "Explain your changes" — coach mode for current interaction
- "Turn on coach mode" — coach mode for rest of session
- When active, each suggestion includes a 1-2 sentence explanation of the underlying writing principle

### 5.4 Platform Adaptation

| Capability | CLI | Desktop | claude.ai |
|-----------|-----|---------|-----------|
| Read files as input | Yes | Yes | Upload/paste |
| Write output to file | Yes | Yes | Artifact/copy |
| Voice profiles (persistent) | `~/.rad-writer/profiles/` | `~/.rad-writer/profiles/` | Project Knowledge |
| Voice profile creation | Auto-save to disk | Auto-save to disk | Artifact + instructions for Project Knowledge |
| Chunked long doc processing | Yes | Yes | Yes |
| Accept/reject workflow | Yes | Yes | Yes |

---

## 6. Plugin Structure

```
rad-writer/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── skills/
│   ├── write/
│   │   └── SKILL.md
│   ├── improve/
│   │   └── SKILL.md
│   ├── review/
│   │   └── SKILL.md
│   └── ai-audit/
│       └── SKILL.md
├── agents/
│   ├── writing-reviewer/
│   │   └── AGENT.md
│   └── voice-analyst/
│       └── AGENT.md
└── references/
    ├── ai-writing-patterns.md
    ├── word-blocklist.md
    ├── sentence-craft.md
    ├── voice-profile-schema.md
    ├── domain-email.md
    ├── domain-blog.md
    ├── domain-web-copy.md
    ├── domain-business-report.md
    ├── domain-research.md
    ├── domain-presentation.md
    ├── domain-prose.md
    ├── domain-technical.md
    └── domain-social.md
```

**Totals:** 4 skills, 2 agents, 13 reference files

---

## 7. What Makes This Different

1. **Domain-specific, not generic.** Nine distinct domain references with conventions, anti-patterns, and quality criteria specific to each writing type. "Good email" and "good research paper" are fundamentally different — the plugin knows that.

2. **AI pattern avoidance is structural, not cosmetic.** Not a post-processing "humanizer" pass. The cross-cutting references inform every skill at every step. The write skill never produces AI tells in the first place. The improve and review skills flag them as part of genuine quality improvement.

3. **Chunked long document processing.** Rolling context summaries prevent the "lost in the middle" problem that plagues naive AI document review. Every section gets full attention while maintaining document-level coherence.

4. **Non-adversarial positioning.** Not a detection evader. Not anti-AI. The thesis is that good writing is good writing — and the patterns that make AI text detectable are the same patterns that make any text worse.

5. **Platform-agnostic with graceful adaptation.** Same plugin works on CLI, Desktop, and claude.ai. Voice profiles persist where the platform supports it, with clear guidance for claude.ai's Project Knowledge workaround.

6. **Suggestion workflow with user control.** Numbered changes, accept/reject individually or in bulk, explanations opt-in. The user stays in control of their text.

---

## 8. Source Material

### NotebookLM Notebooks

- **AI Writing Accountability** — feeds `ai-writing-patterns.md`, `word-blocklist.md`, and the AI pattern awareness across all skills
- **Effective Writing** — feeds `sentence-craft.md` and all 9 domain reference files

### Deep Research Prompts

Nine domain-specific deep research prompts were generated to expand source coverage. These target: email, blog/article, web copy, business report, research/academic, presentation, non-fiction prose, technical writing, and social media/short-form. Results should be incorporated into the corresponding domain reference files.

### Web Research

Competitive landscape research covered: AI humanizer tools (Undetectable.ai, WriteHuman, StealthGPT), AI detection tools (GPTZero, Originality.ai, Turnitin), AI writing patterns (lexical, structural, burstiness), writing quality frameworks (Flesch-Kincaid, Hemingway, plain language guidelines), and the non-native English speaker false positive problem in AI detection.
