---
name: chrome-ext-messaging
description: >
  This skill should be used when implementing messaging between Chrome extension components or
  when the user asks about inter-process communication in extensions. Trigger when: "extension
  messaging", "chrome.runtime.sendMessage", "chrome.tabs.sendMessage", "content script messaging",
  "port.postMessage", "runtime.connect", "Protocol Map", "@webext-core/messaging", "message
  passing", "extension IPC", "sendMessage vs connect", "async message response", "return true
  onMessage", "typed messaging", "message schema".
---

# Chrome Extension Messaging

All extension contexts are strictly siloed — no shared memory. Communication happens exclusively through async message passing with JSON-serializable data. Choose the right pattern for each use case and enforce type safety through Protocol Maps.

## Messaging Patterns

### One-Time Request-Response

For standard async tasks (popup requests data from service worker, content script sends page data):

```typescript
// Sender (popup or content script)
const response = await chrome.runtime.sendMessage({
  action: 'getData',
  query: 'recent',
});

// Receiver (service worker)
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'getData') {
    fetchData(msg.query).then(sendResponse);
    return true; // CRITICAL: keeps channel open for async response
  }
});
```

To send to a specific tab's content script:
```typescript
chrome.tabs.sendMessage(tabId, { action: 'highlight', selector: '.target' });
```

### Long-Lived Ports

For continuous data streams (live AI chat, progress tracking, persistent connections):

```typescript
// Initiate connection
const port = chrome.runtime.connect({ name: 'ai-chat' });

// Send messages
port.postMessage({ prompt: 'Explain this page' });

// Receive responses
port.onMessage.addListener((msg) => {
  console.log('Response chunk:', msg.text);
});

// Detect disconnection
port.onDisconnect.addListener(() => {
  console.log('Connection closed');
});
```

### When to Use Which

| Pattern | Use Case | Lifecycle |
|---------|----------|-----------|
| `sendMessage` | One-off request/response | Single exchange, then done |
| `connect` / `Port` | Streaming data, monitoring | Persistent until disconnect |

## Type-Safe Messaging with Protocol Maps

Use `@webext-core/messaging` to define TypeScript-enforced message contracts:

```typescript
// src/utils/messaging.ts
import { defineExtensionMessaging } from '@webext-core/messaging';

interface ProtocolMap {
  getData: (query: string) => DataResult;
  updateSettings: (settings: Settings) => void;
  getTabInfo: () => TabInfo;
}

export const { sendMessage, onMessage } = defineExtensionMessaging<ProtocolMap>();
```

Usage across contexts:
```typescript
// Sender — compiler verifies payload and return types
const result = await sendMessage('getData', 'recent');

// Receiver — handler signature enforced by TypeScript
onMessage('getData', ({ data: query }) => {
  return fetchData(query); // Must return DataResult
});
```

## Critical Async Rules

1. **Return `true` for async responses.** If the `onMessage` listener performs async work before calling `sendResponse`, the listener MUST return `true` to keep the message channel open.

2. **Async functions always return a Promise.** An `async` listener that doesn't explicitly return a value resolves to `undefined`, sending `null` to the sender and immediately closing the channel.

3. **Handle the "no receiver" error.** If a content script sends a message while the service worker is waking up, the message may be lost. Handle `chrome.runtime.lastError` explicitly.

## Message Design Rules

- Include `action` property for routing
- Include `to` and `from` for multi-context routing
- Keep payloads JSON-serializable (no functions, DOM nodes, classes)
- Validate all messages from content scripts in the service worker

## Additional Resources

### Reference Files

- **`references/messaging-patterns.md`** — Advanced patterns: port management, React hooks, error handling, and multi-context routing
