---
name: fastify-typescript
description: >
  This skill should be used when using TypeScript with Fastify, configuring type providers, using @fastify/type-provider-typebox, using @fastify/type-provider-json-schema-to-ts, typing Fastify plugins, declaration merging for decorators, typing route handlers, FastifyInstance generics, FastifyRequest generics, FastifyReply generics, withTypeProvider, typing custom decorators, or Fastify TypeScript configuration.
---

# Fastify TypeScript Patterns

## Type Providers (Preferred Approach)

NEVER duplicate TypeScript interfaces AND JSON schemas for the same data shape. Use a Type Provider to infer types directly from schemas, eliminating the second source of truth entirely.

Type Providers statically infer TypeScript types from inline JSON Schemas at compile time. This means runtime validation is guaranteed to match compile-time types -- a non-negotiable contract that eliminates an entire class of bugs where validation and types drift apart.

When a route defines a schema, the Type Provider analyzes that schema and automatically types `request.body`, `request.query`, and `request.params` inside the handler. If you change a schema field, incorrect handler code is immediately flagged at compile time. You get safety without ceremony.

### Available Providers

Choose one of these two providers for your project:

- **`@fastify/type-provider-typebox`** -- Uses TypeBox schemas. This is the recommended provider and offers the best developer experience. TypeBox schemas are composable, reusable TypeScript objects that produce both JSON Schema and static types from a single definition.
- **`@fastify/type-provider-json-schema-to-ts`** -- Uses raw JSON Schema objects with `as const` assertions. Choose this when you already have existing JSON Schema definitions or prefer writing schemas in plain JSON Schema format.

### Usage Pattern with TypeBox

Apply the Type Provider to your Fastify instance using `withTypeProvider<T>()`, then define route schemas using TypeBox's `Type` builder. The handler parameters are fully typed automatically:

```typescript
import Fastify from 'fastify'
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox'
import { Type } from '@sinclair/typebox'

const app = Fastify().withTypeProvider<TypeBoxTypeProvider>()

app.post('/user', {
  schema: {
    body: Type.Object({
      name: Type.String(),
      age: Type.Number()
    }),
    response: {
      200: Type.Object({
        id: Type.String(),
        name: Type.String(),
        age: Type.Number()
      })
    }
  }
}, (request, reply) => {
  // request.body is fully typed: { name: string; age: number }
  const { name, age } = request.body
  return reply.send({ id: 'generated-id', name, age })
})
```

### Usage Pattern with JSON Schema to TS

When using the JSON Schema provider, write standard JSON Schema objects with `as const` so the provider can extract literal types:

```typescript
import Fastify from 'fastify'
import { JsonSchemaToTsProvider } from '@fastify/type-provider-json-schema-to-ts'

const app = Fastify().withTypeProvider<JsonSchemaToTsProvider>()

app.post('/user', {
  schema: {
    body: {
      type: 'object',
      properties: {
        name: { type: 'string' },
        age: { type: 'number' }
      },
      required: ['name', 'age']
    } as const
  }
}, (request, reply) => {
  // request.body is typed: { name: string; age: number }
})
```

Always add `as const` to your schema objects when using this provider. Without it, TypeScript widens the literal types and the provider cannot infer specific types.

## Typing Plugins

Type Provider types do NOT automatically propagate across encapsulated contexts in Fastify. Each plugin creates its own encapsulation boundary, and the type provider information is lost when crossing that boundary.

You MUST call `.withTypeProvider<T>()` within each encapsulated plugin context to restore type inference. Type the `FastifyInstance` parameter with your chosen Type Provider generic so that route schemas inside the plugin produce correctly typed handlers:

```typescript
import { FastifyPluginAsync } from 'fastify'
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox'
import { Type } from '@sinclair/typebox'

const userRoutes: FastifyPluginAsync = async (fastify, opts) => {
  const typedFastify = fastify.withTypeProvider<TypeBoxTypeProvider>()

  typedFastify.get('/users/:id', {
    schema: {
      params: Type.Object({
        id: Type.String()
      })
    }
  }, (request, reply) => {
    // request.params.id is correctly typed as string
    const { id } = request.params
  })
}

export default userRoutes
```

If you skip the `withTypeProvider` call inside a plugin, all schema-derived types silently degrade to `unknown`. The code compiles without errors but you lose all type safety -- a dangerous silent failure.

## Declaration Merging for Custom Decorators

TypeScript does not know about properties added via `fastify.decorate()`, `fastify.decorateRequest()`, or `fastify.decorateReply()` by default. Use declaration merging to extend Fastify's core interfaces so that custom properties have full type safety and autocomplete:

```typescript
import { FastifyInstance } from 'fastify'

// Extend FastifyRequest with custom properties
declare module 'fastify' {
  interface FastifyRequest {
    authenticatedUser: User | null
  }
  interface FastifyInstance {
    config: AppConfig
    authenticate: (request: FastifyRequest, reply: FastifyReply) => Promise<void>
  }
  interface FastifyReply {
    sendSuccess: (data: unknown) => FastifyReply
  }
}
```

Place these declarations in a dedicated `types.d.ts` file or at the top of the module that registers the decorators. After declaration merging, every reference to `request.authenticatedUser`, `fastify.config`, or `reply.sendSuccess` is fully typed across your entire codebase.

For generic typed access to decorators, use `getDecorator<T>` and `setDecorator<T>` when you need to work with decorator values in a type-safe way without relying on declaration merging.

## Generics

Fastify's core interfaces accept several generic parameters for advanced customization:

- **`FastifyInstance<Server, Request, Reply, Logger, TypeProvider>`** -- The main application instance. In most cases, only `TypeProvider` matters when using a type provider.
- **`FastifyRequest<RouteGeneric, Server, Request, Schema, TypeProvider>`** -- The request object. `RouteGeneric` defines `Body`, `Querystring`, `Params`, and `Headers`. `Schema` and `TypeProvider` are set automatically by the type provider.
- **`FastifyReply<Server, Request, Reply, RouteGeneric, Schema>`** -- The reply object with its associated route context.

In most cases, the Type Provider handles all generic threading automatically. Avoid manually specifying generics unless you are writing library-level code, creating reusable plugin utilities, or working without a type provider. Manual generic threading is verbose, error-prone, and defeats the purpose of the type provider pattern.

## Plugin Typing Pattern

When writing reusable Fastify plugins, type the plugin function and wrap it with `fastify-plugin` to break encapsulation when needed:

```typescript
import { FastifyPluginAsync } from 'fastify'
import fp from 'fastify-plugin'

interface MyPluginOptions {
  prefix?: string
  enableCache?: boolean
}

const myPlugin: FastifyPluginAsync<MyPluginOptions> = async (fastify, opts) => {
  fastify.decorate('myUtil', myFunction)
  fastify.decorateRequest('requestId', null)
}

export default fp(myPlugin, {
  name: 'my-plugin',
  fastify: '5.x'
})
```

Use `FastifyPluginAsync` for async plugins and `FastifyPluginCallback` for callback-style plugins. Always prefer async. Pass the options interface as the generic parameter to `FastifyPluginAsync<T>` so that `opts` is correctly typed inside the plugin body.

Wrap with `fp()` (fastify-plugin) only when you want the plugin's decorators and hooks to be visible to the parent context. If you omit `fp()`, the plugin is fully encapsulated and its decorators are not accessible from sibling or parent plugins.

## Common TypeScript Mistakes

Avoid these patterns that undermine type safety in Fastify TypeScript projects:

- **Forgetting `withTypeProvider` in nested plugins.** Types silently become `unknown` with no compiler warning. Always call `withTypeProvider<T>()` at the start of every plugin that defines typed routes.
- **Using `as` type assertions instead of letting the Type Provider infer.** Writing `request.body as MyType` defeats the entire purpose of the type provider. If you find yourself casting, the type provider is not configured correctly -- fix the configuration instead.
- **Not declaring module augmentations for custom decorators.** Without declaration merging, decorator properties resolve to `any`, which propagates unsafe types throughout your codebase. Always write `declare module 'fastify'` blocks for every custom decorator.
- **Manually threading generics when a Type Provider is available.** Writing `FastifyRequest<{ Body: MyType }>` is redundant and fragile when a type provider already infers the type from the schema. Let the provider do its job.
- **Forgetting `as const` with the JSON Schema provider.** Without `as const`, TypeScript widens string literals to `string` and the provider cannot infer specific property types. Always assert your schema objects as const.
- **Defining schemas outside route definitions without proper typing.** If you extract schemas to separate variables, ensure they retain their literal types. Use `Type.Object()` from TypeBox or `as const` assertions to preserve type information.
