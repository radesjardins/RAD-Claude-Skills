# rad-context-prompter

Prompt engineering skill that transforms rough ideas into production-ready prompts optimized for specific AI platforms — Claude, GPT, Gemini, Midjourney, and more.

## What It Does

- **Fast mode** for simple prompts — quick generation with minimal back-and-forth
- **Design mode** for complex systems — extracts intent across 9 dimensions before writing
- Applies platform-specific syntax, behavioral patterns, and token optimization
- Prevents AI fabrication with techniques like mixture of experts and chain-of-thought
- Supports system prompts, tool descriptions, agentic workflows, and cross-model migration
- Delivers token-efficient output with zero wasted context

## How to Trigger

Say any of:
- "Write a prompt"
- "Prompt engineering"
- "System prompt"
- "Optimize my prompt"
- "Context engineering"
- "Create a prompt for..."

Or ask naturally:
- "Write me a system prompt for a customer support agent"
- "Optimize this prompt for Claude"
- "Help me migrate this GPT prompt to Gemini"
- "I need a prompt that prevents hallucination for medical content"

## What You Get

A production-ready prompt document including:
- Platform-optimized system prompt or user prompt
- Anti-hallucination patterns where appropriate
- Token usage analysis
- Test cases for validation

## Installation

```bash
mkdir -p ~/.claude/skills
cp -r skills/rad-context-prompter ~/.claude/skills/
```

## License

Apache-2.0
