# RAD Writer — Claude.ai Skills

Domain-smart writing, AI pattern avoidance, voice profiling, and editorial review across 9 content types. Adapted from the [rad-writer plugin](../../plugins/rad-writer/) for Claude.ai.

## Two Options

### Option A: Complete Suite (recommended)

One skill with everything. Import `dist/rad-writer-complete.zip` via **Settings > Customize > Skills**.

Includes the full SKILL.md (write, improve, review, AI audit, voice analysis) plus 13 resource files: AI pattern detection framework, word blocklist (275+ tells), sentence craft guide, voice profile schema, and 9 deep domain guides.

### Option B: Modular Skills

Import only the modes you need. Each is a separate ZIP in `dist/`:

| ZIP File | What It Does | Use When You Want To... |
|----------|-------------|------------------------|
| `rad-writer-write.zip` | Domain-smart drafting with AI avoidance | Write something from scratch |
| `rad-writer-improve.zip` | Tracked changes with accept/reject | Polish existing text |
| `rad-writer-review.zip` | Scored diagnostic with three-pass option | Get feedback on your writing |
| `rad-writer-ai-audit.zip` | Pattern-by-pattern AI diagnostic | Check if text sounds like AI |

Modular skills detect each other and offer natural transitions (write → review → improve → audit).

## How to Import

**As a Skill (recommended):** Go to **Settings > Customize > Skills** on Claude.ai. Upload the `.zip` file(s).

**As Project Knowledge:** Create a Claude.ai Project, add the `.md` file(s) directly.

**As a conversation attachment:** Attach the `.md` file to any conversation for one-off use.

## Example Prompts

### Writing
- "Write me a cold outreach email to [person]"
- "Draft a blog post about [topic]"
- "Create web copy for my landing page"
- "Write a LinkedIn post about [topic]"
- "Draft a technical README for this project"

### Improving
- "Improve this email" [paste text]
- "Make this blog post better"
- "Polish this — it sounds too robotic"
- "Tighten up this report"

### Reviewing
- "Review this writing and tell me what to fix"
- "Give me feedback on this essay"
- "How's my writing?"
- "Do a thorough review of this document"

### AI Auditing
- "Does this sound like AI?"
- "Check this for AI patterns"
- "Run an AI audit on this draft"
- "How can I make this sound more human?"

### Voice Profiling
- "Analyze my writing voice" [paste 3-5 samples]
- "Learn my writing style from these samples"
- "Create a voice profile for my blog writing"

## How It Works

- **9 writing domains:** Email, blog, web copy, business report, research/academic, presentation, prose/essay, technical docs, social media — each with deep convention knowledge
- **AI avoidance baked in:** 275+ lexical tells tracked, burstiness scoring, structural analysis. Avoidance is structural during generation, not cosmetic post-processing.
- **Voice profiles:** Provide 3-5 writing samples → get a downloadable voice profile. Upload to a Project for persistent voice matching, or attach to any conversation.
- **Three-pass review:** Structure & flow → sentence & word craft → AI pattern scan. Deduplicated, severity-ranked findings.
- **Tracked changes:** Every improvement is numbered. Accept all, review individually, or cherry-pick by number.
