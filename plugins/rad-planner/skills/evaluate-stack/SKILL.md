---
name: evaluate-stack
description: >
  This skill should be used when the user says "what stack should I use", "evaluate my
  tech stack", "recommend a stack", "what framework for", "compare frameworks", "is this
  the right stack", "stack recommendation", "best framework for", "technology selection",
  "what database should I use", "Next.js vs Astro", "Supabase vs Firebase", "which ORM",
  "hosting recommendation", "deployment platform", or wants help choosing technologies
  for a new or existing project. Provides AI-native stack recommendations optimized for
  code generation accuracy.
argument-hint: "[project type or description] [--existing to evaluate current stack]"
user-invocable: true
allowed-tools: Read Glob Grep WebSearch WebFetch Agent
---

# Evaluate Stack — AI-Native Technology Selection

Evaluate and recommend technology stacks optimized for AI-assisted development. Recommendations are grounded in the Golden Path proficiency matrix and verified against current information.

## Workflow

### 1. Gather Project Context

Ask the user (if not already provided):
- **Project type:** What are you building? (web app, API, CLI tool, mobile, data pipeline)
- **Scale:** Solo project, small team, or enterprise?
- **Key requirements:** Real-time? Heavy data processing? Content-heavy? AI features?
- **Existing infrastructure:** Any cloud providers, databases, or frameworks already committed?
- **Experience level:** What technologies does the team already know?

### 2. Apply the Golden Path Matrix

Load `references/golden-path-matrix.md`.

Apply the AI-Native Proficiency Tiers and Project-Type Decision Matrix from the reference to select the right stack. Prefer Primary tier technologies unless the project has specific requirements that justify Secondary or lower tiers.

### 3. Verify Current Information

Use the Agent tool to delegate to the `stack-advisor` agent for comprehensive evaluation. Provide the agent with the project context gathered in Step 1 and the initial stack direction from Step 2.

The stack-advisor agent will:
- Use Context7 MCP (if available) to fetch current framework documentation
- Use WebSearch to verify current stable versions and recent breaking changes
- Check compatibility between all recommended components
- Confirm no security vulnerabilities in recommended versions

### 4. Present Recommendation

Output a structured recommendation table:

| Layer | Recommended | Version | AI Tier | Why |
|-------|-----------|---------|---------|-----|
| Language | TypeScript | 5.x | Primary | [rationale] |
| Frontend | [choice] | [version] | [tier] | [rationale] |
| Backend | [choice] | [version] | [tier] | [rationale] |
| Database | [choice] | [version] | [tier] | [rationale] |
| ... | ... | ... | ... | ... |

Include:
- Alternatives considered and why they were rejected
- Compatibility verification results
- Any risks or version-pinning recommendations
- Links to current documentation for each choice

### 5. Answer Follow-Up Questions

Be prepared to:
- Justify any choice against a specific alternative the user prefers
- Explain trade-offs between Primary and Secondary tier options
- Provide migration guidance if switching from an existing stack
- Recommend specific libraries within the chosen framework (e.g., which ORM, which auth library)

### 6. Next Steps

After the user accepts the stack recommendation, suggest:
- Run `/rad-planner:plan-project` to build a full implementation plan using this stack
- Or proceed directly if this was a standalone evaluation

## Key Reference

Load `references/golden-path-matrix.md` for the complete decision matrix, proficiency tiers, and project-type recommendations.
