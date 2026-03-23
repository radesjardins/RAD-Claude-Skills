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

## How Files Are Processed (Chunking)

When you upload a file, the GPT system:
1. Breaks it into **chunks of ~800 tokens** with **400-token overlap** between consecutive chunks
2. Embeds each chunk using `text-embedding-3-large`
3. Stores chunks in a vector database for semantic search

On each query, the system retrieves the **top 5-20 most relevant chunks** (not the
full file). This means:
- Well-structured files with clear headings produce cleaner, more targeted chunks
- Dense paragraphs without headings may chunk unpredictably
- The GPT only sees a fraction of your files at any given time
- If a query doesn't match file content closely enough, retrieval returns nothing
  and the model silently falls back to training data

**You cannot configure chunking** through the GPT Builder UI. API users can adjust
`max_chunk_size_tokens` (100-4096) and `chunk_overlap_tokens`, but Builder users
get the defaults.

**Practical implication:** Structure your files for chunking. Each section under a
heading should be self-contained enough to be useful as an isolated 800-token chunk.

---

## File Format Guidance

### All supported file types

**Via file_search (knowledge retrieval):**
| Category | Formats |
|----------|---------|
| Code | `.c`, `.cpp`, `.cs`, `.go`, `.java`, `.js`, `.php`, `.py`, `.rb`, `.sh`, `.ts` |
| Documents | `.doc`, `.docx`, `.pdf`, `.pptx`, `.txt` |
| Markup/Data | `.css`, `.html`, `.json`, `.md`, `.tex` |

Text files must be `utf-8`, `utf-16`, or `ascii` encoded.

**Additional types when Code Interpreter is enabled:**
- Spreadsheets: `.csv`, `.xls`, `.xlsx`
- Images: up to 20MB each
- Additional data formats for programmatic analysis

### File format priority for text content

| Rank | Format | Retrieval Quality | Best For |
|------|--------|-------------------|----------|
| 1 | **Plain text (.txt)** | Most reliable | Rules, procedures, notes — no parsing overhead |
| 2 | **Markdown (.md)** | Excellent | Structured docs — headings improve chunk targeting |
| 3 | **JSON (.json)** | Excellent for structured data | Catalogs, product data, FAQs — outperforms Markdown for complex queries |
| 4 | **Word (.docx)** | Good | Received documents you can't easily convert |
| 5 | **PDF (simple)** | Acceptable | Single-column, clearly headed documents |
| 6 | **PDF (complex)** | Poor — avoid | Multi-column, scanned, image-heavy — parser frequently fails |
| 7 | **PowerPoint (.pptx)** | Poor — avoid | Positional layout context is lost |

### When to use JSON vs. Markdown

- **JSON** outperforms Markdown for structured/catalog data (product lists, FAQs,
  configuration data). Research found JSON provides more consistent retrieval accuracy
  for complex queries.
- **Markdown** is better for narrative text content (policies, guides, procedures).
  Its heading structure naturally aligns with how the retrieval system chunks content.
- **XML tags** within documents can mark important sections for easier retrieval targeting.

### Web content
Copy-paste web page text into `.txt` or `.md` rather than saving as PDF — exported
PDF formatting almost always degrades retrieval quality.

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

### Enable Code Interpreter for tabular data

If your GPT uses CSV, Excel, or other structured data files, enable Code Interpreter
alongside file_search. The model can then parse structured data programmatically rather
than relying solely on semantic chunk retrieval — significantly improving accuracy for
queries like "what's the total for column X" or "filter rows where status is active."

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

## The Fact Registry Technique

For small, critical datasets (under ~50 items), consider embedding the data directly
in the GPT's instructions rather than in a knowledge file.

### Why this works

Knowledge files depend on semantic search retrieval — if the query doesn't match
closely enough, the GPT won't find it. Data embedded in the instructions is always
visible to the model, bypassing retrieval entirely.

### When to use it

- You have a small, stable dataset (product list, team roster, key facts, FAQ)
- Accuracy for this specific data is critical and retrieval has been unreliable
- The data fits within the 8,000-character instruction limit
- The data rarely changes

### Example

```
# TEAM DIRECTORY
| Name | Role | Email | Department |
|------|------|-------|------------|
| Jane Smith | Director | jane@company.com | Engineering |
| Mike Chen | Manager | mike@company.com | Marketing |
Total: 2 team members. No others exist.
```

The closure statement ("Total: 2. No others exist.") prevents the model from
inventing additional entries from training data.

### When NOT to use it

- Large datasets (50+ items) — consumes too much of the 8,000-character limit
- Frequently changing data — you'd need to edit instructions each time
- Data that retrieves reliably from well-structured knowledge files
- When the 8,000-character limit is already tight

---

## Testing Knowledge Retrieval

Before deploying, verify knowledge retrieval with targeted test questions:

1. Ask a question where the answer is clearly stated in a specific file
2. Ask a question that spans two files — verify both are consulted
3. Ask a question not covered in any file — verify the GPT says "not found" rather
   than hallucinating
4. Ask for a citation — verify it names the correct file
5. Ask the same factual question with different phrasing — verify retrieval is consistent
