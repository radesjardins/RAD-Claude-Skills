# rad-stack-guide Design Spec

**Date:** 2026-04-05
**Status:** Approved
**Scope:** In-place rename and enhancement of rad-stack-detect → rad-stack-guide

---

## Summary

Transform `rad-stack-detect` from a passive detection utility into the entry point and orchestration hub for the entire rad development stack ecosystem. Three-phase lifecycle: Detect & Equip → Guide During Development → Review Before Shipping.

## Goals

1. Auto-detect project stack and identify missing plugins (gap analysis)
2. Write stack-aware guidance into CLAUDE.md so Claude proactively uses the right skills
3. Generate `.claude/settings.json` enabledPlugins for team propagation
4. Integrate rad-code-review v2.0 as the final-gate generalist layer in `/review-for-ship`
5. Add SessionStart hook to prompt detection on new projects
6. Rename plugin to `rad-stack-guide` and reposition in marketplace

## Non-Goals

- No new review logic inside this plugin (it orchestrates, not reviews)
- No PreToolUse hooks for development-time routing (CLAUDE.md rules handle this)
- No hard dependencies on other plugins (graceful degradation remains)

---

## Architecture

```
Phase 1: DETECT & EQUIP       Phase 2: GUIDE              Phase 3: REVIEW
───────────────────────        ──────────────────          ──────────────────
/detect-stack or               CLAUDE.md rules             /review-for-ship
SessionStart auto-prompt       guide Claude to use         dispatches specialists
                               right skills proactively    + rad-code-review as
→ scan project                                             final gate
→ write stack profile          → skill routing rules
→ gap analysis (installed      → team settings.json        → unified report
  vs needed plugins)             enabledPlugins             → fix suggestions
→ CLAUDE.md injection
→ settings.json generation
```

---

## Changes by File

### 1. Rename: rad-stack-detect → rad-stack-guide

- Rename directory: `plugins/rad-stack-detect/` → `plugins/rad-stack-guide/`
- Update `plugin.json`: name, description
- Update `marketplace.json`: name, source path, description, add tags
- Update README.md: name, positioning, description

### 2. plugin.json — Add hooks field

```json
{
  "name": "rad-stack-guide",
  "description": "Auto-detects your tech stack, installs the right plugins, configures Claude for stack-aware development, and orchestrates pre-ship reviews. The hub for the rad development stack.",
  "version": "2.0.0",
  "author": { "name": "RAD", "url": "https://github.com/radesjardins" },
  "license": "Apache-2.0",
  "hooks": [
    {
      "event": "Stop",
      "type": "skill",
      "skill": "stack-startup-check",
      "condition": "first_message"
    }
  ]
}
```

Note: Claude Code hooks fire on events (PreToolUse, PostToolUse, Stop, Notification). For a "session start" check, we use a lightweight skill that the detect-stack skill's instructions tell Claude to consider. The most practical approach is adding guidance in the skill description that triggers on session-relevant phrases, plus a mention in the CLAUDE.md snippet that reminds Claude to check the stack profile.

### 3. detect-stack SKILL.md — Enhanced with 3 new phases

Existing Phases 1-5 remain. Add after Phase 4 (Write Stack Profile):

#### Phase 4.5: Gap Analysis

After writing the profile, check which plugins from the profile are actually available:

- For each plugin in `plugins.core` and `plugins.supporting`:
  - Attempt to reference a known skill from that plugin
  - If the skill doesn't exist / can't be found, mark as "not installed"
- Display gap report:
  ```
  ## Plugin Status
  
  ✓ rad-react — installed
  ✓ rad-typescript — installed
  ✗ rad-nextjs — not installed
  ✗ rad-a11y — not installed
  
  Install missing plugins:
  claude plugins install rad-nextjs@rad-claude-skills
  claude plugins install rad-a11y@rad-claude-skills
  ```
- If all plugins are installed, skip this section

#### Phase 4.6: CLAUDE.md Injection

After gap analysis, offer to add stack-aware guidance to the project's CLAUDE.md:

- Check if `CLAUDE.md` exists in project root
- If it already has a `## Stack Guidance` section, show diff and ask to update
- If no section exists, offer to append
- Content template:

```markdown
## Stack Guidance

This project uses [tech list with versions].
Stack profile: .claude/stack-profile.local.md

### Skill Routing
When working on this project, consult these skills proactively:

[For each core plugin:]
- **[file patterns]**: use [plugin-name] skills ([list 2-3 key skills])

[For each supporting plugin:]
- **[topic area]**: use [plugin-name] skills ([list 1-2 key skills])

### Before Shipping
Run `/review-for-ship` for comprehensive stack-aware review.
```

The skill routing rules are generated dynamically based on detected stack. Examples:

| Detected Tech | File Pattern | Skills to Consult |
|---|---|---|
| React | `*.tsx`, `*.jsx` with JSX | rad-react (react-foundations, react-performance, react-security) |
| Next.js | `app/`, `pages/`, Server Actions | rad-nextjs (nextjs-best-practices, nextjs-security) |
| TypeScript | `*.ts`, `*.tsx` | rad-typescript (typescript-strict-mode, typescript-api-safety) |
| Fastify | `routes/`, `plugins/`, Fastify imports | rad-fastify (fastify-best-practices, fastify-schemas-validation) |
| Astro | `*.astro`, `src/pages/` | rad-astro (astro-best-practices, astro-performance) |
| Accessibility | Any UI components | rad-a11y (a11y-semantic-html, a11y-aria-patterns) |
| Chrome Extension | `manifest.json`, `content/`, `background/` | rad-chrome-extension (chrome-ext-best-practices, chrome-ext-security) |
| Zod | Zod schema files | rad-zod (zod-schema-design, zod-security) |

#### Phase 4.7: Team Settings Generation

After CLAUDE.md injection, offer to generate `.claude/settings.json`:

- Check if file exists
- If exists, merge `enabledPlugins` into existing settings (don't overwrite other fields)
- If not exists, create with enabledPlugins only
- Content:

```json
{
  "enabledPlugins": {
    "rad-stack-guide@rad-claude-skills": true,
    "[plugin]@rad-claude-skills": true
  }
}
```

- Explain: "When teammates clone this repo and trust the project folder, they'll be prompted to install these plugins."

### 4. review-for-ship SKILL.md — Add rad-code-review as final gate

Insert between current Step 3 (Dispatch Review Agents) and Step 4 (Compile Results):

#### Step 3.5: Final Gate — rad-code-review

After all specialist agents have completed and their results are collected:

1. Launch rad-code-review as the final reviewer using the Skill tool (invoke `rad-code-review`)
2. Pass scope as the current project with `--strictness production`
3. rad-code-review covers dimensions the specialists don't:
   - AI slop detection (14 patterns)
   - Architecture review (coupling, boundaries, naming)
   - Release readiness (config, secrets, dependencies, migrations)
   - General security checklist (OWASP 12 categories — overlaps with specialists but catches gaps)
   - Documentation completeness
4. Its verdict becomes the ship/no-ship decision in the unified report

Update the report format to include a "Final Gate" section:

```
## Final Gate: Code Review

**Verdict:** [Ship / No Ship / Conditional]
**Strictness:** production

[rad-code-review findings organized by its standard severity model]
```

The overall assessment logic becomes:
- If rad-code-review says "No Ship" → overall = "Critical Issues Found"
- If any specialist has Critical findings → overall = "Needs Work"
- If rad-code-review says "Ship" and no specialist Criticals → overall = "Ready to Ship"

#### Also add: Profile drift warning

At the start of Step 1 (Read Stack Profile), after reading the profile:
- Parse the `detected` date from YAML frontmatter
- If older than 90 days, warn: "Your stack profile is [N] days old. Consider running `/detect-stack --update` to refresh before review."

### 5. New skill: stack-startup-check

A lightweight skill that fires contextually (not as a hook — as guidance in the detect-stack description triggers):

**Purpose:** When a user starts a session in a project that has no `.claude/stack-profile.local.md`, and the project has a `package.json` or config files, suggest running `/detect-stack`.

**Implementation:** Add trigger phrases to detect-stack's description:
```yaml
description: >
  ...existing triggers...
  Also suggest proactively when starting work in a project that has no
  .claude/stack-profile.local.md but does have package.json or framework
  config files.
```

This is lighter than a hook and doesn't require any new files. The detect-stack skill's description already guides Claude on when to suggest it.

### 6. technology-map.md — Add rad-code-review entry

Add to the Plugin Mapping section:

```markdown
### rad-code-review (via skill)
- **Triggers when:** Always included in review-for-ship as final gate
- **Tier:** Final Gate (runs after all specialist reviewers)
- **Scope:** AI slop detection, architecture, release readiness, general security, documentation
- **Invocation:** Skill tool (not Agent subagent_type) — invoke `rad-code-review`
- **Note:** This is a standalone skill, not a plugin agent. It runs as the generalist complement to the specialist reviewer agents.
```

### 7. marketplace.json — Update entry

```json
{
  "name": "rad-stack-guide",
  "source": "./plugins/rad-stack-guide",
  "description": "Auto-detects your tech stack, recommends and configures the right plugins, injects stack-aware guidance into CLAUDE.md, generates team settings, and orchestrates pre-ship reviews with specialist reviewers + rad-code-review as final gate. The entry point for the rad development stack.",
  "category": "orchestration",
  "tags": ["bundle", "orchestrator", "stack-detection", "review", "developer-experience"]
}
```

### 8. README.md — Rewrite for bundle positioning

New structure:
- Hero: "Install one plugin. It detects your stack, configures everything, and orchestrates reviews."
- Quick Start: 3-step flow (install → detect → develop/ship)
- What It Does: Detect & Equip, Guide, Review sections
- Supported Stacks: table of all detected technologies and their plugins
- Bundle Philosophy: standalone plugins work independently; stack-guide makes them work together
- Installation

---

## Stack Profile Format Changes

The `.claude/stack-profile.local.md` YAML frontmatter gains one new field:

```yaml
---
detected: YYYY-MM-DD
project_name: ...
project_type: ...
technologies: ...
plugins:
  core: [...]
  supporting: [...]
  pre_ship: [...]
  final_gate:
    - rad-code-review
review_agents: [...]
---
```

The `final_gate` field tells `/review-for-ship` to invoke rad-code-review after specialists complete.

---

## Implementation Order

1. Rename directory and update plugin.json
2. Enhance detect-stack SKILL.md (gap analysis, CLAUDE.md injection, settings generation)
3. Enhance review-for-ship SKILL.md (rad-code-review final gate, profile drift warning)
4. Update technology-map.md (add rad-code-review entry, add skill routing patterns)
5. Rewrite README.md
6. Update marketplace.json
7. Update detect-stack description triggers for proactive suggestion

---

## Success Criteria

- `/detect-stack` on a Next.js + React + TypeScript project:
  - Detects all 3 technologies with versions
  - Shows gap analysis (which plugins installed vs missing)
  - Offers to inject CLAUDE.md stack guidance with skill routing rules
  - Offers to generate settings.json enabledPlugins
  - Writes profile with final_gate field
- `/review-for-ship` on same project:
  - Dispatches nextjs-reviewer, react-reviewer, typescript-reviewer, a11y-reviewer in parallel
  - After specialists complete, runs rad-code-review as final gate
  - Produces unified report with specialist findings + final gate verdict
  - Overall ship/no-ship decision driven by rad-code-review verdict
- Marketplace shows rad-stack-guide with orchestration category and bundle tags
