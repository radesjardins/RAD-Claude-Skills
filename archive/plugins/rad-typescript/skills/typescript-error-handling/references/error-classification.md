# Error Classification and Recovery Strategies

## The Four Error Categories

### 1. Transient Errors
**Recoverable without user action. Retry automatically.**

Characteristics: Temporary infrastructure issues, network blips, service overload.

```typescript
type TransientError =
  | { category: 'transient'; code: 'TIMEOUT'; retryAfterMs?: number }
  | { category: 'transient'; code: 'SERVICE_UNAVAILABLE'; retryAfterMs?: number }
  | { category: 'transient'; code: 'RATE_LIMITED'; retryAfterMs: number };

// Retry with exponential backoff
async function withRetry<T>(
  fn: () => Promise<T>,
  maxAttempts = 3,
  baseDelayMs = 1000,
): Promise<T> {
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (attempt === maxAttempts - 1) throw err;
      const delay = baseDelayMs * Math.pow(2, attempt);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  throw new Error('Max retries exceeded');
}
```

### 2. Correctable Errors
**Recoverable with changed input or re-authentication.**

Characteristics: Bad user input, expired credentials, stale data.

```typescript
type CorrectableError =
  | { category: 'correctable'; code: 'VALIDATION_FAILED'; fields: Record<string, string> }
  | { category: 'correctable'; code: 'TOKEN_EXPIRED' }
  | { category: 'correctable'; code: 'CONFLICT'; conflictingId: string };

// Handle by prompting user to fix input or refresh auth
function handleCorrectableError(err: CorrectableError): UserFacingMessage {
  switch (err.code) {
    case 'VALIDATION_FAILED':
      return { type: 'form-errors', fields: err.fields };
    case 'TOKEN_EXPIRED':
      return { type: 'redirect', url: '/login?reason=session-expired' };
    case 'CONFLICT':
      return { type: 'warning', message: `Conflicts with existing item ${err.conflictingId}` };
  }
}
```

### 3. Permanent Errors
**Not recoverable — report and fail gracefully.**

Characteristics: Not found, unauthorized, forbidden.

```typescript
type PermanentError =
  | { category: 'permanent'; code: 'NOT_FOUND'; resource: string; id: string }
  | { category: 'permanent'; code: 'FORBIDDEN'; reason?: string }
  | { category: 'permanent'; code: 'UNAUTHORIZED' };
```

### 4. Fatal Errors
**Abort operation — do not attempt recovery.**

Characteristics: Database corruption, missing required configuration, OOM.

```typescript
type FatalError =
  | { category: 'fatal'; code: 'CONFIG_MISSING'; key: string }
  | { category: 'fatal'; code: 'DATABASE_CORRUPTED'; details: string }
  | { category: 'fatal'; code: 'INVARIANT_VIOLATION'; message: string };

// Fatal errors should crash the process (in Node.js) or show error boundary (React)
function handleFatalError(err: FatalError): never {
  console.error('FATAL ERROR:', err);
  process.exit(1); // Node.js
  // OR: throw err; // React — caught by error boundary
}
```

## Structured Error Type Pattern

```typescript
// Base application error with classification
interface BaseError<Category extends string, Code extends string> {
  readonly category: Category;
  readonly code: Code;
  readonly message: string;
  readonly timestamp: Date;
  readonly traceId?: string; // For distributed tracing
}

// Specific error types
interface DatabaseError extends BaseError<'db', 'CONNECTION' | 'QUERY' | 'CONSTRAINT'> {
  readonly query?: string;
}

interface HttpError extends BaseError<'http', '400' | '401' | '403' | '404' | '429' | '500'> {
  readonly statusCode: number;
  readonly url: string;
  readonly retryable: boolean;
}

interface ValidationError extends BaseError<'validation', 'SCHEMA' | 'BUSINESS_RULE'> {
  readonly fields: Record<string, string[]>;
}

// Union of all app errors
type AppError = DatabaseError | HttpError | ValidationError;
```

## Error Factory Pattern

```typescript
const createError = {
  notFound: (resource: string, id: string): PermanentError => ({
    category: 'permanent',
    code: 'NOT_FOUND',
    resource,
    id,
  }),

  validation: (fields: Record<string, string>): CorrectableError => ({
    category: 'correctable',
    code: 'VALIDATION_FAILED',
    fields,
  }),

  transient: (code: TransientError['code'], retryAfterMs?: number): TransientError => ({
    category: 'transient',
    code,
    retryAfterMs,
  }),
};
```

## Error Handling in HTTP Response

```typescript
import type { FastifyReply } from 'fastify';
import type { AppError } from './errors';

function sendErrorResponse(reply: FastifyReply, error: AppError): void {
  if (error.category === 'permanent') {
    const statusMap: Record<PermanentError['code'], number> = {
      NOT_FOUND: 404,
      FORBIDDEN: 403,
      UNAUTHORIZED: 401,
    };
    reply.status(statusMap[error.code]).send({ error: error.code, message: error.message });
    return;
  }

  if (error.category === 'correctable') {
    if (error.code === 'VALIDATION_FAILED') {
      reply.status(400).send({ error: 'VALIDATION_FAILED', fields: error.fields });
      return;
    }
    reply.status(400).send({ error: error.code });
    return;
  }

  if (error.category === 'transient') {
    reply.status(503).send({
      error: 'SERVICE_UNAVAILABLE',
      retryAfter: error.retryAfterMs ? Math.ceil(error.retryAfterMs / 1000) : undefined,
    });
    return;
  }

  // Fatal: log and send generic 500
  console.error('Fatal error in request handler:', error);
  reply.status(500).send({ error: 'INTERNAL_SERVER_ERROR' });
}
```

## Async Error Accumulation

When multiple parallel operations can fail:

```typescript
import { combineWithAllErrors } from 'neverthrow';

async function validateAll(items: unknown[]): Promise<Result<ValidItem[], ValidationError[]>> {
  const results = items.map(item => parseItem(item));
  const combined = combineWithAllErrors(results);

  return combined.mapErr(errors => errors.flat());
}
```
