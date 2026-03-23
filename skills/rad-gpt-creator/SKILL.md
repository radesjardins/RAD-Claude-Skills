---
name: rad-gpt-creator
description: >
  Guided workflow for creating OpenAI ChatGPT Custom GPTs with well-structured
  instructions, knowledge base design, and anti-hallucination patterns. Use this
  skill whenever the user wants to create, build, design, configure, or improve a
  Custom GPT or ChatGPT assistant, or asks about writing GPT instructions. Also
  trigger when the user mentions "Custom GPT," "GPT Builder," "GPT Store," "ChatGPT
  agent," or asks how to set up a specialized AI assistant inside ChatGPT. Trigger
  even if the user says something casual like "I need a GPT for X" or "help me make
  a ChatGPT expert for Y." If the user is talking about building or updating any kind
  of persistent custom assistant in ChatGPT, use this skill.
---

# RAD GPT Creator — Guided ChatGPT Custom GPT Instruction Builder

This skill walks a user through creating or updating a complete, best-practice-aligned
set of instructions for an OpenAI Custom GPT. The output is a ready-to-paste instruction
set delivered as both a code block in chat and a downloadable `.md` file.

## Before You Begin

Read these two reference files at the start of every GPT creation session:

1. `references/best-practices.md` — Hard limits, instruction design rules, knowledge
   base guidance, and anti-hallucination patterns sourced from OpenAI documentation
   and validated community practice
2. `references/gpt-instruction-template.md` — The Markdown skeleton for final output

Load `references/example-gpts.md` only when drafting section prose in Step 8 or when
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
- During Step 8, propose a draft for each section and ask for approval.
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
  causing the problem described. Drop into Step 8 at those sections only.
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

---

## Step 1 — Focus Area

**What to ask:**
> "What is the focus area or specialty of this GPT? For example: Quality Assurance,
> Code Review, Brand Writing, Research Synthesis, Customer Support, etc."

Detect weak answers ("general helper," "everything") — push for a single, narrow domain.
Gems perform best as single-purpose specialists.

**Example answers to offer if needed:**
- "QA reviewer for 911 dispatch case files against our evaluation standards"
- "Brand voice enforcer for marketing copy"
- "Python code reviewer following PEP 8 and our internal style guide"
- "Research synthesizer for competitive market analysis"

**Capture:** Domain and specialty → feeds Purpose and Scope sections.

---

## Step 2 — Knowledge Base Document Types

**What to ask:**
> "What types of files will you upload to this GPT's knowledge base? For example:
> PDFs, plain text files, Markdown, Word documents, spreadsheets, or others?"

**Key distinction to share if the user seems unsure:** Unlike Google Gemini Gems,
Custom GPT knowledge files do not auto-sync. All files are static snapshots — if
the source document changes, the file must be manually re-uploaded through the GPT
Builder. Plan your file update cadence accordingly.

**Example answers to offer if needed:**
- "Two plain text files (our QA standards and scoring rubric) and one PDF policy manual"
- "Three Markdown files: coding standards, error code reference, and API docs"
- "A mix: one Word doc style guide, two PDFs of vendor contracts"

**Capture:** File types → feeds Source Policy and Knowledge Base Checklist guidance.

---

## Step 3 — Document Names

**What to ask:**
> "What are the names of the specific files you'll upload? Naming them directly in
> the instructions improves how reliably the GPT targets the right document."

**Example answers to offer if needed:**
- "QA Standards v4.txt, Scoring Rubric 2026.txt, EMD Protocol Reference.pdf"
- "brand-voice-guide.md, q1-marketing-playbook.md, product-messaging-matrix.md"
- "API Reference v3.md, Frontend Style Guide.md, Error Code Dictionary.txt"

**Capture:** Exact file names → referenced by name in Source Policy and Workflow.

---

## Step 4 — Goal and Purpose

**What to ask:**
> "What is the primary goal for this GPT? What specific repeatable task does it
> perform, or what problem does it solve consistently?"

Push past vague answers ("help me with stuff") — a GPT exists to do one thing over
and over with consistent, reliable results.

**Example answers to offer if needed:**
- "Review QA case files against our standards and produce a structured findings report"
- "Rewrite rough marketing copy to match our brand voice and style guide"
- "Analyze uploaded Python files for security vulnerabilities and produce a severity-ranked report"
- "Answer employee questions about HR policy using only our official handbook"

**Capture:** Primary objective → core of Purpose section, shapes Workflow.

---

## Step 5 — Must-Have Behaviors

**What to ask:**
> "What must-have behaviors should this GPT always follow? These are non-negotiable —
> things it must do every single time."

**Example answers to offer if needed:**
- "Always read the relevant knowledge file before generating any response"
- "Only use uploaded knowledge files — never use general training knowledge"
- "Always cite which document the answer comes from"
- "Ask clarifying questions if the request is ambiguous before starting"
- "Always output findings in a table: Issue | Severity | Recommendation"
- "State which knowledge file is being referenced at the start of each response"

**Capture:** Required behaviors → Workflow and Constraints sections.

---

## Step 6 — Must-Not-Do Behaviors

**What to ask:**
> "What should this GPT absolutely never do? These are explicit prohibitions."

**Example answers to offer if needed:**
- "Do not search the web — answer only from uploaded knowledge files"
- "Do not use general training knowledge to fill gaps"
- "Do not make up data, statistics, or citations"
- "Do not discuss topics outside the defined scope"
- "Do not rewrite submitted code — only flag issues"
- "Do not be sycophantic or use filler praise"

**Capture:** Prohibitions → Constraints section (placed last for LLM recency bias).

---

## Step 7 — Clarifying Questions

Based on Steps 1-6, identify gaps and ask **1-2 targeted questions**. Common gaps:

- **Output format:** Tables, bullets, narrative, JSON — if not specified, ask.
- **Tone:** Formal, technical, casual, encouraging — if not described, ask.
- **Target audience:** Personal use, team, external clients — if unclear, ask.
- **Workflow steps:** If the task is multi-step and sequence isn't described, ask.
- **Edge cases:** What should the GPT do when the answer isn't in the knowledge files?

If all areas are covered, say so and move directly to Step 8.

---

## Step 8 — Instruction Assembly Walkthrough

For each section below:
1. Propose draft text based on Steps 1-7. Consult `references/example-gpts.md` to
   calibrate prose quality and structure.
2. Present the draft in a Markdown code block.
3. Ask: "Does this look right, or would you like to change anything?"
4. If approved, move on. If changes requested, revise once then move on — apply the
   **one-revision cap** without exception.

**Track total character count** as sections are approved. Flag proactively if the
running total approaches 7,000 characters — at that point, help the user identify
content that belongs in a knowledge file rather than the instructions.

### Section order and source mapping:

**A. Role and Purpose** (Steps 1, 4)
- Define the GPT's identity, expertise, and primary objective.
- Use OpenAI's Persona + Task pillars. Keep to 2-4 sentences.
- Include who it serves and what makes it distinct from generic ChatGPT.

**B. Scope and Boundaries** (Steps 1, 6)
- What it handles and what it does not.
- Include redirect language for off-topic requests.

**C. Source Policy** (Steps 2, 3, 5)
- Define the information hierarchy: knowledge files first, user-provided text second.
- Reference specific file names from Step 3.
- Include the "not found" fallback — explicitly grant permission to say "I don't know."
- If strict source-grounding is needed, use the Source-Only Mode pattern from
  `references/best-practices.md`.

**D. Knowledge File Reference** (Step 3)
- List every file by name with a one-line description of its contents.
- Include: "Always search the attached knowledge files before answering."
- Separate from Source Policy — Source Policy defines rules; this section names the documents.

**E. Workflow** (Steps 4, 5)
- Step-by-step process the GPT follows for each user request.
- Use trigger/instruction pairs for multi-step processes (OpenAI's recommended pattern).
- Include "always do X first" behaviors from Step 5.
- If clarifying questions are required before starting: include that explicitly.

**F. Output Format** (Steps 5, 7)
- Define response structure (tables, numbered lists, headings, JSON, etc.).
- Specify what must always be included (citations, next-step suggestions, etc.).
- Specify what must never appear.

**G. Tone** (Step 7, or inferred from Steps 1, 4)
- Communication style in 1-2 sentences.
- If not specified, propose a tone that fits the domain and purpose.

**H. Constraints** (Step 6, plus Step 7 additions)
- All prohibitions consolidated at the **end** of the instructions.
- Include the anti-hallucination fallback: explicit permission to say "I don't have
  that information" rather than guessing.
- Instruction protection language if the user has sensitive knowledge files (see
  `references/best-practices.md` for the deflection prompt pattern).

Use `references/gpt-instruction-template.md` to assemble these sections.

---

## Step 9 — Final Generation and Delivery

After all sections are approved:

1. **Assemble** the complete instruction set using `references/gpt-instruction-template.md`.
   Verify total character count stays under 8,000 characters.

2. **Present in chat** as a single Markdown code block:
   > "Here are your complete GPT instructions. Copy everything inside the code block
   > and paste it into the Instructions field in the GPT Builder at chatgpt.com."

3. **Write to file** in kebab-case with a `-gpt.md` suffix (e.g., `qa-reviewer-gpt.md`)
   and deliver as a downloadable file.

4. **Provide next steps** in two groups:

   **Required setup:**
   - Open chatgpt.com → Explore GPTs → Create (or edit your existing GPT)
   - Paste instructions into the Instructions field in the Configure tab
   - Upload knowledge files via the Knowledge section in Configure — not through chat
   - Enable or disable capabilities (Web Search, DALL·E, Code Interpreter, Canvas) as
     appropriate for your GPT's purpose
   - Click Save / Update in the top right

   **Recommended before deploying:**
   - Test in the preview panel on the right side of the GPT Builder
   - Run at least 2-3 adversarial prompts: off-topic requests, questions not in your
     knowledge files, attempts to get the GPT to contradict its instructions
   - Iterate one change at a time — changing multiple things simultaneously makes it
     impossible to identify what fixed or broke a behavior
   - Write 10-15 test questions covering your GPT's tasks with expected answers; use
     these to verify performance before sharing

   **Optional / situational:**
   - Add Conversation Starters (the Configure tab's "Conversation starters" field) to
     guide users on how to begin — these help with adoption when sharing with a team
   - If the GPT will be shared with a team, consider the Projects + GPT @mention pattern
     for richer context (see Handling Special Cases below)
   - If you plan to publish to the GPT Store, review OpenAI's usage policies before saving
     as "Public"

---

## Handling Special Cases

### User wants to update an existing GPT
Ask to see the current instructions. Identify which section is causing the problem.
Drop into Step 8 at that section only — skip the full interview.

### User already has partial instructions
Map what exists to the section framework. Walk through only the missing sections.

### User wants multiple GPTs
Complete one fully before starting the next.

### User wants a source-grounded GPT (no general knowledge)
Use the Source-Only Mode pattern from `references/best-practices.md` in the Source
Policy section. Note clearly: Custom GPTs cannot be architecturally locked to knowledge
files the way a dedicated RAG system can. Instructions are the strongest available lever,
not a guarantee. The model may occasionally draw on training data for topics it has
strong priors on.

### User asks about memory across sessions
Custom GPTs do not retain context from previous sessions — each interaction is stateless,
regardless of whether the user has memory turned on in their ChatGPT settings.
The Memory Card workaround (a plain text file in the knowledge base updated after each
session with a structured summary) is the best no-code approach. See
`references/best-practices.md` for the full pattern.

Separately: Custom GPTs can be @mentioned inside ChatGPT Projects, and Projects do have
cross-session memory for the project context. If the user needs continuity, the Projects
+ GPT @mention combination may serve them better than the Memory Card approach alone.

### User asks about sharing and publishing
Custom GPTs can be shared three ways: private (only you), link-only (anyone with the
URL), or public (listed in the GPT Store). For team use on Team/Enterprise plans, GPTs
can be published to an internal workspace directory. Public GPTs are subject to OpenAI's
usage policies. Each user's interactions with a shared GPT are independent — they do
not see each other's chats.

### User is near the 8,000-character instruction limit
Help them identify content that belongs in a knowledge file rather than the instructions.
Reference material, long examples, and detailed reference tables should always live in
knowledge files. Instructions should contain behavior rules, workflow steps, and format
directives — not reference content.

### User asks about instruction confidentiality
By default, GPTs will not reveal uploaded file names. If the user wants to protect the
instruction text itself from being extracted, include the deflection prompt pattern from
`references/best-practices.md` in the Constraints section.

### User asks about capabilities (Web Search, DALL·E, Code Interpreter, Canvas)
These are enabled/disabled per-GPT in the Configure tab under Capabilities. Recommend:
- Enable Web Search only if the GPT needs current information beyond its knowledge files
- Enable Code Interpreter if the GPT needs to run calculations, process data, or generate charts
- Enable DALL·E only if image generation is part of the GPT's purpose
- Disable all unused capabilities to reduce scope creep and off-topic behavior
