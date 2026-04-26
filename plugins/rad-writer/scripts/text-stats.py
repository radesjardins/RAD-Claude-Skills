#!/usr/bin/env python3
"""
text-stats.py — Deterministic measurement of writing patterns.

Computes the metrics rad-writer's skills *describe* — burstiness, em dash density,
hedging density, transition density, sentence/paragraph distributions — directly,
without asking an LLM to eyeball them. Use this in the ai-audit / review skills as
the measurement layer; let the LLM focus on what mechanical metrics can't see
(specificity, voice, lived-experience, register coherence).

Mode:
  full       all metrics (default)
  burstiness sentence-length variance only
  em-dash    em-dash density only
  hedging    hedging density only
  transitions  transition density per paragraph
  paragraphs paragraph length distribution

Usage:
  python3 text-stats.py <file.md|->                       # text or stdin
  python3 text-stats.py - < paste.txt
  python3 text-stats.py file.md --json
  python3 text-stats.py file.md --mode burstiness

Output:
  Default — human-readable text report
  --json  — single JSON object

Exit codes:
  0  any text successfully analyzed (does NOT mean "clean" — these are measurements)
  2  script error (file missing, empty input)

Important framing — read this before relying on the output:

  These metrics are 2023-2024-era stylometric features. They were strong AI signals
  for GPT-3.5 / GPT-4 / Claude 2 output. Newer models (Claude 4.x, GPT-5+) are
  actively suppressing several of them — em dash density in particular dropped
  sharply with GPT-5.1. Treat any single metric as weak evidence; convergent
  patterns across 3+ metrics carry more weight. Do NOT use these to claim
  "this text is X% AI-generated." That claim is not supportable in 2026
  (see arXiv:2509.11915 — perfect AI detection is mathematically impossible).

Pure stdlib Python 3.8+. No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

# Sentence splitter — heuristic, not perfect, but stable across paragraphs
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(\[])")
WORD = re.compile(r"\b[\w'-]+\b")
PARA_SPLIT = re.compile(r"\n\s*\n+")
EM_DASH = re.compile(r"[—–]")  # em dash + en dash
SENTENCE_OPENER = re.compile(r"^[\s\"'(\[]*([A-Za-z]+)")

# Hedging vocabulary — qualifiers that, in clusters, signal uncertainty padding
HEDGES = {
    "may", "might", "could", "perhaps", "possibly", "potentially", "arguably",
    "seemingly", "apparently", "presumably", "ostensibly", "purportedly",
    "somewhat", "rather", "fairly", "quite", "relatively", "moderately",
    "generally", "typically", "usually", "often", "sometimes", "frequently",
    "tends", "tend", "appears", "appear", "seems", "seem", "suggest", "suggests",
    "indicate", "indicates", "imply", "implies", "likely", "unlikely", "probably",
}

# Mechanical transition markers — count per paragraph
TRANSITIONS = {
    "furthermore", "additionally", "moreover", "however", "consequently",
    "subsequently", "nevertheless", "nonetheless", "therefore", "thus", "hence",
    "accordingly", "indeed", "notably", "importantly", "specifically",
    "fundamentally", "ultimately", "essentially", "namely",
}

# AI-associated lexical tells (2023-2024 era — see ai-writing-patterns.md
# for current durability notes; these are NOT a detector, just style markers).
LEXICAL_TELLS = {
    # verbs
    "delve", "delves", "delving", "leverage", "leverages", "leveraging",
    "utilize", "utilizes", "utilizing", "harness", "harnesses", "harnessing",
    "streamline", "streamlines", "streamlining", "underscore", "underscores",
    "underscoring", "foster", "fosters", "fostering", "elevate", "elevates",
    "elevating", "empower", "empowers", "empowering", "spearhead", "spearheads",
    "bolster", "bolsters", "bolstering", "catalyze", "catalyzes",
    "facilitate", "facilitates", "facilitating", "embark", "embarks",
    "embarking", "unpack", "unpacks", "unpacking", "encompass", "encompasses",
    "captivate", "captivates", "resonate", "resonates", "resonating",
    "revolutionize", "revolutionizes", "transform", "transforms",
    # adjectives
    "pivotal", "robust", "innovative", "seamless", "comprehensive", "nuanced",
    "multifaceted", "groundbreaking", "transformative", "holistic",
    "meticulous", "intricate", "invaluable", "paramount", "indispensable",
    # nouns
    "landscape", "realm", "tapestry", "synergy", "synergies", "testament",
    "paradigm", "cornerstone", "linchpin", "bedrock", "nexus", "crucible",
    "beacon", "catalyst", "interplay", "intricacies", "plethora", "myriad",
    # adverbs
    "arguably", "undeniably", "remarkably", "fundamentally", "inherently",
    "intrinsically",
}


# ---------- parsing ----------


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in PARA_SPLIT.split(text) if p.strip()]


def split_sentences(paragraph: str) -> list[str]:
    # Strip markdown headings, list markers, and code fences
    cleaned = re.sub(r"^[#>\-*]+\s*", "", paragraph, flags=re.MULTILINE)
    cleaned = re.sub(r"`[^`]*`", "", cleaned)  # inline code
    parts = SENT_SPLIT.split(cleaned)
    return [s.strip() for s in parts if s.strip()]


def count_words(text: str) -> int:
    return len(WORD.findall(text))


# ---------- metrics ----------


def burstiness(sentences: list[str]) -> dict:
    lengths = [count_words(s) for s in sentences if count_words(s) > 0]
    if len(lengths) < 2:
        return {"sentence_count": len(lengths), "mean": 0, "stdev": 0,
                "min": 0, "max": 0, "interpretation": "too few sentences to measure"}
    mean = statistics.mean(lengths)
    sd = statistics.stdev(lengths)
    interp = (
        "very uniform (≤4) — historical AI signal, but newer models also produce this"
        if sd <= 4 else
        "moderate variance (4-7) — could be either"
        if sd <= 7 else
        "natural variance (7-10) — typical of varied human writing"
        if sd <= 10 else
        "high variance (>10) — strong human signal (dramatic length variation)"
    )
    return {
        "sentence_count": len(lengths),
        "mean": round(mean, 2),
        "stdev": round(sd, 2),
        "min": min(lengths),
        "max": max(lengths),
        "interpretation": interp,
    }


def em_dash_density(text: str) -> dict:
    em_count = len(EM_DASH.findall(text))
    word_count = count_words(text)
    if word_count == 0:
        return {"em_dash_count": 0, "word_count": 0, "per_250_words": 0,
                "interpretation": "no text"}
    per_250 = round(em_count / word_count * 250, 2)
    interp = (
        "natural range (0-2 per 250 words)"
        if per_250 <= 2 else
        "elevated (2-4 per 250 words) — historical AI signal but GPT-5+ suppresses this"
        if per_250 <= 4 else
        "high (>4 per 250 words) — was strong AI signal in 2023-2024 era"
    )
    return {
        "em_dash_count": em_count,
        "word_count": word_count,
        "per_250_words": per_250,
        "interpretation": interp,
    }


def hedging_density(text: str) -> dict:
    words = [w.lower() for w in WORD.findall(text)]
    if not words:
        return {"word_count": 0, "hedge_count": 0, "per_100_words": 0,
                "interpretation": "no text"}
    hedges = sum(1 for w in words if w in HEDGES)
    per_100 = round(hedges / len(words) * 100, 2)
    interp = (
        "low hedging (<1 per 100 words) — assertive (could be over-confident)"
        if per_100 < 1 else
        "natural range (1-3 per 100 words)"
        if per_100 <= 3 else
        "high hedging (>3 per 100 words) — possible padding/AI signal in clusters"
    )
    return {
        "word_count": len(words),
        "hedge_count": hedges,
        "per_100_words": per_100,
        "interpretation": interp,
    }


def transition_density(paragraphs: list[str]) -> dict:
    if not paragraphs:
        return {"paragraph_count": 0, "transition_count": 0,
                "per_paragraph": 0, "interpretation": "no paragraphs"}
    total_transitions = 0
    by_paragraph: list[int] = []
    for p in paragraphs:
        words = [w.lower() for w in WORD.findall(p)]
        count = sum(1 for w in words if w in TRANSITIONS)
        by_paragraph.append(count)
        total_transitions += count
    per_para = round(total_transitions / len(paragraphs), 2)
    interp = (
        "natural flow (0-1 per paragraph)"
        if per_para <= 1 else
        "elevated (1-2 per paragraph) — leans mechanical"
        if per_para <= 2 else
        "high (>2 per paragraph) — strong mechanical-transition signal"
    )
    high_paragraphs = [i + 1 for i, c in enumerate(by_paragraph) if c >= 2]
    return {
        "paragraph_count": len(paragraphs),
        "transition_count": total_transitions,
        "per_paragraph": per_para,
        "high_density_paragraphs": high_paragraphs,
        "interpretation": interp,
    }


def paragraph_distribution(paragraphs: list[str]) -> dict:
    if not paragraphs:
        return {"count": 0, "mean_sentences": 0, "stdev_sentences": 0,
                "interpretation": "no paragraphs"}
    sentence_counts = [len(split_sentences(p)) for p in paragraphs]
    if len(sentence_counts) < 2:
        return {"count": len(sentence_counts), "mean_sentences": sentence_counts[0],
                "stdev_sentences": 0, "interpretation": "single paragraph"}
    mean = statistics.mean(sentence_counts)
    sd = statistics.stdev(sentence_counts)
    uniform = sd < 1.5
    return {
        "count": len(sentence_counts),
        "mean_sentences": round(mean, 2),
        "stdev_sentences": round(sd, 2),
        "min_sentences": min(sentence_counts),
        "max_sentences": max(sentence_counts),
        "uniform": uniform,
        "interpretation": (
            "uniform paragraph lengths (SD < 1.5) — leans templated/AI"
            if uniform else
            "varied paragraph lengths"
        ),
    }


def lexical_tell_count(text: str) -> dict:
    words = [w.lower() for w in WORD.findall(text)]
    if not words:
        return {"word_count": 0, "tell_count": 0, "tells": [],
                "per_500_words": 0, "interpretation": "no text"}
    found: dict[str, int] = {}
    for w in words:
        if w in LEXICAL_TELLS:
            found[w] = found.get(w, 0) + 1
    total = sum(found.values())
    per_500 = round(total / len(words) * 500, 2)
    interp = (
        "clean (0 lexical tells)"
        if total == 0 else
        f"minor ({total} occurrences across {len(found)} unique tells)"
        if total <= 2 else
        f"elevated ({total} occurrences) — was a strong 2023-2024 AI signal; less reliable in 2026 as 'delve' etc. have been deprecated by newer models"
    )
    return {
        "word_count": len(words),
        "tell_count": total,
        "unique_tells": len(found),
        "tells": dict(sorted(found.items(), key=lambda kv: -kv[1])),
        "per_500_words": per_500,
        "interpretation": interp,
    }


# ---------- output ----------


def render_text(report: dict) -> str:
    lines: list[str] = []
    lines.append(f"text-stats: {report['file']}  ({report['word_count']} words, {report['paragraph_count']} paragraphs)")
    lines.append("")
    lines.append("NOTE: These are 2023-2024-era stylometric features. Newer models (Claude 4.x,")
    lines.append("GPT-5+) actively suppress several of them. Use as soft signals only — never")
    lines.append("as 'this is X% AI-generated'. Detection is impossible per arXiv:2509.11915.")

    if "burstiness" in report:
        b = report["burstiness"]
        lines.append("")
        lines.append("BURSTINESS (sentence-length variance)")
        lines.append(f"  sentences: {b['sentence_count']}  mean: {b['mean']}  SD: {b['stdev']}  range: {b['min']}-{b['max']}")
        lines.append(f"  → {b['interpretation']}")

    if "em_dash" in report:
        e = report["em_dash"]
        lines.append("")
        lines.append("EM DASHES")
        lines.append(f"  count: {e['em_dash_count']}  per 250 words: {e['per_250_words']}")
        lines.append(f"  → {e['interpretation']}")

    if "hedging" in report:
        h = report["hedging"]
        lines.append("")
        lines.append("HEDGING DENSITY")
        lines.append(f"  hedges: {h['hedge_count']}  per 100 words: {h['per_100_words']}")
        lines.append(f"  → {h['interpretation']}")

    if "transitions" in report:
        t = report["transitions"]
        lines.append("")
        lines.append("MECHANICAL TRANSITIONS (Furthermore/Additionally/Moreover/etc.)")
        lines.append(f"  total: {t['transition_count']}  per paragraph: {t['per_paragraph']}")
        if t.get("high_density_paragraphs"):
            lines.append(f"  high-density paragraphs (≥2): {t['high_density_paragraphs']}")
        lines.append(f"  → {t['interpretation']}")

    if "paragraphs" in report:
        p = report["paragraphs"]
        lines.append("")
        lines.append("PARAGRAPH LENGTH DISTRIBUTION")
        lines.append(f"  paragraphs: {p['count']}  mean sentences: {p['mean_sentences']}  SD: {p['stdev_sentences']}  range: {p.get('min_sentences', 0)}-{p.get('max_sentences', 0)}")
        lines.append(f"  → {p['interpretation']}")

    if "lexical" in report:
        l = report["lexical"]
        lines.append("")
        lines.append("LEXICAL TELLS (2023-2024 era — see ai-writing-patterns.md for current durability)")
        lines.append(f"  total: {l['tell_count']}  unique: {l['unique_tells']}  per 500 words: {l['per_500_words']}")
        if l.get("tells"):
            top = list(l["tells"].items())[:8]
            lines.append(f"  top: {', '.join(f'{w}({c})' for w, c in top)}")
        lines.append(f"  → {l['interpretation']}")

    lines.append("")
    lines.append("REMEMBER: convergent patterns matter more than any single metric.")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", help="Path to text file, or '-' for stdin")
    p.add_argument(
        "--mode",
        choices=("full", "burstiness", "em-dash", "hedging", "transitions", "paragraphs", "lexical"),
        default="full",
    )
    p.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = p.parse_args(argv)

    if args.path == "-":
        text = sys.stdin.read()
        source = "<stdin>"
    else:
        path = Path(args.path)
        if not path.exists():
            print(f"error: file not found: {path}", file=sys.stderr)
            return 2
        text = path.read_text(encoding="utf-8", errors="replace")
        source = str(path)

    if not text.strip():
        print("error: empty input", file=sys.stderr)
        return 2

    paragraphs = split_paragraphs(text)
    sentences = []
    for p_text in paragraphs:
        sentences.extend(split_sentences(p_text))

    report: dict = {
        "file": source,
        "word_count": count_words(text),
        "paragraph_count": len(paragraphs),
    }

    if args.mode in ("full", "burstiness"):
        report["burstiness"] = burstiness(sentences)
    if args.mode in ("full", "em-dash"):
        report["em_dash"] = em_dash_density(text)
    if args.mode in ("full", "hedging"):
        report["hedging"] = hedging_density(text)
    if args.mode in ("full", "transitions"):
        report["transitions"] = transition_density(paragraphs)
    if args.mode in ("full", "paragraphs"):
        report["paragraphs"] = paragraph_distribution(paragraphs)
    if args.mode in ("full", "lexical"):
        report["lexical"] = lexical_tell_count(text)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_text(report))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
