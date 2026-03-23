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

### Supported file formats

Gems support a wide range of file types:

| Category | Formats |
|----------|---------|
| Documents | Google Docs, TXT, DOC, DOCX, PDF, RTF, DOT, DOTX, Markdown |
| Spreadsheets | Google Sheets, XLS, XLSX, CSV, TSV |
| Presentations | Google Slides, PPTX |
| Images | JPEG/JPG, PNG, WEBP, HEIF |
| Audio | WAV, MP3, AIFF, AAC, OGG Vorbis, FLAC |
| Video | MP4, MOV, MPEG, MPG, AVI, WMV, WEBM, 3GPP, FLV |

### File format priority for text content

For text-heavy knowledge files, format choice affects retrieval quality:

| Rank | Format | Token Efficiency | Live Sync? | Best For |
|------|--------|------------------|------------|----------|
| 1 | Google Docs | High | Yes | Style guides, SOPs, policies, memory cards |
| 2 | Plain text / Markdown | High | No | Structured reference docs, coding standards |
| 3 | Google Sheets | High | Yes | Tabular data, lookup tables, catalogs |
| 4 | DOCX / RTF | Good | No | Received documents you cannot convert |
| 5 | CSV / TSV | Good | No | Structured data when Sheets isn't an option |
| 6 | PDF | Low | No | Documents where visual layout matters |

For logic-heavy tasks (legal analysis, policy docs), clean `.txt` files with clear
headings outperform complex PDFs. For data, structured `.csv` preserves relationships
better than unstructured formats. PDFs consume roughly 258-560 tokens per page via
document vision regardless of text density.

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

## How Knowledge Retrieval Actually Works (RAG Architecture)

Understanding this is critical for writing effective Gem instructions.

### Knowledge files are NOT loaded into context

System instructions (the text in the Instructions field) are always visible to the
model on every turn. Knowledge files are different — they are chunked, vectorized,
and stored in a retrieval index. On each turn, the user's query is matched against
these vectors via semantic search, and only the most relevant chunks are pulled in.

### Silent fallback is the default behavior

When the user's query doesn't match closely enough to any knowledge file content,
retrieval returns nothing — and the model silently falls back to its general training
data. There is no indication to the user that this happened. The model does not say
"I couldn't find this in your files, so I'm using general knowledge." It just answers
from training data as if it were authoritative.

### There is no user control over retrieval thresholds

Google does not expose the relevance threshold for knowledge file retrieval. You cannot
tune how aggressively the Gem searches its files. The only levers available are:
1. **Instruction-level directives** — telling the Gem to always check files first
2. **Document structure** — well-organized files with clear headings retrieve better
3. **File naming** — referencing files by name in instructions improves targeting
4. **The Fact Registry technique** — embedding critical data directly in instructions
   bypasses retrieval entirely (see Anti-Hallucination Patterns below)

### Implications for instruction design

- Without explicit "check your files first" instructions, the Gem will default to
  training data whenever retrieval misses
- Instructions that say "use your knowledge files" are necessary but not sufficient —
  you also need fallback behavior for when retrieval returns nothing
- For mission-critical accuracy, consider the Fact Registry technique for small datasets
  and the Visible Receipt pattern for verification

---

## Source Grounding and Anti-Hallucination

### Why Gems Hallucinate

Gems hallucinate for a specific architectural reason: knowledge files are retrieved
via semantic search, not loaded into context. When retrieval returns nothing (because
the user's query doesn't match the file content closely enough), the model has no
signal that it should refuse to answer — so it answers from training data. The
following patterns address this at different levels of strictness.

### Pattern 1: Grounding Directive (use in ALL knowledge-grounded Gems)

Place this as the FIRST line of the SOURCE POLICY section:

> "Always reference the attached knowledge files before answering any question."

Without this, Gems drift away from uploaded files, especially in longer conversations.
This is the minimum viable anti-hallucination measure.

### Pattern 2: Source of Truth First (Knowledge-First Gems)

Tell the Gem to search knowledge files first, answer from them, cite the source, and
disclose when falling back to general knowledge:

```
Primary sources (in order):
1. Knowledge files attached to this Gem — always search these first.
2. User-provided text in the current chat.
3. General knowledge — use ONLY when files don't contain the answer,
   and explicitly state: "This answer is from general knowledge, not
   your documents."
```

### Pattern 3: Strict Knowledge-Only Mode (Knowledge-Only Gems)

For Gems where accuracy from specific documents is critical:

```
SOURCE-ONLY MODE
- Your exclusive function is to analyze and answer from the attached files.
- Do not search the internet.
- Do not use general training knowledge.
- Do not infer facts not explicitly stated in the files.
- If the answer is not in the files: "This information is not in my
  reference documents."
- Cite the specific document name for every factual claim.
```

This is effective but not airtight — the model may occasionally draw on training
data for topics where it has strong priors.

### Pattern 4: Fact Registry (bypasses RAG entirely)

For small, critical datasets (under ~50 items), embed the data directly in the
instructions rather than in knowledge files. Data in instructions is always visible
to the model; data in knowledge files depends on retrieval matching.

```
# PROJECT REGISTRY
| Name | Client | Status | Key Outcome |
|------|--------|--------|-------------|
| Project Alpha | Acme Corp | Completed | 40% cost reduction |
| Project Beta | GlobalTech | In Progress | Phase 2 deployment |
[... all entries ...]
Total: 12 projects. No others exist.
```

End with an explicit closure statement ("Total: X. No others exist.") to prevent
the model from inventing additional entries.

### Pattern 5: Visible Receipt (verification checkpoint)

Force the Gem to list which documents/sections it found before generating a response:

```
Before answering, output a brief "Sources Found" section listing:
- Which knowledge file(s) matched the query
- Which specific section(s) within those files are relevant
Then construct your answer from those sections only.
```

This catches hallucinations before they reach the final answer — if "Sources Found"
is empty but the Gem still answers confidently, the user knows it's using training data.

### Pattern 6: Verification Fence (pre-output check)

Add a self-check step before the Gem writes its response:

```
Before writing your response, verify that every factual claim, entity name,
and data point appears in the knowledge files. Remove anything that doesn't.
```

### Pattern 7: No-Match Path / Escape Hatch

Define exactly what the Gem should do when it finds nothing in the files:

```
When the query doesn't match any content in the knowledge files:
- Do NOT answer from general knowledge.
- Output: "I couldn't find information about [topic] in my reference documents."
- Suggest: "You might want to [ask differently / check if this topic is covered
  in your knowledge files / upload additional documents]."
```

Without a defined no-match path, the model's default is to satisfy the query
from any available source — which means training data hallucination.

### Pattern 8: Explicit Source Blocking

The most aggressive approach — directly block non-file sources:

```
Look in my attached documents to find information that satisfies the query.
Do NOT use your training knowledge, the Internet, or any other source.
```

### Combining Patterns by Focus Level

| Focus Level | Recommended Patterns |
|-------------|---------------------|
| Knowledge-Only | Grounding Directive + Strict Mode + Verification Fence + No-Match Path |
| Knowledge-First | Grounding Directive + Source of Truth First + Visible Receipt (optional) |
| Balanced | Grounding Directive + citation requirement |
| Training-Primary | No special grounding needed |

### Gems cannot be architecturally restricted to knowledge files

Unlike NotebookLM, which is designed to respond only from uploaded sources, Gems can
access web search, training data, and knowledge files simultaneously. No instruction
can fully replicate NotebookLM's architectural grounding guarantee. The patterns above
are the strongest available levers, not absolute locks.

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

### Temperature is fixed at 1.0
Gemini Gems run at a fixed temperature of 1.0. Unlike other AI platforms, lowering
the temperature in Gemini causes looping and quality degradation rather than more
deterministic output. Do not attempt to override this — instead, use instruction
specificity and output format constraints to control consistency.

---

## Sharing and Security

- When you share a Gem, recipients can see your instruction text and knowledge file
  names (though file contents require separate sharing approval).
- Never embed passwords, API keys, proprietary processes, or sensitive data in the
  instructions or file names of a Gem you intend to share.
- If you need to share a Gem with sensitive instructions, consider creating a
  "public" version with sanitized instructions and keeping a separate "internal"
  version with full detail.

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
- **CRITICAL: Click "Update" after editing knowledge files.** When modifying an existing
  Gem's files, you must click the blue "Update" button. Without this, changes are not
  saved and the Gem reverts to its previous state. This is the single most reported
  cause of "my Gem forgot my documents."
- Known regression (January 2026): Multiple users reported Gems stopped referencing
  knowledge base files entirely. If a Gem suddenly ignores its files, try: (1) remove
  and re-add the files, (2) click Update, (3) test in a new chat session. If the
  problem persists, it may be a platform-side issue — check the Google Gemini community
  forum for current status.
