# AI Codegen Guardrails for TypeScript

AI coding assistants (Claude Code, GitHub Copilot, Cursor) are productive but systematically introduce specific TypeScript anti-patterns. This guide documents the patterns, explains why they occur, and provides the corrections.

## Why AI Generates Unsafe TypeScript

AI models optimize for code that **compiles quickly**, not code that is **safe at runtime**. When the type system pushes back, AI tools reach for escape hatches (`any`, `!`, `as`) rather than restructuring the type hierarchy. They also:

- Cannot verify runtime behavior — they produce plausible shapes, not proven contracts
- Hallucinate methods and deprecated APIs
- Prioritize "making the compiler happy" over type correctness
- Generate code that passes `tsc` but fails at runtime with real data

## The 10 Most Common AI TypeScript Mistakes

### 1. `any` for Complex Types
**What AI does:** Uses `any` when working with external data, generic utilities, or complex types.

```typescript
// AI-generated
async function fetchData(endpoint: string): Promise<any> {
  const res = await fetch(endpoint);
  return res.json();
}

const user = (await fetchData('/api/users/1')) as User;
```

**Correction:**
```typescript
async function fetchUser(id: string): Promise<Result<User, 'not-found' | 'network-error'>> {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) return err(res.status === 404 ? 'not-found' : 'network-error');
  return UserSchema.safeParse(await res.json()).success
    ? ok(UserSchema.parse(await res.json()))
    : err('network-error');
}
```

### 2. Non-Null Assertion Spray
**What AI does:** Adds `!` to silence "Object is possibly undefined" errors.

```typescript
// AI-generated — fragile
const user = getUser(id)!;
const name = user.profile!.name!;
const btn = document.querySelector('#submit-btn')!;
btn.addEventListener('click', handler);
```

**Correction:**
```typescript
const user = getUser(id);
if (!user) throw new Error(`User ${id} not found`);

const name = user.profile?.name;
if (!name) return handleMissingName();

const btn = document.querySelector('#submit-btn');
if (!(btn instanceof HTMLButtonElement)) return;
btn.addEventListener('click', handler);
```

### 3. `.parse()` Instead of `.safeParse()`
**What AI does:** Uses Zod's throwing `.parse()` everywhere.

```typescript
// AI-generated — throws, requires try/catch
const body = CreateUserSchema.parse(request.body);
const config = EnvSchema.parse(process.env);
```

**Correction:**
```typescript
// At startup (throwing is appropriate — crash fast on misconfiguration)
const env = EnvSchema.parse(process.env); // OK at startup

// At API boundary (never throw — return structured error)
const result = CreateUserSchema.safeParse(request.body);
if (!result.success) {
  return reply.status(400).send({
    error: 'VALIDATION_FAILED',
    details: result.error.flatten().fieldErrors,
  });
}
const body = result.data;
```

### 4. Silent Catch Blocks
**What AI does:** Generates empty or trivially-logging catch blocks.

```typescript
// AI-generated — hides all errors
try {
  await processPayment(order);
} catch (err) {
  console.error(err); // "handled"
}
```

**Correction:**
```typescript
try {
  await processPayment(order);
} catch (err) {
  if (err instanceof PaymentDeclinedError) {
    return { ok: false, error: 'PAYMENT_DECLINED', code: err.declineCode };
  }
  if (err instanceof NetworkError) {
    return { ok: false, error: 'NETWORK_ERROR', retryable: true };
  }
  throw new Error('Payment processing failed', { cause: err });
}
```

### 5. Floating Promises
**What AI does:** Calls async functions without awaiting them.

```typescript
// AI-generated — fire and forget, errors lost
function handleClick() {
  updateUserProfile(userId, changes); // Not awaited!
  showSuccessToast();
}
```

**Correction:**
```typescript
async function handleClick() {
  const result = await updateUserProfile(userId, changes);
  if (!result.ok) {
    showErrorToast(result.error);
    return;
  }
  showSuccessToast();
}
```

### 6. Missing `import type`
**What AI does:** Uses regular `import` for type-only imports.

```typescript
// AI-generated — may cause ESM runtime issues
import { User, Product, Order } from './types';
import { UserService } from './services/user';
```

**Correction:**
```typescript
import type { User, Product, Order } from './types';
import { UserService } from './services/user';
// Or inline:
import { UserService, type User } from './services/user';
```

### 7. Enums Instead of Literal Unions
**What AI does:** Generates `enum` declarations.

```typescript
// AI-generated
enum UserStatus {
  Active = 'ACTIVE',
  Inactive = 'INACTIVE',
  Pending = 'PENDING',
}
```

**Correction:**
```typescript
const USER_STATUS = ['active', 'inactive', 'pending'] as const;
type UserStatus = typeof USER_STATUS[number];
// or simply:
type UserStatus = 'active' | 'inactive' | 'pending';
```

### 8. Annotation Instead of `satisfies`
**What AI does:** Annotates config objects with broad types, losing literal specificity.

```typescript
// AI-generated — loses specific types
const config: Record<string, string | boolean> = {
  apiUrl: 'https://api.example.com',
  debug: false,
  timeout: 5000,
};
```

**Correction:**
```typescript
const config = {
  apiUrl: 'https://api.example.com',
  debug: false,
  timeout: 5000,
} satisfies Record<string, string | boolean | number>;
// config.apiUrl: 'https://api.example.com' (specific, not just string)
```

### 9. Missing Exhaustiveness in Switch
**What AI does:** Adds `default: break` or `default: return` in switch statements over unions.

```typescript
// AI-generated — silently ignores new union members
switch (action.type) {
  case 'INCREMENT': return state + 1;
  case 'DECREMENT': return state - 1;
  default: return state; // New action types silently ignored!
}
```

**Correction:**
```typescript
switch (action.type) {
  case 'INCREMENT': return state + 1;
  case 'DECREMENT': return state - 1;
  case 'RESET': return 0;
  default: return assertNever(action.type);
}
```

### 10. Hallucinated APIs
**What AI does:** Uses deprecated or non-existent TypeScript APIs, or features from future versions.

**Signs:** Compiler errors for methods that "should exist", deprecated import paths, incorrect generic signatures.

**Correction:** Always run `tsc --noEmit` and `eslint` on AI-generated code before accepting it. If the AI's code references an API, verify it in the official TypeScript docs.

## The Verification Loop

Require AI-generated TypeScript to pass this before review:

```bash
# 1. Type check
npx tsc --noEmit

# 2. Lint with zero warnings
npx eslint . --ext .ts,.tsx --max-warnings 0

# 3. Run tests
npm test

# 4. Check type coverage (optional but recommended)
npx typescript-coverage-report --threshold 95
```

Configure Claude Code / Copilot to run these checks automatically. Only review code that passes all four.

## Context Injection for Better AI Output

Provide AI with project context to reduce anti-patterns:

1. **Share `tsconfig.json`** — AI adheres to the configured strictness
2. **Share shared type definitions** — AI uses real types, not hallucinated ones
3. **Share Zod schema files** — AI uses `.safeParse()` and infers correctly
4. **Include anti-pattern rules in CLAUDE.md** — enforces standards automatically

```markdown
<!-- CLAUDE.md excerpt -->
## TypeScript Rules
- Never use `any`. Use `unknown` with a type guard.
- Never use `!` for non-null assertion. Use explicit checks.
- Never use `.parse()` at API boundaries. Use `.safeParse()`.
- Never create regular enums. Use string literal unions or `as const` arrays.
- Always use `import type` for type-only imports.
- Always check exhaustiveness in switch over discriminated unions.
```
