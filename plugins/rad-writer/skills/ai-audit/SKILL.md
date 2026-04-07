---
name: ai-audit
description: >
  This skill should be used when the user says "check for AI patterns", "does this sound like AI",
  "AI audit", "ai-audit", "check if this reads as human", "humanize check", "AI tells",
  "does this pass AI detection", "check for AI slop", "is this AI-written", "AI pattern check",
  or wants a deep analysis of whether text exhibits AI-generated writing patterns. Produces a
  diagnostic report with measurable scores and specific, located findings. Does NOT claim to be
  an AI detector — reports patterns, not verdicts. Works across all 9 writing domains with
  domain-specific pattern awareness.
argument-hint: "[paste text or provide file path] [--domain email|blog|web-copy|report|research|presentation|prose|technical|social] [--coach]"
---

# AI Audit Skill

Deep, dedicated analysis of AI writing patterns. Not a detector — a diagnostic tool that identifies specific patterns, measures them, and provides actionable fixes.

**What this skill is:** A pattern-by-pattern breakdown that tells you exactly where and how your text exhibits AI-typical characteristics, with specific suggestions for each finding.

**What this skill is NOT:** An AI detector. It does not render verdicts ("this is 73% AI"). It does not claim to determine authorship. It identifies craft problems that happen to correlate with AI output.

## Setup

**Load these references NOW:**
- `${CLAUDE_SKILL_DIR}/../../references/ai-writing-patterns.md` (primary reference for this skill)
- `${CLAUDE_SKILL_DIR}/../../references/word-blocklist.md` (word/phrase scanning)
- `${CLAUDE_SKILL_DIR}/../../references/sentence-craft.md` (fix recommendations)

## Process

### Step 1: Receive Text

Accept text via paste, file path, or upload.

### Step 2: Detect Domain

Same domain detection as other skills. Load domain reference for domain-specific AI tells:
`${CLAUDE_SKILL_DIR}/../../references/domain-[type].md`

Domain matters because AI patterns differ by genre:
- AI emails: over-formal greetings, "I hope this finds you well", mechanical closings
- AI research: "delve" in every section, uniform hedging, overclaiming in abstracts
- AI blog posts: "In today's [X] landscape" openers, listicle structure, no voice
- AI web copy: buzzword-heavy, "seamless" and "robust" everywhere, vague value props
- AI business reports: corporate jargon clusters, "paradigm shift", passive voice throughout
- AI social: engagement bait patterns, "agree?", forced vulnerability

### Step 3: Lexical Scan

Scan the text against the word blocklist. For each flagged word/phrase:
- Count occurrences
- Note locations (paragraph/sentence numbers)
- Categorize severity (always-avoid vs. context-dependent vs. watch-list)
- Provide specific replacement suggestions

**Output format:**
```
LEXICAL TELLS
  "delve" — 3 occurrences (¶2, ¶5, ¶8)
    Severity: Always avoid
    Replace with: explore, examine, dig into

  "it's important to note" — 2 occurrences (¶1, ¶6)
    Severity: Always avoid
    Replace with: [delete — just state the thing]

  "robust" — 1 occurrence (¶4)
    Severity: Context-dependent (OK in engineering, flagged in marketing)
    Replace with: strong, reliable, solid
```

### Step 4: Structural Analysis

Measure structural patterns:

**Sentence length analysis:**
- Calculate mean sentence length
- Calculate standard deviation (burstiness)
- Identify the longest and shortest sentences
- Flag passages where 3+ consecutive sentences are within 5 words of each other

**Paragraph analysis:**
- Measure paragraph lengths (sentence counts)
- Flag uniform paragraph structure (all paragraphs same length)
- Check for formulaic pattern (topic sentence → evidence → conclusion) in every paragraph

**Transition audit:**
- Count explicit transition words/phrases per paragraph
- Flag paragraphs with 2+ mechanical transitions
- List specific transitions used and suggest natural alternatives

**List pattern check:**
- Flag triplet lists with perfect parallel structure
- Count total list structures vs. prose development

**Output format:**
```
STRUCTURAL ANALYSIS

  Burstiness: SD = 4.2 (AI-typical: <5, human-typical: >8)
    ⚠ Sentences in ¶3-4 are suspiciously uniform (18, 20, 19, 21 words)
    ✓ ¶7 has good variety (6, 23, 4, 31 words)

  Paragraph uniformity: 5 of 7 paragraphs are 4-5 sentences
    ⚠ Consider adding a 1-sentence paragraph or expanding one to 7+ sentences

  Transition density: 2.1 per paragraph (elevated)
    ⚠ "Furthermore" appears 3x, "Additionally" 2x
    → Replace most with natural flow (echo words, logical sequencing)

  Triplet lists: 4 instances of exactly 3 parallel items
    ⚠ Vary list lengths (2, 4, or 5 items) or break parallel structure
```

### Step 5: Rhetorical Pattern Scan

Check for AI-specific rhetorical patterns:

- **Contrast framing:** "It's not about X, it's about Y" — count instances
- **Rule of three:** Mechanical triplets beyond list structures
- **"Tada" intros:** "But here's the thing:", "The result?", etc.
- **Throat-clearing:** Opening sentences that add nothing
- **Hedging clusters:** Back-to-back qualifiers
- **Performed empathy:** Template-shaped concern phrases
- **Em dash density:** Count per page (250 words)

### Step 6: Specificity and Voice Assessment

**Specificity score:**
- Count concrete details (names, numbers, dates, specific examples) per 500 words
- Count vague abstractions ("various stakeholders", "multiple factors", "significant impact") per 500 words
- Ratio indicates how grounded vs. generic the text is

**Voice assessment:**
- Does the text have personality markers? (humor, opinions, asides, self-corrections)
- Is the emotional register uniform or does it shift?
- Are there signs of lived experience or specific knowledge?
- If voice profile loaded: does the text match the profile's patterns?

### Step 7: Present Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI PATTERN AUDIT — [domain type]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall assessment: [1-2 sentences — how many patterns present, how severe]

Scores:
  Burstiness (sentence variety):     [score] / 10  [SD value]
  Lexical originality:               [score] / 10  [blocklist hit count]
  Structural variety:                [score] / 10  [paragraph/transition analysis]
  Specificity:                       [score] / 10  [concrete vs. abstract ratio]
  Voice & personality:               [score] / 10  [personality marker presence]

  Composite:                         [average] / 10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINDINGS (by category)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Lexical tells — detailed findings with locations and replacements]
[Structural patterns — measurements and specific problem areas]
[Rhetorical patterns — contrast framing, triplets, hedging, etc.]
[Specificity gaps — where concrete detail would help]
[Voice observations — what's present and what's missing]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOP 5 FIXES (highest impact)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Most impactful change — what to do and where]
2. [Second — ...]
3. [Third — ...]
4. [Fourth — ...]
5. [Fifth — ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What would you like to do?
1. Improve this text — hand off to improve skill with AI fixes prioritized
2. Dive deeper into a specific category
3. Re-audit after changes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 8: Long Document Handling

Same chunked processing as other skills:
1. Chunk by sections
2. Analyze each with full attention
3. Rolling context summary between chunks
4. Per-section scores, then consolidated report

### Step 9: Follow-Up

Based on user choice:
- **Improve:** Hand to improve skill with AI pattern findings pre-loaded
- **Dive deeper:** Expand on a specific category
- **Re-audit:** After user makes changes, re-run the full audit

## Coach Mode

If `--coach` flag or user requests:
- Each finding includes an explanation of WHY this pattern signals AI
- Explain the underlying mechanism (probabilistic token prediction, RLHF incentives, etc.)
- Teach the craft concept (burstiness, transition techniques, specificity)
- Connect patterns to the forensic stylometry framework: these are statistical fingerprints of safe-middle generation

## Critical Rules

1. **Never claim to detect AI authorship** — report patterns, not verdicts. "This text exhibits 7 patterns commonly associated with AI output" not "This was written by AI."
2. **Frame as craft improvement** — every AI pattern is also a writing quality problem. The fix makes writing better regardless of origin.
3. **Be specific and measurable** — burstiness scores, word counts, paragraph lengths. Not "could use more variety."
4. **Provide fixes, not just diagnoses** — every finding needs an actionable suggestion
5. **Domain context matters** — "robust" in an engineering spec is fine. "Robust" in a blog post is a flag. Apply domain awareness.
6. **The non-native speaker consideration** — lower burstiness and simpler vocabulary are also features of non-native English writing. Frame all findings as craft opportunities, never as "proof" of AI origin. A non-native speaker who uses "it's important to note" three times benefits from learning alternatives regardless.
