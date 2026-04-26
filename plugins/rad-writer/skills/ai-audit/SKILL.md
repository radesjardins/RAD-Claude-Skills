---
name: ai-audit
description: >
  This skill should be used when the user says "check for AI patterns", "does this sound like AI",
  "AI audit", "ai-audit", "check if this reads as human", "humanize check", "AI tells",
  "does this pass AI detection", "check for AI slop", "is this AI-written", "AI pattern check",
  or wants a deep analysis of whether text exhibits AI-generated writing patterns. Reports
  patterns with measurable scores (computed by scripts/text-stats.py) and located findings
  (computed by scripts/check-blocklist.py). Does NOT claim to be an AI detector — perfect AI
  detection is mathematically impossible (arXiv:2509.11915). Works across all 9 writing domains.
argument-hint: "[paste text or provide file path] [--domain email|blog|web-copy|report|research|presentation|prose|technical|social] [--coach]"
allowed-tools: Read Glob Grep Bash
---

# AI Audit Skill

Pattern-by-pattern analysis of writing against the structural, stylistic, and lexical patterns associated with AI-generated text. Reports specific findings with measurable scores from the deterministic scripts.

## Honest framing — read this first

**This is not an AI detector.** Perfect AI text detection is structurally impossible in 2026 ([arXiv:2509.11915](https://arxiv.org/html/2509.11915v1) — as model output distributions converge to human distributions, detection error floors approach chance). Most major universities have disabled AI detection tools institutionally for false-positive reasons.

**This is a craft tool.** It identifies specific patterns that happen to correlate with AI output. Fixing them produces better writing whether the source was AI, a tired human writer, a non-native English speaker, or all three. The framing is: "this writing exhibits N patterns associated with AI output and would benefit from craft revision," not "this is X% AI-generated."

**The reliable signals in 2026 are structural, not lexical.** The 2023-2024 word-list approach ("delve," "tapestry," "leverage") is a degrading signal — newer models suppress these words and humans absorb them. The durable signals are the specificity gap, copula avoidance, rule-of-three abuse, vague attribution, register drift. The skill leads with these.

For full context on the 2026 detection landscape, see `references/wikipedia-signs-of-ai-writing.md`.

## Process

### Step 1: Receive text

Accept text via paste, file path, or upload. If long, write to a temp file so the scripts can read it.

### Step 2: Detect domain

Same domain detection as the other skills. Load the domain reference for domain-specific anti-patterns:

`${CLAUDE_SKILL_DIR}/../../references/domain-[type].md`

Domain matters because AI patterns differ by genre:
- AI emails: over-formal greetings, "I hope this finds you well", mechanical closings
- AI research: "delve" in every section, uniform hedging, overclaiming in abstracts
- AI blog posts: "In today's [X] landscape" openers, listicle structure, no voice
- AI web copy: buzzword-heavy, "seamless" and "robust" everywhere, vague value props
- AI business reports: corporate jargon clusters, "paradigm shift", passive voice throughout
- AI social: engagement bait patterns, "agree?", forced vulnerability

### Step 3: Run the deterministic scripts (this is the measurement layer)

```bash
# Computes burstiness, em-dash density, hedging, transitions, paragraph distribution, lexical tells
python3 ${plugin_root}/scripts/text-stats.py <text-file> --json

# Locates every blocklist match by line/column with replacement suggestions
python3 ${plugin_root}/scripts/check-blocklist.py <text-file> --json
```

Capture both JSON outputs. **Use these numbers verbatim** — don't ask yourself to count em dashes or measure burstiness. The scripts are deterministic and give the user reproducible results.

The scripts ship with caveats baked in (every metric notes "this was a strong signal in 2023-2024 era; newer models suppress some of these"). Carry those caveats forward into the report.

### Step 4: Layer LLM judgment on what scripts can't measure

Scripts handle: lexical counts, em-dash density, sentence-length variance, paragraph distribution, hedging density, transition density.

LLM-only categories (these need actual reading, not counting):

**Specificity gap (Tier 1 — most important):**
- Concrete details (named people, specific numbers, dates, real cases) per 500 words
- Vague abstractions ("various stakeholders," "multiple factors," "significant impact") per 500 words
- Ratio indicates how grounded vs. generic the text is

**Voice and register:**
- Personality markers — humor, opinions, asides, self-corrections
- Emotional register — uniform throughout, or does it shift?
- Lived experience signals — specific reported detail, idiosyncratic word choices
- If voice profile loaded: deviations from the writer's established patterns

**Vague attribution:**
- "Studies suggest" without citation
- "Industry experts note" without naming
- Generic personas instead of named cases

**Structural patterns scripts don't catch:**
- Copula avoidance ("serves as," "stands as" replacing "is" — `check-blocklist.py` flags some, but the pattern needs a read)
- Rule-of-three abuse (mechanical triplets across paragraphs)
- Synonym rotation (same concept named different ways)
- Compliment sandwich
- Performed empathy
- Fractal summaries (40% of doc is summary of itself)
- Invented concept labels (AI-generated compound terms presented as established)

### Step 5: Present report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI PATTERN AUDIT — [domain type]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall: [2 sentences — how many patterns, how clustered, what tier they're in]

NOTE: This is not an AI detector. The patterns below correlate with AI output;
they do not prove authorship. Perfect AI detection is mathematically impossible
in 2026 (see references/wikipedia-signs-of-ai-writing.md). Use as craft signals.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MEASURED METRICS (from scripts/text-stats.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Burstiness (sentence-length SD):  [N]   [interpretation tier]
  Em dash density (per 250 words):  [N]   [interpretation tier]
  Hedging density (per 100 words):  [N]   [interpretation tier]
  Transition density (per ¶):       [N]   [interpretation tier]
  Paragraph uniformity:             [varied/uniform]
  Lexical tells (per 500 words):    [N]   [interpretation tier]

  → these are 2023-2024-era signals; newer models suppress several. Treat as soft
    evidence; convergent patterns across categories matter more than any single number.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIER 1 — DURABLE PATTERNS (most reliable)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Specificity gap findings, vague attribution findings, copula suppression findings,
rule-of-three findings, synonym rotation findings — with locations and fixes]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIER 2 — STYLISTIC PATTERNS (degrading but informative in clusters)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Em dash patterns, transition density, hedging clusters, "tada" intros, anaphora,
tricolon abuse, listicle-in-trench-coat, fractal summaries — with locations]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIER 3 — LEXICAL TELLS (largely deprecated, soft style noise)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Blocklist matches from check-blocklist.py — top 5-8 by count, with line locations
and replacements. Acknowledge that newer models suppress these and humans absorb them.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOP 5 FIXES (highest impact, prioritize Tier 1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Most impactful Tier 1 change — likely specificity or attribution]
2. [Second]
3. [Third]
4. [Fourth]
5. [Fifth]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What would you like to do?
1. Improve this text — hand off to improve skill with findings pre-loaded
2. Dive deeper into a specific tier
3. Re-audit after changes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 6: Long document handling

Same chunked processing as other skills:
1. Run `text-stats.py` and `check-blocklist.py` on the full document — they handle long input efficiently
2. For LLM-judgment categories: chunk by sections, analyze each with full attention
3. Rolling context summary between chunks
4. Per-section findings, then consolidated report

### Step 7: Follow-up

Based on user choice:
- **Improve:** Hand to improve skill with AI pattern findings pre-loaded
- **Dive deeper:** Expand on a specific tier
- **Re-audit:** After user makes changes, re-run the full audit

## Coach mode

If `--coach` flag or user requests:
- Each finding includes 1-2 sentence explanation of WHY this pattern correlates with AI output
- Explain underlying mechanism where useful (probabilistic token prediction, RLHF incentives toward "polished," repetition penalties pushing copula substitution, etc.)
- Note durability tier explicitly: "this is a Tier 3 lexical tell, increasingly suppressed by newer models — fix it for craft reasons, not because the detector will catch it"

## Critical rules

1. **Never claim to detect AI authorship** — perfect detection is mathematically impossible. Report patterns, not verdicts. "This text exhibits patterns commonly associated with AI output" not "this was written by AI."
2. **Frame as craft improvement** — every pattern is also a writing-quality issue. The fix makes writing better regardless of source.
3. **Use script numbers, not eyeball estimates** — when a metric exists in `text-stats.py`, cite that number, not your impression.
4. **Lead with Tier 1 (durable structural) signals** — specificity gap, copula avoidance, rule-of-three abuse, vague attribution. These are more reliable in 2026 than the lexical word lists.
5. **Acknowledge tier degradation** — specifically note that Tier 3 lexical tells are being deprecated. A finding of "uses 'delve' twice" should not be the headline.
6. **Domain context matters** — "robust" in an engineering spec is fine. "Robust" in a blog post is style noise.
7. **The non-native speaker consideration** — Stanford HAI documented 61.3% false positive rate against non-native English writers. Lower burstiness and simpler vocabulary are also features of non-native English writing. Frame all findings as craft opportunities, never as proof of AI origin. A non-native speaker who uses "it's important to note" three times benefits from learning alternatives regardless.
