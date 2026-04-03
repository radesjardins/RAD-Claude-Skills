---
name: fastify-testing
description: >
  This skill should be used when testing Fastify applications, using .inject() for HTTP testing, writing Fastify unit tests, testing Fastify plugins in isolation, separating app from server for testing, using light-my-request, testing route handlers, integration testing Fastify, test setup and teardown with Fastify, parallel test execution, testing Fastify hooks, or mocking in Fastify tests.
---

# Fastify Testing Patterns

You are guiding the user through testing Fastify applications. Follow these instructions precisely when generating test code, reviewing test files, or advising on Fastify test architecture.

## Core Principle: In-Process Injection

NEVER bind Fastify to a real TCP port during unit or integration tests. Use the `.inject()` method for all HTTP simulation. Fastify ships with light-my-request built in, so `.inject()` simulates requests entirely in-process with zero network stack overhead. This means dramatically faster execution and no "address in use" port conflicts when running tests in parallel.

When you see test code that calls `app.listen()` or binds to a port, flag it immediately and refactor to use `.inject()` instead.

## App/Server Separation (Non-Negotiable)

ALWAYS separate plugin and route registration from the network listener. Structure every Fastify project with this separation:

- Create an `app.js` (or `app.ts`) that exports a `build()` or `createApp()` function. This function constructs the Fastify instance, registers all plugins and routes, then returns the instance without listening.
- Create a `server.js` (or `server.ts`) that imports `build()`, calls it, and then calls `app.listen()`. This file contains minimal code and is not tested directly.
- The test suite creates fresh, isolated instances per test case by calling `build()`.

When scaffolding a new Fastify project, always apply this pattern from the start. When reviewing existing code that does not follow this pattern, recommend the refactor as a prerequisite to testability.

### Pattern

```javascript
// app.js
const Fastify = require('fastify')

async function build(opts = {}) {
  const app = Fastify(opts)
  app.register(require('./plugins/db'))
  app.register(require('./routes/users'), { prefix: '/api/users' })
  return app
}

module.exports = build

// server.js
const build = require('./app')

const start = async () => {
  const app = await build({ logger: true })
  await app.listen({ port: 3000, host: '0.0.0.0' })
}

start()
```

## Using .inject()

Write all test assertions against `.inject()` responses. Here is the canonical pattern:

```javascript
const build = require('./app')

test('GET /api/users returns 200', async () => {
  const app = await build()
  const response = await app.inject({
    method: 'GET',
    url: '/api/users'
  })
  expect(response.statusCode).toBe(200)
  expect(JSON.parse(response.payload)).toHaveProperty('users')
})
```

### .inject() Features

Use these capabilities when constructing test requests:

- **All HTTP methods**: Pass `method: 'GET'`, `'POST'`, `'PUT'`, `'PATCH'`, `'DELETE'`, `'OPTIONS'`, or `'HEAD'`.
- **Headers**: Pass a `headers` object to set any request headers including `Authorization`, `Content-Type`, and custom headers.
- **Query strings**: Include query parameters directly in the `url` string (e.g., `/api/users?page=2`) or pass a `query` object.
- **Request payloads**: Pass a `payload` object for JSON bodies. Fastify serializes it automatically when `Content-Type` is `application/json`.
- **Cookies**: Set cookies via the `headers` object using the `Cookie` header string.
- **Response object**: The returned response exposes `statusCode`, `headers`, `payload` (raw string), and a `json()` method for parsed JSON.
- **Automatic ready()**: `.inject()` internally calls `ready()` before dispatching, guaranteeing all plugins are loaded. You do not need to call `await app.ready()` before injecting.

## Testing Plugins in Isolation

Create a minimal Fastify instance in your test file and register ONLY the specific plugin under test. Use `.inject()` to verify hooks, routes, and decorators added by that plugin. Fastify's encapsulation model makes this naturally clean because plugins cannot leak side effects into sibling contexts.

```javascript
const Fastify = require('fastify')
const myPlugin = require('./plugins/auth')

test('auth plugin decorates request with user', async () => {
  const app = Fastify()
  app.register(myPlugin)

  app.get('/test', async (request) => {
    return { hasUser: !!request.user }
  })

  const response = await app.inject({
    method: 'GET',
    url: '/test',
    headers: { authorization: 'Bearer valid-token' }
  })

  expect(response.json().hasUser).toBe(true)
})
```

Do not register unrelated plugins in plugin isolation tests. If a plugin depends on another plugin, register only the direct dependency, not the entire application plugin tree.

## Testing Hooks

Register the hook inside a test-scoped plugin or directly on the test instance. Use `.inject()` to trigger the request lifecycle and assert on the response status, headers, or decorated properties.

For `onClose` hooks specifically, call `await app.close()` and verify the cleanup side effect (e.g., database connection closed, file handle released).

```javascript
test('onRequest hook rejects missing API key', async () => {
  const app = Fastify()
  app.addHook('onRequest', async (request, reply) => {
    if (!request.headers['x-api-key']) {
      reply.code(401).send({ error: 'Missing API key' })
    }
  })
  app.get('/secure', async () => ({ ok: true }))

  const response = await app.inject({ method: 'GET', url: '/secure' })
  expect(response.statusCode).toBe(401)
})
```

## Test Setup and Teardown

Follow these rules for every test file:

- **Create a fresh app instance per test** (or per `describe` block if tests within that block are truly independent and share no mutable state). Prefer per-test instances to eliminate any risk of state leakage.
- **Call `app.close()` in `afterEach` or `afterAll`** to release resources such as database connections, file handles, and timers. Failing to close causes resource leaks and hanging test processes.
- Fastify is test-framework agnostic. Use tap, vitest, jest, or node's built-in test runner. Adapt the setup/teardown syntax to the framework in use.

```javascript
let app

beforeEach(async () => {
  app = await build()
})

afterEach(async () => {
  await app.close()
})
```

## Parallel Test Execution

Because `.inject()` never binds to a port, all tests can run in parallel without conflict. When configuring your test runner, enable parallel execution for maximum speed. Each test file creates its own isolated Fastify instance, so there is no shared state across files.

If using vitest, set `test.pool` to `'forks'` or `'threads'`. If using jest, the default worker-based parallelism works out of the box. If using tap, use `--jobs` to control concurrency.

## Common Testing Mistakes

Watch for and correct these anti-patterns:

- **Binding to a real port**: Causes flaky tests, slow execution, and port conflicts in CI. Always use `.inject()`.
- **Sharing an app instance across tests**: Leads to state leakage where one test's side effects contaminate another. Create a fresh instance per test.
- **Not calling `app.close()`**: Causes resource leaks and tests that hang indefinitely. Always close in teardown.
- **Testing implementation details**: Test the HTTP contract (status codes, response bodies, headers), not internal function calls or private state. If you need to verify a decorator was set, expose it through a route response.
- **Mocking Fastify internals**: Do not mock the request lifecycle, reply object, or plugin system. Use `.inject()` to exercise the real code paths. Reserve mocking for external dependencies like databases and third-party APIs.
- **Forgetting `await`**: Both `build()` and `.inject()` return promises. Missing `await` causes tests to pass vacuously.

## Integration Testing

For tests that exercise the full stack including database access:

- Use test containers (e.g., `@testcontainers/postgresql`) or in-memory databases (e.g., SQLite with `:memory:`) to avoid depending on external infrastructure.
- Register real plugins, not mocks, for integration tests. The goal is to verify the real wiring.
- Use `.inject()` even for integration tests. There is no reason to bind to a port.
- Seed the database before each test and clean it after to maintain isolation. Use transactions that roll back, or truncate tables in teardown.

```javascript
beforeEach(async () => {
  app = await build({ logger: false })
  await seedTestData(app)
})

afterEach(async () => {
  await cleanTestData(app)
  await app.close()
})

test('POST /api/users creates a user in the database', async () => {
  const response = await app.inject({
    method: 'POST',
    url: '/api/users',
    payload: { name: 'Alice', email: 'alice@example.com' }
  })
  expect(response.statusCode).toBe(201)
  expect(response.json()).toHaveProperty('id')
})
```
