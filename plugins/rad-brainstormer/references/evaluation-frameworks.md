# Idea Evaluation Frameworks

This reference covers all convergent and evaluation techniques used in the rad-brainstormer plugin. Each framework includes its full description, facilitation guidance, templates, and practical examples.

---

## 1. Impact/Effort Matrix

### Description

The Impact/Effort Matrix (also called the 2x2 Priority Matrix) is the simplest and most widely used evaluation framework. It plots ideas on two dimensions — the value they would create and the resources required to implement them — producing four clear quadrants that guide prioritization.

### How to Facilitate

1. List all ideas to be evaluated (typically 5-20 ideas works best)
2. Define what "impact" means for this specific context before scoring
3. Define what "effort" means for this specific context before scoring
4. Score each idea on both dimensions (1-5 scale)
5. Plot on the matrix
6. Discuss placement, especially ideas near quadrant boundaries
7. Prioritize based on quadrant

### The Four Quadrants

```
                    HIGH IMPACT
                         |
     Major Projects      |      Quick Wins
     (Plan & resource    |      (Do these first!)
      carefully)         |
                         |
  HIGH EFFORT -----------+----------- LOW EFFORT
                         |
     Hard Slogs          |      Fill-ins
     (Avoid or           |      (Do when you have
      reconsider)        |       spare capacity)
                         |
                    LOW IMPACT
```

**Quick Wins (High Impact, Low Effort)** — The obvious first priority. These deliver high value with minimal investment. Do these immediately. Examples: fixing a confusing button label, adding a missing FAQ entry, enabling an integration that already exists in the codebase.

**Major Projects (High Impact, High Effort)** — Worth doing but require planning, resources, and commitment. Schedule these into the roadmap. Examples: rebuilding the onboarding flow, launching in a new market, building a new core feature.

**Fill-ins (Low Impact, Low Effort)** — Nice-to-haves that don't cost much. Do them when there's spare capacity or when a team member needs a quick win. Examples: minor UI polish, documentation updates, small quality-of-life improvements.

**Hard Slogs (Low Impact, High Effort)** — The danger zone. These consume resources without proportional return. Avoid unless there's a compelling strategic reason. Examples: building a feature only 2% of users requested, supporting an obscure platform, over-engineering a low-traffic page.

### How to Score Impact

Consider these factors when rating impact (1-5):

- **Business value:** Revenue potential, cost savings, competitive advantage
- **User value:** How much does this improve the user's experience or solve their problem?
- **Strategic alignment:** Does this move toward long-term goals?
- **Reach:** How many users/customers does this affect?
- **Urgency:** Is there a time-sensitive opportunity or risk?

### How to Score Effort

Consider these factors when rating effort (1-5):

- **Time:** How long will this take to implement?
- **Complexity:** How technically or logistically challenging is this?
- **Dependencies:** Does this require other work to be done first?
- **Risk:** What's the probability of unexpected complications?
- **Resources:** Does this require skills, tools, or people we don't currently have?

### Presentation Template

```
## Prioritization Results

### Quick Wins (Do First)
- [ ] Idea X — Impact: 4, Effort: 1
- [ ] Idea Y — Impact: 5, Effort: 2

### Major Projects (Plan & Schedule)
- [ ] Idea Z — Impact: 5, Effort: 5
- [ ] Idea W — Impact: 4, Effort: 4

### Fill-ins (When Capacity Allows)
- [ ] Idea V — Impact: 2, Effort: 1

### Reconsidered (Low Priority)
- [ ] Idea U — Impact: 1, Effort: 4 (not worth the investment)
```

### Strengths

- Extremely fast and intuitive
- Creates clear, actionable priorities
- Visual format is easy to share with stakeholders
- Widely understood across organizations

### Limitations

- Ratings are subjective — different people may score differently
- "Impact" and "effort" can mean different things — always define them explicitly
- Doesn't account for dependencies between ideas
- Can oversimplify complex trade-offs
- Doesn't capture timing, strategic fit, or synergies between ideas

---

## 2. Assumption Mapping

### Description

Developed by David Bland and Alex Osterwalder (Strategyzer), Assumption Mapping identifies what needs to be true for an idea to succeed and then prioritizes which assumptions to test first based on their importance and the evidence behind them. It is the bridge between "we like this idea" and "we should build this."

### The Core Question

**"What needs to be true for this idea to work?"**

### The Four Assumption Categories

**Desirability Assumptions** — Will people want this?
- Does this problem actually exist for enough people?
- Will target users recognize this as a solution to their problem?
- Will they be willing to switch from their current approach?
- Do they value this enough to pay for it (or invest time/attention)?
- Will they recommend it to others?

**Feasibility Assumptions** — Can we build/deliver this?
- Do we have the technical capability?
- Do we have the right skills on the team?
- Can we source necessary materials, data, or partnerships?
- Can we build it within our timeline?
- Will it perform at the required scale?

**Viability Assumptions** — Should we build this (from a business perspective)?
- Is the market large enough?
- Can we acquire customers at a sustainable cost?
- Will the unit economics work?
- Does this fit our business model?
- Can we defend this position against competitors?

**Adaptability Assumptions** — Can we sustain this over time?
- Will regulatory changes affect this?
- How will competitors respond?
- Can this scale beyond the initial target?
- Will the underlying technology/platform remain stable?
- Is the team willing and able to maintain this long-term?

### The 2x2 Matrix

```
                    HIGH IMPORTANCE
                         |
   "Leap of Faith"       |     "Known Risks"
   (Test immediately!)   |     (Monitor closely)
   High importance,      |     High importance,
   low evidence          |     high evidence
                         |
  LOW EVIDENCE ----------+---------- HIGH EVIDENCE
                         |
   "Who Cares"           |     "Safe Bets"
   (Don't bother         |     (Proceed with
    testing)             |      confidence)
   Low importance,       |     Low importance,
   low evidence          |     high evidence
                         |
                    LOW IMPORTANCE
```

### Focus on the Leap of Faith Quadrant

Assumptions that are highly important but have little evidence are the riskiest. These are the ones that could kill the entire idea if they turn out to be wrong. Test these first, with the cheapest, fastest experiment possible.

### How to Design Experiments for Risky Assumptions

For each "Leap of Faith" assumption, ask:
1. What's the cheapest way to get evidence? (landing page, survey, prototype, conversation)
2. What's the minimum evidence that would make us confident? (N responses, conversion rate, qualitative feedback)
3. How long will this take? (hours, days, weeks)
4. What's the decision rule? ("If X happens, we proceed. If Y happens, we pivot.")

**Experiment types by cost (lowest to highest):**
- Desk research: search for existing data (minutes)
- Customer conversations: talk to 5 potential users (days)
- Landing page test: measure sign-up intent (days)
- Concierge test: deliver the service manually (weeks)
- Wizard of Oz: simulate the product with human backend (weeks)
- Prototype test: build a minimal version and observe usage (weeks)
- Pilot: launch to a small segment (months)

### Facilitation Process

1. Present the idea clearly
2. Ask: "What needs to be true for this to work?" Brainstorm assumptions freely
3. Categorize each assumption (desirability, feasibility, viability, adaptability)
4. Rate each on importance (1-5) and evidence level (1-5)
5. Plot on the matrix
6. For the top 3-5 "Leap of Faith" assumptions, design experiments
7. Prioritize experiments by speed and cost
8. Define decision rules: what results mean go, pivot, or stop

### Example Application

**Idea:** AI-powered meal planning app for families with food allergies.

**Assumptions mapped:**

| Assumption | Category | Importance | Evidence | Quadrant |
|---|---|---|---|---|
| Families with allergies struggle with meal planning | Desirability | 5 | 2 | Leap of Faith |
| They'd pay $10/month for a solution | Viability | 5 | 1 | Leap of Faith |
| We can build accurate allergy-safe recipe recommendations | Feasibility | 5 | 3 | Known Risk |
| Existing apps don't serve this niche well | Viability | 4 | 3 | Known Risk |
| Users will input their allergy info accurately | Feasibility | 3 | 4 | Safe Bet |
| Users want social features (share with other allergy families) | Desirability | 2 | 1 | Who Cares |

**Priority experiments:**
1. Interview 10 families with food allergies about their meal planning challenges (test assumption 1)
2. Create a landing page describing the app and measure sign-up rate at $10/month price point (test assumption 2)

### Strengths

- Systematic risk identification before committing resources
- Focuses scarce time and budget on the riskiest unknowns
- Creates a clear experimentation roadmap
- Prevents building on unvalidated foundations

### Limitations

- Requires honest self-assessment about what you don't know (teams often overestimate their evidence)
- Importance and evidence ratings are still subjective
- Can be uncomfortable for teams already emotionally invested in an idea
- Some assumptions are hard to test without actually building

---

## 3. Opportunity Solution Trees

### Description

Developed by Teresa Torres and published in "Continuous Discovery Habits" (2021), Opportunity Solution Trees provide a visual framework for connecting brainstormed solutions back to desired outcomes through user opportunities. The key insight: don't brainstorm in a vacuum — brainstorm in the context of a specific opportunity.

### The Four Tiers

```
Desired Outcome (measurable business/product goal)
├── Opportunity A (user need, pain point, or desire)
│   ├── Solution A1 → Experiment A1a
│   ├── Solution A2 → Experiment A2a
│   └── Solution A3 → Experiment A3a
├── Opportunity B (user need, pain point, or desire) ← TARGET
│   ├── Solution B1 → Experiment B1a
│   ├── Solution B2 → Experiment B2a
│   └── Solution B3 → Experiment B3a
└── Opportunity C (user need, pain point, or desire)
    ├── Solution C1 → Experiment C1a
    └── Solution C2 → Experiment C2a
```

**Tier 1: Desired Outcome** — A measurable business or product outcome. "Increase trial-to-paid conversion from 5% to 10%." This is the WHY.

**Tier 2: Opportunities** — User needs, pain points, or desires that, if addressed, would drive the outcome. These come from user research, not assumptions. "Trial users don't understand how the product applies to their specific use case."

**Tier 3: Solutions** — Specific ideas that address a particular opportunity. "Personalized onboarding flow based on user's industry." This is where brainstorming happens.

**Tier 4: Experiments** — The cheapest way to test whether a solution actually addresses the opportunity. "Show 50 trial users a mockup of the personalized flow and measure comprehension."

### The Key Rule

**"Focus on your target opportunity."**

Don't brainstorm solutions across your entire tree. Pick the most promising opportunity and brainstorm deeply for that one. This prevents scattered ideation and ensures solutions are grounded in real user needs.

### How to Build the Tree

1. Start with the desired outcome (product metric, business goal)
2. Research to identify opportunities: interview users, analyze behavior data, review support tickets
3. Map opportunities under the outcome
4. Prioritize: which opportunity, if addressed, would have the biggest impact on the outcome?
5. Select a target opportunity
6. Brainstorm at least 3 solutions for that opportunity (use SCAMPER, Crazy 8s, or Analogical Thinking)
7. For each solution, design the cheapest experiment
8. Run experiments, learn, iterate

### How to Identify Good Opportunities

Good opportunities are:
- Grounded in user research (not team assumptions)
- Specific enough to brainstorm against ("trial users don't understand the value" is better than "onboarding is bad")
- Connected to the desired outcome (addressing this should move the metric)
- Distinct from each other (not overlapping)

### When to Use

- Product discovery: connecting features to user needs and business outcomes
- Roadmap planning: deciding what to build next based on user opportunities
- Team alignment: creating shared understanding of why solutions are being pursued
- After a brainstorming session: organizing generated ideas into a structured framework

### Example Application

**Desired Outcome:** Reduce customer churn from 8% to 4% monthly.

**Opportunities (from user research):**
- A: Users forget about the product between sessions (20% log in less than once/month)
- B: Power features are hard to discover (support tickets about "hidden" features)
- C: Users don't see the impact on their KPIs (no reporting or ROI dashboard)
- D: Team adoption is low — one person uses it, rest of the team doesn't (single point of failure)

**Target Opportunity:** D — Team adoption is low.

**Solutions brainstormed:**
- D1: Team workspace with shared dashboards and collaborative features
- D2: "Invite your team" flow with role-based permissions and guided setup
- D3: Team activity feed showing what colleagues are doing in the product
- D4: Manager-facing ROI report that incentivizes broader rollout
- D5: Slack/Teams integration that brings product value into where teams already work

**Experiments:**
- D1: Mockup test with 10 existing team accounts
- D2: Track "invite" button clicks vs. completion rate
- D5: Build Slack bot MVP and measure daily active interaction

### Strengths

- Keeps solutions grounded in outcomes and user needs
- Prevents "build it because someone thought of it" syndrome
- Creates a clear, visual decision-making framework
- Supports iterative discovery

### Limitations

- Requires user research to populate opportunities (can't just make them up)
- Can be overly structured for early-stage, exploratory brainstorming
- Requires a clear, measurable desired outcome (not always available)
- Needs regular updating as you learn from experiments

---

## 4. Jobs-to-be-Done (JTBD)

### Description

Jobs-to-be-Done is a framework for understanding WHY people adopt products and services. Originated by Clayton Christensen (Harvard) and formalized by Tony Ulwick (Outcome-Driven Innovation). The core premise: people don't buy products — they hire them to do a job. Evaluating ideas through the JTBD lens ensures they serve real, functional, social, and emotional needs.

### The Three Job Dimensions

**Functional Job** — The practical task the user wants to accomplish.
- "Help me get from point A to point B."
- "Help me track my team's progress on a project."
- "Help me prepare a nutritious meal in under 30 minutes."

**Social Job** — How the user wants to be perceived by others.
- "Make me look competent to my manager."
- "Help me seem like a thoughtful gift-giver."
- "Signal that I care about sustainability."

**Emotional Job** — How the user wants to feel.
- "Give me confidence that I'm making the right financial decision."
- "Reduce my anxiety about missing deadlines."
- "Make me feel creative and in control."

### The Job Statement Format

"When [situation], I want to [motivation], so I can [expected outcome]."

Examples:
- "When I'm planning a team offsite, I want to find a venue that works for everyone, so I can create an experience the team remembers positively."
- "When I'm debugging production issues at 2am, I want to quickly identify the root cause, so I can fix it and go back to sleep."
- "When I'm presenting to investors, I want to show clear traction metrics, so I can secure the next round of funding."

### Outcome-Driven Innovation Process (Ulwick)

1. **Define the job:** What job is the user trying to get done?
2. **Create a job map:** Break the job into discrete steps (define, locate, prepare, confirm, execute, monitor, modify, conclude)
3. **Capture desired outcomes:** For each step, what does success look like? Format: "[Direction] the [measure] of [object of control] [context]"
   - "Minimize the time it takes to identify the root cause of a production issue"
   - "Increase the likelihood of choosing a venue that satisfies all attendees"
4. **Survey for importance and satisfaction:** Which outcomes are important but poorly served?
5. **Identify underserved outcomes:** High importance + low satisfaction = opportunity
6. **Brainstorm solutions targeting underserved outcomes**

### Interview Questions to Uncover Jobs

Use these in the research phase before brainstorming:

- "Tell me about the last time you [relevant activity]. Walk me through what happened, step by step."
- "What were you ultimately trying to accomplish?"
- "What triggered you to look for a solution? What changed?"
- "What alternatives did you consider? Why did you choose what you chose?"
- "What was frustrating or difficult about the process?"
- "If you could wave a magic wand, what would you change?"
- "When you finished, how did you know it was done? Were you satisfied?"
- "Who else was involved? What did they think?"

### Using JTBD as an Evaluation Lens

After brainstorming, evaluate each idea against the JTBD framework:

1. What functional job does this idea address? How well?
2. Does it also serve a social job? Which one?
3. Does it serve an emotional job? Which one?
4. Ideas that serve all three dimensions are typically strongest
5. Ideas that only serve the functional job may be commoditized
6. Ideas that miss the functional job entirely won't be adopted regardless of social/emotional appeal

### Example Application

**The Milkshake Story (Christensen's classic example):**

A fast-food chain wanted to sell more milkshakes. Traditional approach: survey customers about flavor, thickness, price. Result: incremental improvements, flat sales.

JTBD approach: observe who buys milkshakes and when. Discovery: 40% were bought before 8am by commuters driving alone. The job: "I have a long, boring commute and need something to keep me occupied and full until lunch." Competitors: not other milkshakes — but bagels, bananas, donuts, and boredom.

Solution: make the milkshake thicker (lasts longer through the commute), add interesting chunks (engagement), provide a drive-through loyalty card (convenience). Sales increased because the solution addressed the actual job.

### Strengths

- Deeply user-centered, prevents feature-driven thinking
- Reveals non-obvious competitors (you compete with anything that does the same job)
- Separates "what people say they want" from "what they actually hire products to do"
- Functional + social + emotional framework catches blind spots

### Limitations

- Requires genuine user research to identify jobs (guessing leads to generic insights)
- Functional jobs are easier to identify than social and emotional ones
- Can be time-consuming to do rigorously
- Risk of over-rationalizing user behavior (sometimes people just want a milkshake)

---

## 5. Pre-Mortem Analysis

### Description

Created by research psychologist Gary Klein in 1989 and published in Harvard Business Review as "Performing a Project Pre-Mortem." The Pre-Mortem inverts the usual optimism of planning by asking participants to imagine the idea has already failed — then explain why. This technique surfaces risks that optimism blindness, groupthink, and planning fallacy would otherwise hide.

Klein's research showed Pre-Mortems improve risk identification by approximately 30% compared to standard planning methods.

### The Core Premise

"It is 6 months from now. We implemented this idea, and it has failed spectacularly. What went wrong?"

By starting from the assumption of failure, participants are psychologically freed to voice concerns they would otherwise suppress (nobody wants to be the pessimist during an exciting planning session).

### Step-by-Step Process (Group Setting)

1. Clearly describe the idea/plan that has been selected
2. Set the scene: "Imagine we're 6 months into the future. This has completely failed. Not a little — catastrophically."
3. Each participant independently writes 2-3 reasons for the failure (5 minutes, no discussion)
4. Go around the room — each person shares one unique failure scenario
5. Continue until all scenarios are shared
6. Categorize the failure scenarios:
   - **Preventable vs. Unpreventable** — Can we do something about this?
   - **Likely vs. Unlikely** — How probable is this failure?
   - **Recoverable vs. Fatal** — If this happens, can we recover?
7. Focus on failures that are: likely, preventable, and potentially fatal
8. For each high-priority failure: brainstorm mitigation strategies
9. Update the plan to include mitigations
10. Decision: proceed (with mitigations), pivot the approach, or abandon the idea

### Adapted for 1-on-1 AI Sessions

Since you don't have multiple participants, the brainstormer plays the role of "diverse failure imaginer":

1. Present the idea clearly
2. AI generates 5-6 failure scenarios from different angles:
   - **Technical failure:** "The technology didn't work as expected because..."
   - **Market failure:** "Users didn't adopt it because..."
   - **Competitive failure:** "A competitor responded by..."
   - **Team/execution failure:** "The team couldn't deliver because..."
   - **Financial failure:** "The economics didn't work because..."
   - **Timing failure:** "The market wasn't ready because..." or "We were too late because..."
3. User reviews and adds their own failure scenarios (they know the domain better)
4. Together, rate each on likelihood (1-5) and severity (1-5)
5. Calculate risk score: likelihood x severity
6. Identify top 3 risks
7. Brainstorm mitigations for each

### Presentation Template

```
## Pre-Mortem Analysis: [Idea Name]

### Failure Scenarios

| # | Failure Scenario | Category | Likelihood (1-5) | Severity (1-5) | Risk Score |
|---|---|---|---|---|---|
| 1 | [Description] | Technical | 3 | 5 | 15 |
| 2 | [Description] | Market | 4 | 4 | 16 |
| 3 | [Description] | Competitive | 2 | 3 | 6 |

### Top Risks & Mitigations

**Risk 1: [Highest risk score]**
- Mitigation A: ...
- Mitigation B: ...
- Early warning signal: ...

**Risk 2: [Second highest]**
- Mitigation A: ...
- Mitigation B: ...
- Early warning signal: ...

### Decision
- [ ] Proceed with mitigations incorporated
- [ ] Pivot approach to address critical risks
- [ ] Abandon — risks are unacceptable
```

### Example Application

**Idea:** Launch a freemium version of a B2B analytics platform.

**Pre-Mortem failure scenarios:**
1. Free users overwhelm support (likelihood: 4, severity: 3, risk: 12) — Mitigation: self-serve knowledge base, community forum, no direct support for free tier
2. Free tier cannibalizes paid revenue (likelihood: 3, severity: 5, risk: 15) — Mitigation: restrict free tier features to personal use only, add team features only in paid
3. Competitors match with their own free tier within weeks (likelihood: 4, severity: 2, risk: 8) — Mitigation: differentiate on depth, not access
4. Infrastructure costs for free users exceed budget (likelihood: 3, severity: 4, risk: 12) — Mitigation: set usage limits, optimize for cost per user
5. Brand perception shifts from "premium" to "cheap" (likelihood: 2, severity: 4, risk: 8) — Mitigation: position free tier as "starter" not "free," maintain premium brand for paid tiers

**Decision:** Proceed with mitigations for risks 1, 2, and 4 built into the launch plan. Set a 90-day review checkpoint.

### Strengths

- Legitimizes pessimism and critical thinking
- Surfaces risks that optimism bias would hide
- Cheap and fast to run (30-60 minutes)
- Research-backed: 30% improvement in risk identification
- Creates actionable mitigations, not just worry

### Limitations

- Can kill team enthusiasm if not facilitated carefully — always frame as "making the idea stronger"
- May surface obvious risks that are already known (but sometimes obvious risks are the ones that get ignored)
- Quality depends on participants' ability to imagine diverse failure modes
- Doesn't quantify probability rigorously — gut estimates only

---

## 6. Dot Voting (Adapted for AI)

### Description

Dot Voting is a facilitation technique for democratically narrowing a large set of ideas. In traditional workshops, participants place dot stickers on their preferred ideas. Adapted for 1-on-1 AI sessions, it becomes a structured multi-criteria scoring exercise that creates transparent, comparable evaluations.

### How to Facilitate

**Step 1: Define Criteria**

Choose 3-5 evaluation criteria. Common options:
- **Impact:** How much value does this create for users or the business?
- **Feasibility:** How realistic is implementation given current resources?
- **Novelty:** How differentiated is this from existing solutions?
- **Alignment:** How well does this fit strategic goals or brand?
- **Speed:** How quickly could this be implemented?
- **Risk:** How likely is this to succeed? (inverse of risk)
- **Delight:** Would this genuinely excite or surprise users?

**Step 2: Weight Criteria (Optional)**

Not all criteria are equally important. Assign multipliers:
- Critical criteria: 2x or 3x weight
- Important criteria: 1.5x weight
- Nice-to-have criteria: 1x weight

Example: Impact (2x), Feasibility (1x), Novelty (1.5x), Alignment (1x)

**Step 3: Score Each Idea**

Rate each idea 1-5 on each criterion:
- 1 = Very low
- 2 = Low
- 3 = Moderate
- 4 = High
- 5 = Very high

**Step 4: Calculate and Rank**

Multiply scores by weights, sum across criteria, rank by total.

**Step 5: Discuss**

The most valuable part is not the ranking itself but the discussion it provokes:
- "Does this ranking feel right to you?"
- "Any ideas ranked lower than your gut tells you they should be?"
- "Any surprises in the results?"
- "The top 2 are very close in score — what would tip the balance?"

### Template

| Idea | Impact (2x) | Feasibility (1x) | Novelty (1.5x) | Alignment (1x) | Total |
|---|---|---|---|---|---|
| Idea A | 4 -> 8 | 3 -> 3 | 5 -> 7.5 | 4 -> 4 | 22.5 |
| Idea B | 5 -> 10 | 2 -> 2 | 3 -> 4.5 | 5 -> 5 | 21.5 |
| Idea C | 3 -> 6 | 5 -> 5 | 2 -> 3 | 3 -> 3 | 17 |
| Idea D | 4 -> 8 | 4 -> 4 | 4 -> 6 | 4 -> 4 | 22 |

**Ranking: A (22.5) > D (22) > B (21.5) > C (17)**

### Facilitation Tip

Have the user score ideas first, then share your own scores. Compare and discuss differences. The disagreements are where the most insight lives. "I scored Idea B higher on feasibility because [reason] — what am I missing?"

### Strengths

- Transparent and multi-dimensional
- Creates a shareable artifact that explains decisions
- Surfaces disagreements constructively
- Scales to any number of ideas

### Limitations

- Scores are still subjective — structured subjectivity, but subjective nonetheless
- Can give false precision (a difference of 0.5 points is not meaningful)
- Numbers should guide discussion, not replace judgment
- Criteria selection influences outcomes heavily — choose them carefully

---

## 7. SWOT Lens for Ideas

### Description

Applying the classic SWOT framework (Strengths, Weaknesses, Opportunities, Threats) to evaluate individual ideas or compare finalists. Unlike SWOT for businesses, this applies the lens to specific proposed solutions.

### How to Facilitate

For each finalist idea, fill out the four quadrants:

**Strengths** — What's inherently good about this idea?
- What advantages does it have?
- What does it do better than alternatives?
- What unique resources or capabilities does it leverage?
- Why would users choose this over competitors?

**Weaknesses** — What's inherently challenging about this idea?
- What would be difficult to execute?
- Where are the capability gaps?
- What are the known limitations?
- What would users complain about?

**Opportunities** — What external factors could make this even better?
- What trends support this direction?
- What partnerships could amplify impact?
- What adjacent markets could be captured?
- What technology developments enable new possibilities?

**Threats** — What external factors could undermine this?
- What competitive responses are likely?
- What regulatory changes could affect this?
- What market shifts could make this irrelevant?
- What dependencies could fail?

### Template

```
## SWOT Analysis: [Idea Name]

| Strengths | Weaknesses |
|---|---|
| - [Strength 1] | - [Weakness 1] |
| - [Strength 2] | - [Weakness 2] |
| - [Strength 3] | - [Weakness 3] |

| Opportunities | Threats |
|---|---|
| - [Opportunity 1] | - [Threat 1] |
| - [Opportunity 2] | - [Threat 2] |
| - [Opportunity 3] | - [Threat 3] |

**Net assessment:** [1-2 sentence summary]
**Key question to resolve:** [The most critical unknown]
```

### Comparison Use

When comparing 2-3 finalists, create a SWOT for each and compare side-by-side. Look for:
- Which idea has the most strengths aligned with your priorities?
- Which idea has the most manageable weaknesses?
- Which idea is best positioned for external opportunities?
- Which idea is most resilient against external threats?

### Strengths

- Quick and intuitive to complete
- Good for comparing 2-3 finalists side-by-side
- Captures both internal and external factors
- Widely understood framework

### Limitations

- Can be superficial if not probed deeply
- Internal vs. external distinction can be blurry for ideas (vs. businesses)
- Doesn't quantify or prioritize within quadrants
- Better for comparison than for go/no-go decisions

---

## Framework Selection Guide

Use this table to select the right evaluation approach for your situation.

| Situation | Best Framework | Why |
|---|---|---|
| Many ideas (10+), need quick filter | Impact/Effort Matrix | Fast, visual, creates clear quadrants for action |
| Few ideas (2-4), need deep validation | Assumption Mapping | Identifies riskiest unknowns and designs experiments |
| Product/feature ideas connected to metrics | Opportunity Solution Trees + JTBD | Keeps solutions grounded in outcomes and user needs |
| Risk assessment before committing | Pre-Mortem | Surfaces failure modes that optimism hides |
| Comparing 2-3 finalists | SWOT Lens or Dot Voting | Side-by-side comparison on multiple dimensions |
| Need stakeholder buy-in for a decision | Dot Voting | Transparent, multi-criteria scoring is easy to explain and defend |
| First-time evaluation (unsure what to use) | Impact/Effort Matrix first, then Pre-Mortem for top picks | Simple starting point, then deeper analysis where it matters |
| High-stakes decision (major investment) | Assumption Mapping + Pre-Mortem + JTBD | Multiple lenses for critical decisions — desirability, risk, and user fit |

### Combining Frameworks

Frameworks work best in sequence, not in isolation:

1. **Wide filter:** Impact/Effort Matrix to go from 15 ideas to 5
2. **User fit:** JTBD lens to check alignment with real user needs
3. **Risk check:** Pre-Mortem on top 2-3 ideas
4. **Validation plan:** Assumption Mapping for the selected idea
5. **Structured plan:** Opportunity Solution Tree to connect to outcomes and experiments
