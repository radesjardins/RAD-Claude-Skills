# rad-chrome-extension — Build production-ready Chrome MV3 extensions. Security, messaging, storage, and Chrome Web Store compliance handled.

Chrome's Manifest V3 changed how extensions are built — service workers instead of background pages, stricter CSP, new permission patterns. rad-chrome-extension keeps Claude aligned with MV3 conventions and the WXT framework, with security and Chrome Web Store compliance built into every component it helps you write.

## What You Can Do With This

- Build an extension popup, content script, or service worker with correct MV3 patterns
- Set up messaging between your background service worker, content scripts, and popup — without the common race conditions
- Request only the permissions you actually need (and understand why the Store rejects over-permissioned extensions)
- Review an extension for security issues before submitting to the Chrome Web Store

## How It Works

| Skill | Purpose |
|-------|---------|
| `chrome-ext-best-practices` | MV3 conventions, WXT framework, project structure |
| `chrome-ext-service-worker` | Service worker lifecycle, persistence patterns, background tasks |
| `chrome-ext-messaging` | Inter-component messaging, ports, connection patterns |
| `chrome-ext-storage` | chrome.storage.local/sync, data patterns, migration |
| `chrome-ext-permissions` | Permission minimization, optional permissions, CWS compliance |
| `chrome-ext-security` | CSP, eval usage, content script trust boundaries, XSS prevention |
| `chrome-ext-ui-react` | React UI in popups and side panels, WXT + React patterns |
| `chrome-ext-testing` | Unit tests, integration tests for extension components |
| `chrome-ext-troubleshooting` | CWS rejections, service worker issues, messaging bugs |

| Agent | Purpose |
|-------|---------|
| `chrome-ext-reviewer` | Reviews extension code for security, messaging patterns, permission over-requesting, and CWS compliance |

## Quick Start

```bash
claude plugins add ./RAD-Claude-Skills/plugins/rad-chrome-extension
```

```
Review my Chrome extension
Is my extension ready for the Chrome Web Store?
Check my extension for security issues
```

## License
Apache-2.0
