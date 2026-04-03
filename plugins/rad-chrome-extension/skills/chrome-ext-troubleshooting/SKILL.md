---
name: chrome-ext-troubleshooting
description: >
  This skill should be used when debugging Chrome extension issues, diagnosing Chrome Web Store
  rejections, or troubleshooting build problems. Trigger when: "extension not working", "CWS
  rejection", "Chrome Web Store rejected", "Yellow Magnesium", "Purple Potassium", "Blue Argon",
  "Red Magnesium", "extension build error", "manifest error", "extension debugging", "service
  worker not waking", "content script not injecting", "message not received", "extension
  permissions error", "pre-release checklist", "extension review".
---

# Chrome Extension Troubleshooting

Common problems fall into three categories: build/packaging issues, runtime bugs, and Chrome Web Store rejections. Most have straightforward diagnoses once the pattern is recognized.

## Build-Time Mistakes

### Case-Sensitive File Paths
Windows is case-insensitive; CWS reviewer runs on Linux (case-sensitive). `Background.js` works locally but fails on submission (Yellow Magnesium rejection).

**Fix:** Verify all file paths match exactly, including capitalization. Test on a case-sensitive filesystem or review the packed `.zip` contents.

### Missing web_accessible_resources
Content scripts cannot load extension assets (images, fonts, CSS) without declaring them:

```json
{
  "web_accessible_resources": [{
    "resources": ["images/*", "fonts/*"],
    "matches": ["<all_urls>"]
  }]
}
```

### Indirect eval() from npm Packages
Third-party libraries may internally use `eval()`, violating MV3 CSP. Audit dependencies:

```bash
# Search for eval in bundled output
grep -r "eval(" .output/chrome-mv3/
grep -r "new Function(" .output/chrome-mv3/
```

**Fix:** Replace the library, isolate in a sandbox page, or find an alternative.

### Accidental Secrets in Source ZIP
Firefox requires a sources `.zip` that can rebuild the extension. `.env` files or secrets may leak:

**Fix:** Add `.env*`, `*.pem`, and credentials to `.gitignore` and verify they're excluded from the ZIP.

## Runtime Debugging

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Event not firing after restart | Listener inside async function | Move to top level, register synchronously |
| State lost between events | Global variables in service worker | Use `chrome.storage` |
| Timer not executing | `setTimeout` in service worker | Replace with `chrome.alarms` |
| Message response is `null` | Missing `return true` in async listener | Add `return true` |
| Content script not injecting | Missing `matches` or permissions | Check manifest and host permissions |
| Fetch failing in service worker | Using `XMLHttpRequest` | Replace with `fetch()` |
| Storage writes silently failing | Sync quota exceeded | Check quotas, batch writes |
| Popup state disappears | Relying on React state only | Back with `chrome.storage` |

## CWS Rejection Quick Reference

| Code | Name | Common Cause | Quick Fix |
|------|------|-------------|-----------|
| Blue Argon | Remote Code | `eval()`, CDN scripts, dynamic imports | Bundle all deps locally |
| Yellow Magnesium | Packaging | Wrong file paths, missing files | Test packed `.zip` on Linux |
| Yellow Zinc | Metadata | Bad description, missing icons | Provide all required assets |
| Purple Potassium | Excessive Permissions | Over-requesting permissions | Audit with `activeTab`, optional perms |
| Purple Lithium | Privacy | Missing privacy policy | Add accessible privacy policy URL |
| Purple Copper | Data Security | HTTP, data in URL params | Use HTTPS everywhere |
| Red Family | Single Purpose | Bundled unrelated features | Split into separate extensions |
| Red Titanium | Obfuscation | Non-standard minification | Use standard minifiers only |
| Grey Titanium | Affiliates | Hidden affiliate injection | Disclose and require user action |

## Pre-Release Checklist

Before every Chrome Web Store submission:

### Permissions
- [ ] Every declared permission backed by code
- [ ] No overly broad permissions (`<all_urls>` audit)
- [ ] Non-core permissions moved to `optional_permissions`
- [ ] Cause-and-effect justification for each permission in privacy tab

### Security
- [ ] No `eval()`, `new Function()`, `setTimeout(string)` in codebase or dependencies
- [ ] No remote code loading (CDN scripts, dynamic imports from URLs)
- [ ] All data transmission over HTTPS
- [ ] Content script messages validated in service worker
- [ ] No sensitive data in URL parameters or headers

### Packaging
- [ ] Packed `.zip` tested locally (not just unpacked)
- [ ] File paths case-correct for Linux
- [ ] All declared resources exist
- [ ] No `.env` or credentials in package
- [ ] Icons provided: 16, 32, 48, 128px
- [ ] Screenshots match current UI

### Functionality
- [ ] Extension works on clean Chrome profile
- [ ] Service worker recovers from termination
- [ ] Popup/side panel state persists via storage
- [ ] Content script works on target pages
- [ ] Onboarding page opens on first install

### Metadata
- [ ] Description accurately reflects ALL features
- [ ] No keyword stuffing
- [ ] Privacy policy URL accessible and accurate
- [ ] Category matches functionality

## Additional Resources

### Reference Files

- **`references/debugging-guide.md`** — Advanced debugging techniques, Chrome DevTools for extensions, and common error messages
