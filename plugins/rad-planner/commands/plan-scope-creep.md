---
description: Detect when current.md is doing things vision.md said are non-goals — focused scope-creep detection complementary to doc-contradiction.
argument-hint: "<project-dir> [--threshold 0.35]"
allowed-tools: Bash, Read
---

Run `scope-creep-detector.py` against `$ARGUMENTS`. The validator looks for two signals:

1. **Dropped non-goal**: a vision.md non-goal whose substantive tokens don't appear in current.md's `## Non-goals` section. The project-level boundary is no longer being acknowledged at the milestone level.

2. **Active creep**: a dropped non-goal whose tokens DO appear in current.md's `## Acceptance criteria` or `## Planned changes`. The milestone appears to be doing exactly what vision.md said it would not.

Severity:
- HIGH: active creep (dropped + appears in plan content).
- MEDIUM: dropped non-goal (boundary forgotten, not yet acted on).
- LOW: weak token match below the high-confidence threshold but worth review.

This is complementary to `/doc-contradiction` — same data sources, different signal: doc-contradiction flags any vision-non-goal-to-AC overlap; scope-creep filters to cases where the milestone non-goals also failed to preserve the boundary.

Run the script:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scope-creep-detector.py" $ARGUMENTS
```

Surface the output verbatim. Exit codes: `0` clean, `1` issues found, `2` script error.
