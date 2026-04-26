# Next.js Security Audit Checklist

Complete pre-deployment security audit with configuration patterns and code examples.

---

## Pre-Deployment Security Audit

Run through every section before deploying to production. Each item is a potential vulnerability.

---

### 1. Authentication & Session Management

- [ ] Session tokens stored in `httpOnly`, `Secure`, `SameSite=Lax` cookies
- [ ] No tokens in `localStorage` or `sessionStorage`
- [ ] Session IDs rotated on privilege escalation (login, role change)
- [ ] Session expiration set to reasonable timeout (e.g., 24h for low-risk, 1h for high-risk)
- [ ] MFA enforced for high-risk actions (password change, payment, admin)
- [ ] Passkeys (WebAuthn/FIDO2) offered as primary auth where possible
- [ ] Failed login attempts rate-limited per IP and per account
- [ ] Account lockout after repeated failures (with notification)

**Cookie configuration pattern:**
```typescript
import { cookies } from 'next/headers';

export async function setSession(token: string) {
  const cookieStore = await cookies();
  cookieStore.set('session', token, {
    httpOnly: true,       // Not accessible via JavaScript
    secure: true,         // HTTPS only
    sameSite: 'lax',      // CSRF protection
    maxAge: 60 * 60 * 24, // 24 hours
    path: '/',
  });
}
```

---

### 2. Server Actions & API Routes

- [ ] Every Server Action implements all 5 security layers (auth, validate, authorize, rate-limit, safe errors)
- [ ] Input validated with Zod/Valibot using `safeParse()` — never `parse()` (which throws)
- [ ] Authorization checks verify the user owns/can access the specific resource (prevents IDOR)
- [ ] Rate limiting applied per-user and per-IP
- [ ] Error responses return generic messages — no stack traces, no internal paths
- [ ] Server Actions marked with `'use server'` at the top of the file or function
- [ ] No database credentials or API keys accessible from Server Actions (use DAL)

**Rate limiting pattern:**
```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '60 s'), // 10 requests per minute
});

export async function protectedAction(data: unknown) {
  const session = await verifyAuth();
  if (!session) throw new Error('Unauthorized');

  const { success } = await ratelimit.limit(session.user.id);
  if (!success) throw new Error('Too many requests');

  // ... proceed with validated input
}
```

---

### 3. Data Access Security

- [ ] All database queries centralized in a Data Access Layer (`lib/dal.ts`)
- [ ] DAL module marked with `import 'server-only'`
- [ ] DAL functions verify authorization before returning data
- [ ] DAL returns DTOs — never raw database records with sensitive fields
- [ ] DAL functions wrapped with `React.cache()` for request deduplication
- [ ] `process.env` access restricted to DAL only
- [ ] React Taint APIs used for extra-sensitive data (passwords, tokens) — experimental

**DTO pattern:**
```typescript
// lib/dal.ts
import 'server-only';

export async function getUserProfile(userId: string) {
  const session = await verifyAuth();
  if (!session) throw new Error('Unauthorized');
  if (session.user.id !== userId && !session.user.isAdmin) {
    throw new Error('Forbidden');
  }

  const user = await db.user.findUnique({ where: { id: userId } });
  if (!user) return null;

  // DTO — exclude sensitive fields
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    avatar: user.avatarUrl,
    // EXCLUDED: passwordHash, apiKey, internalNotes, deletedAt
  };
}
```

---

### 4. Environment Variables

- [ ] `.env` and `.env.local` in `.gitignore`
- [ ] No `NEXT_PUBLIC_` prefix on database URLs, JWT secrets, or private API keys
- [ ] Production secrets stored in secret manager (AWS Secrets Manager, Vault, Vercel)
- [ ] `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` synchronized across multi-instance deployments
- [ ] All required env vars validated at build time or in `instrumentation.ts`
- [ ] No secrets hardcoded in source code

**Startup validation pattern:**
```typescript
// instrumentation.ts
export async function register() {
  const required = ['DATABASE_URL', 'JWT_SECRET', 'SESSION_SECRET'];
  const missing = required.filter(key => !process.env[key]);
  if (missing.length > 0) {
    throw new Error(`Missing required env vars: ${missing.join(', ')}`);
  }
}
```

---

### 5. Security Headers

- [ ] Content Security Policy (CSP) configured with nonce-based script-src
- [ ] `X-Frame-Options: DENY` prevents clickjacking
- [ ] `X-Content-Type-Options: nosniff` prevents MIME-sniffing
- [ ] `Strict-Transport-Security` enforces HTTPS with preload
- [ ] `Referrer-Policy: strict-origin-when-cross-origin` limits referrer leakage
- [ ] `Permissions-Policy` restricts browser feature access (camera, microphone, geolocation)

**Complete headers configuration:**
```typescript
// next.config.ts
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      "script-src 'self' 'nonce-${nonce}' 'strict-dynamic'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' blob: data: https:",
      "font-src 'self'",
      "connect-src 'self' https://api.example.com",
      "frame-ancestors 'none'",
      "base-uri 'self'",
      "form-action 'self'",
    ].join('; '),
  },
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
];

import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  async headers() {
    return [{ source: '/(.*)', headers: securityHeaders }];
  },
};

export default nextConfig;
```

---

### 6. CSRF Protection

- [ ] Server Actions using built-in Origin/Host comparison (automatic)
- [ ] `serverActions.allowedOrigins` configured if behind reverse proxy
- [ ] Route Handlers using cookies have `SameSite=Lax` or `Strict`
- [ ] Third-party CSRF tokens considered for sensitive cookie-based routes

**Allowed origins configuration:**
```typescript
// next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  serverActions: {
    allowedOrigins: ['my-app.example.com', 'staging.example.com'],
  },
};
```

---

### 7. XSS Prevention

- [ ] No usage of `dangerouslySetInnerHTML` without sanitization
- [ ] If rendering dynamic HTML, sanitized with DOMPurify first
- [ ] Redirect URLs validated as relative paths (prevent open redirects)
- [ ] User-generated content escaped by React's default behavior (no bypass)
- [ ] No `eval()`, `new Function()`, or dynamic script injection

**Safe HTML rendering:**
```typescript
import DOMPurify from 'isomorphic-dompurify';

export function SafeHTML({ html }: { html: string }) {
  const clean = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['p', 'b', 'i', 'em', 'strong', 'a', 'ul', 'ol', 'li', 'br', 'h2', 'h3'],
    ALLOWED_ATTR: ['href', 'title'],
  });
  return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}
```

**Open redirect prevention:**
```typescript
export function safeRedirect(url: string, fallback = '/') {
  // Only allow relative paths
  if (!url.startsWith('/') || url.startsWith('//')) {
    return fallback;
  }
  return url;
}
```

---

### 8. Middleware / Proxy Security

- [ ] Middleware NOT used as sole auth boundary (CVE-2025-29927 risk)
- [ ] Auth re-verified in every Route Handler, Server Action, and DAL function
- [ ] Middleware matcher patterns correctly scoped (not accidentally excluding routes)
- [ ] No sensitive business logic in middleware (edge runtime limitations)

---

### 9. Dependency & CI/CD Security

- [ ] Dependabot or Socket enabled for dependency vulnerability scanning
- [ ] SAST tool integrated in CI pipeline
- [ ] Secret scanner (TruffleHog) runs on every PR
- [ ] `npm audit` or `pnpm audit` run during CI
- [ ] Lock files committed (`package-lock.json` or `pnpm-lock.yaml`)
- [ ] No `postinstall` scripts from untrusted packages
- [ ] E2E tests block merge on failure
- [ ] Docker images use non-root user and minimal base image

**CI audit script (package.json):**
```json
{
  "scripts": {
    "audit": "npm audit --audit-level=high",
    "audit:fix": "npm audit fix",
    "preinstall": "npx only-allow pnpm"
  }
}
```

---

### 10. Production Monitoring

- [ ] Failed auth attempts logged and alerted
- [ ] Rate limit triggers monitored
- [ ] Error tracking (Sentry, Datadog) initialized in `instrumentation.ts`
- [ ] Security headers verified with securityheaders.com or similar scanner
- [ ] Regular dependency updates scheduled
- [ ] Incident response plan documented

**Monitoring initialization pattern:**
```typescript
// instrumentation.ts
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    const Sentry = await import('@sentry/nextjs');
    Sentry.init({
      dsn: process.env.SENTRY_DSN,
      tracesSampleRate: 0.1,
      environment: process.env.NODE_ENV,
    });
  }
}
```
