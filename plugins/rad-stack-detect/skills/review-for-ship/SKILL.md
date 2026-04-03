---
name: review-for-ship
description: >
  User-invoked skill to run a comprehensive pre-ship review using all review agents
  relevant to the project's tech stack. Reads the stack profile and dispatches agents
  in parallel. Trigger when the user says "/review-for-ship", "review before shipping",
  "is this ready to deploy", "pre-ship review", "run all reviews", "comprehensive review",
  "final check before shipping", "production readiness check", "is this ready to merge",
  "ship check", "pre-deploy review", "audit everything".
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Agent
---

# Pre-Ship Review

Run all relevant review agents for this project's tech stack. This is the comprehensive quality gate — use it before deploying, merging a major feature, or shipping a release.

**Announce at start:** "Running pre-ship review — dispatching review agents for your stack..."

---

## Step 1: Read Stack Profile

Read `.claude/stack-profile.local.md` from the project root.

**If the file does not exist:**
Tell the user: "No stack profile found. Run `/detect-stack` first to scan your project and identify which review agents apply. Then come back and run `/review-for-ship`."
Stop here.

**If the file exists:**
Parse the YAML frontmatter. Extract:
- `project_name`
- `project_type`
- `technologies` (the list)
- `review_agents` (the list of agents with their `subagent_type` values)
- `plugins.core`, `plugins.supporting`, `plugins.pre_ship`

---

## Step 2: Confirm with User

Before dispatching agents, show the user what will run:

```
## Pre-Ship Review Plan

**Project:** [project_name]
**Type:** [project_type]
**Stack:** [comma-separated technology names]

### Review Agents to Dispatch
[For each agent in review_agents:]
- **[agent name]** — [one-line description of what it reviews]

This will run [N] review agents in parallel. Each agent scans the full project autonomously.

Proceed? (This uses context and tokens proportional to the number of agents.)
```

Wait for user confirmation before proceeding. If the user says no or wants to skip certain agents, adjust accordingly.

---

## Step 3: Dispatch Review Agents

Launch all review agents **in parallel** using the Agent tool. For each agent:

- Set `subagent_type` to the value from the stack profile
- Set `run_in_background` to `true` so all agents run concurrently
- Give each agent a clear prompt:

```
Review the project at [current working directory] for [what this agent reviews].
This is a [project_type] project using [technology list].
Scan the full codebase and report findings organized by severity (Critical, Warning, Info).
Be thorough but practical — focus on issues that would cause real problems in production.
```

### Available Review Agents

Only dispatch agents that are listed in the stack profile's `review_agents` field:

| Agent | subagent_type | Reviews |
|---|---|---|
| Astro Reviewer | `rad-astro:astro-reviewer` | Astro anti-patterns, performance, SSR/SSG issues |
| Next.js Reviewer | `rad-nextjs:nextjs-reviewer` | App Router violations, security, performance |
| React Reviewer | `rad-react:react-reviewer` | Hooks violations, performance, accessibility, security (XSS, IDOR) |
| TypeScript Reviewer | `rad-typescript:typescript-reviewer` | Strict-mode compliance, type safety, AI codegen anti-patterns |
| Fastify Reviewer | `rad-fastify:fastify-reviewer` | Encapsulation violations, validation, production readiness |
| Accessibility Reviewer | `rad-a11y:a11y-reviewer` | WCAG 2.2 AA compliance, ARIA, keyboard navigation, focus management |
| Chrome Extension Reviewer | `rad-chrome-extension:chrome-ext-reviewer` | MV3 security, permissions, Chrome Web Store compliance |
| SEO Auditor | `rad-seo-optimizer:seo-dominator` | Full SEO audit, Core Web Vitals, schema markup |

---

## Step 4: Compile Results

As each agent completes, collect its findings. Once all agents have reported back, compile a unified report.

### Report Format

```
# Pre-Ship Review Report

**Project:** [name]
**Date:** [today's date]
**Stack:** [technologies]
**Agents Run:** [count] of [count]

---

## Summary

**Overall Assessment:** [Ready to Ship / Needs Work / Critical Issues Found]

| Severity | Count |
|----------|-------|
| Critical | [n] |
| Warning  | [n] |
| Info     | [n] |

---

## Findings

### [Agent Name]
**Status:** [Clean / Issues Found]

[If issues found, list them organized by severity]

#### Critical
- [Issue description + file:line + recommended fix]

#### Warnings
- [Issue description + file:line + recommended fix]

#### Info
- [Improvement suggestion]

[Repeat for each agent]

---

## Recommended Actions

Priority order for fixing issues before shipping:

1. **[Critical item]** — [why it matters, what to do]
2. **[Critical item]** — [why it matters, what to do]
3. **[Warning item]** — [why it matters, what to do]
...

---

## What's Next?

[If critical issues: "Fix the critical issues above, then run /review-for-ship again to verify."]
[If only warnings: "The warnings above are worth addressing but aren't blockers. Use your judgment."]
[If clean: "Your project looks good! No critical issues found across all reviewers."]
```

---

## Step 5: Offer Follow-Up

After the report, offer:
- "Want me to fix any of these issues?" (if issues were found)
- "Want me to run a specific reviewer again after fixes?" (for targeted re-check)
- "Want me to save this report?" (write to a file for reference)

---

## Edge Cases

- **Agent fails or times out:** Note which agent failed, report results from the ones that succeeded, and suggest re-running the failed agent individually.
- **No review agents in profile:** If the stack profile has no review agents listed (unusual), tell the user and suggest running `/detect-stack --update` to refresh the profile.
- **User wants partial review:** If the user only wants specific agents, respect that. Only dispatch the requested subset.
