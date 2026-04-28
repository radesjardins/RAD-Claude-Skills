---
name: detect-stack
description: >
  User-invoked skill to scan the current project, detect its tech stack, map technologies
  to installed rad-* plugins, identify missing plugins, inject stack-aware guidance into
  CLAUDE.md, and generate team settings. Trigger when the user says "/detect-stack",
  "what stack is this", "detect my tech stack", "what technologies does this project use",
  "which skills apply here", "which plugins should I use", "scan my project",
  "set up my project for development", "what frameworks am I using", "configure my stack",
  "stack guide", "set up stack guidance".
  Also suggest proactively when starting work in a project that has no
  .claude/stack-profile.local.md but does have package.json or framework config files.
argument-hint: "[--update] [--skip-claude-md] [--skip-settings]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - Edit
  - AskUserQuestion
---

# Stack Detection & Configuration

Scan the current project to detect its technology stack, map it to installed rad-* plugins, identify gaps, configure stack-aware development guidance, and generate team settings.

**Announce at start:** "Scanning your project to detect the tech stack, configure guidance, and map to available skills..."

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
2. The tier (Core, Supporting, Pre-Ship, or Final Gate)
3. The key development skills
4. The review agent (if one exists)

### Tier Assignment Rules

- **Core plugins** — The project's primary framework/platform (e.g., rad-astro for an Astro site, rad-fastify for an API)
- **Supporting plugins** — Technologies used broadly across the project (rad-typescript, rad-zod, rad-a11y)
- **Pre-Ship plugins** — Review-only plugins relevant to the project type (rad-seo-optimizer for websites, rad-a11y for UI projects)
- **Final Gate** — rad-code-review always runs as the last reviewer in `/review-for-ship`

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
  final_gate:
    - rad-code-review
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

### Final Gate
After all specialist reviewers complete, rad-code-review runs as the generalist final gate covering AI slop detection, architecture, release readiness, and general security.
```

---

## Phase 4.5: Gap Analysis

After writing the profile, check which rad-* plugins from the profile are actually available in this environment. For each plugin listed in `plugins.core`, `plugins.supporting`, and `plugins.pre_ship`:

1. Use Glob to search for skill files belonging to each plugin. Heuristics:
   - For marketplace plugins: check if a skill with a name matching the plugin exists in the available skills list
   - Quick check: attempt to find any file path containing the plugin name in a known skills/plugins directory

2. Classify each plugin as **Installed** or **Not Installed**.

3. Display the gap report:

```
## Plugin Status

### Installed
✓ rad-react — React best practices, hooks rules, accessibility, security
✓ rad-typescript — Strict mode, type safety, API boundaries

### Recommended (Not Installed)
✗ rad-nextjs — Server Actions security, App Router patterns, middleware bypass protection
✗ rad-a11y — WCAG 2.2 AA compliance, ARIA patterns, keyboard navigation

To install missing plugins from the rad-claude-skills marketplace:
  claude plugins install rad-nextjs@rad-claude-skills
  claude plugins install rad-a11y@rad-claude-skills
```

4. If all plugins are installed: `All recommended plugins are installed. ✓`

5. If detection fails or is uncertain, skip this phase silently.

---

## Phase 4.6: CLAUDE.md Injection

Unless the user passed `--skip-claude-md`, offer to add stack-aware guidance to the project's CLAUDE.md.

### Check Current State

1. Read `CLAUDE.md` from the project root (if it exists)
2. Search for an existing `## Stack Guidance` section
3. If the section already exists, show the diff between existing and proposed content and ask if they want to update
4. If no section exists (or no CLAUDE.md), show the proposed content and ask:
   > "Want me to add stack guidance to your CLAUDE.md? This helps Claude proactively use the right skills for your stack."

### Content Template

Generate dynamically based on detected technologies. Only include routing rules for technologies that were actually detected:

```markdown
## Stack Guidance

This project uses [comma-separated tech list with versions].
Stack profile: .claude/stack-profile.local.md

### Skill Routing

When working on this project, consult these skills proactively:

- **React components** (`*.tsx`, `*.jsx` with JSX): use rad-react skills (react-foundations, react-performance, react-security)
- **Next.js patterns** (`app/` directory, Server Actions, Route Handlers): use rad-nextjs skills (nextjs-best-practices, nextjs-security)
- **TypeScript code** (`*.ts`, `*.tsx`): use rad-typescript skills (typescript-strict-mode, typescript-api-safety)
- **Fastify server code** (routes, plugins, hooks): use rad-fastify skills (fastify-best-practices, fastify-schemas-validation)
- **Astro pages and components** (`*.astro`, `src/pages/`): use rad-astro skills (astro-best-practices, astro-performance)
- **Accessibility** (any UI components, ARIA, forms, keyboard): use rad-a11y skills (a11y-semantic-html, a11y-aria-patterns)
- **Chrome Extension** (manifest, content scripts, service worker): use rad-chrome-extension skills (chrome-ext-best-practices, chrome-ext-security)
- **Zod schemas** (validation, parsing, type inference): use rad-zod skills (zod-schema-design, zod-security)

### Before Shipping

Run `/review-for-ship` for comprehensive stack-aware review with specialist reviewers + rad-code-review as final gate.
```

### Rules

- Only include routing rules for detected technologies
- Keep routing rules concise — file patterns + 2-3 key skill names
- Don't overwrite any existing content in CLAUDE.md outside the `## Stack Guidance` section
- If CLAUDE.md doesn't exist, create it with just the Stack Guidance section
- If existing CLAUDE.md has conflicting manual guidance, show both and let the user decide

---

## Phase 4.7: Team Settings Generation

Unless the user passed `--skip-settings`, offer to generate or update `.claude/settings.json` with `enabledPlugins`.

### Check Current State

1. Read `.claude/settings.json` if it exists
2. Check if `enabledPlugins` key already exists
3. If it exists, show the diff (new plugins to add)
4. If it doesn't exist, show what will be created

### Content

```json
{
  "enabledPlugins": {
    "rad-stack-guide@rad-claude-skills": true,
    "[each core plugin]@rad-claude-skills": true,
    "[each supporting plugin]@rad-claude-skills": true
  }
}
```

### Rules

- If `.claude/settings.json` already exists, **merge** the `enabledPlugins` field — preserve all other settings
- Only include plugins from the `rad-claude-skills` marketplace
- Don't include pre-ship-only plugins (they're invoked by review-for-ship dynamically)
- Ask permission before writing:
  > "Want me to generate .claude/settings.json with enabledPlugins for your team? When teammates trust this project folder, they'll be prompted to install: [list]"

---

## Phase 5: Report to User

Display a clear, friendly summary:

```
## Stack Configured!

**Project:** [name]
**Type:** [project type]

### Technologies Found
[Table or bullet list of technologies with versions]

### Skills That Apply to This Project

**Core (always active):**
- rad-[name] — [one-sentence explanation]

**Supporting (when relevant):**
- rad-[name] — [one-sentence explanation]

**Pre-Ship Review:**
- [agent-name] — [what it checks]

**Final Gate:**
- rad-code-review — AI slop detection, architecture, security, release readiness

### What's Configured
- ✓ Stack profile saved to `.claude/stack-profile.local.md`
- ✓ / ✗ CLAUDE.md updated with skill routing rules
- ✓ / ✗ Team settings generated at `.claude/settings.json`
- [If gaps:] ⚠ [N] recommended plugins not installed (install commands above)

### What This Means
[2-3 sentences explaining how this changes the development experience.]
```

---

## Edge Cases

- **Monorepo with multiple packages:** Scan each `package.json` in `packages/` or `apps/` directories. Create a single profile noting the full stack across all packages.
- **No package.json:** Rely entirely on file-based detection. Note that the profile may be incomplete.
- **Preact vs React:** If Preact is detected but React is not, note that `rad-react` skills *partially* apply (component patterns and JSX similar, hooks and server components differ).
- **Empty or new project:** If no technologies are detected, say so and suggest the user come back after setup.
- **CLAUDE.md has conflicting content:** Show both existing and proposed, let the user decide.
- **settings.json has custom config:** Preserve all existing settings when merging enabledPlugins.
