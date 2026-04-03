# Detailed Storage Patterns

## chrome.storage API Usage

### Basic Operations

```typescript
// Write
await chrome.storage.local.set({ key: 'value', count: 42 });

// Read
const { key, count } = await chrome.storage.local.get(['key', 'count']);

// Read with defaults
const { theme } = await chrome.storage.local.get({ theme: 'light' });

// Remove
await chrome.storage.local.remove('key');

// Clear all
await chrome.storage.local.clear();
```

### Listening for Changes

```typescript
// Fires when any storage area changes — works in ALL contexts
chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName !== 'local') return;

  for (const [key, { oldValue, newValue }] of Object.entries(changes)) {
    console.log(`${key}: ${oldValue} → ${newValue}`);
  }
});
```

## React Integration

### Custom Storage Hook

```typescript
// src/hooks/useStorage.ts
import { useState, useEffect } from 'react';

export function useStorage<T>(key: string, defaultValue: T) {
  const [value, setValue] = useState<T>(defaultValue);
  const [loading, setLoading] = useState(true);

  // Load initial value
  useEffect(() => {
    chrome.storage.local.get({ [key]: defaultValue }).then((result) => {
      setValue(result[key]);
      setLoading(false);
    });
  }, [key, defaultValue]);

  // Listen for external changes
  useEffect(() => {
    const listener = (
      changes: Record<string, chrome.storage.StorageChange>,
      area: string,
    ) => {
      if (area === 'local' && key in changes) {
        setValue(changes[key].newValue);
      }
    };
    chrome.storage.onChanged.addListener(listener);
    return () => chrome.storage.onChanged.removeListener(listener);
  }, [key]);

  // Setter that persists
  const setStoredValue = async (newValue: T | ((prev: T) => T)) => {
    const resolved = typeof newValue === 'function'
      ? (newValue as (prev: T) => T)(value)
      : newValue;
    setValue(resolved);
    await chrome.storage.local.set({ [key]: resolved });
  };

  return [value, setStoredValue, loading] as const;
}
```

### WXT Reactive Storage in React

```typescript
// Using WXT storage with React
import { storage } from 'wxt/storage';

const theme = storage.defineItem<'light' | 'dark'>('local:theme', {
  defaultValue: 'light',
});

function ThemePicker() {
  const [currentTheme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    theme.getValue().then(setTheme);
    const unwatch = theme.watch(setTheme);
    return unwatch;
  }, []);

  return (
    <button onClick={() => theme.setValue(currentTheme === 'light' ? 'dark' : 'light')}>
      Toggle: {currentTheme}
    </button>
  );
}
```

## IndexedDB in Extensions

### When to Use IndexedDB

- Data exceeds 10 MB (even with `unlimitedStorage`, chrome.storage is slow for large data)
- Binary data (images, audio, model weights, video frames)
- Need structured queries (indexes, ranges)
- Performance-critical read/write operations

### Basic IndexedDB Pattern

```typescript
function openDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('ExtensionDB', 1);

    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains('data')) {
        db.createObjectStore('data', { keyPath: 'id' });
      }
    };

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

async function saveItem(item: { id: string; [key: string]: unknown }) {
  const db = await openDB();
  return new Promise<void>((resolve, reject) => {
    const tx = db.transaction('data', 'readwrite');
    tx.objectStore('data').put(item);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

async function getItem<T>(id: string): Promise<T | undefined> {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('data', 'readonly');
    const request = tx.objectStore('data').get(id);
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}
```

### IndexedDB in Service Workers

IndexedDB is available in service workers. Use it for large data that must persist across service worker restarts:

```typescript
// Service worker — store large data in IndexedDB
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'saveLargeData') {
    saveItem(msg.data).then(() => sendResponse({ success: true }));
    return true;
  }
});
```

## Storage Migration Strategies

### WXT Versioned Migrations

```typescript
const settings = storage.defineItem<Settings>('local:settings', {
  defaultValue: { theme: 'light', fontSize: 14, language: 'en' },
  version: 3,
  migrations: {
    2: (old: any) => ({ ...old, fontSize: old.fontSize ?? 14 }),
    3: (old: any) => ({ ...old, language: old.language ?? 'en' }),
  },
});
```

### Manual Migration on Install

```typescript
// Service worker
chrome.runtime.onInstalled.addListener(async (details) => {
  if (details.reason === 'update') {
    const { version } = await chrome.storage.local.get('version');
    if (!version || version < 2) {
      // Migrate from v1 to v2
      const { oldKey } = await chrome.storage.local.get('oldKey');
      if (oldKey) {
        await chrome.storage.local.set({ newKey: transformData(oldKey) });
        await chrome.storage.local.remove('oldKey');
      }
    }
    await chrome.storage.local.set({ version: 2 });
  }
});
```

## Quota Reference

| Area | Total | Per Item | Max Items | Write Limits |
|------|-------|----------|-----------|--------------|
| local | 10 MB (expandable) | No limit | Unlimited | None |
| session | 10 MB | No limit | Unlimited | None |
| sync | 100 KB | 8 KB | 512 | 1,800/hr, 120/min |
| managed | Read-only | N/A | N/A | Admin-set |

To expand local storage:
```json
{
  "permissions": ["unlimitedStorage"]
}
```

**Note:** Even with `unlimitedStorage`, prefer IndexedDB for data >10 MB due to JSON serialization overhead.
