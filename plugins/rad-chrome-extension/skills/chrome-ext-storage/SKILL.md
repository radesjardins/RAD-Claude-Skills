---
name: chrome-ext-storage
description: >
  This skill should be used when working with data storage in Chrome extensions or when the
  user asks about extension storage patterns. Trigger when: "chrome.storage", "extension
  storage", "storage.local", "storage.sync", "storage.session", "IndexedDB in extension",
  "extension data persistence", "write-through cache", "storage quota", "unlimitedStorage",
  "chrome.storage.onChanged", "reactive storage", "WXT storage", "storage.defineItem",
  "storage migration", "sync vs local storage".
---

# Chrome Extension Storage

Chrome extensions have four storage areas plus IndexedDB. Each serves a different purpose with different lifecycles, quotas, and trade-offs. Choose based on data size, persistence needs, and cross-device requirements.

## Storage Selection Guide

| Mechanism | Best For | Capacity | Lifecycle |
|-----------|----------|----------|-----------|
| `storage.session` | Hot state, temporary variables | 10 MB (in-memory) | Clears on browser close |
| `storage.local` | Device settings, cached data | 10 MB (expandable) | Persists until extension removed |
| `storage.sync` | User preferences across devices | 100 KB total | Syncs across Chrome instances |
| `storage.managed` | Enterprise-pushed config | Read-only | Set by IT admin policy |
| IndexedDB | Large datasets, binary data | ~80% disk | Persists until extension removed |

## When to Use What

**`storage.session`** — In-memory state that must be fast but doesn't need to survive browser restart. Service worker volatile cache. Authentication tokens for the current session.

**`storage.local`** — Default choice for most extension data. Settings, cached API responses, user data that stays on one device. Use `unlimitedStorage` permission to remove the 10 MB cap.

**`storage.sync`** — Small user preferences that should follow the user across devices. Subject to strict quotas: 8 KB per item, 512 items max, 1,800 writes/hour.

**IndexedDB** — Large datasets, binary data (images, model weights, video metadata), or data requiring structured queries. No JSON serialization overhead (uses structured cloning). Can use ~80% of available disk.

## Data That Must Never Be Stored

- **Passwords and credentials** in `storage.local` or `storage.sync` — these are NOT encrypted. Use `storage.session` for temporary auth tokens (clears on browser close).
- **Non-serializable objects** — `chrome.storage` only accepts JSON-serializable types. No `Date`, `Set`, `Map`, `RegExp`, or class instances.

## Write-Through Cache Pattern

For high-performance state management across service worker restarts:

```typescript
// Service worker — write-through cache
let cache: AppState | null = null;

async function getState(): Promise<AppState> {
  if (!cache) {
    const result = await chrome.storage.local.get('appState');
    cache = result.appState ?? DEFAULT_STATE;
  }
  return cache;
}

async function setState(update: Partial<AppState>) {
  cache = { ...(await getState()), ...update };
  await chrome.storage.local.set({ appState: cache });
  // onChanged listeners in popups/side panels auto-update
}
```

## Reactive Storage with WXT

WXT provides a reactive storage API with automatic change notifications:

```typescript
import { storage } from 'wxt/storage';

const userSettings = storage.defineItem<Settings>('local:settings', {
  defaultValue: { theme: 'light' },
});

// Read
const settings = await userSettings.getValue();

// Write
await userSettings.setValue({ theme: 'dark' });

// Watch for changes (works across all contexts)
userSettings.watch((newValue) => {
  updateUI(newValue);
});
```

## Quota Pitfalls

- **Sync throttling:** Exceeding 1,800 writes/hour silently fails. Batch updates.
- **Sync per-item limit:** Objects >8 KB fail. Shard large objects across keys.
- **Session volatility:** Lost on extension reload during development.
- **JSON serialization overhead:** Large objects in `chrome.storage` are slow. Use IndexedDB for large data.

## Additional Resources

### Reference Files

- **`references/storage-guide.md`** — Detailed storage patterns, IndexedDB usage, migration strategies, and React integration
