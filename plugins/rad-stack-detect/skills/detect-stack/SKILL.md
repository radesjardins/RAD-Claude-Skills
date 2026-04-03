---
name: detect-stack
description: >
  User-invoked skill to scan the current project and detect its tech stack, then map
  technologies to installed rad-* plugins. Creates a lightweight stack profile for the
  session. Trigger when the user says "/detect-stack", "what stack is this",
  "detect my tech stack", "what technologies does this project use",
  "which skills apply here", "which plugins should I use", "scan my project",
  "set up my project for development", "what frameworks am I using".
argument-hint: "[--update to refresh an existing profile]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - Edit
---

# Stack Detection

Scan the current project to detect its technology stack, map it to installed rad-* plugins, and create a lightweight stack profile.

**Announce at start:** "Scanning your project to detect the tech stack and map it to available skills..."

---

## Phase 1: Scan the Project

### 1.1 Read package.json

Read `package.json` from the project root. Extract:
- `name` (project name)
- `dependencies` (runtime dependencies)
- `devDependencies` (development dependencies)

If no `package.json` exists, note this and continue with file-based detection only.

### 1.2 Check for Configuration Files

Use Glob to check for these files in the project root:

```
astro.config.*
next.config.*
tailwind.config.*
tsconfig.json
wxt.config.*
Dockerfile
docker-compose.*
compose.*
```

### 1.3 Check for Chrome Extension Manifest

If `manifest.json` exists in the project root (or common extension paths like `src/manifest.json`, `extension/manifest.json`), read it and check for the `manifest_version` field. Only classify as Chrome Extension if `manifest_version` is present.

### 1.4 Check for UI Components

Use Glob to check if the project contains `.tsx`, `.jsx`, or `.astro` files:
```
**/*.tsx
**/*.jsx
**/*.astro
```
If any exist, the project has UI components (relevant for accessibility).

### 1.5 Compile Technology List

Using the detection rules in `references/technology-map.md`, compile a list of detected technologies. For each, note:
- Technology name
- Version (from package.json if available)
- How it was detected (config file, dependency, etc.)

### 1.6 Classify Project Type

Based on detected technologies, classify the project type:
- **Website** — Astro with no API server
- **Web Application** — Next.js, or React + Vite
- **Single Page Application** — React + Vite (no Astro/Next)
- **API Server** — Fastify with no frontend framework
- **Full-Stack Application** — Fastify + any frontend framework
- **Browser Extension** — Chrome Extension manifest or WXT
- **Desktop Application** — Electron

---

## Phase 2: Map Technologies to Plugins

Using `references/technology-map.md`, map each detected technology to:
1. The relevant rad-* plugin
2. The tier (Core, Supporting, or Pre-Ship)
3. The key development skills
4. The review agent (if one exists)

### Tier Assignment Rules

- **Core plugins** — The project's primary framework/platform (e.g., rad-astro for an Astro site, rad-fastify for an API)
- **Supporting plugins** — Technologies used broadly across the project (rad-typescript, rad-tailwind, rad-a11y)
- **Pre-Ship plugins** — Review-only plugins relevant to the project type (rad-seo-optimizer for websites, rad-a11y for UI projects)

---

## Phase 3: Check for Existing Profile

Read `.claude/stack-profile.local.md` if it exists. If found:
- Compare the existing profile to the new detection results
- Note any changes (new technologies added, versions changed, technologies removed)
- If the user passed `--update`, proceed to overwrite
- Otherwise, show the diff and ask if they want to update

---

## Phase 4: Write Stack Profile

Create (or update) `.claude/stack-profile.local.md`.

First, ensure the `.claude/` directory exists. If `.gitignore` exists, check if `*.local.md` is already ignored. If not, suggest the user add `.claude/*.local.md` to `.gitignore`.

**File format:**

```markdown
---
detected: YYYY-MM-DD
project_name: [from package.json name or directory name]
project_type: [classified type]
technologies:
  - name: [tech]
    version: "[version or 'detected']"
    source: "[detection method]"
plugins:
  core:
    - [plugin-name]
  supporting:
    - [plugin-name]
  pre_ship:
    - [plugin-name]
review_agents:
  - name: [agent-name]
    subagent_type: "[full subagent type string]"
---

# Stack Profile: [project name]

## Detected Technologies
- **[Tech Name] [version]** — [one-line description of what it is] (detected via [source])

## Plugin Guide

### Core — Use During Development
These plugins match your project's primary technologies. Their skills should be consulted when writing code.

- **[plugin-name]** — [what it helps with]. Key skills: [list 2-3 most relevant skills]

### Supporting — Use When Relevant
These plugins apply broadly. Consult them when touching related code.

- **[plugin-name]** — [what it helps with]. Key skills: [list 1-2 most relevant skills]

### Pre-Ship — Run Before Deploying
These review agents will be dispatched when you run `/review-for-ship`.

- **[agent-name]** — [what it checks for]

## Quick Reference for CLAUDE.md

Add this to your project's CLAUDE.md so every session knows your stack:

    ## Tech Stack
    This project uses [comma-separated tech list].
    Stack profile: .claude/stack-profile.local.md
    Apply best practices from: [comma-separated plugin list]
    Before shipping, run: /review-for-ship
```

---

## Phase 5: Report to User

Display a clear, friendly summary. Keep it educational — explain what each technology is and why each plugin matters. Use this structure:

### Output Format

```
## Stack Detected!

**Project:** [name]
**Type:** [project type]

### Technologies Found
[Table or bullet list of technologies with versions]

### Skills That Apply to This Project

**Core (always active):**
- rad-[name] — [one-sentence explanation of what it ensures]

**Supporting (when relevant):**
- rad-[name] — [one-sentence explanation]

**Pre-Ship Review:**
- [agent-name] — [what it checks]

### What This Means
[2-3 sentences explaining how this changes the development experience.
Example: "When you ask me to build a component, I'll automatically apply
Astro island architecture patterns, React best practices, Tailwind utility
conventions, and TypeScript strict-mode standards. Before you ship, run
/review-for-ship to get a comprehensive audit from all relevant reviewers."]

### Next Step
I've saved this profile to `.claude/stack-profile.local.md`.

To make this persistent across sessions, add this to your project's `CLAUDE.md`:
[show the snippet from the profile]
```

---

## Edge Cases

- **Monorepo with multiple packages:** If the project has a `packages/` or `apps/` directory with multiple `package.json` files, scan each and note which technologies exist in which package. Create a single profile noting the full stack.
- **No package.json:** Rely entirely on file-based detection. Note that the profile may be incomplete.
- **Preact vs React:** If Preact is detected but React is not, note that `rad-react` skills *partially* apply (component patterns and JSX are similar, but hooks and server components differ).
- **Empty or new project:** If no technologies are detected, say so and suggest the user come back after they've set up their project.
