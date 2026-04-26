# rad-agentic-company-builder

Structured Claude Code workspace scaffolding plus opt-in business-function agents — for the parts of "running a company with AI agents" that actually work in 2026.

## Read this first: what this plugin will NOT do

If you came here for the "AI runs your company" pitch, you came to the wrong plugin. The honest April-2026 reality:

- **Will not give you autonomous executive decision-making.** Strategy, prioritization, and hiring decisions stay with humans.
- **Will not run your sales pipeline end-to-end.** Multi-step autonomous sales workflows do not work reliably (CMU benchmark: best agents complete 24% of real office tasks; HBR / Gartner: 40%+ of agentic AI projects predicted cancelled by 2027).
- **Will not eliminate human-in-the-loop for legal, compliance, or regulated work.** Liability stays with humans.
- **Will not move money out of your bank account.** No production-quality MCPs exist for Mercury, Brex, or Ramp in April 2026.
- **Will not autonomously post to social media.** Buffer and Hootsuite have no MCP. The plugin's `social-drafts` function writes drafts to a folder; humans post.
- **Will not replace your existing IAM or governance.** Agent identity is an unsolved infrastructure problem (per ISACA 2025).
- **Will not magically scaffold "marketing/" or "finance/" agents** because you put folders by those names. Each business-function agent is opt-in via `/rad-agentic-company-builder:add-function-agent`, requires a verified write-capable MCP, and ships with explicit "what this will NOT do" constraints.

If you want a marketing pitch, you can find it elsewhere. If you want a Claude Code workspace scaffold + a small set of opt-in agents that work where the integration actually exists, keep reading.

## What this plugin DOES do

1. **Scaffolds a Claude Code workspace** with hierarchical CLAUDE.md context files, sensible permission defaults, and folder organization for engineering work + optional placeholders for non-engineering content (the placeholders are filing organization, not agents).
2. **Generates a 6-agent engineering team** with tool-restricted role specialization (architect / implementer / reviewer / tester / deployer / docs-writer). This is a real, usable pattern for engineering work.
3. **Configures Claude Code hooks** against the actual documented event list — and ships a `validate-hooks.py` script that catches fictional event names before they end up in your `settings.json`.
4. **Configures MCP server integrations** for verified-working servers (GitHub, Coolify, Postgres, Workspace, Stripe, etc.) — and ships a `check-mcp-config.py` script that catches hardcoded secrets, wrong env-var syntax, and missing transport definitions.
5. **Adds opt-in business-function agents** (`/rad-agentic-company-builder:add-function-agent --function billing`) for the categories where a verified write-capable MCP exists in 2026: billing, bookkeeping, support-tier1, recruiting, compliance, CRM ops, contracts, analytics, marketing-email, web-CMS, and social-drafts. Each function ships with an explicit scope contract listing what it will and won't do.
6. **Audits an existing scaffold** mechanically (via `audit-structure.py`) — concrete pass/fail per check, not "score 7/10."
7. **Documents agentic operations honestly** — token costs, context compaction, headless mode, Routines (cloud-scheduled), failure recovery — citing actual Anthropic documentation, with the deprecated and fictional bits clearly removed.

## The honest capability map for business-function agents

Based on April-2026 MCP server availability:

**Write-capable today (agent can act, with human-in-the-loop for high-impact actions):**
Stripe, HubSpot, Salesforce, Close, Pipedrive, QuickBooks, Xero, Greenhouse, Lever, Mailchimp, Customer.io, Webflow, Slack, Notion, Linear, Asana, Monday, Google Workspace (workspace-mcp), DocuSign, Vanta, Drata, Mixpanel, Amplitude, PostHog, Google Analytics, Meta Ads, Google Ads.

**Read-only or no integration (agent cannot act):**
Mercury, Brex, Ramp (banking — biggest gap), Rippling (HRIS), Buffer / Hootsuite (social scheduling), Help Scout, Zendesk (acts as MCP client only), Ironclad CLM, Apollo (no first-party MCP), Deel (read-only), most clinical/healthcare systems.

**This map is the whole product story.** Every claim the plugin makes is bounded by this map.

## Skills

| Skill | Trigger | What it does |
|---|---|---|
| `/rad-agentic-company-builder:scaffold-company` | "scaffold a company", "set up workspace" | Creates folder hierarchy with CLAUDE.md files at each level; configures company-root `.claude/settings.json` |
| `/rad-agentic-company-builder:scaffold-project` | "scaffold a project", "add a project" | Adds an engineering project with the documented Claude Code conventions; `--wrapper` flag opts into the wrapper/repo layout (with explicit warnings about tooling assumptions) |
| `/rad-agentic-company-builder:generate-agents` | "generate agents", "set up engineering team" | Generates the 6 engineering agents (architect/implementer/reviewer/tester/deployer/docs-writer) with tool restrictions per role |
| `/rad-agentic-company-builder:generate-skills` | "generate skills", "add project skills" | Generates 4 standard project skills (sprint-cycle, api-design, release-prep, daily-standup) |
| `/rad-agentic-company-builder:configure-hooks` | "configure hooks", "set up quality gates" | Configures Claude Code hooks against documented events; runs `validate-hooks.py` after writing |
| `/rad-agentic-company-builder:configure-mcp` | "configure MCP", "add integrations" | Configures MCP server entries; runs `check-mcp-config.py` after writing |
| **`/rad-agentic-company-builder:add-function-agent`** | "add a billing agent", "add a bookkeeping agent", etc. | **NEW in 2.0.** Opt-in business-function agent scaffolding. One function at a time, only where a verified write-capable MCP exists, with explicit scope contracts. |
| `/rad-agentic-company-builder:agentic-operations` | "daily ops", "token optimization", "headless mode" | Reference guide — corrected in 2.0 for Routines, deprecated headers, and `/loop` semantics |

## Agent

| Agent | Purpose |
|---|---|
| `company-auditor` | Runs `audit-structure.py` first, then applies LLM judgment to anything mechanical checks can't cover. Reports pass/fail per check — no subjective 1-10 scores. |

## Scripts (the mechanism)

What earlier versions claimed but didn't enforce, these scripts now actually check:

| Script | What it catches |
|---|---|
| `scripts/audit-structure.py` | Missing CLAUDE.md, invalid JSON in settings/MCP, malformed agent frontmatter, fictional hook events at scale |
| `scripts/validate-hooks.py` | Hook events that don't exist in Claude Code's documented event list (the previous version of this plugin shipped four fictional events) |
| `scripts/check-mcp-config.py` | JSON syntax, missing transport, hardcoded secrets, `$VAR` vs `${VAR}` confusion, Windows npx wrapping |

Pure stdlib Python 3.8+. No `pip install` required.

## What changed in 2.0

This is a major release because the framing changed.

### Removed (fabrication / wrong claims)
- **"The Agentic Bible 2026"** — referenced 8+ times in the previous version as a canonical authority. **It does not exist** as a public reference. Every reference has been removed and replaced with citations to actual Anthropic documentation.
- **Fictional hook events** — `PostToolUseFailure`, `SubagentStart`, `Setup`, `InstructionsLoaded` — none of these exist in Claude Code. Removed from `hook-patterns.md`. The `validate-hooks.py` script catches them if a user adds them anyway.
- **Deprecated header recommendation** — `token-efficient-tools-2025-02-19` is a no-op on Claude 4+ models per Anthropic's current docs. Removed.
- **Wrong Cowork claims** — the previous version said "computer must be awake, Desktop open, missed runs catch up on wake." Cowork is now called **Routines**, runs on Anthropic-managed cloud infrastructure, and keeps working when your laptop is closed. Section rewritten.
- **`/loop` cron / expiration / jitter claims** — `/loop` is in-session polling with simple intervals (e.g., `/loop 5m`). Cron support is `/schedule` (Routines), a different feature. Fixed.
- **"Standard 6-agent team" framing** — these are reasonable starting agents, not industry-standard convergence. Reframed as "six engineering roles you can use as a starting point."

### Reframed (was misleading, now accurate)
- **Plugin description** changed from "AI-agent-driven company infrastructure" to "Claude Code workspace scaffolding + opt-in business-function agents (where MCP exists)."
- **Division placeholders** are now explicitly acknowledged as filing organization, not agent capability. The marketing/finance/operations folders get CLAUDE.md context files but no agents until you opt in via `add-function-agent`.
- **Wrapper/repo pattern** — was previously presented as canonical. Now explicitly opt-in via `--wrapper` flag, with warnings that it breaks `gh` CLI, IDE git integration, Dependabot, and CI assumptions that project root = git root.
- **Cost figures** — the "$6/dev/day" number is sourced (it traces to Anthropic `/cost` telemetry) but Anthropic also publishes a `$13/active-day` enterprise figure. Both are now shown with caveat.
- **Auto mode "Sonnet classifier, 3 denials or 20 turns"** — those specific numbers aren't in Anthropic's docs. Reframed to describe the documented `--permission-mode auto` behavior only.

### Added (the new value)
- **`/rad-agentic-company-builder:add-function-agent`** — opt-in business-function agent scaffolding for the 11 functions where verified write-capable MCPs exist. Each function ships with a scope file (`<function>-scope.md`) that is the honesty contract: what the agent will and will NOT do, human-in-the-loop checkpoints, escalation rules, failure modes.
- **`scripts/audit-structure.py`** — converts the company-auditor's "score this 1-10" to deterministic pass/fail per check.
- **`scripts/validate-hooks.py`** — catches fictional hook events.
- **`scripts/check-mcp-config.py`** — catches secrets, wrong env-var syntax, missing transport.
- **The "Honest capability map" section above** — what works, what doesn't, anchored to actual MCP availability.

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-agentic-company-builder
```

Engineering scaffolding (the validated path):

```
Scaffold a workspace at ./acmecorp
Generate engineering agents
Configure GitHub and Postgres MCP
Configure quality-gate hooks
```

Add a single business-function agent (only after the engineering scaffold is in place):

```
Add a billing agent for the acmecorp project
```

Audit an existing scaffold:

```
Audit my workspace
```

## Sources and citations

The plugin's claims are now grounded in:

- **Claude Code official docs**: https://docs.claude.com/en/docs/claude-code/
- **Claude Code hooks reference**: https://docs.claude.com/en/docs/claude-code/hooks
- **Claude Code subagents**: https://docs.claude.com/en/docs/claude-code/subagents
- **Anthropic best practices**: https://code.claude.com/docs/en/best-practices
- **Routines (formerly Cowork)**: https://claude.ai/code/routines
- **MCP Registry (official)**: https://registry.modelcontextprotocol.io/
- **MCP Apps (Jan 2026)**: Anthropic announcement extending MCP to render UIs in Claude
- **Carnegie Mellon TheAgentCompany benchmark**: https://www.theregister.com/2025/06/29/ai_agents_fail_a_lot/ — the 24% task completion ceiling
- **Gartner agentic AI cancellation prediction**: https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027
- **Stripe MCP**: https://docs.stripe.com/mcp
- **HubSpot MCP**: https://developers.hubspot.com/mcp
- **Vanta MCP**: https://mcpservers.org/servers/VantaInc/vanta-mcp-server
- **DocuSign MCP**: https://developers.docusign.com/platform/mcp-server/

When the plugin makes a factual claim, it cites the source. When it states an opinion, it labels it as such.

## Requirements

- Claude Code CLI installed and authenticated
- **Python 3.8+** for the validator scripts. Without Python, the validators reduce to "templates the model is asked to follow" — i.e., the previous version's behavior.

## License

Apache-2.0
