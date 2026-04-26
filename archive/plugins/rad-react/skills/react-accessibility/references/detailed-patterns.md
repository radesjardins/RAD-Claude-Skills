# React Accessibility — Detailed Patterns

## Focus Restoration on Route Change

```tsx
import { useRef, useEffect } from 'react';

function PageHeading({ title }: { title: string }) {
  const headingRef = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    headingRef.current?.focus();
  }, [title]);

  // tabIndex={-1} allows programmatic focus without entering tab order
  return <h1 tabIndex={-1} ref={headingRef}>{title}</h1>;
}
```

## Focus Trap for Modal

```tsx
import { useRef, useEffect, useCallback } from 'react';

function Modal({ isOpen, onClose, children }: {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}) {
  const modalRef = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      triggerRef.current = document.activeElement as HTMLElement;
      modalRef.current?.focus();
    } else {
      triggerRef.current?.focus(); // Restore focus on close
    }
  }, [isOpen]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
      return;
    }

    if (e.key === 'Tab') {
      const focusable = modalRef.current?.querySelectorAll<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      if (!focusable?.length) return;

      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  }, [onClose]);

  if (!isOpen) return null;

  return (
    <>
      <div className="overlay" aria-hidden="true" onClick={onClose} />
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        tabIndex={-1}
        onKeyDown={handleKeyDown}
      >
        <h2 id="modal-title">Dialog Title</h2>
        {children}
        <button onClick={onClose}>Close</button>
      </div>
    </>
  );
}
```

## Skip Link

```tsx
function SkipLink() {
  return (
    <a
      href="#main-content"
      className="skip-link"
      // CSS: position absolute, off-screen by default,
      // visible on :focus with high z-index
    >
      Skip to main content
    </a>
  );
}

// In layout:
<body>
  <SkipLink />
  <nav>...</nav>
  <main id="main-content" tabIndex={-1}>
    {children}
  </main>
</body>
```

```css
.skip-link {
  position: absolute;
  left: -9999px;
  top: auto;
  width: 1px;
  height: 1px;
  overflow: hidden;
}

.skip-link:focus {
  position: fixed;
  top: 10px;
  left: 10px;
  width: auto;
  height: auto;
  padding: 8px 16px;
  background: #000;
  color: #fff;
  z-index: 9999;
  font-size: 16px;
}
```

## ARIA Live Region for Notifications

```tsx
function Notifications() {
  const [message, setMessage] = useState('');

  return (
    <>
      {/* Polite: waits for user to finish current task */}
      <div aria-live="polite" aria-atomic="true" className="sr-only">
        {message}
      </div>

      {/* Alert: interrupts immediately for urgent messages */}
      <div role="alert" className="sr-only">
        {urgentMessage}
      </div>
    </>
  );
}
```

## Accessible Form Pattern

```tsx
function LoginForm() {
  const [errors, setErrors] = useState<Record<string, string>>({});

  return (
    <form aria-labelledby="login-heading">
      <h2 id="login-heading">Sign In</h2>

      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          aria-required="true"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? "email-error" : undefined}
        />
        {errors.email && (
          <span id="email-error" role="alert">{errors.email}</span>
        )}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          aria-required="true"
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? "password-error" : undefined}
        />
        {errors.password && (
          <span id="password-error" role="alert">{errors.password}</span>
        )}
      </div>

      <button type="submit">Sign In</button>
    </form>
  );
}
```

## Keyboard-Only Interactive Element

```tsx
// BAD: div with onClick — not keyboard accessible
<div onClick={handleClick}>Click me</div>

// GOOD: native button
<button onClick={handleClick}>Click me</button>

// If div is truly necessary (rare), add full keyboard support:
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  }}
>
  Click me
</div>
```

## Image Accessibility

```tsx
// Informative image — describe its meaning
<img src="/chart.png" alt="Sales increased 40% from Q1 to Q2 2026" />

// Decorative image — hide from assistive technology
<img src="/divider.svg" alt="" />
<img src="/bg-pattern.png" role="presentation" alt="" />

// Complex image — use aria-describedby for long description
<figure>
  <img src="/architecture.png" alt="System architecture diagram"
       aria-describedby="arch-desc" />
  <figcaption id="arch-desc">
    The system consists of three layers: a React frontend...
  </figcaption>
</figure>
```

## Testing with React Testing Library

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('form shows error for empty email', async () => {
  render(<LoginForm />);

  // Query by role — matches what assistive technology sees
  const submitButton = screen.getByRole('button', { name: /sign in/i });
  await userEvent.click(submitButton);

  // Query by role alert — checks aria error announcement
  const error = screen.getByRole('alert');
  expect(error).toHaveTextContent('Email is required');

  // Query by label — matches form label association
  const emailInput = screen.getByLabelText(/email/i);
  expect(emailInput).toHaveAttribute('aria-invalid', 'true');
});
```
