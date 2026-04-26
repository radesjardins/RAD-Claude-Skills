---
name: scaffold-company
description: This skill should be used when the user says "scaffold a company", "set up workspace", "create company structure", "build company folder structure", "initialize agentic workspace", "create company hierarchy", "set up divisions", or wants to create a Claude Code workspace with hierarchical CLAUDE.md context files at each directory level. Be honest about what this creates: organized folders with context files, not a self-running company.
argument-hint: "[company-name] [--divisions engineering,product,operations,marketing,finance] [--root path] [--skip-divisions]"
user-invocable: true
allowed-tools: Read Glob Grep Write Edit Bash
---

# Scaffold a Claude Code Workspace

Create a folder hierarchy with CLAUDE.md context files at each level. Claude Code discovers CLAUDE.md files by walking upward from the current working directory, so a hierarchical folder structure becomes a hierarchical instruction set: company-wide rules at the root, division-specific conventions in the middle, project-specific instructions at the bottom.

**What this skill creates:** organized folders + context files + a sane permissions config.

**What this skill does NOT create:** any agent that operates marketing, finance, operations, or product. Those are filing organization. Agents come from `generate-agents` (engineering team) and `add-function-agent` (opt-in business functions where verified write-capable MCPs exist).

## Source of the patterns

- Hierarchical CLAUDE.md discovery: documented in [Claude Code Memory & CLAUDE.md docs](https://docs.claude.com/en/docs/claude-code/memory)
- Permission allow/deny patterns: [Claude Code Settings reference](https://docs.claude.com/en/docs/claude-code/settings)
- Folder organization conventions: opinionated by this plugin's author. Reasonable defaults; not Anthropic-canonical.

## Workflow

### Step 1: Gather requirements

Use `$ARGUMENTS` if provided, otherwise ask:

1. **Company name** — used for root directory and CLAUDE.md identity (e.g., `radorigin`, `acmecorp`)
2. **Root location** — default: user's home directory; user may override
3. **Divisions** — which division folders to create. Default set: `engineering`, `product`, `operations`, `marketing`, `finance`. **These are filing organization** — they get CLAUDE.md context files describing the division's purpose, but no agents until you opt in via `add-function-agent`.
4. **Primary tech stack** — for the engineering CLAUDE.md (e.g., "Next.js, React, TypeScript, PostgreSQL")
5. **Team context** — solo founder vs. team; affects CLAUDE.md tone but not structure

### Step 2: Create directory structure

```
{company}/
├── CLAUDE.md                          # Company-wide context
├── .claude/
│   ├── settings.json                  # Permissions allow/deny
│   └── rules/
│       ├── code-standards.md
│       └── security-policy.md
├── engineering/
│   ├── CLAUDE.md                      # Engineering division context
│   └── (projects added via scaffold-project)
├── product/                           # Optional, --skip-divisions to omit
│   ├── CLAUDE.md
│   ├── roadmaps/
│   ├── specs/
│   └── user-research/
├── operations/                        # Optional
│   ├── CLAUDE.md
│   ├── runbooks/
│   ├── infrastructure/
│   └── vendor-docs/
├── marketing/                         # Optional
│   ├── CLAUDE.md
│   ├── content/
│   ├── campaigns/
│   └── brand/
└── finance/                           # Optional
    ├── CLAUDE.md
    ├── invoices/
    ├── projections/
    └── tax/
```

The non-engineering division folders are **organizational only** until you add a function-specific agent for that division (e.g., `/rad-agentic-company-builder:add-function-agent --function bookkeeping` puts a bookkeeping-agent under `finance/.claude/agents/`).

### Step 3: Generate CLAUDE.md files

Load `references/claude-md-templates.md` and create a CLAUDE.md at each level.

**Company root CLAUDE.md should include:**
- Identity block (company name, structure, team size)
- Universal rules (branch policy, secrets policy, test-before-complete, root-cause-over-patches)
- Code style standards (strict TypeScript, named exports, function/file length limits, actionable errors) — these are opinions; mark as such or omit if you disagree
- Communication standards (completion reports, blocker reporting)

**Division CLAUDE.md files should include:**
- Division purpose
- Conventions and workflows specific to that division
- Note about which function-agents (if any) operate in this division

Keep each file under 200 lines. The Anthropic threshold is "frontier LLMs reliably follow 150–200 instructions"; bloated context files degrade reliability.

### Step 4: Generate settings and rules

**`.claude/settings.json`** at company root:
- `permissions.allow` — safe commands the user shouldn't have to approve every time (`git status`, `npm test`, etc.)
- `permissions.deny` — dangerous patterns (`rm -rf /`, `curl ... | bash`, reads of `.env`)
- `env.NODE_ENV: development` (override per-project as needed)

**`.claude/rules/code-standards.md`** and **`.claude/rules/security-policy.md`** — opinionated but useful starting points; the user owns them after generation.

### Step 5: Run the structure validator

```bash
python3 ${plugin_root}/scripts/audit-structure.py <root> --skip-projects --skip-hooks --skip-mcp --skip-agents
```

This catches: missing CLAUDE.md files, JSON syntax errors in settings.json, malformed structure. The skip flags are because nothing else exists yet — the validator is just confirming the foundation.

If clean, report what was created. If not, surface the findings before declaring done.

### Step 6: Report and next steps

Tell the user:

```
Workspace scaffolded at <path>.

What's there now:
- Hierarchical CLAUDE.md at company root + each division
- Permission allow/deny defaults
- Folder organization for engineering + (optional) other divisions

What's NOT there yet:
- No agents (run: generate-agents for the engineering team)
- No projects (run: scaffold-project to add one)
- No MCP integrations (run: configure-mcp)
- No hooks (run: configure-hooks)
- No business-function agents (run: add-function-agent --function <name>)

The non-engineering divisions are folder organization only. They have no agents or MCP wiring unless you explicitly add them.
```

## Mode flags

- `--divisions <list>` — Comma-separated. Default: `engineering,product,operations,marketing,finance`.
- `--skip-divisions` — Skip all non-engineering divisions. Useful if you only want the engineering scaffold.
- `--root <path>` — Where to create the company directory. Default: user's home directory.

## What this skill does NOT do

- Does not create agents (use `generate-agents` or `add-function-agent`).
- Does not configure hooks (use `configure-hooks`).
- Does not configure MCP integrations (use `configure-mcp` or `add-function-agent`).
- Does not enforce that the user actually uses the structure — Claude Code respects whatever folder organization you have, this skill just creates a starting point.
- Does not pretend the marketing/ folder is an "AI-driven marketing division." It's a folder. Treat it as filing.

## Reference

- `references/claude-md-templates.md` — Complete CLAUDE.md content templates for company root and each division
