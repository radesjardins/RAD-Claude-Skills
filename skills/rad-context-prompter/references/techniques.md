# Prompt Engineering Techniques Catalog

Complete catalog of prompt engineering techniques from Anthropic's official guides.
Each section covers: what the technique is, when to use it, how to apply it, and
structural examples.

---

## §1 — Clear and Direct Instructions

**What:** Specify exactly what you want Claude to do, including output format,
length, constraints, and success criteria.

**When to use:** Always. This is the foundation of every good prompt.

**How to apply:**

- Lead with the task, not background context
- Number sequential steps when order matters
- Specify output format explicitly (JSON, markdown, prose, XML, etc.)
- State length expectations ("2-3 sentences", "under 500 words")
- Include constraints ("use only information from the provided documents")
- Add scope boundaries ("do not refactor surrounding code")

**Weak vs. strong:**

```
WEAK: "Summarize this article."
STRONG: "Summarize this article in 3 bullet points. Each bullet should be one
sentence. Focus on the key findings, not methodology."
```

**Why it works:** Claude has no context beyond what you provide. Ambiguity forces
Claude to guess — and its guesses may not match your expectations. Specificity
eliminates the guessing.

---

## §2 — Role Prompting

**What:** Assign Claude a specific role, persona, or expertise level to shape
tone, style, depth, and approach.

**When to use:**
- When tone or style matters (customer support, technical docs, casual chat)
- When domain expertise improves accuracy (legal, medical, financial analysis)
- When you want a specific perspective (devil's advocate, beginner-friendly)

**How to apply:**

Place the role in the system prompt for persistent effect, or in the user
message for one-off use.

```
SYSTEM: "You are a senior backend engineer specializing in PostgreSQL
performance optimization. You give concise, actionable advice with SQL examples."
```

- Include the domain of expertise
- Specify the communication style
- Mention the intended audience if relevant
- Keep it to 1-3 sentences — don't write a novel

**Key insight:** Even a single sentence of role assignment measurably changes
Claude's output quality. It's especially effective for logic puzzles, math,
and domain-specific tasks.

---

## §3 — XML Tag Structure

**What:** Use XML tags to create clear boundaries between different parts of a
prompt. Claude was specifically trained to recognize XML tags as prompt-organizing
mechanisms.

**When to use:**
- Separating instructions from input data
- Structuring output format
- Wrapping variable/template content
- Organizing multi-section prompts
- Handling multiple documents

**Core tags and conventions:**

```xml
<!-- Organizing input -->
<instructions>What Claude should do</instructions>
<context>Background information</context>
<input>The data to process</input>
<constraints>Rules and limitations</constraints>

<!-- Structuring examples -->
<examples>
  <example>
    <input>Example input</input>
    <output>Expected output</output>
  </example>
</examples>

<!-- Organizing output -->
<thinking>Reasoning steps</thinking>
<answer>Final answer</answer>
<quotes>Extracted evidence</quotes>

<!-- Multi-document structure -->
<documents>
  <document index="1">
    <source>filename.pdf</source>
    <document_content>{{CONTENT}}</document_content>
  </document>
</documents>
```

**Best practices:**
- Use consistent, descriptive tag names across prompts
- Nest tags when content has natural hierarchy
- Don't overuse — flat structure is fine for simple prompts
- Tag names should be self-documenting (not `<a>`, `<b>`)

---

## §4 — Few-Shot / Multishot Prompting

**What:** Provide examples of desired input-output pairs to demonstrate the
expected behavior, format, and quality.

**When to use:**
- Complex or unusual output formats
- Classification or labeling tasks
- When verbal instructions alone are ambiguous
- Tone or style calibration
- Edge case demonstration

**How to apply:**

```xml
<examples>
  <example>
    <input>The product arrived damaged and customer service was unhelpful.</input>
    <output>
      <sentiment>negative</sentiment>
      <topics>product_quality, customer_service</topics>
      <urgency>high</urgency>
    </output>
  </example>
  <example>
    <input>Love this app! The new update is fantastic.</input>
    <output>
      <sentiment>positive</sentiment>
      <topics>product_quality, updates</topics>
      <urgency>low</urgency>
    </output>
  </example>
  <example>
    <input>It works fine I guess. Nothing special.</input>
    <output>
      <sentiment>neutral</sentiment>
      <topics>general_feedback</topics>
      <urgency>low</urgency>
    </output>
  </example>
</examples>
```

**Best practices:**
- **3-5 examples minimum** for complex tasks; more examples = better performance
- **Relevant:** Mirror your actual use case, not contrived scenarios
- **Diverse:** Cover different categories, edge cases, and difficulty levels
- **Structured:** Wrap in `<example>` tags with clear input/output separation
- **Document-specific examples outperform generic ones** for long-context tasks
- Include reasoning in examples using `<thinking>` tags to demonstrate the
  thought process you want Claude to follow

---

## §5 — Chain of Thought / Thinking

**What:** Ask Claude to reason through problems step-by-step before producing
a final answer. This improves accuracy on complex tasks.

**When to use:**
- Math and logic problems
- Multi-step reasoning
- Tasks where the obvious answer is often wrong
- Analysis requiring weighing multiple factors
- Code debugging and architecture decisions

**Key rule:** Thinking only counts when it's "out loud." You cannot ask Claude
to think internally and only output the answer — the reasoning must appear in
the response for it to improve accuracy.

**Approaches by model:**

**Adaptive thinking (Claude 4.6 — recommended):**
```json
{
  "thinking": {"type": "adaptive"},
  "effort": "high"
}
```
Claude dynamically decides when and how much to think. Outperforms manual
extended thinking in evaluations.

**Manual chain of thought (any model):**
```
Analyze this problem step by step.

First, identify the key variables.
Then, consider how they interact.
Finally, provide your conclusion.

Put your reasoning in <thinking> tags and your final answer in <answer> tags.
```

**Structured reasoning with XML:**
```
Consider both sides of this argument:

<arguments_for>
[Think through supporting points]
</arguments_for>

<arguments_against>
[Think through opposing points]
</arguments_against>

<conclusion>
[Weigh both sides and conclude]
</conclusion>
```

**Self-verification:**
Add "Before finishing, verify your answer against [criteria]" to catch errors.

**Tip:** Prefer general instructions ("Think thoroughly") over prescriptive
step-by-step plans. Claude often reasons better when given latitude.

---

## §6 — Prompt Templates with Variable Substitution

**What:** Separate the fixed instruction skeleton from variable input data,
creating reusable prompts.

**When to use:**
- Batch processing (same task, different inputs)
- Production systems with dynamic inputs
- Any prompt that will be reused with different data

**How to apply:**

```
Classify the following customer feedback into one of these categories:
positive, negative, neutral, mixed.

<feedback>
{{CUSTOMER_FEEDBACK}}
</feedback>

Respond with only the category name.
```

**Best practices:**
- Always wrap substituted values in XML tags — this prevents Claude from
  confusing input data with instructions
- Name variables clearly: `{{CUSTOMER_FEEDBACK}}` not `{{INPUT}}`
- Test with adversarial inputs (data that looks like instructions)

---

## §7 — Long Context Handling (20K+ Tokens)

**What:** Techniques for working with large documents or multiple documents
within Claude's context window.

**When to use:**
- Processing documents over 20K tokens
- Multi-document analysis or comparison
- Research tasks requiring evidence from long sources

**Document placement rule:**
Put documents at the TOP of the prompt, query and instructions at the BOTTOM.
This improves response quality by up to 30%.

**Multi-document structure:**
```xml
<documents>
  <document index="1">
    <source>quarterly_report_q4.pdf</source>
    <document_content>
    {{DOCUMENT_1}}
    </document_content>
  </document>
  <document index="2">
    <source>market_analysis_2025.pdf</source>
    <document_content>
    {{DOCUMENT_2}}
    </document_content>
  </document>
</documents>

Based on the documents above, [your query here].
```

**Quote extraction pattern (critical for accuracy):**
```
First, find all passages in the documents that are relevant to the question below.
Place each relevant passage inside <quotes> tags, with a <source> tag identifying
which document it came from.

Then, using ONLY the information in those quotes, answer the question.
Place your answer in <answer> tags.

If the quotes don't contain enough information to answer, say so.

Question: {{QUESTION}}
```

**Scratchpad approach for research:**
```
Use the <scratchpad> to organize your analysis as you work through the documents.
Extract key facts, note contradictions, and track which sources support each finding.

<scratchpad>
[Your working notes here]
</scratchpad>

<answer>
[Final synthesized answer]
</answer>
```

---

## §8 — Hallucination Prevention

**What:** Techniques to keep Claude grounded in provided information and
honest about uncertainty.

**When to use:**
- Factual tasks where accuracy is critical
- Tasks grounded in specific documents
- Knowledge-intensive queries near the edge of Claude's training data
- Any task where making things up would be harmful

**Techniques:**

**1. Allow uncertainty explicitly:**
```
If the documents don't contain enough information to answer confidently,
say "I don't have enough information to answer this" rather than guessing.
```

**2. Evidence-first pattern:**
```
Before answering, find and quote the specific passages that support your answer.
If you can't find supporting evidence, say so.
```

**3. Investigate-before-answering (for agentic/code contexts):**
```xml
<investigate_before_answering>
Never speculate about code or behavior you haven't verified.
Read the relevant files BEFORE making claims about what they contain.
If you're unsure, say so and suggest how to verify.
</investigate_before_answering>
```

**4. Temperature control:**
Use temperature 0 for factual, classification, or deterministic tasks.
Lower temperature = more consistent, less creative outputs.

**5. Grounding in quotes:**
For long documents, require Claude to extract word-for-word quotes before
reasoning. This forces attention to actual content rather than pattern-matching.

---

## §9 — Output Format Control

**What:** Techniques for steering the format, structure, and style of Claude's
responses.

**When to use:** Almost always — unspecified format leads to unpredictable output.

**Positive framing (do X, not don't Y):**
```
WEAK:  "Don't use markdown. Don't include a preamble."
STRONG: "Write in flowing prose paragraphs. Begin directly with the content."
```

**XML format indicators:**
```
Write your analysis in the following structure:
<summary>2-3 sentence overview</summary>
<key_findings>Bulleted list of findings</key_findings>
<recommendation>Your recommended action</recommendation>
```

**Matching prompt style to output style:**
If your prompt uses no markdown, Claude tends to produce less markdown.
If your prompt is terse and direct, output tends to be terse and direct.

**Structured outputs (API):**
Use Anthropic's Structured Outputs feature or tool-use schemas to enforce
JSON/XML structure programmatically.

**Stop sequences:**
In API calls, use `stop_sequences` to halt output at a closing tag (e.g., `</answer>`).
Saves tokens and eliminates unnecessary concluding remarks.

**LaTeX control (Claude 4.6):**
Claude defaults to LaTeX for math. To get plain text:
"Format all math in plain text. Do not use LaTeX notation."

---

## §10 — Prompt Chaining

**What:** Using the output of one prompt as input to the next, creating
multi-step pipelines.

**When to use:**
- Tasks too complex for a single prompt
- When you need to inspect or validate intermediate results
- Generate → Review → Refine workflows
- Tasks where different steps need different techniques or parameters

**Common patterns:**

**Generate → Review → Refine:**
```
Step 1: "Write a [document] about [topic]."
Step 2: "Review this [document] against these criteria: [criteria]. List issues."
Step 3: "Revise the [document] to address these issues: [issues from step 2]."
```

**Extract → Transform → Load:**
```
Step 1: "Extract all dates, names, and amounts from this contract."
Step 2: "Normalize the extracted data into this JSON schema: [schema]."
Step 3: "Validate the normalized data against these business rules: [rules]."
```

**When NOT to chain:**
- Simple tasks a single prompt handles well
- When you don't need to inspect intermediate results
- When latency matters and the task is parallelizable instead

---

## §11 — Tool Use / Function Calling

**What:** Defining tools that Claude can call to extend its capabilities
(calculations, API calls, data retrieval, code execution).

**When to use:**
- Claude needs real-time or external data
- Tasks requiring computation beyond text generation
- Agentic workflows where Claude takes actions
- Forcing structured output via tool schemas

**Tool description best practices:**

```json
{
  "name": "search_documents",
  "description": "Search the internal knowledge base for documents matching a query. Use this when the user asks about company policies, procedures, or historical decisions. Returns the top 5 matching document excerpts.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Natural language search query describing what to find"
      },
      "department": {
        "type": "string",
        "enum": ["engineering", "hr", "legal", "finance"],
        "description": "Department to search within"
      }
    },
    "required": ["query"]
  }
}
```

**Key principles:**
- **Minimize overlap** between tools — Claude struggles when tools have ambiguous boundaries
- **Descriptive parameters** — explain what each parameter does and when to use it
- **Return token-efficient results** — don't dump raw data, return what Claude needs
- **State when to use AND when not to** in the description

**Controlling tool use behavior:**

For proactive action:
```xml
<default_to_action>
When the user asks you to do something, take action directly rather than
suggesting what they could do. Use available tools to accomplish tasks.
</default_to_action>
```

For conservative behavior:
```xml
<do_not_act_before_instructions>
Before taking any action, confirm with the user what you plan to do.
Explain which tools you'll use and what changes will result.
</do_not_act_before_instructions>
```

**Parallel tool calling (Claude 4.5/4.6):**
```xml
<use_parallel_tool_calls>
When multiple tool calls are independent of each other, call them simultaneously.
Never guess parameters that depend on a previous tool's result — call those sequentially.
</use_parallel_tool_calls>
```

**Forcing structured output with tools:**
Define a tool that Claude never actually executes — Claude still returns output
matching the tool schema. Useful for entity extraction, classification, or
any structured output task.

---

## §12 — Recursive Thinking (Iterative Self-Refinement)

**What:** Instead of producing a single-pass answer, the model decomposes the
problem into subproblems and runs each through a draft → self-critique → refine
loop until further passes yield only minor improvements. The model maintains
an evolving "state" (its current best answer) and explicitly transforms it
through small, traceable reasoning steps.

This produces measurably better results than single-pass Chain of Thought on
complex problems because each refinement pass catches errors, fills gaps, and
tightens reasoning that the initial draft missed.

**When to use:**
- Multi-step problems with trade-offs, constraints, or uncertainties
- Architecture and design decisions where the first answer is rarely the best
- Analysis tasks requiring synthesis across many factors
- Any problem where "think harder" would help but "think step by step" isn't enough
- Tasks where the user needs confidence that edge cases were considered

**When NOT to use:**
- Simple factual questions or lookups
- Tasks where speed matters more than depth
- Reasoning-native models (o3, o4-mini, DeepSeek-R1, Qwen3 thinking mode) —
  they already do internal iterative reasoning; adding this scaffold degrades output
- Tasks that are better served by prompt chaining across separate API calls
  (use §10 instead when you need to inspect intermediate results externally)

**Core loop specification:**

```
When solving this problem, use recursive thinking:

1. Problem framing
   - Restate the goal in one sentence.
   - List 3–7 key subproblems or steps you must solve before answering.

2. Subproblem loop (run for each subproblem, at least one full cycle)
   - Draft: produce a step-by-step reasoning trace and a draft solution.
   - Self-critique: analyze your draft, listing at least 3 concrete issues,
     risks, or gaps. Do not rewrite the solution yet.
   - Refine: produce an improved solution that explicitly addresses each
     issue you listed.

3. Convergence check
   - Compare the refined solution to the previous draft.
   - If you can name 2+ substantive improvements, run one more
     critique-and-refine cycle. Otherwise, stop refining this subproblem.

4. Global integration
   - After stabilizing all subproblems, check for contradictions between them.
   - Resolve conflicts explicitly or state the trade-offs.
   - Present a single coherent answer with key assumptions and any major
     alternatives you considered.

Keep the internal reasoning compact. Prioritize a clear, direct final answer.
```

**Optional: branching for hard problems (Tree of Thoughts variant):**

For highly open-ended or ambiguous problems, add branching to the loop. This
turns the linear recursion into a small search process:

```
4. Branching (use when the problem is highly open-ended or ambiguous)
   - At a key decision point, generate 2–4 distinct candidate plans or
     lines of reasoning.
   - Briefly score each candidate for correctness, feasibility, and
     alignment with the user's goal.
   - Continue the recursive loop only on the best 1–2 candidates.
     Discard the rest.
```

The branching step slots in after convergence check on a subproblem where
the solution space is wide. Use it sparingly — each branch multiplies
token cost. Best for architectural decisions, strategy selection, or
problems where the first reasonable approach is unlikely to be optimal.

**Minimal scaffold version:**

For embedding as a short directive inside a larger system prompt:

```
When the task is complex, use recursive thinking:
1. Restate the goal and list key subproblems.
2. For each subproblem, loop: draft → self-critique (3+ concrete issues) →
   refined solution that fixes them.
3. Stop when another loop would only make minor improvements.
4. For hard decisions, keep 2–3 alternative plans, evaluate them, continue
   only with the best.
5. Integrate all stabilized subsolutions into one clear answer, noting key
   assumptions and trade-offs.
```

**Key insight:** The self-critique step is what makes this work. Without it,
the model just rewrites the same draft with different words. The critique
must produce numbered, concrete issues — not vague "could be better"
observations — because specific issues produce specific fixes.

**Model compatibility:**
- Claude 4.x: works well. Claude's instruction-following makes the loop
  reliable. For API use, adaptive thinking (`thinking: {type: "adaptive"}`)
  combined with recursive thinking instructions gives the best results.
- GPT-5.x: works well. Responds to the structure reliably.
- Gemini 2.x/3: works but may need stricter format locks to prevent the
  critique step from drifting into a full rewrite.
- Open-weight models (Llama, Mistral, Qwen2.5): works at 70B+ parameter
  scale. Smaller models tend to produce shallow critiques.
- o3/o4-mini/R1/Qwen3 thinking: do NOT use — these models handle iterative
  refinement internally.
