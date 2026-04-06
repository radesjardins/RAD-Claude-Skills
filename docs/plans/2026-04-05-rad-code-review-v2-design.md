# rad-code-review v2.0 — Design Spec

> Created: 2026-04-05
> Status: Approved
> Approach: Scope-First (Approach 2)

## Summary

Upgrade rad-code-review from v1.0 to v2.0, deployed as a separate `skills/rad-code-review-v2/` directory (fully self-contained, no dependency on v1.0 files). The upgrade addresses four workflow gaps and three detection heuristic gaps identified through competitive analysis (TuringMind, CodeRabbit, anthroos) and cross-pollination from rad-react, rad-nextjs, rad-typescript, and rad-a11y plugins.

## Changes from v1.0

### Workflow Enhancements

#### 1. Git Blame / `--diff-only` Mode (Default for diff/commit scopes)

**Behavior:** When scope is `diff` or `commit`, the orchestrator runs `git diff` and `git blame` *before* spawning the reviewer subagent. The subagent receives:
- Changed files with change annotations (`+` lines highlighted)
- Surrounding context (unchanged lines for comprehension)
- Blame metadata indicating which lines were changed in this diff vs pre-existing

The subagent is instructed to **only flag issues on changed lines** unless the change introduces a dependency on pre-existing broken code (e.g., a new function calls an existing function that has a SQL injection vulnerability).

For `repo` and `tree` scopes, full-scan behavior is unchanged.

**Implementation in orchestrator:**
- Step 3e (Scope File List): Add a new substep that runs `git diff -U5` to capture changed lines with context, and `git blame` on changed files to identify authorship
- Step 6 (Subagent Prompt): Add a `## Diff Context` section to the prompt with annotated diffs and a `## Blame-Aware Review Rules` section instructing the subagent on scoping behavior
- The `--diff-only` flag is implicit for `diff` and `commit` scopes. Users can override with `--full-scan` to get v1.0 behavior on these scopes.

#### 2. Incremental Review with `--since <commit>`

**Behavior:** Review all changes since a specific commit. Equivalent to `git diff <commit>..HEAD` but with blame-aware filtering.

**Implementation:**
- Step 0 (Parse Arguments): Add `--since <commit>` flag parsing
- When present, scope is computed as `git diff <commit>..HEAD --name-only` for file list, and `git diff <commit>..HEAD -U5` for annotated diffs
- All other workflow steps proceed as normal with the computed scope
- Report header includes the `--since` range for traceability

#### 3. Discoverability / Elevator Pitch

**The elevator pitch:** "3-role adversarial review with diff-aware scoping and AI slop detection — the only code reviewer that catches what AI wrote badly and only flags what you changed."

**Implementation:**
- SKILL.md `description` field: Updated with the elevator pitch and sharper trigger phrases
- README.md: Rewritten lead section with compelling positioning, comparison table
- Repo-level README.md: Updated standalone skills table entry
- docs/plugin-strategy.md: Cross-reference updated

### Detection Heuristic Upgrades

#### 4. Performance Profiling Heuristics

Add a new `references/performance-heuristics.md` with grep-able patterns for common performance anti-patterns:

- **N+1 queries:** Database call inside `.map()`, `.forEach()`, `for...of`, or `for` loop — `db.query(...)` or ORM method inside a loop body
- **Unnecessary re-renders (React):** Missing dependency arrays in useEffect, object/array literals in JSX props, inline function definitions in render
- **Unbounded list rendering:** `.map()` on a collection with no pagination, limit, or virtualization
- **Synchronous blocking:** `fs.readFileSync`, `execSync`, `requests.get` (Python) in request handlers
- **Missing pagination:** Database queries without `LIMIT`/`OFFSET` or cursor-based pagination
- **Bundle bloat indicators:** Importing entire libraries when tree-shakeable submodule imports exist (`import _ from 'lodash'` vs `import get from 'lodash/get'`)

Each pattern includes: grep command, detection heuristic, severity, and example bad/good code.

The primary review subagent prompt (Step 6, section 6 "Performance and Reliability") is updated to reference this file and apply these specific heuristics.

#### 5. IDOR Mutation Detection — Framework-Specific Heuristics

Add a new section to `references/security-checklist.md` as **Section 2.4: IDOR in Mutation Endpoints (Framework-Specific Heuristics)**.

Framework-specific patterns:

| Framework | Pattern to Detect | What's Missing |
|-----------|-------------------|----------------|
| Next.js Server Actions | `formData.get('id')` or `params.id` used in DB query | `where: { userId: session.user.id }` or equivalent ownership check |
| Next.js API Routes | `req.query.id` or `params.id` in route handler | Authorization check before `Model.findById()` |
| Express/Fastify | `req.params.id` in route handler for PUT/DELETE/PATCH | Ownership verification middleware or inline check |
| Django | `request.data['id']` or URL kwargs in view | `queryset.filter(user=request.user)` scoping |
| Rails | `params[:id]` in controller action | `current_user.resources.find(params[:id])` scoping |
| Go (net/http, Gin, Echo) | Path parameter extraction used in DB query | User ID from context/session joined in query |

Each pattern includes: specific grep pattern, detection heuristic for the reviewer, and concrete fix example.

#### 6. Hardcoded ARIA State Detection

Add a new subsection to `references/ux-accessibility-checklist.md` under **Section 4 (ARIA)** as **4.3: Dynamic ARIA States**.

Patterns to detect:
- `aria-expanded="true"` or `aria-expanded="false"` as string literals in JSX/HTML (should be dynamic: `aria-expanded={isOpen}`)
- `aria-selected="true"` as string literal (should reflect actual selection state)
- `aria-checked="true"` as string literal (should reflect actual checked state)
- `aria-pressed="true"` as string literal (should reflect actual pressed state)
- `aria-hidden="true"` on elements that are conditionally visible but the attribute never toggles

Detection heuristic: grep for `aria-(expanded|selected|checked|pressed|hidden)="(true|false)"` in JSX/TSX/HTML files. Each match is a probable hardcoded ARIA state that doesn't respond to user interaction.

Severity: Moderate (accessibility violation — screen readers announce incorrect state).

## Files to Create/Modify

### New directory: `skills/rad-code-review-v2/`

Full copy of v1.0 with the following modifications:

| File | Change |
|------|--------|
| `SKILL.md` | Updated description, elevator pitch, new flags (`--since`, `--full-scan`), version 2.0 |
| `README.md` | Rewritten with v2.0 positioning, comparison, new features |
| `ROADMAP.md` | Updated to reflect v2.0 as current, v1.0 items marked complete |
| `workflows/orchestrate-review.md` | Steps 0, 3e, 6, 8 modified for blame-aware scoping |
| `references/security-checklist.md` | New section 2.4 (IDOR framework-specific heuristics) |
| `references/ux-accessibility-checklist.md` | New section 4.3 (Dynamic ARIA States) |
| `references/performance-heuristics.md` | **New file** — performance detection patterns |

### Repo-level updates:

| File | Change |
|------|--------|
| `README.md` | Add v2.0 entry to standalone skills table |
| `docs/plugin-strategy.md` | Update rad-code-review reference to note v2.0 |

## What Does NOT Change

- All v1.0 files remain untouched
- Report format (same structured findings, same severity model)
- Fix application workflow
- Adversarial protocol
- Trust model
- Project-type modules
- Templates
- Scripts (dep-audit.sh, license-check.sh, secrets-scan.sh)
- GitHub Action workflow
- .ucrconfig.yml format

## Success Criteria

- [ ] v2.0 directory is fully self-contained (no file references to v1.0)
- [ ] `--diff-only` is default for diff/commit scopes
- [ ] `--since <commit>` flag works in argument parsing
- [ ] `--full-scan` flag overrides diff-only default
- [ ] Performance heuristics reference file exists with grep-able patterns
- [ ] IDOR section has framework-specific patterns for 6 frameworks
- [ ] ARIA state detection section covers 5 ARIA state attributes
- [ ] README elevator pitch is compelling and specific
- [ ] Repo-level README lists v2.0 alongside v1.0
- [ ] docs/plugin-strategy.md references v2.0
