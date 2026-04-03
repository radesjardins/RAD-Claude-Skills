# rad-stack-detect

Detects your project's tech stack and maps it to installed rad-* plugins. Creates a lightweight stack profile so the right best-practice skills activate during development and the right review agents run before shipping.

## What's Inside

| Component | Count |
|-----------|-------|
| Skills | 2 |
| Agents | 0 (dispatches agents from other rad-* plugins dynamically) |

## Skills

| Skill | Trigger Phrases | What It Does |
|-------|----------------|--------------|
| `detect-stack` | "what stack is this", "detect my tech stack", "which plugins should I use", "scan my project" | Scans package.json, config files, and file types to identify technologies, classifies project type, maps to relevant rad-* plugins, and writes `.claude/stack-profile.local.md` |
| `review-for-ship` | "review before shipping", "is this ready to deploy", "pre-ship review", "production readiness check" | Reads the stack profile and dispatches all relevant review agents in parallel (Astro, Next.js, React, TypeScript, Fastify, a11y, Chrome Extension, SEO) for comprehensive pre-deployment review |

## How It Works

1. **Detect** — Run `detect-stack` to scan your project and generate a stack profile
2. **Develop** — The stack profile tells Claude which rad-* skills apply to your project
3. **Ship** — Run `review-for-ship` to dispatch all relevant reviewer agents at once

## Installation

```bash
claude plugins add ./plugins/rad-stack-detect
```

## Requirements

- Claude Code CLI installed and authenticated
- Other rad-* plugins installed for the review agents to work (rad-react, rad-typescript, rad-a11y, etc.)

## License

Apache-2.0
