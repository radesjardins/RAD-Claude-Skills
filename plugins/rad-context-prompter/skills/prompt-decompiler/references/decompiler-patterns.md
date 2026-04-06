# Decompiler Patterns Reference

Pattern library for reverse-engineering prompts. Used by the prompt-decompiler skill
to identify structures, map techniques to platforms, and guide cross-platform translation.

---

## Part 1 — Structural Pattern Recognition

### Known Prompt Frameworks

When decompiling a prompt, match against these known frameworks to quickly understand
the author's intent and identify missing components.

| Framework | Signature Elements | Typical Use |
|---|---|---|
| **RTF** | Role → Task → Format (3 sections, flat) | Simple one-shot tasks |
| **CO-STAR** | Context → Objective → Style → Tone → Audience → Response | Business writing, marketing |
| **RISEN** | Role → Instructions → Steps → End Goal → Narrowing | Complex multi-step projects |
| **CRISPE** | Capacity → Role → Insight → Statement → Personality → Experiment | Creative work, brand voice |
| **ReAct** | Objective + Starting State + Target State + Actions + Stop Conditions | Autonomous agents |
| **XML-structured** | Nested `<tags>` organizing sections | Claude-optimized complex prompts |
| **Few-shot** | Task instruction + multiple `<example>` blocks | Format-critical classification |
| **Chain of Thought** | Task + explicit thinking/reasoning steps + answer tags | Logic, math, analysis |
| **Recursive** | Subproblem loop + self-critique + refinement cycle | Complex trade-off problems |
| **Planner/Solver/Critic** | Three distinct system prompts + orchestration logic | Multi-agent workflows |

### Prompt Architecture Types

| Architecture | Characteristics | Complexity |
|---|---|---|
| **Single-shot** | One prompt, one response, no state | Low |
| **Multi-turn** | Conversation design with guidelines | Medium |
| **Chained** | Output of prompt N feeds prompt N+1 | Medium-High |
| **Agentic** | Autonomous with tools, state, stop conditions | High |
| **Multi-agent** | Multiple specialized prompts with orchestration | Very High |

### Platform Syntax Fingerprints

Identify the likely source platform from syntax cues:

| Cue | Likely Platform |
|---|---|
| XML tags (`<context>`, `<instructions>`) | Claude / Anthropic API |
| `{system}` / `{user}` / `{assistant}` blocks | OpenAI Chat API |
| `--ar 16:9 --v 6 --style raw` | Midjourney |
| `(word:1.3)` weight syntax, CFG scale | Stable Diffusion / ComfyUI |
| File paths + "Done when:" | Cursor / Windsurf |
| Starting State + Forbidden Actions + Checkpoints | Claude Code / Devin |
| Trigger → Action → Field mapping | Zapier / Make / n8n |
| `[INST]` / `<<SYS>>` | Llama (legacy format) |
| `/ask` / `/run` / `/code` commands | Unity AI |

---

## Part 2 — Technique-Platform Compatibility Matrix

When decompiling, verify that detected techniques are appropriate for the target
platform. Mismatches are a common source of underperformance.

### Reasoning Techniques

| Technique | Claude 4.x | GPT-5.x | Gemini 3 | o3/o4-mini | R1 | Qwen3-think | Llama/Mistral | Qwen2.5 |
|---|---|---|---|---|---|---|---|---|
| Chain of Thought | Yes | Yes | Yes | **NO** | **NO** | **NO** | Yes (70B+) | Yes |
| Adaptive thinking | Yes (native) | No | No | No | No | No | No | No |
| Recursive thinking | Yes | Yes | Partial* | **NO** | **NO** | **NO** | Yes (70B+) | Yes |
| Few-shot examples | Yes | Yes | Yes | Minimal | Yes | Yes | Yes | Yes |
| Role assignment | Yes | Yes | Yes | Minimal effect | Yes | Yes | Yes (important) | Yes |

*Gemini may need stricter format locks to prevent critique drift.

### Structural Techniques

| Technique | Claude | GPT-5.x | Gemini | Cursor/Windsurf | Midjourney | SD/ComfyUI |
|---|---|---|---|---|---|---|
| XML tags | Optimal | Works | Works | Unnecessary | N/A | N/A |
| JSON schema | Via tools | Native | Via tools | N/A | N/A | N/A |
| Nested structure | Handles well | Handles well | May drift | Keep flat | N/A | N/A |
| Comma-separated | Not optimal | Not optimal | Not optimal | N/A | Optimal | Optimal |
| Weighted syntax | N/A | N/A | N/A | N/A | N/A | Required |

### Behavioral Techniques

| Technique | Claude 4.x | GPT-5.x | o3 | Open-weight |
|---|---|---|---|---|
| Positive framing ("do X") | Strong effect | Moderate | Minimal | Moderate |
| Explicit "be concise" | Unnecessary (default) | Helpful | Unnecessary | Important |
| Stop sequences | API supported | API supported | API supported | Varies |
| Temperature control | Supported | Supported | N/A (reasoning) | Supported |
| Grounding anchors | Very effective | Effective | Less needed | Important |
| Output format locking | Follows precisely | Follows well | Follows well | May drift |

---

## Part 3 — Platform Translation Matrix

Quick-reference for cross-platform adaptation. Each row describes what changes
when moving a prompt between platforms.

### From Claude to Other Platforms

| Target | Structure Changes | Technique Changes | Common Pitfalls |
|---|---|---|---|
| **GPT-5.x** | Keep XML for complex prompts, optional for simple. Add explicit conciseness constraints. | Replace adaptive thinking with manual CoT if needed. | GPT may be more verbose — add length constraints |
| **o3/o4-mini** | Strip to bare minimum. Goal + output format only. Under 200 words. | Remove ALL reasoning scaffolding. Remove role if not critical. | Overlong prompts confuse reasoning models |
| **Gemini 3** | Keep structure. Add format-lock examples. Add hallucination guardrails. | Add explicit grounding: "Base response only on provided context." | Gemini drifts on format — add an example |
| **Cursor/Windsurf** | Add: file path, function name, "Done when:", do-not-touch list. | Remove conversational framing. Remove role unless domain-specific. | Missing file scope = wrong file edited |
| **Claude Code** | Add: starting state, target state, allowed/forbidden actions, stop conditions, checkpoints. | Keep techniques but add safety framework. | Missing stop conditions = runaway agent |
| **Midjourney** | Convert prose to comma-separated. Subject first, then style/mood/lighting. Add `--ar --v --style`. | Remove all reasoning. Remove all structure. | Prose sentences produce worse results than descriptors |
| **Ollama** | Simplify heavily. Output as system prompt + user prompt for Modelfile. | Reduce nesting. Shorten. Add explicit role. | Complex prompts lose coherence on smaller models |

### From GPT to Other Platforms

| Target | Key Changes |
|---|---|
| **Claude** | Add XML tags for section boundaries. Leverage literal instruction following. Remove "be concise" (default). |
| **o3** | Strip everything except goal and output format. Remove CoT. |
| **Midjourney** | Extract visual descriptors from prose. Restructure as comma-separated. |

### From Midjourney to Other Image Platforms

| Target | Key Changes |
|---|---|
| **DALL-E 3** | Convert comma-separated to prose. Add "do not include text in the image." |
| **Stable Diffusion** | Add (word:weight) syntax. Add negative prompt block. Add CFG/steps. |
| **ComfyUI** | Split into Positive/Negative prompt blocks. Ask checkpoint model. |

---

## Part 4 — Compression Heuristics

Token categories for the Compress mode analysis:

### Load-Bearing Tokens (always keep)

- Task verb and direct object ("Classify the following...")
- Output format specification
- Constraints that prevent known failure modes
- Few-shot examples (when format is ambiguous without them)
- Role assignment (when domain expertise materially improves output)
- Stop conditions (agentic prompts)
- File paths and scope boundaries (IDE prompts)

### Frequently Redundant Tokens (review for removal)

- "Please" and politeness markers — no measurable effect on output quality
- "Be helpful" / "Be accurate" / "Be thorough" — already default behavior
- Restating the task in multiple ways
- Explaining what the model already knows (e.g., "as an AI language model...")
- Meta-commentary about the prompt itself
- "Important:" / "Note:" / "Remember:" before every instruction (over-prompting)
- Legacy Claude workarounds: "be concise", "skip the preamble" (default in 4.6)
- Redundant negative instructions alongside positive ones

### Context-Dependent Tokens (judge case-by-case)

- Safety guardrails — keep if failure mode is real, remove if hypothetical
- Domain context — keep if model wouldn't have it, remove if common knowledge
- Multiple examples — 3 is usually enough, 5+ only for complex classification
- Detailed reasoning instructions — keep for standard models, remove for reasoning-native
- Temperature/parameter guidance — only relevant for API users

---

## Part 5 — Decompilation Red Flags

When analyzing a prompt, flag these patterns that strongly indicate underperformance:

### Critical (almost always causing problems)

- CoT/step-by-step instructions sent to o3/o4-mini/R1/Qwen3-thinking
- No output format on a task where format matters
- Multiple distinct tasks in a single prompt without clear separation
- Agentic prompt with no stop conditions
- IDE prompt with no file path scope

### Moderate (often causing problems)

- Role assignment that contradicts the task ("You are a poet. Write SQL queries.")
- Examples that don't match the actual use case
- Over-prompting (CRITICAL/MUST/ALWAYS on every instruction)
- XML tags on a simple 2-sentence prompt (unnecessary overhead)
- Negative-only instructions ("Don't use markdown. Don't be verbose.")

### Minor (sometimes suboptimal)

- Politeness tokens ("Please kindly...")
- Explaining what AI is ("As a large language model...")
- Generic role ("You are a helpful assistant")
- Examples that only show easy cases (no edge cases)
