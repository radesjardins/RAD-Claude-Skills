# Advanced Messaging Patterns

## Port Management in React

Create a custom hook for managing extension ports in React components:

```typescript
// src/hooks/useExtensionPort.ts
import { useEffect, useRef, useCallback } from 'react';

export function useExtensionPort(portName: string) {
  const portRef = useRef<chrome.runtime.Port | null>(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const port = chrome.runtime.connect({ name: portName });
    portRef.current = port;
    setConnected(true);

    port.onDisconnect.addListener(() => {
      portRef.current = null;
      setConnected(false);
    });

    return () => {
      port.disconnect();
      portRef.current = null;
    };
  }, [portName]);

  const send = useCallback((message: unknown) => {
    portRef.current?.postMessage(message);
  }, []);

  return { port: portRef.current, send, connected };
}
```

## Handling Service Worker Wake-Up

Content scripts may send messages while the service worker is still starting. Handle gracefully:

```typescript
// Content script — retry on failure
async function sendWithRetry(message: unknown, maxRetries = 3): Promise<unknown> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await chrome.runtime.sendMessage(message);
      if (chrome.runtime.lastError) throw new Error(chrome.runtime.lastError.message);
      return response;
    } catch (err) {
      if (i === maxRetries - 1) throw err;
      await new Promise(r => setTimeout(r, 100 * (i + 1)));
    }
  }
}
```

## Multi-Context Message Routing

For complex extensions with many contexts, use a routing pattern:

```typescript
// src/utils/messaging.ts
interface MessageEnvelope<T = unknown> {
  action: string;
  from: 'popup' | 'sidepanel' | 'content' | 'background';
  to: 'popup' | 'sidepanel' | 'content' | 'background' | 'all';
  payload: T;
  requestId?: string;
}

// Service worker acts as central router
chrome.runtime.onMessage.addListener((msg: MessageEnvelope, sender, sendResponse) => {
  if (msg.to === 'background') {
    handleBackgroundMessage(msg, sendResponse);
    return true;
  }

  if (msg.to === 'content') {
    // Forward to specific tab's content script
    chrome.tabs.query({ active: true, currentWindow: true }, ([tab]) => {
      if (tab?.id) chrome.tabs.sendMessage(tab.id, msg);
    });
    return;
  }

  // Broadcast to all extension contexts
  if (msg.to === 'all') {
    broadcastToExtensionPages(msg);
  }
});
```

## React Component Messaging Hook

Auto-cleanup pattern for React components in popups/side panels:

```typescript
// src/hooks/useMessage.ts
import { useEffect, useCallback } from 'react';

export function useOnMessage<T>(
  action: string,
  handler: (payload: T) => void,
) {
  useEffect(() => {
    const listener = (msg: { action: string; payload: T }) => {
      if (msg.action === action) handler(msg.payload);
    };
    chrome.runtime.onMessage.addListener(listener);
    return () => chrome.runtime.onMessage.removeListener(listener);
  }, [action, handler]);
}

export function useSendMessage() {
  return useCallback(async (action: string, payload?: unknown) => {
    try {
      return await chrome.runtime.sendMessage({ action, payload });
    } catch (err) {
      console.error(`Message failed: ${action}`, err);
      return null;
    }
  }, []);
}
```

## Error Handling Patterns

### chrome.runtime.lastError

Always check `lastError` in callbacks:

```typescript
chrome.tabs.sendMessage(tabId, message, (response) => {
  if (chrome.runtime.lastError) {
    // Tab may not exist or content script not injected
    console.warn('Send failed:', chrome.runtime.lastError.message);
    return;
  }
  // Process response
});
```

### Port Reconnection

Handle port disconnection and reconnect:

```typescript
function createPersistentPort(name: string) {
  let port: chrome.runtime.Port | null = null;

  function connect() {
    port = chrome.runtime.connect({ name });
    port.onDisconnect.addListener(() => {
      port = null;
      // Reconnect after a short delay
      setTimeout(connect, 1000);
    });
    port.onMessage.addListener(handleMessage);
  }

  connect();

  return {
    send: (msg: unknown) => port?.postMessage(msg),
    disconnect: () => port?.disconnect(),
  };
}
```

## Content Script ↔ Host Page Communication

For cases where the content script must communicate with the host page's JavaScript:

```typescript
// Content script — listen for messages from page
window.addEventListener('message', (event) => {
  // Only accept messages from the same frame
  if (event.source !== window) return;
  // Only accept messages with our marker
  if (event.data?.type !== 'MY_EXTENSION_PAGE_MSG') return;

  // Forward to service worker
  chrome.runtime.sendMessage({
    action: 'pageData',
    payload: event.data.payload,
  });
});

// Host page (injected via world: 'MAIN' or web_accessible_resources)
window.postMessage({
  type: 'MY_EXTENSION_PAGE_MSG',
  payload: { data: 'from page' },
}, '*');
```

**Security:** Always validate the `type` field and sanitize `payload`. Never trust messages from the host page.

## Debugging Messages

Use Chrome DevTools to debug message passing:
- Service worker console: `chrome://extensions` → inspect views → service worker
- Content script console: Regular page DevTools console
- Popup console: Right-click popup → Inspect

Log all messages in development:
```typescript
if (process.env.NODE_ENV === 'development') {
  chrome.runtime.onMessage.addListener((msg, sender) => {
    console.log('[MSG]', msg.action, 'from', sender.url?.slice(0, 50));
  });
}
```
