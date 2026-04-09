# Task Format: DAG-Based Dependency Tracking

## Task States

| State | Symbol | Meaning |
|-------|--------|---------|
| `[PENDING]` | `- [ ]` | Not started, waiting for dependencies or execution |
| `[IN PROGRESS]` | `- [ ]` | Currently being worked on by an agent |
| `[BLOCKED]` | `- [ ]` | Dependencies not yet satisfied |
| `[DONE]` | `- [x]` | Implementation complete, awaiting verification |
| `[VERIFIED]` | `- [x]` | Passed validation checks, confirmed working |
| `[DEFERRED]` | `- [ ]` | Intentionally postponed with documented reason |

## Hierarchical Task IDs

Tasks use unique hierarchical identifiers for precise parent-child referencing:

```
1       — Phase-level task
1.1     — First subtask of Phase 1
1.1.1   — Sub-subtask (only if complexity > 7)
1.2     — Second subtask of Phase 1
2       — Phase 2
2.1     — First subtask of Phase 2
```

## Dependency Rules (Directed Acyclic Graph)

### Core Rules
1. **Explicit mapping:** Every task's blockers listed in `Dependencies` field as array of task IDs
2. **No circular dependencies:** If A blocks B, B cannot block A (DAG enforcement)
3. **Transitive blocking:** If A blocks B and B blocks C, then C cannot start until both A and B are complete
4. **No assumed order:** Agents determine execution order from the dependency graph, NOT from document position

### Execution Priority
When multiple tasks are unblocked simultaneously, execute in this order:
1. **Priority level:** high > medium > low
2. **Dependency count:** Tasks that unblock the most downstream work first
3. **Complexity:** Lower complexity first (quick wins build momentum)
4. **Task ID:** Lower ID first (as tiebreaker)

### Cycle Detection
Before finalizing any plan, verify no cycles exist:
- Task A blocks B, B blocks C, C blocks A = DEADLOCK (forbidden)
- If detected, restructure by breaking the cycle at the least-coupled point

## Complexity Scoring

Every task receives a complexity score from 1-10:

| Score | Meaning | Action |
|-------|---------|--------|
| 1-3 | Simple, well-defined, single-file | Execute directly |
| 4-6 | Moderate, multi-file, clear approach | Execute with validation checkpoint |
| 7-8 | Complex, cross-cutting concerns | Must break into subtasks before execution |
| 9-10 | Highly complex, architectural impact | Break into subtasks AND require human review |

**Expansion rule:** Any task scoring > 7 MUST be recursively broken into subtasks, each scoring <= 7.

## Markdown Task Format

```markdown
### Phase 1: [Phase Name] (Milestone M1)

- [ ] **[PENDING]** S1: [Task Title]
  - **Objective:** [1-2 sentences describing what and why]
  - **Main changes:** [Files and behavior being modified]
  - **Dependencies:** None
  - **Priority:** High | Medium | Low
  - **Complexity:** [1-10]
  - **Definition of Done:** [Specific, measurable completion criteria]
  - **Validation:** [Runnable command or verifiable condition]
  - **Rollback:** [How to revert if validation fails]
  - **Test Strategy:** [What tests to write, what they verify]
  - **Anti-Pattern Watch:** [Specific anti-patterns to avoid for this task]

- [ ] **[BLOCKED]** S2: [Task Title]
  - **Objective:** [...]
  - **Dependencies:** [S1]
  - [...]
```

## JSON Task Format

For machine orchestration and programmatic task management:

```json
{
  "tasks": [
    {
      "id": "1.1",
      "title": "Initialize project scaffold",
      "description": "Create project with TypeScript, configure linting and formatting",
      "status": "pending",
      "phase": "Infrastructure Setup",
      "milestone": "M1",
      "dependencies": [],
      "priority": "high",
      "complexity": 2,
      "definitionOfDone": "npm run build succeeds, npm run lint passes",
      "validation": "npm run build && npm run lint",
      "rollback": "git checkout -- .",
      "testStrategy": "Verify TypeScript compilation, lint rules enforce project conventions",
      "antiPatternWatch": [],
      "metadata": {}
    },
    {
      "id": "1.2",
      "title": "Configure database schema",
      "status": "blocked",
      "dependencies": ["1.1"],
      "priority": "high",
      "complexity": 4,
      "validation": "npx prisma db push && npx prisma db seed",
      "rollback": "npx prisma db push --force-reset"
    }
  ]
}
```

## Metadata Preservation

The `metadata` field is JSON-serializable and protected from AI modification during automated operations. Use for:
- Git branch associations
- External ticket references (Jira, Linear, GitHub Issues)
- Manual status notes from human review
- Timestamps for tracking progress
- Custom fields specific to the project

## Parallel Execution

Tasks with no dependency relationship can execute in parallel "waves":

```
Wave 1: [S1] (no dependencies)
Wave 2: [S2, S3] (both depend only on S1, can run simultaneously)
Wave 3: [S4] (depends on S2 AND S3, must wait for both)
```

Agents self-claim the next unblocked task from the queue when idle. No central scheduler needed if the dependency graph is correctly defined.
