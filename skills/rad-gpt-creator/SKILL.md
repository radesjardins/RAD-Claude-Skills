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

**What to ask:**
> "What is the focus area or specialty of this GPT? For example: Quality Assurance,
> Code Review, Brand Writing, Research Synthesis, Customer Support, etc."

Detect weak answers ("general helper," "everything") — push for a single, narrow domain.
GPTs perform best as single-purpose specialists.

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

**What to ask:**
> "What are the names of the specific files you'll upload? Naming them directly in
> the instructions improves how reliably the GPT targets the right document."

**Example answers to offer if needed:**
- "QA Standards v4.txt, Scoring Rubric 2026.txt, EMD Protocol Reference.pdf"
- "brand-voice-guide.md, q1-marketing-playbook.md, product-messaging-matrix.md"
- "API Reference v3.md, Frontend Style Guide.md, Error Code Dictionary.txt"

**Capture:** Exact file names → referenced by name in Source Policy and Workflow.

---

## Step 5 — Goal and Purpose

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

## Step 6 — Must-Have Behaviors

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

## Step 7 — Must-Not-Do Behaviors

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

**If they want Actions:**
Note the external services needed. Actions require an OpenAPI schema (JSON format, version 3.1.0) defining the API endpoints. For each Action:
- What service it connects to
- What operations it needs (read, write, or both)
- Authentication type (none, API key, or OAuth)
- Whether the operation is consequential (requires user confirmation before executing)

Flag: If the GPT has both Actions (external API access) and access to sensitive knowledge files, warn about the "lethal trifecta" security risk — an AI with access to private data that also processes untrusted input and can send data externally.

**Guidance on capability choices based on Source Focus Level:**
- **Knowledge-Only GPTs:** Disable Web Search. Enable Code Interpreter only if the GPT needs to process data from uploaded files.
- **Knowledge-First GPTs:** Disable Web Search by default. Enable only if explicitly needed for supplementary information.
- **Balanced/Training-Primary GPTs:** Enable Web Search if current information matters.

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
from Step 3 to select the right template:

**Knowledge-Only (Level 1):**
- Use the strict SOURCE-ONLY MODE pattern
- Include: "Always search the attached knowledge files before responding"
- Include: Verification requirement ("Confirm every claim appears in the files")
- Include: Fallback response ("I don't have that information in my reference documents")
- Include: Explicit blocking ("Do not use general training knowledge. Do not search the web.")
- If Web Search capability is enabled, add: "Do NOT use web search unless the user explicitly requests it"
- Reference specific file names from Step 4
- Optional: Visible Receipt ("List which files matched before answering")

**Knowledge-First (Level 2):**
- Use the "Source of Truth First" pattern
- Include: Priority order (1. Knowledge files, 2. User text, 3. General knowledge with disclosure)
- Include: Disclosure requirement ("If answering from general knowledge, say so explicitly")
- Include: Fallback with offer ("Not found in my files. Shall I try with general knowledge?")
- Reference specific file names from Step 4

**Balanced (Level 3):**
- List knowledge files as primary reference alongside training and web search
- Include: Citation requirement when using knowledge files
- No special grounding restrictions

**Training-Primary (Level 4):**
- Mention knowledge files as supplementary reference
- No grounding restrictions or source-blocking language

For Levels 1 and 2, consider the **Fact Registry** technique: if the user has a small,
critical dataset (under ~50 items), embed it directly in the instructions rather than
relying on file_search retrieval. Data in instructions is always visible to the model;
data in knowledge files depends on retrieval matching. But watch the 8,000-character
limit — this technique trades instruction space for retrieval reliability.

For Levels 1 and 2, also consider the **Knowledge Index** approach: a dedicated file
mapping every knowledge file to its contents and query types, serving as a "table of
contents and lookup engine" for the retrieval system.

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
   - Write 3-4 Conversation Starters that demonstrate the GPT's core use cases. Good
     starters are specific tasks, not vague questions. Example: Instead of "Ask me anything
     about HR policy," use "What's the policy on taking bereavement leave?" Starters
     guide users on how to interact and significantly improve adoption when sharing.
     Note: Conversation Starters support up to 55,000 characters total — they can also
     serve as a workaround to provide additional context beyond the 8,000-character
     instruction limit.

   **Optional / situational:**
   - If the GPT will be shared with a team, consider the Projects + GPT @mention pattern
     for richer context (see Handling Special Cases below)
   - If you plan to publish to the GPT Store, review OpenAI's usage policies before saving
     as "Public"

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

### User is building a GPT with Actions and sensitive knowledge files
Warn about the security risk: a GPT that has access to private data (knowledge files),
processes untrusted input (user queries), and can send data externally (via Actions)
creates what security researchers call the "lethal trifecta." Prompt injection attacks
can potentially trick the GPT into exfiltrating knowledge file content through API calls.

Mitigations:
- Use the `x-openai-isConsequential: true` flag on write operations to require user confirmation
- Limit Action scopes to the minimum necessary operations
- Include explicit instruction protection in the Constraints section
- Consider separating sensitive knowledge into a different GPT that doesn't have Actions
- OWASP ranks prompt injection as the #1 security risk for LLM applications (2025)
