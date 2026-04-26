---
name: write
description: >
  This skill should be used when the user says "write me a...", "draft a...", "create a...",
  "I need a...", "compose a...", "write an email", "draft a blog post", "create a report",
  "write a LinkedIn post", "draft a presentation", "write web copy", "compose a memo",
  or wants any non-code text written from scratch. Handles 9 writing domains: email, blog,
  web copy, business report, research/academic, presentation, prose/essay, technical docs,
  and social media. Gathers context before writing, avoids AI writing patterns, and optionally
  writes in the user's voice profile.
argument-hint: "[what to write] [--domain email|blog|web-copy|report|research|presentation|prose|technical|social] [--coach]"
---

# Write Skill

Generate domain-appropriate text from scratch with AI pattern avoidance baked in — not as a post-processing step, but as a constraint during generation.

## Setup

**Check for voice profile:**
- If file system available, check for `~/.rad-writer/profiles/default.md` or a named profile
- If found, load and apply voice patterns during generation
- If not found, proceed with clean domain-appropriate style

## Process

### Step 1: Detect Domain

Infer the writing domain from the user's request. If ambiguous, ask:

> What kind of writing is this?
> 1. Email
> 2. Blog post / article
> 3. Website copy
> 4. Business report / memo / proposal
> 5. Research / academic
> 6. Presentation (slides / speaker notes)
> 7. Prose / essay
> 8. Technical documentation
> 9. Social media / short-form

Once determined, load the domain reference:
`${CLAUDE_SKILL_DIR}/../../references/domain-[type].md`

### Step 2: Gather Context

Ask domain-specific questions BEFORE writing. Pull questions from the domain reference file's "Context-gathering questions" section.

**Rules:**
- Never ask more than 3-4 questions
- Skip questions the user already answered in their request
- If the user provided attachments or rich context, extract answers from those
- If the user says "just write it" with minimal context, do your best and note assumptions

**Domain question examples:**

| Domain | Key questions |
|--------|--------------|
| Email | Who's the recipient? What's the relationship? What's the ask? Tone? |
| Blog | Topic? Target reader? Key takeaway? Your angle/thesis? |
| Web copy | Product/service? Target customer? Awareness level? Desired action? |
| Report | Audience? Purpose (inform/recommend/persuade)? Key data points? |
| Research | Target publication? Section? Discipline? |
| Presentation | Context (keynote/update/pitch)? Audience expertise? Time constraint? |
| Prose | Topic? Publication/context? Argument or story? |
| Technical | What are you documenting? Who's the reader? What should they do after? |
| Social | Platform? Goal? Audience? |

### Step 3: Generate

**Load now** (needed for generation):
- `${CLAUDE_SKILL_DIR}/../../references/ai-writing-patterns.md`
- `${CLAUDE_SKILL_DIR}/../../references/word-blocklist.md`
- `${CLAUDE_SKILL_DIR}/../../references/sentence-craft.md`

Write the text following these constraints:

**Domain conventions:**
- Follow the positive patterns from the loaded domain reference
- Avoid the domain-specific anti-patterns

**AI pattern avoidance (active during generation, framed honestly):**

Generate writing that doesn't trip the patterns in `ai-writing-patterns.md`. The goal is craft quality — *this writing happens to also avoid the structural patterns associated with AI output, but framing this as "evading detection" is dishonest in 2026 (perfect AI detection is mathematically impossible — see arXiv:2509.11915).*

Concrete generation constraints:
- Avoid words from the always-avoid list in `word-blocklist.md` (these are stale clichés regardless of who's writing)
- Vary sentence length deliberately (target SD > 7)
- Vary paragraph length — mix short and long
- Use transitions when they mark a real turn in the argument, not as mechanical glue (Furthermore, Additionally, Moreover)
- Em dashes sparingly — max ~2-3 per 250 words; reserve for genuine emphasis or interruption
- No throat-clearing openers ("It's important to note...", "In today's [X] landscape...")
- No performative hedging clusters ("may potentially," "could possibly")
- Break the topic-sentence → evidence → summary formula sometimes
- Don't reflexively use rule-of-three lists; vary list lengths
- **Include specific, concrete detail per major section** (named cases, numbers, dates — this is the durable Tier 1 signal of human writing)
- Use the same word for the same concept; resist synonym rotation
- Replace "serves as" / "stands as" with "is" wherever it works

**Voice profile (if loaded):**
- Match the sentence length distribution from the profile
- Use the vocabulary level and word preferences
- Match the tone attributes (formality, warmth, directness)
- Apply distinctive markers (fragments, rhetorical questions, etc.)
- Respect anti-patterns (words/structures the writer avoids)

### Step 4: Long Document Handling

For substantial drafts (more than approximately 1 page):

**First large draft in a session — framing note (once, non-repeating):**
> I'll generate a full draft based on your context. This works best as a starting point for your own revision — not a final product.

**Section-by-section generation:**
1. Outline the sections first, share with user
2. Generate each section, pausing between major sections for user feedback
3. Carry forward a rolling context summary (~200 words) between sections:
   - Key terminology established
   - Argument flow and narrative arc
   - Tone baseline
4. User can redirect between sections ("make that section more specific" or "skip ahead")

### Step 5: Output

**Platform adaptation:**
- **CLI/Desktop with file system:** Offer to save to a file. Display in chat as well.
- **claude.ai:** Output in chat. For longer content, use artifacts when appropriate.
- **All platforms:** Output clean, ready-to-use text. No meta-commentary mixed into the output.

## Coach Mode

If `--coach` flag is set or user says "explain your choices" / "turn on coach mode":
- After generating, add brief notes explaining key writing decisions
- Focus on domain-specific choices and AI pattern avoidance decisions
- 1-2 sentences per insight, not a full writing lesson

## Critical Rules

1. **Avoid the always-avoid blocklist words** — these are clichés regardless of authorship
2. **Vary sentence and paragraph length deliberately** — target burstiness SD > 7
3. **Gather context before writing** — don't generate blindly from a vague request
4. **Respect the domain** — an email and a research paper have different rules
5. **Voice profile is an enhancement, not a gate** — produce good output without one; with one, treat it as descriptive baseline (see `references/voice-profile-schema.md` on what voice profiles can and can't do)
6. **Don't claim to evade AI detection** — the goal is craft quality. See `references/wikipedia-signs-of-ai-writing.md` on why detection-evasion is not a defensible claim in 2026.
7. **Don't announce the constraints in the output** — just write well. The user reads the text, not the meta-commentary.
