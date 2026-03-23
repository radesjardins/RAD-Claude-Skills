# Prompt Patterns Reference

Two sections: patterns to follow (structural skeletons for common task types) and
patterns to avoid (35 anti-patterns that waste tokens and cause re-prompts).

---

# Part 1 — Structural Patterns

Ready-to-use structural patterns for common task types. Each pattern shows the
skeleton — fill in the bracketed sections for your specific use case.

---

## Pattern 1 — Standard Prompt Skeleton

The universal structure that works for most tasks. Not every section is needed
for every prompt — include what's relevant.

```
[ROLE — who the AI is]

[TASK — what to do, stated clearly and directly]

[CONTEXT — background info the model needs]

<instructions>
[Step-by-step instructions, numbered if order matters]
</instructions>

<input>
[The data to process — wrapped in XML to separate from instructions]
</input>

<output_format>
[Exactly how the output should look]
</output_format>

<examples>
  <example>
    <input>[Example input]</input>
    <o>[Example output]</o>
  </example>
</examples>
```

**Ordering principle:** Role → Task → Context → Instructions → Input →
Format → Examples. Put the longest section (usually input/documents) early;
put the query/task near the end for long-context prompts.

---

## Pattern 2 — System Prompt for Interactive Chat

For Claude.ai, Claude Desktop, or chatbot deployments with ongoing conversations.

```
You are [role with domain expertise]. You help [target audience] with
[scope of tasks].

<guidelines>
- [Communication style: concise/verbose, formal/casual, etc.]
- [How to handle ambiguity: ask clarifying questions vs. make assumptions]
- [Scope boundaries: what to help with, what to decline]
- [Key domain knowledge or conventions to follow]
</guidelines>

<tools>
[Description of available tools and when to use each one]
</tools>

<safety>
[Any guardrails: topics to avoid, escalation criteria, etc.]
</safety>
```

---

## Pattern 3 — Quote-Grounded Research

For tasks requiring accurate answers grounded in provided documents.
Prevents hallucination by forcing evidence extraction before reasoning.

```
You are a research analyst. Answer questions using ONLY the information
in the provided documents. If the documents don't contain enough
information, say so explicitly.

<documents>
  <document index="1">
    <source>[document name/path]</source>
    <document_content>
    {{DOCUMENT_CONTENT}}
    </document_content>
  </document>
</documents>

<instructions>
1. Read the question below carefully.
2. Find all passages in the documents relevant to the question.
3. Place each relevant passage in <quotes> tags with its source.
4. Using ONLY the quoted passages, compose your answer.
5. Place your answer in <answer> tags.
6. If the quotes don't support a confident answer, state what's missing.
</instructions>

<question>
{{USER_QUESTION}}
</question>
```

---

## Pattern 4 — Classification / Labeling

For categorizing inputs into predefined categories.

```
Classify the following [item type] into exactly one of these categories:
[category_1], [category_2], [category_3], [category_4].

<rules>
- [Any classification rules or edge case handling]
- If uncertain between two categories, choose [tie-breaking rule].
- Respond with ONLY the category name, nothing else.
</rules>

<examples>
  <example>
    <input>[Example that clearly belongs to category_1]</input>
    <o>category_1</o>
  </example>
  <example>
    <input>[Edge case example]</input>
    <o>category_3</o>
  </example>
  <example>
    <input>[Another example with different category]</input>
    <o>category_2</o>
  </example>
</examples>

<input>
{{ITEM_TO_CLASSIFY}}
</input>
```

---

## Pattern 5 — Agentic System Prompt

For Claude Code, tool-using agents, or autonomous workflows.

```
You are [role]. You accomplish tasks by using the tools available to you.

<capabilities>
[What you can do — read files, write code, search, etc.]
</capabilities>

<workflow>
1. Understand the task. If requirements are ambiguous, ask for clarification.
2. Plan your approach. For complex tasks, break into steps.
3. Execute using available tools. Prefer parallel tool calls when independent.
4. Verify results. Run tests, check output, confirm correctness.
5. Report what you did and any issues encountered.
</workflow>

<decision_framework>
- [When to ask vs. act autonomously]
- [When to use which tool]
- [How to handle errors or unexpected results]
</decision_framework>

<safety>
- For reversible, local actions: proceed without confirmation.
- For irreversible or shared-impact actions: confirm with the user first.
- Never [specific dangerous actions to avoid].
</safety>
```

---

## Pattern 6 — Tool Description Template

For defining tools in the Anthropic API or MCP.

```json
{
  "name": "[verb_noun in snake_case]",
  "description": "[What it does — 1 sentence]. Use this when [trigger conditions]. Returns [what comes back]. Do NOT use for [disambiguation from similar tools].",
  "input_schema": {
    "type": "object",
    "properties": {
      "[param_name]": {
        "type": "[string|number|boolean|array|object]",
        "description": "[What this parameter controls and its format]",
        "enum": ["[valid_values — if finite set]"]
      }
    },
    "required": ["[required_params]"]
  }
}
```

**Principles:**
- Name = verb_noun (`search_documents`, `create_user`, `get_status`)
- Description states WHEN to use AND when NOT to use
- Parameter descriptions include format expectations
- Use enums for finite value sets
- Mark only truly required parameters as required

---

## Pattern 7 — Evaluation / Review

For having an AI evaluate, grade, or review content against criteria.

```
You are an expert [domain] reviewer. Evaluate the following [item type]
against the criteria below.

<criteria>
1. [Criterion 1]: [What good/bad looks like]
2. [Criterion 2]: [What good/bad looks like]
3. [Criterion 3]: [What good/bad looks like]
</criteria>

<input>
{{ITEM_TO_EVALUATE}}
</input>

<output_format>
For each criterion:
- Score: [1-5 or pass/fail]
- Assessment: [1-2 sentences explaining the score]

Overall score: [aggregate]
Summary: [2-3 sentences with key strengths and improvements]
</output_format>
```

---

## Pattern 8 — CLAUDE.md / Project Instructions

For creating project-level instructions that load into every conversation.

```markdown
# [Project Name]

[One-sentence description of what this project does.]

## Key Paths
- [path/] — [what's in this directory]
- [path/] — [what's in this directory]
- [important_file] — [what this file does]

## Build & Test
- Build: `[command]`
- Test: `[command]`
- Lint: `[command]`

## Conventions
- [Language/framework-specific convention]
- [Naming convention]
- [Architecture pattern]

## Workflow
- [Git workflow: branching, commit style, PR process]
- [Deployment process if relevant]

## Common Pitfalls
- [Thing that's easy to get wrong and how to avoid it]
- [Non-obvious requirement or gotcha]
```

**Keep under 100 lines.** Every line costs tokens on every turn.

---

## Pattern 9 — Prompt Improvement

For improving an existing prompt that isn't performing well.

```
You are an expert prompt engineer following Anthropic's official methodology.

<current_prompt>
{{PROMPT_TO_IMPROVE}}
</current_prompt>

<observed_issues>
{{DESCRIPTION_OF_PROBLEMS}}
</observed_issues>

<instructions>
1. Analyze the current prompt against these quality criteria:
   - Clarity: Would a colleague understand what to do?
   - Structure: Are instructions separated from data with XML tags?
   - Specificity: Is the output format explicitly defined?
   - Examples: Are few-shot examples provided for complex tasks?
   - Positive framing: Does it say what TO DO (not what NOT to do)?

2. Identify the root cause of each observed issue.

3. Rewrite the prompt applying the minimum changes needed to fix the issues.

4. Explain what you changed and why, referencing specific techniques.
</instructions>
```

---

## Pattern 10 — Multi-Turn Conversation Design

For designing prompts that handle ongoing conversations.

```
You are [role] helping [audience] with [scope].

<conversation_guidelines>
- Maintain context from earlier messages in the conversation.
- If the user changes topic, acknowledge and pivot naturally.
- For multi-step processes, track progress and guide the user through each step.
- If you need information the user hasn't provided, ask for it specifically.
</conversation_guidelines>

<response_style>
- [Length: concise/detailed]
- [Tone: professional/casual/empathetic]
- [Format: prose/bullets/structured]
</response_style>

<edge_cases>
- If the user asks something outside your scope: [how to handle]
- If the user is frustrated: [how to handle]
- If the request is ambiguous: [ask clarifying questions vs. make best guess]
- If you're unsure: [admit uncertainty vs. provide best effort]
</edge_cases>
```

---

## Pattern 11 — Skill / Instruction File

For writing Claude Code skills or instruction files.

```yaml
---
name: [kebab-case-name]
description: >
  [What it does — 1 sentence]. [When to use — specific triggers, contexts,
  phrases that should activate this skill]. [Key capabilities].
---
```

```markdown
# [Skill Name]

[1-2 sentence purpose statement: what this skill makes Claude do.]

## Workflow

[Numbered steps of how Claude should operate when this skill is active.]

## Principles

[Key principles that guide decision-making — explain WHY, not rigid rules.
Use reasoning-based language: "Validate inputs because malformed data
causes silent failures" not "ALWAYS validate inputs".]

## Reference Files

[Links to detailed reference docs in references/ directory for
progressive disclosure — keep the main file lean.]
```

**Key conventions:**
- Description field is the trigger — be generous with activation contexts
- Use reasoning-based language, not rigid ALWAYS/NEVER rules
- Keep main file under 300 lines; move depth to references/
- Include examples of good and bad outcomes when helpful

---

## Pattern 12 — Multi-Agent Orchestration (Planner / Solver / Critic)

For complex tasks that benefit from separating planning, execution, and
evaluation into distinct agent roles. Works with Claude Code agent teams,
n8n AI Agent workflows, LangGraph, CrewAI, AutoGen, or custom orchestration
code. Any model that follows system prompts can fill any role.

**When to use:** Tasks with multiple interdependent subproblems, tasks
requiring tool use combined with critical evaluation, or workflows where
you want explicit quality gates between steps.

**When NOT to use:** Simple tasks a single agent handles in 1-2 tool calls.
The overhead of multi-agent coordination isn't worth it for straightforward work.

**Roles:**

- **Planner**: decomposes the task, maintains global state, selects the next
  subproblem, synthesizes the final answer. Does not solve domain problems
  or call external tools directly.
- **Solver**: proposes concrete solutions for one subproblem at a time, calls
  tools when needed, produces explicit reasoning traces. Does not self-critique
  or finalize answers.
- **Critic**: evaluates Solver outputs against explicit criteria, drives
  refinement. Does not solve tasks from scratch or rewrite solutions.

You can merge Planner into Critic or Solver for a two-agent setup.

### Planner system prompt

```
You are the Planner agent. You manage recursive problem solving across
multiple agents.

Behavior:
1. Read the user's request and restate the overall goal in one sentence.
2. Decompose the goal into 3–7 ordered subproblems.
3. For each subproblem, decide:
   - Inputs required (from user, tools, or prior subproblems)
   - Which tools may be helpful
   - What success criteria look like.
4. For the current subproblem, construct a concise task message for the
   Solver that includes:
   - Subproblem description
   - Relevant context from previous steps
   - Any tool constraints
   - Explicit success criteria.
5. After receiving the Solver's answer and the Critic's review:
   - Decide whether to trigger another Solver pass or move on.
   - Maintain a short "state summary" of accepted decisions and key
     assumptions.
6. When all subproblems are complete, produce a global consistency check:
   - Note any contradictions or unresolved trade-offs.
   - If serious issues remain, loop specific subproblems again.
7. Synthesize a single coherent answer for the user from the accepted
   subproblem results.

You do not solve domain problems in detail and do not call external
tools directly.
```

### Solver system prompt

```
You are the Solver agent. You solve one subproblem at a time, using
tools if available.

For each task from the Planner:
1. Restate the subproblem and list key constraints and success criteria.
2. If tools are available and needed, call them to gather data or perform
   computations before finalizing your draft.
3. Produce a draft solution with an explicit reasoning trace:
   - Step-by-step logic
   - How tool results influenced your reasoning
   - Assumptions you had to make.
4. Structure your output as:
   - Reasoning: short, numbered steps
   - DraftSolution: concise proposal or answer
   - OpenIssues: known gaps, uncertainties, or risks.

Do not self-critique or finalize the answer. The Critic will review
your draft and guide revisions.
```

### Critic system prompt

```
You are the Critic agent. You evaluate Solver outputs and drive
refinement. You do not solve tasks from scratch.

For each Solver output:
1. Read:
   - The original user request (or Planner summary)
   - The current subproblem description
   - The Solver's latest output.
2. Evaluate against these criteria:
   - Logical correctness and internal consistency
   - Faithfulness to tool outputs and given context
   - Coverage of constraints and success criteria
   - Safety, clarity, and practicality.
3. Produce:
   - Issues: numbered list of 3–10 concrete problems or risks
   - Severity: tag per issue (critical / important / minor)
   - ImprovementGuidance: specific instructions to the Solver on how
     to revise — which steps to change, what extra tool calls are
     needed, how to tighten reasoning.
4. Conclude with a RefinementNeeded flag:
   - yes: if resolving your issues would materially improve the solution
   - no: if issues are minor and the Planner can accept the solution.

You may propose alternative directions but must not fully rewrite the
solution yourself.
```

### Orchestration logic

```
1. Send user request to Planner.
2. Planner returns decomposition + first subproblem task for Solver.
3. Loop per subproblem:
   a. Send task + current state to Solver.
   b. Send Solver output to Critic.
   c. If Critic says RefinementNeeded: yes AND refinement budget remains,
      send ImprovementGuidance + original task back to Solver.
   d. When RefinementNeeded: no OR budget exhausted, record subproblem
      as "accepted".
   e. Ask Planner for next subproblem, passing updated state.
4. When all subproblems accepted, Planner synthesizes the final answer.

Budget: 2–3 Solver–Critic cycles per subproblem. Hard cap prevents
runaway loops.
```

**Model compatibility:**
- Claude Code agent teams: native support. Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Planner is the lead agent, Solver and Critic are teammates.
- n8n / LangGraph / CrewAI: implement the orchestration logic as workflow nodes. Each agent is a separate LLM call with its own system prompt.
- Any model that follows system prompts reliably can fill any role (Claude, GPT-5, Gemini, Qwen 70B+). Smaller open-weight models tend to rubber-stamp in the Critic role — use a stronger model for Critic if mixing model sizes.

---
---

# Part 2 — Anti-Patterns

35 patterns that waste tokens and cause re-prompts. Read this section when the user
pastes a bad prompt and asks you to fix it, or when diagnosing underperformance.

---

## Task Anti-Patterns

| # | Pattern | Bad Example | Fixed |
|---|---------|------------|-------|
| 1 | **Vague task verb** | "help me with my code" | "Refactor `getUserData()` to use async/await and handle null returns" |
| 2 | **Two tasks in one prompt** | "explain AND rewrite this function" | Split into two prompts: explain first, rewrite second |
| 3 | **No success criteria** | "make it better" | "Done when the function passes existing unit tests and handles null input without throwing" |
| 4 | **Over-permissive agent** | "do whatever it takes" | Explicit allowed actions list + explicit forbidden actions list |
| 5 | **Emotional task description** | "it's totally broken, fix everything" | "Throws uncaught TypeError on line 43 when `user` is null" |
| 6 | **Build-the-whole-thing** | "build my entire app" | Break into Prompt 1 (scaffold), Prompt 2 (core feature), Prompt 3 (polish) |
| 7 | **Implicit reference** | "now add the other thing we discussed" | Always restate the full task — never reference "the thing we discussed" |

## Context Anti-Patterns

| # | Pattern | Bad Example | Fixed |
|---|---------|------------|-------|
| 8 | **Assumed prior knowledge** | "continue where we left off" | Include Memory Block with all prior decisions |
| 9 | **No project context** | "write a cover letter" | "PM role at B2B fintech, 2yr SWE experience transitioning to product, shipped 3 features as tech lead" |
| 10 | **Forgotten stack** | New prompt contradicts prior tech choice | Always include Memory Block with established stack |
| 11 | **Hallucination invite** | "what do experts say about X?" | "Cite only sources you are certain of. If uncertain, say so explicitly rather than guessing." |
| 12 | **Undefined audience** | "write something for users" | "Non-technical B2B buyers, no coding knowledge, decision-maker level" |
| 13 | **No mention of prior failures** | (blank) | "I already tried X and it didn't work because Y. Do not suggest X." |

## Format Anti-Patterns

| # | Pattern | Bad Example | Fixed |
|---|---------|------------|-------|
| 14 | **Missing output format** | "explain this concept" | "3 bullet points, each under 20 words, with a one-sentence summary at top" |
| 15 | **Implicit length** | "write a summary" | "Write a summary in exactly 3 sentences" |
| 16 | **No role assignment** | (blank) | "You are a senior backend engineer specializing in Node.js and PostgreSQL" |
| 17 | **Vague aesthetic adjectives** | "make it look professional" | "Monochrome palette, 16px base font, 24px line height, no decorative elements" |
| 18 | **No negative prompts for image AI** | "a portrait of a woman" | Add: "no watermark, no blur, no extra fingers, no distortion, no text overlay" |
| 19 | **Prose prompt for Midjourney** | Full descriptive sentence | "subject, style, mood, lighting, composition, --ar 16:9 --v 6" |

## Scope Anti-Patterns

| # | Pattern | Bad Example | Fixed |
|---|---------|------------|-------|
| 20 | **No scope boundary** | "fix my app" | "Fix only the login form validation in `src/auth.js`. Touch nothing else." |
| 21 | **No stack constraints** | "build a React component" | "React 18, TypeScript strict, no external libraries, Tailwind only" |
| 22 | **No stop condition for agents** | "build the whole feature" | Explicit stop conditions + ✅ checkpoint output after each step |
| 23 | **No file path for IDE AI** | "update the login function" | "Update `handleLogin()` in `src/pages/Login.tsx` only" |
| 24 | **Wrong template for tool** | GPT-style prose prompt used in Cursor | Adapt to File-Scope Template (Template G) |
| 25 | **Pasting entire codebase** | Full repo context every prompt | Scope to only the relevant function and file |

## Reasoning Anti-Patterns

| # | Pattern | Bad Example | Fixed |
|---|---------|------------|-------|
| 26 | **No CoT for logic task** | "which approach is better?" | "Think through both approaches step by step before recommending" |
| 27 | **Adding CoT to reasoning models** | "think step by step" sent to o1/o3 | Remove it — reasoning models think internally, CoT instructions degrade output |
| 28 | **Expecting inter-session memory** | "you already know my project" | Always re-provide the Memory Block in every new session |
| 29 | **Contradicting prior work** | New prompt ignores earlier architecture | Include Memory Block with all established decisions |
| 30 | **No grounding rule for factual tasks** | "summarize what experts say about X" | "Use only information you are highly confident is accurate. Say [uncertain] if not." |

## Agentic Anti-Patterns

| # | Pattern | Bad Example | Fixed |
|---|---------|------------|-------|
| 31 | **No starting state** | "build me a REST API" | "Empty Node.js project, Express installed, `src/app.js` exists" |
| 32 | **No target state** | "add authentication" | "`/src/middleware/auth.js` with JWT verify. `POST /login` and `POST /register` in `/src/routes/auth.js`" |
| 33 | **Silent agent** | No progress output | "After each step output: ✅ [what was completed]" |
| 34 | **Unlocked filesystem** | No file restrictions | "Only edit files inside `src/`. Do not touch `package.json`, `.env`, or any config file." |
| 35 | **No human review trigger** | Agent decides everything autonomously | "Stop and ask before: deleting any file, adding any dependency, or changing the database schema" |
