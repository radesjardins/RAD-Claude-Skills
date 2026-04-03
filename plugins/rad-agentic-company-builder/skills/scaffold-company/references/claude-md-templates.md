# CLAUDE.md Templates

Complete templates for each level of the agentic company hierarchy. Replace `{COMPANY}` with the actual company name, `{ROLE}` with team description.

---

## Company Root — `{COMPANY}/CLAUDE.md`

```markdown
# {COMPANY} — Global Development Standards

## Identity
Working for {COMPANY}. {ROLE_DESCRIPTION}.
All code must be production-quality on first review.

## Universal rules
- NEVER commit directly to main. Always work on feature branches.
- NEVER expose secrets, API keys, or credentials in code or logs.
- NEVER delete or modify existing tests without explicit instruction.
- NEVER use force-push on shared branches.
- Always run the project's test suite before declaring work complete.
- When encountering an error, find the root cause. Do not patch symptoms.
- Prefer small, focused commits with descriptive messages (conventional commits format).
- If a task is ambiguous, write interpretation in a comment before implementing.

## Code style
- TypeScript strict mode everywhere. No `any` types except in test mocks.
- Prefer named exports over default exports.
- Functions under 40 lines. Files under 300 lines. Extract when exceeded.
- Error messages must be actionable: state what happened, why, and how to fix it.

## Communication
- When reporting work completion, include: what changed, what was tested, what risks remain.
- If unable to complete a task, explain specifically what blocked and what information would unblock.
```

---

## Engineering Division — `engineering/CLAUDE.md`

```markdown
# Engineering Division — {COMPANY}

## Purpose
Software development division. All application projects live here.

## Conventions
- Every project uses the wrapper/repo pattern (management context above git, dev instructions inside git)
- Shared packages live in `shared-packages/` for cross-project code
- Code review is mandatory before merge — use the reviewer agent
- All projects must have CI/CD configured before first production deploy

## Project structure
Each project follows:
- `{project}/CLAUDE.md` — Project management context (sprint goals, architecture decisions)
- `{project}/task-specs/` — Agent task specifications
- `{project}/repo/` — Git boundary (actual source code)
- `{project}/artifacts/` — Cowork output staging area

## Standards
- Test coverage minimum: 80% on changed files
- All PRs require passing CI before merge
- Database migrations must be reversible
- API changes must update shared type definitions
```

---

## Product Division — `product/CLAUDE.md`

```markdown
# Product Division — {COMPANY}

## Purpose
Product specifications, roadmaps, and user research.

## Conventions
- Roadmaps organized by quarter in `roadmaps/`
- Feature specs in `specs/` with standardized format: Problem, Proposed Solution, Success Metrics, Open Questions
- User research artifacts in `user-research/` organized by study
- All specs must reference the roadmap item they support

## File formats
- Roadmaps: Markdown with timeline tables
- Specs: Markdown following the template in `specs/TEMPLATE.md`
- Research: Markdown summaries with links to raw data
```

---

## Operations Division — `operations/CLAUDE.md`

```markdown
# Operations Division — {COMPANY}

## Purpose
Infrastructure, DevOps, and vendor management.

## Conventions
- Runbooks in `runbooks/` must be copy-pasteable — every command tested
- Infrastructure configs documented in `infrastructure/`
- Vendor documentation and contracts in `vendor-docs/`
- Incident response follows the runbook at `runbooks/incident-response.md`

## Safety rules
- NEVER modify production infrastructure without a rollback plan
- All infrastructure changes go through code review
- Database backups verified weekly
- Credentials rotated on schedule (see credential rotation policy)
```

---

## Marketing Division — `marketing/CLAUDE.md`

```markdown
# Marketing Division — {COMPANY}

## Purpose
Content creation, campaigns, and brand management.

## Conventions
- Blog drafts in `content/blog-drafts/` — one file per post
- Campaign materials in `campaigns/` organized by campaign name
- Brand assets and style guide in `brand/`
- All public-facing content must align with `brand/style-guide.md`

## Content standards
- Blog posts: 800-2000 words, actionable, include code examples where relevant
- Social media: Match brand voice from style guide
- Documentation: Technical accuracy prioritized over marketing language
```

---

## Finance Division — `finance/CLAUDE.md`

```markdown
# Finance Division — {COMPANY}

## Purpose
Financial tracking, projections, and tax documentation.

## Conventions
- Invoices in `invoices/` organized by year and month
- Financial projections in `projections/` by quarter
- Tax documents in `tax/` by tax year
- All financial data is CONFIDENTIAL — never include in commits or logs

## Security
- Financial files must NEVER be committed to git repositories
- No financial data in CLAUDE.md files that might be committed
- Access to this division should be restricted to authorized personnel only
```

---

## `.claude/settings.json` — Company Root Settings

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Read(~/.ssh/config)",
      "Bash(git *)",
      "Bash(npm run *)",
      "Bash(npx *)",
      "Bash(node *)",
      "Bash(cat *)",
      "Bash(ls *)",
      "Bash(head *)",
      "Bash(tail *)",
      "Bash(wc *)",
      "Bash(grep *)",
      "Bash(find *)",
      "Bash(echo *)",
      "Bash(mkdir *)",
      "Bash(cp *)",
      "Bash(mv *)"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(rm -rf ~)",
      "Bash(curl * | bash)",
      "Bash(wget * | bash)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(~/.aws/credentials)"
    ]
  },
  "env": {
    "NODE_ENV": "development"
  }
}
```

---

## `.claude/rules/code-standards.md`

```markdown
---
globs: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
---
# Code Standards

- TypeScript strict mode. No `any` types except in test mocks.
- Prefer named exports over default exports.
- Functions under 40 lines. Files under 300 lines.
- Error messages must be actionable.
- Use conventional commits: feat:, fix:, chore:, refactor:, test:, docs:
```

---

## `.claude/rules/security-policy.md`

```markdown
# Security Policy

- Never expose secrets, API keys, or credentials in code or logs
- All user input validated at API boundaries (Zod schemas recommended)
- Parameterized queries only (ORMs handle this)
- CORS restricted to known origins in production
- Rate limiting on authentication endpoints
- No raw SQL except in migration files
```
