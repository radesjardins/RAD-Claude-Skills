# Changelog

All notable changes to `rad-coolify-orchestrator` will be documented in this file.

## [2.0.0] - 2026-04-27

### Added (mechanism)
- `scripts/lint-dockerfile.py` — Coolify-specific Dockerfile linter (unpinned base, missing USER/EXPOSE/HEALTHCHECK, secret-shaped ARGs/ENVs, single-stage warning, COPY . reminder)
- `scripts/lint-compose.py` — Coolify-specific docker-compose validator (missing healthchecks/restart, hardcoded secrets, privileged mode, port conflicts with Coolify reserved ports 80/443/8000, stateful services without volumes)
- `scripts/check-coolify-env.py` — env handling validator (.env in git, .gitignore gaps, hardcoded secrets across files, Nixpacks version-pin gap)
- `scripts/audit-cicd.py` — CI/CD validator (curl without --fail, hardcoded webhook URLs/tokens, :latest image tags, missing test gate, missing post-deploy status check)
- `scripts/README.md` — full script docs + when-the-agent-runs-which table
- All scripts pure stdlib Python 3.8+, end-to-end tested against deliberately broken fixtures

### Updated (current Coolify state, April 2026)
- **Build packs:** Nixpacks flagged as in maintenance mode (Railway moved focus to Railpack in 2025); Railpack reframed from "available with opt-in" to "NOT yet a Coolify build pack option" (active community discussion #5282/#5519/#7983 but no merged PR)
- **Reverse proxy:** Caddy added as experimental alternative to Traefik (added at beta.237) — coolify-deploy SKILL covers both
- **Shared variables:** expanded to 4 scopes (server/team/project/environment) with `{{scope.VAR}}` interpolation syntax (beta.471, April 2026) — coolify-security SKILL updated
- **API token expiration:** new in beta.474 — coolify-cicd/api-reference.md updated
- **PostgreSQL 18 + pgvector 18:** added in beta.463 (Feb 2026) — coolify-databases SKILL updated
- **Webhook canonical method is GET** per Coolify's own docs (POST also works) — coolify-cicd SKILL updated to show both
- **HMAC webhook signing strengthened** in beta.474 — noted in coolify-cicd
- **Old container accumulation in Swarm rolling updates** (Issue #8299, Feb 2026) — bug noted in swarm-guide.md

### Honest framing pass
- **"Zero-downtime"** reframed in coolify-deploy SKILL with explicit conditions (single-container only, no host port bindings, working healthcheck, attachable volumes; recreate strategy fallback when conditions fail)
- **Sentinel** explicitly framed as "lightweight metrics side-car, not full observability" in coolify-observability SKILL — clarifies CPU/RAM/disk/network only, no log aggregation, no tracing, no APM
- **API stability caveats** added to coolify-cicd/api-reference.md (Issues #7702, #8782 — spec-vs-behavior gaps documented)
- **Coolify v4 is rolling beta** explicitly stated in coolify-deploy SKILL (latest is `v4.0.0-beta.474`, ~474 betas over 2 years, v4.0.0 stable milestone not closed)
- **Coolify Cloud disambiguation** in plugin description (managed product, $5/month + $3/server, out of scope for this plugin)
- **Coolify v5 in early development** noted (April 2025 announcement, full PHP rewrite, no release date)
- **Docker Swarm itself supported through 2030** (Mirantis) — clarifies that the "experimental" label is about Coolify integration, not Swarm viability

### Updated (agent — Opus 4.7 platform pass)
- `coolify-reviewer` agent: **Opus 4.7 default** (with Sonnet 4.6 fallback note)
- New "Step 0: Run the deterministic validators" — agent invokes the four scripts before LLM judgment passes
- Steps 2-5 reframed as "judgment-only — script already covered structure"
- New JSON output mode (`--json`) for skill consumption alongside markdown for human reading
- Mechanism-first architecture documented at top of agent file

### Verified
- Bundled `@radoriginllc/coolify-mcp` confirmed published on npm at v1.0.0; 27 tools verified in source vs README
- All major technical claims (Sentinel, Swarm, UFW+Docker, API endpoints, database engines) re-verified against current Coolify docs and GitHub issues

## [1.0.0] - 2026-04-03

### Added
- Initial release with 7 skills: deploy, databases, security, cicd, troubleshoot, observability, infrastructure
- coolify-reviewer agent for autonomous Coolify config/Dockerfile auditing
- Decision trees for build pack selection, database provisioning, troubleshooting flows
- Anti-pattern documentation for all domains
- Runnable commands and worked examples throughout
- Coverage report documenting research sources and confidence levels

### Notes
- All content verified against Coolify v4.x self-hosted
- Swarm and Railpack content marked as experimental
- Multi-server content sourced from official docs + community patterns
