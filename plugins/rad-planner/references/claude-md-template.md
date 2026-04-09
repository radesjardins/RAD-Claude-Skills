# CLAUDE.md Generation Template

CLAUDE.md is a "Contract of Intent" -- not documentation. Keep it under 200 lines. Test every line with: "If I remove this, will the AI make a mistake?" If no, cut it.

## Structure: WHY / WHAT / HOW

### Section 1: Project Description (WHY)
```markdown
# [Project Name]

[1-2 sentences: what this project does and the core problem it solves]

**Stack:** [Frontend] + [Backend] + [Database] + [Key libraries]
**Status:** [Active development | Maintenance | MVP | Production]
```

### Section 2: Architecture (WHAT)
```markdown
## Architecture

[High-level directory map -- only non-obvious structure]

src/
  api/          # API route handlers
  components/   # React components (atomic design)
  lib/          # Shared utilities and helpers
  db/           # Database schema, migrations, seeds
  middleware/   # Request middleware (auth, logging)

**Key patterns:**
- [Pattern 1, e.g., "Repository pattern for data access"]
- [Pattern 2, e.g., "Server Components by default, Client only when needed"]
```

### Section 3: Libraries and Constraints (WHAT)
```markdown
## Stack Rules

**Use:**
- [Library A] for [purpose]
- [Library B] for [purpose]

**Do NOT use:**
- [Library C] — [reason, e.g., "deprecated, use Library A instead"]
- [Pattern D] — [reason]
```

### Section 4: Repo Etiquette (HOW)
```markdown
## Workflow

**Branches:** `feat/[name]`, `fix/[name]`, `chore/[name]`
**Commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`)
**PRs:** Require description + test plan

## Commands

```bash
npm run dev          # Start dev server
npm run build        # Production build
npm test             # Run test suite
npm run lint         # Lint check
npm run db:migrate   # Run database migrations
npm run db:seed      # Seed development data
```
```

### Section 5: Standards and Guardrails (HOW)
```markdown
## Standards

- TypeScript strict mode, no `any` types
- All API routes must validate input with Zod
- All database queries through ORM (no raw SQL except migrations)
- Error handling: Result pattern, no try-catch for expected failures
- Functions max 50 lines, files max 300 lines

## DO NOT:
- Change API contracts without updating all consumers
- Commit .env files or hardcoded secrets
- Use `as` type assertions (use type guards instead)
- Skip tests for new features
- Use default exports (named exports only)
```

### Section 6: Context Links (Progressive Disclosure)
```markdown
## References

@docs/ARCHITECTURE.md — Read when: modifying system architecture
@docs/API.md — Read when: adding or modifying API endpoints
@docs/TESTING.md — Read when: writing tests or changing test infrastructure
```

## What to EXCLUDE (Token-Saving Rules)

Remove from CLAUDE.md if:
- **Standard language conventions** -- AI already knows TypeScript/Python/Go syntax
- **File-by-file descriptions** -- AI can read files dynamically with Glob/Read
- **Detailed API documentation** -- link to external docs, don't inline
- **Linter-enforced rules** -- spacing, indentation, formatting handled by tooling
- **Vague platitudes** -- "write clean code", "make it fast", "ensure security"
- **Volatile information** -- version numbers that change, feature flags, temporary state
- **Git history context** -- AI can run `git log` and `git blame`

## Formatting Rules

- Use **IMPORTANT** or **YOU MUST** for critical rules (increases adherence)
- Repeat critical instructions if AI consistently misses them
- Use bullet points, not paragraphs (scannable structure)
- Group rules by feature domain (backend, frontend, testing)
- Use code blocks for commands and patterns
- Maximum line count: 200 (absolute max: 300)

## Path-Scoped Rules (For Large Projects)

For codebases where different directories need different rules, generate `.claude/rules/*.md` files:

```yaml
---
description: React component conventions
paths: "src/components/**/*.tsx"
---

- Use Server Components by default
- Client Components only for interactivity (onClick, useState, useEffect)
- Colocate component, test, and styles in same directory
- Props interface named [ComponentName]Props
```

These load ONLY when Claude works on matching files, saving context in all other situations.
