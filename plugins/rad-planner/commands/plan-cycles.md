---
description: Detect cycles in milestone dependency graphs across planning/current.md and (optionally) planning/archive/*.md.
argument-hint: "<plan-dir> [--include-archive]"
allowed-tools: Bash, Read
---

Run `dependency-cycle-detector.py` against `$ARGUMENTS`. The validator parses milestone dependencies from three conventions:

1. Dedicated `## Dependencies` section listing milestone IDs
2. Inline `Depends on: M1, M3` field anywhere in the doc
3. Per-AC `(depends on M2)` parenthetical

It builds a directed graph and runs DFS cycle detection. Self-dependencies (a milestone listing itself) are flagged MEDIUM. True cycles across multiple milestones are flagged HIGH.

For a single `current.md`, the graph is usually trivial. Pass `--include-archive` to also scan `planning/archive/*.md` for the full historical milestone graph.

Run the script:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/dependency-cycle-detector.py" $ARGUMENTS
```

Surface the output verbatim. Exit codes: `0` clean, `1` cycle detected, `2` script error.
