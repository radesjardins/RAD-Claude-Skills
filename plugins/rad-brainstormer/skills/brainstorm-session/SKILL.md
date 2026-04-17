---
name: brainstorm-session
description: >
  Let's brainstorm, I need ideas, help me think through, brainstorm with me, what
  should I build, how should I approach this — open-ended exploration of possibilities.
  Handles blank slate to refining an existing concept.
argument-hint: "[topic or problem]"
---

# Brainstorming Ideas Into Reality

The ultimate brainstorming partner. Help turn problems, ideas, and blank slates into fully formed designs through natural collaborative dialogue, proven ideation methodologies, and structured evaluation.

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have completed the brainstorming process and the user has approved the output. This applies regardless of perceived simplicity.
</HARD-GATE>

## Execution: parallel-first

This skill chains many phases with heavy sub-agent dispatch. To keep wall-clock time and context usage sane:

- **Context exploration** (Phase 1 state detection + Phase 1 file exploration + optional Phase 3 domain research) has no inter-step dependencies. Issue parallel Read/Glob/Grep calls, and if domain research is triggered, dispatch `domain-researcher` concurrently with the local file reads — do not serialize.
- **Phase 7 design presentation** reads existing files (codebase structure, related specs). Batch those reads.
- **Phase 11 spec review loop** — each iteration is a single `spec-reviewer` dispatch; iterations are inherently sequential, but any file reads the spec needs should be parallel within the iteration.
- **What to serialize, always:** the anti-anchoring question sequence in Phase 2 (user must respond before you offer ideas), and the divergent → convergent transition (mixing modes defeats the protocol).

Opus 4.7 and Sonnet 4.6 handle parallel batching well; Haiku 4.5 may prefer serial execution for reliability.

## Mode Flags

This skill honors two mode flags when passed in the invocation (`/rad-brainstormer:brainstorm-session --non-interactive`, etc.):

- `--non-interactive` — Skip all user-approval gates. Produce a best-effort output, commit the artifact, and emit a trailing JSON block listing `awaiting_user_review` items (e.g., unconfirmed scope, unvalidated top pick, unresolved spec-review escalations). For agent/CI callers that deadlock on interactive menus.
- `--resume <run-id>` — Load checkpoint state from `.brainstorm/state/<run-id>.json` and continue from the last saved phase. See "Checkpoint & Resume" below.

If neither flag is present, run interactively as documented.

## Checkpoint & Resume

Long brainstorms (domain research + full divergent/convergent + design + spec review) are compaction-prone. Save state to `.brainstorm/state/<run-id>.json` at these transitions:

1. After Phase 1 (starting state detected, context explored)
2. After Phase 3 (domain research complete, if dispatched)
3. End of Phase 5 (divergent phase complete — all ideas captured)
4. End of Phase 6 (convergent phase complete — finalists selected)
5. After Phase 10 (output document written)
6. After each successful Phase 11 spec-review iteration

Checkpoint schema:
```json
{
  "run_id": "string",
  "skill": "brainstorm-session",
  "phase": "1 | 3 | 5 | 6 | 10 | 11-iter-N",
  "started_at": "ISO-8601",
  "last_saved": "ISO-8601",
  "topic": "string",
  "starting_state": "blank_slate | vague_idea | clear_idea | improving_existing | needs_evaluation",
  "domain_brief": "JSON from domain-researcher or null",
  "ideas_generated": ["string"],
  "finalists": ["string"],
  "recommended": "string or null",
  "output_path": "string or null",
  "spec_review_history": [{"iteration": 1, "status": "issues_found", "issues": []}],
  "awaiting_user_review": ["string"]
}
```

On `--resume <run-id>`, load the file, announce the phase you're resuming from, and continue. Do not re-run completed phases.

## Anti-Pattern: "This Is Too Simple To Need Brainstorming"

Every topic goes through at minimum a light brainstorming process. A simple utility, a quick feature, a business question — all of them. "Simple" topics are where unexamined assumptions cause the most wasted work. The process can be short (a few exchanges for truly simple things), but MUST explore before committing.

## Checklist

Complete these steps in order:

1. **Detect starting state** — Where is the user? (blank slate / vague idea / clear idea / improving existing)
2. **Explore context** — Check project files, docs, recent commits (if software-related)
3. **Anti-anchoring check** — Draw out the user's existing thinking BEFORE offering yours
4. **Domain orientation** — Does this need domain research? If yes, dispatch domain-researcher agent
5. **Offer visual companion** (if topic involves visual decisions) — own message, not combined with questions
6. **Divergent ideation** — Select and apply appropriate techniques based on starting state
7. **Convergent evaluation** — Filter and prioritize using appropriate framework
8. **Propose 2-3 approaches** — With trade-offs and a recommendation
9. **Present design/output** — Scaled to domain (spec for software, strategy doc for business, etc.)
10. **Write output document** — Save to appropriate location, commit
11. **Spec review loop** (if software) — Dispatch spec-reviewer agent, fix issues, repeat until approved
12. **User reviews output** — Get explicit approval
13. **Transition** — Route to appropriate next step based on domain

## Process Flow

```
Detect Starting State
       │
       ▼
Explore Context ──► Anti-Anchoring: Draw out user ideas first
       │
       ▼
Domain Research Needed? ──yes──► Dispatch domain-researcher agent
       │ no                              │
       ▼                                 ▼
Visual Questions Ahead? ──yes──► Offer Visual Companion (own message)
       │ no                              │
       ▼◄───────────────────────────────┘
SELECT METHODOLOGY (based on starting state)
       │
       ▼
┌──────────────────────────────────────┐
│ DIVERGENT PHASE                      │
│ "We're in idea generation mode —     │
│  all ideas welcome, no filtering"    │
│                                      │
│ Apply selected techniques            │
│ Capture ALL ideas (user's + yours)   │
│ NO evaluation during this phase      │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│ CONVERGENT PHASE                     │
│ "Let's switch to evaluation mode"    │
│                                      │
│ Apply evaluation framework           │
│ Narrow to 2-3 top candidates         │
│ Optionally dispatch idea-challenger  │
└──────────────┬───────────────────────┘
               │
               ▼
Propose 2-3 Approaches (with trade-offs + recommendation)
               │
               ▼
Present Design/Output (section by section, get approval after each)
               │
               ▼
Write Output Document + Commit
               │
               ▼
Domain-Specific Routing:
  Software → spec review loop → writing-plans skill
  Business → business model canvas → action plan
  Content  → content strategy doc → editorial calendar
  Research → research plan → methodology outline
  General  → action plan with next steps
```

## Phase 1: Starting State Detection

Before asking a single question about the topic, determine WHERE the user is:

| Signal | Starting State | Approach |
|--------|---------------|----------|
| "I want to build something but don't know what" | Blank slate | Creative unblocking → Starbursting → HMW |
| "I have this vague idea about..." | Vague idea | Clarifying questions → SCAMPER → Reverse Brainstorm |
| "I want to build X but need to think through the design" | Clear idea | Six Thinking Hats → Morphological Analysis → Design |
| "I have X but want to make it better" | Improving existing | SCAMPER → 5 Whys → TRIZ (if technical) |
| "I have several ideas and need help choosing" | Needs evaluation | Jump to Convergent Phase |

If unclear, ask: "Where are you in your thinking? Are you starting from scratch, exploring a vague idea, or refining something specific?"

## Phase 2: Anti-Anchoring Protocol

**CRITICAL — Do this BEFORE offering any ideas.**

Research on human–AI ideation consistently shows that when AI suggests ideas first, humans anchor on them — producing fewer, less varied, less original ideas. The brainstormer must counteract this:

1. Ask: "Before I share any ideas, what have you been thinking so far? Even half-formed thoughts are valuable."
2. Ask: "What direction appeals to you intuitively, regardless of whether it seems feasible?"
3. Ask: "Is there anything you've already ruled out? Why?"
4. Capture and acknowledge ALL user ideas before adding yours
5. When offering ideas, frame them as building on the user's: "Building on your idea about X, what if we also..."

## Phase 3: Domain Orientation

Assess whether domain research would improve the brainstorming:

- **Research needed**: The topic involves an industry, market, or technical domain where current context matters
- **Research not needed**: Personal/creative topics, well-understood domains, or user is the domain expert
- **Ask if unsure**: "I want to make sure I'm well-informed about [domain]. Want me to do some quick research before we dive in?"

If research is needed, dispatch the `domain-researcher` agent directly (it is defined in this plugin with `model: opus`, JSON-first output):

```
Agent tool:
  subagent_type: domain-researcher
  description: "Research [domain] for brainstorming"
  prompt: <substitute references/subagent-prompts/domain-research.md with {topic} and {session_context}>
```

Parse the JSON response (markdown fallback accepted — see the agent's output contract). Weave the brief into questions naturally — do not dump a research report on the user. If the brief contains items in its `surprises` field, flag them prominently before continuing.

## Phase 4: Methodology Selection

Reference `references/methodology-catalog.md` for detailed technique instructions.

### For Blank Slate:
1. Run a warm-up exercise (from `references/creative-unblocking.md`)
2. **Starbursting** — Generate questions about the problem space
3. **How Might We** — Reframe the best questions as opportunity statements
4. **Crazy 8s** (adapted) — Rapid-fire idea generation on the best HMW questions
5. → Convergent phase

### For Vague Idea:
1. Clarifying questions to understand the kernel of the idea
2. **SCAMPER** — Systematically explore modifications and variations
3. **Reverse Brainstorming** — "How could we make this fail?" then invert
4. **Analogical Thinking** — "How would [company/domain] approach this?"
5. → Convergent phase

### For Clear Idea Needing Design:
1. **Six Thinking Hats** — Explore from all perspectives
2. **Morphological Analysis** — Break into dimensions, combine options
3. → Convergent phase (lighter, since idea is already focused)

### For Improving Existing:
1. **SCAMPER** — What can be substituted, combined, adapted, modified, eliminated, reversed?
2. **5 Whys** — What's the root cause of what needs improving?
3. **TRIZ** (if technical contradiction exists) — Systematic inventive problem solving
4. → Convergent phase

### For Already Has Ideas:
1. Skip divergent phase (or brief expansion with analogical thinking)
2. → Jump directly to convergent phase

## Phase 5: Divergent Phase Discipline

During ideation:
- **Announce the mode**: "We're in idea generation mode — all ideas are welcome, no filtering yet."
- **Never evaluate during generation**: If the user says "that won't work," redirect: "Good concern — let's capture that for evaluation. What else comes to mind?"
- **Build, don't redirect**: Use "Yes, and..." to build on user ideas
- **Capture everything**: Keep a running list of all ideas generated
- **Know when to stop**: When ideas start repeating or becoming incremental, it's time to converge

## Phase 6: Convergent Phase

Reference `references/evaluation-frameworks.md` for detailed framework instructions.

1. Present the complete idea list: "We've generated [N] ideas. Let's evaluate them."
2. Select appropriate framework based on situation
3. Walk through evaluation with the user
4. Optionally dispatch idea-challenger agent for top candidates
5. Narrow to 2-3 finalist approaches

## Phase 7: Design & Output

Adapt the output format to the domain:

### Software Projects
- Present design section by section, get approval after each (in `--non-interactive` mode, skip approvals and mark unconfirmed sections in `awaiting_user_review`)
- Cover: architecture, components, data flow, error handling, testing
- Write spec to `docs/plans/YYYY-MM-DD-<topic>-design.md` (user preferences override)
- Run `spec-reviewer` agent (max 5 iterations — see escalation below)
- User reviews spec
- Transition: hand off to `/rad-planner:plan-project` for implementation planning. If `rad-planner` is not installed, surface this to the user and suggest installing it.

#### Spec Review Loop (Phase 11)

Dispatch `spec-reviewer` with the substituted `references/subagent-prompts/spec-review.md` template, passing the current `iteration` and `max_iterations` (default 5) and any prior iteration's `blocking_issues`. Parse the JSON response:

- `status: approved` → proceed to user review
- `status: issues_found` and `iteration < max_iterations` → fix blocking issues, increment iteration, re-dispatch
- `escalation_required: true` (or `iteration >= max_iterations` with issues remaining) → stop looping. Surface the `unresolved_issues` JSON to the user with: "Spec review hit iteration cap with unresolved issues. Please decide: (a) accept these as known gaps, (b) rewrite the affected sections yourself, or (c) drop back to design phase." In `--non-interactive` mode, commit the current spec and add the unresolved issues to `awaiting_user_review`.

### Business/Strategy
- Present as a strategic brief
- Cover: value proposition, target audience, competitive positioning, key risks, next steps
- Write to `docs/brainstorm/YYYY-MM-DD-<topic>-strategy.md`
- Transition: action plan with concrete next steps

### Product Discovery
- Present as Opportunity Solution Tree or lean canvas
- Cover: target outcome, opportunities, solution candidates, experiments to run
- Write to `docs/brainstorm/YYYY-MM-DD-<topic>-discovery.md`
- Transition: experiment plan

### Content/Marketing
- Present as content strategy
- Cover: audience, topics, channels, differentiation, content calendar
- Write to `docs/brainstorm/YYYY-MM-DD-<topic>-content.md`
- Transition: editorial plan

### General Problem-Solving
- Present as action plan
- Cover: root cause, solution approach, steps, risks, success criteria
- Write to `docs/brainstorm/YYYY-MM-DD-<topic>-plan.md`
- Transition: next steps with owners and timelines

## Visual Companion

A browser-based companion for showing mockups, diagrams, and visual options. Available as a tool — not a mode.

**Offering**: When upcoming questions involve visual content, offer once:
> "Some of what we're working on might be easier to explain if I can show it in a browser. I can put together mockups, diagrams, and comparisons as we go. Want to try it?"

**This offer MUST be its own message.** Don't combine with questions.

**Per-question decision**: Even after acceptance, decide FOR EACH QUESTION whether to use browser or terminal.
- **Browser**: mockups, wireframes, layout comparisons, architecture diagrams, side-by-side designs
- **Terminal**: requirements questions, conceptual choices, tradeoff lists, scope decisions

If accepted, read the visual companion guide:
`scripts/` directory contains the visual companion server (start-server.sh, stop-server.sh, frame-template.html, helper.js, server.js)

## Key Principles

- **One question at a time** — Don't overwhelm with multiple questions
- **Multiple choice preferred** — Lower cognitive load than open-ended when possible
- **Anti-anchoring always** — User ideas first, yours second
- **Phase discipline** — Never mix divergent and convergent modes
- **YAGNI ruthlessly** — Remove unnecessary complexity from all outputs
- **Explore alternatives** — Always generate multiple options before settling
- **Incremental validation** — Present output in sections, get approval before moving on
- **Be flexible** — Go back and re-explore when something doesn't make sense
- **Adapt to energy** — If user is stuck, switch techniques. If flowing, stay out of the way.
- **Domain-aware** — Research when needed, adapt output to domain

## Working in Existing Codebases (Software)

- Explore current structure before proposing changes. Follow existing patterns.
- Where existing code has problems that affect the work, include targeted improvements as part of the design.
- Don't propose unrelated refactoring. Stay focused on the goal.

## Large Project Decomposition

Before asking detailed questions, assess scope. If the request describes multiple independent subsystems:
1. Flag it immediately
2. Help decompose into sub-projects: independent pieces, relationships, build order
3. Brainstorm the first sub-project through the normal flow
4. Each sub-project gets its own brainstorm → spec → plan cycle
