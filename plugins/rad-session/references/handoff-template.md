# HANDOFF.md Template

This is the canonical structure for HANDOFF.md files. The `/wrapup` skill follows this template every time, adapting content but keeping sections consistent across all projects.

## Template

```markdown
# Session Handoff

**Date:** YYYY-MM-DD
**Status:** [One-line project state]

## Last Session Summary
[2-4 sentences — outcomes, not play-by-play]

## Where I Left Off
- [Specific file, feature, or task in progress]
- [Include paths and line numbers when relevant]

## Key Decisions
- [Decision]: [Brief reasoning — the WHY matters more than the WHAT]

## What NOT To Do
- [Failed approach]: [Why it failed — so the next session doesn't retry it]
- [Gotcha discovered]: [What it is and how to avoid it]

## Open Work
- [Item]: [Current state described as a fact, not an instruction]

## Modified Files
- `path/to/file` — [what changed, briefly]

## Key Insights
[Non-obvious things the next session must know — API quirks, environment issues,
user preferences discovered, architectural constraints not captured in CLAUDE.md]
```

## Rules

1. **Every section is optional.** Omit sections that don't apply — never fill with "N/A" or "None."
2. **Be specific.** "`src/auth.ts:45-80` — added JWT validation middleware" beats "made auth changes."
3. **State, not instructions.** "Open Work" describes what IS, not what to DO. "EBirdProvider started, API auth not wired" — not "Wire up the eBird API auth next."
4. **Keep it scannable.** Bullet points over paragraphs. One idea per bullet.
5. **Target length:** 30-80 lines depending on session complexity. Lighter sessions get shorter handoffs.
6. **Traps are gold.** The "What NOT To Do" section is the most valuable part of the handoff — it prevents the next session from re-running dead ends. Always include a WHY.
