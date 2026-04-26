---
name: Zod Error Handling
description: This skill should be used when the user asks about "Zod error handling", "parse vs safeParse", "ZodError", "z.treeifyError", "z.flattenError", "z.prettifyError", "formatting Zod errors", "Zod error messages", "custom Zod errors", "z.config error map", "Zod error precedence", "Zod validation errors for API response", or "how to display Zod errors to users". Provides comprehensive guidance on Zod's error system, formatting utilities, and customization.
version: 1.0.0
---

# Zod Error Handling

## `.parse()` vs `.safeParse()`: The Decision Rule

| Use | When |
|---|---|
| `.parse()` | Data is expected to always be valid; failure is a programming error or unrecoverable exception. Use with `try/catch`. |
| `.safeParse()` | Validating untrusted external data where failures are routine (forms, API requests). Returns result without throwing. |
| `.parseAsync()` / `.safeParseAsync()` | Schemas with async `.refine()` calls. |

```typescript
// .parse() — throws ZodError on failure
try {
  const user = UserSchema.parse(rawData);
  // user is fully typed
} catch (err) {
  if (err instanceof ZodError) {
    // handle validation failure
  }
}

// .safeParse() — never throws; returns discriminated union
const result = UserSchema.safeParse(rawData);
if (result.success) {
  const user = result.data; // typed T
} else {
  const errors = result.error; // ZodError
}
```

**Prefer `.safeParse()` in performance-critical code.** Throwing and catching exceptions in JavaScript is expensive. In high-throughput handlers or tight loops, `.safeParse()` avoids that overhead entirely.

## ZodError Structure

A `ZodError` contains an `.issues` array. Each issue provides:

```typescript
{
  code: "invalid_type" | "too_small" | "custom" | ..., // Machine-readable error code
  path: ["user", "address", 0, "zip"],                 // Path to invalid field
  message: "Expected string, received number",         // Human-readable message
  // Additional fields depending on code
}
```

Access issues directly for programmatic error handling:

```typescript
const result = Schema.safeParse(data);
if (!result.success) {
  result.error.issues.forEach(issue => {
    console.log(`${issue.path.join(".")} — ${issue.message}`);
  });
}
```

## Zod 4 Error Formatting Utilities

Zod 4 replaces the deprecated `.format()` and `.flatten()` instance methods with top-level functions. Choose based on audience:

### `z.prettifyError(error)` — Developer Logs

Generates a multi-line, human-readable string. Use for server logs and debug output:

```typescript
const result = Schema.safeParse(badData);
if (!result.success) {
  console.error(z.prettifyError(result.error));
  // ✗ user.email: Invalid email
  // ✗ user.age: Expected number, received string
}
```

### `z.flattenError(error)` — Simple API Responses

Returns a shallow object: `{ formErrors: string[], fieldErrors: { [key]: string[] } }`. Best for flat schemas (one level deep):

```typescript
const result = CreateUserSchema.safeParse(body);
if (!result.success) {
  return res.status(400).json(z.flattenError(result.error));
  // { formErrors: [], fieldErrors: { email: ["Invalid email"], age: ["Required"] } }
}
```

### `z.treeifyError(error)` — Nested UI Forms

Converts a flat `ZodError` into a nested object mirroring the schema shape. Essential for complex multi-level forms:

```typescript
const result = OrderSchema.safeParse(formData);
if (!result.success) {
  const tree = z.treeifyError(result.error);
  // tree.properties.shipping.properties.address.properties.zip.errors
  // → ["Invalid ZIP code format"]
}
```

**TypeScript hint:** If the IDE shows `properties` doesn't exist, pass the schema type explicitly:

```typescript
const tree = z.treeifyError<typeof OrderSchema>(result.error); // ✅
```

## Never Expose Raw ZodErrors to Clients

Returning the raw `ZodError` or unformatted `.issues` array to API clients is an anti-pattern:

- Exposes internal data model structure
- Verbose and difficult to consume
- Can reveal sensitive field names

```typescript
// BAD: Leaks internal structure
res.status(400).json(result.error);

// GOOD: Formatted for client consumption
res.status(400).json({
  message: "Validation failed",
  errors: z.flattenError(result.error).fieldErrors,
});
```

## Error Customization in Zod 4

The fragmented Zod 3 approach (`invalid_type_error`, `required_error`, per-schema `errorMap`) is replaced by a **single unified `error` parameter** on all schema methods:

```typescript
// Zod 3 (deprecated pattern)
z.string({ invalid_type_error: "Must be a string", required_error: "Required" })

// Zod 4 — unified error parameter
z.string({ error: "Must be a string" })
z.string({ error: (issue) => issue.input === undefined ? "Required" : "Must be text" })
```

The `error` parameter accepts:
- A string (used for all error cases)
- A function `(issue: ZodIssue) => string | undefined` (for conditional messages)

### Error Precedence (Highest to Lowest)

1. **Schema-level `error` parameter** — defined inline on the schema
2. **Per-parse error maps** — passed to `.parse({ errorMap: ... })` (rare)
3. **Global config** — set via `z.config({ customError: ... })`
4. **Locale defaults** — built-in Zod error messages

```typescript
// Schema-level wins over global
z.config({
  customError: (issue) => "Global default error",
});

const EmailSchema = z.email({ error: "Must be a valid email address" }); // This wins
```

### Global Configuration

Set global error handling at application startup:

```typescript
import { z } from "zod";

z.config({
  customError: (issue, ctx) => {
    if (issue.code === "invalid_type" && issue.input === undefined) {
      return "This field is required";
    }
    return undefined; // Fall through to Zod's default message
  },
});
```

### Internationalization

Load locale files for translated error messages:

```typescript
import { z } from "zod";
import { es } from "zod/locales/es"; // Spanish

z.config(es());
```

## The `reportInput` Security Warning

Zod intentionally omits raw input from error issues to prevent accidental logging of passwords or PII. The `reportInput: true` flag re-enables this:

```typescript
// RISKY: Logs user's raw password in error output
z.config({ reportInput: true });

// Only enable in development/debugging environments
// Never in production
```

## Additional Resources

- **`references/error-formatting.md`** — Complete examples of all formatting utilities with nested schema scenarios
- **`references/custom-errors.md`** — Advanced error customization: conditional messages, i18n setup, error map patterns
