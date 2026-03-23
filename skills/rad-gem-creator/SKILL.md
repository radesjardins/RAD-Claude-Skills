---
name: rad-gem-creator
description: >
  Guided workflow for creating Google Gemini Gems with well-structured instructions,
  knowledge base design, and anti-hallucination patterns. Use this skill whenever the
  user wants to create, build, design, configure, or improve a Gemini Gem, custom Gemini
  assistant, or asks about writing Gem instructions. Also trigger when the user mentions
  "Gem," "Gems," "Gemini Gem," "custom Gemini," or asks how to set up a specialized AI
  assistant inside Google Gemini. Trigger even if the user says something casual like
  "I need a Gem for X" or "help me make a Gemini expert for Y." If the user is talking
  about building or updating any kind of persistent custom agent in Google Gemini, use
  this skill.
---

# RAD Gem Creator — Guided Gemini Gem Instruction Builder

This skill walks a user through creating or updating a complete, best-practice-aligned
set of instructions for a Google Gemini Gem. The output is a ready-to-paste Markdown
instruction set delivered as both a code block in chat and a downloadable `.md` file.

## Before You Begin

Read these two reference files at the start of every Gem session — they are needed
throughout the workflow:

1. `references/best-practices.md` — Condensed rules from Google's docs and expert sources
2. `references/gem-instruction-template.md` — The Markdown skeleton for final output

Load `references/example-gems.md` only when drafting section prose in Step 8 or when
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
- If after one clarification attempt the answer is still unclear, accept what you have
  and move on. Do not stall the workflow.
- If the user asks for examples at any point, provide them immediately for the current
  question.

### Revision Cap
- During Step 8, propose a draft for each section and ask for approval.
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
  causing the problem the user described. Drop into Step 8 at those sections only —
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

---

## Step 1 — Focus Area

Ask the user what the Gem's focus area or domain is. This defines the Gem's specialty.

**What to ask:**
> "What is the focus area or specialty of this Gem? For example: Brand Design,
> Quality Assurance, Code Review, Research Synthesis, Content Writing, etc."

**Detecting weak answers:** If the user says something like "general helper" or
"everything," explain that Gems perform best as single-purpose specialists and ask
them to narrow the scope.

**Example answers to offer if needed:**
- "Quality Assurance document reviewer for 911 dispatch protocols"
- "Brand voice enforcer for marketing copy"
- "Python code reviewer following PEP 8 and our internal style guide"
- "Research synthesizer for competitive market analysis"

**Capture:** The Gem's domain and specialty. This feeds into the Purpose/Role and
Scope sections of the final instructions.

---

## Step 2 — Knowledge Base Document Types

Ask what types of documents the user will upload to the Gem's knowledge base.

**What to ask:**
> "What types of documents will you add to this Gem's knowledge base? Options include:
> Google Docs, Google Sheets, NotebookLM notebooks, PDFs, Markdown files, plain text,
> CSV, DOCX, or others."

**Why it matters (share with user if they seem unsure):** Google Docs and Sheets
auto-sync from Drive — edits are reflected in the Gem automatically. All other file
types are static snapshots that require manual re-upload when changed. NotebookLM
notebooks can hold up to 300 sources and bypass the Gem's 10-file limit.

**Gem limits to mention if relevant:** Gems support up to 10 knowledge files (100 MB
each). Free-plan users are also limited to a small number of total Gems — if the user
is on a free plan and near their Gem count limit, note that they may need to delete an
existing Gem before saving a new one.

**Example answers to offer if needed:**
- "Two Google Docs (style guide and SOPs) plus one NotebookLM notebook with all our policy PDFs"
- "Three Markdown files with our coding standards, linting rules, and API reference"
- "A mix: one Google Sheet with our product catalog, two PDFs of vendor contracts"

**Capture:** File types and whether live-sync (Google Docs/Sheets) or static uploads
are involved. This feeds into the Source Policy section.

---

## Step 3 — Document and Notebook Names

Ask for the specific names of the documents or notebooks that will be included.

**What to ask:**
> "What are the names of the specific documents or notebooks you'll add to the
> knowledge base? These names may be referenced directly in the Gem's instructions
> to improve retrieval accuracy."

**Why it matters:** Naming specific files in the instructions (e.g., "Refer to the
Brand Voice Guide when reviewing tone") significantly improves how well the Gem
targets the right document for a given query.

**Example answers to offer if needed:**
- "Brand Voice Guide, Q1 2026 Marketing Playbook, Product Messaging Matrix"
- "AQUA 7 Review Standards, EMD Protocol Reference, QI Staff Handbook"
- "Company API Reference v3, Frontend Style Guide, Error Code Dictionary"

**Capture:** Exact document names. These will be referenced by name in the Source
Policy and Workflow sections of the instructions.

---

## Step 4 — Goal and Purpose

Ask what the user wants to accomplish with this Gem.

**What to ask:**
> "What is your primary goal for this Gem? What problem does it solve or what task
> does it perform for you repeatedly?"

**Detecting weak answers:** If the user says "help me with stuff" or "answer questions,"
push for the specific repeatable task. Gems exist because you do something over and over
and want consistent results.

**Example answers to offer if needed:**
- "Review QA case files against our standards and produce a structured findings report"
- "Take rough marketing copy and rewrite it to match our brand voice and style guide"
- "Analyze uploaded Python files for security vulnerabilities and produce a severity-ranked report"
- "Generate lesson plans aligned to my uploaded syllabus and state standards"

**Capture:** The Gem's primary objective. This becomes the core of the Purpose section
and shapes the Workflow section.

---

## Step 5 — Must-Have Behaviors

Ask what behaviors the Gem absolutely must exhibit.

**What to ask:**
> "What 'must-have' behaviors should this Gem always follow? These are non-negotiable
> rules — things it must do every time."

**Example answers to offer if needed:**
- "Always read the Brand Voice Guide before generating any copy"
- "Only use the uploaded knowledge files to answer — never use general training knowledge"
- "Always cite which document and section the answer comes from"
- "Ask clarifying questions before starting if the user's request is ambiguous"
- "Always output findings in a three-column table: Issue, Severity, Recommendation"
- "Start every response by stating which knowledge file(s) are relevant to the query"

**Capture:** Required behaviors. These feed into the Behaviors/Rules and Workflow
sections. If the user specifies source-grounding requirements, they also strengthen
the Source Policy section.

---

## Step 6 — Must-Not-Do Behaviors

Ask what the Gem should never do.

**What to ask:**
> "What should this Gem absolutely never do? These are explicit prohibitions —
> behaviors you want to block."

**Example answers to offer if needed:**
- "Do not search the web for answers"
- "Do not use general training knowledge to fill gaps — say 'I don't know' instead"
- "Do not be sycophantic or use filler praise"
- "Do not make up data, statistics, or citations"
- "Do not discuss topics outside the defined scope"
- "Do not rewrite submitted code — only flag issues"
- "Do not provide legal, medical, or financial advice"

**Capture:** Explicit prohibitions. These feed into the Constraints section and
reinforce the negative constraints at the end of the instructions (exploiting
LLM recency bias).

---

## Step 7 — Clarifying Questions

Based on the answers collected in Steps 1-6, identify any gaps and ask **1-2 targeted
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

If all areas are adequately covered from Steps 1-6, say so and move directly to Step 8.

---

## Step 8 — Instruction Assembly Walkthrough

Now walk the user through building each section of the Gem's instructions. For each
section:

1. Propose draft text based on the user's answers from Steps 1-7. Consult
   `references/example-gems.md` to calibrate prose quality and structure.
2. Present the draft in a Markdown code block so the user sees exactly what it will look like.
3. Ask: "Does this look right, or would you like to change anything?"
4. If the user approves, move to the next section.
5. If they request changes, revise once and re-present. Then move on — apply the
   **one-revision cap** and do not revisit the section again in this session.

### Section order and source mapping:

**A. Purpose and Role** (from Steps 1, 4)
- Define the Gem's identity, expertise level, and primary objective.
- Use the Persona + Task pillars from Google's framework.
- Keep it to 2-4 sentences.

**B. Scope and Boundaries** (from Steps 1, 6)
- Define what the Gem handles and what it does not.
- Include redirect language for off-topic requests.

**C. Source Policy** (from Steps 2, 3, 5)
- Define the priority order for information sources.
- If the user wants source-grounded answers: use the "Source of Truth First" pattern.
- Reference specific document names from Step 3.
- Include the "not found in sources" fallback behavior.
- If NotebookLM notebooks are involved, add the notebook-specific grounding language.

**D. Knowledge File Reference** (from Step 3)
- List every attached file by name with a one-line description of what it contains.
- Include the directive: "Always reference the attached files before answering."
- This is a separate section from Source Policy — Source Policy defines the rules;
  Knowledge File Reference names the actual documents.

**E. Workflow** (from Steps 4, 5)
- Define the step-by-step process the Gem follows when handling a user query.
- Include any "always do X first" behaviors from Step 5.
- If the user specified structured reasoning, include the extract-then-answer pattern.

**F. Output Format** (from Step 5 or Step 7)
- Define the structure of every response (tables, lists, headings, JSON, etc.).
- Specify what must always be included (citations, confidence level, next steps, etc.).
- Specify what must never be included.

**G. Tone** (from Step 7 or inferred from Steps 1, 4)
- Define the communication style in 1-2 sentences.
- If not explicitly stated, propose a tone that fits the domain and purpose.

**H. Constraints** (from Step 6, plus any additions from Step 7)
- Consolidate all prohibitions into a single section placed at the **end** of the
  instructions (per Google's recommendation to put negative constraints last for
  better adherence).
- Include the anti-hallucination fallback: permission to say "I don't know" or
  "Not found in my sources."

Use the template structure from `references/gem-instruction-template.md` to assemble
these sections.

---

## Step 9 — Final Generation and Delivery

After all sections are approved:

1. **Assemble** the complete instruction set by combining all approved sections into
   the template from `references/gem-instruction-template.md`.

2. **Present in chat** as a single Markdown code block with a brief intro:
   > "Here are your complete Gem instructions. Copy everything inside the code block
   > and paste it into the Instructions field of your Gem builder at gemini.google.com."

3. **Write to a file** named after the Gem in kebab-case (e.g., `qa-document-reviewer-gem.md`)
   and deliver it as a downloadable file.

4. **Provide next steps** in two groups:

   **Required setup (do these now):**
   - Paste the instructions into the Instructions field: gemini.google.com → Explore Gems → New Gem
   - Add knowledge files through the Gem editor's Knowledge section — not through the chat
   - Click Save after adding files (the preview pane does not auto-save)

   **Recommended before deploying:**
   - Test with the preview pane using normal prompts and at least 2-3 adversarial prompts
     (off-topic requests, questions not in your knowledge files, attempts to break the output format)
   - Iterate one change at a time when debugging — changing multiple things simultaneously
     makes it impossible to identify what fixed or broke a behavior

   **Optional:**
   - The "magic wand" rewrite button can suggest additions, but your instructions are
     already well-structured — review any suggestions critically before accepting
   - If you're using Google Docs in your knowledge base, the Memory Card workaround
     (a running Google Doc summarizing past sessions) can provide cross-session continuity
     since Gems do not have native cross-chat memory

---

## Handling Special Cases

### User wants to create multiple Gems
Complete one Gem fully before starting the next. Do not interleave.

### User already has partial instructions
Ask to see them. Map what exists to the section framework above, identify gaps,
and walk through only the missing sections.

### User wants to update an existing Gem
Ask to see the current instructions and ask what behavior they want to change or add.
Diagnose which section is responsible. Drop into Step 8 at that section only — do not
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
