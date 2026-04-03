# React Security — Detailed Patterns

## Complete Server Action Auth Pattern (Next.js)

```tsx
// lib/auth.ts — server-only
import 'server-only';
import { getServerSession } from 'next-auth';
import { authOptions } from './auth-options';
import { db } from './db';

export async function requireAuth() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id) throw new Error('UNAUTHORIZED');
  return session.user;
}

export async function requireOwnership(resourceOwnerId: string) {
  const user = await requireAuth();
  if (user.id !== resourceOwnerId) throw new Error('FORBIDDEN');
  return user;
}
```

```tsx
// app/actions/posts.ts
'use server'
import 'server-only';
import { z } from 'zod';
import { requireAuth, requireOwnership } from '@/lib/auth';
import { db } from '@/lib/db';
import { revalidatePath } from 'next/cache';

const UpdatePostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(10),
});

export async function updatePost(postId: string, formData: FormData) {
  // 1. Auth check
  const user = await requireAuth();

  // 2. Ownership check (prevents IDOR)
  const post = await db.post.findUnique({ where: { id: postId } });
  if (!post || post.authorId !== user.id) {
    return { error: 'Not found' }; // Deliberately vague
  }

  // 3. Input validation
  const parsed = UpdatePostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  });
  if (!parsed.success) {
    return { errors: parsed.error.flatten().fieldErrors };
  }

  // 4. Mutation — only after all checks pass
  await db.post.update({
    where: { id: postId },
    data: parsed.data,
  });

  revalidatePath(`/posts/${postId}`);
  return { success: true };
}
```

## Zod Validation for FormData

```tsx
import { z } from 'zod';

// Define schema matching form fields
const ContactSchema = z.object({
  name: z.string().min(1, 'Name required').max(100),
  email: z.string().email('Invalid email'),
  message: z.string().min(10).max(2000),
  // Coerce file uploads
  attachment: z.instanceof(File).optional(),
});

export async function submitContact(formData: FormData) {
  'use server';
  const parsed = ContactSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
    message: formData.get('message'),
    attachment: formData.get('attachment') || undefined,
  });

  if (!parsed.success) {
    return {
      errors: parsed.error.flatten().fieldErrors,
    };
  }
  // All fields are typed and validated here
  await sendContactEmail(parsed.data);
  return { success: true };
}
```

## Content Security Policy (CSP)

Add CSP headers in Next.js to prevent XSS even if sanitization is bypassed:

```tsx
// next.config.ts
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      "script-src 'self' 'nonce-{nonce}'",  // nonces for inline scripts
      "style-src 'self' 'unsafe-inline'",   // adjust based on CSS-in-JS usage
      "img-src 'self' data: blob:",
      "connect-src 'self' https://api.yourservice.com",
      "frame-ancestors 'none'",             // prevents clickjacking
    ].join('; '),
  },
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
];

export default {
  async headers() {
    return [{ source: '/(.*)', headers: securityHeaders }];
  },
};
```

## Data Minimization — DTO Pattern

Never return raw database records from Server Components or Server Actions:

```tsx
// BAD: exposes all fields including hashed password, internal IDs, etc.
export async function getUser(id: string) {
  return await db.user.findUnique({ where: { id } });
}

// GOOD: explicit field selection returns only what the client needs
export async function getUser(id: string) {
  const user = await db.user.findUnique({
    where: { id },
    select: {
      id: true,
      name: true,
      email: true,
      role: true,
      // passwordHash: NOT included
      // internalFlags: NOT included
    },
  });
  return user;
}
```

## Electron + React Security

Electron apps embedding React have a critical additional attack surface: XSS can escalate to Remote Code Execution (RCE) if `nodeIntegration` is enabled for renderer processes.

### Mandatory Electron Security Config

```javascript
// main/index.ts
const win = new BrowserWindow({
  webPreferences: {
    nodeIntegration: false,       // REQUIRED — prevents RCE via XSS
    contextIsolation: true,       // REQUIRED — isolates preload from renderer
    sandbox: true,                // Recommended — OS-level sandboxing
    webSecurity: true,            // Never disable
    allowRunningInsecureContent: false,
  },
});
```

### Safe IPC via contextBridge

```javascript
// preload.ts — only expose what the renderer needs
import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('api', {
  // Allowlist specific channels — never expose ipcRenderer directly
  readFile: (path: string) => ipcRenderer.invoke('read-file', path),
  saveSettings: (data: unknown) => ipcRenderer.invoke('save-settings', data),
});
```

```javascript
// main/ipc-handlers.ts — validate in main process
ipcMain.handle('save-settings', async (event, data) => {
  // Validate with Zod before touching filesystem
  const parsed = SettingsSchema.safeParse(data);
  if (!parsed.success) throw new Error('Invalid settings');
  await writeSettings(parsed.data);
});
```

**Never:**
- Expose `ipcRenderer` directly via contextBridge
- Accept file paths from renderer without validation (path traversal risk)
- Load remote content with `nodeIntegration: true`
- Serve local HTML over `file://` protocol (use custom protocol with CSP)

## URL Validation

```tsx
// BAD: javascript: URL executes script on click
<a href={userProvidedUrl}>Click</a>

// GOOD: validate before rendering
function SafeLink({ href, children }: { href: string; children: React.ReactNode }) {
  const isValidUrl = (() => {
    try {
      const url = new URL(href);
      return url.protocol === 'https:' || url.protocol === 'http:';
    } catch {
      return false;
    }
  })();

  if (!isValidUrl) return <span>{children}</span>;
  return <a href={href} rel="noopener noreferrer">{children}</a>;
}
```

## Dependency Security

- Run `npm audit` or `pnpm audit` in CI — fail builds on high-severity vulnerabilities
- Pin direct dependencies with exact versions in `package.json` to prevent supply chain attacks
- Review CHANGELOG before upgrading major versions of authentication libraries
- Never install packages with names similar to well-known packages (typosquatting)
