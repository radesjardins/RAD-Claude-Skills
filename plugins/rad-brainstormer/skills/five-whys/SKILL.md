---
name: five-whys
description: >
  This skill should be used when the user says "5 whys", "root cause analysis",
  "why does this keep happening", "find the root cause", "trace this problem",
  or needs to dig beneath surface symptoms to find the real problem before
  brainstorming solutions. Based on Toyota's production system methodology.
argument-hint: "[problem or symptom to trace]"
---

Apply the 5 Whys root cause analysis to: **$ARGUMENTS**

Originally from Toyota's production system, adapted here for brainstorming. The goal is to ensure the RIGHT problem is being solved before generating solutions.

## The Process

Start with the stated problem, then ask "Why?" repeatedly:

1. **Problem**: [stated problem]
   "Why does this happen?" / "Why is this a problem?"

2. **Why 1**: [user's answer]
   "And why does THAT happen?"

3. **Why 2**: [user's answer]
   "And why is that the case?"

4. **Why 3**: [user's answer]
   "What causes that?"

5. **Why 4**: [user's answer]
   "And what's behind that?"

6. **Why 5**: [user's answer — likely close to root cause]

## Rules
- The user drives the answers. Ask one "Why?" at a time.
- Do not lead — genuinely ask, do not suggest the answer.
- Sometimes 3 Whys are enough. Sometimes 7 are needed. Stop when hitting a root cause (something systemic, structural, or foundational).
- If the chain branches (multiple causes), explore the most impactful branch first.
- It is acceptable to conclude "Why #3 is the real root cause here."

## After Finding the Root Cause
Present: "Now that [root cause] has been identified as the core issue, this is what to brainstorm solutions for — not the original symptom of [stated problem]. Proceed to brainstorm solutions for this root cause?"

If yes, recommend the appropriate brainstorming technique based on the root cause nature. Consult `references/methodology-catalog.md` for technique selection guidance.
