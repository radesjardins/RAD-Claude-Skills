# Detailed Extension Testing Guide

## Testing Permission Flows

### Dynamic Permission Request

```typescript
// Test that permission request UI handles grant
test('enables feature on permission grant', async () => {
  // Mock chrome.permissions.request to return true
  vi.spyOn(chrome.permissions, 'request').mockResolvedValue(true);

  render(<FeatureToggle />);
  fireEvent.click(screen.getByRole('button', { name: /enable advanced/i }));

  await waitFor(() => {
    expect(screen.getByText('Feature enabled')).toBeInTheDocument();
  });
  expect(chrome.permissions.request).toHaveBeenCalledWith({
    permissions: ['bookmarks'],
  });
});

// Test that permission deny is handled gracefully
test('shows explanation on permission deny', async () => {
  vi.spyOn(chrome.permissions, 'request').mockResolvedValue(false);

  render(<FeatureToggle />);
  fireEvent.click(screen.getByRole('button', { name: /enable advanced/i }));

  await waitFor(() => {
    expect(screen.getByText(/permission required/i)).toBeInTheDocument();
  });
});
```

### Update Warning Testing

When a new version adds permissions that trigger install warnings:
1. Build the packed `.crx` with the new permissions
2. Use Chrome's Extension Update Testing Tool to simulate the update
3. Verify the extension handles the "disabled pending permission acceptance" state

## Testing Messaging Flows

### Unit Testing Message Handlers

```typescript
describe('message handler', () => {
  it('responds to getData', async () => {
    // Set up test data
    await chrome.storage.local.set({ data: [1, 2, 3] });

    // Simulate message
    const response = await new Promise((resolve) => {
      handleMessage(
        { action: 'getData', query: 'all' },
        { id: chrome.runtime.id } as chrome.runtime.MessageSender,
        resolve
      );
    });

    expect(response).toEqual([1, 2, 3]);
  });
});
```

### Integration Testing: Content Script → Service Worker → UI

```typescript
// E2E with Playwright
test('full messaging flow', async ({ page, context }) => {
  // Navigate to host page
  await page.goto('https://example.com');

  // Click content script's injected button
  const button = page.locator('my-extension >> button.extract');
  await button.click();

  // Open extension popup
  const popup = await context.newPage();
  await popup.goto(`chrome-extension://${extensionId}/popup.html`);

  // Verify extracted data appears in popup
  await expect(popup.locator('[data-testid="extracted-title"]')).toHaveText('Example Domain');
});
```

### Service Worker Termination Resilience

```typescript
test('recovers from service worker termination', async ({ page, context }) => {
  // Send initial message (works)
  await page.evaluate(() => chrome.runtime.sendMessage({ action: 'ping' }));

  // Terminate service worker via chrome://serviceworker-internals
  // Or use chrome.processes API if available

  // Send another message — should recover
  const response = await page.evaluate(() =>
    chrome.runtime.sendMessage({ action: 'ping' })
      .catch(() => 'reconnected')
  );

  expect(response).toBeDefined();
});
```

## Testing Storage Flows

### Unit Testing with fake-browser

```typescript
import { fakeBrowser } from '@webext-core/fake-browser';

describe('storage service', () => {
  beforeEach(async () => {
    await chrome.storage.local.clear();
    await chrome.storage.sync.clear();
    await chrome.storage.session.clear();
  });

  it('persists settings to local storage', async () => {
    await saveSettings({ theme: 'dark', fontSize: 16 });
    const { settings } = await chrome.storage.local.get('settings');
    expect(settings).toEqual({ theme: 'dark', fontSize: 16 });
  });

  it('triggers onChanged when data updates', async () => {
    const listener = vi.fn();
    chrome.storage.onChanged.addListener(listener);

    await chrome.storage.local.set({ count: 1 });

    expect(listener).toHaveBeenCalledWith(
      { count: { newValue: 1 } },
      'local'
    );
  });
});
```

### Integration Testing: Reactive UI Updates

```typescript
test('UI updates when storage changes externally', async () => {
  render(<StatusDisplay />);

  // Initially shows default
  expect(screen.getByText('Status: idle')).toBeInTheDocument();

  // Simulate storage change from background
  await chrome.storage.local.set({ status: 'active' });

  // UI should react via onChanged listener
  await waitFor(() => {
    expect(screen.getByText('Status: active')).toBeInTheDocument();
  });
});
```

## Testing Content Script DOM Interaction

```typescript
describe('content script', () => {
  it('extracts page title', () => {
    document.title = 'Test Page';
    const result = extractPageInfo();
    expect(result.title).toBe('Test Page');
  });

  it('injects UI element', () => {
    injectButton();
    const button = document.querySelector('[data-extension-button]');
    expect(button).toBeTruthy();
    expect(button?.getAttribute('aria-label')).toBe('Open extension');
  });

  it('cleans up on removal', () => {
    const cleanup = injectButton();
    expect(document.querySelector('[data-extension-button]')).toBeTruthy();

    cleanup();
    expect(document.querySelector('[data-extension-button]')).toBeNull();
  });
});
```

## Testing Accessibility

```typescript
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('popup has no accessibility violations', async () => {
  const { container } = render(<Popup />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});

test('keyboard navigation works', async () => {
  render(<SettingsPanel />);
  const firstButton = screen.getByRole('button', { name: /theme/i });

  // Tab to first button
  await userEvent.tab();
  expect(firstButton).toHaveFocus();

  // Enter activates
  await userEvent.keyboard('{Enter}');
  expect(screen.getByRole('listbox')).toBeVisible();

  // Escape closes
  await userEvent.keyboard('{Escape}');
  expect(screen.queryByRole('listbox')).not.toBeInTheDocument();
  expect(firstButton).toHaveFocus(); // Focus restored
});
```

## Test Organization

```
tests/
├── unit/
│   ├── utils.test.ts           # Pure utility tests
│   ├── storage-service.test.ts # Storage logic
│   └── message-handler.test.ts # Message routing
├── integration/
│   ├── popup.test.tsx          # Popup UI + storage
│   ├── sidepanel.test.tsx      # Side panel UI
│   └── messaging.test.ts      # Cross-context messaging
└── e2e/
    ├── install-flow.spec.ts    # First install experience
    ├── content-script.spec.ts  # Content script injection
    └── full-journey.spec.ts    # Multi-context user flow
```

## Vitest Configuration for Extensions

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import { WxtVitest } from 'wxt/testing';

export default defineConfig({
  test: {
    mockReset: true,
    setupFiles: ['./test/setup.ts'],
  },
  plugins: [WxtVitest()],
});
```
