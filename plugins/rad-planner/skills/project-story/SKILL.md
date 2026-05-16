---
name: project-story
description: >
  This skill should be used when the user says "write me a project story", "summarize the project",
  "draft a state-of-the-project narrative", "explain where this project is", "what's the state of
  this project", "draft an onboarding brief", "give me a project update", "create a project story",
  "tell me the project story", "write a plain-English project summary", "narrate the project",
  or wants a plain-language narrative summary of a project synthesized from the canonical doc set
  (vision.md, decisions/, planning/current.md, status.md, roadmap.md). Output is prose for a human
  reader, not a planning artifact — for onboarding a collaborator, explaining the project to a
  non-developer, sending an investor / stakeholder update, or catching your own future-self up
  after time away.
argument-hint: "[--output <path>] [--audience non-dev|investor|future-self|new-collaborator]"
user-invocable: true
allowed-tools: Read Glob Bash Write Edit
---

# Project Story — Plain-language synthesis from canonical doc set

You are synthesizing a plain-language narrative of the project's current state from rad-planner's canonical doc set. The deliverable is **prose for a human reader**, not a planning artifact. The reader is someone who needs to understand the project — a non-developer stakeholder, a new collaborator joining the team, a funder, the user's own future-self after time away, or an investor.

## What this skill is — and what it isn't

**This skill produces:**
- A plain-English narrative summarizing what the project is, what it isn't, where it is, what's pending, and the bottom line
- Output as a single Markdown file (no front-matter, no YAML, just prose with section headings)
- Structure validated against a real use case (Faunero PROJECT-STORY.md, 2026-05-15)

**This skill does NOT:**
- Generate planning artifacts (those are `/plan`'s job)
- Validate or modify the canonical doc set (those are validators / `/plan --improve`'s job)
- Make claims not backed by source (every section is grounded in a canonical doc)
- Use marketing language, superlatives, or sensational framing (the principle is honest synthesis)

## Input — the canonical doc set

Read the following from `docs/` (skip gracefully if absent — note what's missing at the end):

| Doc | Used for |
|---|---|
| `docs/vision.md` | One-line product test, target users, product principles, non-goals, success signals |
| `docs/architecture.md` | Technical shape, deployment, what the user actually sees |
| `docs/planning/current.md` | Active milestone, acceptance criteria, pending work, scope |
| `docs/status.md` | Where work actually stands, recent decisions during execution, blockers |
| `docs/decisions/*.md` | Locked architectural / product decisions, lineage |
| `docs/roadmap.md` (optional) | Now / Next / Later / Parked, tier commitments |

If `docs/` doesn't exist or all canonical files are missing, ask the user where the project state lives before proceeding. Don't invent sources.

## Output — the narrative format

The structure follows the validated Faunero format. **Adapt to what the project actually has** — not every section applies to every project. Omit sections that have no canonical-doc backing rather than fabricating content.

### Section order (full shape)

1. **Title + date + temporary-or-permanent marker** — e.g., "# The {Project} Story — what we're building and where we are\n\n*A plain-language summary of what's been decided, what's still ahead, and when actual coding starts. Written {YYYY-MM-DD}. {Temporary — move out of repo when no longer useful | Living document — refresh via /refresh-story}.*"
2. **One-line product test** — H2 "What {Project} is, in one line". The one-liner from `vision.md`'s product statement, plus a sentence about *why this boundary matters*: "That sentence is the test for every feature."
3. **Product shape** — H2 (depends on project) — e.g., "Two phases, one product" for products with distinct user-flows; "One tool, three modes" for tools; skip if no natural structure.
4. **Who it's for (in build order)** — H2 "Who it's for (in build order)". Target users from `vision.md`. List in priority order, with the first anchor user named. Add entry-points / starting-shapes if `vision.md` enumerates them.
5. **What {Project} is explicitly NOT** — H2 "What {Project} is explicitly NOT". From `vision.md` non-goals. Frame as a bulleted list with brief explanations. Include the redirect principle: "When a user asks {Project} to do something out-of-scope, the system [says no and redirects | does X]."
6. **How the money works** (if applicable) — H2 from `roadmap.md` tier commitments or `vision.md` business model. Skip if no commercial dimension.
7. **Why we paused / what we decided** (if applicable) — H2. For projects that had a deliberate planning phase, narrate the decision discipline. From `decisions/` lineage + any "lessons-learned" docs.
8. **What we decided (the simple list)** — H2. High-signal one-liners from `decisions/*.md`. Group by category (vision, architecture, economics, etc.). Map to decision-record IDs in parentheses.
9. **Where we are right now** — H2. From `status.md`. Three sub-points: (a) what's complete and locked, (b) what's actively underway, (c) what's pending before the next milestone.
10. **What's next (before code | before beta | before ship)** — H2. From `planning/current.md` acceptance criteria + `roadmap.md` "Next". Be honest about what's substantial work vs what's a small step.
11. **What the user will actually see when it ships** (if applicable) — H2. From `architecture.md` user flow + `vision.md` success signals. A step-by-step walkthrough of the experience. Skip if too early for this.
12. **What's not done yet (the honest list)** — H2. Bulleted list of substantive pending work. No glossing. From `planning/current.md` open items + `roadmap.md` Later.
13. **What changed by doing all this** (if applicable) — H2. For projects that went through a deliberate planning reset, name what's different now vs before. From decisions/lessons-learned.
14. **The bottom line** — H2. Two-sentence wrap. State of the project + what's true now that wasn't before.

### Rendering rules

- **Plain English.** No jargon unless `vision.md` itself uses it. No acronyms without expansion the first time.
- **No marketing language.** Avoid "revolutionary", "the only", "world-class", "best-in-class". Concrete claims only.
- **Grounded in source.** Every substantive claim should be traceable to a canonical doc. If you find yourself wanting to write something that's NOT in the source, surface that as a gap to the user rather than inventing it.
- **Honest about uncertainty.** "We think X" / "We're not sure about Y" is fine. Don't paper over open questions.
- **Voice: knowledgeable narrator.** Not breathless, not corporate. Match the voice of `vision.md` itself.
- **Length proportional to project complexity.** A small project's story is ~80-150 lines. A complex multi-phase product like the validated Faunero example is ~250 lines. Don't pad.

## Workflow

### Step 1: Confirm output target

Ask the user where to write the story. Offer two defaults:

```
Where should I write the project story?

  1. PROJECT-STORY.md at repo root (temporary, for shares; gitignore by default)
  2. docs/story.md (in-repo persistence; refreshed via /refresh-story)
  3. Custom path (specify)
```

If user passed `--output <path>`, skip the prompt and use that path.

### Step 2: Read canonical doc set

In parallel:

- `docs/vision.md`
- `docs/architecture.md`
- `docs/planning/current.md`
- `docs/status.md`
- `docs/decisions/*.md` (glob)
- `docs/roadmap.md` (if present)
- `docs/lessons-learned.md` (if present)
- `AGENTS.md` or `CLAUDE.md` (for project framing — secondary source)

Note which canonical files are absent. If `vision.md` AND `status.md` are both absent, this skill can't proceed meaningfully — ask the user where the project state lives.

### Step 3: Determine audience and adapt

If `--audience` was passed, use it. Otherwise infer or ask. Audience affects:

- **non-dev**: Plain English bias high. Skip technical architecture detail. Focus on what/why/who.
- **investor**: Add success-signal language, market framing. From `vision.md` success signals + `roadmap.md` if commercial.
- **future-self**: Bias toward what you-3-months-from-now will need to remember. Heavy on decisions + open questions.
- **new-collaborator**: Bias toward context — what's locked, what's still being decided, where to start reading.

If no audience inferred, default to non-dev (most general).

### Step 4: Synthesize section by section

For each section in the structure above:

1. Pull source content from canonical docs
2. Synthesize into plain-English prose
3. Apply the rendering rules
4. Cross-check: does every claim have a source? Flag any orphan claims back to the user before writing.

Skip sections without canonical backing (don't fabricate them).

### Step 5: Write the file

Write to the chosen path. Single Markdown file. No frontmatter.

### Step 6: Surface gaps

After writing, surface any gaps or notes to the user:

- Canonical docs that were missing (and what content was inferred or skipped as a result)
- Sections that were skipped (with reason)
- Claims that needed user judgment (if any)
- Suggestion to refresh via `/refresh-story` when canonical docs evolve

## Cross-plugin notes

- This skill reads `docs/` written by rad-planner's `/plan` workflow. It does not write to those docs.
- For non-rad-planner-shaped projects (no canonical `docs/` structure), `narrate-project` in the future `rad-explain` plugin handles that case more flexibly.
- Pairs with `/refresh-story` for ongoing maintenance.

## Output contract

- Single Markdown file at user-specified path
- No front-matter
- Section headings as specified
- Plain English throughout
- All claims traceable to canonical source
- Footer: "*Generated by /rad-planner:project-story from canonical doc set on {YYYY-MM-DD}. Refresh via /rad-planner:refresh-story.*"

## When you finish

Surface a 3-5 line summary:

```
Project story written to {path}.

Sources used: vision.md, architecture.md, planning/current.md, status.md, {N} decision records.
Sections included: {list}.
Sections skipped: {list with reason if applicable}.

Refresh via /rad-planner:refresh-story when canonical docs evolve.
```
