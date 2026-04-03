# rad-gem-creator

Guided workflow for building Google Gemini Gems. Walks you through an interview process and produces ready-to-paste instruction sets aligned to Google's best practices.

## What It Does

- Conducts a structured interview to understand your Gem's purpose and audience
- Generates knowledge base preparation checklists and file recommendations
- Configures source focus levels (Knowledge-Only through Training-Primary)
- Applies anti-hallucination instruction patterns
- Assembles step-by-step Gem instructions with revision caps
- Delivers output as both a code block and downloadable `.md` file

## How to Trigger

Say any of:
- "Create a Gem"
- "Gemini assistant"
- "Build a Gem"
- "Gem instructions"
- "Custom Gemini"

Or ask naturally:
- "I want to create a Gemini Gem for my company's knowledge base"
- "Help me build a Gem that answers questions about our product docs"
- "Make me a Gem for code review in Python"

## What You Get

A complete Gem instruction set including:
- System instructions ready to paste into Google AI Studio
- Knowledge base file list with preparation guidance
- Conversation starters
- Test cases to validate behavior

## Installation

```bash
mkdir -p ~/.claude/skills
cp -r skills/rad-gem-creator ~/.claude/skills/
```

## License

Apache-2.0
