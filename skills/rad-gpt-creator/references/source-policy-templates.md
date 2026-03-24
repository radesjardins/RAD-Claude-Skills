# Source Policy Templates — GPT Creator

Use these templates when assembling Section C (Source Policy) of the GPT instructions.
Select the template matching the Source Focus Level chosen in Step 3.

---

## Knowledge-Only (Level 1)

Use the strict SOURCE-ONLY MODE pattern:
- Include: "Always search the attached knowledge files before responding"
- Include: Verification requirement ("Confirm every claim appears in the files")
- Include: Fallback response ("I don't have that information in my reference documents")
- Include: Explicit blocking ("Do not use general training knowledge. Do not search the web.")
- If Web Search capability is enabled, add: "Do NOT use web search unless the user explicitly requests it"
- Reference specific file names from Step 4
- Optional: Visible Receipt ("List which files matched before answering")

## Knowledge-First (Level 2)

Use the "Source of Truth First" pattern:
- Include: Priority order (1. Knowledge files, 2. User text, 3. General knowledge with disclosure)
- Include: Disclosure requirement ("If answering from general knowledge, say so explicitly")
- Include: Fallback with offer ("Not found in my files. Shall I try with general knowledge?")
- Reference specific file names from Step 4

## Balanced (Level 3)

- List knowledge files as primary reference alongside training and web search
- Include: Citation requirement when using knowledge files
- No special grounding restrictions

## Training-Primary (Level 4)

- Mention knowledge files as supplementary reference
- No grounding restrictions or source-blocking language

---

## Fact Registry Technique (Levels 1 and 2)

If the user has a small, critical dataset (under ~50 items), embed it directly in the
instructions rather than relying on file_search retrieval. Data in instructions is
always visible to the model; data in knowledge files depends on retrieval matching.
Watch the 8,000-character limit — this technique trades instruction space for
retrieval reliability.

## Knowledge Index Approach (Levels 1 and 2)

A dedicated file mapping every knowledge file to its contents and query types, serving
as a "table of contents and lookup engine" for the retrieval system.
