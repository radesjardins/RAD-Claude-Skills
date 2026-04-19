# AI Coding Anti-Patterns: The "Do Not Do" Constraint List

These 14 anti-patterns are extracted from documented failures, common AI architectural hallucinations, and coding dead-ends. The planner must check every proposed plan against this list before approval.

## Architecture Anti-Patterns

### 1. Do Not Use the "Vector Sidecar" Pattern
**What:** Maintaining a separate vector database alongside your primary transactional database.
**Why it fails:** Synchronization gaps, brittle ETL pipelines, stale data retrieval, combinatorial explosion of access control logic.
**Instead:** Use hybrid search within a unified relational schema (PostgreSQL + pgvector).

### 2. Do Not Over-Engineer MCP Servers
**What:** Building complex abstraction layers around MCP servers for AI agents.
**Why it fails:** Agents fight the abstraction rather than scripting against raw data.
**Instead:** Narrowly scope MCP to authentication, network boundaries, and security gates. Let agents use simple CLIs for data access.

### 3. Do Not Gatekeep Context via Rigid Subagents
**What:** Building rigidly specialized subagents (e.g., isolated "PythonTests" agent) that hide holistic system context.
**Why it fails:** Prevents AI from reasoning about cross-module impacts.
**Instead:** Favor dynamic "Master-Clone" architectures where a fully-contextualized master spawns identical clones for specific tasks.

## Context Management Anti-Patterns

### 4. Do Not Create "Kitchen Sink" Sessions
**What:** Mixing unrelated tasks, feature builds, and refactoring in a single AI conversation.
**Why it fails:** Severe context bleed -- AI confuses priorities and drops important constraints.
**Instead:** Start a fresh thread for every specific, bounded task. One task per conversation.

### 5. Do Not Trust Auto-Compaction
**What:** Relying on built-in auto-compaction to manage token limits during long sessions.
**Why it fails:** Highly lossy and opaque -- AI forgets crucial architectural decisions and migration contexts.
**Instead:** Use the "Document & Clear" pattern: dump state to markdown, clear session, rehydrate from file.

### 6. Do Not Permit Infinite Exploration
**What:** Issuing open-ended instructions like "investigate this issue" without search boundaries.
**Why it fails:** Agent reads hundreds of irrelevant files, rapidly consuming context and polluting reasoning.
**Instead:** Set strict search boundaries: specific directories, file patterns, and a maximum number of files to examine.

### 7. Do Not Overload CLAUDE.md / AGENTS.md
**What:** Treating system instruction files as exhaustive documentation dumps.
**Why it fails:** Past 150-200 instructions, AI arbitrarily ignores critical rules. Context window exhausted.
**Instead:** Keep under 200 lines. Cut anything AI can infer from the codebase. Use progressive disclosure to link external docs.

### 8. Do Not Trap Agent in Endless Correction Loops
**What:** Repeatedly prompting the AI to fix a mistake after it has already failed twice.
**Why it fails:** Context becomes polluted with failed approaches and apologies. Each retry makes output worse.
**Instead:** After 2 consecutive failures on the same issue, clear context immediately. Analyze the failure, write a fresh structurally sound prompt, restart.

## Code Quality Anti-Patterns

### 9. Do Not Fall into the "Fallback Trap"
**What:** Instructing AI to "add a fallback mechanism" or "add error handling to catch this" when it encounters an edge case.
**Why it fails:** Masks root causes, leads to silent failures and accumulating technical debt.
**Instead:** Always force the AI to identify and fix the underlying root cause. Never mask errors.

### 10. Do Not Allow "Comments Everywhere"
**What:** Accepting generated code cluttered with excessive explanatory comments.
**Why it fails:** AI over-comments to assist its internal reasoning, but this creates bloated code with high cognitive load for human reviewers.
**Instead:** Require comments only where logic is non-obvious. Self-documenting code is the goal.

### 11. Do Not Accept Stale APIs or Hallucinated Dependencies
**What:** Blindly executing code that calls third-party systems without verification.
**Why it fails:** AI exhibits "By-the-Book Fixation" -- uses deprecated endpoints, hallucinated imports, or legacy API versions.
**Instead:** Always verify third-party API calls against current documentation. Use Context7 or web search for current API references.

### 12. Do Not Edit Tests Just to Turn Them Green
**What:** Allowing AI to delete tests, remove assertions, or modify test expectations to match broken implementation.
**Why it fails:** Silently erodes test quality. Tests become meaningless green checks that miss real bugs.
**Instead:** Use coverage gates as behavioral guardrails. Tests define correct behavior; implementation must match tests, not the reverse.

### 13. Do Not Tolerate Unsolicited Over-Engineering
**What:** Allowing AI to perform premature refactoring, create unrequested helper functions, or invent extra abstractions.
**Why it fails:** Codebase succumbs to "hallucination entropy" -- unnecessary complexity introduced by AI trying to be helpful.
**Instead:** Demand the simplest possible approach. Three similar lines of code is better than a premature abstraction.

### 14. Do Not "Shoot and Forget"
**What:** Accepting AI code output without formal verification and test-driven validation.
**Why it fails:** Industry reports consistently show higher vulnerability rates and accumulated technical debt when AI output is integrated without review — the specific magnitude varies by codebase and review rigor, but the direction is unambiguous.
**Instead:** Mandate that every AI-generated artifact is reviewed against strict architectural specifications before integration. AI is a draft generator, not an independent developer.

## How to Use This List

During plan review, the risk-assessor agent checks every proposed task against these 14 constraints. If any task instruction could trigger one of these anti-patterns, it must be flagged with:
- The specific anti-pattern number and name
- Why the current plan risks triggering it
- A concrete alternative approach
