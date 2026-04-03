---
name: fastify-schemas-validation
description: >
  This skill should be used when writing Fastify JSON schemas, configuring Ajv validation, using fast-json-stringify serialization, defining request body/querystring/params/headers schemas, sharing schemas with addSchema and $ref, using fluent-json-schema, configuring response schemas, handling validation errors, setting up custom validators, working with Fastify schema design, coercion issues, nullable types, or allErrors configuration.
---

# Fastify Schemas, Validation & Serialization

## Core Philosophy: Schema-First

Fastify rejects implicit behavior. You MUST define explicit JSON Schema contracts for ALL routes. Schemas are not optional documentation — they are the mechanism that unlocks pre-compiled validation via Ajv and JIT serialization via fast-json-stringify. Never execute business logic on unknown or invalid data. Fail fast: if a request does not match the contract, reject it before it reaches your handler.

Every route you write must have schemas defined for both request validation and response serialization. Treat schema omission as a bug, not a convenience tradeoff.

## Request Validation with Ajv

### Schema Locations

You can attach validation schemas to four locations on a route:

- **`body`** — Use for POST, PUT, and PATCH request bodies. This is the most common validation target. Define the shape of the incoming JSON payload here.
- **`querystring`** (or the alias `query`) — Use for URL query parameters. Define expected parameter names, types, and constraints. Remember that all query values arrive as strings, so rely on Ajv coercion or define types accordingly.
- **`params`** — Use for URL path parameters (e.g., `/users/:id`). Always define the expected type. A common pattern is `{ type: 'object', properties: { id: { type: 'integer' } }, required: ['id'] }`.
- **`headers`** — Use for request headers. This is rarely needed, but useful when you must enforce a specific header value or presence (e.g., `X-API-Key`). Remember that header names are lowercased by Node.js.

### How Validation Works Internally

Schemas are compiled into optimized JavaScript functions at startup, not at request time. This means the first request is fast — there is no cold-start penalty per route. Ajv automatically coerces types when the schema specifies a type that differs from the incoming value. For example, the string `"42"` becomes the number `42` when the schema declares `type: "number"`. This coercion is enabled by default in Fastify's Ajv configuration.

Validation is only attempted for requests with `Content-Type: application/json` by default. If you register custom content-type parsers, the body is validated ONLY if the schema includes a `content` property that maps the MIME type. If you forget this mapping, validation is silently skipped.

### Hard Rules for Request Validation

- **NEVER pass user-provided schemas to Fastify.** Ajv validation internally uses `new Function()` to compile schemas into validators. If a user can control the schema definition, they can achieve arbitrary code execution on your server. Always define schemas statically in your codebase.

- **NEVER use Ajv `$async` validators to perform database lookups during validation.** This opens a denial-of-service vector — an attacker can flood your validation layer with requests that each trigger expensive database queries. Perform data-existence checks in a `preHandler` hook instead.

- **Keep `allErrors: false` (the default) in production.** Setting `allErrors: true` forces the validator to continue checking all constraints even after the first failure. An attacker can craft payloads with many intentional violations against complex schemas, causing the validator to do excessive work. Reserve `allErrors: true` for development environments only.

- **NEVER use `anyOf` for nullable primitives when type coercion is enabled.** The values `0` and `false` may coerce to `null` unexpectedly when you write `anyOf: [{ type: 'string' }, { type: 'null' }]`. Use the `nullable` keyword instead: `{ type: 'string', nullable: true }`.

- **Custom async validators MUST return `{error}` objects, not throw.** If a custom validator throws an exception, it causes an unhandled promise rejection that crashes the process. Always return an error object from custom validation functions.

### Configuring a Custom Ajv Instance

When you need to customize Ajv behavior, pass your configuration through Fastify's `ajv` option at server instantiation. Do not create a standalone Ajv instance and try to wire it in manually. Use the `customOptions` property to set Ajv options and `plugins` to add Ajv plugins:

```js
const fastify = require('fastify')({
  ajv: {
    customOptions: {
      removeAdditional: 'all',
      coerceTypes: true,
      useDefaults: true
    },
    plugins: [require('ajv-formats')]
  }
})
```

Set `removeAdditional: 'all'` to strip unknown properties from incoming payloads — this prevents unexpected data from reaching your handlers. Set `useDefaults: true` to let Ajv fill in default values declared in schemas.

## Shared Schemas with addSchema and $ref

### Registering Reusable Schemas

Use `fastify.addSchema()` to register reusable schemas at the application level. Every schema you register must have a `$id` property. Define domain objects like User, Product, or Address once, then reference them everywhere:

```js
fastify.addSchema({
  $id: 'User',
  type: 'object',
  properties: {
    id: { type: 'integer' },
    name: { type: 'string' },
    email: { type: 'string', format: 'email' }
  },
  required: ['id', 'name', 'email']
})
```

### Referencing Shared Schemas

Reference registered schemas using the `$ref` keyword with the schema's `$id`. Fastify resolves these references at compile time, so there is no runtime cost:

```js
fastify.post('/users', {
  schema: {
    body: { $ref: 'User#' },
    response: {
      201: { $ref: 'User#' }
    }
  }
}, handler)
```

You can also reference nested properties within a shared schema using JSON Pointer syntax: `{ $ref: 'User#/properties/email' }`.

### Using fluent-json-schema

The `fluent-json-schema` library provides a programmatic, chainable API to construct and extend JSON schemas. Use it when schemas become complex or when you want to compose schemas from reusable fragments:

```js
const S = require('fluent-json-schema')

const userSchema = S.object()
  .prop('id', S.integer().required())
  .prop('name', S.string().required())
  .prop('email', S.string().format('email').required())

fastify.addSchema(userSchema.id('User').valueOf())
```

Prefer fluent-json-schema over hand-written JSON Schema objects when your schemas exceed ~15 properties or involve conditional logic. It prevents typos and provides IDE autocompletion.

## Response Serialization with fast-json-stringify

### How Serialization Works

Fastify bypasses `JSON.stringify()` for response serialization when you define response schemas. Instead, it uses `fast-json-stringify` to JIT-compile your schema into an optimized serialization function at startup. This yields 2-3x faster serialization compared to native `JSON.stringify()`.

### Defining Response Schemas

Define output schemas per status code. Use the status code number or category as the key:

```js
fastify.get('/users/:id', {
  schema: {
    params: { type: 'object', properties: { id: { type: 'integer' } } },
    response: {
      200: {
        type: 'object',
        properties: {
          id: { type: 'integer' },
          name: { type: 'string' }
        }
      },
      '4xx': {
        type: 'object',
        properties: {
          error: { type: 'string' },
          message: { type: 'string' }
        }
      }
    }
  }
}, handler)
```

You can use `2xx`, `3xx`, `4xx`, `5xx`, or `default` as catch-all keys for status code ranges.

### Rules for Response Schemas

- **ALWAYS define response schemas for performance.** Without them, Fastify falls back to the slow native `JSON.stringify()`. Response schemas also act as a security boundary — they strip any properties not declared in the schema, preventing accidental data leaks (e.g., password hashes, internal IDs).

- Response schemas can be defined globally (via a plugin), per-route, or per-status-code. Prefer per-route schemas for clarity.

- Use `reply.serializer(fn)` to override serialization for specific routes that need custom behavior (e.g., streaming responses, binary data). Only use this escape hatch when the default fast-json-stringify pipeline cannot handle your use case.

### Edge Cases You Must Handle

- **Stream error Content-Type mismatch:** If a route outputs a stream with `text/plain` but the error handler returns JSON, you MUST explicitly set `Content-Type: application/json` in the error handler. Otherwise, the client receives JSON with a `text/plain` Content-Type header, and many clients will fail to parse it. This produces a hard 500 error in some configurations.

- **Custom content-type parser regex mismatch:** If you register a custom content-type parser with a regex (e.g., `/^application\/.*json$/`), every MIME type that matches that regex MUST appear in the schema's `content` map. Any matched type that is missing from the `content` map bypasses validation entirely — the body arrives un-validated in your handler with no warning.

## Validation Error Handling

### Default Behavior

When a schema validation fails, Fastify returns a `400 Bad Request` response with a structured error body. The default format includes `statusCode`, `error`, `message`, and `validation` fields. The `validation` array contains the specific Ajv error details.

### Customizing Error Responses

Use `schemaErrorFormatter` to customize the error format at the Fastify instance or route level:

```js
const fastify = require('fastify')({
  schemaErrorFormatter: (errors, dataVar) => {
    return new Error(`Validation failed: ${errors.map(e => e.message).join(', ')}`)
  }
})
```

Alternatively, use `setErrorHandler` to catch validation errors alongside other errors:

```js
fastify.setErrorHandler((error, request, reply) => {
  if (error.validation) {
    reply.status(400).send({
      error: 'Validation Error',
      details: error.validation
    })
    return
  }
  reply.status(500).send({ error: 'Internal Server Error' })
})
```

### Production Error Handling Rules

- **Return minimal error information in production.** Never expose full Ajv error details to external clients — they reveal your internal schema structure and can aid attackers in crafting bypass payloads. Log the full error server-side and return a generic message to the client.

- **Differentiate validation errors from other 400 errors.** Check `error.validation` to determine whether the error originated from schema validation. This lets you return appropriate error formats for different failure modes.

- **Never trust that validation errors are safe to display.** Ajv error messages can contain fragments of the incoming data. If a user submits malicious content in a field and your error handler echoes the Ajv message, you may expose yourself to reflected XSS in non-browser clients or log injection attacks.

## Common Pitfalls and How to Avoid Them

- **Forgetting to define `querystring` schema types as strings:** Query parameters always arrive as strings. If your schema says `type: 'integer'` without Ajv coercion enabled, validation fails on every request. Either enable coercion (the default) or declare types as `string` and parse manually.

- **Using `additionalProperties: false` without listing all properties:** If you set `additionalProperties: false` but forget to declare a property in `properties`, that property is silently stripped from the validated object. Audit your schemas carefully when using this option.

- **Confusing `nullable` with `type: ['string', 'null']`:** In JSON Schema draft-07 (which Fastify uses by default), `nullable: true` is the correct way to allow null values. The array syntax `type: ['string', 'null']` works in draft-04 but behaves inconsistently with Ajv coercion in Fastify's configuration.

- **Not testing schemas in isolation:** Use Ajv directly in unit tests to verify your schemas accept valid data and reject invalid data before integrating them into routes. This catches schema bugs faster than end-to-end testing.
