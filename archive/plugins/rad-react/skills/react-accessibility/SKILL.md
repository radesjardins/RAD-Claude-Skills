---
name: react-accessibility
description: This skill should be used when the user is working on accessibility in React, asking about "ARIA attributes", "focus management", "keyboard navigation", "screen reader support", "semantic HTML in React", "accessibility testing", "react-axe", "eslint-plugin-jsx-a11y", "focus trap", "skip links", "color contrast", "a11y", "accessible forms", "aria-live", or building inclusive React interfaces.
---

# React Accessibility

Build accessible React interfaces using semantic HTML, ARIA, focus management, keyboard navigation, and automated testing. Accessibility is not an add-on — it is a structural quality of the component architecture.

## Semantic HTML First

Use native elements: `<nav>`, `<main>`, `<button>`, `<header>`, `<section>` instead of `<div>`. Native elements provide built-in keyboard behavior and screen reader announcements.

- Use React Fragments (`<>...</>`) to group elements without breaking semantic layout (lists, tables)
- Use `htmlFor` (not `for`) to associate labels with inputs
- **First rule of ARIA:** Use native semantic HTML instead of ARIA whenever possible

## ARIA in JSX

All `aria-*` attributes remain **hyphen-cased** in JSX (unlike standard DOM props which use camelCase):

```tsx
<button aria-expanded={isOpen} aria-controls="menu-panel">
  Menu
</button>
```

Keep ARIA states synchronized with React state — `aria-expanded` must reflect whether the menu is actually open.

## Focus Management

React's constant DOM updates can cause focus to be lost or reset to the document body. Manage focus explicitly:

### Restoring Focus

When content changes (route transitions, deleted items, view switches):
1. Apply `tabIndex={-1}` to the target element (makes it programmatically focusable)
2. Use `useRef` + `useEffect` to call `.focus()` after render

### Focus Traps (Modals/Dialogs)

When a modal opens:
- Trap `Tab`/`Shift+Tab` cycling within the modal
- Make background content `inert` or `aria-hidden="true"`
- `Escape` key closes the dialog
- Restore focus to the trigger element on close

### Skip Links

Hidden anchors that become visible on keyboard focus. Allow users to bypass repetitive navigation and jump to main content.

## Keyboard Navigation

**All interactive functionality must be operable with keyboard.** Critical rules:

- Use natively focusable elements (`<button>`, `<a>`, `<input>`) — not `<div onClick>`
- Never remove focus outlines (`outline: 0`) without a visible replacement
- Use `:focus-visible` for keyboard-only focus styles
- Attach `onFocus`/`onBlur` alongside mouse events

## Color Contrast

- Text: minimum 4.5:1 contrast ratio (WCAG AA)
- Large text (18pt regular / 14pt bold): 3:1 minimum
- Never use color alone to convey meaning — add icons or text

## Screen Reader Considerations

- Informative images need descriptive `alt` text
- Decorative images use `alt=""` or `role="presentation"`
- Dynamic content (toasts, route changes) needs `aria-live="polite"` or `role="alert"`

## Development Tools

### eslint-plugin-jsx-a11y

Real-time AST linting in the editor. Flags missing `alt` text, incorrect ARIA roles, and inaccessible patterns during development.

### react-axe (@axe-core/react)

Audits the rendered DOM at runtime. Logs violations to Chrome DevTools console, categorized by severity. **Import dynamically in development only:**

```tsx
if (process.env.NODE_ENV !== 'production') {
  import('react-axe').then(axe => axe.default(React, ReactDOM, 1000));
}
```

## Testing Accessibility

1. **Manual keyboard test:** Disconnect mouse, navigate entire app with Tab, Shift+Tab, Enter, Space, Escape
2. **React Testing Library:** Use `getByRole` and `getByLabelText` as primary selectors — if RTL cannot find the element, assistive technology cannot either
3. **Screen readers:** Test with NVDA (Firefox), JAWS (Chrome/Edge), VoiceOver (Safari)

## Additional Resources

### Reference Files

- **`references/detailed-patterns.md`** — Complete code examples for focus management, focus traps, skip links, ARIA patterns, and accessible component templates
