# Permission-by-Permission Guide

## Common Permissions and When They're Needed

### activeTab
**Provides:** Temporary host permission for the currently active tab after user invokes extension.
**Required when:** Extension needs to read or modify the current page on user action (click toolbar icon, keyboard shortcut, context menu).
**Not required when:** Extension needs persistent background access to pages.
**Install warning:** None.

### tabs
**Provides:** Access to sensitive `Tab` properties: `url`, `pendingUrl`, `title`, `favIconUrl`.
**Required when:** Extension must read URLs or titles of tabs without having host permission for those sites.
**Not required when:** Using most `chrome.tabs` methods (query, create, update, remove) — these work without the permission.
**Install warning:** None.
**Note:** If you have host permissions for a site, you automatically get access to these properties for matching tabs.

### storage
**Provides:** Access to `chrome.storage` API (local, sync, session, managed).
**Required when:** Using `chrome.storage.local.get/set`, `chrome.storage.sync.get/set`, etc.
**Not required when:** Using web APIs like `localStorage`, `sessionStorage`, or IndexedDB.
**Install warning:** None.

### cookies
**Provides:** Access to `chrome.cookies` API for querying, setting, and observing cookies.
**Required when:** Need to read/write cookies from background context, access `SameSite` values, or monitor cookie changes.
**Not required when:** Only using `document.cookie` in content scripts or extension pages.
**Install warning:** None (but may require host permissions for specific domains).

### alarms
**Provides:** Access to `chrome.alarms` API for scheduling periodic or delayed tasks.
**Required when:** Any scheduled or periodic task in the service worker (replaces setTimeout/setInterval).
**Install warning:** None.

### offscreen
**Provides:** Access to `chrome.offscreen` API for creating offscreen documents.
**Required when:** Service worker needs DOM operations (parsing HTML, clipboard, audio).
**Install warning:** None.

### sidePanel
**Provides:** Access to `chrome.sidePanel` API.
**Required when:** Extension uses a side panel.
**Install warning:** None.

### declarativeNetRequest
**Provides:** Network request interception and modification via declarative rules.
**Required when:** Blocking or redirecting network requests (ad blocking, privacy protection).
**Install warning:** "Block page content" (less alarming than old webRequest).
**Note:** Use `declarativeNetRequestWithHostAccess` for dynamic rules targeting specific hosts.

### scripting
**Provides:** Programmatic script injection via `chrome.scripting.executeScript`.
**Required when:** Dynamically injecting content scripts (not declared in manifest).
**Install warning:** Depends on host permissions.

### contextMenus
**Provides:** Add items to Chrome's right-click context menu.
**Required when:** Extension adds custom context menu entries.
**Install warning:** None.

### notifications
**Provides:** Create desktop notifications via `chrome.notifications` API.
**Required when:** Extension shows OS-level notifications.
**Install warning:** None.

### bookmarks
**Provides:** Access to bookmark tree via `chrome.bookmarks` API.
**Required when:** Reading, creating, or modifying bookmarks.
**Install warning:** "Read and change your bookmarks."

### history
**Provides:** Access to browsing history via `chrome.history` API.
**Required when:** Querying or modifying browser history.
**Install warning:** "Read your browsing history."

### downloads
**Provides:** Manage downloads via `chrome.downloads` API.
**Required when:** Initiating, pausing, or monitoring downloads.
**Install warning:** "Manage your downloads."

## Permission Narrowing Strategies

### Strategy 1: Replace tabs with activeTab
If you only need the current tab's URL after user action, `activeTab` is sufficient:

```diff
- "permissions": ["tabs"]
+ "permissions": ["activeTab"]
```

### Strategy 2: Replace <all_urls> with specific hosts
If your extension only interacts with specific sites:

```diff
- "host_permissions": ["<all_urls>"]
+ "host_permissions": ["https://api.example.com/*", "https://docs.example.com/*"]
```

### Strategy 3: Move to optional
Non-core features should request at runtime:

```diff
- "permissions": ["bookmarks", "history"]
+ "permissions": [],
+ "optional_permissions": ["bookmarks", "history"]
```

### Strategy 4: Replace webRequest with declarativeNetRequest
MV3 replaces the powerful `webRequest` API with the declarative alternative:

```diff
- "permissions": ["webRequest", "webRequestBlocking"]
+ "permissions": ["declarativeNetRequest"]
```

### Strategy 5: Use content_scripts instead of scripting
If scripts are always injected on the same pages, declare them statically:

```diff
- "permissions": ["scripting"],
- "host_permissions": ["https://example.com/*"]
+ "content_scripts": [{
+   "matches": ["https://example.com/*"],
+   "js": ["content.js"]
+ }]
```

## Permission Audit Checklist

1. For each permission in manifest:
   - [ ] Grep codebase for corresponding `chrome.*` API calls
   - [ ] Verify at least one code path uses this permission
   - [ ] Check if a narrower alternative exists
2. For each host permission:
   - [ ] Verify the extension actually makes requests to this host
   - [ ] Check if `activeTab` could replace it
   - [ ] Consider moving to `optional_host_permissions`
3. For the install warning:
   - [ ] Test packed `.crx` to see exact warning text
   - [ ] Prepare justification for each warning-triggering permission
   - [ ] Record video demonstrating permission usage
