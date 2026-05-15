---
description: Flag acceptance criteria that have no apparent verification path in the plan's validation commands.
argument-hint: "<file> [--threshold 0.15]"
allowed-tools: Bash, Read
---

Run `coverage-validator.py` against `$ARGUMENTS`. The validator computes stemmed token overlap between each AC in `## Acceptance criteria` and the entries in `## Validation commands`.

Severity policy:
- HIGH: no `## Validation commands` section, or section is empty — every AC is uncovered.
- MEDIUM: a specific AC has overlap below threshold with every validation command.
- LOW: ratio of validation commands to ACs is suspiciously low (≥5 ACs, ratio <0.2).

This is heuristic. Token overlap can miss legitimate pairings (an AC about "rate limiting" validated by a command named `test:api`). The validator surfaces signals; the user judges.

Run the script:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/coverage-validator.py" $ARGUMENTS
```

Surface the output verbatim. Exit codes: `0` clean, `1` issues found, `2` script error.
