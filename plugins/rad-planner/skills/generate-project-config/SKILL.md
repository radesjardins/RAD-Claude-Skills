---
name: generate-project-config
description: >
  This skill should be used when the user says "generate CLAUDE.md", "create project
  config", "setup project files", "generate project configuration", "create CLAUDE.md
  from plan", "write my CLAUDE.md", "setup project for AI coding", "generate architecture
  docs", or wants to create the persistent reference files (CLAUDE.md, ARCHITECTURE.md,
  etc.) that execution agents need after an implementation plan has been approved.
argument-hint: "[path to approved plan] [--output-dir path]"
user-invocable: true
allowed-tools: Read Glob Grep Write
---

# Generate Project Config — Persistent Reference File Generation

Generate the project-level configuration files that execution agents need to work effectively. These files persist across sessions and provide the "constitution" that keeps AI agents aligned with the project's architecture and conventions.

**Prerequisite:** An approved implementation plan should exist. If no plan exists, recommend running `/rad-planner:plan-project` first.

## What Gets Generated

### 1. CLAUDE.md (Required)

Load `references/claude-md-template.md` for the WHY/WHAT/HOW structure.

Generate a CLAUDE.md that:
- Stays under 200 lines
- Includes only information the AI cannot infer from the codebase
- Uses progressive disclosure (links to external docs, not inline content)
- Contains specific, verifiable rules (not vague platitudes)
- Lists essential commands the AI would need to guess otherwise

**Extract from the approved plan:**
- Tech stack and version pins
- Architecture decisions and key patterns
- Coding conventions and constraints
- Test commands and coverage requirements
- Branch naming and commit conventions

### 2. ARCHITECTURE.md (Recommended for multi-component projects)

Generate an architecture document that includes:
- Component diagram (Mermaid syntax)
- Data flow descriptions
- System boundaries and interfaces
- Key design decisions with rationale
- Integration points with external services

### 3. tasks.md (If not already generated)

Export the plan's task list in machine-readable format:
- Hierarchical task IDs
- Dependency arrays
- Task states with checkboxes
- Validation criteria per task

### 4. Path-Scoped Rules (Optional, for large projects)

If the project has distinct domains (frontend/backend/database), generate `.claude/rules/*.md` files:

```yaml
---
description: [Domain] conventions
paths: "src/[domain]/**/*"
---
[Domain-specific rules]
```

These load only when Claude works on matching files, saving context in other situations.

## Workflow

### Step 1: Read the Approved Plan

Read the implementation plan and extract:
- Project name and description
- Tech stack details
- Architecture and component structure
- Coding conventions mentioned in the plan
- Test strategy and commands
- File structure (target files section)

### Step 2: Check Existing Config

Look for existing project configuration:
- CLAUDE.md — merge with existing content, don't overwrite
- .claude/rules/ — check for existing rules
- README.md — extract stack/convention info
- package.json — extract scripts and dependencies
- tsconfig.json — extract TypeScript configuration

### Step 3: Generate Files

Generate each file following its template. For each file:
1. Show the user a preview of what will be generated
2. Explain key decisions (what was included and why, what was excluded and why)
3. Get confirmation before writing

### Step 4: Token-Saving Audit

After generation, review the CLAUDE.md against the exclusion checklist:
- Remove any standard language conventions (AI knows them)
- Remove file-by-file descriptions (AI can search)
- Remove linter-enforced rules (delegate to tooling)
- Remove vague platitudes ("write clean code")
- Test each line: "If I remove this, will the AI make a mistake?"

Report the final line count. If over 200 lines, flag the excess and suggest what to move to reference files.

## Output

Files are written to the project root (or `--output-dir` if specified):
- `CLAUDE.md` — Primary project configuration
- `docs/ARCHITECTURE.md` — Architecture documentation (if applicable)
- `tasks.md` — Machine-readable task list (if not already present)
- `.claude/rules/*.md` — Path-scoped rules (if large project)

## Key Reference

Load `references/claude-md-template.md` for the complete generation template with structure, formatting rules, and token-saving exclusions.
