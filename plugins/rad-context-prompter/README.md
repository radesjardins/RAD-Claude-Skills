# rad-context-prompter — Write, debug, and optimize prompts for 30+ AI platforms. No guessing.

Different AI models need different prompting strategies — what works for Claude degrades output on o3, and vice versa. rad-context-prompter maps your task type to the right technique for the right model, diagnoses why a prompt is failing with a coded taxonomy, and can reverse-engineer existing prompts to translate them across platforms.

## Features

- **Systematic tool-specific routing** across 30+ platforms (Claude, GPT, Gemini, o3, Midjourney, Stable Diffusion, Cursor, Claude Code, n8n, and more)
- **35 anti-pattern diagnostic reference** covering task, context, format, scope, reasoning, and agentic failures
- **12 technique selection matrix** mapping task types to optimal prompt engineering techniques
- **Hard rules** preventing token waste (e.g., CoT on reasoning-native models degrades output)
- **Prompt decompiler** for reverse-engineering existing prompts — structural analysis, technique identification, cross-platform translation, compression
- **Prompt debugger agent** for autonomous failure diagnosis with coded taxonomy (F1-F7), root cause analysis, and targeted before/after fixes

## Components

| Type | Name | Purpose |
|------|------|---------|
| Skill | `prompt-engineering` | Core prompt writing, system prompt design, technique selection, tool routing |
| Skill | `prompt-decompiler` | Reverse-engineer, analyze, translate, compress, and split existing prompts |
| Agent | `prompt-debugger` | Diagnose why a prompt failed and suggest minimal targeted fixes |

## Skills

### prompt-engineering

The core skill. Triggers on: "write a prompt", "prompt engineering", "system prompt", "optimize my prompt", "CLAUDE.md", "few-shot examples", "context engineering".

Two modes:
- **Fast mode**: Clear task + known tool → immediate prompt output
- **Design mode**: System prompts, agentic architectures, production pipelines → consultative workflow

Includes 6 reference files: techniques (12 sections), patterns (35 anti-patterns + 12 structural patterns), templates (13 templates A-M), tool routing (30+ platforms), context engineering, and evaluation checklist.

### prompt-decompiler

Advanced prompt reverse-engineering. Triggers on: "decompile this prompt", "analyze this prompt", "adapt this prompt for", "why does this prompt work", "convert this prompt".

Six analysis modes:
- **Anatomize**: Structural fingerprint + component map + technique identification + weakness map
- **Translate**: Cross-platform adaptation with translation notes
- **Compress**: Token audit and optimization with before/after diff
- **Decompose**: Split complex prompts into sequential chains
- **Forensics**: Technique-by-technique effectiveness analysis with scoring
- **Diagnose**: Weakness identification (also see prompt-debugger agent for deep analysis)

## Agent

### prompt-debugger

Autonomous prompt failure analyst. Triggers on: "my prompt isn't working", "debug this prompt", "getting hallucinations", "model keeps ignoring my instructions".

Diagnostic framework:
- **7-category failure taxonomy** (F1-F7) with 35 specific failure patterns
- **Root cause analysis** tracing symptom → mechanism → fix
- **Targeted fixes** with BEFORE/AFTER/WHY format
- **Verification step** checking Golden Rule, intent preservation, platform compatibility

## Installation

```bash
claude plugins:add /path/to/rad-context-prompter
```

Or add to your marketplace configuration.

## License

Apache-2.0
