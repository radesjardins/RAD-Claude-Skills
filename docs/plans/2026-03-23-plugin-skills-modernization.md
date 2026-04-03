# RAD-Claude-Skills Modernization Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring all plugins and standalone skills into compliance with the official Claude Code skill spec (agentskills.io) and migrate from the legacy `commands/` format to `skills/*/SKILL.md`.

**Architecture:** Systematic file-by-file updates across 2 plugins (rad-brainstormer, rad-seo-optimizer) and 6 standalone skills. Each task is scoped to one component so changes can be reviewed and committed incrementally.

**Tech Stack:** Markdown, YAML frontmatter, Claude Code plugin system

---

## Audit Summary

### Scope

| Component | Skills | Commands (legacy) | Agents | References |
|---|---|---|---|---|
| rad-brainstormer plugin | 5 | 7 | 3 | 5 |
| rad-seo-optimizer plugin | 11 | 6 | 3 | 7 |
| Standalone skills | 6 | -- | -- | varies |
| **Totals** | **22** | **13** | **6** | **12+** |

### Issue Categories Found

| Severity | Count | Description |
|---|---|---|
| CRITICAL | 6 | Broken discoverability, broken cross-references, major size violations |
| HIGH | 3 | All descriptions fail spec (no third-person, no trigger phrases, not pushy) |
| MODERATE | 4 | Second-person writing style, legacy commands/ format, orphaned references |
| LOW | 5 | Missing optional frontmatter, non-standard fields, minor formatting |

### Detailed Findings

#### CRITICAL Issues

1. **rad-code-review: SKILL.md is nested in `skill/` subdirectory** instead of at the skill root. Claude Code will NOT discover this skill.
2. **rad-brainstorming: `name` field mismatch** -- frontmatter says `brainstorming` but directory is `rad-brainstorming`. Spec requires these match.
3. **rad-seo-optimizer: 4 broken cross-skill references in `full-seo-audit`** -- delegates to `content-optimizer`, `schema-markup`, `competitor-analysis`, `seo-monitor` which don't exist (actual names: `content-strategist`/`on-page-optimizer`, `schema-architect`, `competitor-intelligence`, and `seo-monitor` doesn't exist at all).
4. **3 standalone skills exceed 500-line / 2000-word limits** -- rad-context-prompter (429 lines/3639 words), rad-gem-creator (482/3799), rad-gpt-creator (509/3973).
5. **3 SEO plugin skills exceed 500-line limit** -- aeo-optimizer (587 lines), technical-seo (592), link-building-strategy (506).
6. **All 13 commands use legacy `commands/` format** with non-standard `arguments:` frontmatter.

#### HIGH Issues

7. **ALL 22 skill descriptions fail the spec** -- none use third-person ("This skill should be used when..."), none include specific trigger phrases, none are "pushy" to combat undertriggering.
8. **Missing `allowed-tools` on all SEO plugin skills (11)** and most standalone skills (5 of 6).
9. **rad-code-review `allowed-tools` is YAML list** instead of spec-required space-delimited string.

#### MODERATE Issues

10. **Second-person writing ("you/your")** in ~15 skill bodies instead of imperative/infinitive form.
11. **`google-ranking-systems.md` reference is orphaned** in SEO plugin -- not referenced by any skill.
12. **`domain-research-guide.md` reference is unreferenced** in brainstormer plugin.
13. **Agent `color` field** is non-standard (all 6 agents).

#### LOW Issues

14. **Missing `argument-hint`** on all skills that accept arguments.
15. **Missing `license`/`repository` fields** in plugin.json manifests.
16. **Non-standard `version` field** in some skill frontmatter.
17. **`@{{UCR_DIR}}` template variables** in rad-code-review may not resolve.
18. **DOT graph in rad-brainstorming** may not render in all contexts.

---

## Task Plan

### Task 1: Fix Critical Discoverability Blockers

**Files:**
- Move: `skills/rad-code-review/skill/SKILL.md` -> `skills/rad-code-review/SKILL.md`
- Modify: `skills/rad-brainstorming/SKILL.md` (fix name field)
- Modify: `plugins/rad-seo-optimizer/skills/full-seo-audit/SKILL.md` (fix cross-references)

- [ ] **Step 1: Move rad-code-review SKILL.md to correct location**

Move `skills/rad-code-review/skill/SKILL.md` to `skills/rad-code-review/SKILL.md`. Move any sibling files in `skill/` up one level if needed, then remove the empty `skill/` directory.

- [ ] **Step 2: Fix rad-brainstorming name mismatch**

In `skills/rad-brainstorming/SKILL.md`, change the frontmatter `name: brainstorming` to `name: rad-brainstorming`.

- [ ] **Step 3: Fix broken cross-skill references in full-seo-audit**

In `plugins/rad-seo-optimizer/skills/full-seo-audit/SKILL.md`, find the Cross-Skill Delegation Reference and fix:
- `content-optimizer` -> `on-page-optimizer` (or `content-strategist` depending on context)
- `schema-markup` -> `schema-architect`
- `competitor-analysis` -> `competitor-intelligence`
- `seo-monitor` -> remove or note as "planned" if it's a future skill

- [ ] **Step 4: Verify fixes**

Run `find plugins/ skills/ -name "SKILL.md" -type f` to confirm all SKILL.md files are at the correct directory depth (exactly one level below the skill directory).

- [ ] **Step 5: Commit**

```bash
git add skills/rad-code-review/ skills/rad-brainstorming/SKILL.md plugins/rad-seo-optimizer/skills/full-seo-audit/SKILL.md
git commit -m "fix: critical discoverability blockers — move SKILL.md, fix name mismatch, fix cross-references"
```

---

### Task 2: Rewrite ALL Skill Descriptions (22 skills)

This is the highest-impact change. Every skill description must be rewritten to:
- Use third-person: "This skill should be used when the user asks to..."
- Include 4-8 specific trigger phrases users would actually type
- Be "pushy" to combat undertriggering (per official skill-creator guidance)

**Files:** All 22 SKILL.md files across both plugins and standalone skills.

- [ ] **Step 1: Rewrite rad-brainstormer plugin skill descriptions (5 skills)**

Each description should follow this pattern:
```yaml
description: >
  This skill should be used when the user says "let's brainstorm", "I need ideas",
  "help me think through", "brainstorm with me", or wants to explore a problem space
  before committing to an approach. Also use for any creative ideation, even if the
  user doesn't explicitly say "brainstorm" — any open-ended "what should I build?"
  or "how should I approach this?" qualifies.
```

Skills to update:
- `brainstorm-session` — triggers: "brainstorm", "I need ideas", "help me think", "explore options"
- `creative-unblock` — triggers: "I'm stuck", "no ideas", "writer's block", "can't think of anything"
- `design-sprint` — triggers: "design this", "create a spec", "design sprint", "software design"
- `idea-evaluation` — triggers: "evaluate ideas", "which idea is best", "prioritize", "compare options"
- `idea-generation` — triggers: "generate ideas", "more ideas", "alternatives", "what else could work"

- [ ] **Step 2: Rewrite rad-seo-optimizer plugin skill descriptions (11 skills)**

Same pattern. Each gets domain-specific trigger phrases:
- `full-seo-audit` — "audit my SEO", "check my site", "SEO score", "SEO health check"
- `aeo-optimizer` — "AI visibility", "how does my brand appear in AI", "AI search optimization"
- `technical-seo` — "site speed", "core web vitals", "crawlability", "robots.txt"
- `keyword-discovery` — "keyword research", "what keywords", "find keywords for"
- `on-page-optimizer` — "optimize this page", "improve my title tags", "meta descriptions"
- `schema-architect` — "add schema", "structured data", "JSON-LD", "rich snippets"
- `competitor-intelligence` — "competitor analysis", "who ranks for", "what are competitors doing"
- `content-strategist` — "content strategy", "what should I write about", "content gaps"
- `broken-link-fixer` — "broken links", "404 errors", "dead links", "fix links"
- `link-building-strategy` — "link building", "get backlinks", "domain authority"
- `seo-report-generator` — "SEO report", "generate audit report", "summarize SEO findings"

- [ ] **Step 3: Rewrite standalone skill descriptions (6 skills)**

- `rad-brainstorming` — same triggers as brainstorm-session (these are sibling skills)
- `rad-code-review` — "review my code", "code review", "is this ready to ship", "check for bugs"
- `rad-context-prompter` — "write a prompt", "prompt engineering", "system prompt", "optimize my prompt"
- `rad-gem-creator` — "create a Gem", "Gemini assistant", "build a Gem", "Gem instructions"
- `rad-gpt-creator` — "create a GPT", "custom GPT", "build a GPT", "GPT instructions"
- `rad-para-second-brain` — "organize my notes", "PARA method", "second brain", "weekly review"

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: rewrite all 22 skill descriptions with third-person voice, trigger phrases, and pushy anti-undertrigger language"
```

---

### Task 3: Migrate Legacy Commands to Skills

Convert all 13 `commands/*.md` files to `skills/*/SKILL.md` format, then remove `commands/` directories.

**Files:**
- Create: 5 new skills in `plugins/rad-brainstormer/skills/` (5whys, hmw, reverse, scamper, six-hats)
- Modify: 2 existing skills in `plugins/rad-brainstormer/skills/` to absorb command functionality (brainstorm-session, idea-evaluation)
- Modify: 5 existing skills in `plugins/rad-seo-optimizer/skills/` to absorb command functionality
- Create: 1 new skill in `plugins/rad-seo-optimizer/skills/` (fix-seo router)
- Delete: `plugins/rad-brainstormer/commands/` directory
- Delete: `plugins/rad-seo-optimizer/commands/` directory

- [ ] **Step 1: Create 5 new brainstormer technique skills**

For each technique command that has no corresponding skill, create a new skill directory:

```
plugins/rad-brainstormer/skills/five-whys/SKILL.md
plugins/rad-brainstormer/skills/how-might-we/SKILL.md
plugins/rad-brainstormer/skills/reverse-brainstorm/SKILL.md
plugins/rad-brainstormer/skills/scamper/SKILL.md
plugins/rad-brainstormer/skills/six-hats/SKILL.md
```

Each SKILL.md should:
- Have proper frontmatter with third-person description and trigger phrases
- Include `argument-hint` (e.g., `[concept to SCAMPER]`)
- Contain the command's body content adapted to imperative form
- Reference the appropriate `references/` files (methodology-catalog.md, facilitation-principles.md, etc.)

- [ ] **Step 2: Add argument-hint to existing brainstormer skills that absorb commands**

Add `argument-hint: "[topic or problem]"` to `brainstorm-session/SKILL.md` and `idea-evaluation/SKILL.md` since they absorb the `/brainstorm` and `/evaluate` commands.

- [ ] **Step 3: Add argument-hint to existing SEO skills that absorb commands**

For each SEO command being absorbed, add `argument-hint` to the corresponding skill:
- `full-seo-audit` — `argument-hint: "[URL or file path to audit]"`
- `aeo-optimizer` — `argument-hint: "[brand name or URL]"`
- `competitor-intelligence` — `argument-hint: "[competitor URL or domain]"`
- `keyword-discovery` — `argument-hint: "[topic or seed keyword]"`
- `schema-architect` — `argument-hint: "[URL or page to add schema to]"`

- [ ] **Step 4: Create fix-seo router skill**

The `fix-seo` command has unique routing logic not covered by any existing skill. Create:
```
plugins/rad-seo-optimizer/skills/fix-seo/SKILL.md
```
With description including triggers like "fix my SEO", "fix this SEO issue", "how do I fix [specific issue]".

- [ ] **Step 5: Delete legacy commands directories**

```bash
rm -rf plugins/rad-brainstormer/commands/
rm -rf plugins/rad-seo-optimizer/commands/
```

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat: migrate all 13 legacy commands to skills format, remove commands/ directories"
```

---

### Task 4: Fix Writing Style — Imperative Form

Convert second-person ("you/your") to imperative/infinitive form across all skill bodies.

**Files:** All SKILL.md files with second-person violations (~15 files).

- [ ] **Step 1: Fix brainstormer plugin skills (5 files)**

Common replacements:
- "You MUST complete these steps" -> "Complete these steps in order"
- "Your job: diagnose WHY" -> "Diagnose WHY the user is stuck"
- "your recommendation" -> "a recommendation"
- "You've generated 15-25 ideas" -> "After generating 15-25 ideas"
- "ALWAYS draw out user ideas before offering your own" -> "Draw out user ideas before offering alternatives"

- [ ] **Step 2: Fix SEO plugin skills (~6 files with moderate violations)**

Worst offenders:
- `keyword-discovery` — "You are an expert SEO keyword researcher" -> "Act as an expert SEO keyword researcher" or remove entirely and use imperative instructions
- `aeo-optimizer` — "your brand" -> "the brand" / "the client's brand" throughout (~30 instances)
- Others — scattered "your site" -> "the site", "you" -> imperative form

- [ ] **Step 3: Fix standalone skills (~4 files)**

- `rad-brainstorming` — "you should be able to answer" -> "be able to answer", etc.
- `rad-context-prompter` — "You are a prompt engineer" -> imperative role instructions
- `rad-gem-creator` / `rad-gpt-creator` — minor fixes

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "style: convert all skill bodies from second-person to imperative/infinitive form"
```

---

### Task 5: Progressive Disclosure — Extract Oversized Content to References

Move detailed reference material out of oversized SKILL.md files into `references/` directories.

**Files:**

| Skill | Current Words | Target | Content to Extract |
|---|---|---|---|
| `rad-context-prompter` | 3,639 | ~1,800 | Tool Routing section (~160 lines) -> `references/tool-routing.md` |
| `rad-gem-creator` | 3,799 | ~2,000 | Source Policy templates + Step 9 assembly -> `references/source-policy-templates.md` |
| `rad-gpt-creator` | 3,973 | ~2,000 | Source Policy + Capabilities/Actions + Special Cases -> `references/` files |
| `aeo-optimizer` | 3,313 | ~2,000 | Detailed phase steps -> `references/aeo-phases.md` |
| `technical-seo` | 3,473 | ~2,000 | Platform-specific fixes -> `references/platform-fixes.md` |
| `link-building-strategy` | 2,980 | ~2,000 | Outreach templates -> `references/outreach-templates.md` |

- [ ] **Step 1: Extract rad-context-prompter Tool Routing section**

Move the Tool Routing section (lines ~122-285) to `skills/rad-context-prompter/references/tool-routing.md`. Replace in SKILL.md with:
```markdown
## Tool Routing
For model-specific tool routing details, consult `references/tool-routing.md`.
```

- [ ] **Step 2: Extract rad-gem-creator content**

Move Source Policy templates and Step 9 assembly details to `skills/rad-gem-creator/references/source-policy-templates.md`. Keep a summary and pointer in SKILL.md.

- [ ] **Step 3: Extract rad-gpt-creator content**

Move Source Policy templates, Capabilities/Actions details, and Special Cases to reference files under `skills/rad-gpt-creator/references/`.

- [ ] **Step 4: Extract SEO plugin oversized content (3 skills)**

- `aeo-optimizer`: Extract detailed 8-phase steps to `references/aeo-phases.md`
- `technical-seo`: Extract platform-specific fixes to `references/platform-fixes.md`
- `link-building-strategy`: Extract outreach templates to `references/outreach-templates.md`

- [ ] **Step 5: Verify all new reference files are properly referenced from SKILL.md**

Each extracted section must have a pointer in the SKILL.md body explaining when to consult the reference file.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "refactor: extract oversized SKILL.md content into references/ for progressive disclosure"
```

---

### Task 6: Add Missing Frontmatter Fields

Add `allowed-tools` and `argument-hint` where appropriate. Fix rad-code-review's `allowed-tools` format.

**Files:** All 22 SKILL.md files.

- [ ] **Step 1: Add allowed-tools to SEO plugin skills (11 files)**

Most SEO skills need: `allowed-tools: WebSearch WebFetch Read Write Glob Grep Bash Agent`
Determine the minimal set per skill based on what each actually uses.

- [ ] **Step 2: Add allowed-tools to standalone skills (5 files missing it)**

Determine appropriate tools per skill.

- [ ] **Step 3: Fix rad-code-review allowed-tools format**

Change from YAML list to space-delimited string:
```yaml
# FROM:
allowed-tools:
  - Read
  - Glob
  ...

# TO:
allowed-tools: Read Glob Grep Bash Write Edit Agent
```

- [ ] **Step 4: Add argument-hint to skills that accept arguments**

Any skill that was formerly a command with `arguments:` should get `argument-hint`.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: add allowed-tools and argument-hint frontmatter to all skills"
```

---

### Task 7: Fix Orphaned References and Minor Issues

**Files:**
- `plugins/rad-seo-optimizer/references/google-ranking-systems.md` — add reference from a skill
- `plugins/rad-brainstormer/references/domain-research-guide.md` — add reference from agent or skill
- `plugins/rad-brainstormer/.claude-plugin/plugin.json` — add license field
- `plugins/rad-seo-optimizer/.claude-plugin/plugin.json` — add license field

- [ ] **Step 1: Reference google-ranking-systems.md from full-seo-audit or technical-seo**

Add a line like: "For background on Google's ranking systems, consult `references/google-ranking-systems.md`."

- [ ] **Step 2: Reference domain-research-guide.md from domain-researcher agent**

Add a line to `agents/domain-researcher/AGENT.md` referencing `references/domain-research-guide.md`.

- [ ] **Step 3: Add license to plugin.json files**

Add `"license": "MIT"` (or appropriate license) to both plugin manifests.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "chore: fix orphaned references and add license to plugin manifests"
```

---

### Task 8: Validate and Test

- [ ] **Step 1: Run structural validation**

Verify all skills are discoverable:
```bash
# Every skill directory should contain SKILL.md at its root
find plugins/*/skills/ skills/ -maxdepth 2 -name "SKILL.md" | sort

# No commands/ directories should remain
find plugins/ -type d -name "commands" | sort
```

- [ ] **Step 2: Validate all frontmatter**

For each SKILL.md, verify:
- `name` field exists and matches directory name
- `description` field exists, uses third-person, includes trigger phrases
- `allowed-tools` is space-delimited (not YAML list)
- No unknown/non-standard frontmatter fields

- [ ] **Step 3: Validate all cross-references**

For each SKILL.md that references another skill or reference file, verify the target exists.

- [ ] **Step 4: Word count check**

Verify no SKILL.md exceeds 500 lines or 3000 words after extractions.

- [ ] **Step 5: Test plugin loading**

```bash
claude --plugin-dir plugins/rad-brainstormer
claude --plugin-dir plugins/rad-seo-optimizer
```

Verify skills appear in the skill list and trigger on expected phrases.

- [ ] **Step 6: Commit any fixes from validation**

```bash
git add -A
git commit -m "fix: address issues found during validation pass"
```

---

## Execution Order and Dependencies

```
Task 1 (Critical blockers)
    |
    v
Task 2 (Descriptions) ──> Task 3 (Migrate commands)
    |                          |
    v                          v
Task 4 (Writing style) ──> Task 5 (Progressive disclosure)
                               |
                               v
                          Task 6 (Frontmatter fields)
                               |
                               v
                          Task 7 (Minor fixes)
                               |
                               v
                          Task 8 (Validate & test)
```

Tasks 2 and 3 can run in parallel after Task 1.
Tasks 4 and 5 can run in parallel after Task 2.
Tasks 6 and 7 can run in parallel after Task 5.
Task 8 must run last.

## Estimated Scope

- **Files to modify:** ~35
- **Files to create:** ~8 (5 new technique skills, 1 fix-seo skill, ~2 new reference files)
- **Files to delete:** ~13 (all command files + 2 commands directories)
- **Total commits:** 7-8
