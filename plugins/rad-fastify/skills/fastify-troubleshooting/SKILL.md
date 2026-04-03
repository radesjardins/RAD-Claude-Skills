---
name: fastify-troubleshooting
description: >
  This skill should be used when debugging Fastify issues, identifying Fastify anti-patterns, diagnosing common Fastify mistakes, performing Fastify error troubleshooting, investigating request.body undefined in hook, fixing decorator shared across requests, resolving hook executing twice, handling reply already sent error, debugging encapsulation not working, fixing schema validation bypassed, diagnosing serialization error 500, handling Fastify crash unhandled rejection, troubleshooting plugin not loading, resolving decorator not found, or diagnosing Fastify performance problems.
---

# Fastify Troubleshooting & Anti-Patterns

You are diagnosing and fixing Fastify issues. Follow these rules strictly. Every section is organized by category with NEVER rules (things you must prevent) and BUG patterns (common mistakes to detect and fix).

## Schema & Validation Issues

### NEVER: Accept User-Provided Schemas

Never allow user-supplied JSON Schema objects to be passed into Fastify route schemas. Fastify's validation and serialization compilers (Ajv and fast-json-stringify) use `new Function()` internally to generate optimized code from schemas. If a user can control the schema definition, they can inject arbitrary JavaScript that executes on the server. Treat this as a CRITICAL security vulnerability with no exceptions. Always hardcode schemas in your route definitions or load them from trusted configuration files that users cannot modify.

### NEVER: Use Ajv $async for Database Lookups

Never use Ajv's `$async` keyword to perform database reads during schema validation. Validation runs on every incoming request before your business logic, and async validators that hit the database open a denial-of-service vector where attackers can flood your validation layer with expensive queries. Move all async business logic validation (uniqueness checks, existence lookups, permission verification) into a `preHandler` hook where you have full control over execution flow, caching, and error handling.

### BUG: anyOf with Nullable Primitives

When type coercion is enabled (which Fastify enables by default), using `anyOf: [{ type: "number" }, { type: "null" }]` causes unexpected coercion behavior. Values like `0` and `false` coerce to `null` instead of being treated as valid numbers or booleans. This happens because Ajv's coercion logic tries each branch of anyOf and null coercion takes precedence for falsy values. Fix this by using the `nullable: true` keyword on the type definition instead of anyOf. Write `{ type: "number", nullable: true }` rather than the anyOf pattern for primitive nullable types.

### BUG: allErrors Denial of Service

When `allErrors: true` is set in the Ajv configuration, Ajv is forced to validate the entire payload and collect every validation error instead of stopping at the first failure. Attackers can craft deeply nested or highly complex payloads that force the validator to traverse the entire structure, causing CPU exhaustion. Keep `allErrors: false` (the default) in production. If you need detailed validation errors for development, enable allErrors only in non-production environments behind an environment check.

### BUG: Custom Async Validator Crashes

Custom async validators that throw exceptions instead of returning an error object cause unhandled promise rejections. In Node.js, unhandled promise rejections crash the process (default behavior since Node.js 15+). This means a single malformed request can bring down your entire server. Always return `{ error: new Error('message') }` from async validators. Never use `throw` inside a custom validator function. Wrap validator logic in try/catch and return the error object from the catch block.

### BUG: Content-Type Parser Bypass

When you register a custom content-type parser with a regex pattern (e.g., `/^application\/vnd\..+\+json$/`), the regex may match content types that are not explicitly listed in your route schema's `content` map. When Fastify matches a content type via the parser but cannot find it in the schema's content map, the body is parsed but validation is SILENTLY BYPASSED. The request proceeds to your handler with an unvalidated body. Fix this by ensuring every content type your parser regex can match is explicitly listed in the schema's content map with its corresponding validation schema.

## Decorator Issues

### NEVER: Use Reference Types in decorateRequest/decorateReply

Never pass a reference type (object, array, Map, Set) as the default value in `fastify.decorateRequest()` or `fastify.decorateReply()`. Writing `fastify.decorateRequest('user', {})` creates ONE object that is shared across ALL concurrent requests. This causes memory leaks, cross-request data leakage, and serious security vulnerabilities where one user's data bleeds into another user's response. Fastify actively blocks this pattern in newer versions and will throw an error. Fix this by initializing with `null` and populating the decorator in an `onRequest` hook:

```javascript
fastify.decorateRequest('user', null)
fastify.addHook('onRequest', async (request) => {
  request.user = {}
})
```

### NEVER: Use Arrow Functions for Decorators

Never use arrow functions when defining decorator methods or when accessing decorators via `this`. Arrow functions capture the `this` binding from their enclosing lexical scope, which means `this` will NOT refer to the Fastify instance, Request, or Reply object. Instead, `this` will be whatever the enclosing scope's `this` is (often `undefined` in strict mode or the module scope). Always use regular function expressions or named functions when you need to access `this` for Fastify decorators.

### BUG: Dynamic Property Addition

Adding properties to request or reply objects at runtime without declaring them as decorators deoptimizes V8's hidden class system. V8 creates hidden classes to track object shapes (the set of properties and their types). When you add a property that was not declared upfront, V8 must create a new hidden class and transition the object, which triggers deoptimization of any compiled code that operated on the old shape. Declare all decorators upfront with `null` values to lock the object shape at startup. Even if you do not know the runtime value, declaring the property with `null` ensures V8 can optimize access patterns.

## Hook Issues

### NEVER: Mix async/await with done Callback

Never define a hook as an async function AND call the `done` callback. If your hook function is async or returns a Promise, Fastify already handles completion via the Promise resolution. Calling `done()` in addition causes the hook chain to advance twice: once when `done()` is called and once when the Promise resolves. Symptoms include hooks running twice, duplicate database operations, unexpected behavior, and double responses that crash with "Reply already sent." Use EITHER async/await OR the done callback pattern, never both in the same hook function.

### BUG: Forgetting `return reply`

In async hooks that intercept the request by calling `reply.send()`, you must end the hook with `return reply`. Without the return statement, Fastify does not know the hook has handled the response. The request continues to the route handler, which also sends a response, causing double execution and a "Reply already sent" error. Always follow this pattern in intercepting hooks:

```javascript
fastify.addHook('preHandler', async (request, reply) => {
  if (!request.user) {
    reply.code(401).send({ error: 'Unauthorized' })
    return reply
  }
})
```

### BUG: Early Body Access

Accessing `request.body` in `onRequest` or `preParsing` hooks always returns `undefined`. Body parsing occurs between the `preParsing` and `preValidation` lifecycle stages. If you need access to the parsed body, move your logic to the `preValidation` hook or later (preValidation, preHandler, or the route handler itself). The full lifecycle order is: onRequest -> preParsing -> [body parsing] -> preValidation -> preHandler -> handler.

### NEVER: Call reply.send() in onError

Never call `reply.send()` inside an `onError` hook. The `onError` hook fires after an error has already been routed to the error handler and a response is being prepared. Calling `reply.send()` at this point throws an exception because the response is already being handled. The `onError` hook exists for telemetry, logging, and error tracking only. If you need to customize error responses, use `setErrorHandler` instead, which fires before the response is sent and gives you full control over the reply.

### BUG: Sending Data After Response

Calling `reply.send()` in `onResponse`, `onTimeout`, or `onRequestAbort` hooks will fail because the response has already been sent to the client. The `onResponse` hook fires after the response is fully sent. The `onTimeout` and `onRequestAbort` hooks fire after the connection is already dead or timed out. Use these hooks exclusively for cleanup operations, logging, metrics collection, and resource release. Never attempt to send data to the client from these hooks.

## Error Handling Issues

### NEVER: Throw Strings

Never use `throw 'error message'` in Fastify routes or hooks. When you throw a string instead of an Error object, it bypasses the custom error handler chain. The thrown string skips any plugin-scoped error handlers and hits only the default global handler, which cannot extract stack traces or error metadata from a plain string. Always throw proper Error objects: `throw new Error('message')`. If you need custom error properties, extend the Error class or use libraries like `http-errors` that produce proper Error instances with status codes.

### BUG: Stream Error Content-Type Mismatch

When a route is configured to return a stream with `text/plain` Content-Type and the route throws an error, the error handler generates a JSON error response. However, fast-json-stringify attempts to serialize the JSON error using the stream route's Content-Type header, which is still set to `text/plain`. This mismatch causes a hard 500 error. Fix this by ensuring your error handler explicitly sets the Content-Type header to `application/json` before sending the error response:

```javascript
fastify.setErrorHandler((error, request, reply) => {
  reply.header('content-type', 'application/json')
  reply.code(error.statusCode || 500).send({ error: error.message })
})
```

### BUG: Multiple setErrorHandler in Same Scope

Calling `setErrorHandler` multiple times within the same encapsulation scope silently overrides the previous handler. Only the last registered handler takes effect. If you need different error handling for different groups of routes, use encapsulated plugins. Register each plugin with its own `setErrorHandler` call. The encapsulation boundary ensures each plugin's error handler only applies to routes within that plugin's scope.

## Architecture Issues

### NEVER: Expose Node.js Directly to the Internet

Never expose your Fastify server directly on a public port. Node.js does not handle TLS termination efficiently, cannot serve multiple domains, and lacks the hardened request parsing that dedicated reverse proxies provide. Always deploy Fastify behind a reverse proxy such as Nginx, HAProxy, Caddy, or a cloud load balancer. Configure `fastify.register(require('@fastify/under-pressure'))` for load shedding and set the `trustProxy` option to match your proxy configuration.

### BUG: Assuming Reverse Encapsulation

Fastify's encapsulation is a directed acyclic graph (DAG) that flows strictly downward from parent to child. A parent plugin CANNOT access decorators, hooks, or routes registered in a child plugin. If you register a decorator inside a child plugin and expect to use it in a sibling or parent plugin, it will be undefined. Fix this by wrapping shared plugins with `fastify-plugin` (also known as `fp`), which elevates the plugin's registrations to the parent scope:

```javascript
const fp = require('fastify-plugin')

module.exports = fp(async function sharedPlugin (fastify) {
  fastify.decorate('sharedUtil', () => { /* ... */ })
})
```

## Quick Diagnosis Table

Use this table when a user reports a symptom to quickly identify the likely cause and fix:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| request.body undefined | Accessing in onRequest/preParsing | Move to preValidation or later hook |
| Hook runs twice | Mixing async + done callback | Use only one pattern, never both |
| Decorator undefined in sibling plugin | Encapsulation boundary | Wrap with fastify-plugin to elevate scope |
| 500 on error with streams | Content-Type mismatch | Set Content-Type in error handler |
| Cross-request data leakage | Reference type in decorator | Use null + onRequest pattern |
| Process crash on validation | Async validator throws | Return {error}, never throw |
| Validation bypassed | Content-type not in schema map | Map all parser content types explicitly |
| Slow serialization | Missing response schemas | Add response schemas to all routes |
| Reply already sent | Missing return reply in hook | Add return reply after reply.send() |
| Error handler not called | Throwing string instead of Error | Always throw Error objects |
| Decorator undefined at runtime | Arrow function binding | Use regular function expressions |
| Performance degradation | Dynamic property addition | Declare all decorators upfront with null |
