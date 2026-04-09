# TDD Constraints for Execution Agents

Automated tests act as an objective "external oracle" for AI agents -- providing unambiguous, continuous feedback without requiring human intervention. As context windows fill, AI judgment degrades, but test results remain deterministic.

## The Red-Green-Refactor Cycle

### Red Phase (Write Failing Tests First)
- Write tests based on approved specifications BEFORE any implementation code
- Tests must define expected inputs, outputs, and error states from the plan
- Run tests to confirm they FAIL -- this prevents hallucinated implementations
- **Hard rule:** If a test passes before implementation exists, the test is wrong

### Green Phase (Minimum Code to Pass)
- Write the MINIMUM amount of code necessary to make failing tests pass
- **Hard constraint:** NEVER modify test expectations to match broken implementation
- If a test fails after implementation, the implementation is wrong, not the test
- Keep implementation simple -- no premature optimization or abstraction

### Refactor Phase (Clean Without Breaking)
- Refactor implementation only after all tests are green
- Run full test suite after every refactor step
- If any test breaks during refactor, revert the refactor immediately

## Mutation Testing (Sanity Check)

AI agents are prone to writing trivial tests (e.g., `expect(1).toBe(1)`). To verify test quality:

1. **Break the implementation** -- introduce a deliberate bug (e.g., change `>` to `>=`)
2. **Run the test** -- confirm it FAILS (catches the bug)
3. **Revert the break** -- restore correct implementation
4. **Confirm green** -- test passes again

If the test passes despite the broken implementation, the test is useless and must be rewritten.

## Testing Criteria Per Task

Every task in the plan must specify:

### 1. Unit Tests
- What functions/modules to test in isolation
- Mock boundaries: what external dependencies to mock (APIs, databases, file system)
- Minimum coverage threshold (recommend 80%+ for new code)
- Edge cases to cover explicitly:
  - Null/undefined inputs
  - Empty arrays/objects
  - Boundary values (0, -1, MAX_INT)
  - Invalid types
  - Concurrent access (if applicable)

### 2. Integration Tests
- What components interact in this task
- Test data setup and teardown
- API contract verification (request/response shapes)
- Database state assertions (after operations)

### 3. End-to-End Tests (Where Applicable)
- User journey scenarios in Gherkin format:
  ```gherkin
  Feature: User Registration
    Scenario: Successful registration
      Given a new user with valid credentials
      When they submit the registration form
      Then an account is created
      And they receive a confirmation email
      And they are redirected to the dashboard
  ```
- Critical paths that must work before deployment
- Smoke tests for deployment verification

## Test Organization

```
__tests__/
├── unit/                    # Isolated function tests
│   ├── auth.test.ts
│   └── validation.test.ts
├── integration/             # Component interaction tests
│   ├── api/
│   │   └── users.test.ts
│   └── db/
│       └── migrations.test.ts
└── e2e/                     # Full user journey tests
    └── registration.test.ts
```

## Coverage as Behavioral Guardrail

Code coverage in agentic workflows serves a different purpose than in traditional development:
- It is a **regression signal** -- ensuring AI's rapid iterations don't silently erode existing functionality
- Set minimum thresholds that block task completion if not met
- Track coverage direction: if coverage drops after a task, the task likely broke something

Recommended minimums:
- New code: 80% line coverage
- Modified code: Coverage must not decrease
- Critical paths (auth, payments, data mutations): 90%+ coverage

## What the Plan Must Include

For each task that involves code generation, the plan must specify:

```markdown
**Test Strategy:**
- Unit: [What to test, what to mock]
- Integration: [What interactions to verify]
- Edge cases: [Specific boundary conditions]
- Coverage target: [Percentage]
- Test command: [Exact command to run tests]
- Expected result: [What "passing" looks like]
```

## Anti-Pattern: Test Editing

If an execution agent modifies a test to make it pass:
1. Flag immediately as anti-pattern #12 ("Do Not Edit Tests Just to Turn Them Green")
2. Revert the test to its original form
3. Fix the implementation to match the test
4. If the test itself is genuinely wrong (spec changed), document the spec change in the plan first, THEN update the test
