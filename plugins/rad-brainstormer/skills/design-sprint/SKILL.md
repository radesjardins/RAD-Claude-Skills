---
name: design-sprint
description: >
  This skill should be used when the user says "design this", "create a spec",
  "design sprint", "architecture for this", "write a design doc", or has already
  chosen a software direction and needs a complete design specification. Use when
  the user has moved past ideation and needs architecture, components, data flow,
  error handling, and testing planned out. Not for ideation — use brainstorm-session
  for that.
---

# Software Design Sprint

Turn a chosen software approach into a complete, reviewable design spec ready for implementation planning.

**Prerequisite:** The user has already decided WHAT to build (either through brainstorm-session or by coming in with a clear idea). This skill handles HOW to design it.

<HARD-GATE>
Do NOT write any code, scaffold any project, or invoke any implementation tool until the design is approved by the user. This is a DESIGN skill, not an implementation skill.
</HARD-GATE>

## Checklist

Complete these steps in order:

1. **Explore project context** — Check files, docs, recent commits
2. **Confirm scope** — Verify the chosen approach with the user. If they haven't chosen, route them back to brainstorm-session.
3. **Offer visual companion** (if UI work involved) — own message only
4. **Ask clarifying questions** — One at a time, focused on technical design decisions
5. **Design for isolation** — Break into units with clear boundaries and interfaces
6. **Present design sections** — One section at a time, get approval after each:
   - Architecture overview
   - Component breakdown
   - Data model / flow
   - API design (if applicable)
   - Error handling strategy
   - Testing strategy
   - Migration / deployment considerations (if applicable)
7. **Write design doc** — Save to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` (user preferences override)
8. **Spec review loop** — Dispatch spec-reviewer agent; fix issues and re-dispatch until approved (max 5 iterations)
9. **User reviews spec** — "Spec written and committed. Please review and let me know about any changes."
10. **Transition** — Invoke the writing-plans skill

## Design Principles

### Design for Isolation and Clarity
- Break the system into smaller units that each have one clear purpose
- Units communicate through well-defined interfaces
- Each unit can be understood and tested independently
- Ask for each unit: what does it do, how do you use it, what does it depend on?
- Can someone understand what a unit does without reading its internals?
- Can you change internals without breaking consumers?
- When a file grows large, that's a signal it's doing too much

### Follow Existing Patterns
- Explore the current codebase structure before proposing changes
- Follow existing conventions (naming, file organization, testing patterns)
- Where existing code has problems that affect the work, include targeted improvements
- Don't propose unrelated refactoring

### YAGNI
- Remove unnecessary features from all designs
- Don't add configurability that hasn't been requested
- Don't design for hypothetical future requirements
- The right amount of complexity is the minimum needed for the current task

## Asking Questions

- One question per message
- Prefer multiple choice when the options are known
- Focus on decisions that affect the design (not implementation details)
- If a topic needs more exploration, break it into multiple questions

## Presenting the Design

- Scale each section to its complexity: a few sentences if straightforward, up to 200-300 words if nuanced
- Ask after each section whether it looks right
- Be ready to go back and revise if something doesn't make sense

## After the Design

### Write the spec document
- Save to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
- Use clear, concise language

### Spec Review Loop
1. Dispatch spec-reviewer agent
2. If issues found: fix, re-dispatch, repeat until approved
3. If loop exceeds 5 iterations, surface to human for guidance

### User Review Gate
> "Spec written and committed to `<path>`. Please review it and let me know if you want to make any changes before we start the implementation plan."

Wait for user response. If changes requested, make them and re-run spec review.

### Transition
Invoke the writing-plans skill to create an implementation plan.
The ONLY skill invoked after design-sprint is writing-plans. Do NOT invoke frontend-design, mcp-builder, or any other implementation skill.

## Visual Companion

For questions that involve visual decisions (UI layouts, architecture diagrams), use the visual companion:
- Read the guide at `scripts/` directory for the server infrastructure
- Decide per-question whether browser or terminal is better
- Use browser for: mockups, wireframes, layouts, diagrams
- Use terminal for: technical decisions, tradeoffs, scope questions
