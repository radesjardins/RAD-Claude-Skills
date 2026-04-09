---
name: review
description: >
  This skill should be used when the user says "review this writing", "give me feedback on",
  "critique this", "what can I improve", "how's my writing", "is this any good", "check my
  writing", "writing feedback", "does this sound right", "proofread this", or wants diagnostic
  feedback on existing text without a rewrite. Produces a structured assessment with scored
  categories and specific findings. For thorough multi-pass review of longer or high-stakes
  documents, dispatches the writing-reviewer agent. Works across all 9 writing domains.
argument-hint: "[paste text or provide file path] [--domain email|blog|web-copy|report|research|presentation|prose|technical|social] [--thorough] [--coach]"
---

# Review Skill

Diagnostic feedback on writing quality. Tells you what's working, what's not, and where to focus — without rewriting the text for you.

## Setup

**Check for voice profile:**
- If available, include "voice consistency" as a scored category

## Process

### Step 1: Receive Text

Accept text via paste, file path, or upload (same as improve skill).

### Step 2: Detect Domain

Same domain detection logic as improve skill. Load the corresponding domain reference:
`${CLAUDE_SKILL_DIR}/../../references/domain-[type].md`

### Step 3: Decide Depth

**Standard review (default):** Handle directly within this skill. Appropriate for:
- Documents under ~3 pages
- Quick feedback requests
- Casual "how's this?" checks

**Thorough review:** Dispatch the `writing-reviewer` agent. Triggered when:
- User explicitly asks for thorough/deep review (`--thorough` flag)
- Document is roughly 3+ pages
- User says "really look at this carefully" or similar

When dispatching the agent:
```
I'll run a thorough multi-pass review. This analyzes structure and flow,
sentence-level craft, and AI patterns separately, then consolidates findings.
```

Pass the text, detected domain, and domain reference to the agent.

### Step 4: Analyze (Standard Review)

**Load now** (needed for analysis):
- `${CLAUDE_SKILL_DIR}/../../references/ai-writing-patterns.md` (AI patterns category)
- `${CLAUDE_SKILL_DIR}/../../references/word-blocklist.md` (lexical tells)
- If sentence/structure issues are found: `${CLAUDE_SKILL_DIR}/../../references/sentence-craft.md`

Read the full text. Evaluate across these categories:

**Scored categories (each rated on a 3-point scale: Strong / Adequate / Needs Work):**

1. **Clarity** — Is the meaning immediately clear? Are there ambiguous references, unnecessarily complex sentences, or vague language?

2. **Structure** — Does the document flow logically? Are sections in the right order? Do paragraphs develop ideas or just state them? Are transitions natural?

3. **Voice** — Does the writing have personality? Is the tone consistent and appropriate for the audience? Does it sound like a person or a template?

4. **Domain conventions** — Does it follow the expectations for this type of writing? (e.g., email has a clear ask, research has proper hedging, web copy has CTAs)

5. **AI patterns** — Are there detectable AI writing patterns? (lexical tells, structural uniformity, mechanical transitions, hedging clusters)

6. **Voice consistency** (only if voice profile loaded) — Does the text match the writer's established patterns?

**For each category:** 1-2 sentence justification explaining the rating.

### Step 5: Specific Findings

After the scored overview, list specific findings:

Each finding has:
- **Number** — sequential ID
- **Location** — where in the text (paragraph number, section, or quote)
- **Category** — which scored category it falls under
- **Issue** — what's wrong, specifically
- **Suggestion** — how to fix it

**Priority ranking:** Order findings by impact. Lead with the most important issues.

### Step 6: Present Review

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WRITING REVIEW — [domain type]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall: [2-3 sentence impression — what's working and what needs attention]

  Clarity:           Strong / Adequate / Needs Work — [justification]
  Structure:         Strong / Adequate / Needs Work — [justification]
  Voice:             Strong / Adequate / Needs Work — [justification]
  Domain conventions: Strong / Adequate / Needs Work — [justification]
  AI patterns:       Clean / Minor / Notable — [justification]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINDINGS ([N] total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Top 3 priorities:
1. [Most impactful issue and what to do about it]
2. [Second most impactful]
3. [Third most impactful]

All findings:
[1] [Location] — [Category] — [Issue]. Suggestion: [fix]
[2] [Location] — [Category] — [Issue]. Suggestion: [fix]
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What would you like to do?
1. Dive deeper into a specific category
2. Improve this text — hand off to improve skill
3. Run AI audit — deep AI pattern analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 7: Long Document Handling

For documents longer than ~3 pages (when handling directly, not via agent):

1. Chunk by sections (headings, chapters, natural breaks)
2. Review each chunk with full attention
3. Carry forward rolling context summary (~200 words):
   - Terminology and voice baseline from earlier sections
   - Issues already flagged
   - Structural arc and flow assessment
4. Present section-by-section findings, then rolled-up summary
5. User can drill into any section: "tell me more about the Findings section"

### Step 8: Follow-Up Actions

Based on user's choice:
- **Dive deeper:** Expand on a specific category with more detailed analysis
- **Improve:** Hand text to the improve skill for the accept/reject workflow
- **AI audit:** Hand text to the ai-audit skill for deep pattern analysis

## Coach Mode

If `--coach` flag or user requests:
- Each finding includes a 1-2 sentence explanation of the underlying writing principle
- After the review, offer 2-3 general writing tips based on the patterns observed
- Frame as learning, not criticism

## Critical Rules

1. **Review, don't rewrite** — the distinction between this skill and improve is that review diagnoses. The user does the fixing (or hands off to improve).
2. **AI patterns are one category, not the focus** — unless the user specifically asks about AI patterns, treat them as one of six categories. Don't lead with "this sounds like AI."
3. **Be specific** — "paragraph 3 has three sentences averaging 19 words each" is useful. "Sentence variety could be improved" is not.
4. **Be honest but constructive** — if the writing is bad, say so clearly, but pair every diagnosis with a fix.
5. **Dispatch the agent for thorough reviews** — don't try to do a multi-pass deep review within this skill. That's what the writing-reviewer agent is for.
