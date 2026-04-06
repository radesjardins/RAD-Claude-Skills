# rad-testing Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `rad-testing` Claude Code plugin that provides cross-cutting JavaScript/TypeScript testing guidance covering strategy, Vitest, Playwright, mocking, async patterns, and cross-tool architecture — filling the gaps that no single official documentation site covers.

**Architecture:** Six skills covering distinct testing domains, one agent (testing-reviewer) for auditing existing test files, all grounded in both the "Software Testing and Validation" NotebookLM notebook and official docs. Skills are deliberately cross-framework and complement (not duplicate) existing rad-react, rad-fastify, and rad-nextjs plugin testing sections.

**Tech Stack:** Claude Code plugin format (SKILL.md / AGENT.md), NotebookLM CLI (`notebooklm ask`), web fetch for official docs, existing plugin patterns from rad-typescript and rad-react as structural reference.

---

## Source Strategy

Each skill is built from two source types:

### NotebookLM Notebook
**ID:** `d9099714-23fb-455a-a5c8-018304419300`  
**Title:** Software Testing and Validation  
**Set context before querying:** `notebooklm use d9099714`

### Online Official Sources
Fetch these before writing skills — save key excerpts in scratch notes:
- Vitest config guide: `https://vitest.dev/config/`
- Vitest coverage: `https://vitest.dev/guide/coverage`
- Vitest browser mode: `https://vitest.dev/guide/browser/`
- Playwright best practices: `https://playwright.dev/docs/best-practices`
- Playwright locators: `https://playwright.dev/docs/locators`
- Playwright CI: `https://playwright.dev/docs/ci`
- Testing Library query priority: `https://testing-library.com/docs/queries/about#priority`
- MSW concepts: `https://mswjs.io/docs/concepts`
- Kent C. Dodds — Testing Trophy: `https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications`
- Kent C. Dodds — Write tests. Not too many.: `https://kentcdodds.com/blog/write-tests`
- Kent C. Dodds — Merits of Mocking: `https://kentcdodds.com/blog/the-merits-of-mocking`

---

## Plugin File Structure

```
plugins/rad-testing/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── testing-philosophy/
│   │   └── SKILL.md          # Why, when, trophy vs pyramid, AI paradox
│   ├── testing-vitest/
│   │   └── SKILL.md          # Config, TypeScript, coverage, browser mode, monorepo
│   ├── testing-playwright/
│   │   └── SKILL.md          # E2E, POM, locators, flaky tests, CI, a11y
│   ├── testing-mocks/
│   │   └── SKILL.md          # Mock strategy, MSW, vi.mock, theatre tests
│   ├── testing-async/
│   │   └── SKILL.md          # waitFor, fake timers, race conditions, concurrent tests
│   └── testing-architecture/
│       └── SKILL.md          # Cross-tool composition, file structure, coverage thresholds
├── agents/
│   └── testing-reviewer.md   # Audits test files for anti-patterns
├── LICENSE                   # Apache 2.0 (own work — no upstream attribution needed)
└── README.md
```

**Reference plugins for structural patterns:**
- `plugins/rad-typescript/.claude-plugin/plugin.json` — plugin.json format
- `plugins/rad-react/skills/react-foundations/SKILL.md` — skill frontmatter format
- `plugins/rad-react/agents/react-reviewer.md` — agent format (flat `.md` file, NOT a subdirectory)

**SKILL.md frontmatter rule (applies to all 6 skills):**
Every SKILL.md uses exactly two frontmatter fields — `name` and `description`. No `metadata`, `version`, `category`, or `tags` blocks exist in the real skill spec. The `description` must be a trigger-phrase string following the pattern `"This skill should be used when the user..."` listing the keywords/phrases that activate it. Content summaries are wrong.

```markdown
---
name: testing-philosophy
description: "This skill should be used when the user asks about testing strategy, 'Testing Trophy', 'Testing Pyramid', 'Testing Honeycomb', 'behavior vs implementation', 'AI testing paradox', 'test ROI', 'ice cream cone anti-pattern', 'how many tests should I write', 'when to write tests', 'unit vs integration', 'what kind of tests', or 'test distribution'."
---
```

---

## Recommended NotebookLM Queries (Per Skill)

These are the exact queries to run against the notebook when drafting each skill. Run them sequentially in one session after `notebooklm use d9099714`.

### For `testing-philosophy`
```
1. "What testing strategies and philosophies does this notebook cover? Summarize the Testing Trophy, Testing Pyramid, Testing Honeycomb, and the AI Testing Paradox, including their recommended test distributions and tradeoffs."

2. "What does this notebook say about testing behavior vs implementation details? What specific anti-patterns does it warn against, and what examples does it give of tests that test the wrong thing?"

3. "What guidance does this notebook give about the ROI of testing — when are tests not worth writing, what is the cost of over-testing, and what is the ice cream cone anti-pattern?"

4. "What does this notebook say about the 'Avoid the Test User' concept — the anti-pattern of testing through an abstract user or role rather than real UI interactions? How does this differ from general 'behavior vs implementation' guidance?"

5. "What does this notebook say about snapshot testing — when are snapshots useful vs when do they become brittle? What is the difference between UI snapshots and serializer snapshots, and what are the common snapshot abuse patterns to avoid?"
```

### For `testing-vitest`
```
4. "What does this notebook cover about Vitest configuration — specifically how to share config across a monorepo using the Projects feature, how defineProject differs from defineConfig, and how to use mergeConfig with a shared config file?"

5. "What does this notebook say about Vitest coverage — the difference between V8 and Istanbul providers, how coverage works in a monorepo, the limitation that coverage options cannot be inside project configs, and how to merge coverage reports with nyc?"

6. "What does this notebook say about Vitest Browser Mode — why to use it over jsdom, how to set it up with Playwright provider, what limitations exist with vi.spyOn in native ESM environments, and the { spy: true } workaround?"

7. "What are the specific Vitest mocking primitives this notebook covers — vi.fn(), vi.mock(), vi.spyOn(), vi.stubGlobal(), vi.useFakeTimers(), and vi.setSystemTime() — with examples of when to use each?"
```

### For `testing-playwright`
```
8. "What does this notebook say about Playwright locator strategy — the full priority order from role-based locators down to data-testid, why CSS/XPath are brittle, and how to use the VS Code extension and codegen to generate resilient locators?"

9. "What does this notebook say about preventing flaky Playwright tests — specifically replacing page.waitForTimeout() with auto-waiting, using web-first assertions like toBeVisible(), and ensuring strict test isolation with fresh browser contexts?"

10. "What does this notebook say about Playwright CI setup — Linux environments, selective browser installation, parallelism and sharding, authentication state reuse across the test suite, and the trace viewer on first retry strategy?"

11. "What does this notebook say about accessibility testing with Playwright — using @axe-core/playwright, scanning full pages vs specific elements with AxeBuilder.include(), filtering by WCAG tags, and handling known violations with snapshots or disableRules?"

12. "What does this notebook say about Page Object Model (POM) structure — the directory layout for tests/page-objects/fixtures/utils, how to centralize selectors, and the tradeoffs of POM vs other organization approaches?"
```

### For `testing-mocks`
```
13. "What does this notebook say about the decision of WHEN to mock — the specific conditions under which mocking is justified (financial cost, network boundaries, animation, callback props) versus when it should be avoided (saving milliseconds, internal modules, child components, E2E tests)?"

14. "What does this notebook say about MSW (Mock Service Worker) as the recommended network mocking tool — how it works, why it's preferred over patching fetch/axios, and how it eliminates flaky CI behavior?"

15. "What does this notebook say about 'theatre tests' — how over-mocking by AI tools leads to green CI but broken production, and what strategies prevent it?"

16. "What does this notebook say about test doubles taxonomy — the differences between fakes, stubs, spies, and mocks — and any guidance on when each is appropriate?"
```

### For `testing-async`
```
17. "What does this notebook cover about async testing patterns — waitFor usage, the difference between getBy*, queryBy*, and findBy* queries, timing pitfalls, and common mistakes that cause tests to give false positives on async code?"

18. "What does this notebook say about fake timers in Vitest — vi.useFakeTimers(), vi.setSystemTime(), how to advance time in tests, and the gotchas that trip developers up?"

19. "What does this notebook cover about testing concurrent or parallel async operations, Promise chains, and async state updates in React components?"
```

### For `testing-architecture`
```
20. "What does this notebook say about how Vitest, Testing Library, MSW, and Playwright should work together as a unified testing strategy — any guidance on which tool owns which concern and how they compose?"

21. "What does this notebook cover about test file organization — naming conventions, directory structures, co-location vs. separate test directories, and what makes a test suite maintainable at scale?"

22. "What does this notebook say about coverage thresholds — is 100% coverage a goal, what does diminishing returns look like, and what is meaningful coverage versus coverage theatre?"

23. "What does this notebook say about test data management — fixture patterns, factory functions, seeding, teardown, and how to avoid tests that depend on shared state?"
```

---

## Tasks

---

### Task 1: Scaffold plugin.json and README

**Files:**
- Create: `plugins/rad-testing/.claude-plugin/plugin.json`
- Create: `plugins/rad-testing/README.md`

**Reference:** Read `plugins/rad-typescript/.claude-plugin/plugin.json` for exact format.

- [ ] **Step 1: Read the reference plugin.json**

```bash
cat plugins/rad-typescript/.claude-plugin/plugin.json
```

- [ ] **Step 2: Create plugin.json**

```json
{
  "name": "rad-testing",
  "version": "1.0.0",
  "description": "JavaScript/TypeScript testing standards — philosophy (Testing Trophy, AI paradox), Vitest (config, coverage, browser mode, monorepo), Playwright (POM, locators, CI, a11y), mock strategy (MSW, vi.mock, theatre tests), async patterns (waitFor, fake timers), and cross-tool architecture. Fills the gaps official docs don't cover.",
  "author": {
    "name": "RAD",
    "url": "https://github.com/radesjardins"
  },
  "license": "Apache-2.0",
  "keywords": [
    "testing",
    "vitest",
    "playwright",
    "msw",
    "testing-library",
    "mocking",
    "coverage",
    "async",
    "typescript",
    "tdd",
    "e2e",
    "unit-testing",
    "integration-testing"
  ]
}
```

- [ ] **Step 3: Create README.md**

```markdown
# rad-testing

JavaScript/TypeScript testing guidance for modern full-stack applications. Covers the decisions, architecture, and patterns that official documentation deliberately skips.

## Skills

| Skill | What it covers |
|-------|----------------|
| `testing-philosophy` | Testing Trophy vs Pyramid, behavior vs implementation, AI testing paradox, test ROI |
| `testing-vitest` | Vitest config, TypeScript, coverage (V8/Istanbul), browser mode, monorepo Projects |
| `testing-playwright` | E2E architecture, Page Object Model, locators, flaky test prevention, CI, a11y |
| `testing-mocks` | Mock strategy decisions, MSW handler architecture, vi.mock/vi.spyOn, theatre tests |
| `testing-async` | waitFor pitfalls, fake timers, async state, concurrent test patterns |
| `testing-architecture` | Cross-tool composition (Vitest + RTL + MSW + Playwright), file structure, coverage thresholds |

## Agent

**testing-reviewer** — Audits existing test files for anti-patterns: over-mocking, implementation detail testing, missing isolation, brittle selectors, fixed timeouts, and coverage theatre.

## Relationship to Other Plugins

This plugin covers **cross-cutting testing infrastructure** only. Framework-specific testing patterns live in:
- `rad-react` — React component test patterns (render, userEvent, provider wrappers)
- `rad-fastify` — Fastify `.inject()` in-process testing
- `rad-nextjs` — Next.js Server Component testing, route handler testing
- `rad-a11y` — Accessibility testing with axe-core (also referenced in `testing-playwright`)
```

- [ ] **Step 4: Verify structure**

```bash
ls plugins/rad-testing/
ls plugins/rad-testing/.claude-plugin/
```

Expected: `.claude-plugin/` directory and `README.md` visible.

---

### Task 2: Build `testing-philosophy` skill

**Files:**
- Create: `plugins/rad-testing/skills/testing-philosophy/SKILL.md`

**Research steps before writing:**

- [ ] **Step 1: Run NotebookLM queries 1–5**

```bash
notebooklm use d9099714
notebooklm ask "What testing strategies and philosophies does this notebook cover? Summarize the Testing Trophy, Testing Pyramid, Testing Honeycomb, and the AI Testing Paradox, including their recommended test distributions and tradeoffs."
notebooklm ask "What does this notebook say about testing behavior vs implementation details? What specific anti-patterns does it warn against?"
notebooklm ask "What guidance does this notebook give about the ROI of testing — when are tests not worth writing, and what is the ice cream cone anti-pattern?"
notebooklm ask "What does this notebook say about the 'Avoid the Test User' concept — the anti-pattern of testing through an abstract user or role rather than real UI interactions?"
notebooklm ask "What does this notebook say about snapshot testing — when are snapshots useful vs brittle, difference between UI and serializer snapshots, and common snapshot abuse patterns?"
```

- [ ] **Step 2: Fetch official sources**

```bash
# Fetch Kent C. Dodds Testing Trophy post
# URL: https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
# Fetch: https://kentcdodds.com/blog/write-tests
# Fetch: https://kentcdodds.com/blog/avoid-the-test-user
```

- [ ] **Step 3: Write SKILL.md**

Frontmatter (two fields only — see SKILL.md frontmatter rule in Plugin File Structure above):
```markdown
---
name: testing-philosophy
description: "This skill should be used when the user asks about testing strategy, 'Testing Trophy', 'Testing Pyramid', 'Testing Honeycomb', 'behavior vs implementation', 'AI testing paradox', 'test ROI', 'ice cream cone anti-pattern', 'how many tests should I write', 'when to write tests', 'unit vs integration', 'what kind of tests', 'test distribution', or 'theatre tests'."
---
```

Content must cover (all with concrete examples, not abstractions):
- **Testing Trophy** — static analysis (base) → unit → integration (widest) → E2E (tip). Contrast with Pyramid.
- **The core mantra** — "Write tests. Not too many. Mostly integration." (Dodds). What this means concretely.
- **Behavior vs implementation** — Side-by-side example of brittle test (tests `state.isOpen`) vs robust test (finds button by role, clicks, checks visible text).
- **The AI Testing Paradox** — AI verifies what code *does* (even if buggy), not what it *should* do. Mitigation: write test names/specifications first, then let AI fill mechanical setup.
- **Theatre tests** — green CI, broken production. How over-mocking causes this.
- **Test ROI** — diminishing returns past ~70% coverage. The last 30% usually tests zero-logic code.
- **Avoid the Test User** — the anti-pattern of testing through an abstract test helper/role/wrapper rather than through what a real user sees and does. Symptoms: `wrapper.instance()`, testing internal state, testing through a "TestUser" abstraction that bypasses the real UI.
- **Snapshot testing** — when useful (serializing non-HTML output like config objects, API response shapes) vs. brittle (full DOM snapshots that fail on any cosmetic change). The difference between UI snapshots (almost always a mistake) and serializer snapshots (occasionally useful). Never commit snapshots you haven't read.
- **Anti-patterns** — ice cream cone (E2E-heavy), trophy inversion (unit-heavy), testing private methods, shallow rendering, over-snapshotting.

- [ ] **Step 4: Verify skill is readable**

```bash
head -30 plugins/rad-testing/skills/testing-philosophy/SKILL.md
```

---

### Task 3: Build `testing-vitest` skill

**Files:**
- Create: `plugins/rad-testing/skills/testing-vitest/SKILL.md`

**Research steps before writing:**

- [ ] **Step 1: Run NotebookLM queries 4–7**

```bash
notebooklm ask "What does this notebook cover about Vitest configuration — specifically how to share config across a monorepo using the Projects feature, how defineProject differs from defineConfig, and how to use mergeConfig?"
notebooklm ask "What does this notebook say about Vitest coverage — V8 vs Istanbul providers, monorepo coverage limitations, and merging reports with nyc?"
notebooklm ask "What does this notebook say about Vitest Browser Mode — why to use it over jsdom, setup with Playwright provider, and the vi.spyOn ESM limitation with the { spy: true } workaround?"
notebooklm ask "What are the specific Vitest mocking primitives — vi.fn(), vi.mock(), vi.spyOn(), vi.stubGlobal(), vi.useFakeTimers(), vi.setSystemTime() — with examples of when to use each?"
```

- [ ] **Step 2: Fetch official sources**

```bash
# https://vitest.dev/config/
# https://vitest.dev/guide/coverage
# https://vitest.dev/guide/browser/
# https://vitest.dev/guide/workspace  (monorepo/projects)
```

- [ ] **Step 3: Write SKILL.md**

**Frontmatter:**
```markdown
---
name: testing-vitest
description: "This skill should be used when the user asks about Vitest configuration, 'vitest.config', 'vitest coverage', 'V8 vs Istanbul', 'vitest browser mode', 'vitest monorepo', 'vitest projects', 'defineProject', 'mergeConfig', 'vi.mock', 'vi.spyOn', 'vi.fn', 'vi.useFakeTimers', 'vi.stubGlobal', 'vitest TypeScript', 'vitest workspace', or setting up Vitest."
---
```

Content must cover (all sections with real code):

**Configuration:**
```typescript
// vitest.config.ts — share Vite config
import { defineConfig, mergeConfig } from 'vitest/config'
import viteConfig from './vite.config'

export default mergeConfig(viteConfig, defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
  }
}))
```

**Monorepo / Projects (Vitest 3+):**
```typescript
// vitest.config.ts (root)
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    projects: ['packages/*'],  // glob discovers sub-packages
  }
})

// packages/ui/vitest.config.ts (per-package)
import { defineProject, mergeConfig } from 'vitest/config'
import sharedConfig from '../../vitest.shared'

export default mergeConfig(sharedConfig, defineProject({
  test: {
    environment: 'jsdom',
  }
}))
```

**Coverage:**
- V8 provider (`@vitest/coverage-v8`) — recommended, faster, native source maps
- Istanbul (`@vitest/coverage-istanbul`) — for legacy projects needing Istanbul-specific reports
- Coverage config must live at root level only (not inside project configs)
- Monorepo merge: `nyc merge coverage coverage/merged.json && nyc report --reporter=lcov`

**Browser Mode:**
```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    browser: {
      enabled: true,
      provider: 'playwright',  // not 'preview' for CI
      instances: [{ browser: 'chromium' }],
    }
  }
})
```

- Why: jsdom doesn't fire real events, misses CSS layout, misses native browser APIs
- ESM gotcha: `vi.spyOn(obj, 'method')` fails with sealed module namespace
- Fix: `vi.mock('./module.js', { spy: true })` — spies all exports without replacing

**Mocking primitives table:**
| Primitive | Use when |
|---|---|
| `vi.fn()` | Need a callable spy with call tracking |
| `vi.mock('module')` | Replace an entire module's exports |
| `vi.spyOn(obj, 'method')` | Wrap a real method to track calls or change return |
| `vi.stubGlobal('fetch', fn)` | Replace globals (fetch, localStorage, etc.) |
| `vi.useFakeTimers()` | Control setTimeout/setInterval/Date |
| `vi.setSystemTime(date)` | Control `new Date()` in tests |

- [ ] **Step 4: Verify**

```bash
head -40 plugins/rad-testing/skills/testing-vitest/SKILL.md
```

---

### Task 4: Build `testing-playwright` skill

**Files:**
- Create: `plugins/rad-testing/skills/testing-playwright/SKILL.md`

**Research steps before writing:**

- [ ] **Step 1: Run NotebookLM queries 8–12**

```bash
notebooklm ask "What does this notebook say about Playwright locator strategy — the full priority order, why CSS/XPath are brittle, and how codegen generates resilient locators?"
notebooklm ask "What does this notebook say about preventing flaky Playwright tests — replacing waitForTimeout(), using web-first assertions, and strict test isolation with fresh browser contexts?"
notebooklm ask "What does this notebook say about Playwright CI setup — Linux environments, selective browser installation, sharding, auth state reuse, and trace viewer on first retry?"
notebooklm ask "What does this notebook say about accessibility testing with Playwright — @axe-core/playwright, AxeBuilder.include(), WCAG tags, and handling known violations?"
notebooklm ask "What does this notebook say about Page Object Model structure — directory layout for tests/page-objects/fixtures/utils and centralized selectors?"
```

- [ ] **Step 2: Fetch official sources**

```bash
# https://playwright.dev/docs/best-practices
# https://playwright.dev/docs/locators
# https://playwright.dev/docs/pom
# https://playwright.dev/docs/ci
```

- [ ] **Step 3: Write SKILL.md**

**Frontmatter:**
```markdown
---
name: testing-playwright
description: "This skill should be used when the user asks about Playwright, 'E2E testing', 'end-to-end tests', 'Page Object Model', 'POM', 'Playwright locators', 'getByRole Playwright', 'flaky tests', 'playwright CI', 'playwright sharding', 'playwright auth', 'trace viewer', 'playwright accessibility', 'axe-core playwright', 'playwright best practices', or 'page.waitForTimeout'."
---
```

Content must cover:

**Locator priority (with examples):**
```typescript
// 1. Role — best (mirrors user + assistive tech perception)
page.getByRole('button', { name: 'Submit' })

// 2. Label — for form inputs
page.getByLabel('Email address')

// 3. Placeholder
page.getByPlaceholder('Enter email')

// 4. Text — for non-interactive elements
page.getByText('Welcome back')

// 5. Alt text
page.getByAltText('Profile photo')

// 6. Test ID — last resort
page.getByTestId('submit-btn')  // only if no semantic option exists

// AVOID — brittle, breaks on refactor
page.locator('.btn.btn-primary > span:nth-child(2)')
page.locator('//div[@class="form"]/button[2]')
```

**Page Object Model:**
```
tests/
├── e2e/
│   ├── auth.spec.ts
│   └── checkout.spec.ts
├── page-objects/
│   ├── LoginPage.ts
│   └── CheckoutPage.ts
├── fixtures/
│   └── users.ts           # test data
└── utils/
    └── auth-helper.ts     # reusable setup
```

```typescript
// page-objects/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.page.getByLabel('Email').fill(email)
    await this.page.getByLabel('Password').fill(password)
    await this.page.getByRole('button', { name: 'Sign in' }).click()
  }
}
```

**Flaky test prevention:**
```typescript
// BRITTLE — arbitrary timeout
await page.waitForTimeout(2000)
await expect(page.getByText('Welcome')).toBeVisible()

// CORRECT — web-first assertion auto-retries
await expect(page.getByText('Welcome')).toBeVisible()
// No explicit wait needed — Playwright retries until timeout
```

**Auth state sharing:**
```typescript
// playwright.config.ts
export default defineConfig({
  globalSetup: './global-setup.ts',
  use: {
    storageState: 'playwright/.auth/user.json',
  },
})

// global-setup.ts
async function globalSetup() {
  const browser = await chromium.launch()
  const page = await browser.newPage()
  await page.goto('/login')
  await page.getByLabel('Email').fill(process.env.TEST_USER_EMAIL!)
  await page.getByLabel('Password').fill(process.env.TEST_USER_PASSWORD!)
  await page.getByRole('button', { name: 'Sign in' }).click()
  await page.context().storageState({ path: 'playwright/.auth/user.json' })
  await browser.close()
}
```

**CI configuration (GitHub Actions):**
```yaml
- name: Install Playwright browsers
  run: npx playwright install chromium  # only what you need, not all browsers

- name: Run E2E tests
  run: npx playwright test --shard=${{ matrix.shard }}/4  # split across 4 runners

# playwright.config.ts — trace on first retry only
use: {
  trace: 'on-first-retry',   # not 'on' — too slow; not 'off' — blind on failure
  screenshot: 'only-on-failure',
}
```

**Accessibility testing:**
```typescript
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test('homepage has no a11y violations', async ({ page }) => {
  await page.goto('/')
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze()
  expect(results.violations).toEqual([])
})

// Scan only a specific revealed element after interaction
test('modal is accessible', async ({ page }) => {
  await page.getByRole('button', { name: 'Open dialog' }).click()
  const results = await new AxeBuilder({ page })
    .include('[role="dialog"]')
    .analyze()
  expect(results.violations).toEqual([])
})
```

- [ ] **Step 4: Verify**

```bash
head -40 plugins/rad-testing/skills/testing-playwright/SKILL.md
```

---

### Task 5: Build `testing-mocks` skill

**Files:**
- Create: `plugins/rad-testing/skills/testing-mocks/SKILL.md`

**Research steps before writing:**

- [ ] **Step 1: Run NotebookLM queries 13–16**

```bash
notebooklm ask "What does this notebook say about WHEN to mock — conditions that justify mocking vs when to avoid it, including guidance on financial cost, network boundaries, animation, callback props, internal modules, child components, and E2E tests?"
notebooklm ask "What does this notebook say about MSW as the recommended network mocking tool — how it works, why it's preferred over patching fetch/axios, and how it eliminates flaky CI behavior?"
notebooklm ask "What does this notebook say about theatre tests — how over-mocking leads to green CI but broken production, and what strategies prevent it?"
notebooklm ask "What does this notebook say about test doubles taxonomy — the differences between fakes, stubs, spies, and mocks?"
```

- [ ] **Step 2: Fetch official sources**

```bash
# https://mswjs.io/docs/concepts
# https://mswjs.io/docs/best-practices/avoid-request-assertions
# https://kentcdodds.com/blog/the-merits-of-mocking
```

- [ ] **Step 3: Write SKILL.md**

**Frontmatter:**
```markdown
---
name: testing-mocks
description: "This skill should be used when the user asks about 'when to mock', 'MSW', 'Mock Service Worker', 'vi.mock', 'vi.spyOn', 'vi.fn', 'test doubles', 'stubs vs mocks', 'theatre tests', 'over-mocking', 'mocking strategy', 'should I mock this', 'mock the database', 'mock network requests', 'msw handlers', or 'asserting on requests'."
---
```

Content must cover:

**Mock decision framework (the decision tree):**
```
Is this a real boundary you don't control? (payment API, 3rd-party service)
  → YES: Mock it
Is this a network call in a unit/integration test?
  → YES: Use MSW
Is this a slow side effect? (email sending, PDF generation)
  → YES: Mock it
Is this an internal module / child component / function in YOUR codebase?
  → NO: Do not mock — test the real thing
Is this an E2E test?
  → NO: Do not mock (except payment endpoints)
Does mocking save milliseconds but not real test time?
  → NO: Do not mock
```

**MSW setup:**
```typescript
// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw'

export const handlers = [
  http.get('/api/user', () => {
    return HttpResponse.json({ id: '1', name: 'Jane' })
  }),
  http.post('/api/checkout', async ({ request }) => {
    const body = await request.json()
    if (!body.items?.length) {
      return HttpResponse.json({ error: 'No items' }, { status: 400 })
    }
    return HttpResponse.json({ orderId: 'ord_123' })
  }),
]

// src/mocks/server.ts (Node / Vitest)
import { setupServer } from 'msw/node'
import { handlers } from './handlers'
export const server = setupServer(...handlers)

// vitest.setup.ts
import { server } from './src/mocks/server'
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

**Per-test handler overrides:**
```typescript
it('shows error when API fails', async () => {
  server.use(
    http.get('/api/user', () => {
      return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 })
    })
  )
  // render component, assert error state shown
})
// After test, server.resetHandlers() removes the override
```

**Why NOT to assert on requests (MSW best practice):**
```typescript
// WRONG — tests implementation detail (the fetch call), not behavior
let capturedRequest: Request | undefined
server.use(
  http.post('/api/order', ({ request }) => {
    capturedRequest = request  // ← capturing to assert later
    return HttpResponse.json({ id: 'ord_1' })
  })
)
await submitOrder()
expect(capturedRequest).toBeDefined()  // ← this is an implementation detail test

// CORRECT — assert on the UI response to the API
await submitOrder()
await expect(screen.findByText('Order confirmed!')).resolves.toBeInTheDocument()
```

**Test doubles taxonomy:**
| Type | Has real logic? | Records calls? | Use when |
|---|---|---|---|
| **Stub** | No — returns fixed data | No | You need a value, don't care about calls |
| **Spy** | Yes — wraps real impl | Yes | You want to verify a real method was called |
| **Mock** | No — scripted responses | Yes | You need to verify calls AND control responses |
| **Fake** | Yes — simplified impl | No | In-memory DB, in-memory email service |

**Theatre test pattern (what to avoid):**
```typescript
// THEATRE — everything mocked, tests that code calls things, not that it works
vi.mock('./api')
vi.mock('./database')
vi.mock('./emailService')
// Tests pass in CI. Real app: database writes fail silently.
// This is the AI over-mocking pattern — verified the code's wiring, not its behavior.
```

- [ ] **Step 4: Verify**

```bash
head -40 plugins/rad-testing/skills/testing-mocks/SKILL.md
```

---

### Task 6: Build `testing-async` skill

**Files:**
- Create: `plugins/rad-testing/skills/testing-async/SKILL.md`

**Research steps before writing:**

- [ ] **Step 1: Run NotebookLM queries 17–19**

```bash
notebooklm ask "What does this notebook cover about async testing patterns — waitFor usage, the difference between getBy*, queryBy*, and findBy* queries, timing pitfalls, and false positives on async code?"
notebooklm ask "What does this notebook say about fake timers in Vitest — vi.useFakeTimers(), vi.setSystemTime(), how to advance time, and common gotchas?"
notebooklm ask "What does this notebook cover about testing concurrent or parallel async operations, Promise chains, and async state updates in React components?"
```

- [ ] **Step 2: Fetch official sources**

```bash
# https://testing-library.com/docs/dom-testing-library/api-async
# https://vitest.dev/api/vi#vi-usefaketimers
```

- [ ] **Step 3: Write SKILL.md**

**Frontmatter:**
```markdown
---
name: testing-async
description: "This skill should be used when the user asks about 'waitFor', 'findBy', 'async testing', 'fake timers', 'vi.useFakeTimers', 'vi.setSystemTime', 'async state updates', 'testing Promises', 'false positive tests', 'test always passes', 'missing await', 'getBy vs findBy vs queryBy', or 'async React components'."
---
```

**RTL boundary note (include this in the skill body):**

> **Scope:** This skill covers the async variants of Testing Library queries (`findBy*`, `waitFor`) and Vitest timer APIs. For synchronous RTL query selection (`getByRole`, `getByLabel`, etc.), custom render wrappers, and `renderHook`, see `rad-react` → `react-engineering`. The split is: `rad-testing/testing-async` owns *how to handle timing and async* — `rad-react/react-engineering` owns *which queries to use and how to render*.

Content must cover:

**Query selector guide (Testing Library):**
```typescript
// getBy* — throws if not found. Use when element MUST exist.
screen.getByRole('button', { name: 'Submit' })

// queryBy* — returns null if not found. Use to assert element DOES NOT exist.
expect(screen.queryByText('Error')).not.toBeInTheDocument()

// findBy* — returns Promise, retries until found or timeout. Use for async.
const button = await screen.findByRole('button', { name: 'Submit' })
```

**waitFor patterns and pitfalls:**
```typescript
// CORRECT — wait for the effect of an async action
await userEvent.click(submitButton)
await waitFor(() => {
  expect(screen.getByText('Saved!')).toBeInTheDocument()
})

// GOTCHA — waitFor only waits for the callback to stop throwing.
// If callback has multiple assertions, first failure re-runs the whole thing.
// Keep waitFor callbacks to ONE assertion.
await waitFor(() => {
  expect(screen.getByText('Saved!')).toBeInTheDocument()
  expect(screen.queryByText('Error')).not.toBeInTheDocument() // ← AVOID
})

// CORRECT — split into sequential waitFor calls
await waitFor(() => expect(screen.getByText('Saved!')).toBeInTheDocument())
expect(screen.queryByText('Error')).not.toBeInTheDocument()  // now synchronous

// TRAP — false positive from not awaiting
// This test ALWAYS passes even when it should fail:
it('shows error', () => {  // ← missing async
  userEvent.click(submitButton)  // ← missing await
  waitFor(() => expect(screen.getByText('Error')).toBeInTheDocument())  // ← missing await
})
```

**Fake timers:**
```typescript
beforeEach(() => {
  vi.useFakeTimers()
})

afterEach(() => {
  vi.useRealTimers()  // CRITICAL — always restore or later tests break
})

it('shows toast for 3 seconds then hides', () => {
  render(<Toast message="Saved!" duration={3000} />)
  expect(screen.getByText('Saved!')).toBeInTheDocument()

  vi.advanceTimersByTime(3000)

  expect(screen.queryByText('Saved!')).not.toBeInTheDocument()
})

// GOTCHA — fake timers conflict with async utilities
// If your component uses setTimeout AND a real Promise, you need:
vi.useFakeTimers({ shouldAdvanceTime: true })
// Or manually flush microtasks:
await vi.runAllTimersAsync()
```

**System time control:**
```typescript
it('shows "expired" for items past their date', () => {
  vi.setSystemTime(new Date('2026-01-15'))  // freeze time

  render(<ExpiryBadge expiresAt="2026-01-14" />)

  expect(screen.getByText('Expired')).toBeInTheDocument()
})
```

**Testing async state updates in React:**
```typescript
it('loads and displays user profile', async () => {
  // MSW handler returns { name: 'Jane' } for GET /api/user
  render(<UserProfile userId="1" />)

  // Loading state first
  expect(screen.getByRole('progressbar')).toBeInTheDocument()

  // Wait for data to load
  expect(await screen.findByText('Jane')).toBeInTheDocument()

  // Loading state gone
  expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
})
```

- [ ] **Step 4: Verify**

```bash
head -40 plugins/rad-testing/skills/testing-async/SKILL.md
```

---

### Task 7: Build `testing-architecture` skill

**Files:**
- Create: `plugins/rad-testing/skills/testing-architecture/SKILL.md`

**Research steps before writing:**

- [ ] **Step 1: Run NotebookLM queries 20–23**

```bash
notebooklm ask "What does this notebook say about how Vitest, Testing Library, MSW, and Playwright work together as a unified testing strategy — which tool owns which concern?"
notebooklm ask "What does this notebook cover about test file organization — naming conventions, co-location vs separate directories, and what makes a test suite maintainable at scale?"
notebooklm ask "What does this notebook say about coverage thresholds — is 100% coverage a goal, what does diminishing returns look like, and what is meaningful coverage?"
notebooklm ask "What does this notebook say about test data management — fixture patterns, factory functions, seeding, teardown, and avoiding shared state between tests?"
```

- [ ] **Step 2: Write SKILL.md**

**Frontmatter:**
```markdown
---
name: testing-architecture
description: "This skill should be used when the user asks about 'test file structure', 'where to put tests', 'test organization', 'coverage thresholds', 'coverage percentage', 'how much coverage', '100% coverage', 'test data factories', 'fixture factories', 'test naming conventions', 'co-locate tests', 'vitest playwright together', 'MSW vitest playwright', 'cross-tool testing', or 'test isolation rules'."
---
```

Content must cover:

**The four-tool architecture (who owns what):**
| Tool | Layer | Owns |
|---|---|---|
| TypeScript + ESLint | Static | Type errors, lint violations — zero runtime cost |
| Vitest | Unit + Integration | Pure logic, module contracts, API handlers |
| Vitest + Testing Library + MSW | Component Integration | Component behavior with real child renders + mocked network |
| Playwright | E2E | Critical user flows end-to-end in real browser |

**File structure for a full-stack app:**
```
src/
├── components/
│   ├── LoginForm.tsx
│   └── LoginForm.test.tsx     # co-located component test
├── lib/
│   ├── auth.ts
│   └── auth.test.ts           # co-located unit test
└── mocks/
    ├── handlers.ts             # MSW handlers (shared: vitest + playwright)
    ├── server.ts               # Vitest server
    └── browser.ts              # Browser/Storybook worker

tests/                          # Playwright E2E only
├── e2e/
│   ├── auth.spec.ts
│   └── checkout.spec.ts
├── page-objects/
│   └── LoginPage.ts
└── fixtures/
    └── users.ts

vitest.config.ts
playwright.config.ts
vitest.setup.ts                 # global beforeAll/afterAll for MSW server
```

**Coverage philosophy:**
- 70–80% overall is the practical sweet spot for most apps
- 100% is achievable but the last 20% tests code with no logic (getters, type exports, index re-exports)
- Coverage to prioritize: business logic, data transforms, validation, error handling paths
- Coverage to skip: framework wiring code, generated code, type definitions, configuration files
- Never set `100` as a hard threshold — it incentivizes trivial tests

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 70,    // branches harder to saturate; 70 is realistic
        statements: 80,
      },
      exclude: [
        'src/types/**',
        'src/mocks/**',
        '**/*.config.*',
        '**/*.d.ts',
        '**/index.ts',   // re-export barrels
      ]
    }
  }
})
```

**Test data factories:**
```typescript
// tests/fixtures/factory.ts
export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: crypto.randomUUID(),
    name: 'Test User',
    email: `test-${Date.now()}@example.com`,
    role: 'member',
    createdAt: new Date(),
    ...overrides,
  }
}

// In a test
const admin = createUser({ role: 'admin' })
const guest = createUser({ name: 'Guest', email: 'guest@test.com' })
```

**Test isolation rules:**
- Each test gets its own data via factory — no shared `const user = createUser()` at module scope
- MSW `server.resetHandlers()` in `afterEach` — never rely on handler state across tests
- Database tests: wrap each test in a transaction, roll back at end — never delete manually
- Never use `Date.now()` or `Math.random()` in assertions — factories control IDs, fake timers control time

**Naming conventions:**
```
LoginForm.test.tsx          # unit/integration
LoginForm.spec.tsx          # also fine, pick one convention
auth.test.ts                # lib/utility
auth.spec.ts                # E2E tends to use .spec, unit/integration .test
                            # pick one pair and use consistently
```

- [ ] **Step 3: Verify**

```bash
head -40 plugins/rad-testing/skills/testing-architecture/SKILL.md
```

---

### Task 8: Build `testing-reviewer` agent

**Files:**
- Create: `plugins/rad-testing/agents/testing-reviewer.md`

> **Critical:** Agent files are flat `.md` files directly in `agents/`. They are NOT `AGENT.md` inside a subdirectory. The correct path is `agents/testing-reviewer.md`.

**Reference:** Read `plugins/rad-react/agents/react-reviewer.md` for the exact format.

- [ ] **Step 1: Read reference agent**

```bash
cat plugins/rad-react/agents/react-reviewer.md
```

- [ ] **Step 2: Write `agents/testing-reviewer.md`**

The file must begin with this frontmatter (matching the pattern from `react-reviewer.md`):

```markdown
---
name: testing-reviewer
model: sonnet
color: orange
description: >
  Reviews test files for anti-patterns: fixed timeouts, over-mocking of internal modules,
  missing await on userEvent/waitFor/findBy calls, unsafe fake timer usage, brittle CSS/XPath
  locators, implementation detail testing, and coverage theatre. Use when completing a test
  suite, before committing test files, or when the user says "review my tests", "check my
  test quality", "are my tests good", "audit my test suite", or "check for testing
  anti-patterns".
whenToUse: >
  Use this agent when a user has written or modified test files and wants them reviewed for
  correctness, maintainability, and anti-pattern avoidance. Also trigger proactively after
  significant test writing work.
tools:
  - Read
  - Glob
  - Grep
  - Bash
---
```

Then the agent body must instruct it to scan all test files and report findings by severity:

The agent must be configured to audit test files for these specific anti-patterns (with detection patterns and severity):

**High severity (always report):**
- Fixed timeouts: `waitForTimeout`, `setTimeout` in test body, `sleep`
- Over-mocking internal modules: `vi.mock('./` more than 3 times in one test file
- Missing `await` on `userEvent.*` calls (produces false positives)
- Missing `await` on `waitFor` / `findBy*` queries
- `vi.useFakeTimers()` without matching `vi.useRealTimers()` in afterEach
- `screen.debug()` left in committed test code
- Assertions on request objects captured from MSW handlers (implementation detail testing)

**Medium severity (report with context):**
- `getBy*` used where element may not exist (should be `queryBy*`)
- Multiple assertions inside a single `waitFor` callback
- Shallow rendering import (`import { shallow } from 'enzyme'`)
- `wrapper.instance()`, `wrapper.state()`, `wrapper.find('ClassName')` — Enzyme implementation detail patterns
- CSS selector locators in Playwright tests (`.btn`, `#submit`, `div > span`)
- XPath locators in Playwright tests (`//div[@class=...]`)
- `page.waitForTimeout` in Playwright tests

**Low severity (suggest improvement):**
- `data-testid` used where a role/label locator is possible
- Test description uses "should" prefix (verbose, prefer "does" or declarative)
- Test file has no `afterEach` cleanup when MSW server is used
- `console.log` or `console.error` in test body

- [ ] **Step 3: Verify**

```bash
cat plugins/rad-testing/agents/testing-reviewer.md
```

Expected: file starts with `---` frontmatter block containing `name`, `model`, `color`, `description`, `whenToUse`, and `tools` fields.

---

### Task 9: Final validation and marketplace.json update

**Files:**
- Read: `.claude-plugin/marketplace.json`
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Verify all skill files exist**

```bash
find plugins/rad-testing -name "*.md" | sort
```

Expected output:
```
plugins/rad-testing/README.md
plugins/rad-testing/agents/testing-reviewer.md
plugins/rad-testing/skills/testing-architecture/SKILL.md
plugins/rad-testing/skills/testing-async/SKILL.md
plugins/rad-testing/skills/testing-mocks/SKILL.md
plugins/rad-testing/skills/testing-philosophy/SKILL.md
plugins/rad-testing/skills/testing-playwright/SKILL.md
plugins/rad-testing/skills/testing-vitest/SKILL.md
```

- [ ] **Step 2: Read marketplace.json to understand entry format**

```bash
head -60 .claude-plugin/marketplace.json
```

- [ ] **Step 3: Add rad-testing entry to `.claude-plugin/marketplace.json`**

Add an entry matching the format of other plugin entries. Key fields:
- `name`: "rad-testing"
- `description`: match the plugin.json description
- `version`: "1.0.0"
- `category`: "testing"
- `tags`: match plugin.json keywords

- [ ] **Step 4: Verify plugin.json is valid JSON**

```bash
python3 -m json.tool plugins/rad-testing/.claude-plugin/plugin.json
```

Expected: parsed JSON printed without error. If error: fix the syntax before committing.

- [ ] **Step 5: Commit**

```bash
git add plugins/rad-testing/ .claude-plugin/marketplace.json
git commit -m "feat: add rad-testing plugin — 6 skills, 1 agent covering Vitest, Playwright, MSW, async patterns, and cross-tool testing architecture"
```

---

## Self-Review

**Spec coverage check:**

| Requirement | Covered by |
|---|---|
| Testing strategy / philosophy | Task 2 — `testing-philosophy` |
| Vitest config, coverage, browser mode, monorepo | Task 3 — `testing-vitest` |
| Playwright POM, locators, flaky tests, CI, a11y | Task 4 — `testing-playwright` |
| Mock strategy, MSW, theatre tests | Task 5 — `testing-mocks` |
| Async patterns, waitFor, fake timers | Task 6 — `testing-async` |
| Cross-tool architecture, file structure, coverage thresholds, test data | Task 7 — `testing-architecture` |
| Anti-pattern enforcement agent | Task 8 — `testing-reviewer` agent |
| Plugin scaffolding (plugin.json, README) | Task 1 |
| Marketplace registration | Task 9 |
| NotebookLM queries documented | Source Strategy + each task's Step 1 |
| Official online sources documented | Source Strategy + each task's Step 2 |

**No placeholders found** — all tasks contain actual code, commands, and expected outputs.

**Type consistency** — No cross-task type references; each skill is self-contained.

---

## Notes on Scope Boundaries

These topics are intentionally **excluded** from `rad-testing` — they belong to other plugins:

| Topic | Lives in | Reason |
|---|---|---|
| Synchronous RTL queries (`getByRole`, `getByLabel`), `renderHook`, custom render wrappers | `rad-react` — `react-engineering` | Framework-specific; `rad-testing` owns the async variants only |
| Fastify `.inject()` in-process testing | `rad-fastify` — `fastify-testing` | Framework-specific |
| Next.js Server Component testing, route handler testing | `rad-nextjs` — `nextjs-testing` | Framework-specific |
| axe-core deep dive, WCAG rule reference | `rad-a11y` — `a11y-testing` | `rad-testing` only covers the Playwright integration surface |
| Zod schema testing patterns | `rad-zod` | Zod-specific validation test patterns belong there |
| Electron testing | Out of scope for v1.0 | Notebook has sources but the audience is small; revisit for v1.1 |
