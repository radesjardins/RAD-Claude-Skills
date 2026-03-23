# Custom GPT Knowledge Base Checklist

Use this checklist when preparing files for a Custom GPT's knowledge base.
Present this to the user if they opt in during Step 0.

---

## Limits

| Attribute | Limit |
|---|---|
| Files per GPT | 20 |
| Max file size | 512 MB per file |
| Max tokens per file | 2,000,000 (~1M words) |
| File update method | Manual re-upload via GPT Builder UI only |
| Auto-sync | Not supported — all files are static snapshots |

---

## File Format Guidance

**Best choices (most reliable retrieval):**
- `.txt` — Plain text. No parsing overhead. Most consistent retrieval.
- `.md` — Markdown. Excellent structure; headings improve chunk targeting.
- `.docx` — Word documents. Clean text extraction.

**Acceptable with caveats:**
- `.pdf` (simple) — Single-column, clearly headed PDFs retrieve acceptably.
  Avoid: multi-column layouts, scanned pages, heavy image content.
- `.csv` — Tabular data works best when Code Interpreter is also enabled.
  For structured data queries requiring precision, JSON is more reliable than CSV.

**Avoid:**
- `.pdf` (complex) — Multi-column, scanned, or image-heavy PDFs often produce
  extraction errors or missed content.
- `.pptx` — Slide layout and positional context are lost during extraction.

**Web content:** Copy-paste web page text into a `.txt` or `.md` file rather than
saving PDFs of web pages — the exported PDF formatting almost always degrades retrieval.

---

## Document Structure for Better Retrieval

The GPT's retrieval system breaks files into semantic chunks and embeds them. Well-structured
documents chunk predictably and retrieve reliably.

**Do:**
- Use consistent H1/H2/H3 headings throughout
- Add front matter to every file:
  ```
  Document: [Name]
  Purpose: [What this file covers]
  Date: [Last updated]
  Scope: [What it applies to]
  ```
- Keep sections focused — one concept per section
- Use numbered lists or bullet points for rules and procedures
- Bold key terms and rules so they survive chunking

**Avoid:**
- Dense multi-topic paragraphs with no headings
- Tables embedded in PDFs (often misread)
- Footnotes and endnotes (often extracted out of order)
- Running headers/footers with page numbers (add noise to every chunk)

---

## File Organization Strategy

### Focused files beat monoliths
A single 200-page PDF covering 15 topics retrieves far less reliably than 15 focused
files of ~13 pages each. Break large documents by topic whenever possible.

### Naming conventions
Use descriptive, dated filenames. The GPT Builder doesn't auto-sort, so meaningful
names matter for your own management.

Good: `qa-standards-v4-2026.txt`, `brand-voice-guide-q1.md`
Avoid: `doc1.pdf`, `final_final_v3.docx`

### The Knowledge Index pattern (required for 4+ files)
When attaching four or more files, create a dedicated index file:

```
Document: knowledge-index.md
Purpose: Map of all knowledge files in this GPT

FILE LIST
---------
qa-standards-v4-2026.txt
  Contains: QA evaluation criteria, scoring rubric, required behaviors
  Use when: Reviewing or scoring any case file

brand-voice-guide-q1.md
  Contains: Tone, vocabulary, prohibited phrases, style examples
  Use when: Generating or reviewing any marketing copy

product-messaging-matrix.md
  Contains: Approved product claims, competitive positioning, key benefits
  Use when: Writing product-related content or answering product questions
```

Name this file `knowledge-index.md` and reference it explicitly in the Source Policy:
"Refer to knowledge-index.md to identify which file to consult for a given query."

---

## Updating Knowledge Files

All Custom GPT knowledge files are static. There is no auto-sync.

When a source document changes:
1. Update the file locally
2. Open the GPT in the GPT Builder
3. Go to Configure → Knowledge
4. Remove the old file
5. Upload the new version
6. Click Save / Update

**Cadence planning:** If a document changes frequently (weekly or more), consider
whether a Custom GPT with static files is the right tool, or whether a Projects +
instructions approach (which supports live file uploads per conversation) would serve
better.

---

## Testing Knowledge Retrieval

Before deploying, verify knowledge retrieval with targeted test questions:

1. Ask a question where the answer is clearly stated in a specific file
2. Ask a question that spans two files — verify both are consulted
3. Ask a question not covered in any file — verify the GPT says "not found" rather
   than hallucinating
4. Ask for a citation — verify it names the correct file
5. Ask the same factual question with different phrasing — verify retrieval is consistent
