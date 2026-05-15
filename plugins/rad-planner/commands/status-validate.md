---
description: Validate a docs/status.md file against the 8-section schema, freshness, and evidence-based results.
argument-hint: "<file>"
allowed-tools: Bash, Read
---

Run `status-validator.py` against `$ARGUMENTS`. The validator checks:

- All 8 expected sections present
- Freshness vs git mtime (warns if stale)
- Validation results are evidence-based (commands run, output captured), not chat synthesis

Run the script:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/status-validator.py" $ARGUMENTS
```

Surface the output verbatim. Exit codes: `0` clean, `1` issues, `2` script error.

This command works on any `status.md`-shaped file — it doesn't require rad-session to be installed, but the schema it validates was designed by rad-session.
