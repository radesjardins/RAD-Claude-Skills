# Zod Error Customization Patterns

## The Unified `error` Parameter

In Zod 4, all schema methods accept a unified `error` parameter for customizing messages:

```typescript
// String shorthand — same message for all error cases
z.string({ error: "Please enter a valid text value" })
z.number({ error: "Please enter a number" })
z.string().min(8, { error: "Password must be at least 8 characters" })

// Function — conditional messages based on the issue
z.string({ error: (issue) => {
  if (issue.input === undefined || issue.input === null) return "This field is required";
  if (issue.code === "invalid_type") return "Please enter text, not a number";
  return undefined; // Fall through to Zod default
}})
```

The function receives a `ZodIssue` object and returns a `string` (custom message) or `undefined` (use Zod's default).

## Field-Level Error Customization

```typescript
const RegisterSchema = z.strictObject({
  username: z.string()
    .min(3, { error: "Username must be at least 3 characters" })
    .max(20, { error: "Username cannot exceed 20 characters" })
    .regex(/^[a-z0-9_]+$/, { error: "Username can only contain letters, numbers, and underscores" }),

  email: z.email({ error: "Please enter a valid email address" }),

  password: z.string({ error: "Password is required" })
    .min(12, { error: "Password must be at least 12 characters for security" }),

  role: z.enum(["user", "moderator"], {
    error: (issue) => `Role must be 'user' or 'moderator', received '${issue.input}'`
  }),

  birthdate: z.coerce.date({
    error: (issue) => issue.code === "invalid_date"
      ? "Please enter a valid date"
      : "Birthdate is required"
  }).refine(d => d < new Date(), { message: "Birthdate must be in the past" }),
});
```

## Object-Level Refinement Errors

`.refine()` and `.check()` on object schemas can target a specific field via `path`:

```typescript
const PasswordChangeSchema = z.object({
  currentPassword: z.string(),
  newPassword: z.string().min(12),
  confirmPassword: z.string(),
})
.refine(
  data => data.newPassword === data.confirmPassword,
  {
    message: "New passwords do not match",
    path: ["confirmPassword"], // Error attributed to the confirmPassword field
  }
)
.refine(
  data => data.newPassword !== data.currentPassword,
  {
    message: "New password must differ from current password",
    path: ["newPassword"],
  }
);
```

## Global Error Configuration

Set at application startup to establish defaults for all schemas:

```typescript
// config/zod.ts — import this before any schema usage
import { z } from "zod";

z.config({
  customError: (issue, ctx) => {
    // Provide better messages for common cases across the whole app
    switch (issue.code) {
      case "invalid_type":
        if (issue.input === undefined || issue.input === null) {
          return "This field is required";
        }
        return `Expected ${issue.expected}, received ${issue.received}`;

      case "too_small":
        if (issue.type === "string") {
          return `Must be at least ${issue.minimum} characters`;
        }
        if (issue.type === "number") {
          return `Must be at least ${issue.minimum}`;
        }
        break;

      case "invalid_string":
        if (issue.validation === "email") return "Please enter a valid email address";
        if (issue.validation === "url") return "Please enter a valid URL";
        break;
    }
    return undefined; // Fall through to Zod's built-in message
  },
});
```

## Internationalization (i18n)

Zod 4 ships with built-in locale files:

```typescript
import { z } from "zod";

// Load locale based on user's language preference
async function setLocale(lang: string) {
  const locale = await import(`zod/locales/${lang}`).catch(() => import("zod/locales/en"));
  z.config(locale.default());
}

// At startup for a server-rendered app:
z.config((await import("zod/locales/es")).default()); // Spanish errors globally

// For per-request locale (multi-language API):
// Each validation uses the user's preferred language
```

Available locales: `en`, `ar`, `de`, `es`, `fr`, `it`, `ja`, `ko`, `pt`, `ru`, `tr`, `zh-CN`, `zh-TW`, and others (check `zod/locales/`).

## Error Precedence: Understanding Override Order

```typescript
z.config({ customError: () => "Global fallback" }); // Level 3 (lowest)

const perParseErrorMap = (issue: ZodIssue) => "Per-parse error"; // Level 2

const FieldSchema = z.string({ error: "Schema-level error" }); // Level 1 (highest)

// Parsing with per-parse error map (rarely needed):
FieldSchema.parse(123, { errorMap: perParseErrorMap });
// Level 1 wins: "Schema-level error"

// Without schema-level error:
z.string().parse(123, { errorMap: perParseErrorMap });
// Level 2 wins: "Per-parse error"

// Without either:
z.string().parse(123);
// Level 3 wins: "Global fallback"

// Without any custom config:
// Zod's built-in message: "Expected string, received number"
```

## Error Handling Pattern for Express/Fastify

```typescript
// Error handler middleware that processes ZodErrors gracefully
function handleZodError(err: unknown, req: Request, res: Response, next: NextFunction) {
  if (err instanceof z.ZodError) {
    return res.status(400).json({
      status: "error",
      message: "Validation failed",
      errors: z.flattenError(err).fieldErrors,
    });
  }
  next(err);
}

// Usage in route
app.post("/users", async (req, res, next) => {
  try {
    const body = CreateUserSchema.parse(req.body);
    // ... process body
  } catch (err) {
    next(err); // ZodError flows to handleZodError middleware
  }
});

// Or with safeParse (preferred — no try/catch overhead)
app.post("/users", async (req, res) => {
  const result = CreateUserSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({
      status: "error",
      errors: z.flattenError(result.error).fieldErrors,
    });
  }
  // process result.data
});
```
