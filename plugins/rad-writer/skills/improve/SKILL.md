---
name: improve
description: >
  This skill should be used when the user says "improve this", "make this better", "clean this up",
  "rewrite this", "fix this writing", "polish this", "edit this", "tighten this up", "help me
  rewrite", "make this more professional", "make this sound better", "make this less AI",
  "humanize this", or pastes/uploads text and wants it improved. Takes existing text and produces
  an improved version with numbered changes the user can accept or reject individually.
  Works across all 9 writing domains with domain-aware improvements and light AI pattern detection.
argument-hint: "[paste text or provide file path] [--domain email|blog|web-copy|report|research|presentation|prose|technical|social] [--coach]"
---

# Improve Skill

Take existing text and make it better. Produce an improved version with numbered, trackable changes the user controls.

## Setup

**Check for voice profile:**
- If file system available, check for `~/.rad-writer/profiles/default.md` or named profile
- If found, use as a target for voice consistency

## Process

### Step 1: Receive Text

Accept text via:
- **Paste in chat** — user pastes directly
- **File path** — user provides a path (CLI/Desktop)
- **Upload** — user uploads a document (claude.ai/Desktop)

If the user says "improve this" without text, ask: "Paste the text you'd like me to improve, or provide a file path."

### Step 2: Detect Domain

Infer the domain from content:
- Email signatures, greetings, subject lines → email
- Headings, subheadings, blog-style openings → blog
- CTAs, product language, conversion-oriented → web copy
- Executive summaries, data references, formal tone → business report
- Citations, methodology, abstract → research
- Slide markers, bullet-heavy, speaker notes → presentation
- Essay structure, narrative voice, personal → prose
- Code references, steps, API language → technical
- Short-form, hashtags, platform markers → social

If uncertain, ask. Load: `${CLAUDE_SKILL_DIR}/../../references/domain-[type].md`

### Step 3: Analyze and Improve

**Load now** (needed for analysis):
- `${CLAUDE_SKILL_DIR}/../../references/ai-writing-patterns.md`
- `${CLAUDE_SKILL_DIR}/../../references/word-blocklist.md`
- `${CLAUDE_SKILL_DIR}/../../references/sentence-craft.md`

Read the full text. Identify improvements in these categories:

1. **Clarity** — vague language, ambiguous references, unnecessarily complex sentences
2. **Structure** — paragraph organization, flow, transitions, section order
3. **Word choice** — AI blocklist words, weak verbs, vague adjectives, jargon misuse
4. **Sentence craft** — uniformity, rhythm, variety (check burstiness)
5. **Domain conventions** — does it follow the patterns for this type of writing?
6. **AI patterns** — light pass for tells (em dashes, hedging clusters, mechanical transitions, throat-clearing). Flag naturally alongside other improvements, not as a separate category
7. **Tone** — appropriate for audience? Consistent? Voice profile alignment (if loaded)?

**Number every change.** Each improvement gets a unique number.

### Step 4: Present Suggestions

**Short documents (~1 page or less):**

Show the improved version with numbered inline changes:

```
Hi Sarah,

[1] I wanted to follow up on → Following up on our conversation
Thursday about the Q3 roadmap.

[2] It's important to note that → [removed — throat-clearing]
the timeline has shifted.

We're now targeting August 15 for
[3] the deliverable → the beta release [be specific]
```

Then present the menu:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[N] changes suggested

1. Accept all — show clean version
2. Review individually — accept/reject each
3. Explain changes — show reasoning for each
4. Revise further — additional pass
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Long documents (multi-page):**

1. Detect section breaks (headings, chapters, natural divisions)
2. Process each section with full attention
3. Carry forward a rolling context summary (~200 words) between sections:
   - Key terminology established in earlier sections
   - Structural decisions (argument flow, narrative arc)
   - Issues already flagged (avoid redundant findings)
   - Tone and voice baseline detected in opening sections
4. Present section-by-section summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMPROVEMENT SUMMARY — [document name] ([N] suggestions)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

By section:
  Executive Summary:  [1-3]   2 clarity, 1 AI pattern
  Methodology:        [4-6]   1 passive voice, 2 structure
  Findings:           [7-11]  3 clarity, 2 word choice
  Recommendations:    [12-14] 1 structure, 2 tone

1. Accept all — write clean version
2. Walk through all — one at a time
3. Walk through by section — pick a section
4. Show annotated version — inline comments
5. Explain changes — show reasoning for all
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 5: Handle User Choices

**Accept all:** Output the clean improved version.

**Review individually:** Walk through each change:
```
Change [1]: "I wanted to follow up on" → "Following up on"
  Category: Clarity
  Accept (a) / Reject (r) / Explain (e)?
```

**Accept by number:** User can say "accept 1, 3, 7-11, reject the rest"

**Accept by section:** User can say "accept all in Executive Summary, walk through Findings"

**Explain changes:** For each suggestion, provide 1-2 sentences on the underlying principle.

### Step 6: Output

After accept/reject is complete:

- **Short text:** Display clean version in chat for copy/paste
- **Long text on CLI/Desktop:** Offer to write clean version to file
- **Long text on claude.ai:** Output as artifact or in chat
- **All platforms:** Clean output only — no tracked changes, no meta-commentary

## Coach Mode

If `--coach` flag or user requests explanations:
- Each suggestion includes a brief note on the writing principle behind it
- Keep explanations to 1-2 sentences
- Focus on patterns the user can apply to future writing, not just this text

## Critical Rules

1. **Number every change** — the accept/reject workflow depends on trackable IDs
2. **Don't rewrite everything** — preserve the writer's voice. Fix problems, don't impose a different style
3. **AI patterns are woven in, not separate** — flag "delve" as a word choice issue, not as "AI detected"
4. **Long docs get chunked** — never process a multi-page document in one pass without the rolling context summary
5. **The user controls the output** — never auto-apply changes. Always present, then wait
6. **Preserve meaning** — improvements should never change what the text says, only how it says it
