# Extension Context Boundaries

## Service Worker (Background)

**Lifecycle:** Ephemeral, event-driven. Wakes to process events, auto-terminates after ~30 seconds of inactivity. All in-memory state and global variables lost on termination.

**Capabilities:**
- All Chrome extension APIs
- Network requests via `fetch()` (NOT `XMLHttpRequest`)
- No DOM access, no `window` object
- Cannot use `setTimeout`/`setInterval` reliably (use `chrome.alarms`)

**Responsibilities:**
- Central event handling and orchestration
- Alarm scheduling and periodic tasks
- Network request interception (Declarative Net Request)
- Cross-context message routing
- State persistence coordination

**Key rules:**
- Register ALL event listeners synchronously at the top level
- Never store state in global variables — use `chrome.storage`
- Use `chrome.alarms` instead of `setTimeout`/`setInterval`
- Use `chrome.offscreen` for DOM-dependent tasks

## Content Scripts

**Lifecycle:** Tied to the web page they are injected into. Destroyed when page navigates or closes.

**Capabilities:**
- Full DOM access to host page
- Isolated World — cannot see host page's JS variables/functions
- Limited Chrome API access (`chrome.runtime`, `chrome.storage`, `chrome.i18n`)
- Subject to host page's CSP for `fetch()` requests

**Responsibilities:**
- Reading and modifying web page content
- Injecting extension UI into pages
- Scraping page data
- Forwarding page events to service worker

**Key rules:**
- Treat as UNTRUSTED — runs alongside potentially malicious page code
- Use Shadow DOM (`createShadowRootUi`) for injected UI to prevent CSS pollution
- Proxy network requests through service worker to bypass host CSP
- Never expose secrets or sensitive extension state to content scripts
- Use `document.createElement` and `textContent` (never `innerHTML` with untrusted data)

## Popups

**Lifecycle:** Highly transient. Renders from scratch on toolbar icon click. Completely destroyed (all state lost) when it loses focus — clicking anywhere outside kills it.

**Capabilities:**
- Standard HTML/JS with full Chrome API access
- Own isolated document context
- Cannot touch webpage DOM (must message content scripts)

**Responsibilities:**
- Quick user interactions (toggles, settings, quick data entry)
- Displaying status information
- Triggering background operations

**Key rules:**
- Never store state in React `useState` alone — it dies on every close
- Persist all state to `chrome.storage` and rehydrate on open
- Keep interactions quick and focused — popups should not host complex workflows

## Side Panels

**Lifecycle:** Persistent — remains open across tab navigation. Does NOT close when user clicks elsewhere. Stays open until manually closed.

**Capabilities:**
- Full extension page with all Chrome APIs
- Own isolated document context
- Can be tab-specific or global

**Responsibilities:**
- Complex, persistent tools (AI assistants, reading tools, multi-step forms)
- Long-running interactions that should survive tab switches
- Persistent dashboards and monitors

**Key rules:**
- Good choice for complex UI that would be annoying as a popup
- Still requires message passing to communicate with content scripts
- Clean up listeners and ports when panel closes

## Offscreen Documents

**Lifecycle:** Created programmatically via `chrome.offscreen.createDocument()`. Lifespan depends on the declared `Reason`:
- `AUDIO_PLAYBACK` — auto-closes after 30s of silence
- `CLIPBOARD`, `DOM_PARSER` — stays open until explicitly closed

**Capabilities:**
- Full DOM access (hidden HTML page)
- Only `chrome.runtime` for message passing
- No other Chrome extension APIs

**Responsibilities:**
- Tasks requiring DOM that service worker cannot do:
  - Parsing HTML with `DOMParser`
  - Clipboard operations
  - Audio/video playback
  - Canvas operations

**Key rules:**
- Delegate tasks via message passing from service worker
- Provide specific `Reason` when creating
- Close with `chrome.offscreen.closeDocument()` when done
- Only one offscreen document can exist at a time

## Extension Pages (Options, Override)

**Lifecycle:** Standard web page lifecycle. Opens in a tab or embedded panel.

**Capabilities:**
- Full DOM access
- Full Chrome API access
- Standard page navigation

**Responsibilities:**
- Extension configuration and settings
- Override pages (New Tab, History, Bookmarks)
- Complex dashboards requiring full-page layout

## Cross-Context Communication

All contexts are strictly siloed — no shared memory or objects. Communication via:

| From → To | Method |
|-----------|--------|
| Any → Service Worker | `chrome.runtime.sendMessage()` |
| Service Worker → Tab | `chrome.tabs.sendMessage(tabId, ...)` |
| Any ↔ Any (persistent) | `chrome.runtime.connect()` / `chrome.tabs.connect()` |
| Page → Content Script | `window.postMessage()` (use with caution) |

All cross-boundary data must be JSON-serializable. No functions, DOM nodes, or class instances.
