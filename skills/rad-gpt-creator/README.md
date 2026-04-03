# rad-gpt-creator

Guided workflow for building OpenAI Custom GPTs. Conducts a structured interview and produces production-ready instructions that respect the 8,000-character instruction limit.

## What It Does

- Walks through a guided interview to define your GPT's purpose, audience, and behavior
- Manages the 8,000-character instruction limit with real-time tracking
- Configures knowledge base design (20 files max, 512 MB each)
- Sets up capabilities and Actions (web search, code interpreter, DALL-E, Canvas)
- Applies anti-hallucination patterns and source focus levels
- Delivers production-ready GPT with test cases and conversation starters

## How to Trigger

Say any of:
- "Create a GPT"
- "Custom GPT"
- "Build a GPT"
- "GPT instructions"
- "Configure my GPT"

Or ask naturally:
- "I need a Custom GPT that helps my team write SQL queries"
- "Build me a GPT for onboarding new employees"
- "Help me create a GPT that uses our API docs as a knowledge base"

## What You Get

A complete Custom GPT configuration including:
- Instructions (within the 8,000-character limit)
- Knowledge base file recommendations
- Capability settings
- Conversation starters
- Test cases to validate behavior

## Installation

```bash
mkdir -p ~/.claude/skills
cp -r skills/rad-gpt-creator ~/.claude/skills/
```

## License

Apache-2.0
