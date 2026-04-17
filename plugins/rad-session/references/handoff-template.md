# HANDOFF.md Template

Canonical structure for HANDOFF.md files. The `/wrapup` skill follows this template every time, adapting content but keeping sections consistent across all projects.

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
- TRIED: [specific approach that was attempted]
  FAILED BECAUSE: [root cause — not just "it didn't work"]
  CORRECT APPROACH: [what actually worked, or what should be tried instead — omit if unknown]

## Open Work
- [Item]: [Current state described as a fact, not an instruction]

## Modified Files
- `path/to/file` — [what changed, briefly]

## Key Insights
[Non-obvious things the next session must know — API quirks, environment issues,
user preferences discovered, architectural constraints not captured in CLAUDE.md]
```

## Canonical trap format (What NOT To Do)

Every trap entry uses a structured three-part form so `/startup` can reliably extract it into the next session's briefing without paraphrasing. The prefix tokens (`TRIED:`, `FAILED BECAUSE:`, `CORRECT APPROACH:`) are load-bearing — don't rewrite them.

**Full form (preferred):**

```
- TRIED: [specific approach that was attempted]
  FAILED BECAUSE: [root cause — not just "it didn't work"]
  CORRECT APPROACH: [what actually worked, or what should be tried instead]
```

**Compact form (when the correct approach is unknown):**

```
- TRIED: [approach] — FAILED BECAUSE: [root cause]
```

### Good vs. bad examples

**Bad** (unstructured, no root cause, no corrective action):
```
- Don't mock the Stripe webhook, it doesn't work
```

**Good** (full form):
```
- TRIED: mocking the Stripe webhook in integration tests
  FAILED BECAUSE: signature verification ran against the mock, not the real code path — prod broke on deploy
  CORRECT APPROACH: use `stripe listen` against a real test-mode endpoint
```

**Good** (compact form, correct approach not yet known):
```
- TRIED: sharing the Supabase client across server components — FAILED BECAUSE: cookies leaked between requests in RSC streaming
```

## Rules

1. **Every section is optional.** Omit sections that don't apply — never fill with "N/A" or "None."
2. **Be specific.** "`src/auth.ts:45-80` — added JWT validation middleware" beats "made auth changes."
3. **State, not instructions.** "Open Work" describes what IS, not what to DO. "EBirdProvider started, API auth not wired" — not "Wire up the eBird API auth next."
4. **Keep it scannable.** Bullet points over paragraphs. One idea per bullet.
5. **Target length:** 30-80 lines depending on session complexity. Lighter sessions get shorter handoffs.
6. **Traps are gold.** The "What NOT To Do" section is the most valuable part of the handoff — it prevents the next session from re-running dead ends. Always include a `FAILED BECAUSE:` clause with a real root cause.
