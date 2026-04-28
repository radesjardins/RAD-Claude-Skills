# AI Writing Patterns Reference

> **Last verified:** 2026-04-26
> **Status:** Patterns associated with LLM-generated text. **Not a detection metric.** Use for craft improvement; the writing gets better regardless of authorship.
> **Honest framing:** As of 2026, perfect AI detection is mathematically impossible at high confidence ([arXiv:2509.11915](https://arxiv.org/html/2509.11915v1)). Newer models actively suppress named tells (GPT-5.1 dropped em dash usage; "delve" usage in newer model output declined sharply per [Wikipedia: Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)). Treat any single pattern below as **weak evidence**; convergent patterns across categories carry more weight.
> **Canonical reference:** [Wikipedia: Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) — see `wikipedia-signs-of-ai-writing.md` in this folder for context on why this is the credible 2026 reference.

**Core principle:** AI models use probabilistic next-token prediction, trained via RLHF to produce text humans find "helpful," "professional," and "polished." This drives them toward the "safe middle" of the word distribution — high-probability, generic phrasing that avoids linguistic risk. The patterns below are the visible consequences. Fix them and the writing gets better; that's the win, not "evading detection."

---

## How to use this reference

The patterns are organized by **durability** — how reliably they signal AI text in 2026.

- **Tier 1 (durable):** Structural and semantic patterns that emerge from next-token dynamics. Hard for newer models to suppress without changing fundamental behavior. Most useful for craft work.
- **Tier 2 (degrading but still informative):** Stylistic and rhetorical patterns. Often present in 2024-era output; many are being trained-out. Useful as soft signals in clusters.
- **Tier 3 (largely deprecated):** The 2023-2024 lexical tells. Specific words like "delve" and "tapestry" that became famous as AI markers. Newer models suppress them; human writers absorb them culturally; humanizers strip them in one pass. **Still worth replacing for style reasons** — most are clichés — but their AI-tell status is a lagging signal.

When auditing or improving text in Claude.ai, work tier-by-tier: Tier 1 first (most durable signals + biggest craft wins), Tier 2 if structural is clean, Tier 3 last (style polish, not detection).

---

## Tier 1 — Durable structural and semantic patterns

These are the most reliable 2026 signals. They emerge from how LLMs compose text at the token level, not from any specific vocabulary.

### Specificity Gap (most reliable)

AI defaults to abstract claims without grounded detail. Generic examples, unnamed sources, missing dates, "various stakeholders," "many studies suggest." This is the most durable AI tell because it is not a surface feature — it's a property of the *content itself*. Newer models are narrowing this gap for factual domains but it persists for personal voice and idiosyncratic reported detail.

**Watch for:** "industry experts note," "observers have argued," "some studies suggest" with no actual citations. Generic personas ("the modern marketer," "today's CFO") instead of named people. Statistics without sources or dates.

**Fix:** Demand specific names, numbers, dates, sources. Replace abstract claims with concrete examples from actual research, lived experience, or named cases.

### Vague Attribution

Related to the specificity gap. AI cannot hold a specific source in mind during generation, so it produces phrases that *sound like* attribution but aren't. "Recent research has shown..." (which research? where?). "Most experts agree..." (which experts? on what?).

**Fix:** If the claim has a source, name it (with link / citation). If you can't, drop the attribution scaffolding and just make the claim — better honest assertion than fake citation.

### Copula Suppression ("serves as," "stands as," "marks," "represents")

AI substitutes inflated verbs for simple "is" / "are" because of token-level repetition penalties pushing toward variety. Documented ~10% reduction in "is" / "are" usage in academic writing post-2023. **One of the most durable tells** because it emerges from how the model handles repetition, not from any specific word.

**Watch for:** "The framework serves as a tool for..." (just say "is"). "This stands as a reminder that..." ("is a reminder"). "The data represents a shift..." ("shows a shift").

**Fix:** Wherever the inflated verb can be replaced by "is" or "are" without loss, do it.

### Rule of Three Abuse (mechanical triplets)

AI applies the "Rule of Three" reflexively, adding a third element even when unnecessary. "Focused, aligned, measurable." "Engaging, informative, and actionable." "No theory. No fluff. Just execution." Humans like triplets too, but AI uses them so consistently that *every* list ending up as exactly three parallel items is the signal.

**Watch for:** Multiple consecutive sentences that each end in a parallel triplet; three-item lists where the third item feels padded.

**Fix:** Vary list lengths (2, 4, 5 items). Break parallel structure deliberately. Make at least one list end on a single emphatic item.

### Elegant Variation (synonym rotation)

Avoiding repetition by rotating synonyms even when the original word is the right one. "Kubernetes" becomes "the orchestration platform" becomes "the container runtime." Human writers repeat key terms when they need to; AI rotates compulsively.

**Fix:** Use the same word for the same concept. Repetition signals seriousness; synonym soup signals decoration.

### Present Participle Clause Stacking

AI uses "-ing" clause constructions at 2-5x the human rate. "Walking into the office, she noticed the changes." "Having considered the options, the team decided..." "Recognizing the opportunity, they moved quickly."

**Fix:** One or two per page is fine. Five per page is a tell. Convert most to direct independent clauses.

### Sentence Length Uniformity (still meaningful, less reliable than 2024)

AI traditionally produced sentences averaging 15-25 words with low standard deviation (typically SD < 5 in 2023-2024 era). Human writing has higher variance (SD > 8). **Newer models produce higher burstiness** so this is less reliable than it once was — but extreme uniformity (SD < 4 across a whole document) still carries signal.

**Quick check in Claude.ai:** ask Claude to compute the mean and standard deviation of sentence lengths across the passage. SD below 4 across a whole document is uniform; SD above 7 reads as natural human variance.

**Caveats:** Non-native English writers naturally produce low-burstiness text. Technical, legal, and academic writing also do. Burstiness alone is not evidence of AI; it's one feature among many.

**Fix:** Vary sentence length deliberately. Mix fragments, short punchy sentences, and longer subordinate-clause-heavy ones. Target SD > 7.

### Paragraph Uniformity ("rectangular paragraphs")

AI produces paragraphs of remarkably similar length, each following topic-sentence → evidence → summary structure. Page looks rectangular. Human writing varies paragraph length dramatically — one-sentence paragraphs for emphasis, long paragraphs for complex ideas.

**Fix:** Mix one-sentence paragraphs and longer ones. Break the topic-sentence formula sometimes.

---

## Tier 2 — Degrading but still informative

These were strong 2024-era signals. Many are being trained out; some still appear in clusters.

### "Tada" Intros and Forced Closers

False-casual openers and formulaic closers that create an "uncanny valley" of attempted personality. Many newer models have reduced these but they persist, especially in chat-style outputs.

**Dramatic reveals:**
- "But here's the thing:" / "Here's the uncomfortable truth:"
- "The result?" / "The answer?"
- "Spoiler alert:" / "Plot twist:"

**False-casual openers:**
- "Let's face it..." / "Let's get real..."
- "Let's dive in." / "Let's break it down."
- "It's no secret that..."

**Pseudo-conversational questions:**
- "Sound familiar?"
- "Ever wondered why...?"

**Temporal/world-building openers:**
- "In today's fast-paced [world/landscape]..."
- "In a world where..." / "In the ever-evolving landscape of..."

**Forced enthusiasm:**
- "Great question!" / "Absolutely!"
- "I'd be happy to help with that!"

**Formulaic closers (equally telling):**
- "I hope this helps!"
- "Let me know if you need anything else!"
- "Feel free to reach out!"
- "Don't hesitate to ask!"

### Mechanical Transitions

"Furthermore," "Additionally," "Moreover" used as connective tissue rather than because the logic demands them. Documented 3-5x higher frequency in AI text vs. human casual/semi-formal writing (pre-2025; varies by current model).

**Quick check in Claude.ai:** ask Claude to flag any paragraph containing two or more of {Furthermore, Additionally, Moreover, That being said, On the other hand, In light of the above, Consequently, Subsequently}.

**Fix:** Use transitions when they actually mark a turn in the argument. Default to natural flow — the next sentence either continues or contrasts the previous one without needing a bookmark.

### Hedging Clusters

AI hedges excessively, especially in clusters: "may potentially," "could possibly," "might arguably." Back-to-back qualifiers signal the model trying to avoid commitment. Documented behavior; less prevalent in newer Anthropic and OpenAI outputs but still appears.

**Quick check in Claude.ai:** ask Claude to count hedging tokens (may, might, could, possibly, perhaps, somewhat, generally, typically, often, tends to) per 100 words. Above 3 in clusters signals padding.

**Fix:** Pick one hedge or commit. "Likely" is a hedge; "may potentially" is two hedges doing one job.

### Em Dash Usage

AI models trained on text from 2022-2024 used em dashes at noticeably elevated rates. Verified directional findings:
- A study of 10,000 ecology abstracts found em dash relative frequency **more than doubled** from 2021 to 2025 ([Piece of K analysis](https://www.pieceofk.fr/the-rise-of-the-em-dash-in-ecology-abstracts/)).
- Sean Goedecke's controlled comparison: GPT-3.5 produced 0 em dashes; GPT-4o produced ~16; GPT-4.1 produced ~14 in similar test prompts ([Sean Goedecke analysis](https://www.seangoedecke.com/em-dashes/)). The often-cited "10x" multiplier for GPT-4o vs GPT-3.5 is approximately accurate.

**Important update:** GPT-5.1 actively suppressed em dash usage. As model providers patch this signal, em dash density becomes a lagging indicator. The widely-circulated "AI uses em dashes every 50-80 words; humans every 500 words" ratio is **practitioner folklore** — directionally consistent with the verified findings but not from a peer-reviewed study.

**Five specific AI em dash patterns:**
1. **Contrast framing:** "Credit card fraud isn't just evolving—it's accelerating!" False dramatic tension.
2. **Parenthetical insertion:** "AI models—particularly ChatGPT—use em dashes at a higher rate." Where commas or parentheses would do.
3. **Semantic bridging:** Joining ideas that should be separate sentences.
4. **Dramatic pause/reveal:** "The answer was surprisingly simple—just three lines of code."
5. **Inappropriate substitution:** Replacing colons, semicolons, commas, and periods with em dashes mechanically.

**Human pattern:** Uses em dashes sparingly for genuine emphasis or interruption. The key difference is *uniformity* — AI uses them mechanically; humans use them deliberately.

**Quick check in Claude.ai:** ask Claude to count em dashes per 250 words. Above 4 was a strong signal in 2024; in 2026 it's elevated but not conclusive.

### "Not X. Not Y. Just Z." Countdown

Dramatic negative parallelism to build fake tension before an unremarkable point: "Not a framework. Not a methodology. Just a better way to think about code." If the final point isn't surprising, one contrast is enough.

### Anaphora Abuse

Repeating the exact same sentence opening in quick succession to manufacture rhetorical momentum. "We need to rethink... We need to rebuild... We need to reimagine..." One or two repetitions can be powerful. Three or more reads as AI pattern, not deliberate rhetoric.

### Tricolon Abuse

Stringing multiple three-part sentences back-to-back. AI applies parallel structure so aggressively that entire paragraphs become rhythmically identical: "Products impress people; platforms empower them. Products solve problems; platforms create worlds." One per section is fine; three in a row is a tell.

### Gerund Fragment Litany

Verbless fragments built on gerunds simulating cinematic pacing: "Reviewing pull requests. Debugging edge cases. Attending architecture meetings." Reads as LinkedIn post / movie trailer.

### "Listicle in a Trench Coat"

Numbered lists disguised as essay structure: "The first wall is..." / "The second wall is..." / "The third wall is..." Each "paragraph" the same length, same shape, could be a bullet point.

### Bold-First Bullets

Every bullet starts with a bolded keyword + colon + explanation:
- **Scalability:** The system handles...
- **Reliability:** The architecture ensures...

Visual uniformity that screams template. Human bullet lists vary their formatting.

### Fractal Summaries

Document summarizes what it will say, says it, then summarizes what it said — at every level. Introduction previews all sections; each section previews and summarizes itself; conclusion re-summarizes everything. Result: 40% of the document is summary.

### One-Point Dilution

Padding a single 800-word argument into 4,000 words of circular repetition with different metaphors. Each restatement uses different words but adds zero new information.

### Invented Concept Labels

AI creates fake compound terms and treats them as established concepts: "supervision paradox," "acceleration trap," "workload creep." These cluster abstract problem-nouns to manufacture intellectual authority. Real domain terminology has citations; invented labels have scare quotes and no source.

---

## Tier 3 — Lexical tells (largely deprecated, still useful as style noise)

These are the famous 2023-2024 word-list tells. Important caveats:

- **The Wikipedia guide explicitly notes "delve" usage dropped sharply in 2025** as models were updated. It remains a soft signal in clusters but is no longer reliable as a first-signal word.
- **Words on these lists migrate into human writing.** Max Planck Institute (2024) documented 50%+ frequency increases of these words in *human-authored* academic essays — humans absorbed AI vocabulary culturally.
- **Verified frequency claims:** "delve" went from 349 PubMed uses in 2020 to 2,847 in 2023 to 2,630+ in early 2024 — roughly a **654% increase** ([Scientific American](https://www.scientificamerican.com/article/chatbots-have-thoroughly-infiltrated-scientific-publishing/), [Shapira analysis](https://pshapira.net/2024/03/31/delving-into-delve/)). Other commonly-cited multipliers (foster 10.8×, tapestry 7.2×, landscape 6.1×, nuanced 4.8×) are widely repeated but a peer-reviewed source for those specific numbers is hard to locate; the *direction* is correct (these words spiked) but the precise multipliers should be treated as folklore unless you can cite [Kobak et al. 2024 (arXiv:2406.07016)](https://arxiv.org/html/2406.07016v1) or similar measured data.
- **Treat as style guidance, not detection.** Most of these are clichés worth replacing whatever the source.

The full word list with replacement suggestions lives in [`word-blocklist.md`](word-blocklist.md). When auditing in Claude.ai, paste a passage and ask Claude to scan it against the always-avoid list — it will flag specific words and offer replacements.

### Quick reference (the 2023-2024 canonical list)

**Verbs:** delve, leverage, utilize, harness, streamline, underscore, foster, navigate (metaphorical), elevate, empower, spearhead, bolster, catalyze, endeavor, facilitate, embark, unpack, unravel, encompass, captivate, resonate, revolutionize, transform

**Adjectives:** pivotal, robust, innovative, seamless, cutting-edge, comprehensive, nuanced, multifaceted, groundbreaking, transformative, holistic, meticulous, intricate, invaluable, paramount, indispensable, exemplary

**Nouns:** landscape, realm, tapestry, synergy, testament, paradigm, cornerstone, linchpin, nexus, beacon, catalyst, plethora, myriad

**Adverbs:** arguably, undeniably, notably, remarkably, fundamentally, inherently, ultimately, intrinsically

### Magic Adverbs (named category)

quietly, deeply, fundamentally, remarkably, arguably — adverbs AI uses to inject artificial significance. "The team quietly shipped a fix" — was it actually quiet, or is the adverb doing fake-dramatic work? Cut the adverb and see if the sentence loses real meaning.

### Gravitas Words

crucial, essential, fundamental, pivotal — AI inflates importance with these. Often pure filler. "This is a crucial step" → "This step..." When every point is "crucial," nothing is.

### Throat-Clearing Openers

- "It's important to note that..."
- "In today's [X] landscape..."
- "Generally speaking..."
- "From a broader perspective..."
- "It's worth mentioning that..."
- "When it comes to [X]..."
- "At the end of the day..."
- "In the realm of..."

These are reliably clichés in any context.

---

## Emotional and Voice Patterns (durability varies)

### Performed Empathy

Template-shaped concern phrases: "This can be incredibly frustrating..." / "It's completely understandable that..." / "Many people struggle with..." Real empathy is specific. Performed empathy is generic.

### Compliment Sandwich

AI cannot deliver direct criticism. It invariably leads with a positive statement before addressing flaws, then ends with another positive. "The architecture is well-structured. However, the error handling needs significant improvement. Overall, this is a strong foundation." So consistent that the opening compliment becomes a warning flag.

### Emotional Flatness

AI maintains a consistent emotional register throughout. No tonal shifts, no humor, no frustration. Even when prompted to be "passionate," the passion is uniform rather than peaking.

### Missing Personality Markers

Human writing has interrupted thoughts, self-corrections, asides, opinions stated without justification, inside references, humor that risks falling flat. AI text is clean, balanced, safe. That safety is itself a signal.

### Absence of Lived Experience

AI can define "rain" but has never been caught in a thunderstorm. Generic sensory descriptions, "weak sauce" character renderings (gruff truck drivers, businesslike businessmen, sunsets "painted across the sky"). Specificity from actual experience is hard to fake.

### False Vulnerability

Polished, risk-free pseudo-vulnerability that never actually risks discomfort. "And yes, since we're being honest..." or "This is not a rant; it's a diagnosis." Real vulnerability names personal failures, admits confusion, stakes positions that might draw criticism.

### "Fake Casual Quotes"

Putting casualness in scare quotes to perform relatability rather than writing naturally: "what developers call 'good enough'" or "what we might charitably call 'progress'." The scare quotes signal "I'm being casual" instead of just being casual.

---

## B2B and Professional "Workslop"

### Corporate-Heavy Clichés

When a business document is filled with "synergies," "paradigm shifts," and "best-in-class solutions," it was likely AI-padded. These clichés cause content to "blend in" rather than stand out.

### The "No Fluff" Irony

AI frequently includes "no fluff" to signal conciseness — but "no fluff" is itself filler. A phrase AI adds when prompted to be concise, signaling the opposite of what it claims.

### Institutional Padding

AI-generated professional content sounds impressive without committing to specifics. Watch for paragraphs that feel authoritative but say nothing concrete — abstract nouns, no specific numbers, no named cases, no evidence.

### AI Suspicion Tax

Phrases like "I hope this email finds you well" now trigger automated cybersecurity suspicion filters. Two related vendor-sourced data points worth knowing about (treat as vendor data, not academic):

- **SlashNext's 2023 State of Phishing Report**: 1,265% increase in phishing email volume Q4 2022 → Q3 2023, attributed to generative AI ([SlashNext press release](https://slashnext.com/press-release/slashnexts-2023-state-of-phishing-report-reveals-a-1265-increase-in-phishing-emails-since-the-launch-of-chatgpt-in-november-2022-signaling-a-new-era-of-cybercrime-fueled-by-generative-ai/)). Note: the 1,265% figure measures *all* phishing volume, not specifically AI-linked phishing — SlashNext attributes the surge to AI but did not measure AI-linked specifically.
- **KnowBe4 Phishing Threat Trends Report** (Sept 2024 - Feb 2025): 82.6% of phishing emails contained AI-generated content ([Security Magazine coverage](https://www.securitymagazine.com/articles/101490-82-of-all-phishing-emails-utilized-ai)).

The implication: legitimate AI-assisted professional writing now risks getting caught in spam filters because it matches known phishing patterns. Boilerplate openers/closers aren't just bad writing — they're a security liability.

---

## Measurement (in Claude.ai)

The Claude Code plugin ships Python validators (`text-stats.py`, `check-blocklist.py`) that compute these directly. In Claude.ai, ask Claude to compute the metrics on a passage you paste — Claude can count tokens, sentences, and word matches reliably for short-to-medium documents. For long documents (10K+ words), batch in sections.

| Metric | Tier | Default thresholds (2026 — soft signals only) |
|---|---|---|
| Burstiness (sentence-length SD) | Tier 1 | <4 uniform · 4-7 moderate · 7-10 natural · >10 strongly varied |
| Em dash density (per 250 words) | Tier 2 | 0-2 natural · 2-4 elevated · >4 was strong 2024 signal |
| Hedging density (per 100 words) | Tier 2 | <1 assertive · 1-3 natural · >3 padding signal in clusters |
| Transition density (per paragraph) | Tier 2 | 0-1 natural · 1-2 mechanical · >2 strong signal |
| Lexical tell count (per 500 words) | Tier 3 | 0 clean · 1-2 minor · 3+ was strong signal in 2024 |
| Paragraph uniformity (sentence-count SD) | Tier 1 | <1.5 uniform/templated · ≥1.5 varied |

### Convergent Signature

A high-confidence "this looks AI" assessment requires convergence across categories:
1. Tier 1 structural — specificity gap, copula avoidance, rule of three abuse
2. Tier 2 stylistic — em dashes, transitions, hedging clusters
3. Tier 3 lexical — multiple words from the blocklist

**No single pattern is conclusive.** Three or more categories with elevated signals is informative — but even then, the right framing is "this writing exhibits patterns associated with AI output and would benefit from craft revision," not "this is X% AI-generated."

---

## The "Human Sandwich" Test

The most significant tell remains the absence of human strategy at the start and human editing at the end. Content that lacks both feels generic regardless of authorship. The fix isn't to trick detectors — it's to add genuine human input: a real thesis, specific examples from experience, idiosyncratic word choices, editing that breaks the patterns above.

---

## Sources

The patterns and frequency claims here are drawn from:

- [Wikipedia: Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) — primary reference
- [Uncertainty in Authorship (arXiv:2509.11915)](https://arxiv.org/html/2509.11915v1) — theoretical impossibility of perfect detection
- [Kobak et al. 2024: ChatGPT excess vocabulary (arXiv:2406.07016)](https://arxiv.org/html/2406.07016v1) — measured vocabulary shifts
- [Catch Me If You Can? Not Yet — EMNLP 2025 Findings](https://aclanthology.org/2025.findings-emnlp.532.pdf) — voice mimicry capability ceilings
- [The em dash dilemma — Sean Goedecke](https://www.seangoedecke.com/em-dashes/) — controlled GPT-3.5 vs 4o vs 4.1 em dash counts
- [Em dashes in ecology abstracts — Piece of K](https://www.pieceofk.fr/the-rise-of-the-em-dash-in-ecology-abstracts/) — 10K-abstract empirical study
- [Delving into delve — Philip Shapira](https://pshapira.net/2024/03/31/delving-into-delve/) — PubMed delve tracking
- [Pangram Labs: Why Perplexity and Burstiness Fail](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai) — practical rebuttal of dominant detection methods
- [Stanford HAI: AI-Detectors Biased Against Non-Native English Writers](https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers/) — 61.3% false-positive rate finding (still governing reference)

Where claims here cite a specific frequency multiplier without a primary source, treat as folklore — the *direction* of the claim is supported, the *precise number* may not be.
