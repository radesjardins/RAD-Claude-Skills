---
name: fastify-best-practices
description: >
  This skill should be used when working on any Fastify project or when the user asks about
  Fastify best practices, conventions, or patterns. Trigger when: working on a Fastify project,
  creating Fastify plugins, registering routes, using decorators, organizing Fastify application
  structure, using @fastify/autoload, creating encapsulated contexts, working with fastify-plugin,
  building Fastify APIs, configuring Fastify server options, using the register API, understanding
  Fastify encapsulation, project scaffolding with fastify-cli
---

# Fastify: Core Architecture & Best Practices

## Core Mental Model — The Plugin Tree

Understand that a Fastify application is a **directed acyclic graph (DAG) of encapsulated contexts**, not a flat middleware chain. Every call to `fastify.register()` creates a new child node in this tree. The root Fastify instance is the only context that is not itself a plugin.

The DAG is managed internally by the `avvio` library. Avvio guarantees deterministic, async loading in the exact order plugins are registered. Never rely on timing assumptions — rely on registration order.

Plugins signal readiness in exactly one of two ways: by returning a Promise, or by calling the `done` callback. Never mix both in the same plugin. If the plugin function is `async`, never accept or call `done` — Fastify will await the returned Promise. If the function is synchronous, call `done()` when setup is complete.

```js
// CORRECT: async plugin — no done parameter
module.exports = async function myPlugin(fastify, opts) {
  // setup logic
}

// CORRECT: callback plugin — call done explicitly
module.exports = function myPlugin(fastify, opts, done) {
  // setup logic
  done()
}

// WRONG: mixing async and done — causes hangs or double-resolution
module.exports = async function myPlugin(fastify, opts, done) {
  await someSetup()
  done() // BUG: never do this in an async function
}
```

## Encapsulation Rules — Hard Invariants

These five rules are non-negotiable. Every architectural decision in Fastify flows from them:

1. **Child inherits everything from parent and ancestors.** A plugin registered inside another plugin sees all decorators, hooks, and parsers from its parent chain up to root.

2. **Siblings are completely isolated.** Two plugins registered at the same level share nothing with each other. Plugin A cannot see Plugin B's decorators, routes, or hooks, even if they are registered on the same parent.

3. **Parents cannot access child entities.** A parent context never sees decorators, hooks, or routes added by its children. Data flows downward only.

4. **`fastify-plugin` elevates contents to the parent scope.** Wrapping a plugin with `require('fastify-plugin')(fn)` breaks encapsulation intentionally — the plugin's decorators, hooks, and parsers are applied to the parent context instead of a new child context. Use this deliberately for shared infrastructure (database connections, authentication strategies, custom parsers). Never use it for route plugins.

5. **`onClose` hooks execute in reverse registration order.** The last plugin registered closes first. Use this for teardown sequences where database connections must close before the connection pool shuts down.

When deciding whether to use `fastify-plugin`, apply this test: "Does this plugin provide shared infrastructure that multiple sibling plugins need?" If yes, wrap it. If it defines routes or feature-specific logic, do not wrap it.

```js
// Shared DB connection — WRAP with fastify-plugin
const fp = require('fastify-plugin')
module.exports = fp(async function dbPlugin(fastify, opts) {
  const pool = await createPool(opts.connectionString)
  fastify.decorate('db', pool)
  fastify.addHook('onClose', async () => pool.end())
})

// Feature routes — DO NOT wrap
module.exports = async function billingRoutes(fastify, opts) {
  // fastify.db is available here via inheritance
  fastify.get('/invoices', async (request, reply) => {
    return fastify.db.query('SELECT * FROM invoices')
  })
}
```

## Project Organization

Structure projects by feature, not by layer. Use these top-level directories:

```
src/
  plugins/       # Shared infrastructure (db, auth, config) — wrapped with fastify-plugin
  routes/        # Feature route plugins — NOT wrapped, auto-loaded with prefixes
    billing/
      index.js   # Routes for /billing
    users/
      index.js   # Routes for /users
  schemas/       # JSON Schema definitions for validation and serialization
  hooks/         # Application-wide hooks (if needed beyond plugin-level hooks)
  app.js         # Build function — exports configured Fastify instance
  server.js      # Entry point — calls app.js then listen()
```

Always separate the server build function from the listen call. Export a `build` or `init` function from `app.js` that configures and returns the Fastify instance without calling `listen`. The `server.js` entry point imports `build`, calls it, then calls `listen`. This separation is critical for testing — tests import `build` and use `fastify.inject()` without binding to a port.

```js
// app.js
const autoload = require('@fastify/autoload')
const path = require('path')

module.exports = async function build(opts = {}) {
  const app = require('fastify')(opts)

  // Register shared plugins first
  app.register(autoload, {
    dir: path.join(__dirname, 'plugins'),
    options: opts
  })

  // Register routes second — they inherit from plugins above
  app.register(autoload, {
    dir: path.join(__dirname, 'routes'),
    options: opts
  })

  return app
}

// server.js
const build = require('./app')

async function start() {
  const app = await build({ logger: true })
  await app.listen({ port: 3000, host: '0.0.0.0' })
}
start()
```

Use `@fastify/autoload` to scan directories and register each file as a plugin automatically. Autoload respects directory structure for route prefixes — a file at `routes/billing/index.js` gets the prefix `/billing`. Configure autoload with `dirNameRoutePrefix: true` to enable this. Autoload registers files in filesystem order within each directory, but all plugins at one level complete before the next directory is processed.

Group routes by feature domain, not by HTTP method. Place all billing-related routes (GET, POST, PUT, DELETE) in `routes/billing/index.js`, not in separate `get.js` or `post.js` files. Use route prefixes for versioning: register the billing plugin with `{ prefix: '/v1/billing' }`.

## Decorator Pattern — Critical for Performance

Use `decorate`, `decorateRequest`, and `decorateReply` to extend Fastify objects. Decorators define the shape of objects before V8 compiles them, enabling hidden class optimization. Adding ad-hoc properties without decorators forces V8 into slow dictionary mode.

**Never use reference types (objects, arrays, Maps, Sets) as the initial value in `decorateRequest` or `decorateReply`.** The initial value is shared across ALL requests on the same instance. Passing an object literal as the default creates a single object that every request mutates — causing cross-request data leaks and memory corruption.

```js
// WRONG — shared mutable reference, security vulnerability
fastify.decorateRequest('user', {})  // Every request shares THIS object

// CORRECT — initialize with null, populate per-request in a hook
fastify.decorateRequest('user', null)
fastify.addHook('onRequest', async (request, reply) => {
  request.user = await authenticate(request)
})
```

Use `null` for objects you will assign later. Use `''` (empty string) for strings. Use `0` for numbers. The key constraint is that the initial value must be a primitive or null so it is copied by value, not shared by reference.

**Never use arrow functions when defining decorator functions.** Arrow functions capture the outer `this`, breaking Fastify's binding. Use regular function declarations or expressions.

```js
// WRONG — arrow function breaks this binding
fastify.decorate('authenticate', async (request) => {
  // `this` is NOT the fastify instance here
})

// CORRECT — regular function preserves this binding
fastify.decorate('authenticate', async function (request) {
  // `this` is the fastify instance
})
```

Duplicate decorator names within the same encapsulation scope throw an immediate exception. Use `fastify.hasDecorator('name')` to check before decorating if your plugin might be registered multiple times. Decorators respect encapsulation — a decorator added in a child scope is invisible to the parent and sibling scopes.

## Route Registration

Always register routes inside encapsulated plugins, never on the root instance directly. This ensures route-specific hooks and decorators do not leak across features.

Use the full route options object for non-trivial routes. Declare route-level hooks in the route config — they execute last in their lifecycle category, after all plugin-level hooks in the encapsulation chain.

```js
module.exports = async function userRoutes(fastify, opts) {
  fastify.route({
    method: 'GET',
    url: '/:id',
    schema: {
      params: {
        type: 'object',
        properties: {
          id: { type: 'string', format: 'uuid' }
        },
        required: ['id']
      },
      response: {
        200: {
          type: 'object',
          properties: {
            id: { type: 'string' },
            name: { type: 'string' },
            email: { type: 'string' }
          }
        }
      }
    },
    preHandler: async function (request, reply) {
      // Route-level hook — runs after all plugin-level preHandler hooks
      await this.authenticate(request)
    },
    handler: async function (request, reply) {
      const user = await this.db.query('SELECT * FROM users WHERE id = $1', [request.params.id])
      return user
    }
  })
}
```

Always define `response` schemas. Fastify uses response schemas for serialization via `fast-json-stringify`, which is 2-5x faster than `JSON.stringify`. Omitting response schemas means falling back to the slow path.

Use route constraints for advanced routing needs: version-based routing with `constraints: { version: '2.0.0' }`, host-based routing with `constraints: { host: 'api.example.com' }`. Constraints are evaluated at route matching time, not at registration time.

## Hooks Lifecycle

Know the exact hook execution order. Hooks run in this sequence for each request:

1. `onRequest` — runs before parsing. Use for authentication, rate limiting.
2. `preParsing` — can modify raw request body stream before parsing.
3. `preValidation` — runs after parsing, before schema validation. Use for body transformation.
4. `preHandler` — runs after validation. Use for authorization, data loading.
5. `preSerialization` — runs before serializing the response payload. Use for response transformation.
6. `onSend` — runs after serialization, before sending. Use for setting headers, compression.
7. `onResponse` — runs after the response is sent. Use for logging, metrics.
8. `onError` — runs when an error is thrown during the request lifecycle.

Within each hook category, execution order is: ancestor hooks first (from root down to current scope), then plugin-level hooks in registration order, then route-level hooks last. This ordering is deterministic and cannot be changed.

To short-circuit the request lifecycle from any hook, call `reply.send()` and return. Do not throw errors to abort — use `reply.code(403).send({ error: 'Forbidden' })`.

## Logging

Always enable the built-in Pino logger by passing `{ logger: true }` to the Fastify constructor. Never install Pino separately or create your own logger instance — Fastify's integrated logger provides request-scoped logging with automatic request ID tracking.

Use `request.log` inside route handlers and hooks, not `fastify.log`. The `request.log` instance includes the request ID automatically, making log correlation trivial.

```js
fastify.get('/users/:id', async function (request, reply) {
  request.log.info({ userId: request.params.id }, 'fetching user')
  // NOT: fastify.log.info(...)
})
```

Set the log level per route when needed by adding `logLevel: 'warn'` to the route options. This suppresses noisy info-level logs for health check endpoints without affecting the rest of the application.

## Error Handling

Use `fastify.setErrorHandler()` to define a centralized error handler within an encapsulation scope. Error handlers respect encapsulation — a child scope's error handler overrides the parent's for routes within that scope.

Always set explicit status codes on errors. Use the `@fastify/sensible` plugin for standardized HTTP errors with `reply.notFound()`, `reply.badRequest()`, etc. Alternatively, throw errors with a `statusCode` property: `const err = new Error('Not found'); err.statusCode = 404; throw err`.

Never send raw error stacks in production. Fastify automatically strips stack traces when `NODE_ENV=production` for 500 errors, but always define explicit error responses for expected errors.

## Validation and Serialization

Use JSON Schema for all input validation (params, querystring, body, headers) and output serialization. Define schemas as standalone objects in a `schemas/` directory and reference them via `$ref` using `fastify.addSchema()`.

```js
// schemas/user.js
const userSchema = {
  $id: 'user',
  type: 'object',
  properties: {
    id: { type: 'string', format: 'uuid' },
    name: { type: 'string', minLength: 1, maxLength: 255 },
    email: { type: 'string', format: 'email' }
  },
  required: ['id', 'name', 'email']
}

// In a plugin
fastify.addSchema(userSchema)

// In a route — reference by $ref
{
  schema: {
    response: {
      200: { $ref: 'user#' }
    }
  }
}
```

Prefer `ajv` (Fastify's default) for validation. Use `@fastify/type-provider-typebox` or `@fastify/type-provider-zod` if you need TypeScript type inference from schemas. Never disable validation in production.

## Testing

Always use `fastify.inject()` for testing. Inject sends a simulated HTTP request through the full Fastify lifecycle without opening a network socket. Import the `build` function, create an instance, and inject requests.

```js
const build = require('./app')

test('GET /users/:id returns user', async () => {
  const app = await build()
  const response = await app.inject({
    method: 'GET',
    url: '/users/abc-123'
  })
  assert.strictEqual(response.statusCode, 200)
  assert.strictEqual(response.json().id, 'abc-123')
  await app.close()
})
```

Always call `app.close()` after each test to trigger `onClose` hooks and clean up resources. Never call `app.listen()` in tests unless you are specifically testing network behavior.

## TypeScript Integration

When using TypeScript, always use a type provider for end-to-end type safety from schema to handler. Install `@fastify/type-provider-typebox` and define schemas with `Type.Object()` from `@sinclair/typebox`. The route handler parameters are automatically typed from the schema.

```ts
import Fastify from 'fastify'
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox'
import { Type } from '@sinclair/typebox'

const app = Fastify().withTypeProvider<TypeBoxTypeProvider>()

app.get('/users/:id', {
  schema: {
    params: Type.Object({
      id: Type.String({ format: 'uuid' })
    }),
    response: {
      200: Type.Object({
        id: Type.String(),
        name: Type.String()
      })
    }
  }
}, async (request, reply) => {
  // request.params.id is typed as string
  return { id: request.params.id, name: 'Alice' }
})
```

Declare custom decorator types using module augmentation on `FastifyInstance`, `FastifyRequest`, and `FastifyReply` interfaces to get full IntelliSense across your codebase.

## Common Anti-Patterns to Avoid

- **Registering routes on the root instance.** Always wrap routes in a plugin passed to `register`.
- **Using `fastify-plugin` on route plugins.** This leaks route hooks and decorators to siblings.
- **Calling `listen` inside `app.js`.** Breaks testability. Separate build from listen.
- **Adding properties to `request` without `decorateRequest`.** Defeats V8 optimization.
- **Using middleware instead of hooks.** Fastify supports Express middleware via `@fastify/middie`, but native hooks are faster and more predictable. Prefer hooks.
- **Ignoring response schemas.** Missing serialization schemas fall back to slow `JSON.stringify`.
- **Calling `done` in an async plugin.** Causes double-resolution bugs or silent hangs.
- **Sharing mutable state via decorator defaults.** Use null + per-request hook initialization.
