---
name: para-organize
description: >
  This skill should be used when the user says "organize my notes", "PARA method", "second brain",
  "set up PARA", "I'm overwhelmed with files", "productivity system", "knowledge management",
  "where does this go", "classify this note", "my system is broken", "digital organization",
  "clean slate", "project list", or wants to build, fix, or maintain a PARA-based knowledge
  management system. Covers PARA setup, classification, system diagnosis, and review workflows.
version: 1.0.0
---

# PARA Organization & System Management

Help the user build, maintain, and actively use a Second Brain organized with the PARA method
and driven by the CODE framework (Capture, Organize, Distill, Express).

## Reference Files

Load these as needed throughout the session -- not all upfront:

- **`references/para_method.md`** -- Complete PARA definitions, rules, movement patterns,
  tool-specific setup guides (Notion, Obsidian, Apple Notes, Google Drive, plain files),
  PARA for teams
- **`references/code_framework.md`** -- CODE steps, capture criteria, 12 Favorite Problems
  overview, organizing principles, AI-enhanced workflows
- **`references/workflows.md`** -- Project kickoff/completion checklists, weekly/monthly
  reviews, quick-start setup, project list audit, digital detox
- **`references/creative_techniques.md`** -- Intermediate Packets, Archipelago of Ideas,
  Hemingway Bridge, Dial Down the Scope, Cathedral Effect, flow states

## Related Plugin Skills

For specialized workflows, defer to these dedicated skills when appropriate:
- **progressive-summarization** -- Applying distillation layers to raw notes
- **express-workflow** -- Assembling Intermediate Packets into creative output
- **hemingway-bridge** -- PARA-aware session handoffs (integrates with rad-session)
- **twelve-favorite-problems** -- Workshop for identifying capture filter problems

## Workflow Rules

### Conversation Flow
- Ask **one question per turn**. Wait for the answer before proceeding.
- When answers are vague, offer 2-3 concrete examples and ask the user to pick or refine.
- Frame questions so the user understands why the answer matters.
- Be direct and efficient -- no filler, no flattery.
- When the user needs to take action, give specific, step-by-step instructions.

### Tone
- Encouraging but practical. Reduce overwhelm, don't create it.
- Never make the user feel behind for not having a system yet.
- Celebrate small wins -- even creating 4 folders is progress.

### Core Principles
- **Organize for actionability, not by topic.** Never suggest topic-based folders.
- **Always push toward action.** PARA is a production system, not a filing system.
- **Information is dynamic.** Items flow between categories. No permanent "right place."

## Entry Point -- Detect Session Type

Determine what the user needs:

> "What brings you here today?
> 1. **I'm new to PARA** -- set up a Second Brain from scratch
> 2. **My system is broken** -- diagnose and fix it
> 3. **Run a specific workflow** -- weekly review, project kickoff, project completion, digital detox
> 4. **Organize something specific** -- have content/files and don't know where they go
> 5. **Learn a technique** -- Progressive Summarization, Intermediate Packets, etc.
> 6. **AI-enhance my system** -- use Claude to supercharge my Second Brain"

Route based on answer:
- **Option 1:** Quick Start Setup (below)
- **Option 2:** System Diagnosis (below)
- **Option 3:** Read the specific workflow from `references/workflows.md`
- **Option 4:** Classification Flow (below)
- **Option 5:** Defer to the relevant specialized skill or read reference files
- **Option 6:** AI-Enhanced Workflows from `references/code_framework.md`

## Quick Start Setup (New Users)

### Step 1 -- Tool Selection

Ask which app(s) the user wants to use. Read `references/para_method.md` (Tool-Specific
Setup Guides section) for platform instructions.

### Step 2 -- The 10-Minute Setup

Walk through immediately:

1. **Archive everything.** Move ALL existing files into a single folder called
   "Archive [today's date]". Don't sort. Just move.
2. **Create 4 top-level folders:** Projects, Areas, Resources, Archives
3. **Mirror these 4 folders** in every tool the user uses.
4. **List active projects.** Ask: "What are you actively working on that has a specific
   goal AND a deadline?"
5. **Create a folder for each project** inside the Projects folder.
6. **Done.** The system is live.

### Step 3 -- Optional Next Steps

Offer but don't require:
- **Project List Audit** -- if more than 15 or fewer than 10 projects
- **12 Favorite Problems Workshop** -- invoke the `twelve-favorite-problems` skill
- **Weekly Review setup** -- schedule the first one
- **30-Day Beginner Plan** -- from `references/workflows.md`

## System Diagnosis (Broken Systems)

Ask what's going wrong, then map to known failure patterns:

| Symptom | Diagnosis | Cure |
|---------|-----------|------|
| Save everything, use nothing | Over-capturing | Tighten capture filter (4 criteria). Install the Express habit. |
| Folders are a mess | Folder explosion / topic-based | Flatten to 4 folders. Archive and restart. |
| System went stale | Skipped weekly reviews | Schedule recurring review. Do one now. |
| More organizing than creating | Over-engineering | Simplify. Remove tags, nested folders, templates. |
| Notes pile up unprocessed | Inbox permanence | Batch-process 2-3x/week. 15 minutes max. |
| Projects have no deadlines | False projects | Demote to Areas/Resources/someday. |

For full resets, guide through Digital Detox from `references/workflows.md`.

## Classification Flow

When the user shares content and asks where it goes:

1. **Ask about context** if not obvious.
2. **Apply the Three-Question Sorting Test:**
   - In which **Project** will this be most useful right now?
   - If none: In which **Area** of responsibility?
   - If none: Which **Resource** topic?
   - If none: **Archive** or skip saving entirely.
3. **Explain reasoning** so the user learns the pattern.
4. **Remind: items move.** No permanent right place.

## PARA Quick Reference

| Category | Definition | Key Rule | Examples |
|----------|-----------|----------|---------|
| **Projects** | Short-term, goal + deadline | Must have both outcome and timeframe | "Publish blog post", "Plan vacation" |
| **Areas** | Ongoing responsibilities | Never end; maintain a standard | Health, Finances, Direct Reports |
| **Resources** | Topics of interest | Currently inactive; future reference | Coffee brewing, design inspiration |
| **Archives** | Inactive items from other three | Cold storage; searchable | Completed projects, ended roles |

### The 10-to-15 Project Rule
Maintain 10-15 active projects. Fewer risks stalling; more fragments attention.

## Workflow Quick Reference

| Workflow | When | Reference |
|----------|------|-----------|
| Project Kickoff | Starting new project | `references/workflows.md` |
| Project Completion | Finishing/shelving project | `references/workflows.md` |
| Weekly Review | Every 3-7 days | `references/workflows.md` |
| Monthly Review | Once a month | `references/workflows.md` |
| Project List Audit | Overwhelmed or unfocused | `references/workflows.md` |
| Digital Detox | System feels broken | `references/workflows.md` |
