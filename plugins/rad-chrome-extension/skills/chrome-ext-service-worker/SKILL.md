---
name: chrome-ext-service-worker
description: >
  This skill should be used when working with Chrome extension service workers or background
  scripts. Trigger when: "service worker lifecycle", "background script", "extension service
  worker", "chrome.alarms", "offscreen document", "service worker restart", "top-level listener",
  "service worker idle", "event listener registration", "chrome.offscreen", "service worker
  termination", "state rehydration", "persistent background", "MV3 background", "service worker
  wake-up", "keepalive", "setTimeout in service worker".
---

# Chrome Extension Service Workers

MV3 replaced persistent background pages with ephemeral, event-driven service workers. They wake to process events and terminate after ~30 seconds of inactivity. All in-memory state is lost on termination. Code must be structured around this fundamental constraint.

## The Ephemeral Lifecycle

```
[Event occurs] → [Worker starts] → [Script executes top-to-bottom]
→ [Registered listeners fire] → [~30s idle] → [Worker terminates]
→ [All global variables lost]
```

Every handler must assume zero prior state. Rehydrate from storage at the start of every event.

## Hard Rules

### 1. Register Listeners Synchronously at Top Level

The browser scans for listeners on the first turn of the event loop. Listeners inside promises, callbacks, `setTimeout`, or `async` functions will NOT be registered in time.

```typescript
// CORRECT — synchronous, top-level
export default defineBackground(() => {
  chrome.runtime.onMessage.addListener(handleMessage);
  chrome.alarms.onAlarm.addListener(handleAlarm);
  chrome.runtime.onInstalled.addListener(handleInstall);
});

// WRONG — async, buried inside callback
export default defineBackground(async () => {
  await someSetup();
  // TOO LATE — worker may have already handled the event
  chrome.runtime.onMessage.addListener(handleMessage);
});
```

### 2. Never Use setTimeout/setInterval

Standard timers are canceled on termination. Replace with `chrome.alarms`:

```typescript
// WRONG — unreliable
setTimeout(() => checkForUpdates(), 60000);

// CORRECT — survives worker restarts
chrome.alarms.create('check-updates', { periodInMinutes: 1 });
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'check-updates') checkForUpdates();
});
```

### 3. Never Store State in Global Variables

```typescript
// WRONG — lost on restart
let userPrefs = {};

// CORRECT — persist to storage
async function getPrefs() {
  const { prefs } = await chrome.storage.local.get('prefs');
  return prefs ?? DEFAULT_PREFS;
}
```

### 4. Use fetch(), Not XMLHttpRequest

`XMLHttpRequest` is unavailable in service workers. All network requests use `fetch()`.

## State Rehydration Pattern

"Hydrate, Don't Store" — every event handler reads current state from storage:

```typescript
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'getStatus') {
    chrome.storage.local.get('status').then(({ status }) => {
      sendResponse(status ?? { active: false });
    });
    return true; // async response
  }
});
```

## Offscreen Documents

For tasks requiring DOM that the service worker cannot access:

```typescript
async function parseHTML(html: string): Promise<string> {
  // Create offscreen document if not exists
  const contexts = await chrome.runtime.getContexts({
    contextTypes: [chrome.runtime.ContextType.OFFSCREEN_DOCUMENT],
  });

  if (!contexts.length) {
    await chrome.offscreen.createDocument({
      url: 'offscreen.html',
      reasons: [chrome.offscreen.Reason.DOM_PARSER],
      justification: 'Parse HTML content',
    });
  }

  // Delegate via message passing
  return chrome.runtime.sendMessage({ action: 'parseHTML', html });
}
```

Valid reasons: `CLIPBOARD`, `DOM_PARSER`, `AUDIO_PLAYBACK`, `DOM_SCRAPING`, `BLOBS`, `GEOLOCATION`, `WORKERS`, and more.

Only one offscreen document can exist at a time.

## Additional Resources

### Reference Files

- **`references/lifecycle-patterns.md`** — Advanced patterns: keepalive techniques, alarm scheduling, install/update handlers, and long-running operation strategies
