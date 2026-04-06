# Prompt Quality Evaluation Checklist

Run through this checklist before delivering any prompt. Not every item
applies to every prompt — skip items irrelevant to the specific task.
Focus on the sections most relevant to the prompt type.

---

## 1. Clarity & Structure

- [ ] **Golden Rule passed:** A colleague with no context would understand
  what this prompt asks Claude to do.
- [ ] **Task stated upfront:** The prompt leads with what to do, not
  background context.
- [ ] **Instructions are unambiguous:** No phrases that could be interpreted
  multiple ways.
- [ ] **Sequential steps numbered:** When order matters, steps are explicitly
  numbered.
- [ ] **XML tags used for boundaries:** Instructions, input data, examples,
  and output format are in separate tagged sections.
- [ ] **Long context placed first:** Documents/data at top, query at bottom
  (for 20K+ token prompts).

---

## 2. Technique Selection

- [ ] **Right techniques for the task type:** Checked the technique selection
  guide in SKILL.md and applied appropriate techniques.
- [ ] **Few-shot examples included:** 3-5 diverse, relevant examples for
  tasks with complex output formats or non-obvious expectations.
- [ ] **Chain of thought requested:** For complex reasoning, math, multi-step
  analysis, or tasks where the obvious answer is often wrong.
- [ ] **Role assigned:** When tone, style, or domain expertise matters.
- [ ] **Hallucination prevention applied:** For factual tasks — evidence-first
  pattern, uncertainty allowance, or quote grounding.
- [ ] **Template-ready:** If the prompt will be reused, variables are wrapped
  in XML tags and clearly named.

---

## 3. Output Control

- [ ] **Output format specified:** The prompt explicitly states how the
  response should be structured (JSON, XML, prose, bullets, etc.).
- [ ] **Positive framing used:** Instructions say what TO DO, not what NOT
  to do. ("Write in prose" not "Don't use bullet points.")
- [ ] **Length expectations set:** Word count, sentence count, or other
  length constraints stated when relevant.
- [ ] **Prompt style matches output style:** If you want terse output, the
  prompt itself is terse. If you want structured output, the prompt is structured.
- [ ] **Stop sequences considered:** For API use — can a stop sequence
  eliminate unnecessary trailing content?

---

## 4. Context Efficiency

- [ ] **Minimal high-signal tokens:** No redundant, obvious, or filler
  instructions ("be helpful", "write good code").
- [ ] **No over-prompting:** No excessive CRITICAL/MUST/ALWAYS/NEVER
  language (especially for Claude 4.5/4.6).
- [ ] **Variables separated from skeleton:** Reusable template with clear
  variable boundaries.
- [ ] **Appropriate context loaded:** Not too much (token waste) or too
  little (missing information).
- [ ] **System prompt is lean:** For persistent system prompts, every line
  earns its token cost.

---

## 5. Model Compatibility

- [ ] **No deprecated features:** Not using prefilled responses on last
  assistant turn (deprecated in Claude 4.6).
- [ ] **Appropriate thinking settings:** Adaptive thinking for Claude 4.6,
  manual CoT or extended thinking for older models.
- [ ] **Tool descriptions are clean:** Concise, unambiguous, no overlapping
  tools, clear when-to-use guidance.
- [ ] **Temperature appropriate:** 0 for deterministic/factual tasks,
  0.5-1.0 for creative tasks.
- [ ] **Legacy prompting removed:** No instructions needed only for older
  models ("be concise", "skip preamble" — already default in 4.6).

---

## 6. Safety & Edge Cases

- [ ] **Edge cases addressed:** The prompt handles (or tells Claude how to
  handle) unusual inputs, missing data, or ambiguous cases.
- [ ] **Uncertainty allowed:** Claude can say "I don't know" or "I'm not
  sure" when appropriate.
- [ ] **Reversibility considered:** For agentic prompts — dangerous or
  irreversible actions require confirmation.
- [ ] **Input injection considered:** Variable inputs wrapped in XML tags
  to prevent data from being interpreted as instructions.
- [ ] **Scope boundaries set:** Claude knows what's in-scope and what to
  decline or escalate.

---

## 7. Evaluation Readiness

- [ ] **Success criteria clear:** You could objectively determine if the
  prompt's output is correct/good.
- [ ] **Test cases writable:** You could write 5-10 test inputs with
  expected outputs to validate the prompt.
- [ ] **Iteratively improvable:** The prompt structure allows targeted
  fixes without rewriting everything.
- [ ] **Failure modes identifiable:** You know what "bad output" looks like
  and can trace it to a specific prompt weakness.

---

## Quick Triage (for reviewing existing prompts)

When reviewing a prompt that's already in use but underperforming, check
these first — they catch the most common issues:

1. **Would a colleague understand it?** → Fix clarity
2. **Is it telling Claude what NOT to do?** → Reframe positively
3. **Are instructions mixed with data?** → Separate with XML tags
4. **Is it over-prompting with CRITICAL/MUST/ALWAYS?** → Simplify
5. **Missing examples?** → Add 3-5 few-shot examples
6. **Missing output format?** → Specify explicitly
7. **Hallucination risk?** → Add evidence-first or uncertainty allowance
8. **Model mismatch?** → Check for deprecated features or legacy workarounds

---

## Prompt Evaluation Framework (for production prompts)

For prompts going into production, establish formal evaluation:

**Components needed:**
1. **Test cases:** Minimum 20 for development, 100+ for production
2. **Golden answers:** Expert-verified correct/ideal responses
3. **Grading method:** Code-graded (exact match, keyword, regex),
   model-graded (Claude evaluates output), or human-graded
4. **Metrics:** Accuracy, format compliance, latency, token usage

**Evaluation cycle:**
1. Baseline: Run test cases against current prompt, record scores
2. Modify: Apply one technique or change at a time
3. Re-evaluate: Run same test cases, compare to baseline
4. Ship or iterate: If improved, ship; if not, try different technique

**Tools:**
- Anthropic Workbench — built-in evaluation
- Promptfoo — third-party framework for comprehensive evaluation
- Custom scripts — for domain-specific grading logic
