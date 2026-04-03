# React Extension Patterns

## Form Autofill in Host Page React SPAs

When an extension autofills forms on third-party React SPAs, simply mutating `input.value` fails because React tracks state internally. Dispatch a native event to trigger React's lifecycle:

```typescript
function setInputValue(input: HTMLInputElement, value: string) {
  // Get React's internal value setter
  const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value'
  )?.set;

  nativeInputValueSetter?.call(input, value);

  // Dispatch event to trigger React's onChange
  input.dispatchEvent(new Event('input', { bubbles: true }));
  input.dispatchEvent(new Event('change', { bubbles: true }));
}
```

## MutationObserver for Dynamic SPAs

Watch for DOM changes in single-page applications:

```typescript
function watchForElement(selector: string, callback: (el: Element) => void) {
  // Check if already exists
  const existing = document.querySelector(selector);
  if (existing) {
    callback(existing);
    return;
  }

  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      for (const node of mutation.addedNodes) {
        if (node instanceof Element) {
          const match = node.matches(selector) ? node : node.querySelector(selector);
          if (match) {
            callback(match);
            observer.disconnect();
            return;
          }
        }
      }
    }
  });

  observer.observe(document.body, { childList: true, subtree: true });
  return observer;
}
```

## Extension-Specific React Hooks

### useExtensionMessage

Listen for messages from other extension contexts:

```typescript
function useExtensionMessage<T>(
  action: string,
  handler: (data: T, sender: chrome.runtime.MessageSender) => void
) {
  useEffect(() => {
    const listener = (
      msg: { action: string; payload: T },
      sender: chrome.runtime.MessageSender
    ) => {
      if (msg.action === action) handler(msg.payload, sender);
    };
    chrome.runtime.onMessage.addListener(listener);
    return () => chrome.runtime.onMessage.removeListener(listener);
  }, [action, handler]);
}
```

### useActiveTab

Get information about the currently active tab:

```typescript
function useActiveTab() {
  const [tab, setTab] = useState<chrome.tabs.Tab | null>(null);

  useEffect(() => {
    chrome.tabs.query({ active: true, currentWindow: true }).then(([t]) => {
      setTab(t ?? null);
    });

    const listener = (activeInfo: chrome.tabs.TabActiveInfo) => {
      chrome.tabs.get(activeInfo.tabId).then(setTab);
    };
    chrome.tabs.onActivated.addListener(listener);
    return () => chrome.tabs.onActivated.removeListener(listener);
  }, []);

  return tab;
}
```

### useAlarm

React wrapper for chrome.alarms:

```typescript
function useAlarm(name: string, callback: () => void) {
  useEffect(() => {
    const listener = (alarm: chrome.alarms.Alarm) => {
      if (alarm.name === name) callback();
    };
    chrome.alarms.onAlarm.addListener(listener);
    return () => chrome.alarms.onAlarm.removeListener(listener);
  }, [name, callback]);
}
```

## Performance in Extension UIs

### Popup Performance
Popups should render instantly. Avoid:
- Heavy initial data fetching
- Large bundle sizes
- Complex animations on mount

Prefer:
- Pre-cached data in `chrome.storage.session`
- Code splitting for popup-specific bundles
- Simple CSS transitions over JS animations

### Side Panel Performance
Side panels persist longer but still need efficiency:
- Virtualize long lists (react-window, @tanstack/virtual)
- Debounce storage writes
- Clean up subscriptions on unmount

### Content Script UI Performance
Injected UI affects host page performance:
- Keep Shadow DOM trees small
- Avoid frequent DOM mutations
- Use `requestAnimationFrame` for visual updates
- Never block the host page's main thread

## Accessibility in Extension UIs

### Popup Accessibility
- Browser automatically focuses the popup document
- Use semantic HTML (`<button>`, `<a>`, `<input>`)
- Tab order flows naturally with semantic elements
- Minimum touch target: 44x44px for mobile-friendly extensions

### Side Panel Accessibility
- Implement landmark regions (`<main>`, `<nav>`, `<aside>`)
- Announce dynamic content changes with `aria-live`
- Support keyboard shortcuts for common actions

### Content Script Injected UI
- Focus trap: keep Tab cycling within injected modals
- Focus restore: return focus to trigger element on close
- Screen reader announcements: use `aria-live="polite"` for status changes
- Escape key: always close injected overlays

### WCAG Compliance Checklist for Extensions
- WCAG 2.1 (Keyboard Accessible): all interactive elements operable via keyboard
- WCAG 2.4.3 (Focus Order): logical sequential tab order
- WCAG 2.4.7 (Focus Visible): clear focus indicators
- WCAG 4.1.2 (Name, Role, Value): custom controls expose name, role, state programmatically

## Dark Mode Support

```typescript
// Detect system preference
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

// Or read from extension settings
const { theme } = await chrome.storage.sync.get({ theme: 'system' });

function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    chrome.storage.sync.get({ theme: 'system' }).then(({ theme }) => {
      if (theme === 'system') {
        setDark(prefersDark.matches);
        prefersDark.addEventListener('change', (e) => setDark(e.matches));
      } else {
        setDark(theme === 'dark');
      }
    });
  }, []);

  return (
    <div className={dark ? 'dark' : 'light'}>
      {children}
    </div>
  );
}
```
