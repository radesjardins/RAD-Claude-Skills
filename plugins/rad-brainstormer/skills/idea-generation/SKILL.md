---
name: idea-generation
description: >
  Generate ideas, I need more options, what else could work, give me alternatives,
  more ideas please. Pure divergent ideation using SCAMPER, Reverse Brainstorming,
  Starbursting, Analogical Thinking. For evaluation, use idea-evaluation.
---

# Idea Generation — Pure Divergent Thinking

Generate the maximum number of diverse, creative ideas using proven brainstorming methodologies. This skill is ONLY about generating ideas — evaluation comes later.

<HARD-GATE>
Do NOT evaluate, filter, rank, or dismiss any idea during this skill. All ideas are captured.
When the user evaluates during generation, redirect: "Good concern — let's capture that for later. What else comes to mind?"
</HARD-GATE>

## Mode Announcement

Start every session with:
> "We're in idea generation mode — all ideas welcome, no filtering. I'll ask you for ideas first, then add mine. We'll evaluate everything later."

## Anti-Anchoring Protocol

Draw out user ideas before offering alternatives:
1. "What ideas have you already been considering, even half-formed ones?"
2. Capture and acknowledge ALL user ideas
3. Then build on them: "Building on your idea about X, what if..."
4. Only then introduce new directions

## Technique Selection

Assess the situation and select the technique(s):

| Situation | Primary Technique | Support Technique |
|-----------|------------------|-------------------|
| Modifying/improving something | SCAMPER | Analogical Thinking |
| Stuck / can't think of anything | Reverse Brainstorm | Random Entry |
| Problem poorly understood | Starbursting | 5 Whys |
| Need creative alternatives | Six Thinking Hats (Green+Yellow) | Crazy 8s |
| Technical contradiction | TRIZ | Morphological Analysis |
| Need cross-domain inspiration | Analogical Thinking | Random Entry |
| Warm-up needed | Worst Possible Idea | Crazy 8s |
| Reframing needed | How Might We | Starbursting |

Load `references/methodology-catalog.md` for detailed technique instructions.

## Technique Execution

### SCAMPER
Work through all 7 lenses one at a time. For each:
- Ask the user a targeted question related to that lens
- Capture their ideas
- Build with "Yes, and..." additions
- Move to next lens

### Reverse Brainstorming
1. Flip the problem: "How could we make [problem] WORSE?"
2. Generate 8-12 "worst" ideas together
3. Invert each one into a potential solution
4. Capture all inversions as candidate ideas

### Starbursting
1. Place the topic in the center
2. Generate questions across all 6 dimensions: Who, What, When, Where, Why, How
3. Don't answer yet — just generate questions
4. The questions themselves reveal the solution space

### Analogical Thinking
1. Identify 3-5 analogous domains (nature, other industries, famous companies)
2. For each: "How does [domain] solve a similar challenge?"
3. Extract transferable principles
4. Apply to the current problem

### How Might We
1. Reframe the problem as multiple HMW questions (8-12)
2. Vary the angle: different stakeholders, moments, constraints
3. Select the most promising HMW questions
4. Generate 3-5 ideas for each selected question

### Crazy 8s (Adapted for text)
1. "Let's do rapid-fire: I'll give you 60 seconds per prompt. Don't overthink."
2. Give 8 prompts, one at a time
3. Capture whatever comes — quality doesn't matter
4. Review for unexpected gems

### Random Entry
1. Pick a random concept: "The word is '[random]'"
2. "What connections can you see between [random word] and your problem?"
3. Explore the unexpected associations
4. Often produces the most novel ideas

## Capturing Ideas

Maintain a running numbered list of ALL ideas generated:
```
## Ideas Generated So Far
1. [User's idea] — from: user
2. [Built on #1] — from: collaborative
3. [New direction] — from: brainstormer
...
```

Present the updated list periodically to keep track.

## When to Stop

The divergent phase ends when:
- Ideas start repeating or becoming incremental
- The user signals they're ready to move on
- After generating 15-25 ideas (a good target range)
- Energy is flagging

Transition: "We've generated [N] ideas. Ready to switch to evaluation mode? If so, I recommend using [framework] based on what we have."

If the user wants to evaluate, suggest they invoke the idea-evaluation skill or `/evaluate`.
