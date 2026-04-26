---
name: agentic-operations
description: This skill should be used when the user asks about "daily operating rhythm", "agentic operations", "token optimization", "credential rotation", "autonomous agent patterns", "headless mode", "agent failure recovery", "morning briefing", "agent monitoring", "context compaction strategy", "PARA methodology for agents", "Routines", "scheduled agents", or wants guidance on running and maintaining a Claude Code workspace day-to-day.
user-invocable: true
allowed-tools: Read Glob Grep
---

# Agentic Operations Reference

Practical guidance for daily Claude Code workspace operations. Every claim in this file is grounded in current Anthropic documentation (verified April 2026); the previous version of this skill propagated several outdated and fictional claims that have been removed in 2.0.

## Source

- [Claude Code official docs](https://docs.claude.com/en/docs/claude-code/)
- [Best practices for agentic coding](https://code.claude.com/docs/en/best-practices)
- [Routines (cloud-scheduled tasks)](https://claude.ai/code/routines) — formerly called "Cowork"
- [Anthropic pricing and prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)

---

## The three-checkpoint daily rhythm

This is one workable pattern; not the only one. Adapt to your team's reality.

### Morning review (suggested 15-30 min)
- Check overnight scheduled task results — verify expected output files exist with valid data
- Scan error logs / dashboards for the prior 24 hours
- Run `/cost` or check Anthropic Console for spend against your daily budget
- Verify connected MCP servers are responsive (`/mcp` in Claude Code)
- Check credential expiration dates (flag anything due within 7 days)
- Set the day's task queue based on results

### Midday spot-check (~10 min)
- Watch in-progress agents for stalls (no checkpoint heartbeat in >10 minutes)
- Monitor context window utilization on long-running sessions (intervene before ~85%)
- Check session-level token burn rate
- Handle agents hitting errors or rate limits
- Kill zombie tasks and re-queue with adjusted parameters

### End-of-day wrap (~15 min)
- Assess quality of agent output, accept or reject
- Review total daily token spend
- Queue overnight tasks (if you use Routines or scheduled agents)
- Plan tomorrow's priority tasks

---

## Autonomous execution patterns

### Headless mode (`claude -p` / `--print`)

Run Claude Code as a one-shot process for CI/CD, cron jobs, scripted workflows.

```bash
claude -p "Implement the user profile endpoint from tasks/plans/user-profile.md" \
  --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "Bash(npm run *)" "Bash(git *)" \
  --max-turns 50 \
  --max-budget-usd 2.00 \
  --output-format json
```

All of these flags are documented and current as of April 2026.

**Three permission strategies for autonomous runs:**
1. `--allowedTools` whitelist — safest, explicit tool list
2. `--permission-mode auto` — middle ground; the auto mode lets Claude decide whether to prompt. Specific termination behavior (e.g., "stops after N denials") is not documented in detail; verify behavior in your context before relying on it for unattended runs.
3. `--dangerously-skip-permissions` — sandboxed environments only

### `/loop` (in-session polling)

`/loop <interval> <prompt>` runs the prompt repeatedly while the session stays open. Examples:

```
/loop 5m /check-deploy
/loop 2h /review-pending-prs
```

Omit the interval to let Claude self-pace. **`/loop` does NOT support cron expressions** — that's a different feature (`/schedule`, see Routines below). `/loop` dies when the session ends.

### `/schedule` and Routines (cloud-scheduled tasks)

For scheduled tasks that run independent of any open session, use **Routines** at [claude.ai/code/routines](https://claude.ai/code/routines) or via the `/schedule` command. Key facts:

- **Run on Anthropic-managed cloud infrastructure.** Your laptop can be closed, asleep, off — the routine still fires at its scheduled time.
- **Schedule options:** hourly, daily, weekdays, weekly, or one-off manual runs. Cron expressions supported.
- **A few minutes of stagger** is normal at scheduled times (load distribution).

This is the correct mechanism for "every Monday morning, generate the deploy-readiness report" or "in two weeks, open a cleanup PR for the feature flag we just shipped."

### Fresh-agent iterative pattern ("Ralph Wiggum")

A reliable autonomous pattern: pick task → implement → validate (run tests) → commit → update status → reset context → repeat. A fresh agent each iteration prevents context degradation. State persists through files (task list, CLAUDE.md, git history, test results).

This pattern shows up in many production agentic-coding workflows. The cost: each iteration pays the context-rebuild tax. The benefit: each iteration's reasoning is fresh and uncontaminated by prior failed attempts.

---

## Token cost optimization

Anthropic's `/cost` telemetry produces an average around **$6/dev/day** in some published summaries; the company's enterprise documentation cites a **$13/active-day** figure for organizational deployments. The two numbers cover different cohorts. Either way: 90% of users are well below $30/active-day. Heavy autonomous use can blow past these without noticing.

### Strategies that move the needle

1. **Prompt caching** — cache reads cost 0.1× standard input tokens. The default cache TTL is 5 minutes (this is a recent regression from a previous 1-hour default — track Anthropic's changelog if you need the 1-hour tier). Pays off after a single read within the TTL window for the 5-minute tier.
2. **Model routing** — Sonnet for ~80% of tasks, Opus for architecture/review/judgment-heavy work, Haiku for classification or pattern-matching jobs.
3. **Context hygiene** — `/clear` between unrelated tasks, `/compact` with custom instructions when switching focus.
4. **Output constraints** — output tokens cost ~5x input. Format constraints ("respond in 3 bullets") have outsized impact.
5. **Avoid stale beta headers** — the previous version of this skill recommended the `token-efficient-tools-2025-02-19` beta header. Anthropic's current docs explicitly state this header is a no-op on Claude 4+ models and should be removed. **Don't add it.**

---

## Credential rotation

| Credential | Rotation period |
|---|---|
| Production API keys | 60–90 days |
| OAuth access tokens | 15–30 minutes (automatic) |
| OAuth refresh tokens | 7–14 days |
| MCP server credentials | 60–90 days |
| SSH keys | Annually (or on compromise) |

Automate via your CI/CD pipeline or secrets manager. Implement grace periods (old + new keys valid simultaneously). Never hardcode.

---

## Failure modes and recovery

### Common failures
- **Loop stalls** — agent calls the same tool with identical args repeatedly. Fix: external deduplication enforcement (a hook or wrapper script that detects the pattern).
- **Context exhaustion** — silent quality degradation before the window fills. Symptoms: vague responses, hallucinated paths, dropped instructions. Fix: compact + sub-agent decomposition + the fresh-agent iterative pattern.
- **Zombie tasks** — alive by metrics but producing no useful output. Fix: wall-clock timeouts at 2× expected duration.

### Recovery preference order
1. Resume from checkpoint
2. Degrade gracefully with partial results
3. Kill and re-queue
4. Escalate to human

### Architecture principles
- **Idempotent operations** — running a task twice must be safe
- **Explicit timeouts** on every external call
- **State externalization** to files (enables process restart without replay)
- **External loop guardrails** — runtime enforces termination limits, not the agent

---

## PARA for workspace context

The PARA methodology (Tiago Forte) maps cleanly to a workspace folder hierarchy:

- **Projects** (short-term, defined goals) → Active engineering projects with dedicated agents
- **Areas** (ongoing responsibilities) → Workspace divisions with standing CLAUDE.md instructions
- **Resources** (reference material) → Shared knowledge bases, vendor docs
- **Archives** (inactive items) → Completed projects, old specs, deprecated configs

The folder hierarchy IS the PARA structure. Division folders are Areas. Project folders are Projects. The `references/` and `vendor-docs/` folders are Resources. This is the most credible organizational framework for structuring agent context.

---

## Honest scope of this skill

This skill is a **reference guide**, not an executable workflow. It describes patterns; you decide which to adopt. Specifically:

- The "three-checkpoint rhythm" is one workable pattern, not a prescription
- The cost figures are starting estimates; your actual spend depends entirely on usage patterns
- The credential rotation periods are common-sense defaults, not regulatory minimums
- The PARA mapping works well for many people; if your workflow doesn't match, ignore it

When operational claims appear elsewhere in the plugin docs, they should be cross-checked against this file. If they conflict, this file is more recent and more honest.
