---
description: Detect contradictions between vision.md non-goals and planning/current.md acceptance criteria via stemmed token overlap.
argument-hint: "<project-dir> [--threshold 0.4]"
allowed-tools: Bash, Read
---

Run `doc-contradiction.py` against `$ARGUMENTS`. The validator finds candidate contradictions — for example, vision.md says "Not adding social features" and current.md proposes ACs that look like social features.

Run the script:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/doc-contradiction.py" $ARGUMENTS
```

Surface the output verbatim. Findings are advisory (always exit 0). Token-overlap detection surfaces candidates — semantic contradiction needs the user's judgment.
