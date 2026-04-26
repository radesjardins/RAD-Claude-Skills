# Zod Error Formatting: Complete Reference

## ZodError Issue Structure

Each issue in `error.issues` contains:

```typescript
interface ZodIssue {
  code: ZodIssueCode;       // Machine-readable type (see codes below)
  path: (string | number)[]; // Path to the invalid field
  message: string;           // Human-readable message
  // Additional fields depending on code:
  expected?: string;         // For invalid_type
  received?: string;         // For invalid_type
  minimum?: number;          // For too_small
  maximum?: number;          // For too_big
  keys?: string[];           // For unrecognized_keys
  options?: Primitive[];     // For invalid_enum_value
}
```

### ZodIssueCodes

| Code | Triggered By |
|---|---|
| `invalid_type` | Wrong primitive type (string received number, etc.) |
| `too_small` | `.min()`, `.length()`, `.nonempty()` violations |
| `too_big` | `.max()`, `.length()` violations |
| `invalid_string` | `.email()`, `.url()`, `.uuid()`, `.regex()` failures |
| `invalid_enum_value` | Value not in `.enum()` options |
| `unrecognized_keys` | Extra keys in `z.strictObject()` |
| `custom` | `.refine()` / `.check()` failures |
| `invalid_union` | None of the union options matched |
| `invalid_discriminator_value` | Discriminator key not in discriminated union options |

## `z.treeifyError()` — Nested Form Errors

Converts `ZodError` into a nested object mirroring the schema shape:

```typescript
const OrderSchema = z.object({
  customerId: z.string().uuid(),
  items: z.array(z.object({
    productId: z.string(),
    quantity: z.number().int().positive(),
    price: z.number().positive(),
  })),
  shipping: z.object({
    address: z.object({
      street: z.string(),
      city: z.string(),
      zip: z.string().regex(/^\d{5}$/, "Invalid ZIP"),
    }),
    method: z.enum(["standard", "express", "overnight"]),
  }),
});

const badOrder = {
  customerId: "not-a-uuid",
  items: [{ productId: "p1", quantity: -1, price: 0 }],
  shipping: { address: { street: "123 Main", city: "NYC", zip: "bad" }, method: "teleport" }
};

const result = OrderSchema.safeParse(badOrder);
if (!result.success) {
  const tree = z.treeifyError<typeof OrderSchema>(result.error);
  /*
  tree = {
    properties: {
      customerId: { errors: ["Invalid UUID"] },
      items: {
        items: [{
          properties: {
            quantity: { errors: ["Number must be greater than 0"] },
            price: { errors: ["Number must be greater than 0"] }
          }
        }]
      },
      shipping: {
        properties: {
          address: {
            properties: {
              zip: { errors: ["Invalid ZIP"] }
            }
          },
          method: { errors: ["Invalid enum value. Expected 'standard' | 'express' | 'overnight'"] }
        }
      }
    }
  }
  */
}
```

Usage in React with React Hook Form (when not using zodResolver):
```typescript
// Map treeified errors to form error state
const errors = z.treeifyError<typeof FormSchema>(zodError);
setError("shipping.address.zip", { message: errors.properties?.shipping?.properties?.address?.properties?.zip?.errors?.[0] });
```

## `z.flattenError()` — Simple API Responses

Best for flat schemas (one level deep). Groups errors into form-level and field-level:

```typescript
const LoginSchema = z.object({
  email: z.email(),
  password: z.string().min(8),
});

const result = LoginSchema.safeParse({ email: "bad", password: "short" });
if (!result.success) {
  const flat = z.flattenError(result.error);
  /*
  {
    formErrors: [],                         // Top-level errors (from .refine() on the whole object)
    fieldErrors: {
      email: ["Invalid email address"],
      password: ["String must contain at least 8 character(s)"]
    }
  }
  */
}
```

For cross-field validation errors (from `.refine()` on the object), they appear in `formErrors`:

```typescript
const PasswordChangeSchema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string(),
}).refine(d => d.password === d.confirmPassword, {
  message: "Passwords don't match",
  path: [], // No specific field — goes to formErrors
});

const flat = z.flattenError(result.error);
// { formErrors: ["Passwords don't match"], fieldErrors: {} }
```

## `z.prettifyError()` — Development Logging

Multi-line formatted string for logs and CLI output:

```typescript
const result = ComplexSchema.safeParse(badData);
if (!result.success) {
  console.error(z.prettifyError(result.error));
  /*
  ✗ customerId: Invalid UUID
  ✗ items[0].quantity: Number must be greater than 0
  ✗ items[0].price: Number must be greater than 0
  ✗ shipping.address.zip: Invalid ZIP
  ✗ shipping.method: Invalid enum value
  */
}
```

## Accessing Issues Programmatically

For custom error handling (e.g., mapping errors to a specific response format):

```typescript
function zodErrorToApiErrors(error: z.ZodError) {
  return error.issues.map(issue => ({
    field: issue.path.join("."),
    code: issue.code,
    message: issue.message,
  }));
}

// Returns:
// [
//   { field: "email", code: "invalid_string", message: "Invalid email" },
//   { field: "shipping.address.zip", code: "invalid_string", message: "Invalid ZIP" }
// ]
```

## Error Formatting for Different Consumers

| Consumer | Format | Function |
|---|---|---|
| Server log / debugging | Multi-line human string | `z.prettifyError()` |
| REST API client | `{ fieldErrors: { field: string[] } }` | `z.flattenError()` |
| Complex nested form | Nested object mirroring schema | `z.treeifyError()` |
| Custom format | Raw issues array | `error.issues` |
| Type-safe programmatic | Per-issue handling | `error.issues.forEach()` |
