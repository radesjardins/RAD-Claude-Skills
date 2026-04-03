---
name: chrome-ext-testing
description: >
  This skill should be used when writing or setting up tests for a Chrome extension. Trigger
  when: "test chrome extension", "extension unit test", "extension e2e test", "Vitest extension",
  "Playwright extension", "@webext-core/fake-browser", "test content script", "test service
  worker", "test messaging", "test storage", "extension integration test", "test permission
  flow", "extension test framework", "mock chrome API", "browser mode testing".
---

# Chrome Extension Testing

Extension testing spans three tiers: unit tests for pure logic, integration tests for messaging/storage/UI, and E2E tests for multi-context journeys. Vitest with `@webext-core/fake-browser` handles the first two. Playwright handles E2E with real browser contexts.

## Framework Selection

| Tier | Framework | Why |
|------|-----------|-----|
| Unit | Vitest | Fast, Vite-native, works with WXT |
| Integration | Vitest Browser Mode | Real browser DOM for authentic behavior |
| E2E | Playwright | Isolated browser contexts, Shadow DOM piercing |

## Unit Testing

Test pure logic, utilities, and API-mocked code with `@webext-core/fake-browser`:

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    setupFiles: ['./test/setup.ts'],
  },
});

// test/setup.ts
import { fakeBrowser } from '@webext-core/fake-browser';
vi.stubGlobal('browser', fakeBrowser);
vi.stubGlobal('chrome', fakeBrowser);
```

What to test:
- Algorithms, formatting helpers, data transformers
- Storage read/write logic (fake-browser polyfills chrome.storage)
- Message routing logic (fake-browser polyfills chrome.runtime)
- Utility functions

```typescript
import { describe, it, expect } from 'vitest';

describe('storage utils', () => {
  it('reads with defaults', async () => {
    const result = await chrome.storage.local.get({ theme: 'light' });
    expect(result.theme).toBe('light');
  });

  it('persists and retrieves data', async () => {
    await chrome.storage.local.set({ count: 42 });
    const { count } = await chrome.storage.local.get('count');
    expect(count).toBe(42);
  });
});
```

## Integration Testing

Test UI interactions, messaging, and storage flows:

- Use Vitest Browser Mode for authentic DOM/CSS behavior
- Test loading, error, and empty states
- Test keyboard navigation and accessibility
- Mock external APIs and network requests

```typescript
describe('Popup', () => {
  it('loads settings from storage', async () => {
    await chrome.storage.local.set({ theme: 'dark' });
    render(<Popup />);
    expect(screen.getByRole('button', { name: /dark/i })).toBeInTheDocument();
  });

  it('saves settings on change', async () => {
    render(<Popup />);
    fireEvent.click(screen.getByRole('button', { name: /toggle/i }));
    const { theme } = await chrome.storage.local.get('theme');
    expect(theme).toBe('dark');
  });
});
```

## E2E Testing with Playwright

Test multi-context journeys across service worker, content scripts, and UI:

```typescript
import { test, expect, chromium } from '@playwright/test';

test('content script injects UI', async () => {
  const context = await chromium.launchPersistentContext('', {
    args: [`--load-extension=.output/chrome-mv3`],
  });

  const page = await context.newPage();
  await page.goto('https://example.com');

  // Pierce Shadow DOM to find injected UI
  const button = page.locator('my-extension >> button');
  await expect(button).toBeVisible();
});
```

### E2E Scenarios Worth Testing
- Service worker termination recovery (terminate via `chrome.processes`, verify UI detects and retries)
- Permission grant/deny flows
- Full data flow: host page → content script → service worker → storage → UI update
- Install/update lifecycle (onboarding page opens)

## Test Quality Standards

- Test user-visible behavior, not implementation details
- Use accessibility-first selectors: `getByRole`, `getByLabelText`, `data-testid`
- Each test gets fresh storage (clear in beforeEach)
- Use async, auto-waiting assertions (`toBeVisible()`)
- Never use hard-coded `sleep()` or timeouts

## Additional Resources

### Reference Files

- **`references/testing-guide.md`** — Detailed test patterns for permissions, messaging, storage, and service worker testing
