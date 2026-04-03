---
name: scaffold-company
description: This skill should be used when the user says "scaffold a company", "create agentic company", "set up company structure", "build company folder structure", "initialize agentic workspace", "create company hierarchy", "set up divisions", or wants to create the full agentic company directory layout with CLAUDE.md files at every level. Also triggers on "agentic bible setup" or "company architecture".
argument-hint: "[company-name] [--divisions engineering,product,operations,marketing,finance]"
user-invocable: true
---

# Scaffold Agentic Company Structure

Create a complete agentic company folder hierarchy following the architecture from The Agentic Bible 2026. The structure uses CLAUDE.md files at every directory level to provide scoped agent context — company-wide rules at the root, division-specific conventions in the middle, and project-specific instructions at the bottom.

## Core Architecture Principle

Claude Code discovers CLAUDE.md files by walking **upward from the current working directory** to the filesystem root. A hierarchical folder structure directly translates into a hierarchical instruction set. The folder tree IS the org chart for agents.

## Scaffolding Process

### Step 1: Gather Requirements

Collect from the user (use `$ARGUMENTS` if provided, otherwise ask interactively):

1. **Company name** — used for root directory and CLAUDE.md identity (e.g., "radorigin", "acmecorp")
2. **Root location** — where to create the company directory (default: user's home directory)
3. **Divisions** — which divisions to create. Standard set:
   - `engineering/` — Software development
   - `product/` — Specs, roadmaps, user research
   - `operations/` — Infrastructure, DevOps, runbooks
   - `marketing/` — Content, campaigns, brand
   - `finance/` — Invoices, projections, tax
4. **Founder/team context** — solo founder or team size (affects CLAUDE.md tone)
5. **Primary tech stack** — used in engineering CLAUDE.md (e.g., "Next.js, React, TypeScript, PostgreSQL")

### Step 2: Create Directory Structure

Generate the full tree using Bash:

```
{company}/
├── CLAUDE.md
├── .claude/
│   ├── settings.json
│   └── rules/
│       ├── code-standards.md
│       └── security-policy.md
├── engineering/
│   ├── CLAUDE.md
│   └── (projects added via scaffold-project skill)
├── product/
│   ├── CLAUDE.md
│   ├── roadmaps/
│   ├── specs/
│   └── user-research/
├── operations/
│   ├── CLAUDE.md
│   ├── runbooks/
│   ├── infrastructure/
│   └── vendor-docs/
├── marketing/
│   ├── CLAUDE.md
│   ├── content/
│   ├── campaigns/
│   └── brand/
└── finance/
    ├── CLAUDE.md
    ├── invoices/
    ├── projections/
    └── tax/
```

### Step 3: Generate CLAUDE.md Files

Create a CLAUDE.md at each level with appropriate content:

**Company root CLAUDE.md** must include:
- Identity block (company name, structure, team size)
- Universal rules (branch policy, secrets policy, test-before-complete, root-cause-over-patches)
- Code style standards (strict TypeScript, named exports, function/file length limits, actionable errors)
- Communication standards (completion reports, blocker reporting)

**Division CLAUDE.md files** must include:
- Division identity and purpose
- Division-specific conventions and workflows
- Scoped rules that only apply when agents work inside that division

Refer to `references/claude-md-templates.md` for complete template content for each division.

### Step 4: Generate Settings and Rules

**`.claude/settings.json`** at company root:
- Permission allow-list for safe commands (git, npm, node, standard file ops)
- Permission deny-list for dangerous patterns (rm -rf /, curl pipe bash, .env reads)
- NODE_ENV=development default

**`.claude/rules/code-standards.md`**:
- TypeScript strict mode, no `any` types
- Named exports preferred
- Function/file length limits
- Conventional commits format

**`.claude/rules/security-policy.md`**:
- Never expose secrets in code or logs
- Parameterized queries only
- Input validation at boundaries
- CORS restricted in production

### Step 5: Report and Next Steps

After scaffolding, summarize what was created and suggest next steps:
1. Run `scaffold-project` to add projects within engineering/
2. Run `generate-agents` to populate agent definitions
3. Run `configure-hooks` to set up quality gates

## Additional Resources

### Reference Files

- **`references/claude-md-templates.md`** — Complete CLAUDE.md content templates for company root and all five divisions
