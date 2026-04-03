---
name: chrome-ext-best-practices
description: >
  This skill should be used when working on any Chrome extension project or when the user asks
  about Chrome extension best practices, conventions, or patterns. Trigger when: setting up a
  new Chrome extension, configuring WXT, asking about MV3 architecture, "Chrome extension project
  structure", "WXT config", "extension entrypoints", "manifest v3 setup", "when to use content
  script vs service worker", "extension context boundaries", "Chrome extension build",
  "wxt.config.ts", "extension packaging", "Chrome Web Store submission", "cross-browser extension".
---

# Chrome Extension Best Practices

MV3 Chrome extensions operate across multiple isolated contexts with no shared memory. The architecture must respect these boundaries while maintaining clean code organization. WXT is the recommended framework — it provides file-based routing, automatic manifest generation, and Vite-powered builds.

## Core Mental Model

Every extension context (service worker, content script, popup, side panel) is a separate process. Communication happens exclusively through async message passing with JSON-serializable data. The service worker is ephemeral — it wakes to handle events and terminates after ~30 seconds of inactivity.

## WXT Project Structure

```
my-extension/
├── src/
│   ├── entrypoints/          # Isolated contexts (file-based routing)
│   │   ├── background.ts     # Service worker
│   │   ├── popup/            # Popup UI (index.html + App.tsx)
│   │   ├── sidepanel/        # Side panel UI
│   │   ├── options/          # Options page
│   │   └── content.ts        # Content script (or *.content.ts)
│   ├── components/           # Shared React components
│   ├── hooks/                # Custom React hooks
│   ├── utils/                # Shared utilities
│   │   ├── messaging.ts      # Protocol Map definitions
│   │   └── storage.ts        # Storage wrappers
│   └── assets/               # CSS, images, SVGs
├── public/                   # Static files (copied to output)
├── wxt.config.ts             # WXT configuration
├── tsconfig.json
└── package.json
```

Enable `srcDir: 'src'` in `wxt.config.ts` to keep configuration files at root and source in `src/`.

## Context Selection Guide

| Context | When to Use | Lifecycle | DOM Access | Chrome APIs |
|---------|------------|-----------|------------|-------------|
| Service Worker | Event handling, orchestration, network interception, alarms | Ephemeral (~30s idle) | None | All |
| Content Script | Read/modify web pages, inject UI | Tied to web page | Host page DOM | Limited |
| Popup | Quick interactions, toggles, settings | Transient (dies on blur) | Own document | All |
| Side Panel | Persistent tools, multi-step flows | Persists until closed | Own document | All |
| Offscreen Document | DOM tasks from background (DOMParser, clipboard, audio) | Reason-based | Own document | `chrome.runtime` only |
| Options Page | Extension settings dashboard | Standard page | Own document | All |

## Shared vs. Context-Specific Code

**Shared utilities** (in `src/utils/` or `src/shared/`) — only code used by 2+ contexts:
- TypeScript Protocol Maps for type-safe messaging
- Storage wrappers with reactive subscription
- Data schemas, Zod validators, API types

**Context-specific code** stays in its `entrypoints/` file:
- Service worker: event listeners, alarms, orchestration logic
- Content scripts: DOM manipulation, UI injection
- Popups/side panels: React components, UI state

## Organization Principles

- Small extensions: organize by file type (all components together)
- Large extensions: organize by feature (group components, hooks, logic by domain)
- Separate business logic from presentational components
- Extension APIs (`browser.*`/`chrome.*`) must be called inside entrypoint `main` functions, not at module scope

## WXT Entrypoints System

WXT uses file-based routing. The filename determines the entrypoint type:
- `background.ts` → service worker
- `popup/index.html` → popup UI
- `*.content.ts` → content scripts with inline metadata via `defineContentScript()`
- HTML entrypoints use `<meta>` tags for manifest properties

WXT automatically generates `manifest.json` from the directory structure and inline configurations. No manual manifest needed.

## Build and Packaging

- `wxt` — starts dev server with HMR
- `wxt build` — production build with tree-shaking and minification
- `wxt zip` — creates packaged ZIP for store submission
- `wxt build -b firefox` — cross-browser targeting

Review bundles for code splitting efficiency. WXT/Vite shares large dependencies (React, Tailwind) across entrypoints. Test packed `.zip` locally before submission — unpacked and packed extensions behave differently.

## Additional Resources

### Reference Files

- **`references/wxt-project-structure.md`** — Detailed WXT configuration, entrypoint metadata, manifest generation, and build pipeline
- **`references/context-boundaries.md`** — Deep dive into each extension context's lifecycle, capabilities, and communication patterns
