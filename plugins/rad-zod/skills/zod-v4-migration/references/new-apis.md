# Zod v4 New APIs Reference

## `z.config()` — Global Configuration

Replaces `z.setErrorMap()`. Called once at application initialization:

```typescript
import { z } from "zod";

// Load a built-in locale
import { es } from "zod/locales/es";
z.config(es());

// Custom global error handler
z.config({
  customError: (issue) => {
    if (issue.input === undefined) return "Required";
    if (issue.code === "invalid_type") return `Expected ${issue.expected}`;
    return undefined; // Use Zod's built-in message
  },
});

// Combine locale + custom overrides
z.config({
  ...es(),
  customError: (issue) => {
    // Custom overrides that take precedence over the locale
    if (issue.code === "custom") return issue.message; // Pass custom messages through
    return undefined; // Fall through to locale messages
  },
});
```

## Registries and `.meta()` — Schema Metadata

Registries store metadata about schemas without affecting validation logic:

```typescript
// Global registry (built-in)
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.email(),
}).meta({
  id: "UserSchema",         // Must be globally unique — used by JSON Schema generation
  title: "User",
  description: "A registered user in the system",
  examples: [{ id: "550e8400...", email: "user@example.com" }],
});

// Access metadata
z.globalRegistry.get(UserSchema); // { id: "UserSchema", title: "User", ... }

// Custom typed registry
const UIRegistry = z.registry<{ label: string; placeholder?: string; required?: boolean }>();

const EmailField = z.email();
UIRegistry.add(EmailField, { label: "Email Address", placeholder: "you@example.com", required: true });

UIRegistry.get(EmailField); // { label: "Email Address", placeholder: "...", required: true }
```

### Registry Use Cases

**Dynamic form generation:**
```typescript
function renderField(schema: z.ZodType) {
  const meta = UIRegistry.get(schema);
  if (!meta) return null;
  return `<input placeholder="${meta.placeholder}" ${meta.required ? "required" : ""}>`;
}
```

**OpenAPI / JSON Schema generation:**
```typescript
const jsonSchema = z.toJSONSchema(UserSchema);
// Includes $id, title, description from .meta()
```

### Registry ID Conflict Avoidance

```typescript
// WRONG: ID registered multiple times if function called more than once
function createSchema() {
  return z.string().meta({ id: "my-schema" }); // ❌ Duplicate ID on second call
}

// CORRECT: Static module-level definition
export const MySchema = z.string().meta({ id: "my-schema" }); // ✅ Registered once
```

## `z.toJSONSchema()` — JSON Schema Export

```typescript
const AddressSchema = z.object({
  street: z.string().meta({ description: "Street address line 1" }),
  city: z.string(),
  country: z.string().length(2).meta({ description: "ISO 3166-1 alpha-2 country code" }),
  zip: z.string().regex(/^\d{5}(-\d{4})?$/),
}).meta({ title: "Address", id: "Address" });

const jsonSchema = z.toJSONSchema(AddressSchema);
/*
{
  "$schema": "http://json-schema.org/draft-07/schema",
  "$id": "Address",
  "title": "Address",
  "type": "object",
  "properties": {
    "street": { "type": "string", "description": "Street address line 1" },
    "city": { "type": "string" },
    "country": { "type": "string", "minLength": 2, "maxLength": 2, "description": "..." },
    "zip": { "type": "string", "pattern": "^\\d{5}(-\\d{4})?$" }
  },
  "required": ["street", "city", "country", "zip"]
}
*/
```

## `z.file()` — Browser File Validation

```typescript
// Basic file validation
const AvatarSchema = z.file();

// With constraints
const AvatarSchema = z.file()
  .min(1)                          // Minimum 1 byte (not empty)
  .max(5 * 1024 * 1024)            // Maximum 5MB
  .type("image/jpeg", "image/png", "image/webp"); // Allowed MIME types

const DocumentSchema = z.file()
  .max(10 * 1024 * 1024)           // 10MB max
  .type("application/pdf", "application/msword", "text/plain");

// In a form schema
const UploadFormSchema = z.object({
  title: z.string().min(1).max(100),
  file: z.file().max(10 * 1024 * 1024),
  thumbnail: z.file().type("image/*").optional(),
});
```

## `z.templateLiteral()` — Structured String Schemas

```typescript
// Semantic version string
const SemVerSchema = z.templateLiteral([
  "v",
  z.number().int().min(0), ".",
  z.number().int().min(0), ".",
  z.number().int().min(0),
]);
// Matches: "v1.0.0", "v2.14.3"

// CSS dimension value
const CssDimensionSchema = z.templateLiteral([
  z.number(), z.enum(["px", "em", "rem", "%", "vh", "vw"])
]);
// Matches: "16px", "1.5rem", "100%"

// API route pattern
const UserRouteSchema = z.templateLiteral([
  "/users/", z.string().uuid(), "/posts/", z.string().uuid()
]);
// Matches: "/users/abc123/posts/def456"

// The TypeScript type is a template literal type:
type SemVer = z.infer<typeof SemVerSchema>; // `v${number}.${number}.${number}`
```

## New ISO Date/Time Schemas

```typescript
// ISO 8601 date string (YYYY-MM-DD)
const DateSchema = z.iso.date();
DateSchema.parse("2026-03-29"); // ✅
DateSchema.parse("March 29, 2026"); // ❌

// ISO 8601 datetime string
const DateTimeSchema = z.iso.datetime();
DateTimeSchema.parse("2026-03-29T14:30:00Z"); // ✅
DateTimeSchema.parse("2026-03-29T14:30:00+05:30"); // ✅

// With options
const LocalDateTimeSchema = z.iso.datetime({ offset: true }); // Require offset
const UtcDateTimeSchema = z.iso.datetime({ offset: false }); // Require Z suffix

// ISO 8601 time string (HH:MM:SS)
const TimeSchema = z.iso.time();
TimeSchema.parse("14:30:00"); // ✅

// ISO 8601 duration string (P1Y2M3DT4H5M6S)
const DurationSchema = z.iso.duration();
DurationSchema.parse("P1Y2MT3H"); // ✅
```

## `.safeExtend()` — Extending Refined Schemas

```typescript
const BaseSchema = z.object({ name: z.string() })
  .refine(d => d.name.length > 0, "Name required");

// .extend() would throw — use .safeExtend()
const ExtendedSchema = BaseSchema.safeExtend({ age: z.number() });

// safeExtend also prevents overwriting existing keys with incompatible types:
const S = z.object({ x: z.string() });
S.safeExtend({ x: z.number() }); // ❌ TypeScript error: can't overwrite x with incompatible type
S.safeExtend({ x: z.string().min(1) }); // ✅ Refinement of same type is allowed
```

## `.check()` — Multi-Issue Refinement

```typescript
// .refine() can only add one issue
// .check() can add multiple issues and use custom issue codes

const PasswordSchema = z.string().check((ctx) => {
  const value = ctx.value;
  if (value.length < 12) {
    ctx.issue({ code: "too_small", minimum: 12, type: "string", inclusive: true, message: "Too short" });
  }
  if (!/[A-Z]/.test(value)) {
    ctx.issue({ code: "custom", message: "Must contain an uppercase letter" });
  }
  if (!/[0-9]/.test(value)) {
    ctx.issue({ code: "custom", message: "Must contain a number" });
  }
  if (!/[!@#$%^&*]/.test(value)) {
    ctx.issue({ code: "custom", message: "Must contain a special character" });
  }
  // All failing rules reported in a single parse, not just the first
});
```
