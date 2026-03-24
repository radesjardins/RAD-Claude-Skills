# Source Policy Templates — Gem Creator

Use these templates when assembling Section C (Source Policy) of the Gem instructions.
Select the template matching the Source Focus Level chosen in Step 3.

---

## Knowledge-Only (Level 1)

Use the strict SOURCE-ONLY MODE pattern:
- Include: Grounding Directive ("Always reference attached files before answering")
- Include: Verification Fence ("Before writing, confirm every claim appears in your files")
- Include: No-Match Path ("If not found: 'This information is not in my reference documents.'")
- Include: Explicit Source Blocking ("Do not use general training knowledge. Do not search the web.")
- Optional: Visible Receipt pattern ("List matched documents before answering")
- Reference specific document names from Step 4

## Knowledge-First (Level 2)

Use the "Source of Truth First" pattern:
- Include: Grounding Directive
- Include: Priority order (1. Knowledge files, 2. User-provided text, 3. General knowledge with disclosure)
- Include: Disclosure requirement ("If answering from general knowledge, say so explicitly")
- Include: No-Match Path with fallback offer ("Not found in my files. Would you like me to answer from general knowledge?")
- Reference specific document names from Step 4

## Balanced (Level 3)

- List knowledge files as a primary reference alongside training and web search
- Include: Citation requirement when using knowledge files
- Include: No special grounding restrictions
- Reference document names from Step 4 as available resources

## Training-Primary (Level 4)

- Mention knowledge files as supplementary reference only
- Include: Directive to check files when the topic directly matches a document's scope
- No grounding restrictions or source-blocking language

---

## Fact Registry Technique (Levels 1 and 2)

If the user has a small set of critical data points (under ~50 items), embed them
directly in the instructions rather than relying on knowledge file retrieval. Data in
instructions is always visible to the model; data in knowledge files depends on
retrieval matching.

## NotebookLM-Grounded Gems

If NotebookLM notebooks are part of the knowledge base, strengthen the grounding
language with the notebook-specific patterns from `references/best-practices.md`.
Emphasize that even with this pattern, Gems cannot be architecturally restricted from
training data the way NotebookLM can — the instructions are the strongest available
lever, not a guarantee.
