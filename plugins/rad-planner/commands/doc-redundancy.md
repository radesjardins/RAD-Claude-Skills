---
description: Detect cross-doc bullet duplicates via Jaccard similarity across the canonical doc set.
argument-hint: "<project-dir> [--threshold 0.6]"
allowed-tools: Bash, Read
---

Run `doc-redundancy.py` against `$ARGUMENTS`. The validator computes Jaccard similarity between bullet/checkbox items across `vision.md`, `architecture.md`, `planning/current.md`, and `decisions/*.md` to surface content that's been duplicated rather than cross-referenced.

Run the script:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/doc-redundancy.py" $ARGUMENTS
```

Surface the output verbatim. Findings are advisory (always exit 0) — the user judges whether each pair is a real redundancy or a legitimate restatement.
