# The Wikipedia "Signs of AI Writing" Guide — and How rad-writer Relates to It

Wikipedia's editor community published [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) in September 2025. As of April 2026, it is widely considered the most credible publicly maintained reference on the subject — TechCrunch called it "the best guide to spotting AI writing."

This file is a pointer + relation note, not a copy. Read the source.

## Why it's the canonical 2026 reference

- **Empirically grounded and timestamped** — explicitly notes which lexical clusters belong to which model era and which tells are already deprecated by newer models.
- **Editor-community curated** — Wikipedia editors deal with AI-padded edits at scale; their pattern catalog is built from forensic experience, not vendor marketing.
- **Honest about limits** — does not claim detection accuracy. Lists patterns as evidence to weigh, not verdicts.
- **Continuously updated** — unlike a published book or static blog post, it adapts as models evolve.

## Key findings rad-writer reflects

The Wikipedia guide and supporting research (Kobak et al. on excess vocabulary, Goedecke on em dashes, the "Catch Me If You Can?" EMNLP 2025 paper on voice mimicry, the arXiv "Uncertainty in Authorship" paper on detection theory) have shifted the consensus:

1. **AI text detection is structurally impossible at high confidence.** As LLM output distributions converge to human distributions, error floors approach chance. ([arXiv:2509.11915](https://arxiv.org/html/2509.11915v1))
2. **The 2023-2024 lexical tells are partially deprecated.** "Delve" usage in newer models dropped sharply in 2025. GPT-5.1 suppressed em dash usage. Model providers actively patch named tells once they go public. Word lists are a moving target.
3. **Structural patterns are more durable than lexical ones.** Rule of three abuse, copula avoidance ("serves as" replacing "is"), elegant variation (synonym rotation), present participle stacking, and the specificity gap emerge from next-token probability dynamics — harder to suppress without changing model behavior fundamentally.
4. **Multiple major universities have disabled AI detection institutionally** (Vanderbilt, Cornell, multiple UC campuses, Pittsburgh, Iowa, Waterloo, Johns Hopkins position) due to false-positive risk and equity concerns.
5. **Stanford HAI documented 61.3% false-positive rate against non-native English writers**, with one detector flagging 97.8% of TOEFL essays as AI. This finding has not been overturned.
6. **OpenAI built and shelved a 99.9%-effective watermarking system** because internal research showed 30% user defection if deployed. The detection problem is partially solvable, but commercially / institutionally not.

## What rad-writer does and doesn't claim, given this context

| rad-writer claim | Honesty status |
|---|---|
| "Frame as craft improvement, not detection" | **Aligned with consensus.** The skill's AI audit mode says verbatim: "Never claim to detect AI authorship — report patterns, not verdicts." |
| "Lexical blocklist (250+ words/phrases)" | **Partial.** Most are still cliché worth replacing; framing them as "AI tells" is a lagging signal in 2026. The blocklist remains as **style guidance** (these are stale words), with caveats that their AI-tell status is degrading. |
| "Burstiness as a measurement" | **Partial.** Still directionally valid but: (a) newer models produce higher burstiness; (b) non-native English writers naturally produce low burstiness; (c) technical/legal writing produces low burstiness. Use as soft signal. |
| "Em dash density as a measurement" | **Partial.** GPT-5.1 actively suppresses em dashes. The "every 50-80 words vs. every 500" ratio is practitioner folklore, not peer-reviewed. The directional finding (em dashes were elevated in GPT-4o output) is correct. |
| "Voice profile from 3-5 samples → write in your voice" | **Partial.** EMNLP 2025 Findings paper showed structured-genre voice mimicry (emails, news) reaches 95-97% accuracy; informal-genre voice mimicry (blogs, Reddit) sits at 19-21%. More samples (2 → 10) yield "very little" improvement. The profile schema is honest in calling profiles "descriptive patterns that inform style guidance"; some marketing language overpromises. |
| "Specificity gap, vague attribution, register drift" as durable tells | **Aligned.** These are the structural patterns the consensus identifies as more durable than lexical surface features. |

## Recommended reading order if you're new to this

1. [Wikipedia: Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) — start here
2. [The best guide to spotting AI writing comes from Wikipedia (TechCrunch, Nov 2025)](https://techcrunch.com/2025/11/20/the-best-guide-to-spotting-ai-writing-comes-from-wikipedia/) — context on why
3. [Uncertainty in Authorship: Why Perfect AI Detection Is Mathematically Impossible (arXiv:2509.11915)](https://arxiv.org/html/2509.11915v1) — the theoretical impossibility argument
4. [Catch Me If You Can? Not Yet — EMNLP 2025 Findings](https://aclanthology.org/2025.findings-emnlp.532.pdf) — what voice mimicry can and can't do
5. [Pangram: Why Perplexity and Burstiness Fail to Detect AI](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai) — practical rebuttal of the dominant detection method

The rad-writer skill's `ai-writing-patterns.md` reference is structured to align with this view: durable structural tells first, lexical tells second with explicit "this signal is degrading" notes.
