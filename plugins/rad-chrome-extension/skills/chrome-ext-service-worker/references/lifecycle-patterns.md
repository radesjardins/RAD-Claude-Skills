# Service Worker Lifecycle Patterns

## Installation and Update Handlers

```typescript
export default defineBackground(() => {
  // Fires on first install and on extension updates
  chrome.runtime.onInstalled.addListener((details) => {
    if (details.reason === 'install') {
      // First install — set defaults, open onboarding
      chrome.storage.local.set({ version: 1, onboarded: false });
      chrome.tabs.create({ url: 'onboarding.html' });
    }

    if (details.reason === 'update') {
      // Extension updated — run migrations
      migrateData(details.previousVersion);
    }
  });

  // Register all other listeners synchronously
  chrome.alarms.onAlarm.addListener(handleAlarm);
  chrome.runtime.onMessage.addListener(handleMessage);
});
```

## Alarm Scheduling Patterns

### One-Time Delayed Task

```typescript
// Schedule a task for 5 minutes from now
chrome.alarms.create('delayed-task', { delayInMinutes: 5 });

// Handle it
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'delayed-task') {
    performDelayedTask();
  }
});
```

### Periodic Task

```typescript
// Run every 30 minutes
chrome.alarms.create('periodic-sync', { periodInMinutes: 30 });

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'periodic-sync') {
    syncData();
  }
});
```

### Named Alarms for Different Tasks

```typescript
const ALARMS = {
  SYNC: 'sync-data',
  CLEANUP: 'cleanup-cache',
  NOTIFY: 'check-notifications',
} as const;

chrome.alarms.create(ALARMS.SYNC, { periodInMinutes: 15 });
chrome.alarms.create(ALARMS.CLEANUP, { periodInMinutes: 60 });
chrome.alarms.create(ALARMS.NOTIFY, { periodInMinutes: 5 });

chrome.alarms.onAlarm.addListener((alarm) => {
  switch (alarm.name) {
    case ALARMS.SYNC: return syncData();
    case ALARMS.CLEANUP: return cleanupCache();
    case ALARMS.NOTIFY: return checkNotifications();
  }
});
```

## Long-Running Operations

The service worker may terminate during long operations. Strategies:

### Strategy 1: Chunk Work with Alarms

Break large tasks into small chunks, scheduling each via alarm:

```typescript
chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name === 'process-batch') {
    const { queue } = await chrome.storage.local.get('queue');
    if (!queue?.length) return;

    // Process one batch
    const batch = queue.slice(0, 10);
    const remaining = queue.slice(10);
    await processBatch(batch);

    // Save progress and schedule next batch
    await chrome.storage.local.set({ queue: remaining });
    if (remaining.length > 0) {
      chrome.alarms.create('process-batch', { delayInMinutes: 0.1 });
    }
  }
});
```

### Strategy 2: Offscreen Document for DOM Work

For DOM-heavy operations that take time:

```typescript
// Create offscreen doc for processing
await chrome.offscreen.createDocument({
  url: 'processor.html',
  reasons: [chrome.offscreen.Reason.DOM_SCRAPING],
  justification: 'Process large HTML dataset',
});

// Let the offscreen document do the work
// It can use DOM APIs and report progress via messages
chrome.runtime.sendMessage({
  action: 'processData',
  target: 'offscreen',
  data: largeDataset,
});
```

### Strategy 3: Keepalive with Active Ports

A service worker stays alive while it has active port connections:

```typescript
// Popup/side panel keeps worker alive by maintaining a port
const port = chrome.runtime.connect({ name: 'keepalive' });

// Service worker
chrome.runtime.onConnect.addListener((port) => {
  if (port.name === 'keepalive') {
    // Worker stays alive while this port is open
    port.onDisconnect.addListener(() => {
      // UI closed, worker may terminate soon
    });
  }
});
```

**Warning:** Do not abuse keepalive. The 30-second idle timeout exists for performance. Only keep the worker alive when actively processing user-visible tasks.

## Startup Handling

```typescript
export default defineBackground(() => {
  // Fires when the extension starts (browser launch, enable, update)
  chrome.runtime.onStartup.addListener(async () => {
    // Rehydrate critical state
    const { settings } = await chrome.storage.local.get('settings');
    // Set up alarms if needed
    const alarms = await chrome.alarms.getAll();
    if (!alarms.find(a => a.name === 'periodic-sync')) {
      chrome.alarms.create('periodic-sync', { periodInMinutes: 30 });
    }
  });
});
```

## Debugging Service Workers

### Access the Console
Navigate to `chrome://extensions`, find your extension, click "Inspect views: service worker".

### Force Termination
Navigate to `chrome://serviceworker-internals`, find your extension's worker, and click "Stop" to simulate idle termination. Test that your extension recovers correctly.

### Common Debugging Issues

| Symptom | Likely Cause |
|---------|-------------|
| Event not firing after restart | Listener not registered at top level |
| State lost between events | Using global variables instead of storage |
| Timer not executing | Using `setTimeout` instead of `chrome.alarms` |
| Fetch failing | Using `XMLHttpRequest` (not available) |
| Message response is `null` | Missing `return true` in async listener |
| Worker never wakes | Listener registered inside `async` function |

## Declarative Net Request

For network request interception (replaces MV2's `webRequest`):

```typescript
// Rules defined in a JSON file
// rules.json
[{
  "id": 1,
  "priority": 1,
  "action": { "type": "block" },
  "condition": {
    "urlFilter": "tracking.example.com",
    "resourceTypes": ["script", "xmlhttprequest"]
  }
}]
```

```json
// manifest.json (via WXT config)
{
  "declarative_net_request": {
    "rule_resources": [{
      "id": "ruleset_1",
      "enabled": true,
      "path": "rules.json"
    }]
  }
}
```

Dynamic rules can be updated at runtime:
```typescript
chrome.declarativeNetRequest.updateDynamicRules({
  addRules: [newRule],
  removeRuleIds: [oldRuleId],
});
```
