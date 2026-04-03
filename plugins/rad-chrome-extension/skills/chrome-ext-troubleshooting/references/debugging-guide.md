# Extension Debugging Guide

## Chrome DevTools for Extensions

### Service Worker Console
1. Navigate to `chrome://extensions`
2. Find your extension
3. Click "Inspect views: service worker"
4. Console shows service worker logs, errors, and network activity

### Content Script Console
Open the regular page DevTools (F12). Content script logs appear in the Console tab. Filter by your extension's file names.

### Popup/Side Panel Console
Right-click the popup or side panel → Inspect. Opens DevTools for that specific context.

### Force Service Worker Termination
1. Navigate to `chrome://serviceworker-internals`
2. Find your extension's worker
3. Click "Stop"
4. Verify your extension recovers correctly when the next event fires

## Common Error Messages

### "Could not establish connection. Receiving end does not exist."
**Cause:** Message sent to a context that doesn't exist (tab closed, service worker not running, content script not injected).
**Fix:**
- Wrap `sendMessage` in try/catch
- Check `chrome.runtime.lastError` in callbacks
- Implement retry logic for service worker wake-up

```typescript
try {
  const response = await chrome.runtime.sendMessage(msg);
} catch (err) {
  if (err.message.includes('Receiving end does not exist')) {
    // Service worker not ready or tab closed
    await new Promise(r => setTimeout(r, 100));
    // Retry once
  }
}
```

### "The message port closed before a response was received."
**Cause:** `onMessage` listener did not return `true` for async response.
**Fix:** Return `true` from the listener when using `sendResponse` asynchronously:

```typescript
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'fetchData') {
    fetchData().then(sendResponse); // async
    return true; // MUST return true
  }
});
```

### "Cannot access contents of url. Extension manifest must request permission."
**Cause:** Content script or `chrome.tabs.executeScript` targeting a URL not covered by permissions.
**Fix:** Add the URL pattern to `host_permissions` or use `activeTab` with user gesture.

### "Refused to execute inline script because it violates CSP"
**Cause:** Inline `<script>` tag or inline event handler in extension HTML.
**Fix:** Move all JavaScript to external `.js` files. Replace `onclick="handler()"` with `addEventListener`.

### "Service worker registration failed."
**Cause:** Syntax error in background script, or background script path wrong in manifest.
**Fix:** Check the service worker source for syntax errors. Verify the path matches exactly.

### "Uncaught (in promise) Error: Extension context invalidated."
**Cause:** Extension was updated/reloaded while content script was running.
**Fix:** Detect invalidation and clean up:

```typescript
function isExtensionValid() {
  try {
    chrome.runtime.getURL('');
    return true;
  } catch {
    return false;
  }
}

// Check before sending messages
if (isExtensionValid()) {
  chrome.runtime.sendMessage(msg);
}
```

## Debugging Storage Issues

### Inspect Storage Contents
```typescript
// In any extension context's console
chrome.storage.local.get(null, (items) => console.log('local:', items));
chrome.storage.sync.get(null, (items) => console.log('sync:', items));
chrome.storage.session.get(null, (items) => console.log('session:', items));
```

### Monitor Storage Changes
```typescript
chrome.storage.onChanged.addListener((changes, area) => {
  for (const [key, { oldValue, newValue }] of Object.entries(changes)) {
    console.log(`[${area}] ${key}:`, oldValue, '→', newValue);
  }
});
```

### Check Storage Quota
```typescript
chrome.storage.local.getBytesInUse(null, (bytes) => {
  console.log(`Local storage: ${(bytes / 1024).toFixed(1)} KB`);
});

chrome.storage.sync.getBytesInUse(null, (bytes) => {
  console.log(`Sync storage: ${(bytes / 1024).toFixed(1)} KB / 100 KB`);
});
```

## Debugging Messaging

### Log All Messages (Development Only)
```typescript
// Service worker
chrome.runtime.onMessage.addListener((msg, sender) => {
  console.log('[MSG IN]', {
    action: msg.action,
    from: sender.tab?.url?.slice(0, 50) ?? sender.url ?? 'unknown',
    frameId: sender.frameId,
  });
});
```

### Verify Content Script Injection
```typescript
// In page console
chrome.runtime.sendMessage(
  '<your-extension-id>',
  { action: 'ping' },
  (response) => {
    if (chrome.runtime.lastError) {
      console.error('Content script not injected:', chrome.runtime.lastError);
    } else {
      console.log('Content script responds:', response);
    }
  }
);
```

## Network Request Debugging

### Monitor Extension Network Activity
Open DevTools for the service worker and switch to the Network tab. All `fetch()` calls from the service worker appear here.

### Debug Content Script Fetch Failures
If content script `fetch()` fails due to host page CSP:
1. Open host page DevTools → Console
2. Look for "Refused to connect" CSP violation messages
3. Solution: Proxy requests through the service worker via messaging

## Performance Debugging

### Bundle Size Analysis
```bash
# WXT provides built-in bundle analysis
wxt build --analyze
```

### Memory Profiling
In the service worker DevTools, use the Memory tab to take heap snapshots. Watch for:
- Growing memory across events (potential leak)
- Large objects retained after they should be garbage collected
- Listeners accumulating without cleanup

### Extension Performance Impact
Use Chrome's Task Manager (Shift+Esc) to monitor:
- Extension's CPU usage
- Memory consumption per context
- Network activity
