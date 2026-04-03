# rad-brainstorming

Collaborative ideation skill that transforms rough ideas into fully-formed designs and specifications before any code is written. Enforces a "design first, build second" discipline.

## What It Does

- Explores project context and asks focused clarifying questions (one at a time)
- Proposes 2-3 different approaches with trade-offs and a recommendation
- Presents the design incrementally, getting approval at each section
- Writes a formal design spec document to `docs/superpowers/specs/`
- Runs an automated spec self-review for placeholders, contradictions, and ambiguity
- Hard-gates implementation until the design is approved

## How to Trigger

Say any of:
- "Let's brainstorm"
- "I need ideas"
- "Help me design this"
- "What should I build?"
- "How should I approach this?"

Or ask naturally:
- "I want to add a notification system but I'm not sure how to architect it"
- "Help me think through the data model for this feature"
- "What are some approaches for handling real-time updates?"

## What You Get

A written design spec saved as a markdown file with:
- Architecture decisions and component breakdown
- Data flow and error handling strategy
- Testing approach
- Trade-offs considered and rationale for the chosen approach

The skill then transitions to implementation planning via the `writing-plans` skill.

## Installation

```bash
mkdir -p ~/.claude/skills
cp -r skills/rad-brainstorming ~/.claude/skills/
```

## License

Apache-2.0
