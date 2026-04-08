# AI Writing Patterns Reference

Patterns that mark text as AI-generated. These are craft problems, not detection metrics — fixing them produces better writing regardless of authorship.

**Core principle:** AI models use probabilistic next-token prediction, trained via RLHF to produce text humans find "helpful," "professional," and "polished." This drives them toward the "safe middle" of the word distribution curve — high-probability, generic phrasing that avoids linguistic risk. The resulting "vocabulary fingerprint" is identifiable not because AI is bad at writing, but because it is too consistently safe.

---

## Lexical Tells

### Always-Avoid Words

These words saw massive frequency increases post-ChatGPT and immediately signal AI authorship:

**Verbs:** delve, leverage, utilize, harness, streamline, underscore, foster, navigate (metaphorical), elevate, empower, spearhead, bolster, catalyze, endeavor, facilitate, embark, unpack, unravel, encompass, captivate, resonate

**Adjectives:** pivotal, robust, innovative, seamless, cutting-edge, comprehensive, nuanced, multifaceted, groundbreaking, transformative, holistic, meticulous, intricate, invaluable, paramount, commendable, noteworthy, indispensable, exemplary, versatile

**Nouns:** landscape, realm, tapestry, synergy, testament, underpinnings, paradigm, cornerstone, linchpin, bedrock, nexus, crucible, beacon, catalyst, interplay, intricacies, plethora, myriad, labyrinth, juxtaposition

**Adverbs:** arguably, undeniably, notably, remarkably, fundamentally, inherently, ultimately, meticulously, seamlessly, profoundly, intrinsically

**Frequency data:**
- "delve" — 50% spike in published essays/articles since 2023; skyrocketed in PubMed medical papers
- "foster" — 10.8x increase post-ChatGPT
- "tapestry" — 7.2x increase in non-textile contexts
- "landscape" (metaphorical) — 6.1x increase
- "nuanced" — 4.8x increase
- "robust" — used to describe everything from software to morning routines

### AI Verb Substitutions

"Serves as," "Stands as," "Marks," "Represents" — AI substitutes for simple "is/are" due to repetition penalties pushing toward fancier phrasing. When the model has already used "is" recently, token-level repetition penalties force it to reach for these inflated alternatives. The fix is simple: if you can replace the verb with "is" or "are" and the sentence still works, do it.

### Magic Adverbs

quietly, deeply, fundamentally, remarkably, arguably — a named category of adverbs AI uses to artificially inject significance into mundane descriptions. These make flat writing feel profound without adding substance. "The team quietly shipped a fix" — was it actually quiet, or is the adverb doing fake-dramatic work? "This fundamentally changes the equation" — does it, or is "fundamentally" just filler? Cut the adverb and see if the sentence loses real meaning. If it doesn't, the adverb was decoration.

### Gravitas Words

crucial, essential, fundamental, pivotal — AI inflates importance with these words. They are often pure filler, removable without changing meaning. "This is a crucial step" → "This step..." "It's essential to understand" → just explain it. When every point is "crucial," nothing is. Reserve these for genuinely high-stakes statements.

### Context-Dependent Words

These are legitimate in specific domains but signal AI in general prose:

| Word | OK in | Flag in |
|------|-------|---------|
| leverage | Finance, physics | General business writing, emails |
| robust | Engineering, statistics | Marketing, casual writing |
| comprehensive | Research methodology | Blog posts, emails |
| utilize | Legal, technical specs | Anywhere "use" works |
| facilitate | Academic, governance | Anywhere "help" or "enable" works |
| implement | Software engineering | General business writing |
| subsequently | Legal, academic | Blog posts, emails, prose |
| seamless | UX research (precise usage) | SaaS marketing (placeholder for missing technical detail) |

---

## Phrase Tells

### Throat-Clearing Openers
- "It's important to note that..." — just state the thing
- "In today's [X] landscape..." — dated cliché, universally flagged
- "Generally speaking..." — either be specific or cut it
- "From a broader perspective..." — vague hedging
- "It's worth mentioning that..." — if it's worth mentioning, mention it
- "When it comes to [X]..." — filler, go direct
- "At the end of the day..." — cliché
- "In the realm of..." — pretentious filler
- "In an era where..." — temporal throat-clearing
- "As we navigate..." — metaphorical filler

### Mechanical Transitions
- "Furthermore," / "Additionally," / "Moreover," — AI uses these 3-5x more than humans in casual/semi-formal writing
- "That being said," — almost always unnecessary
- "On the other hand," — overused hedging connector
- "It should be noted that..." — passive throat-clearing
- "With that in mind," — rarely adds value
- "In light of the above," — bureaucratic
- "Consequently," / "Subsequently," — overly formal for most contexts

### False Profundity
- "This represents a paradigm shift..." — almost never true
- "At its core, [X] is about..." — vague abstraction
- "The implications are far-reaching..." — show, don't tell
- "This underscores the importance of..." — lazy emphasis
- "[X] is not just [Y], it's [Z]" — the AI "reframe" pattern (contrast framing)
- "It's not about X, it's about Y" — manufactured profundity on mundane topics

### The "Tada" Intros and Forced Closers
AI uses these to manufacture conflict or excitement. False-casual openers that create an "uncanny valley" of attempted personality:

**Dramatic reveals:**
- "But here's the thing:" / "Here's the uncomfortable truth:"
- "Here's what you need to know..."
- "The goal?" / "The result?" / "The answer?"
- "And honestly? It's been a wild ride."
- "Spoiler alert:" / "Plot twist:"

**False-casual openers:**
- "Let's face it..." / "But let's get real..."
- "Let's dive in." / "Let's break it down."
- "Then I realized:"
- "It's no secret that..."
- "Now more than ever..."

**Pseudo-conversational questions:**
- "Sound familiar?"
- "Not all [X] are created equal."
- "Whether you're a [persona A] or [persona B]..."
- "Ever wondered why...?"

**Temporal/world-building openers:**
- "In today's fast-paced [world/landscape]..."
- "In a world where..." / "In the ever-evolving landscape of..."
- "As the [industry] continues to evolve..."

**Forced enthusiasm:**
- "Great question!" / "Absolutely!"
- "I'd be happy to help with that!"

**Formulaic closers (equally telling):**
- "I hope this helps!"
- "Let me know if you need anything else!"
- "Feel free to reach out!"
- "Don't hesitate to ask!"
- "Is there anything else I can help you with?"

### Hedging Clusters
AI text often hedges excessively — qualifying everything, never committing:
- "may potentially," "could possibly," "might arguably"
- "to some extent," "in certain respects," "in many ways"
- Back-to-back hedges: "It could potentially be argued that this may..."

### Hyperbolic and Grandiose Language
AI struggles with descriptive restraint. Optimized for "engaging" or "powerful" content, it resorts to unrealistic exaggerations:
- "revolutionizing the industry" — almost never accurate
- "unlocking unprecedented value" — empty superlative
- "game-changing" — overused to meaninglessness
- "best-in-class" — unsubstantiated claim
- Undue emphasis: describing subjects as "leading experts" or having a "global legacy" without evidence

---

## Punctuation and Typographic Tells

### The Em Dash Obsession

The most infamous AI punctuation marker in 2026. AI models are "deeply infatuated" with the em dash, using it for semantic bridging when they cannot find a more sophisticated way to link thoughts. Em dashes became **twice as common** in scientific abstracts after AI became mainstream.

**Frequency data:**
- AI text: em dashes appear every 50-80 words
- Human text: approximately every 500 words
- GPT-4o uses roughly 10x more em dashes than GPT-3.5
- Historical baseline: English em dash usage settled to 0.25-0.275% of words in modern human writing

**Five specific AI em dash patterns:**
1. **Contrast framing:** "Credit card fraud isn't just evolving—it's accelerating!" False dramatic tension between negation and assertion.
2. **Parenthetical insertion:** "AI models—particularly ChatGPT—use em dashes at a higher rate." Paired em dashes where commas or parentheses would suffice.
3. **Semantic bridging:** Joining ideas that should be separate sentences. "The tool chose the optimal approach—one that minimized latency while maximizing throughput."
4. **Dramatic pause/reveal:** "The answer was surprisingly simple—just three lines of code." Artificial suspense before a reveal.
5. **Inappropriate substitution:** Replacing colons, semicolons, commas, and periods with em dashes. AI treats the em dash as universal punctuation.

**Human pattern:** Uses em dashes sparingly for genuine emphasis or interruption. Varies between em dashes, parentheses, commas, and colons depending on rhetorical effect. The key difference is *uniformity* — AI uses them mechanically and frequently; humans use them deliberately and sparingly.

**Fix:** If a document has more than 2-3 em dashes per page, replace most with commas, parentheses, periods, or restructured sentences. Reserve em dashes for moments of genuine surprise or interruption.

### Rigid Grammar and "Illusion of Perfection"

Human writing is naturally "messy" — fragments, idiosyncratic comma usage, occasional grammatical risks. AI writing is "sanitized": strict formal rules, consistent Oxford comma usage, zero typos. The default output is "too clean," creating a tone readers identify as "8th-grade book report" or "overly polished."

### Structural Formatting and Lists

AI defaults to structured lists and bullet points even when narrative flow would be more appropriate. Over-relies on colons (:) to introduce lists or set up a "ta-da" moment. In documents, this manifests as excessive boldface, inline-header vertical lists, and tables for information that could be explained naturally in prose.

---

## Structural Tells

### Sentence Length Uniformity

**The #1 structural signal.** AI produces sentences averaging 15-25 words with low standard deviation (typically SD < 5). Human writing has higher variance (SD > 8). This creates a "hypnotic" or "monotonous" feel that lulls readers into skim mode.

**AI-typical pattern:**
> The new policy aims to improve employee satisfaction. It includes flexible working hours and remote options. These changes reflect current workplace trends. Management believes this will boost productivity. The implementation will begin next quarter.

Five sentences: 8, 9, 6, 7, 7 words. SD = 1.1. Robotic.

**Human-typical pattern:**
> The new policy? Flexible hours, remote work, the whole package. Management spent six months surveying employees — turns out the number one complaint wasn't pay or benefits but the feeling of being chained to a desk from nine to five. Implementation starts in January.

Four sentences: 3, 8, 27, 4 words. SD = 10.8. Natural.

### Paragraph Uniformity

AI produces paragraphs of remarkably similar length, each following topic-sentence → evidence → summary structure. This creates "rectangular" paragraph shapes on the page. Human writing varies paragraph length dramatically — one-sentence paragraphs for emphasis, long paragraphs for complex ideas.

### The Participial Phrase Problem

AI uses participial phrase constructions at 2-5x the human rate:
- "Walking into the office, she noticed the changes."
- "Having considered the options, the team decided..."
- "Recognizing the opportunity, they moved quickly."

One or two per page is fine. Five per page is a tell.

### The Rule of Three (Mechanical Triplets)

AI applies the "Rule of Three" with mechanical frequency, adding a third element even when unnecessary:
- "focused, aligned, measurable"
- "No theory. No fluff. Just execution."
- "clarity, consistency, and creativity"
- "engaging, informative, and actionable"

Humans like triplets too, but AI uses them reflexively. If every list has exactly three items with perfect parallel structure, that's a pattern.

### Formulaic Section Structure

AI documents follow a rigid pattern per section:
1. Topic sentence stating the main point
2. 2-3 supporting sentences with evidence
3. Concluding sentence restating or transitioning

Every section, every time. Human writing breaks this pattern frequently — starting with an anecdote, burying the point mid-paragraph, ending abruptly for effect.

### Repetitive Subject-Verb-Object (SVO) Structure

AI defaults to simple SVO ordering, sentence after sentence. Human writing varies syntactic structure — inverted sentences, fronted adverbials, embedded clauses, occasional passive voice for strategic emphasis.

### Anaphora Abuse

Repeating the exact same sentence opening in quick succession. AI does this to create rhetorical momentum, but the effect is mechanical rather than persuasive:
- "They assume that users will pay... They assume that developers will build... They assume that ecosystems will emerge..."
- "We need to rethink... We need to rebuild... We need to reimagine..."

One or two repetitions can be powerful. Three or more in sequence reads as an AI pattern, not deliberate rhetoric.

### Tricolon Abuse

Stringing multiple three-part sentences back-to-back. AI applies parallel structure so aggressively that entire paragraphs become rhythmically identical:
- "Products impress people; platforms empower them. Products solve problems; platforms create worlds."

One balanced sentence per section is fine. Three in a row is a tell.

### Gerund Fragment Litany

Stringing together verbless fragments built on gerunds to simulate cinematic pacing:
- "Reviewing pull requests. Debugging edge cases. Attending architecture meetings."

AI uses this to create a montage effect — choppy, present-tense fragments that imply action without committing to actual narrative. Reads as a LinkedIn post or movie trailer, not prose.

### "Not X. Not Y. Just Z." Countdown

Dramatic negative parallelism to build fake tension before an unremarkable point:
- "Not a framework. Not a methodology. Just a better way to think about code."

The countdown structure manufactures significance for conclusions that don't earn it. If the final point is genuinely surprising, one contrast is enough.

### "Listicle in a Trench Coat"

Disguising lists by forcing items into uniformly sized paragraphs with sequential markers:
- "The first wall is..." / "The second wall is..." / "The third wall is..."

The content is a numbered list dressed up as an essay. Each "paragraph" is the same length, follows the same structure, and could be a bullet point. If every section starts with an ordinal marker, it's a listicle pretending to be long-form writing.

### Bold-First Bullets

Almost universally starting every bullet point with a bolded keyword followed by a colon and explanation. This creates visual uniformity that screams template:
- **Scalability:** The system handles...
- **Reliability:** The architecture ensures...
- **Security:** The framework provides...

Human bullet lists vary their formatting — some bold, some not, some with colons, some without.

### Fractal Summaries

Summarizing what it will say, saying it, then summarizing what it said — at every level of the document. Introduction previews all sections. Each section opens with a mini-preview and closes with a mini-summary. Conclusion re-summarizes everything. The result is a document that is 40% summary of itself.

### One-Point Dilution

Padding a single 800-word argument into 4,000 words of circular repetition with different metaphors. The core idea appears in the introduction, reappears with a sports analogy, shows up again with a historical parallel, and returns one more time in the conclusion. Each restatement uses different words but adds zero new information.

### Invented Concept Labels

AI creates fake compound terms and treats them as established concepts:
- "supervision paradox," "acceleration trap," "workload creep"

These cluster abstract problem-nouns with domain words to manufacture intellectual authority. The terms sound like they come from published research but don't — they're generated on the spot. Real domain terminology has citations; invented labels have scare quotes and no source.

---

## Emotional and Voice Tells

### Emotional Flatness

AI maintains a consistent emotional register throughout. No tonal shifts, no humor, no frustration, no enthusiasm that feels genuine. Even when prompted to be "passionate," the passion is uniform rather than peaking and ebbing.

### The Empathy Performance

AI produces performed empathy — template-shaped concern:
- "This can be incredibly frustrating..."
- "It's completely understandable that..."
- "Many people struggle with..."

Real empathy is specific. Performed empathy is generic.

### Missing Personality Markers

Human writing has quirks — interrupted thoughts, self-corrections, asides, opinions stated without justification, inside references, humor that risks falling flat. AI text is clean, balanced, and safe. That safety is itself a tell.

### The Absence of Lived Experience

AI can define "rain" and its associations, but has never been caught in a thunderstorm. This absence leads to generic sensory descriptions and "weak sauce" character/scenario renderings where truck drivers are gruff, businessmen are businesslike, and every sunset is "painted across the sky."

### False Vulnerability

Simulates self-awareness that reads as hollow. "And yes, since we're being honest..." or "This is not a rant; it's a diagnosis" — polished, risk-free pseudo-vulnerability. The "vulnerability" is pre-packaged and safe; it never risks actual discomfort or reveals genuine uncertainty. Real vulnerability is specific and uncomfortable — it names personal failures, admits confusion, or stakes out positions that might draw criticism.

### "Fake Casual Quotes"

Putting casualness in quotation marks to perform relatability rather than writing naturally:
- "what developers call 'good enough'"
- "what we might charitably call 'progress'"

The scare quotes signal "I'm being casual now" instead of actually being casual. Real informal writing doesn't announce itself — it just uses informal language directly.

### Compliment Sandwich

AI cannot deliver direct criticism. It invariably leads with a positive statement before addressing flaws, then ends with another positive. "The architecture is well-structured. However, the error handling needs significant improvement. Overall, this is a strong foundation." This pattern is so consistent that the opening compliment becomes a warning flag that criticism is coming.

### The Subtext Void

In human communication, people rarely say exactly what they mean — they use irony, sarcasm, repression, implication. AI lacks this intuitive understanding, producing dialogue and arguments that are too articulate, too civil, too perfectly structured.

---

## B2B and Professional "Workslop"

### Corporate-Heavy Clichés
When a business document is filled with "synergies," "paradigm shifts," and "best-in-class solutions," it was likely AI-padded. These industry clichés cause content to "blend in" rather than stand out.

### The "No Fluff" Irony
AI frequently includes "no fluff" to signal conciseness — but "no fluff" is itself filler. A phrase AI adds when prompted to be concise, signaling the opposite of what it claims.

### Institutional Padding
AI-generated professional content seeks to sound impressive without committing to specifics. Watch for paragraphs that feel authoritative but say nothing concrete — lots of abstract nouns, no specific numbers, examples, or evidence.

### AI Suspicion Tax
Formulaic phrases like "I hope this email finds you well" now trigger automated cybersecurity suspicion filters. A 1,265% surge in AI-linked phishing attacks since 2023 means that approximately 82.6% of phishing emails utilize AI-generated content. The result: legitimate AI-assisted professional writing gets caught in spam filters or triggers recipient suspicion simply because it matches known phishing patterns. Boilerplate openers and closers aren't just bad writing — they're now a security liability.

---

## The "Human Sandwich" Test

The most significant tell remains the absence of human strategy at the start and human editing at the end. Content that lacks both feels generic, robotic, and low-effort. The fix isn't to trick detectors — it's to add genuine human input: a real thesis, specific examples from experience, idiosyncratic word choices, and editing that breaks the patterns above.

---

## Measurement

### Burstiness Score

Measure sentence length standard deviation across a passage:
- **< 4.0** — highly uniform, strong AI signal
- **4.0-7.0** — moderate variance, could be either
- **> 7.0** — natural human variance
- **> 10.0** — strong human signal (dramatic variation)

### Hedging Density

Count qualifying words/phrases per 100 words:
- **< 1.0** — assertive (possibly over-confident)
- **1.0-3.0** — natural range
- **> 3.0** — excessive hedging, AI signal

### Transition Density

Count explicit transition words/phrases per paragraph:
- **0-1 per paragraph** — natural flow
- **2+ per paragraph consistently** — mechanical, AI signal

### Lexical Tell Count

Count words from the always-avoid list per 500 words:
- **0** — clean
- **1-2** — minor concern
- **3+** — strong AI signal

### Em Dash Density

Count em dashes per page (approximately 250 words):
- **0-2** — natural range
- **3-4** — elevated, worth checking
- **5+** — strong AI signal

### Convergent Signature

A high-confidence AI identification involves convergence of multiple signals:
1. **Lexical density** — high concentration of blacklisted words
2. **Structural monotony** — low burstiness, predictable paragraph shapes
3. **Typographic obsessions** — mechanical em dash use, rigid grammar
4. **Rhetorical crutches** — contrast framing, rule of three, "tada" intros
5. **Information voids** — lack of specific detail, lived experience, or subtext

No single pattern is conclusive. Three or more patterns converging is a strong signal.
