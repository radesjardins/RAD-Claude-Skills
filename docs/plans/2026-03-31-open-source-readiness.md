# Open-Source Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare the rad-skills-repo for public sharing with complete community health files, hardened .gitignore, GitHub templates, and comprehensive README documentation for every plugin and standalone skill.

**Architecture:** Documentation-only changes across 25+ files. No code changes. Root-level community health files follow GitHub's standard conventions. Each plugin/skill README follows a consistent template covering purpose, features, skills list, trigger phrases, and installation.

**Tech Stack:** Markdown, GitHub community health file conventions, MIT license

---

## Current State Assessment

### Files That Exist and Are Complete
| File | Status | Notes |
|------|--------|-------|
| `LICENSE` | Complete | MIT, 2025-2026 RAD |
| `SECURITY.md` | Complete | Private reporting, timeline, scope, best practices |
| `CONTRIBUTING.md` | Needs minor fix | References `CODE_OF_CONDUCT.md` which doesn't exist yet |

### Files That Exist but Need Updates
| File | Issue |
|------|-------|
| `.gitignore` | Minimal — missing node_modules, logs, build artifacts, OS files, coverage, archives |
| `README.md` | Severely outdated — only lists 1 plugin (SEO) + 5 standalone skills. Repo now has 14 plugins + 6 skills |

### Files That Are Missing
| File | Purpose |
|------|---------|
| `CODE_OF_CONDUCT.md` | Contributor Covenant (referenced in CONTRIBUTING.md but absent) |
| `.github/PULL_REQUEST_TEMPLATE.md` | Standardize PR descriptions |
| `.github/ISSUE_TEMPLATE/bug_report.md` | Structured bug reports |
| `.github/ISSUE_TEMPLATE/feature_request.md` | Structured feature requests |
| `.github/ISSUE_TEMPLATE/config.yml` | Issue template chooser config |
| `CHANGELOG.md` | Track releases and changes for users |

### Plugin READMEs Missing (5 of 14)
| Plugin | Skills | Agents | Complexity |
|--------|--------|--------|------------|
| `rad-agentic-company-builder` | 7 | 1 | Medium |
| `rad-brainstormer` | 10 | 3 | Medium |
| `rad-google-workspace` | 93 (42 services + 41 recipes + 10 personas) | 0 | High |
| `rad-react` | 6 | 1 | Medium |
| `rad-seo-optimizer` | 12 | 3 | Medium (root README already has detail) |

### Plugin READMEs That Exist (8 of 14) — Need Consistency Review
- `rad-a11y`, `rad-astro`, `rad-docker`, `rad-fastify`, `rad-nextjs`, `rad-tailwind`, `rad-typescript`, `rad-zod`

### Standalone Skill READMEs Missing (5 of 6)
| Skill | Has SKILL.md |
|-------|-------------|
| `rad-brainstorming` | Yes |
| `rad-context-prompter` | Yes |
| `rad-gem-creator` | Yes |
| `rad-gpt-creator` | Yes |
| `rad-para-second-brain` | Yes |

(`rad-code-review` already has a comprehensive README)

---

## Task 1: Create CODE_OF_CONDUCT.md

**Files:**
- Create: `CODE_OF_CONDUCT.md`

This file is already referenced by `CONTRIBUTING.md:75` but doesn't exist. Use the Contributor Covenant v2.1, the most widely adopted code of conduct for open-source projects.

- [ ] **Step 1: Create `CODE_OF_CONDUCT.md`**

Write the full Contributor Covenant v2.1 with:
- Contact method: GitHub Issues (consistent with SECURITY.md and CONTRIBUTING.md)
- Attribution to Contributor Covenant

- [ ] **Step 2: Verify the link in CONTRIBUTING.md resolves**

Read `CONTRIBUTING.md:75` and confirm `[Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md)` will resolve correctly.

- [ ] **Step 3: Commit**

```bash
git add CODE_OF_CONDUCT.md
git commit -m "docs: add Contributor Covenant Code of Conduct v2.1"
```

---

## Task 2: Harden .gitignore for Open Source

**Files:**
- Modify: `.gitignore`

Current `.gitignore` is 22 lines. For an open-source repo that users will clone and potentially develop against, it needs coverage for: Node.js artifacts, Python artifacts, logs, OS-specific files (expanded), editor configs (expanded), build outputs, coverage reports, temporary files, and archives.

- [ ] **Step 1: Rewrite `.gitignore` with comprehensive patterns**

Organize into clear sections:
- **OS files:** .DS_Store, Thumbs.db, desktop.ini, ._*, .Spotlight-V100, .Trashes, ehthumbs.db
- **IDE/Editor:** .vscode/, .idea/, *.swp, *.swo, *.sublime-workspace, *.sublime-project, .project, .classpath, .settings/
- **Node.js:** node_modules/, npm-debug.log*, yarn-debug.log*, yarn-error.log*, .pnpm-debug.log*, package-lock.json (if not needed), .npm/
- **Python:** __pycache__/, *.py[cod], *$py.class, *.egg-info/, dist/, build/, .eggs/
- **Build/Output:** *.output, optimization-workspace/, out/, .next/, .nuxt/, .cache/
- **Coverage/Testing:** coverage/, .nyc_output/, *.lcov, .vitest/
- **Secrets:** .env, .env.local, .env.*.local, *.key, *.pem, credentials.json, *.secret
- **Archives/Binaries:** *.zip, *.tar.gz, *.rar, *.7z
- **Logs:** *.log, logs/

- [ ] **Step 2: Commit**

```bash
git add .gitignore
git commit -m "chore: harden .gitignore for open-source distribution"
```

---

## Task 3: Create GitHub Issue and PR Templates

**Files:**
- Create: `.github/PULL_REQUEST_TEMPLATE.md`
- Create: `.github/ISSUE_TEMPLATE/bug_report.md`
- Create: `.github/ISSUE_TEMPLATE/feature_request.md`
- Create: `.github/ISSUE_TEMPLATE/config.yml`

These files reference patterns already established in `CONTRIBUTING.md` (bug report, feature request, PR submission).

- [ ] **Step 1: Create `.github/ISSUE_TEMPLATE/bug_report.md`**

YAML frontmatter issue template with fields:
- name, description, title prefix, labels
- Body: skill/plugin affected, Claude Code version, expected behavior, actual behavior, steps to reproduce, additional context

- [ ] **Step 2: Create `.github/ISSUE_TEMPLATE/feature_request.md`**

YAML frontmatter issue template with fields:
- name, description, title prefix, labels
- Body: problem/use case, proposed solution, which plugin/skill, alternatives considered

- [ ] **Step 3: Create `.github/ISSUE_TEMPLATE/config.yml`**

Template chooser configuration. Include a link to Discussions for questions.

```yaml
blank_issues_enabled: false
contact_links:
  - name: Questions & Discussion
    url: https://github.com/radesjardins/RAD-Claude-Skills/discussions
    about: Ask questions, share ideas, or show what you've built
```

- [ ] **Step 4: Create `.github/PULL_REQUEST_TEMPLATE.md`**

PR template with sections:
- Summary of changes
- Type of change (bug fix, new skill/plugin, improvement, docs)
- Checklist: tested locally, follows style guide, updated docs, no secrets committed

- [ ] **Step 5: Commit**

```bash
git add .github/
git commit -m "docs: add GitHub issue and PR templates"
```

---

## Task 4: Create CHANGELOG.md

**Files:**
- Create: `CHANGELOG.md`

Follows [Keep a Changelog](https://keepachangelog.com/) format. Since this is the initial public release, include one entry summarizing the current state.

- [ ] **Step 1: Create `CHANGELOG.md`**

Include:
- Header explaining the format (Keep a Changelog + Semantic Versioning)
- `[Unreleased]` section listing all 14 plugins and 6 standalone skills as the initial offering
- Group by: Added

- [ ] **Step 2: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: add CHANGELOG.md for release tracking"
```

---

## Task 5: Create Missing Plugin READMEs (5 plugins)

**Files:**
- Create: `plugins/rad-agentic-company-builder/README.md`
- Create: `plugins/rad-brainstormer/README.md`
- Create: `plugins/rad-google-workspace/README.md`
- Create: `plugins/rad-react/README.md`
- Create: `plugins/rad-seo-optimizer/README.md`

Each README follows this consistent template (matching existing plugin READMEs):

```markdown
# RAD [Plugin Name]

[1-2 sentence description from plugin.json]

## What's Inside

| Component | Count |
|-----------|-------|
| Skills | N |
| Agents | N |
| References | N |

## Skills

| Skill | Trigger Phrases | What It Does |
|-------|----------------|--------------|
| ... | ... | ... |

## Agents (if applicable)

| Agent | When To Use | What It Does |
|-------|------------|--------------|
| ... | ... | ... |

## Installation

\`\`\`bash
claude plugins add ./plugins/rad-[name]
\`\`\`

## Requirements

- Claude Code CLI installed and authenticated
- [Any additional requirements]

## License

MIT
```

For each plugin README, read the SKILL.md frontmatter of each skill to extract accurate trigger phrases and descriptions. Read agent frontmatter for agent descriptions.

- [ ] **Step 5a: Create `plugins/rad-agentic-company-builder/README.md`**

Read all 7 skill SKILL.md files + 1 agent file in this plugin to extract descriptions and triggers.

Content: 7 skills (scaffold-company, scaffold-project, generate-agents, generate-skills, configure-hooks, configure-mcp, agentic-operations), 1 agent (company-auditor). Note prerequisite: based on "The Agentic Bible 2026".

- [ ] **Step 5b: Create `plugins/rad-brainstormer/README.md`**

Read all 10 skill SKILL.md files + 3 agent files.

Content: 10 skills covering ideation methodologies (brainstorm-session, creative-unblock, design-sprint, five-whys, how-might-we, idea-evaluation, idea-generation, reverse-brainstorm, scamper, six-hats), 3 agents (domain-researcher, idea-challenger, spec-reviewer).

- [ ] **Step 5c: Create `plugins/rad-google-workspace/README.md`**

Read plugin.json for the full skill list. This is the largest plugin (93 skills).

Organize README into clear sections:
- Service Skills (42): grouped by Google service (Gmail, Calendar, Drive, Docs, Sheets, Slides, Chat, Meet, Tasks, Forms, Keep, Classroom, Model Armor, etc.)
- Workflow Recipes (41): common cross-service patterns
- Role-Based Personas (10): pre-configured personas for different job roles
- Note prerequisite: requires the `gws` CLI binary

- [ ] **Step 5d: Create `plugins/rad-react/README.md`**

Read all 6 skill SKILL.md files + 1 agent file.

Content: 6 skills (react-foundations, react-app-building, react-performance, react-accessibility, react-security, react-engineering), 1 agent (react-reviewer). Note: includes React 19 patterns, useEffect anti-patterns, IDOR checks.

- [ ] **Step 5e: Create `plugins/rad-seo-optimizer/README.md`**

Read all 12 skill SKILL.md files + 3 agent files.

Content: 12 skills, 3 agents, references. Note: the root README.md already has extensive SEO optimizer documentation that can inform this plugin-level README, but the plugin README should be self-contained.

- [ ] **Step 5f: Commit**

```bash
git add plugins/rad-agentic-company-builder/README.md
git add plugins/rad-brainstormer/README.md
git add plugins/rad-google-workspace/README.md
git add plugins/rad-react/README.md
git add plugins/rad-seo-optimizer/README.md
git commit -m "docs: add README.md for 5 plugins missing documentation"
```

---

## Task 6: Create Missing Standalone Skill READMEs (5 skills)

**Files:**
- Create: `skills/rad-brainstorming/README.md`
- Create: `skills/rad-context-prompter/README.md`
- Create: `skills/rad-gem-creator/README.md`
- Create: `skills/rad-gpt-creator/README.md`
- Create: `skills/rad-para-second-brain/README.md`

Each standalone skill README follows this template:

```markdown
# RAD [Skill Name]

[1-2 sentence description]

## What It Does

[3-5 bullet points on capabilities]

## How to Trigger

[List trigger phrases from SKILL.md frontmatter description]

Or ask naturally:
- "[example natural language request]"
- "[another example]"

## What You Get

[Describe the output/deliverable]

## Installation

\`\`\`bash
mkdir -p ~/.claude/skills
cp -r skills/rad-[name] ~/.claude/skills/
\`\`\`

## License

MIT
```

For each skill, read the full SKILL.md to understand its workflow, output format, and unique features.

- [ ] **Step 6a: Create `skills/rad-brainstorming/README.md`**

Read SKILL.md. Key features: ideation before implementation, multiple brainstorming methodologies, divergent/convergent phases.

- [ ] **Step 6b: Create `skills/rad-context-prompter/README.md`**

Read SKILL.md. Key features: prompt engineering for any AI tool, system prompts, tool descriptions, agentic workflows, cross-model migration.

- [ ] **Step 6c: Create `skills/rad-gem-creator/README.md`**

Read SKILL.md. Key features: guided interview workflow, Google Gemini Gems, structured instructions, anti-hallucination patterns.

- [ ] **Step 6d: Create `skills/rad-gpt-creator/README.md`**

Read SKILL.md. Key features: guided interview workflow, OpenAI Custom GPTs, instruction authoring, knowledge base design.

- [ ] **Step 6e: Create `skills/rad-para-second-brain/README.md`**

Read SKILL.md. Key features: PARA method (Projects, Areas, Resources, Archives), Progressive Summarization, weekly reviews, capture workflows.

- [ ] **Step 6f: Commit**

```bash
git add skills/rad-brainstorming/README.md
git add skills/rad-context-prompter/README.md
git add skills/rad-gem-creator/README.md
git add skills/rad-gpt-creator/README.md
git add skills/rad-para-second-brain/README.md
git commit -m "docs: add README.md for 5 standalone skills missing documentation"
```

---

## Task 7: Review and Ensure Consistency of 8 Existing Plugin READMEs

**Files:**
- Review: `plugins/rad-a11y/README.md`
- Review: `plugins/rad-astro/README.md`
- Review: `plugins/rad-docker/README.md`
- Review: `plugins/rad-fastify/README.md`
- Review: `plugins/rad-nextjs/README.md`
- Review: `plugins/rad-tailwind/README.md`
- Review: `plugins/rad-typescript/README.md`
- Review: `plugins/rad-zod/README.md`
- Review: `skills/rad-code-review/README.md`

Read each existing README. Verify each one has:
- Clear description of what the plugin does
- Skills table with names and descriptions
- Agent table (if applicable)
- Installation instructions
- Trigger phrases or usage examples
- License mention

- [ ] **Step 7a: Read all 9 existing READMEs and note any gaps**

Flag any README that is missing key sections compared to the template.

- [ ] **Step 7b: Update any READMEs with missing sections**

Only modify if a README is clearly incomplete (e.g., missing installation instructions or skill descriptions). Do not rewrite READMEs that are already comprehensive.

- [ ] **Step 7c: Commit (only if changes were made)**

```bash
git add plugins/*/README.md skills/*/README.md
git commit -m "docs: normalize existing plugin and skill READMEs for consistency"
```

---

## Task 8: Update Root README.md

**Files:**
- Modify: `README.md`

The root README is severely outdated. It only lists 1 plugin (SEO Optimizer) and 5 standalone skills. The repo now has **14 plugins** and **6 standalone skills**.

- [ ] **Step 8a: Rewrite the components overview section**

Update the directory tree, "Plugins vs. Skills" section, and the "Available Components" tables to list all 14 plugins and 6 skills with accurate skill/agent counts.

**Plugins table should include all 14:**
| Plugin | Skills | Agents | What It Does |
|--------|--------|--------|-------------|
| rad-a11y | 6 | 1 | WCAG 2.2 AA accessibility |
| rad-agentic-company-builder | 7 | 1 | AI-agent-driven company infrastructure |
| rad-astro | 5 | 1 | Astro 5/6 framework standards |
| rad-brainstormer | 10 | 3 | Ideation methodologies |
| rad-docker | 3 | 0 | Docker best practices |
| rad-fastify | 8 | 1 | Fastify framework standards |
| rad-google-workspace | 93 | 0 | Google Workspace integration |
| rad-nextjs | 4 | 1 | Next.js App Router standards |
| rad-react | 6 | 1 | Modern React best practices |
| rad-seo-optimizer | 12 | 3 | SEO toolkit |
| rad-tailwind | 1 | 0 | Tailwind CSS v4 standards |
| rad-typescript | 6 | 1 | Production TypeScript |
| rad-zod | 6 | 1 | Zod v4 validation |

**Standalone Skills table should include all 6:**
| Skill | What It Does |
|-------|-------------|
| rad-brainstorming | Creative ideation before implementation |
| rad-code-review | Professional-grade code review with AI slop detection |
| rad-context-prompter | Prompt engineering for any AI platform |
| rad-gem-creator | Google Gemini Gem instruction builder |
| rad-gpt-creator | OpenAI Custom GPT builder |
| rad-para-second-brain | PARA method knowledge management |

- [ ] **Step 8b: Update installation instructions**

Ensure install examples cover the plugin install command and mention all 14 plugins, not just SEO Optimizer.

- [ ] **Step 8c: Trim the overly-detailed SEO section**

The root README currently has ~350 lines dedicated solely to the SEO Optimizer. Now that each plugin has its own README, the root README should have a brief summary for each plugin (2-3 sentences) with a link to the plugin's own README, not duplicate the full documentation. Keep the detailed SEO content in `plugins/rad-seo-optimizer/README.md`.

Similarly, trim the Code Review section and link to `skills/rad-code-review/README.md`.

- [ ] **Step 8d: Add links to community health files**

Add a "Contributing" section at the bottom that links to:
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `CHANGELOG.md`

- [ ] **Step 8e: Commit**

```bash
git add README.md
git commit -m "docs: update root README to reflect all 14 plugins and 6 skills"
```

---

## Task 9: Clean Up desktop.ini Files

**Files:**
- Remove from tracking: `docs/desktop.ini`, `docs/plans/desktop.ini`

These Windows-generated files should not be in the repo. The hardened `.gitignore` from Task 2 already covers `desktop.ini`, but existing tracked files need to be removed from git tracking.

- [ ] **Step 1: Remove desktop.ini files from git tracking**

```bash
git rm --cached docs/desktop.ini docs/plans/desktop.ini
```

- [ ] **Step 2: Commit**

```bash
git commit -m "chore: remove Windows desktop.ini files from tracking"
```

---

## Summary

| Task | Files Created | Files Modified | Priority |
|------|--------------|----------------|----------|
| 1. CODE_OF_CONDUCT.md | 1 | 0 | High (blocks CONTRIBUTING.md link) |
| 2. Harden .gitignore | 0 | 1 | High |
| 3. GitHub Templates | 4 | 0 | High |
| 4. CHANGELOG.md | 1 | 0 | Medium |
| 5. Plugin READMEs (5 missing) | 5 | 0 | High |
| 6. Skill READMEs (5 missing) | 5 | 0 | High |
| 7. Review existing READMEs | 0 | 0-9 | Medium |
| 8. Update root README | 0 | 1 | High |
| 9. Clean up desktop.ini | 0 | 0 (git rm) | Low |
| **Totals** | **16+** | **2-12** | |

**Estimated new files: 16** | **Estimated modified files: 2-12** | **Commits: 9**
