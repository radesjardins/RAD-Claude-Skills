---
description: Lint a plan-shaped markdown file for required sections, AC checkbox format, and vague language.
argument-hint: "<file> [--mode sections|checklist|status|all]"
allowed-tools: Bash, Read
---

Run `plan-lint.py` against `$ARGUMENTS`. The validator checks:

- Required sections present (Objective, Current milestone, Acceptance criteria, Validation commands, Stop conditions, Notes for the next session)
- Acceptance criteria use the `- [ ]` checkbox format
- Validation commands appear runnable
- No vague language in critical fields ("verify it works", "should work", "tbd", etc.)

If no `--mode` flag is supplied, default to `--mode all`.

Run the script:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/plan-lint.py" $ARGUMENTS
```

Surface the output verbatim. The exit code is significant: `0` = clean, `1` = issues found, `2` = script error. If `2`, the file is likely missing or unreadable — surface the error.

This command works on any plan-shaped markdown — it doesn't have to be inside a rad-planner project.
