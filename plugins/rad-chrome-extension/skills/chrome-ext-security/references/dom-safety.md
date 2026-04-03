# DOM Safety and XSS Prevention

## Injection Sinks to Avoid

These DOM APIs interpret strings as HTML or code and are XSS vectors when used with untrusted input:

| Dangerous Sink | Safe Alternative |
|----------------|-----------------|
| `element.innerHTML = data` | `element.textContent = data` |
| `document.write(data)` | `document.createElement()` + append |
| `element.insertAdjacentHTML()` | Build DOM nodes programmatically |
| `eval(data)` | Parse JSON with `JSON.parse()` |
| `new Function(data)` | Use static function references |
| `setTimeout(string)` | `setTimeout(function)` |

## Trusted Types API

Enforce sanitization at the browser level by requiring all injection sink inputs to pass through a policy:

```typescript
// Create a Trusted Types policy
const policy = trustedTypes.createPolicy('extension-policy', {
  createHTML: (input: string) => DOMPurify.sanitize(input),
  createScriptURL: (input: string) => {
    if (input.startsWith(chrome.runtime.getURL(''))) return input;
    throw new Error('Blocked untrusted script URL');
  },
});

// Usage — passes through sanitization automatically
element.innerHTML = policy.createHTML(untrustedData);
```

Enable Trusted Types enforcement in CSP:

```
script-src 'self'; require-trusted-types-for 'script'
```

## Shadow DOM for UI Isolation

When injecting extension UI into web pages, use Shadow DOM to prevent CSS pollution:

```typescript
// WXT pattern
export default defineContentScript({
  matches: ['<all_urls>'],
  cssInjectionMode: 'ui',
  main(ctx) {
    createShadowRootUi(ctx, {
      name: 'my-extension',
      position: 'inline',
      onMount(container) {
        const root = createRoot(container);
        root.render(<App />);
        return root;
      },
      onRemove(root) {
        root.unmount();
      },
    });
  },
});
```

Shadow DOM benefits:
- Host page CSS cannot affect extension UI
- Extension CSS cannot leak into host page
- Events can be isolated from host page
- Prevents class name collisions

## Safe DOM Construction

Build DOM elements programmatically instead of string concatenation:

```typescript
// DANGEROUS — XSS if title contains HTML
container.innerHTML = `<h1>${item.title}</h1><p>${item.description}</p>`;

// SAFE — programmatic construction
const h1 = document.createElement('h1');
h1.textContent = item.title;
const p = document.createElement('p');
p.textContent = item.description;
container.append(h1, p);
```

## Message Input Validation

Validate all data received via message passing before using it in DOM operations:

```typescript
// Service worker — validate before processing
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // Verify sender is our extension
  if (sender.id !== chrome.runtime.id) return;

  // Validate message structure
  if (typeof message !== 'object' || !message.action) return;

  // Type-check specific fields
  if (message.action === 'updateTitle' && typeof message.title === 'string') {
    // Safe to process
  }
});
```

## Content Script DOM Reading Safety

When reading data from the host page DOM, sanitize before sending to service worker:

```typescript
// Content script — sanitize scraped data
const title = document.querySelector('h1')?.textContent?.trim() ?? '';
const url = window.location.href;

// Validate URL before sending
try {
  new URL(url); // throws if malformed
  chrome.runtime.sendMessage({ action: 'pageData', title, url });
} catch {
  console.error('Invalid URL detected');
}
```

## React-Specific DOM Safety

In React extension UIs:
- Never use `dangerouslySetInnerHTML` with untrusted data
- If required, always sanitize with DOMPurify first
- Use `textContent` via refs instead of `innerHTML`
- Validate all props that come from message passing or storage
