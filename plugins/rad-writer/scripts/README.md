# rad-writer scripts

Deterministic measurement layer for the rad-writer skills. Replaces "ask the LLM to count em dashes" with actual Python computation. Saves tokens, gives reproducible results, and makes claims like "burstiness SD" mean something concrete.

All scripts are pure Python 3.8+ stdlib. No `pip install` required.

## Honest framing — read this before relying on the output

These scripts measure 2023-2024-era stylometric features that were strong AI signals for GPT-3.5 / GPT-4 / Claude 2 output. The 2026 reality:

- **Newer models actively suppress these patterns.** GPT-5.1 dropped em dash usage. "Delve" usage in newer model output declined sharply per Wikipedia's "Signs of AI Writing" guide.
- **Word-list matching is a soft signal.** Humanizers defeat it in one pass; human writers absorb AI vocabulary culturally; the cat-and-mouse game has no stable equilibrium.
- **Perfect AI detection is mathematically impossible.** See arXiv:2509.11915 — as model output distributions converge to human distributions, detection error floors approach chance.

Use the scripts to *measure craft features* that happen to correlate with AI output. The most useful framing for a writer is: "high lexical-tell density signals stale vocabulary worth refreshing, regardless of authorship." Avoid framings like "this is X% AI-generated" — that claim is not supportable in 2026.

## text-stats.py

Computes the measurable features:

```bash
python3 scripts/text-stats.py file.md                          # all metrics
python3 scripts/text-stats.py file.md --json
python3 scripts/text-stats.py file.md --mode burstiness
python3 scripts/text-stats.py file.md --mode em-dash
python3 scripts/text-stats.py file.md --mode hedging
python3 scripts/text-stats.py file.md --mode transitions
python3 scripts/text-stats.py file.md --mode paragraphs
python3 scripts/text-stats.py file.md --mode lexical
echo "$TEXT" | python3 scripts/text-stats.py -
```

Reports:
- **Burstiness** — sentence-length mean, SD, range, with interpretation tier
- **Em dash density** — count and per-250-words rate
- **Hedging density** — qualifier word count per 100 words
- **Mechanical transitions** — Furthermore/Additionally/Moreover/etc. per paragraph; flags high-density paragraphs by index
- **Paragraph length distribution** — mean sentences, SD, range, "uniform" flag
- **Lexical tell count** — unique tells found + frequency, top items

Every metric ships with the same caveat: this was a strong signal in 2023-2024 era; 2026 newer models suppress several of these; convergent patterns matter more than any single metric.

**Exit codes:** `0` always (these are measurements, not pass/fail), `2` script error.

## check-blocklist.py

Deterministic word-list scan with line/column locations and replacement suggestions:

```bash
python3 scripts/check-blocklist.py file.md
python3 scripts/check-blocklist.py file.md --severity always-avoid
python3 scripts/check-blocklist.py file.md --top 20
python3 scripts/check-blocklist.py file.md --json
python3 scripts/check-blocklist.py --list                       # print blocklist itself
echo "$TEXT" | python3 scripts/check-blocklist.py -
```

Catches single-word matches (delve, leverage, foster, robust, etc.) and multi-word phrases ("it's important to note", "in today's [X] landscape", "let's dive in", etc.) with severity tiers:

- **always-avoid** — strong style noise even outside AI-detection context
- **context** — fine in some domains (e.g., "robust" in engineering) but flagged in general writing
- **watch** — not a categorical reject; cluster signal

**Exit codes:** `0` no matches, `1` matches found, `2` script error.

## When the skills run these scripts

| Skill | Script | When |
|---|---|---|
| `ai-audit` | `text-stats.py --json` + `check-blocklist.py --json` | Before LLM analysis — gives the LLM concrete numbers to discuss |
| `review` (`--thorough`) | `text-stats.py --json` + `check-blocklist.py --json` | Pre-feeds writing-reviewer agent |
| `improve` | `check-blocklist.py --json` | To pre-flag specific words for the LLM to consider replacing |
| `write` | (none — generation phase) | Scripts are for analysis, not generation |

## What these scripts deliberately do NOT do

- **Do not compute an "AI score"** — there is no defensible single number. Each metric ships with its own interpretation tier and caveats.
- **Do not modify the text.** They report; the user (or a downstream skill) decides what to change.
- **Do not check semantic AI tells** — vague attribution, specificity gap, register drift, lived-experience absence — those need LLM judgment.
- **Do not validate that newer-model AI output looks like older-model AI output.** Many tells documented here are GPT-3.5/GPT-4 vintage; current frontier models behave differently.
- **Do not claim authorship.** "X patterns associated with AI output" ≠ "this is AI."
