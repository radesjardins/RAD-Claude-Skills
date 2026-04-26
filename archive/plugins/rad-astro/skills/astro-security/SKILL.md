---
name: astro-security
description: >
  This skill should be used when implementing Astro security, configuring Content Security Policy in Astro, preventing XSS in Astro, using set:html safely, handling secrets in Astro, configuring astro:env, Astro authentication patterns, Astro Session API, CSRF protection in Astro, configuring security.checkOrigin, Astro cookie security, middleware security patterns, Astro CORS configuration, protecting API endpoints, security.allowedDomains, environment variable security in Astro, import.meta.env secret leakage
---

# Astro Security

## Core Security Model

Understand that Astro's static-first architecture provides inherent security advantages. Static HTML has a minimal attack surface because there is no server-side code executing at request time. However, when you enable SSR or hybrid rendering modes, you introduce server-side attack vectors that require explicit hardening. Configure security centrally in `astro.config` via the `security` object. Treat every SSR endpoint and server island as a potential attack surface that needs validation, authentication, and input sanitization.

When working in static-only mode, focus your security efforts on build-time data validation and Content Security Policy headers. When working in SSR or hybrid mode, apply the full set of protections described below.

## Content Security Policy (Astro 6)

Enable the built-in CSP support by adding `security: { csp: true }` to `astro.config`. When enabled, Astro automatically generates nonces for inline scripts and styles, injecting them into both the HTML and the CSP header. This prevents XSS attacks by blocking any script or style that does not carry a valid nonce.

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';

export default defineConfig({
  security: {
    csp: true
  }
});
```

Be aware that View Transitions may conflict with strict CSP policies. Test thoroughly when combining `security.csp` with `<ViewTransitions />`. If you encounter issues, consider using a custom CSP header via middleware instead of the built-in option.

For custom CSP headers or when you need fine-grained control over directives, inject the `Content-Security-Policy` header in middleware:

```typescript
// src/middleware.ts
export const onRequest = async (context, next) => {
  const response = await next();
  response.headers.set(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
  );
  return response;
};
```

## XSS Prevention & set:html (CRITICAL)

Astro escapes all dynamic content in templates by default. When you write `{variable}` in an Astro template, the output is HTML-escaped and safe from XSS. Do not circumvent this protection unnecessarily.

The `set:html` directive renders raw, unescaped HTML. This is a direct XSS vector. NEVER use `set:html` with user-provided or untrusted content without sanitization. Always sanitize with DOMPurify before passing content to `set:html`:

```astro
---
import DOMPurify from 'dompurify';
const cleanHTML = DOMPurify.sanitize(userContent);
---
<div set:html={cleanHTML} />
```

Markdown and MDX content from Content Collections is generally safe because it is processed at build time. However, content sourced from external APIs, databases, or user input at request time MUST be sanitized before rendering with `set:html`. When in doubt, sanitize. The performance cost of DOMPurify is negligible compared to the risk of XSS.

## Secret & Environment Variable Handling (CRITICAL)

Understand that `import.meta.env` values are INLINED at build time in Astro 6. This means any secret placed in `import.meta.env` gets permanently baked into the server bundle. NEVER use `import.meta.env` for sensitive values such as API keys, database connection strings, or authentication tokens.

For runtime secrets, use `process.env` directly in server-side code. The preferred approach is the `astro:env` module for type-safe environment variable management:

```typescript
// astro.config.mjs
import { defineConfig, envField } from 'astro/config';

export default defineConfig({
  env: {
    schema: {
      API_URL: envField.string({ context: 'client', access: 'public' }),
      DB_SECRET: envField.string({ context: 'server', access: 'secret' }),
      SESSION_KEY: envField.string({ context: 'server', access: 'secret' }),
    }
  }
});
```

Follow these rules strictly:

- `context: 'server'` makes the variable available only in server-side code. Use this for all secrets.
- `context: 'client'` makes the variable available in the browser. NEVER put secrets here.
- `access: 'secret'` ensures the value is NEVER inlined into build output. Use this for all sensitive values.
- `access: 'public'` allows inlining. Only use for non-sensitive configuration like public API URLs.

Then import in server-side code:

```typescript
import { DB_SECRET } from 'astro:env/server';
import { API_URL } from 'astro:env/client';
```

## CSRF Protection

Enable CSRF protection by setting `security: { checkOrigin: true }` in `astro.config`. This may be the default in Astro 6, but verify and set it explicitly. When enabled, Astro automatically validates the `Origin` header on POST, PUT, and DELETE requests, rejecting any cross-origin form submissions and API calls.

```javascript
export default defineConfig({
  security: {
    checkOrigin: true
  }
});
```

This is essential for any site that handles form submissions or mutations. Do not disable it unless you have implemented your own CSRF token mechanism.

## Host Injection Prevention

Configure `security: { allowedDomains: ['example.com'] }` in `astro.config` to prevent host header injection attacks. This restricts requests to only those claiming to originate from the listed domains:

```javascript
export default defineConfig({
  security: {
    allowedDomains: ['example.com', 'www.example.com']
  }
});
```

This is particularly important for SSR deployments behind reverse proxies where the `Host` header can be spoofed. Always list all valid domains your application serves.

## Authentication & Session Management

### Session API (Astro 6)

Use Astro's built-in Session API for server-side session management. Sessions are stored server-side with only the session ID sent to the client as a cookie. Configure the session backend (memory, Redis, database) in `astro.config`:

```javascript
export default defineConfig({
  session: {
    driver: 'redis',
    // driver-specific options
  }
});
```

Access sessions in endpoints and middleware via `context.session`. Store only the minimum data needed in sessions. Never store raw passwords or full credit card numbers in session data.

### Cookie Security (Non-Negotiable)

When setting cookies, always apply these attributes:

- `httpOnly: true` — prevents JavaScript access so XSS cannot steal session cookies
- `secure: true` — cookies are only sent over HTTPS
- `sameSite: 'lax'` or `sameSite: 'strict'` — prevents CSRF via cookie-based attacks
- Set a reasonable `maxAge` — never use infinite sessions

Use the `Astro.cookies` API for server-side cookie management:

```typescript
Astro.cookies.set('session', sessionId, {
  httpOnly: true,
  secure: true,
  sameSite: 'lax',
  maxAge: 60 * 60 * 24 * 7, // 1 week
  path: '/',
});
```

### Middleware Authentication Pattern

Implement authentication checks in middleware to protect routes consistently:

```typescript
// src/middleware.ts
export const onRequest = async (context, next) => {
  const sessionId = context.cookies.get('session')?.value;

  if (protectedRoute(context.url) && !await validateSession(sessionId)) {
    return context.redirect('/login');
  }

  if (sessionId) {
    const user = await getUser(sessionId);
    context.locals.user = user;  // APPEND to locals, never overwrite entire locals
  }

  return next();
};
```

Always append to `context.locals` rather than replacing it. Other middleware or integrations may have already set values on `locals`.

## API Endpoint Security

Validate authentication in every mutating endpoint (POST, PUT, DELETE). Never assume a request is authenticated just because it reached the endpoint. Use Astro Actions with middleware gating via `getActionContext()` for automatic auth checks where possible.

Implement rate limiting by injecting rate-limit headers in middleware. Return 429 status with a `Retry-After` header when limits are exceeded. Validate and sanitize all request body data — never trust client input. Parse request bodies with schema validation (e.g., Zod) before processing.

Return minimal error information in production. Never expose stack traces, internal paths, or implementation details in error responses:

```typescript
// src/pages/api/data.ts
export async function POST({ request, locals }) {
  if (!locals.user) {
    return new Response(JSON.stringify({ error: 'Unauthorized' }), { status: 401 });
  }

  try {
    const body = await request.json();
    const validated = schema.parse(body); // Zod validation
    const result = await processData(validated);
    return new Response(JSON.stringify(result), { status: 200 });
  } catch (e) {
    // Log full error server-side, return minimal info to client
    console.error(e);
    return new Response(JSON.stringify({ error: 'Request failed' }), { status: 400 });
  }
}
```

## CORS Configuration

For API endpoints consumed by external origins, set CORS headers explicitly in middleware. Never use `Access-Control-Allow-Origin: *` when credentials are involved. Specify the exact allowed origin:

```typescript
// In middleware
const allowedOrigin = 'https://app.example.com';
response.headers.set('Access-Control-Allow-Origin', allowedOrigin);
response.headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
response.headers.set('Access-Control-Allow-Credentials', 'true');
```

Handle preflight OPTIONS requests for complex requests by returning a 204 response with the appropriate CORS headers. Only allow the HTTP methods and headers that your endpoints actually need.

## Security Checklist

Before deploying any Astro application with SSR or hybrid rendering, verify each item:

1. `security.csp: true` enabled in astro.config (Astro 6)
2. `security.checkOrigin: true` set for CSRF protection
3. `security.allowedDomains` configured with all valid domains
4. NO use of `set:html` with unsanitized user content anywhere in the codebase
5. All secrets use `process.env` or `astro:env` with `access: 'secret'`
6. NO secrets stored in `import.meta.env`
7. All cookies set with `httpOnly`, `secure`, and `sameSite` attributes
8. Authentication enforced via middleware populating `context.locals`
9. Rate limiting applied to all public API endpoints
10. CORS configured explicitly with specific origins (no wildcard with credentials)
