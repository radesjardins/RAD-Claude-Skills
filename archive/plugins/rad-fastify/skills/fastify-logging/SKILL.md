---
name: fastify-logging
description: >
  This skill should be used when configuring Fastify logging, setting up Pino logger, using child loggers, implementing log redaction, configuring log transports, using pino-pretty for development, async logging with sonic-boom, structured JSON logging, request correlation IDs, log levels, configuring pino.final for crash handling, multi-target log transports, or Fastify observability.
---

# Fastify Logging with Pino

You are configuring logging for a Fastify application. Fastify ships with Pino as its built-in logger. Follow these instructions precisely — they encode hard constraints and production-critical patterns.

## Core Architecture

Pino is an asynchronous, zero-overhead, structured JSON logger. It maximizes throughput by offloading formatting and I/O to worker threads rather than performing them on the main event-loop thread. This is fundamental to how Fastify achieves its performance characteristics — never undermine it by adding synchronous formatting in-process.

Enable logging by passing `logger: true` in Fastify options for default behavior, or pass a custom Pino configuration object for fine-grained control. You can also pass a pre-configured Pino instance directly if you need to share the same logger across multiple parts of your application.

```javascript
// Minimal — default Pino with info level
const fastify = require('fastify')({ logger: true })

// Custom configuration object
const fastify = require('fastify')({
  logger: {
    level: 'info',
    // additional Pino options here
  }
})

// Pre-configured Pino instance
const pino = require('pino')
const logger = pino({ level: 'debug' })
const fastify = require('fastify')({ logger })
```

## Request Correlation

Fastify automatically generates and injects a `reqId` into every log message throughout the entire request lifecycle. This is a hard invariant — every log line produced within a request context carries this ID, enabling you to trace all activity for a single request across your log output.

Customize ID generation via the `genReqId` option when you need deterministic or externally-provided IDs (e.g., propagating a trace ID from an upstream load balancer):

```javascript
const fastify = require('fastify')({
  logger: true,
  genReqId: (req) => req.headers['x-request-id'] || crypto.randomUUID()
})
```

Do not roll your own correlation mechanism. Use this built-in facility.

## Child Loggers

Always use `logger.child()` to create scoped loggers that automatically attach contextual metadata to every log line they produce. This eliminates the need to manually pass context data on every `log.info()` call.

```javascript
// Module-scoped child logger
const paymentLogger = fastify.log.child({ module: 'payments' })
paymentLogger.info('Processing refund') // { module: 'payments', msg: 'Processing refund', ... }

// User-scoped child logger within a route
fastify.get('/account', async (request, reply) => {
  const userLogger = request.log.child({ userId: request.user.id })
  userLogger.info('Fetching account details')
  // Every line from userLogger carries reqId AND userId
})
```

The `request.log` property is itself a child logger that already carries the `reqId`. Build on top of it — do not create a fresh logger from `fastify.log` inside request handlers unless you intentionally want to lose the request correlation.

Tie `userId`, `traceId`, `tenantId`, or module name to child loggers based on what makes sense for your tracing and debugging needs.

## Redaction (Non-Negotiable in Production)

Never manually mask sensitive data with string replacement or custom serializers. Use Pino's built-in `redact` option, which operates at the serialization layer and scrubs values before they are written anywhere.

```javascript
const fastify = require('fastify')({
  logger: {
    redact: [
      'req.headers.authorization',
      'req.headers.cookie',
      'password',
      'creditCard',
      'user.ssn'
    ]
  }
})
```

Pino supports dot-notation paths and wildcard patterns for deep scrubbing:

```javascript
redact: ['*.password', 'user.*.ssn', 'payload.billing.cardNumber']
```

Redacted fields appear as `[Redacted]` in the output. This is the only acceptable approach — manual masking is error-prone and inevitably misses edge cases.

## Async Logging (Production)

In production, always use asynchronous logging. Pino uses sonic-boom under the hood to buffer log writes and flush them in the background, preventing I/O from blocking the event loop.

```javascript
const pino = require('pino')

// Async file destination
const logger = pino(
  pino.destination({ dest: '/var/log/app.log', sync: false })
)

// Async stdout (default when using transport)
const fastify = require('fastify')({
  logger: {
    level: 'info'
    // transports are async by default
  }
})
```

Never use `sync: true` in production — it blocks the event loop on every log write and destroys throughput under load. Synchronous mode exists only for testing and debugging scenarios where you need guaranteed write ordering.

## Environment-Adaptive Configuration

Adapt your logging configuration to the environment without changing application code. Use the `transport` option to control output formatting:

```javascript
const fastify = require('fastify')({
  logger: {
    level: process.env.LOG_LEVEL || 'info',
    redact: ['req.headers.authorization', 'req.headers.cookie'],
    transport: process.env.NODE_ENV === 'development'
      ? { target: 'pino-pretty', options: { colorize: true } }
      : undefined
  }
})
```

- **Production**: Emit standard JSON lines. Observability platforms (Datadog, ELK, Grafana Loki) ingest JSON natively. Do not format or prettify.
- **Development**: Use `pino-pretty` for human-readable, colorized output. Install it as a dev dependency only.

Never conditionally require `pino-pretty` in application code. The `transport` option handles this cleanly.

## Crash Handling with pino.final

Node.js cannot safely recover from uncaught exceptions or unhandled promise rejections. Use `pino.final()` inside global error handlers to perform a synchronous, blocking write of the fatal error before the process exits. This guarantees the crash reason reaches your logs even though the async buffer has not flushed.

```javascript
const pino = require('pino')
const logger = pino({ /* config */ })

process.on('uncaughtException', pino.final(logger, (err, finalLogger) => {
  finalLogger.fatal(err, 'Uncaught exception — shutting down')
  process.exit(1)
}))

process.on('unhandledRejection', pino.final(logger, (err, finalLogger) => {
  finalLogger.fatal(err, 'Unhandled rejection — shutting down')
  process.exit(1)
}))
```

You must intentionally crash after logging. Never swallow uncaught exceptions — the process is in an undefined state and continuing risks data corruption or silent failures.

## Multi-Target Transports

Route logs to multiple destinations simultaneously using Pino's transport targets:

```javascript
const fastify = require('fastify')({
  logger: {
    transport: {
      targets: [
        { target: 'pino/file', options: { destination: '/var/log/app.log' }, level: 'info' },
        { target: 'pino/file', options: { destination: 1 }, level: 'info' }, // stdout
        { target: 'pino-loki', options: { host: 'http://loki:3100' }, level: 'warn' }
      ]
    }
  }
})
```

Critical constraint: you cannot use `formatters.level` hook with multi-target transports. The transport pipeline needs the numeric level value for routing decisions. If you replace it with a string via a formatter, level-based routing breaks silently.

## Performance Constraints

Follow these rules to preserve Pino's performance characteristics:

- **Never format timestamps in-process.** Pino emits epoch milliseconds by default. Formatting timestamps (ISO strings, etc.) in the application process drastically degrades logging throughput. Let your transport or log aggregator handle timestamp formatting.
- **`logger.flush()` does not work when pino-pretty is active.** The pretty-print transport manages its own buffering. Do not rely on `flush()` in development if you are using pino-pretty.
- **Log level filtering happens before serialization.** If your production level is `info`, then `debug` and `trace` calls are essentially no-ops — they do not serialize their arguments. Set the appropriate level for production to avoid unnecessary work.
- **Avoid logging large objects.** Even with async I/O, serializing large payloads consumes CPU on the main thread. Log only what you need for debugging and observability.

## Complete Production Configuration Pattern

```javascript
const fastify = require('fastify')({
  logger: {
    level: process.env.LOG_LEVEL || 'info',
    redact: ['req.headers.authorization', 'req.headers.cookie', '*.password'],
    serializers: {
      req: (req) => ({
        method: req.method,
        url: req.url,
        hostname: req.hostname,
        remoteAddress: req.ip
      })
    },
    transport: process.env.NODE_ENV === 'development'
      ? { target: 'pino-pretty', options: { colorize: true, translateTime: 'HH:MM:ss Z' } }
      : undefined
  },
  genReqId: (req) => req.headers['x-request-id'] || crypto.randomUUID()
})
```

When generating logging configuration for a Fastify application, always include redaction, environment-adaptive transport, and custom request ID generation as baseline requirements. These are not optional enhancements — they are production necessities.
