# Business Report Writing Reference

## The Pyramid Principle (Barbara Minto)

### Core Concept
Start with the answer. Then provide the supporting arguments. Then provide the data behind each argument. The reader should be able to stop at any level and have a complete (if less detailed) understanding.

### Structure
```
Conclusion / Recommendation
├── Supporting Argument 1
│   ├── Data / Evidence 1a
│   └── Data / Evidence 1b
├── Supporting Argument 2
│   ├── Data / Evidence 2a
│   └── Data / Evidence 2b
└── Supporting Argument 3
    ├── Data / Evidence 3a
    └── Data / Evidence 3b
```

### MECE Principle for Supporting Arguments
Supporting arguments beneath the pyramid's conclusion should be **Mutually Exclusive and Collectively Exhaustive** (MECE). Mutually exclusive means no overlap between arguments — if two points say the same thing from different angles, merge them. Collectively exhaustive means the arguments together cover all the relevant ground — the reader shouldn't think "but what about...?" MECE prevents redundancy and gaps simultaneously.

### Applying the Pyramid
- **Do this**: "We should expand into the APAC market. Three factors support this: growing demand (15% YoY), favorable regulatory changes, and our existing customer pull-through from US enterprise accounts."
- **Not that**: "Let me walk you through the history of our international expansion efforts, the current market landscape, and then I'll share some thoughts on where we might consider going next."

### The SCQA Framework (within the Pyramid)
Use SCQA to structure the opening of any report:
- **Situation**: What is the current state? (Accepted fact, not controversial)
- **Complication**: What has changed or gone wrong? (The tension)
- **Question**: What do we need to decide or resolve? (Implied by the complication)
- **Answer**: Your recommendation or finding. (The top of the pyramid)

Example:
- **S**: "Our customer support team handles 2,400 tickets per week."
- **C**: "Ticket volume has grown 35% in the last quarter while headcount has stayed flat. Average response time has increased from 4 hours to 11 hours."
- **Q**: (Implied: How do we restore response times without proportionally increasing headcount?)
- **A**: "We recommend implementing a tiered triage system with AI-assisted categorization, which our analysis suggests will reduce average response time to 3 hours within 60 days at a cost of $45K."

---

## Executive Summary Craft

### What an Executive Summary Must Do
An executive summary is not an introduction. It is a *standalone document* that conveys the complete story for readers who will never read the full report.

### Structure
1. **Context** (1-2 sentences): Why this report exists. What triggered it.
2. **Key finding or recommendation** (1-2 sentences): The answer, not the question.
3. **Supporting evidence** (3-5 bullets): The critical data points or arguments.
4. **Implications** (1-2 sentences): What happens if we act. What happens if we don't.
5. **Next steps** (2-3 bullets): Who does what, by when.

### Executive Summary Formula (Condensed)
When time is extremely tight, use this sequence: **Problem/Opportunity** -> **Proposed Solution** -> **Key Insights/Proof** -> **Recommendations** -> **Value/ROI**. Each element gets one sentence or bullet. The entire summary should answer: "Why are we here, what should we do, and what's the payoff?"

### Executive Summary Mistakes
| Mistake | Example | Why it fails |
|---|---|---|
| Summary of the document structure | "Section 1 covers the market analysis. Section 2 presents our methodology..." | This is a table of contents, not a summary. |
| Burying the lead | "After extensive analysis of market conditions, competitive dynamics, and internal capabilities..." | The reader stops reading before reaching the conclusion. |
| Too long | 2-page executive summary for a 10-page report | If the summary is 20% of the report, it's not a summary. |
| No recommendation | "The data suggests several possible directions..." | Executives want a recommendation, not a menu. |
| Hedging everything | "It appears that there may be an opportunity to potentially..." | Commit to a position. Note risks in the body. |

### Length Guidelines
- For a 5-10 page report: Half a page.
- For a 20-50 page report: 1 page.
- For a 100+ page report: 1-2 pages max.
- Rule: If the executive summary exceeds 1 page, the writer hasn't done enough synthesis.

---

## Data Presentation

### When to Use Tables
- Comparing 3+ items across multiple dimensions.
- Presenting exact numbers that the reader may need to reference.
- Showing structured data with clear row/column relationships.
- **Do this**: A table comparing three vendors on price, features, support, and integration.
- **Not that**: A table with one row or one column — that's just a list.

### When to Use Prose
- Explaining trends, causation, or narrative relationships.
- When the data needs interpretation, not just presentation.
- When there are 1-2 data points that support an argument.
- **Do this**: "Revenue grew 23% YoY, driven primarily by enterprise expansion (up 41%) while SMB contracted 8%."
- **Not that**: A paragraph that reads like a table being narrated aloud: "Q1 revenue was $4.2M. Q2 revenue was $4.8M. Q3 revenue was $5.1M. Q4 revenue was $5.9M."

### When to Use Visualization
- Showing trends over time (line chart).
- Comparing proportions (bar chart, not pie chart — pie charts are almost always worse than bar charts).
- Showing distribution or correlation (scatter plot, histogram).
- When the *shape* of the data matters more than exact values.

### Action Titles for Data
Title charts and tables with the insight, not the category. "Q3 revenue missed targets due to pricing, not volume" tells the reader what to conclude. "Q3 Revenue Analysis" forces them to figure it out. Action titles turn every visual into an argument rather than a puzzle.

### The "What-So What-Now What" Framework
Apply to every data point and every chart: **What** (the fact or number), **So What** (why it matters or what it means), **Now What** (the action it implies). If you can't complete all three for a data point, it doesn't belong in the body of the report — move it to the appendix.

### Data Presentation Rules
- **Label everything**: Axis labels, units, time periods, data sources. If a chart can be misread, it will be.
- **Don't dual-axis**: Two Y-axes on one chart creates false visual correlations. Use two separate charts.
- **Start bar charts at zero**: Truncated axes exaggerate differences. If the difference is real, it'll show at zero.
- **Cite sources**: "Source: Internal analytics, Q3 2025" belongs on every chart and table.
- **Round appropriately**: "$4,237,891.23" implies false precision. "$4.2M" is what the reader needs.
- **Highlight the insight**: Bold the row that matters. Add a callout to the chart. Don't make the reader hunt for the point of the data.

---

## Recommendation Framing

### Strong Recommendation Structure
1. **State the recommendation clearly**: "We recommend X."
2. **Provide the rationale**: 2-3 key reasons, ordered by importance.
3. **Quantify the impact**: Expected outcomes in specific, measurable terms.
4. **Acknowledge risks and mitigations**: "The primary risk is Y. We mitigate this by Z."
5. **Define next steps**: Who does what, by when, at what cost.

### Explicit Trade-Off Framing
Acknowledging trade-offs builds credibility more than pretending they don't exist. State what you're gaining *and* what you're giving up: "We are trading near-term complexity for long-term cost structure" or "This approach sacrifices customization for speed-to-market." Readers trust writers who show they've weighed costs, not just benefits.

### Accountability in Language
Never use passive voice to evade responsibility. "A mistake was made" is a tell that the writer is hiding the actor. Write "Our team made a mistake" or "I made an error in the forecast." Passive-voice blame-avoidance erodes trust faster than the mistake itself.

### Recommendation Language

| Weak | Strong |
|---|---|
| "We suggest considering the possibility of..." | "We recommend..." |
| "It might be beneficial to explore..." | "We should pursue X because..." |
| "One option would be to..." | "The best option is X. Here's why." |
| "Going forward, we could potentially..." | "Next step: [team] implements [action] by [date]." |

### When Presenting Multiple Options
- Lead with your recommended option. Don't bury it as "Option C."
- Present no more than 3 options. More than 3 causes decision paralysis.
- Use a comparison matrix with consistent criteria.
- Make the criteria explicit: cost, timeline, risk, strategic alignment, resource requirements.
- Include a "do nothing" option with its consequences, if relevant. Sometimes the cost of inaction is the strongest argument for action.

---

## Report Structures

### Memo (1-3 pages)
**Use when**: Internal decision-making, proposing a specific action, summarizing a meeting or decision.

Structure:
```
TO: [Audience]
FROM: [Author]
DATE: [Date]
RE: [Specific subject — not vague]

RECOMMENDATION / KEY POINT (1-2 sentences)

BACKGROUND (2-3 sentences — only what the reader needs, not everything you know)

ANALYSIS (3-5 paragraphs or sections with supporting evidence)

NEXT STEPS (bulleted, with owners and deadlines)
```

### Report (5-30 pages)
**Use when**: Detailed analysis, quarterly reviews, project post-mortems, research findings.

Structure:
```
Executive Summary (0.5-1 page)
Introduction / Context (0.5 page)
Methodology (if applicable) (0.5-1 page)
Findings (bulk of the document, organized by theme or importance)
Analysis / Discussion (interpretation of findings)
Recommendations (prioritized, with rationale)
Appendix (raw data, supplementary charts, detailed methodology)
```

### Proposal (3-15 pages)
**Use when**: Seeking approval or funding for a project, partnership, or investment.

Structure:
```
Executive Summary (0.5 page)
Problem Statement (what's wrong, what's at stake)
Proposed Solution (what you want to do, how it works)
Scope and Timeline (what's included, what's not, key milestones)
Budget / Resource Requirements (specific numbers)
Expected Outcomes (measurable, time-bound)
Risks and Mitigations (honest assessment)
Next Steps / Ask (the specific decision you need)
```

### Amazon 6-Page Memo Format
Jeff Bezos replaced PowerPoint with narrative memos. The format:
1. **No bullet points** — full paragraphs force clearer thinking. If you can't write it as a complete sentence, you haven't thought it through.
2. **6 pages max** — forces prioritization. If it doesn't fit in 6 pages, you're including things that don't matter.
3. **Read silently at the start of the meeting** — the memo *is* the presentation. No pre-reads that nobody does.
4. **Structure**: Context -> Tenets (principles guiding the decision) -> Current state -> Proposed approach -> Key arguments and data -> FAQ (anticipated objections and responses).
5. **Appendix allowed** — supporting data, mockups, and detailed analysis go here but don't count toward the 6 pages.

The discipline of the 6-pager forces the author to synthesize and prioritize. If your first draft is 12 pages, you haven't identified what matters most.

---

## Corporate Jargon Blocklist

Replace these with specific, concrete language:

| Jargon | What to write instead |
|---|---|
| "Leverage" | Use, apply, build on |
| "Synergies" | Specific shared resources or combined effects |
| "Actionable insights" | Findings (then state the specific action) |
| "Move the needle" | Increase revenue by X%, reduce churn by Y% |
| "Circle back" | "We'll revisit this on [date]" |
| "Deep dive" | "Detailed analysis of [specific topic]" |
| "Low-hanging fruit" | "Quick wins" or better, name the specific wins |
| "Bandwidth" (for people) | Availability, capacity, time |
| "Best-in-class" | Compared to whom? By what measure? State it. |
| "Align" / "Alignment" | Agree, match, coordinate. Or be specific: "Marketing and Sales need to agree on lead scoring criteria." |
| "Stakeholders" | Name them. "The VP of Engineering and the CFO" is clearer than "key stakeholders." |
| "Paradigm shift" | Describe the actual change. |
| "Value-add" | What specific value? State it. |
| "Ecosystem" | Platform? Partner network? Supply chain? Be specific. |
| "Holistic approach" | Describe what you're actually including. |
| "Robust" | Strong? Reliable? Feature-rich? Each means something different. |
| "Scalable" | "Handles 10x current volume without infrastructure changes" |
| "End-to-end" | From [start point] to [end point] |
| "North star" | Primary goal, guiding metric |
| "Boil the ocean" | Scope too broadly, try to do everything at once |

### Zombie Nouns (Nominalizations)
Nominalization turns verbs into abstract nouns, burying the action and bloating sentences. These are the hallmarks of bureaucratic writing:

| Zombie noun | Revived verb |
|---|---|
| "conducted an investigation" | "investigated" |
| "make a provision for" | "provide" |
| "came to the realization" | "realized" |
| "performed an analysis of" | "analyzed" |
| "facilitated a discussion about" | "discussed" |
| "reached a conclusion that" | "concluded" |

**Test**: If you can put "the" or "a" in front of a verb's noun form and it appears in your writing, you've nominalized. Undo it.

### The Jargon Test
Read your report aloud. Every time you use a word that wouldn't appear in a conversation with a smart friend, replace it. If your smart friend would say "Wait, what do you mean by that?" you're using jargon as a substitute for specificity.

---

## Visual Hierarchy in Reports

### Page-Level Hierarchy
1. **Title**: Clear, specific, includes the date or reporting period.
2. **Executive summary / Key findings**: Visually distinct (boxed, shaded, or otherwise separated from the body).
3. **Section headings**: Consistent formatting, numbered if the document is longer than 10 pages.
4. **Subsection headings**: Smaller than section headings but clearly distinct from body text.
5. **Body text**: Consistent font, size, and spacing throughout.
6. **Callouts**: Key numbers, quotes, or findings pulled out and emphasized (bold, larger font, or boxed).
7. **Charts and tables**: Titled, sourced, and placed immediately after their first reference in text.
8. **Footnotes / Endnotes**: For caveats, methodological notes, and source details.

### Formatting Rules
- **One font family** throughout. Two at most (one for headings, one for body).
- **Page numbers** on every page. Header or footer with report title and date.
- **Consistent margins**: 1" on all sides minimum. Don't cram content to avoid a page break.
- **White space is structure**: Dense pages signal dense thinking — and not in a good way.
- **Charts titled as insights, not descriptions**: "Enterprise revenue grew 41% while SMB contracted" (not "Revenue by Segment, Q1-Q4 2025").

### Common Visual Hierarchy Mistakes
- Walls of text with no subheadings.
- Charts with no titles, no axis labels, or no source citations.
- Inconsistent formatting (some sections bolded, some not; varying heading sizes).
- Orphaned headings: a heading at the bottom of a page with the content on the next page.
- Decorative elements (clip art, unnecessary borders, excessive color) that distract from content.
- Using 5 colors when 2 would suffice. Every color should encode information, not decoration.

---

## Context-Gathering Questions

Before writing any business report, ask:
1. **Who is the primary audience?** Their role, what they already know, what decision they need to make.
2. **What is the single most important thing the reader should take away?** If they remember one thing, what should it be?
3. **What decision does this report support?** Every report should drive toward a decision or inform an action.
4. **What format is expected?** Memo, full report, presentation deck, 6-pager? Match the culture.
5. **What data is available?** What's confirmed, what's estimated, what's missing?
6. **What's the political landscape?** Are there competing proposals? Sensitive topics? Prior decisions this builds on?
7. **What's the deadline and distribution?** Who sees it, how is it shared, and when is it due?
8. **What happened last time?** Previous reports on this topic set expectations for format, depth, and approach.

---

## Quality Criteria for Business Report Review

- [ ] The executive summary stands alone — a reader who reads nothing else gets the full picture
- [ ] The recommendation or key finding appears in the first paragraph, not the last
- [ ] The Pyramid Principle is followed: conclusion first, then supporting arguments, then evidence
- [ ] Every data point is sourced, labeled, and presented in the most effective format (table, chart, or prose)
- [ ] Charts are titled as insights ("X grew 41%") not descriptions ("X by Quarter")
- [ ] Numbers are rounded appropriately and use consistent units
- [ ] Corporate jargon is replaced with specific, concrete language
- [ ] The report is the right format for the context (memo vs. report vs. proposal)
- [ ] Next steps include owners and deadlines
- [ ] Visual hierarchy is consistent: headings, spacing, formatting
- [ ] The report is no longer than it needs to be — every section earns its place
- [ ] Risks are acknowledged, not hidden. Mitigations are proposed, not hand-waved.

---

## AI Pattern Considerations

### Common AI Tells in Business Reports
- **Balanced to the point of uselessness**: "There are both advantages and disadvantages to this approach." Real analysts take positions. They say "We recommend X despite risk Y, because Z."
- **Filler introductions**: "In today's rapidly evolving business landscape, organizations face unprecedented challenges..." This is word count, not content. Start with the specific situation.
- **Generic SWOT analysis**: AI-generated SWOTs tend toward the obvious. "Strength: Strong brand. Weakness: Limited resources. Opportunity: Growing market. Threat: Competition." Each quadrant should contain *specific, non-obvious* insights.
- **Symmetric pros/cons lists**: AI tends to generate exactly as many cons as pros, each at similar length. Real analysis is asymmetric — sometimes there are 5 strong reasons for and 2 weak reasons against.
- **Fabricated specificity**: AI may generate plausible-sounding but fictitious statistics. "Studies show that 67% of companies..." Every number in a business report must be sourced and verifiable.
- **Consultant-speak density**: "We need to leverage our core competencies to drive synergistic value creation across the enterprise." This says nothing. Real recommendations are specific: "Engineering and Sales should co-own the API partner program, targeting 5 integrations by Q3."
- **Missing the "so what"**: AI presents data without interpretation. "Revenue was $4.2M in Q1 and $4.8M in Q2." So what? Is that good? Below target? Above the market? The "so what" is the point of the data.
- **Recommendation-free analysis**: AI reports often end with "further analysis is needed" instead of a concrete recommendation. If you have enough data to write a report, you have enough to make a recommendation (with appropriate caveats).

### Making AI-Assisted Reports Sound Human
- Verify every statistic. Replace any unverifiable number with either a real sourced number or remove it.
- Add the "so what" after every data point. What does this mean for the decision?
- Take a position. If the analysis supports option A over option B, say so clearly.
- Reference internal context that only someone in the organization would know: prior decisions, team dynamics, existing infrastructure.
- Vary sentence structure. AI reports tend toward uniform sentence length and construction.
- Include at least one honest caveat: "We're less confident about the Q4 projections because they depend on the partnership closing, which is not yet certain."
- Name specific people, teams, and systems rather than using generic categories.
- Cut every instance of "it is important to note that" — just note it.
