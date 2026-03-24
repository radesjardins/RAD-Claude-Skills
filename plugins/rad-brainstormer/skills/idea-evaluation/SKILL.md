---
name: idea-evaluation
description: >
  This skill should be used when the user says "evaluate these ideas", "which idea
  is best", "help me prioritize", "compare these options", "rank these", "how do I
  choose", or has a set of ideas and needs structured evaluation. Provides frameworks
  like Impact/Effort Matrix, Assumption Mapping, Pre-Mortem, JTBD, and Dot Voting
  to filter, rank, and select from existing ideas.
argument-hint: "[topic or problem]"
---

# Idea Evaluation — Structured Convergent Thinking

Evaluate, prioritize, and select the strongest ideas using proven evaluation frameworks. This skill is ONLY about evaluation — ideation should already be complete.

## Mode Announcement

> "We're in evaluation mode now. We'll look at each idea critically and constructively to find the strongest candidates."

## Step 1: Gather the Idea Set

If ideas aren't already listed:
- Ask the user to enumerate all candidate ideas
- Ensure the list is complete: "Are there any other options we should consider before evaluating?"
- Number each idea for easy reference

## Step 2: Select Framework

Reference `references/evaluation-frameworks.md` for detailed guidance on each.

| Situation | Recommended Framework | Why |
|-----------|----------------------|-----|
| 10+ ideas, need quick triage | **Impact/Effort Matrix** | Fast visual sorting into 4 quadrants |
| 3-5 ideas, need deep validation | **Assumption Mapping** | Tests what needs to be true for each to work |
| Product/feature ideas | **Opportunity Solution Trees** | Connects solutions to user outcomes |
| High-stakes decision | **Pre-Mortem + Assumption Mapping** | Catches blind spots and untested assumptions |
| 2-3 finalists, need to compare | **Dot Voting** (multi-criteria scoring) | Transparent, structured comparison |
| "Who is this for?" unclear | **Jobs-to-be-Done** lens | Reframes around user needs |

Recommend a framework and explain why, but let the user choose.

## Step 3: Apply the Selected Framework

### Impact/Effort Matrix
1. Define "impact" criteria with user (business value? user value? strategic alignment?)
2. Define "effort" criteria (development time? complexity? dependencies? risk?)
3. For each idea, collaboratively score impact (1-5) and effort (1-5)
4. Place on the 2x2 grid:
   - **Quick Wins** (high impact, low effort) — Do these first
   - **Major Projects** (high impact, high effort) — Plan carefully
   - **Fill-ins** (low impact, low effort) — When time allows
   - **Hard Slogs** (low impact, high effort) — Deprioritize or drop
5. Present the grid and recommended priority order

### Assumption Mapping
1. For each top idea, ask: "What needs to be true for this to work?"
2. Generate assumptions across: Desirability, Feasibility, Viability, Adaptability
3. For each assumption, assess:
   - Importance: How critical? (High/Medium/Low)
   - Evidence: How much proof? (Strong/Some/None/Contradicted)
4. Plot on 2x2: Importance vs Evidence
5. Focus on top-left quadrant (high importance, low evidence) — these are the riskiest assumptions
6. For each risky assumption, suggest how to test it cheaply

### Pre-Mortem
1. "Imagine it's 6 months from now. Idea [X] was implemented and failed spectacularly. Why?"
2. Generate 5-8 failure scenarios together (user first, then brainstormer adds)
3. For each: likelihood (H/M/L) and preventability (Y/P/N)
4. High-likelihood, preventable failures → these become design requirements
5. High-likelihood, non-preventable failures → these might kill the idea

### Opportunity Solution Trees
1. Clarify the desired outcome (the metric to move)
2. Map opportunities (user needs, pain points) under the outcome
3. Map each idea under the opportunity it addresses
4. Check: are some opportunities over-served (many solutions) while others are empty?
5. Focus on the highest-value opportunity with the fewest good solutions

### Jobs-to-be-Done Lens
1. For each idea, ask: "What job is the user hiring this to do?"
2. Explore three dimensions:
   - Functional: What task do they need to accomplish?
   - Social: How do they want to be perceived?
   - Emotional: How do they want to feel?
3. Ideas that serve all three dimensions tend to be strongest
4. Ideas that only serve functional jobs may be commoditized easily

### Dot Voting (Multi-Criteria)
1. Define 3-5 criteria (e.g., impact, feasibility, novelty, alignment, urgency)
2. Weight criteria if needed (user decides)
3. Score each idea 1-5 on each criterion
4. Calculate weighted totals
5. Present as ranked table:
   | Idea | Impact | Feasibility | Novelty | Alignment | Total |
6. Discuss surprises — does the ranking match intuition?

## Step 4: Challenge Top Candidates

For the top 2-3 ideas, optionally run a deeper challenge:
- Dispatch the idea-challenger agent for systematic stress-testing
- Or do a quick inline challenge: "Playing devil's advocate on Idea [X] — what could go wrong?"

## Step 5: Present Results

Clear, ranked output:
```
## Evaluation Results

### Recommended: [Idea Name]
**Why:** [2-3 sentences on why this won]
**Riskiest assumption:** [What to test first]
**Next step:** [Concrete action]

### Strong Alternative: [Idea Name]
**Why:** [What makes this worth considering]
**Trade-off vs recommended:** [What you gain/lose]

### Not Recommended (for now): [Ideas that didn't make the cut]
**Why:** [Brief reason for each]
```

## Step 6: Transition

Based on what the evaluated ideas are for:
- Software project → suggest design-sprint skill
- Business/product → suggest action plan or experiment design
- Content → suggest content strategy
- General → suggest next concrete steps

Ask: "Ready to move forward with [recommended idea]? If so, I can help with [appropriate next step]."
