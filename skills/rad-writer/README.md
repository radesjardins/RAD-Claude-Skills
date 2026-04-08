# RAD Writer — Claude.ai Skill

Domain-smart writing, AI pattern avoidance, voice profiling, and editorial review across 9 content types. Adapted from the [rad-writer plugin](../../plugins/rad-writer/) for Claude.ai.

## What's Included

Import `dist/rad-writer-complete.zip` via **Settings > Customize > Skills** on Claude.ai.

The skill includes a SKILL.md with 5 modes (write, improve, review, AI audit, voice analysis) plus 13 resource files:

- AI writing patterns framework (structural detection, not cosmetic)
- Word blocklist (275+ lexical tells by severity)
- Sentence craft guide (burstiness, transitions, paragraph techniques)
- Voice profile schema (for learning and matching your writing style)
- 9 domain guides: email, blog, web copy, business report, research/academic, presentation, prose/essay, technical docs, social media

## How to Import

**As a Skill (recommended):** Settings > Customize > Skills > upload `rad-writer-complete.zip`. Activates automatically in any conversation.

**As Project Knowledge:** Add the `.md` files to a Claude.ai Project for project-scoped use.

**As a conversation attachment:** Attach `SKILL.md` to any conversation for one-off use.

## Example Prompts

- "Write me a cold outreach email to [person]"
- "Draft a blog post about [topic]"
- "Improve this — it sounds too robotic" [paste text]
- "Review this writing and tell me what to fix"
- "Does this sound like AI?" [paste text]
- "Analyze my writing voice" [paste 3-5 samples]
- "Create web copy for my landing page"
- "Write a LinkedIn post about [topic]"

## How It Works

- **9 writing domains**: Each with deep convention knowledge, anti-patterns, and domain-specific AI tells
- **AI avoidance baked in**: 275+ lexical tells tracked, burstiness scoring, structural analysis — avoidance is structural during generation, not cosmetic post-processing
- **Voice profiles**: Provide 3-5 writing samples → get a downloadable voice profile artifact. Upload to a Project for persistent voice matching, or attach to any conversation.
- **Three-pass review**: Structure & flow → sentence & word craft → AI pattern scan. Deduplicated, severity-ranked findings.
- **Tracked changes**: Every improvement is numbered. Accept all, review individually, or cherry-pick by number.
- **Not an AI detector**: The AI audit reports patterns with fixes, not verdicts. Every "AI tell" is also a craft problem — fix the writing quality, detectability solves itself.
