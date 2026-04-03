---
name: chrome-ext-ui-react
description: >
  This skill should be used when building React UI for Chrome extensions or when the user asks
  about UI patterns in extensions. Trigger when: "React in extension", "extension popup React",
  "side panel React", "Shadow DOM React", "content script UI", "createShadowRootUi",
  "extension accessibility", "rem to px extension", "portal in extension", "React popup state",
  "extension UI patterns", "Radix in extension", "Shadcn extension", "extension keyboard
  navigation", "ARIA in extension", "focus management extension".
---

# React UI in Chrome Extensions

React works in extension popups, side panels, options pages, and content script injected UIs. Each context has unique constraints. The core challenges are: state dies with popup close, Shadow DOM is required for content script UI, and portaled components break in Shadow DOM.

## State Management Rule

Extension popups render from scratch on every toolbar click and die when they lose focus. Side panels persist longer but still need storage-backed state.

**Never rely on React `useState` alone for persistent data.** Always back state with `chrome.storage`:

```typescript
function useChromeState<T>(key: string, defaultValue: T) {
  const [value, setValue] = useState<T>(defaultValue);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    chrome.storage.local.get({ [key]: defaultValue }).then((result) => {
      setValue(result[key]);
      setLoading(false);
    });
    const listener = (changes: Record<string, chrome.storage.StorageChange>, area: string) => {
      if (area === 'local' && key in changes) setValue(changes[key].newValue);
    };
    chrome.storage.onChanged.addListener(listener);
    return () => chrome.storage.onChanged.removeListener(listener);
  }, [key]);

  const set = async (newValue: T) => {
    setValue(newValue);
    await chrome.storage.local.set({ [key]: newValue });
  };
  return [value, set, loading] as const;
}
```

## Shadow DOM for Content Script UI

Inject extension UI into web pages using Shadow DOM to prevent CSS pollution:

```typescript
export default defineContentScript({
  matches: ['<all_urls>'],
  cssInjectionMode: 'ui',
  main(ctx) {
    const ui = createShadowRootUi(ctx, {
      name: 'my-extension',
      position: 'inline',
      onMount(container) {
        const root = createRoot(container);
        root.render(<App />);
        return root;
      },
      onRemove(root) { root.unmount(); },
    });
    ui.mount();
  },
});
```

## Fix Portaled Components

React UI libraries (Radix UI, Headless UI, Shadcn) portal modals, dialogs, and tooltips to `document.body`. In content scripts, this forces them outside the Shadow DOM, stripping all styles. Configure the portal container:

```tsx
import { PortalProvider } from '@radix-ui/react-portal';

function App({ container }: { container: HTMLElement }) {
  return (
    <PortalProvider container={container}>
      <Dialog>{/* Portals inside Shadow DOM */}</Dialog>
    </PortalProvider>
  );
}
```

## Convert rem to px

React UI libraries use `rem` units that scale based on the host page's root font size. If a host page sets `font-size: 10px`, the extension UI appears broken. Convert at build time:

```typescript
// postcss.config.ts
import remToPx from '@thedutchcoder/postcss-rem-to-px';

export default {
  plugins: [remToPx({ baseValue: 16 })],
};
```

## When to Skip React

Use vanilla DOM code for "Integrated UIs" — small buttons, text highlights, minor visual tweaks:
- `document.createElement()` for simple elements
- `MutationObserver` for monitoring dynamic SPAs
- Native event listeners for interactions

React is best for complex dashboards, side panels, and feature-rich popups.

## Accessibility Essentials

- Toolbar action icon must include a `title` for screen readers
- Use `getByRole()` and `getByLabelText()` as selectors — stable on third-party pages
- Injected modals must implement focus trapping
- Restore focus to the previous element when closing injected UI
- Use `aria-live` regions for async state updates
- Icon-only buttons require `aria-label`
- Custom controls need `role`, `tabindex="0"`, and keyboard event handlers

## Common React Mistakes in Extensions

1. **Using Redux for global state** — duplicates memory per tab, serialization issues with ephemeral service workers
2. **Not dispatching events on host React forms** — programmatic `input.value` changes don't trigger React; dispatch an `input` event
3. **Async race conditions** — components unmount before background response arrives; use cleanup patterns
4. **Missing `useEffect` cleanup** — always remove `chrome.storage.onChanged` and `chrome.runtime.onMessage` listeners
5. **Throttle high-frequency events** — debounce before sending messages to service worker

## Additional Resources

### Reference Files

- **`references/react-extension-patterns.md`** — Advanced patterns: form autofill, MutationObserver, extension-specific hooks, and performance optimization
