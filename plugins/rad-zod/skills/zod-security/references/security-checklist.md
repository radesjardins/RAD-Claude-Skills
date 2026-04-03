# Zod Security Review Checklist

A comprehensive checklist for reviewing TypeScript code that uses Zod for validation.

## 1. Boundary Coverage

**Finding:** Validation missing at system entry points.

**Check every entry point:**
- [ ] HTTP request bodies validated with Zod before processing
- [ ] URL query parameters parsed and validated (not accessed as raw strings)
- [ ] Path parameters validated (especially IDs — use `.uuid()` or appropriate format)
- [ ] HTTP response data from external APIs validated before use
- [ ] Environment variables validated at startup (before app logic runs)
- [ ] Message queue / event payloads validated at consumer entry
- [ ] File upload contents validated (type, size) before processing
- [ ] Database results validated when schema may have diverged from TypeScript types
- [ ] WebSocket messages validated on receipt

**Red flag:** `const body = req.body as UserType` — unsafe cast without parsing.

## 2. Object Strictness at Boundaries

**Finding:** Using `z.object()` instead of `z.strictObject()` at external-facing endpoints allows mass assignment (over-posting) patterns.

**Check:**
- [ ] All POST/PUT/PATCH body schemas at public API endpoints use `z.strictObject()`
- [ ] No `.passthrough()` on schemas that receive untrusted input
- [ ] No `z.looseObject()` at API entry points

**Exceptions (document them):**
- `z.object()` (strip mode) is correct for internal reshaping and response schema outbound
- `.passthrough()` is correct only when explicitly proxying opaque data you don't own

## 3. Custom Validators

**Finding:** `z.custom()` without a validator is equivalent to `z.unknown()` — no validation occurs.

**Check:**
- [ ] Every `z.custom()` has a meaningful predicate function
- [ ] Predicate does not trivially return `true`
- [ ] `z.instanceof()` used for class instances rather than manual `instanceof` in `z.custom()`

```typescript
// RED FLAG — validates nothing
const S = z.custom();
const S = z.custom(() => true);
const S = z.custom<File>(); // No predicate

// CORRECT
const S = z.custom<File>(val => val instanceof File);
```

## 4. PATCH Endpoint Schema Safety

**Finding:** Reusing creation schemas with `.partial()` for PATCH endpoints causes default values to overwrite existing data in Zod 4.

**Check:**
- [ ] PATCH endpoint schemas do not derive from `.partial()` on schemas with `.default()` values
- [ ] PATCH schemas produce `undefined` for omitted fields (not default values)
- [ ] Database update logic ignores `undefined` fields (uses only provided fields)

**Verification:**
```typescript
// If any schema field has .default(), it is NOT safe to use with .partial() for PATCH
const hasDefaults = Object.values(schema.shape).some(
  field => field instanceof z.ZodDefault
);
```

## 5. Coercion Constraints

**Finding:** Unconstrained `z.coerce.*` can produce unexpected values (NaN, Invalid Date, unexpected numeric conversions).

**Check:**
- [ ] `z.coerce.number()` followed by `.finite()` to reject NaN and Infinity
- [ ] `z.coerce.number()` followed by range validation (`.min()`, `.max()`)
- [ ] `z.coerce.date()` followed by `.refine(d => !isNaN(d.getTime()))` for Invalid Date protection
- [ ] `z.coerce.boolean()` not used where `"false"` must be treated as false (it coerces to `true`)
- [ ] Input constrained before coercion via `.pipe()` pattern

```typescript
// VULNERABLE
const AgeSchema = z.coerce.number(); // Accepts NaN, Infinity, hex strings

// SECURE
const AgeSchema = z.string()
  .regex(/^\d+$/, "Must be a whole number")
  .pipe(z.coerce.number().int().min(0).max(150).finite());
```

## 6. Error Exposure

**Finding:** Raw `ZodError` returned to clients exposes internal schema structure.

**Check:**
- [ ] No `res.json(zodError)` or `res.json(result.error)` in API routes
- [ ] Errors sanitized with `z.flattenError()`, `z.treeifyError()`, or custom formatting before sending
- [ ] Error responses include only field names and user-friendly messages
- [ ] Internal error details logged server-side, not included in client responses

## 7. The `reportInput` Flag

**Finding:** `reportInput: true` logs raw user input (including passwords, tokens, PII) in error issues.

**Check:**
- [ ] `reportInput: true` not present in `z.config()` in production code
- [ ] `reportInput` not enabled in any schema-level error configuration
- [ ] If present, is it gated behind `process.env.NODE_ENV === "development"`?

## 8. Schema Location and Hoisting

**Finding:** Schemas defined inside request handlers, render functions, or loops are re-instantiated on every call.

**Check:**
- [ ] All `z.object()`, `z.array()`, `z.union()`, etc. calls at module top level (not inside functions)
- [ ] Schema factory functions that return schemas are called at module scope, not inside handlers

**Exception:** Dynamic schemas where constraints vary per request are acceptable if the base schema is hoisted and only constraints (not the schema structure) are dynamic.

## 9. Async Validation and Race Conditions

**Finding:** Async refinements checking uniqueness in databases can be subject to TOCTOU (time-of-check, time-of-use) race conditions.

**Check:**
- [ ] Async refinements (e.g., "check email not already taken") are not the sole uniqueness enforcement
- [ ] Database-level unique constraints back up any async Zod refinements
- [ ] `parseAsync()` / `safeParseAsync()` used when schema has async `.refine()` calls

## 10. Environment Variable Security

**Finding:** Secrets in environment variables accessed without validation — type mismatch or missing required vars discovered at runtime in production.

**Check:**
- [ ] All `process.env` access is mediated through a validated config object
- [ ] Secret variables (API keys, tokens) validated for minimum length/format
- [ ] Startup fails fast with clear error if required env vars are missing
- [ ] No default values provided for security-critical secrets (force explicit configuration)

```typescript
// BAD: Silent undefined for missing secrets
const apiKey = process.env.STRIPE_SECRET_KEY; // could be undefined

// GOOD: Fail fast at startup
const EnvSchema = z.object({
  STRIPE_SECRET_KEY: z.string().startsWith("sk_").min(40),
  // No .default() for secrets — must be explicitly provided
});
export const env = EnvSchema.parse(process.env); // Throws if STRIPE_SECRET_KEY missing
```
