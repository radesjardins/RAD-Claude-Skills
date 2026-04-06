---
name: hemingway-bridge
description: >
  This skill should be used when the user says "hemingway bridge", "wrap up session",
  "save my progress", "where did I leave off", "session handoff", "end of session",
  "capture what I was working on", "pick up where I left off", "PARA handoff",
  "what should I do next session", or wants to capture session state in a PARA-aware
  format before stopping work. Integrates with rad-session's wrapup/startup cycle.
version: 1.0.0
---

# Hemingway Bridge — PARA-Aware Session Handoffs

Capture session state using the Hemingway Bridge technique: stop work while momentum
is still high, document current status, next steps, and open questions so the next
session starts with zero ramp-up time.

Named after Hemingway's practice of stopping mid-sentence so he always knew where to
pick up the next day.

## When to Use

- End of any work session (before the user is exhausted)
- Pausing or shelving a project
- Before going on vacation or leave
- Handing off work to someone else
- When the user says "I'm done for today"
- Proactively at end of long sessions involving PARA work

## Hemingway Bridge Capture Process

### Step 1: Identify Active Context

Ask one question:
> "What were you working on today? Give me a quick brain dump -- projects touched,
> decisions made, anything unfinished."

If the session context is already clear from conversation history, skip the question
and proceed directly.

### Step 2: Build the Bridge

Capture these four elements:

1. **Current Status** -- What was just completed or accomplished
2. **Next Steps** -- What was planned next (be specific: "write the intro section"
   not "keep working on it")
3. **Open Questions** -- Unresolved decisions, blockers, or unknowns
4. **First Action** -- The single, concrete thing to do when returning
   (this eliminates decision fatigue at session start)

### Step 3: Map to PARA Context

Add PARA-specific context to the bridge:

- **Active Project:** Which project folder this work belongs to
- **Materials Created:** New IPs, notes, or drafts produced this session
- **Materials Needed:** What to gather or read before the next session
- **Capture Inbox:** Anything captured during the session that still needs
  to be sorted into PARA folders

### Step 4: Write the Bridge Note

Generate a bridge note in this format:

```markdown
## Hemingway Bridge — [Project Name]
**Date:** [today's date]
**Session Duration:** [approximate time spent]

### Status
[What was accomplished this session — outcomes only, not narrative]

### Next Steps
1. [Specific next action — the thing to do FIRST when returning]
2. [Second priority]
3. [Third priority]

### Open Questions
- [Decision or unknown that needs resolving]
- [Blocker or dependency]

### PARA Context
- **Project:** [Project folder name]
- **New IPs created:** [List any Intermediate Packets produced]
- **Unsorted captures:** [Items still in inbox needing classification]
- **Related materials:** [Notes/files to review next session]

### Momentum Notes
[Anything to preserve the creative state — a half-formed idea, an intuition
about direction, a connection noticed but not yet explored]
```

### Step 5: File the Bridge

Recommend where to save the bridge note:
- **Inside the project folder** if the work is project-specific
- **In the daily log** if multiple projects were touched
- **In HANDOFF.md** if integrating with rad-session (see below)

## Integration with rad-session

When the rad-session plugin is installed, the Hemingway Bridge integrates with the
`/wrapup` skill's three-tier persistence model:

### HANDOFF.md Integration

The bridge note maps to HANDOFF.md sections:

| Hemingway Bridge | HANDOFF.md Section |
|-----------------|-------------------|
| Status | Last Session Summary |
| Next Steps | Open Work |
| Open Questions | Open Work |
| First Action | Where I Left Off |
| Decisions made | Key Decisions |
| Failed approaches | What NOT To Do |
| New IPs created | Modified Files |
| Momentum Notes | Key Insights |

When `/wrapup` runs after a PARA-focused session, incorporate the PARA Context
section into the handoff:

```markdown
## Where I Left Off
- [Project Name]: [specific task in progress]
- PARA inbox has [N] unsorted captures from this session

## Open Work
- [Next Step 1]: [current state]
- [Open Question]: [context needed for decision]

## Key Insights
- New IP created: [description] — filed in [PARA location]
- [Momentum note or creative intuition worth preserving]
```

### Session Startup Integration

When starting a new session after a Hemingway Bridge was written:

1. Read the bridge note (or HANDOFF.md if using rad-session)
2. Present the "First Action" to the user immediately
3. Surface any unsorted inbox items for quick PARA classification
4. Resume work with full context -- zero ramp-up time

## Bonus: Send-Off Technique

Before wrapping up, suggest the user send a draft or work-in-progress for feedback:
> "Consider sharing what you have so far with someone for feedback. When you return,
> you'll have fresh input waiting -- a natural on-ramp back into the work."

This combines the Hemingway Bridge (preserving momentum) with the IP feedback loop
(getting external input while you're away).

## Key Principles

- **Stop before exhaustion.** The bridge works best when written with energy remaining.
- **Be specific, not vague.** "Write the introduction paragraph for the API doc" beats
  "keep working on the docs."
- **Preserve creative state.** Half-formed ideas and intuitions are the most fragile
  context -- capture them even if they feel incomplete.
- **One clear first action.** The next session should start with zero decision-making.

## Reference Files

For the full Hemingway Bridge technique and other creative techniques:
- **`../para-organize/references/creative_techniques.md`** -- Complete technique descriptions
