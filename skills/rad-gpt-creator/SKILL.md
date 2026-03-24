---
name: rad-gpt-creator
description: >
  This skill should be used when the user says "create a GPT", "custom GPT", "build a GPT",
  "GPT instructions", "ChatGPT assistant", "configure my GPT", or wants to create, improve,
  or configure an OpenAI Custom GPT. Provides a guided interview workflow for well-structured
  instructions, knowledge base design, and anti-hallucination patterns.
---

# RAD GPT Creator — Guided ChatGPT Custom GPT Instruction Builder

This skill walks a user through creating or updating a complete, best-practice-aligned
set of instructions for an OpenAI Custom GPT. The output is a ready-to-paste instruction
set delivered as both a code block in chat and a downloadable `.md` file.

## Before Beginning

Read these two reference files at the start of every GPT creation session:

1. `references/best-practices.md` — Hard limits, instruction design rules, knowledge
   base guidance, and anti-hallucination patterns sourced from OpenAI documentation
   and validated community practice
2. `references/gpt-instruction-template.md` — The Markdown skeleton for final output

Load `references/example-gpts.md` only when drafting section prose in Step 10 or when
the user asks for examples. Do not load it upfront.

Load `references/knowledge-base-checklist.md` only if the user opts into the knowledge
base review in Step 0.

---

## Workflow Rules

### Conversation Flow
- Ask **one question per turn**. Wait for the user's answer before proceeding.
- If the user's answer is weak or vague, offer 2-3 concrete example answers and ask
  them to pick or refine. Accept the answer after one clarification attempt.
- Provide examples immediately if the user asks for them at any point.

### Revision Cap
- During Step 10, propose a draft for each section and ask for approval.
- If the user requests changes, revise and re-present **once**.
- After one revision cycle per section, accept the result and move on.
- Apply this consistently — no section stalls the session.

### Tone and Style
- Direct and efficient. No filler, no flattery, no preamble.
- When proposing draft instruction text, present it in a Markdown code block.

### Output
- Final instructions use **Markdown headings** as the structural format.
- The 8,000-character instruction limit is a hard constraint — flag proactively if
  draft instructions are approaching it, and help the user trim or offload to knowledge
  files before it becomes a blocker.
- Deliver the final product two ways:
  1. A complete code block in chat (for copy-paste into the GPT Builder)
  2. A downloadable `.md` file named after the GPT in kebab-case (e.g., `qa-reviewer-gpt.md`)

---

## Entry Point — Detect Session Type

Before starting the interview, determine what the user needs:

- **New GPT:** Proceed to Step 0.
- **Update an existing GPT:** Ask to see the current instructions. Map them to the
  section framework (Role, Scope, Source Policy, Knowledge Reference, Workflow,
  Output Format, Tone, Constraints). Identify which sections are missing, weak, or
  causing the problem described. Drop into Step 10 at those sections only.
- **Multiple GPTs:** Complete one fully before starting the next.

---

## Step 0 — Knowledge Base Checklist Gate

Before starting the interview, ask:

> "Before we build your GPT's instructions, would you like to review the knowledge
> base preparation checklist? It covers file format guidance, naming conventions,
> the 20-file limit, and structure tips for better retrieval. If you already have your
> files ready, we can skip it. Or I can give you a quick summary of the most important points."

- **Full review:** Read `references/knowledge-base-checklist.md` and present its contents.
  Then proceed to Step 1.
- **Quick summary:** Share these four points, then proceed to Step 1:
  1. 20 files per GPT, 512 MB each, up to 2 million tokens per file. Plain text and
     Markdown (.txt, .md) deliver the most reliable retrieval — use them wherever possible.
  2. PDFs work but are slower and riskier. Single-column, clearly headed PDFs retrieve
     better than complex layouts. Multi-column and scanned PDFs often fail.
  3. Structure your documents with consistent headings (H1/H2/H3). Break large monolithic
     files into smaller focused files — one topic per file retrieves better than one file
     per everything.
  4. Add a Knowledge Index file (a short document listing each file and what it covers)
     when you have four or more knowledge files. This significantly improves retrieval
     targeting.
- **Skip:** Proceed directly to Step 1.

### How Custom GPTs Retrieve from Knowledge Files (Share if the User Seems Unclear)

If the user seems confused about how knowledge files work, or asks why their GPT isn't using their documents, share this explanation:

> "Quick technical note: Custom GPTs don't load your knowledge files into memory like a person reading a document. Instead, your files are broken into small chunks (~800 tokens each), converted into mathematical representations, and stored in a vector database. Each time you ask a question, the GPT searches this database for chunks that semantically match your query — typically returning only 5-20 of the most relevant chunks, not the entire file.
>
> This means if your question doesn't closely match the language in your documents, the GPT may not find the relevant chunks — and it will silently fall back to its general training knowledge without telling you. That's why how we write the instructions matters: we need to explicitly tell the GPT to search its files first and admit when it can't find something."

This sets up why the Source Focus Level question (Step 3) matters.

---

## Step 1 — Focus Area

Ask what the GPT's focus area or domain is. Detect weak answers ("general helper",
"everything") and push for a single-purpose specialty.

> "What is the focus area or specialty of this GPT? For example: Quality Assurance,
> Code Review, Brand Writing, Research Synthesis, Customer Support, etc."

**Capture:** Domain and specialty → Purpose and Scope sections.

---

## Step 2 — Knowledge Base Document Types

Ask what file types will be uploaded. Share if relevant: all GPT knowledge files are
static snapshots (no auto-sync) — re-upload manually when source documents change.

> "What types of files will you upload to this GPT's knowledge base? For example:
> PDFs, plain text files, Markdown, Word documents, spreadsheets, or others?"

**Capture:** File types → Source Policy and Knowledge Base Checklist guidance.

---

## Step 3 — Source Focus Level

Ask how heavily the GPT should rely on its knowledge files versus general training and web search. This shapes the entire Source Policy and determines which capabilities to enable.

**What to ask:**
> "How focused should this GPT be on your knowledge files? Pick the level that fits:
>
> 1. **Knowledge-Only (Strict)** — Answer ONLY from uploaded files. Say 'not found' if the answer isn't in the documents. No web search, no general knowledge. Best for: compliance, policy Q&A, document analysis where accuracy from specific sources is critical.
>
> 2. **Knowledge-First (Recommended for most GPTs)** — Check files first, cite them. If the answer isn't there, disclose that and offer to try with general knowledge. Best for: brand voice editors, internal knowledge bases, reference-heavy assistants.
>
> 3. **Balanced** — Use files alongside training data and web search equally. Files inform answers but don't override other sources. Best for: creative tools with reference material, coding assistants with style guides.
>
> 4. **Training-Primary** — Files are supplementary reference. The GPT primarily uses its training and web search. Best for: general-purpose assistants with a few reference docs."

**If the user doesn't choose or is ambiguous** (e.g., "I want it to use my files"):
> "When your documents don't contain the answer, what should the GPT do?
> A) Refuse to answer and say 'Not found in my documents'
> B) Tell the user it's switching to general knowledge, then answer
> C) Just answer naturally using whatever sources work best
>
> This determines the guardrails I'll build into the instructions."

Map: A → Knowledge-Only, B → Knowledge-First, C → Balanced.

**If the user has no knowledge files:** Skip this step — the GPT uses training and web search by default.

**Capture:** Source focus level (1-4) → primary input for Source Policy in Step 10.

---

## Step 4 — Document Names

Ask for specific file names. Naming them in the instructions improves retrieval targeting.

> "What are the names of the specific files you'll upload? Naming them directly in
> the instructions improves how reliably the GPT targets the right document."

**Capture:** Exact file names → referenced by name in Source Policy and Workflow.

---

## Step 5 — Goal and Purpose

Ask what the GPT should accomplish. Push past vague answers — a GPT exists to perform
a specific repeatable task with consistent results.

> "What is the primary goal for this GPT? What specific repeatable task does it
> perform, or what problem does it solve consistently?"

**Capture:** Primary objective → core of Purpose section, shapes Workflow.

---

## Step 6 — Must-Have Behaviors

Ask what non-negotiable behaviors the GPT must always follow. Offer examples if needed
(e.g., "always cite sources", "always read X file first", "output in table format").

> "What must-have behaviors should this GPT always follow? These are non-negotiable —
> things it must do every single time."

**Capture:** Required behaviors → Workflow and Constraints sections.

---

## Step 7 — Must-Not-Do Behaviors

Ask what the GPT should never do. Offer examples if needed (e.g., "don't use web
search", "don't make up data", "don't discuss off-topic subjects").

> "What should this GPT absolutely never do? These are explicit prohibitions."

**Capture:** Prohibitions → Constraints section (placed last for LLM recency bias).

---

## Step 8 — Capabilities and Actions

Ask what tools and integrations the GPT needs.

**What to ask:**
> "Let's configure what tools this GPT should have access to. For each, tell me yes or no:
>
> - **Web Search** — Can the GPT search the internet for current information?
> - **Code Interpreter** — Can it run Python code, analyze data, create charts?
> - **DALL-E Image Generation** — Can it create images?
> - **Canvas** — Can it use the collaborative editing canvas?
>
> Also: Does this GPT need to connect to any external APIs or services? For example, pulling data from your CRM, posting to Slack, querying a database, or accessing a third-party tool. If so, we'll set up Actions."

**If they want Actions or need guidance on capability choices by Source Focus Level:**
Read `references/capabilities-actions.md` for Actions setup (OpenAPI schema requirements,
authentication, consequential flags) and the security warning for GPTs that combine
Actions with sensitive knowledge files.

**Capture:** Capabilities to enable/disable, and any Actions needed → feeds Configure tab setup in Step 11 and may add to Constraints section.

---

## Step 9 — Clarifying Questions

Based on Steps 1-8, identify gaps and ask **1-2 targeted questions**. Common gaps:

- **Output format:** Tables, bullets, narrative, JSON — if not specified, ask.
- **Tone:** Formal, technical, casual, encouraging — if not described, ask.
- **Target audience:** Personal use, team, external clients — if unclear, ask.
- **Workflow steps:** If the task is multi-step and sequence isn't described, ask.
- **Edge cases:** What should the GPT do when the answer isn't in the knowledge files?
- **Source focus vs. capability contradiction**: If the user chose Knowledge-Only but
  also wants Web Search enabled, or chose Training-Primary but said "never use general
  knowledge" in must-not-do, resolve the contradiction now.

If all areas are covered, say so and move directly to Step 10.

---

## Step 10 — Instruction Assembly Walkthrough

For each section below:
1. Propose draft text based on Steps 1-9. Consult `references/example-gpts.md` to
   calibrate prose quality and structure.
2. Present the draft in a Markdown code block.
3. Ask: "Does this look right, or would you like to change anything?"
4. If approved, move on. If changes requested, revise once then move on — apply the
   **one-revision cap** without exception.

**Track total character count** as sections are approved. Flag proactively if the
running total approaches 7,000 characters — at that point, help the user identify
content that belongs in a knowledge file rather than the instructions.

### Section order and source mapping:

**A. Role and Purpose** (Steps 1, 5)
- Define the GPT's identity, expertise, and primary objective.
- Use OpenAI's Persona + Task pillars. Keep to 2-4 sentences.
- Include who it serves and what makes it distinct from generic ChatGPT.

**B. Scope and Boundaries** (Steps 1, 7)
- What it handles and what it does not.
- Include redirect language for off-topic requests.

**C. Source Policy** (from Steps 2, 3, 4, 6 — anchored by Source Focus Level from Step 3)

This is the most critical section for knowledge-grounded GPTs. Use the focus level
from Step 3 to select the right template from `references/source-policy-templates.md`.
Four levels are defined: Knowledge-Only (strict), Knowledge-First, Balanced, and
Training-Primary. The reference also covers the Fact Registry technique and Knowledge
Index approach for Levels 1-2. Always reference specific file names from Step 4.

**D. Knowledge File Reference** (Step 4)
- List every file by name with a one-line description of its contents.
- Include: "Always search the attached knowledge files before answering."
- Separate from Source Policy — Source Policy defines rules; this section names the documents.

**E. Workflow** (Steps 5, 6)
- Step-by-step process the GPT follows for each user request.
- Use trigger/instruction pairs for multi-step processes (OpenAI's recommended pattern).
- Include "always do X first" behaviors from Step 6.
- If clarifying questions are required before starting: include that explicitly.

**F. Output Format** (Steps 6, 9)
- Define response structure (tables, numbered lists, headings, JSON, etc.).
- Specify what must always be included (citations, next-step suggestions, etc.).
- Specify what must never appear.

**G. Tone** (Step 9, or inferred from Steps 1, 5)
- Communication style in 1-2 sentences.
- If not specified, propose a tone that fits the domain and purpose.

**H. Constraints** (Step 7, plus Step 8 and 9 additions)
- All prohibitions consolidated at the **end** of the instructions.
- Include the anti-hallucination fallback: explicit permission to say "I don't have
  that information" rather than guessing.
- Instruction protection language if the user has sensitive knowledge files (see
  `references/best-practices.md` for the deflection prompt pattern).

Use `references/gpt-instruction-template.md` to assemble these sections.

---

## Step 11 — Final Generation and Delivery

After all sections are approved:

1. **Assemble** using `references/gpt-instruction-template.md`. Verify total stays under
   8,000 characters.
2. **Present in chat** as a single Markdown code block with paste-into-GPT-Builder intro.
3. **Write to file** in kebab-case with `-gpt.md` suffix (e.g., `qa-reviewer-gpt.md`).
4. **Provide next steps:**
   - Required: open chatgpt.com → Explore GPTs → Create, paste instructions into Configure
     tab, upload knowledge files via Knowledge section (not chat), enable/disable capabilities,
     click Save/Update.
   - Recommended: test in preview panel with normal + adversarial prompts, iterate one change
     at a time, write 10-15 test questions with expected answers, write 3-4 Conversation
     Starters (specific tasks, not vague questions — Starters support up to 55,000 characters
     and can supplement the 8,000-character instruction limit).
   - Optional: Projects + GPT @mention pattern for team use, review OpenAI usage policies
     before publishing to GPT Store.

---

## Handling Special Cases

### User wants to update an existing GPT
Ask to see the current instructions. Identify which section is causing the problem.
Drop into Step 10 at that section only — skip the full interview.

### User already has partial instructions
Map what exists to the section framework. Walk through only the missing sections.

### User wants multiple GPTs
Complete one fully before starting the next.

### User wants a source-grounded GPT (no general knowledge)
Use the Source-Only Mode pattern from `references/best-practices.md` in the Source
Policy section. Note clearly: Custom GPTs cannot be architecturally locked to knowledge
files the way a dedicated RAG system can. Instructions are the strongest available lever,
not a guarantee.

### Other special cases
For guidance on memory across sessions, sharing/publishing, instruction confidentiality,
capability configuration, the 8,000-character limit, and Actions security (lethal
trifecta), read `references/capabilities-actions.md`.
