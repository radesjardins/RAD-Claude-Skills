# WXT Project Structure and Configuration

## wxt.config.ts

Primary configuration file for WXT projects:

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  srcDir: 'src',
  modules: ['@wxt-dev/module-react'],
  manifest: {
    name: 'My Extension',
    permissions: ['storage', 'activeTab'],
    // WXT merges this with auto-generated manifest
  },
  runner: {
    startUrls: ['https://example.com'],
    // Opens URL when starting dev server
  },
});
```

## Entrypoint Types and Metadata

### Service Worker (background.ts)

```typescript
// src/entrypoints/background.ts
export default defineBackground(() => {
  // All listeners MUST be registered synchronously here
  chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    // handle message
    return true; // keep channel open for async
  });

  chrome.alarms.onAlarm.addListener((alarm) => {
    // handle alarm
  });
});
```

### Content Scripts (*.content.ts)

```typescript
// src/entrypoints/content.ts
export default defineContentScript({
  matches: ['https://example.com/*'],
  runAt: 'document_idle',
  main() {
    // DOM access available here
  },
});
```

Content scripts with UI injection:

```typescript
export default defineContentScript({
  matches: ['<all_urls>'],
  cssInjectionMode: 'ui',
  main(ctx) {
    const ui = createShadowRootUi(ctx, {
      name: 'my-extension-ui',
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
    ui.mount();
  },
});
```

### HTML Entrypoints (popup, sidepanel, options)

```
src/entrypoints/popup/
├── index.html    # Entry HTML file
├── App.tsx       # React root component
└── main.tsx      # React mount point
```

HTML entrypoints use `<meta>` tags for manifest properties:

```html
<!-- popup/index.html -->
<!DOCTYPE html>
<html>
<head>
  <meta name="manifest.default_popup" content="popup.html" />
  <script type="module" src="./main.tsx"></script>
</head>
<body>
  <div id="root"></div>
</body>
</html>
```

## Manifest Generation

WXT automatically generates `manifest.json` from:
1. Directory structure (entrypoint files)
2. Inline metadata (`defineContentScript()`, `defineBackground()`)
3. HTML `<meta>` tags
4. `wxt.config.ts` manifest overrides

The generated manifest lives in `.output/chrome-mv3/manifest.json` (or equivalent for target browser).

## Build Pipeline

### Development
```bash
wxt           # Start dev server with HMR
wxt -b firefox  # Target Firefox
```

### Production
```bash
wxt build       # Build for Chrome
wxt build -b firefox  # Build for Firefox
wxt zip         # Build + package as ZIP
wxt zip -b firefox    # ZIP for Firefox (includes sources ZIP)
```

### Build Output
```
.output/
├── chrome-mv3/        # Chrome build
│   ├── manifest.json  # Auto-generated
│   ├── background.js  # Service worker
│   ├── popup.html     # Popup UI
│   ├── content-scripts/
│   └── chunks/        # Shared code
└── firefox-mv3/       # Firefox build (if targeted)
```

## Versioned Storage Migrations

WXT provides a versioned storage API for managing data migrations across extension updates:

```typescript
import { storage } from 'wxt/storage';

const userSettings = storage.defineItem<UserSettings>('local:settings', {
  defaultValue: { theme: 'light', fontSize: 14 },
  version: 2,
  migrations: {
    // Runs when upgrading from version 1 to 2
    2: (oldValue) => ({
      ...oldValue,
      fontSize: oldValue.fontSize ?? 14,
    }),
  },
});
```

## CI/CD and Automated Publishing

WXT supports automated publishing via `wxt submit` and GitHub Actions:

```yaml
# .github/workflows/publish.yml
- run: wxt zip
- run: wxt submit --chrome-zip .output/chrome-mv3.zip
  env:
    CHROME_EXTENSION_ID: ${{ secrets.CHROME_EXTENSION_ID }}
    CHROME_CLIENT_ID: ${{ secrets.CHROME_CLIENT_ID }}
    CHROME_CLIENT_SECRET: ${{ secrets.CHROME_CLIENT_SECRET }}
    CHROME_REFRESH_TOKEN: ${{ secrets.CHROME_REFRESH_TOKEN }}
```

## Auto-Imports

WXT provides auto-imports for common utilities:
- `browser` (from `webextension-polyfill`)
- `defineBackground`, `defineContentScript`, `defineUnlistedScript`
- `createShadowRootUi`, `createIntegratedUi`, `createContentScriptUi`
- `storage` (from `wxt/storage`)

Configure additional auto-imports in `wxt.config.ts`:

```typescript
export default defineConfig({
  imports: {
    addons: {
      vueTemplate: false,
    },
    presets: ['react'],
  },
});
```
