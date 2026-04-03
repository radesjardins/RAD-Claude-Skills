# Zod Attack Scenarios and Fixes

## Scenario 1: Mass Assignment (Over-Posting) Attack

**Setup:** A user registration endpoint that uses `z.object()` — vulnerable to role escalation.

```typescript
// VULNERABLE
const RegisterSchema = z.object({
  email: z.email(),
  password: z.string().min(8),
  // "role" not defined — z.object() will strip it, but...
});

app.post("/register", async (req, res) => {
  const body = RegisterSchema.parse(req.body);
  // POST { email: "...", password: "...", role: "admin" }
  // After parse: { email: "...", password: "..." } — "role" stripped ✓

  // BUT if the developer used req.body directly for the DB call (common mistake):
  await db.users.create({ ...body, ...req.body }); // role: "admin" sneaks through!

  // Or if the ORM accepts unknown fields and stores them:
  await User.create(body); // Depends on ORM behavior
});
```

**Attack:** `POST /register { "email": "attacker@x.com", "password": "pass", "role": "admin" }`

**Fix:**
```typescript
// SECURE: z.strictObject rejects the request outright before any processing
const RegisterSchema = z.strictObject({
  email: z.email(),
  password: z.string().min(8),
  // Any additional fields → 400 Bad Request
});
// POST with "role": "admin" → ZodError: unrecognized_keys → 400 returned immediately
```

## Scenario 2: PATCH Endpoint Data Loss

**Setup:** Reusing a creation schema for partial updates in Zod 4.

```typescript
// VULNERABLE
const UserSchema = z.object({
  name: z.string(),
  role: z.enum(["admin", "user"]).default("user"),
  bio: z.string().default(""),
  isActive: z.boolean().default(true),
});

app.patch("/users/:id", async (req, res) => {
  // Request: PATCH /users/123 { "name": "New Name" }
  const body = UserSchema.partial().parse(req.body);
  // Expected: { name: "New Name" }
  // Actual:   { name: "New Name", role: "user", bio: "", isActive: true }
  // ← defaults injected for missing fields!

  await db.users.update({ where: { id: req.params.id }, data: body });
  // Overwrites role, bio, and isActive with defaults!
});
```

**Impact:** User's existing role, bio, and active status silently reset to defaults.

**Fix:**
```typescript
// SECURE: Dedicated PATCH schema with no defaults
const PatchUserSchema = z.strictObject({
  name: z.string().optional(),
  bio: z.string().optional(),
  // role and isActive intentionally excluded from self-service PATCH
});

app.patch("/users/:id", async (req, res) => {
  const body = PatchUserSchema.parse(req.body);
  // { name: "New Name" } — only the provided field

  // Update only the provided fields
  const updates = Object.fromEntries(
    Object.entries(body).filter(([, v]) => v !== undefined)
  );
  await db.users.update({ where: { id: req.params.id }, data: updates });
});
```

## Scenario 3: Coercion Confusion

**Setup:** Numeric ID parameter accepted via coercion without constraints.

```typescript
// VULNERABLE
const ParamSchema = z.object({
  id: z.coerce.number(),
});

app.get("/users/:id", async (req, res) => {
  const { id } = ParamSchema.parse(req.params);
  // GET /users/0xff → id = 255 (hex string parsed!)
  // GET /users/1e300 → id = Infinity!
  // GET /users/NaN  → id = NaN (isNaN check bypassed — typeof NaN === "number")

  const user = await db.users.findById(id); // Unpredictable behavior
});
```

**Fix:**
```typescript
// SECURE: Constrain input, validate result
const ParamSchema = z.object({
  id: z.string()
    .regex(/^\d+$/, "ID must be a positive integer")
    .pipe(z.coerce.number().int().positive().finite()),
});
// GET /users/0xff → 400 (fails regex)
// GET /users/1e300 → 400 (fails regex)
// GET /users/0 → 400 (fails .positive())
```

## Scenario 4: PII Leakage via reportInput

**Setup:** `reportInput: true` accidentally committed to production config.

```typescript
// VULNERABLE — in production config
z.config({ reportInput: true });

const LoginSchema = z.object({
  email: z.email(),
  password: z.string().min(8),
});

app.post("/login", async (req, res) => {
  const result = LoginSchema.safeParse(req.body);
  if (!result.success) {
    // result.error.issues[0].input === { email: "...", password: "hunter2" }
    logger.error("Validation failed", result.error.issues); // ← logs password!
    return res.status(400).json(z.flattenError(result.error));
  }
});
```

**Impact:** Passwords, tokens, and PII logged to your logging platform.

**Fix:**
```typescript
// Remove reportInput from production config
// Only enable in development behind NODE_ENV guard:
if (process.env.NODE_ENV === "development") {
  z.config({ reportInput: true });
}
```

## Scenario 5: z.custom() Validation Bypass

**Setup:** A schema using `z.custom()` without a validator for a custom type.

```typescript
// VULNERABLE — accepts any value
const FileSchema = z.object({
  avatar: z.custom<File>(), // No predicate — accepts anything
});

// Attacker sends: { "avatar": { "malicious": "payload" } }
// Zod accepts it as "File" — type cast unsound at runtime
const { avatar } = FileSchema.parse(req.body);
avatar.arrayBuffer(); // Throws: avatar.arrayBuffer is not a function
```

**Fix:**
```typescript
// SECURE: Validate with Zod 4's built-in file schema
const FileSchema = z.object({
  avatar: z.file().max(5 * 1024 * 1024).type("image/jpeg", "image/png"),
});

// Or with custom() when instanceof check is needed
const FileSchema = z.object({
  avatar: z.custom<File>(val => val instanceof File && val.size > 0),
});
```
