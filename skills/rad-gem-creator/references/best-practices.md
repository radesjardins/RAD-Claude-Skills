# Gem Best Practices — Condensed Reference

This file condenses the key principles from Google's official Gem documentation,
Google Cloud prompt engineering guides, and expert community patterns. Use it to
inform decisions during the Gem creation workflow.

---

## Instruction Design

### The Four Pillars Framework (Google's Official Recommendation)
Structure instructions around Persona, Task, Context, and Format. Not every Gem
needs all four, but using at least Persona + Task + one other pillar produces
noticeably better results than unstructured prose.

### Front-load critical rules
Place the most important behavioral constraints and persona definitions at the
top of the instructions. Google's prompting strategy guide recommends placing
critical instructions early. Repeating the most critical constraint at the very
end also helps, because LLMs exhibit recency bias — they attend more strongly to
what they read last.

### One Gem = one job
Gems that try to handle multiple unrelated tasks suffer from instruction conflicts,
confused persona behavior, and degraded output quality. Build separate Gems for
separate functions.

### Instruction length sweet spot
Google does not publish a hard character limit. The context window supports up to
~1 million tokens on paid plans. However, practical effectiveness peaks well below
that. Community consensus and testing suggest 2,000–10,000 characters for most Gems.
Beyond that, the model's attention dilutes and it may start ignoring knowledge files.
Move lengthy reference material into knowledge files instead of cramming it into
the instructions.

### Formatting: Markdown headings
Markdown is the most widely recommended and reliably parsed format for Gem instructions.
Gemini was trained extensively on Markdown-formatted text and has strong affinity for
headings, bold, and bullet lists. XML-style tags are an alternative for strict logic
boundaries, but Markdown is the default recommendation for most users. JSON is not
recommended for instructions — only for output format specification.

### Use Gemini's "magic wand" rewrite as a draft, not the final product
The "Use Gemini to re-write instructions" button expands rough notes into structured
prompts. It is useful for learning what good instruction structure looks like. However,
it may introduce conversational filler, weaken negative constraints, or add unwanted
behaviors. Always review, tighten, and test the output before saving.

---

## Knowledge Base Design

### File format priority
Google Docs and Google Sheets are preferred because they auto-sync from Drive. Markdown
and plain text are token-efficient and well-parsed. PDFs consume far more tokens
(~258-560 per page via document vision) and should be reserved for content where
visual layout matters.

### Structure documents for retrieval
Use consistent headings (H1, H2, H3). Add front matter (name, purpose, date, scope).
Avoid burying key rules in dense paragraphs. Prefer multiple small focused files over
a single monolith — Google warns that very large uploads can miss details.

### The Knowledge Index pattern
If a Gem uses 4+ knowledge files, include a dedicated document listing every file
and what it covers. This helps the Gem's retrieval target the correct file.

### Permanent vs. temporary files
Files added through the Gem editor's Knowledge section are permanent and available
every session. Files attached during a chat are temporary and vanish when the session
ends. Always add reference material through the editor, not the chat window.

---

## Source Grounding and Anti-Hallucination

### The "Source of Truth First" pattern
Write an explicit Source Policy section in the instructions that tells the Gem to
search its knowledge files first, answer from those files, cite the source, and
say "not found" if the answer is absent. This is the strongest lever against
hallucination within the Gem architecture.

### Grant permission to say "I don't know"
LLMs default to satisfying the user's query at any cost, which leads to fabricated
answers. Explicitly instruct the Gem: "If the requested information is not in your
knowledge files, state 'I don't have that information.' Do not guess or infer."

### Require citations
Forcing the model to cite specific documents and sections creates a mechanical
verification step that anchors responses to actual content and reduces free-associative
hallucination.

### Gems cannot be architecturally restricted to knowledge files
Unlike NotebookLM, which is designed to respond only from uploaded sources, Gems can
access web search, training data, and knowledge files simultaneously. No instruction
can fully replicate NotebookLM's architectural grounding guarantee. The instructions
are the strongest available lever, not an absolute lock.

### NotebookLM "Source-Only" emulation
When a NotebookLM notebook is attached to the Gem's knowledge base, use this pattern
in the instructions to approximate NotebookLM's strict source-grounding behavior:

```
SOURCE-ONLY MODE (when using NotebookLM sources)
- Your exclusive function is to analyze, extract, and synthesize information
  from the attached NotebookLM notebook(s).
- Do not search the internet.
- Do not use general training knowledge.
- Do not infer facts not explicitly stated in the notebook sources.
- If the answer is not in the notebook: say "This information is not present
  in the provided documentation."
- Cite the specific source document for every factual claim.
```

This approximation is effective but not airtight — the model may occasionally draw
on training data for topics where it has strong priors.

---

## Cross-Chat Memory

### Gems do not have cross-chat memory
As of February 2026, Gemini's personal memory features ("Instructions for Gemini"
and "Past Gemini chats" personalization) are explicitly not available for Gems.
Each new chat session starts fresh with only the saved instructions and knowledge files.

### The Memory Card workaround
Maintain a Google Doc as a running memory file in the Gem's knowledge base. At the
end of each session, ask the Gem to produce a structured summary. Copy that summary
into the Google Doc. Because Google Docs auto-sync, the Gem reads the latest version
at the start of every new conversation. Keep the Memory Card focused and periodically
pruned — large memory files dilute attention.

---

## Testing and Iteration

### Use the preview pane before saving
The preview panel in the Gem builder lets you test prompts without saving. Use it.
Previewing does not auto-save — you must explicitly click Save.

### Test with adversarial prompts
Before saving, deliberately ask the Gem about off-topic subjects, request information
not in the knowledge base, and try to get it to break its output format. Fix any
failures in the instructions before deploying.

### Iterate one variable at a time
When debugging a Gem that isn't behaving correctly, change one thing at a time
(an instruction, a knowledge file, a constraint) and re-test. Changing multiple
variables simultaneously makes it impossible to identify what fixed (or broke)
the behavior.

### Context poisoning
If a Gem starts ignoring its instructions on your primary account, accumulated
personal context from Gemini's memory/personalization features may be overriding
the Gem's directives. Remedies: clear outdated items from Settings > Saved Info,
add an instruction to deprioritize personal context, or toggle Gemini Apps Activity
off and back on.

---

## Operational Constraints

- Gems can only be created, edited, and deleted in the web app (gemini.google.com) —
  not on mobile. They can be used on both web and mobile.
- Gems cannot be used with Gemini Live.
- Up to 10 files per Gem knowledge base, 100 MB each.
- NotebookLM notebooks bypass the 10-file limit (up to 300 sources per notebook
  on Pro/Ultra plans).
- The Gem name and description fields are primarily organizational — instructions
  are what drive behavior.
- Google Docs/Sheets auto-sync from Drive; all other file types are static snapshots.
