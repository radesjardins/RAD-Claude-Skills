---
description: Flag a plan that lacks any effort/size estimate signal (section, inline field, milestone-suffix, or per-AC parenthetical).
argument-hint: "<file>"
allowed-tools: Bash, Read
---

Run `estimate-validator.py` against `$ARGUMENTS`. The validator scans a planning/current.md for any conventional estimate signal:

1. Dedicated section: `## Effort`, `## Estimate`, `## Size`, `## Sizing`, `## Complexity`
2. Inline field: `Effort: M`, `Estimate: ~2 days`, `Size: Large`
3. T-shirt size suffix on the milestone line: `M2 (M):` or `M3 [L]`
4. Per-AC parenthetical: `- [ ] Task X (S)` or `- [ ] Task Y (~2d)`

If none are present, the plan is flagged MEDIUM. Partial coverage (some ACs estimated but not most) is flagged LOW.

Run the script:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/estimate-validator.py" $ARGUMENTS
```

Surface the output verbatim. Exit codes: `0` clean (at least one signal present), `1` issues found (no estimate signals), `2` script error.
