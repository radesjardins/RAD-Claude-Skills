# Content Security Policy Rules for MV3

## CSP Object Declaration

MV3 requires CSP as an object with distinct directives for different execution contexts:

```json
{
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'",
    "sandbox": "sandbox allow-scripts allow-forms; script-src 'self' 'unsafe-eval'"
  }
}
```

### extension_pages Directive

Applies to all standard extension pages (popup, side panel, options, background service worker).

**Allowed:**
- `'self'` — scripts bundled in the extension
- `'wasm-unsafe-eval'` or `'wasm-eval'` — for WebAssembly
- `'inline-speculation-rules'` — for speculation rules

**Banned:**
- `'unsafe-eval'` — no eval(), new Function(), setTimeout(string)
- `'unsafe-inline'` — no inline `<script>` tags, inline event handlers, `javascript:` URLs
- Remote domains — no `https://cdn.example.com` or any external domain
- `blob:` or `data:` for script sources

### sandbox Directive

Applies only to sandboxed extension pages. These pages:
- Have NO access to Chrome extension APIs (except `chrome.runtime` messaging)
- CAN use `'unsafe-eval'` if needed
- Are isolated from the rest of the extension
- Useful for running third-party code or user scripts safely

```json
{
  "sandbox": {
    "pages": ["sandbox.html"]
  },
  "content_security_policy": {
    "sandbox": "sandbox allow-scripts; script-src 'self' 'unsafe-eval'"
  }
}
```

## Content Script CSP

Content scripts are subject to the HOST PAGE's CSP, not the extension's. This means:

- If a host page restricts `connect-src`, content script `fetch()` calls to that domain will fail
- If a host page blocks `style-src 'unsafe-inline'`, dynamically injected styles may fail
- Content scripts cannot inject `<script>` tags into pages with strict CSP

**Workaround:** Proxy network requests through the service worker using message passing:

```typescript
// Content script
const response = await chrome.runtime.sendMessage({
  action: 'fetch',
  url: 'https://api.example.com/data',
});

// Service worker
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'fetch') {
    fetch(msg.url)
      .then(r => r.json())
      .then(data => sendResponse({ data }))
      .catch(err => sendResponse({ error: err.message }));
    return true; // keep channel open
  }
});
```

## WebAssembly CSP

To use WebAssembly in extension pages, add `'wasm-unsafe-eval'` to `script-src`:

```json
{
  "content_security_policy": {
    "extension_pages": "script-src 'self' 'wasm-unsafe-eval'; object-src 'self'"
  }
}
```

## Inline Script Alternatives

Since inline scripts are banned, use these alternatives:

| Banned Pattern | Alternative |
|----------------|-------------|
| `<script>code</script>` | External `<script src="script.js">` |
| `onclick="handler()"` | `element.addEventListener('click', handler)` |
| `javascript:void(0)` | `href="#"` with event listener |
| `<style>inline</style>` | External stylesheet or `CSSStyleSheet` API |

## CSP Violation Debugging

Monitor CSP violations during development:

```typescript
// In extension pages
document.addEventListener('securitypolicyviolation', (e) => {
  console.error('CSP violation:', {
    directive: e.violatedDirective,
    blockedURI: e.blockedURI,
    sourceFile: e.sourceFile,
    lineNumber: e.lineNumber,
  });
});
```

## web_accessible_resources CSP

Resources declared in `web_accessible_resources` are accessible from web pages but follow the extension's CSP. Configure carefully:

```json
{
  "web_accessible_resources": [{
    "resources": ["images/*", "styles/*"],
    "matches": ["https://example.com/*"]
  }]
}
```

- Limit `matches` to only the domains that need access
- Never expose sensitive scripts or HTML pages
- Each resource is accessible via `chrome-extension://<id>/path`
