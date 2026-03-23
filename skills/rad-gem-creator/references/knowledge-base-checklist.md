# Knowledge Base Preparation Checklist

Use this checklist before building your Gem to ensure your knowledge files are
structured for maximum retrieval accuracy and minimal token waste.

---

## File Format Rankings

Not all file formats perform equally in Gemini's knowledge retrieval pipeline.
Choose formats based on how often the content changes and how well Gemini parses them.

### All supported file types

Gems accept a wide range of formats:

| Category | Supported Formats |
|----------|------------------|
| Documents | Google Docs, TXT, DOC, DOCX, PDF, RTF, DOT, DOTX, HWP, HWPX, Markdown (.md) |
| Spreadsheets | Google Sheets, XLS, XLSX, CSV, TSV |
| Presentations | Google Slides, PPTX |
| Images | JPEG/JPG, PNG, WEBP, HEIF |
| Audio | WAV, MP3, AIFF, AAC, OGG Vorbis, FLAC |
| Video | MP4, MOV, MPEG, MPG, AVI, WMV, WEBM, 3GPP, FLV |

### Text content format priority

For text-heavy knowledge files, format choice directly affects retrieval quality
and token efficiency:

| Rank | Format | Token Efficiency | Live Sync from Drive? | Best For |
|------|--------|------------------|-----------------------|----------|
| 1 | **Google Docs** | High | Yes — auto-updates every session | Style guides, SOPs, policies, memory cards |
| 2 | **Markdown (.md)** | High | No — static snapshot | Structured reference docs, coding standards |
| 3 | **Google Sheets** | High | Yes — auto-updates every session | Tabular data, lookup tables, product catalogs |
| 4 | **Plain text (.txt)** | High | No — static snapshot | Simple reference content, glossaries |
| 5 | **DOCX / RTF** | Good | No — static snapshot | Received documents you cannot convert |
| 6 | **CSV / TSV** | Good | No — static snapshot | Structured data when Sheets is not an option |
| 7 | **PDF** | Low | No — static snapshot | Published reports with charts, diagrams, tables |

### Why PDFs rank last for text-only content

Gemini processes each PDF page as an image using document vision, consuming roughly
258–560 tokens per page regardless of how much text is on the page. The same content
as plain text or a Google Doc uses a fraction of those tokens. Use PDFs only when
the visual layout (charts, diagrams, scanned forms) carries meaning that plain text
cannot reproduce.

For logic-heavy tasks (legal analysis, policy docs), clean `.txt` files with clear
headings outperform complex PDFs. For structured data, `.csv` preserves relationships
better than unstructured formats.

### The live sync advantage

Google Docs and Google Sheets linked from Drive maintain a live connection. When you
edit the source file, the Gem automatically reads the latest version at the start of
the next conversation — no re-upload needed. All other file types are frozen snapshots.
If the source changes, you must delete the old file from the Gem and re-upload the new
version manually.

---

## Hard Limits

- **10 files maximum** in a Gem's permanent knowledge base.
- **100 MB maximum** per file.
- Instructions + knowledge files + conversation history + model responses all share
  a single context window (~1 million tokens on paid plans, less on free tier).
  Larger knowledge bases leave less room for conversation.

### Bypassing the 10-file limit with NotebookLM

A single NotebookLM notebook can hold up to 300 sources on Pro/Ultra plans (50 on free).
Attaching a NotebookLM notebook to a Gem's knowledge base counts as one "file" but
gives the Gem access to all sources inside that notebook. Notebooks also auto-sync —
when you add or update sources in NotebookLM, the connected Gem picks up the changes.

---

## File Naming Conventions

Name your knowledge files so the Gem (and you) can identify them unambiguously.
The Gem's instructions will reference these files by name.

**Do:**
- Use descriptive, specific names: `Brand Voice Guide`, `AQUA 7 Review Standards`,
  `Product API Reference v3`
- Include version or date if the content is versioned: `HR Policy Manual - March 2026`
- Keep names short enough to reference naturally in instructions

**Don't:**
- Use generic names: `Document 1`, `Reference`, `Notes`
- Use names that overlap: `Guide` and `Guidelines` in the same knowledge base

---

## Document Structure Tips

How you organize content inside each file directly affects retrieval quality. Gemini's
parsing works best when it can identify sections by heading, find relevant passages by
structure, and chunk content logically.

### Use headings consistently
- Use H1 (`#`) for the document title.
- Use H2 (`##`) for major sections.
- Use H3 (`###`) for subsections.
- Do not skip heading levels (e.g., jumping from H1 to H3).

### Add front matter to every document
At the top of each file, include:
- **Document name** (matching the file name)
- **Purpose** — one sentence explaining what this document covers
- **Last updated** — date of most recent revision
- **Scope** — what topics this document addresses and does not address

Example:
```
# Brand Voice Guide
Purpose: Defines tone, vocabulary, and style rules for all customer-facing copy.
Last updated: 2026-02-15
Scope: Marketing copy, product descriptions, email campaigns.
Does NOT cover: Internal communications, legal disclaimers, press releases.
```

### Prefer multiple focused files over one monolith
Google's documentation warns that very large uploads can cause the model to miss
details spread across the content. Three 5-page documents organized by topic will
typically outperform a single 15-page document covering everything.

### Keep a Knowledge Index document
If your Gem uses more than 3-4 knowledge files, create a separate Google Doc called
`[Gem Name] Knowledge Index` that lists every file and briefly describes what it
contains. Add this as one of your 10 files. This helps the Gem identify which file
to search for a given query.

Example:
```
# QA Reviewer Gem — Knowledge Index

1. AQUA 7 Review Standards — Scoring criteria and compliance rules for case reviews
2. EMD Protocol Reference — Medical dispatch protocol decision trees and definitions
3. QI Staff Handbook — Team procedures, escalation paths, and reporting requirements
4. QA Findings Template — Required format for completed review reports
```

---

## The Memory Card Pattern

Gems do not have cross-chat memory. Each new conversation starts fresh with only
the Gem's instructions and attached knowledge files. If your workflow requires
continuity across sessions, use this workaround:

1. Create a Google Doc named `[Gem Name] Memory Card`.
2. Add it to the Gem's Knowledge section via Google Drive.
3. At the end of each productive session, ask the Gem to summarize key decisions,
   preferences, and outcomes in a structured format.
4. Copy that summary and paste it into the Memory Card doc (replacing or appending).
5. Because Google Docs auto-sync, the Gem will read the updated Memory Card at the
   start of the next conversation.

Keep the Memory Card focused and periodically pruned. Large memory files dilute
the model's attention across too much context.

---

## The Fact Registry Technique

For small, critical datasets (under ~50 items), consider embedding the data directly
in the Gem's instructions rather than in a knowledge file. This is called a "Fact
Registry."

### Why this works

Knowledge files depend on semantic search retrieval — if the user's question doesn't
match the file content closely enough, the Gem may not find it. Data embedded in the
instructions is always visible to the model on every turn, bypassing retrieval entirely.

### When to use it

- You have a small, stable dataset (product list, team roster, project registry, FAQ)
- Accuracy for this specific data is critical
- The data fits comfortably in the instructions (under ~500 words)
- The data rarely changes (since it's in the instructions, not a live-syncing Google Doc)

### Example

```
# PROJECT REGISTRY
| Name | Client | Status | Key Outcome |
|------|--------|--------|-------------|
| Project Alpha | Acme Corp | Completed | 40% cost reduction |
| Project Beta | GlobalTech | In Progress | Phase 2 deployment |
| Project Gamma | StartupXYZ | Planning | Q3 2026 launch |
Total: 3 projects. No others exist.
```

The closure statement ("Total: 3 projects. No others exist.") is important — it
prevents the model from inventing additional entries from training data.

### When NOT to use it

- Large datasets (50+ items) — these consume too much instruction space
- Frequently changing data — use a Google Doc knowledge file instead (live sync)
- Data that is already in well-structured, clearly-headed knowledge files with
  good retrieval performance

---

## Pre-Build Checklist

Before opening the Gem builder at gemini.google.com:

- [ ] All knowledge files are named descriptively and unambiguously
- [ ] Each file has front matter (name, purpose, date, scope)
- [ ] Files that will change frequently are Google Docs or Sheets (for live sync)
- [ ] Static files (PDFs, Markdown, DOCX) are finalized and current
- [ ] Total file count is 10 or fewer (or using NotebookLM notebooks to consolidate)
- [ ] No single file is excessively large — split monoliths into focused topic files
- [ ] If using 4+ files, a Knowledge Index document is prepared
- [ ] If cross-session memory is needed, a Memory Card Google Doc is prepared
- [ ] Text-only content is in Google Docs, Markdown, or plain text — not PDF
- [ ] PDFs are reserved for documents where visual layout carries meaning
- [ ] REMINDER: After adding or changing knowledge files in an existing Gem, you
  MUST click the blue "Update" button. Without this, changes are not saved. This
  is the most common cause of "my Gem forgot my documents."
