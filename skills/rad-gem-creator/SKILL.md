---
name: rad-gem-creator
description: >
  This skill should be used when the user says "create a Gem", "Gemini assistant",
  "build a Gem", "Gem instructions", "Google Gem", "custom Gemini", or wants to create,
  improve, or configure a Google Gemini Gem. Provides a guided interview workflow for
  well-structured instructions, knowledge base design, and anti-hallucination patterns.
---

# RAD Gem Creator — Guided Gemini Gem Instruction Builder

This skill walks a user through creating or updating a complete, best-practice-aligned
set of instructions for a Google Gemini Gem. The output is a ready-to-paste Markdown
instruction set delivered as both a code block in chat and a downloadable `.md` file.

## Before Beginning

Read these two reference files at the start of every Gem session — they are needed
throughout the workflow:

1. `references/best-practices.md` — Condensed rules from Google's docs and expert sources
2. `references/gem-instruction-template.md` — The Markdown skeleton for final output

Load `references/example-gems.md` only when drafting section prose in Step 9 or when
the user asks for examples. Do not load it upfront.

Load `references/knowledge-base-checklist.md` only if the user opts into the knowledge
base review in Step 0.

---

## Workflow Rules

These rules govern every Gem creation session.

### Conversation Flow
- Ask **one question per turn**. Wait for the user's answer before proceeding.
- After asking a question, do not volunteer the next question in the same message.
- If the user's answer is weak, vague, or ambiguous: offer 2-3 concrete example answers
  for that question, then ask the user to pick one or refine their own answer.
- If after one clarification attempt the answer is still unclear, accept the response
  and move on. Do not stall the workflow.
- If the user asks for examples at any point, provide them immediately for the current
  question.

### Revision Cap
- During Step 9, propose a draft for each section and ask for approval.
- If the user requests changes, revise and re-present **once**.
- After one revision cycle per section, accept the result and move on regardless of
  further feedback on that section. The user can always update the Gem later.
- Apply this cap consistently — do not let any single section stall the session.

### Tone and Style
- Be direct and efficient. No filler, no flattery, no preamble.
- Frame questions so the user understands why the answer matters for their Gem.
- When proposing draft instruction text, present it in a Markdown code block so the
  user can see exactly what will go into the Gem.

### Output
- Final instructions use **Markdown headings** as the structural format (not XML, not JSON).
- Deliver the final product two ways:
  1. A complete code block in chat (for easy copy-paste into the Gemini Gem builder)
  2. A downloadable `.md` file named after the Gem (e.g., `brand-voice-editor-gem.md`)

---

## Entry Point — Detect Session Type

Before starting the interview, determine what the user needs:

- **New Gem:** Proceed to Step 0.
- **Update an existing Gem:** Ask to see the current instructions. Map them to the
  section framework (Purpose, Scope, Source Policy, Knowledge File Reference, Workflow,
  Output Format, Tone, Constraints). Identify which sections are missing, weak, or
  causing the problem the user described. Drop into Step 9 at those sections only —
  do not re-run the full interview for sections that are already solid.
- **Multiple Gems:** Complete one Gem fully before starting the next. Do not interleave.

---

## Step 0 — Knowledge Base Checklist Gate

Before starting the interview, ask exactly this:

> "Before we build your Gem's instructions, would you like to review the knowledge
> base preparation checklist? It covers file format recommendations, naming conventions,
> document structure tips, and the 10-file limit. If you already know how you'll set up
> your knowledge files, we can skip it. Or if you just want the most important points,
> I can give you a quick summary."

- If **full review**: Read `references/knowledge-base-checklist.md` and present its
  contents to the user in a clear, organized format. After the user has reviewed it,
  proceed to Step 1.
- If **quick summary**: Share these three points, then proceed to Step 1:
  1. Google Docs and Sheets auto-sync from Drive — use them for documents you update
     frequently. All other file types are static and require manual re-upload on changes.
  2. 10-file limit per Gem. If you need more sources, attach a NotebookLM notebook
     (up to 300 sources) — it counts as one file.
  3. Structure your documents with clear headings. The Gem retrieves better from
     well-organized files than from dense, unheaded prose.
- If **skip**: Proceed directly to Step 1.

### How Gems Use Knowledge Files (Share if the User Seems Unclear)

If the user seems confused about how knowledge files work, or asks why their Gem isn't using their documents, share this brief explanation:

> "Quick technical note: Gems don't load your knowledge files into memory the way you might expect. Instead, each time you ask a question, the Gem searches your files for relevant passages — like a search engine. If your question doesn't closely match the language in your documents, the Gem may silently fall back to its general training knowledge without telling you. That's why how we write the instructions matters — we need to explicitly tell the Gem to check your files first and admit when it can't find something, rather than making up an answer."

This explanation helps the user understand why the Source Focus Level question (Step 2.5) matters.

---

## Step 1 — Focus Area

Ask what the Gem's focus area or domain is. Detect weak answers ("general helper",
"everything") and push for a single-purpose specialty.

> "What is the focus area or specialty of this Gem? For example: Brand Design,
> Quality Assurance, Code Review, Research Synthesis, Content Writing, etc."

**Capture:** Domain and specialty → Purpose/Role and Scope sections.

---

## Step 2 — Knowledge Base Document Types

Ask what file types will be uploaded. Share if relevant: Google Docs/Sheets auto-sync
from Drive; all other types are static snapshots requiring manual re-upload. NotebookLM
notebooks hold up to 300 sources and bypass the 10-file limit. Gems support up to 10
knowledge files (100 MB each).

> "What types of documents will you add to this Gem's knowledge base? Options include:
> Google Docs, Google Sheets, NotebookLM notebooks, PDFs, Markdown files, plain text,
> CSV, DOCX, or others."

**Capture:** File types and live-sync vs. static → Source Policy section.

---

## Step 3 — Source Focus Level

Ask how heavily the Gem should rely on its knowledge files versus its general training and web search. This is the single most important architectural decision for the Gem — it shapes the entire Source Policy section of the instructions.

**What to ask:**
> "How focused should this Gem be on your knowledge files? Here are four levels — pick the one that best fits your use case:
>
> 1. **Knowledge-Only (Strict)** — The Gem answers ONLY from your uploaded files. If the answer isn't in your documents, it says 'I don't have that information.' It will not use general knowledge or web search. Best for: compliance reviews, policy Q&A, document analysis where accuracy is critical.
>
> 2. **Knowledge-First (Recommended for most Gems)** — The Gem checks your files first and cites them. If the answer isn't in your files, it tells you and then offers to try with general knowledge or web search. Best for: brand voice editors, process guides, reference-heavy assistants.
>
> 3. **Balanced** — The Gem uses your files alongside its training data and web search equally. Files inform its answers but don't override everything else. Best for: creative brainstorming with reference material, coding assistants with style guides.
>
> 4. **Training-Primary** — Your files are supplementary reference. The Gem primarily uses its general training and web search, consulting your files only when directly relevant. Best for: general-purpose assistants with a few reference docs."

**If the user doesn't choose or gives an ambiguous answer** (e.g., "I want it to use my documents" or "just make it smart"):
Ask this follow-up:
> "When your documents don't contain the answer to a question, what should the Gem do?
> A) Refuse to answer and say 'Not found in my documents'
> B) Tell the user it's switching to general knowledge, then answer
> C) Just answer naturally using whatever sources are best
>
> This helps me set the right guardrails."

Map the answer: A → Knowledge-Only, B → Knowledge-First, C → Balanced.

**If the user has no knowledge files:**
Skip this step entirely. The Gem will use general training and web search by default.

**Capture:** The source focus level (1-4). This is the primary input for the Source Policy section in the instruction assembly step.

---

## Step 4 — Document and Notebook Names

Ask for specific file/notebook names. Naming them in the instructions significantly
improves retrieval targeting.

> "What are the names of the specific documents or notebooks you'll add to the
> knowledge base? These names may be referenced directly in the Gem's instructions
> to improve retrieval accuracy."

**Capture:** Exact document names → referenced by name in Source Policy and Workflow.

---

## Step 5 — Goal and Purpose

Ask what the Gem should accomplish. Push past vague answers ("help me with stuff") —
Gems exist to perform a specific repeatable task with consistent results.

> "What is your primary goal for this Gem? What problem does it solve or what task
> does it perform for you repeatedly?"

**Capture:** Primary objective → core of Purpose section, shapes Workflow.

---

## Step 6 — Must-Have Behaviors

Ask what non-negotiable behaviors the Gem must always follow. Offer examples if needed
(e.g., "always cite sources", "always read X file first", "output in table format").

> "What 'must-have' behaviors should this Gem always follow? These are non-negotiable
> rules — things it must do every time."

**Capture:** Required behaviors → Behaviors/Rules, Workflow, and Source Policy sections.

---

## Step 7 — Must-Not-Do Behaviors

Ask what the Gem should never do. Offer examples if needed (e.g., "don't use web
search", "don't make up data", "don't discuss off-topic subjects").

> "What should this Gem absolutely never do? These are explicit prohibitions —
> behaviors you want to block."

**Capture:** Prohibitions → Constraints section (placed last for LLM recency bias).

---

## Step 8 — Clarifying Questions

Based on the answers collected in Steps 1-7, identify any gaps and ask **1-2 targeted
clarifying questions**. Do not ask more than two.

Common gaps to check for:

- **Output format**: If the user hasn't specified how the Gem should structure its
  responses (tables, bullet points, narrative, JSON, etc.), ask now.
- **Tone**: If the user hasn't described the communication style (formal, casual,
  technical, encouraging, blunt), ask now.
- **Target audience**: If it's unclear who the Gem is serving (the user personally,
  their team, external clients, students), ask now.
- **Workflow steps**: If the Gem's task involves a multi-step process and the user
  hasn't described the sequence, ask now.
- **Edge cases**: If there's an obvious failure mode the user hasn't addressed
  (e.g., what should the Gem do when a document doesn't contain the answer?), ask now.
- **Source focus ambiguity**: If the user chose a source focus level in Step 3 but their
  must-have or must-not-do behaviors seem to contradict it (e.g., they chose "Knowledge-First"
  but said "never use web search"), resolve the contradiction now.

If all areas are adequately covered from Steps 1-7, say so and move directly to Step 9.

---

## Step 9 — Instruction Assembly Walkthrough

Now walk the user through building each section of the Gem's instructions. For each
section:

1. Propose draft text based on the user's answers from Steps 1-8. Consult
   `references/example-gems.md` to calibrate prose quality and structure.
2. Present the draft in a Markdown code block so the user sees exactly what it will look like.
3. Ask: "Does this look right, or would you like to change anything?"
4. If the user approves, move to the next section.
5. If they request changes, revise once and re-present. Then move on — apply the
   **one-revision cap** and do not revisit the section again in this session.

### Section order and source mapping:

**A. Purpose and Role** (from Steps 1, 5)
- Define the Gem's identity, expertise level, and primary objective.
- Use the Persona + Task pillars from Google's framework.
- Keep it to 2-4 sentences.

**B. Scope and Boundaries** (from Steps 1, 7)
- Define what the Gem handles and what it does not.
- Include redirect language for off-topic requests.

**C. Source Policy** (from Steps 2, 3, 4, 5 — anchored by the Source Focus Level from Step 3)

This is the most critical section for knowledge-grounded Gems. Use the focus level
chosen in Step 3 to select the right template from `references/source-policy-templates.md`.
Four levels are defined: Knowledge-Only (strict), Knowledge-First, Balanced, and
Training-Primary. The reference also covers the Fact Registry technique for Levels 1-2
and NotebookLM-specific grounding patterns. Always reference specific document names
from Step 4.

**D. Knowledge File Reference** (from Step 4)
- List every attached file by name with a one-line description of what it contains.
- Include the directive: "Always reference the attached files before answering."
- This is a separate section from Source Policy — Source Policy defines the rules;
  Knowledge File Reference names the actual documents.

**E. Workflow** (from Steps 5, 6)
- Define the step-by-step process the Gem follows when handling a user query.
- Include any "always do X first" behaviors from Step 6.
- If the user specified structured reasoning, include the extract-then-answer pattern.

**F. Output Format** (from Step 6 or Step 8)
- Define the structure of every response (tables, lists, headings, JSON, etc.).
- Specify what must always be included (citations, confidence level, next steps, etc.).
- Specify what must never be included.

**G. Tone** (from Step 8 or inferred from Steps 1, 5)
- Define the communication style in 1-2 sentences.
- If not explicitly stated, propose a tone that fits the domain and purpose.

**H. Constraints** (from Step 7, plus any additions from Step 8)
- Consolidate all prohibitions into a single section placed at the **end** of the
  instructions (per Google's recommendation to put negative constraints last for
  better adherence).
- Include the anti-hallucination fallback: permission to say "I don't know" or
  "Not found in my sources."

Use the template structure from `references/gem-instruction-template.md` to assemble
these sections.

---

## Step 10 — Final Generation and Delivery

After all sections are approved:

1. **Assemble** the complete instruction set using `references/gem-instruction-template.md`.
2. **Present in chat** as a single Markdown code block with a paste-into-Gem-builder intro.
3. **Write to file** in kebab-case (e.g., `qa-document-reviewer-gem.md`).
4. **Provide next steps:**
   - Required: paste instructions at gemini.google.com → Explore Gems → New Gem, add
     knowledge files via the Knowledge section (not chat), click Save. When editing an
     existing Gem, click the blue "Update" button or changes are lost.
   - Recommended: test with preview pane using normal + adversarial prompts, iterate one
     change at a time. If sharing, warn that recipients can see instruction text and file names.
   - Optional: "magic wand" rewrite button for suggestions, Memory Card workaround
     (running Google Doc) for cross-session continuity.

---

## Handling Special Cases

### User wants to create multiple Gems
Complete one Gem fully before starting the next. Do not interleave.

### User already has partial instructions
Ask to see them. Map what exists to the section framework above, identify gaps,
and walk through only the missing sections.

### User wants to update an existing Gem
Ask to see the current instructions and ask what behavior they want to change or add.
Diagnose which section is responsible. Drop into Step 9 at that section only — do not
re-run the full interview for sections that are working correctly.

### User wants a NotebookLM-grounded Gem
When NotebookLM notebooks are part of the knowledge base, strengthen the Source Policy
with the "Notebook-Only Mode" pattern from `references/best-practices.md`. Emphasize
that even with this pattern, Gems cannot be architecturally restricted from training
data the way NotebookLM can — the instructions are the strongest available lever, not
a guarantee.

### User asks about the Gem's name or description fields
The Name field is primarily organizational — it helps the user identify the Gem and
provides implicit contextual framing. Instructions are what drive behavior. Recommend
a clear, descriptive name (2-5 words encoding scope and function) and a one-sentence
description stating the Gem's purpose.

### User is near or at their Gem limit
Free-plan users have a small cap on total Gems. If the user can't save a new Gem,
they likely need to delete an existing one first. Paid plans (Gemini Advanced) support
more Gems. Direct the user to gemini.google.com → Explore Gems to manage existing Gems.
