# RAD Code Review — Roadmap

## v1.0

The foundation. A complete, production-ready code review skill.

- Full 10-category review (functional, security, AI slop, architecture, tests, performance, UX, accessibility, release readiness, documentation)
- 8 project-type modules (web app, API, Chrome extension, CLI, library, Electron, mobile, SaaS)
- Sequential adversarial review (dual-engine mode with Claude and Codex)
- Review-of-review calibration pass
- Fix application with build/test validation
- Structured JSON report with severity-ranked findings
- Report history and comparison between runs
- `.ucrconfig.yml` project-level configuration
- GitHub Action for CI/CD (PR comments, check runs, artifact upload)
- Local-only mode (no network dependencies)
- Dependency vulnerability audit (npm, yarn, pnpm, pip, cargo, go, gem, composer)
- License compliance checking with copyleft detection
- Secrets scanning (gitleaks + pattern fallback, never exposes values)
- Cross-platform install (bash + PowerShell)

## v2.0 (current)

Diff-aware scoping, actionable detection heuristics, and practical PR workflow support.

- **Blame-aware diff scoping** — `diff` and `commit` scopes only flag issues on changed lines by default, with dependency chain detection for pre-existing issues that new code depends on
- **Incremental review (`--since <commit>`)** — review all changes since a specific commit, with blame-aware filtering
- **`--full-scan` override** — opt out of blame-aware filtering to get v1.0-style full review on any scope
- **Framework-specific IDOR detection** — concrete grep-able mutation ownership patterns for Next.js Server Actions, Next.js API Routes, Express/Fastify, Django/DRF, Rails, and Go (Gin/Echo/Chi/net/http), plus multi-tenant isolation checks
- **Performance profiling heuristics** — new reference file with 8 detection patterns: N+1 queries in loops, unnecessary React re-renders, unbounded list rendering, synchronous blocking in handlers, missing pagination, bundle bloat indicators, missing caching, missing database indexes
- **Dynamic ARIA state detection** — catches hardcoded `aria-expanded`, `aria-selected`, `aria-checked`, `aria-pressed`, and frozen `aria-hidden` as string literals instead of dynamic values
- **Finding attribution** — every finding tagged as `introduced`, `pre-existing-dependency`, or `pre-existing-secret` for clear signal in PR review workflows
- **Adversarial blame validation** — adversarial pass now verifies blame-scoping decisions to catch issues that were incorrectly filtered or incorrectly included
- **Updated elevator pitch and discoverability** — sharper skill description, better trigger phrases, compelling README positioning

## v2.1 (planned)

Deeper domain-specific review capabilities.

- **Interactive findings management** — Numbered end-of-review menu with accept, fix, and filter options. Accept specific findings or all minor findings as intentional; they are persisted to `.ucrconfig.yml` with expiry dates and optional justification notes. Show-new-only mode filters the current report against `.ucr/history/` to surface only findings introduced since the last review. First-run `.ucrconfig.yml` creation with optional `.gitignore` integration.
- **Threat model mode** — Given an architecture description or diagram, enumerate attack surfaces, trust boundaries, and data flow risks. Produce a lightweight threat model alongside the code review.
- **API contract review** — Validate that implementation matches OpenAPI/Swagger schema. Detect undocumented endpoints, missing error responses, request/response type mismatches, and breaking changes between schema versions.
- **Schema/migration review** — Analyze database migrations for: data loss risk, missing rollback, index performance, constraint correctness, and compatibility with ORM models. Support for SQL migrations, Prisma, Alembic, ActiveRecord, and Flyway.
- **Infra/deploy config deep review** — Extended analysis of Dockerfiles, Kubernetes manifests, Terraform/Pulumi configs, CI/CD pipelines, and cloud IAM policies.

## v3.0 (planned)

Interactive and visual review capabilities, plus extensibility.

- **Accessibility deep-dive mode** — Interactive accessibility audit using Playwright to render pages, run axe-core, check keyboard navigation, verify ARIA attributes, test screen reader compatibility, and validate color contrast.
- **UI/UX teardown mode** — Visual analysis via screenshots. Review layout consistency, spacing, typography hierarchy, interactive element sizing, loading states, error states, empty states, and responsive breakpoints.
- **Performance-focused mode** — Integrate with profiling data (Lighthouse, webpack-bundle-analyzer, py-spy, Go pprof) to correlate code patterns with measured performance characteristics.
- **Custom project-type module support** — User-defined project-type modules in `.ucr/project-types/` that extend or override built-in modules.
- **Plugin system for custom checks** — Define custom review rules as small scripts or prompt fragments.

## v4.0 (future)

Cross-service intelligence and continuous operation.

- **Multi-repo/monorepo cross-service analysis** — Review changes in context of the full service graph.
- **Runtime behavior verification integration** — Correlate code review findings with runtime data from APM tools.
- **Production incident correlation** — Given a post-mortem, trace root cause back to specific code patterns.
- **Continuous review mode** — Watch for code changes and run incremental reviews automatically.
