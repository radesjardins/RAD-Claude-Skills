---
name: agentic-operations
description: This skill should be used when the user asks about "daily operating rhythm", "agentic operations", "token optimization", "credential rotation", "autonomous agent patterns", "headless mode", "agent failure recovery", "morning briefing", "agent monitoring", "context compaction strategy", "PARA methodology for agents", or wants guidance on running and maintaining an agentic company day-to-day.
user-invocable: true
---

# Agentic Company Operations Guide

Reference guide for the daily operating rhythm, autonomous execution patterns, cost optimization, and maintenance practices needed to run an agentic company effectively. Based on The Agentic Bible 2026.

## The Three-Checkpoint Daily Rhythm

### Morning Review (7:00-8:30 AM)
- Check overnight scheduled task results — verify output files exist with valid data
- Scan error logs via dashboards or `ccusage` CLI
- Run `/cost` or check Anthropic Console for overnight spend against daily budget
- Verify all MCP servers are responsive
- Check credential expiration dates (flag anything due within 7 days)
- Set the day's agent task queue based on results

### Midday Monitoring (12:00-1:00 PM)
- Watch running agents for stalls (no checkpoint heartbeat in >10 minutes)
- Monitor context window utilization (intervene before 85%)
- Check current session token burn rate
- Handle agents hitting errors or rate limits
- Kill zombie tasks and re-queue with adjusted parameters

### Evening Wrap-Up (5:00-6:00 PM)
- Assess quality of all agent output, accept or reject
- Review total daily token spend
- Queue overnight tasks using Batch API (50% discount) for non-urgent work
- Plan tomorrow's priority tasks

## Autonomous Execution Patterns

### Headless Mode (`-p` / `--print`)

Run Claude Code as a one-shot process for CI/CD, cron jobs, and scripted workflows:

```bash
claude -p "Implement the user profile endpoint from tasks/plans/user-profile.md" \
  --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "Bash(npm run *)" "Bash(git *)" \
  --max-turns 50 \
  --max-budget-usd 2.00 \
  --output-format json
```

Three permission strategies for autonomous runs:
1. `--allowedTools` whitelist — safest, explicit tool list
2. Auto mode (Sonnet classifier) — middle ground, 3 denials or 20 total terminates
3. `--dangerously-skip-permissions` — sandboxed environments only

### The `/loop` Command

Session-scoped recurring tasks:
- Syntax: `/loop <interval> <prompt>`
- Intervals: seconds (min 1m), minutes, hours, days
- Cron expressions: standard 5-field (`minute hour day month weekday`)
- Session-scoped: dies when terminal closes
- 3-day auto-expiration
- Up to 10% jitter on recurring tasks

### Fresh-Agent Iterative Pattern ("Ralph Wiggum")

Most reliable autonomous pattern: pick task -> implement -> validate (run tests) -> commit -> update status -> reset context -> repeat. A fresh agent is spawned each iteration to prevent context degradation. State is persisted through files (task list, CLAUDE.md, git history, test results).

## Token Cost Optimization

Average Claude Code cost: ~$6/developer/day (90% of users below $12).

### Strategies (60-80% reduction possible)

1. **Prompt caching** — cache read tokens cost 10% of standard input. Pays off after single read within 5-minute window.
2. **Model routing** — Sonnet for 80% of tasks, Opus only for architecture/review, Haiku for classification.
3. **Context hygiene** — `/clear` between unrelated tasks, `/compact` with custom instructions.
4. **Token-efficient tool use** — beta header `token-efficient-tools-2025-02-19`.
5. **Output constraints** — output tokens cost 5x input, so format constraints have outsized impact.

## Credential Rotation Schedule

| Credential | Rotation Period |
|-----------|----------------|
| Production API keys | 60-90 days |
| OAuth access tokens | 15-30 minutes (automatic) |
| OAuth refresh tokens | 7-14 days |
| MCP server credentials | 60-90 days |
| SSH keys | Annually (or on compromise) |

Automate via CI/CD. Implement grace periods (old + new keys valid simultaneously). Never hardcode.

## Failure Modes and Recovery

### Common Failures
- **Loop stalls** — agent calls same tool with identical args. Fix: external deduplication enforcement.
- **Context exhaustion** — silent quality degradation before window fills. Fix: compaction + sub-agent decomposition.
- **Zombie tasks** — alive by metrics but producing no output. Fix: wall-clock timeouts at 2x expected duration.

### Recovery Preference Order
1. Resume from checkpoint
2. Degrade gracefully with partial results
3. Kill and re-queue
4. Escalate to human

### Architecture Principles
- **Idempotent operations** — running a task twice must be safe
- **Explicit timeouts** on every external call
- **State externalization** to files (enables process restart without replay)
- **External loop guardrails** — runtime enforces termination limits, not the agent

## PARA for Agent Context

The PARA methodology (Projects, Areas, Resources, Archives) maps to agentic architecture:

- **Projects** (short-term, defined goals) -> Active engineering projects with dedicated agents
- **Areas** (ongoing responsibilities) -> Company divisions with standing CLAUDE.md instructions
- **Resources** (reference material) -> Shared knowledge bases, documentation, vendor docs
- **Archives** (inactive items) -> Completed projects, old specs, deprecated configs

The folder hierarchy IS the PARA structure. Division folders are Areas. Project folders are Projects. The `references/` and `vendor-docs/` folders are Resources.

## Cowork Scheduling

Cowork supports: hourly, daily, weekly, weekdays, manual. Critical constraint: **computer must be awake and Claude Desktop open**. Missed runs catch up with one execution on wake.

For always-on operation:
- Dedicated machine that stays powered on
- Energy management settings to prevent sleep
- Docker containers or cloud VMs for persistent compute
- GitHub Actions for periodic autonomous work
