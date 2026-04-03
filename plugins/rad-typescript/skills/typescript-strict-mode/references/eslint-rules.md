# ESLint Rules for TypeScript Production Code

The TypeScript compiler catches type-level errors. ESLint with `@typescript-eslint` extends enforcement into runtime patterns the compiler cannot see.

## Required Package Setup

```bash
npm install --save-dev \
  @typescript-eslint/parser \
  @typescript-eslint/eslint-plugin \
  eslint
```

## Production ESLint Configuration

```js
// eslint.config.js (flat config)
import tseslint from '@typescript-eslint/eslint-plugin';
import tsparser from '@typescript-eslint/parser';

export default [
  {
    files: ['**/*.ts', '**/*.tsx'],
    plugins: { '@typescript-eslint': tseslint },
    parser: tsparser,
    parserOptions: {
      project: './tsconfig.json',
    },
    rules: {
      // === ZERO-ANY POLICY ===
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unsafe-assignment': 'error',
      '@typescript-eslint/no-unsafe-call': 'error',
      '@typescript-eslint/no-unsafe-member-access': 'error',
      '@typescript-eslint/no-unsafe-return': 'error',
      '@typescript-eslint/no-unsafe-argument': 'error',

      // === NO UNSAFE ASSERTIONS ===
      '@typescript-eslint/consistent-type-assertions': [
        'error',
        {
          assertionStyle: 'as',
          objectLiteralTypeAssertions: 'never', // No `{} as Type` — use Zod
        },
      ],
      '@typescript-eslint/no-non-null-assertion': 'error',
      '@typescript-eslint/no-non-null-asserted-optional-chain': 'error',

      // === ERROR HANDLING ===
      '@typescript-eslint/no-floating-promises': 'error',       // Await all promises
      '@typescript-eslint/promise-function-async': 'error',     // Async fns return Promise
      '@typescript-eslint/no-misused-promises': 'error',        // No promise in boolean
      'no-empty': ['error', { allowEmptyCatch: false }],        // No silent catches

      // === TYPE IMPORTS ===
      '@typescript-eslint/consistent-type-imports': [
        'error',
        { prefer: 'type-imports', fixStyle: 'inline-type-imports' },
      ],
      '@typescript-eslint/no-import-type-side-effects': 'error',

      // === CODE QUALITY ===
      '@typescript-eslint/no-unused-vars': [
        'error',
        { argsIgnorePattern: '^_', varsIgnorePattern: '^_' },
      ],
      '@typescript-eslint/prefer-nullish-coalescing': 'error',  // ?? over ||
      '@typescript-eslint/prefer-optional-chain': 'error',      // ?. over && chains
      '@typescript-eslint/no-unnecessary-type-assertion': 'error',
      '@typescript-eslint/no-unnecessary-condition': 'error',

      // === ENUM SAFETY ===
      '@typescript-eslint/prefer-literal-type': 'off', // Covered by enum rules below
      'no-restricted-syntax': [
        'error',
        {
          selector: 'TSEnumDeclaration:not([const=true])',
          message: 'Prefer string literal unions or const enums over regular enums',
        },
      ],
    },
  },
  // Relaxed rules for test files
  {
    files: ['**/*.test.ts', '**/*.spec.ts'],
    rules: {
      '@typescript-eslint/no-non-null-assertion': 'warn', // More lenient in tests
    },
  },
];
```

## Rule Categories Explained

### Zero-Any Policy
These rules implement the principle that `any` is never acceptable:

| Rule | What It Catches |
|------|----------------|
| `no-explicit-any` | Direct `any` annotations |
| `no-unsafe-assignment` | Assigning `any` to typed variable |
| `no-unsafe-call` | Calling `any` as function |
| `no-unsafe-member-access` | Accessing properties on `any` |
| `no-unsafe-return` | Returning `any` from typed function |
| `no-unsafe-argument` | Passing `any` to typed parameter |

**When `any` is unavoidable:** Use `unknown` with a type guard instead. If you must accept `any` (e.g., at a true external boundary), use `// eslint-disable-next-line @typescript-eslint/no-explicit-any` with a comment explaining why.

### Promise Safety
```typescript
// Caught by no-floating-promises:
async function fetchData() { return data; }
fetchData(); // Error! Promise not awaited

// Fix:
await fetchData();
// Or explicitly fire-and-forget:
void fetchData();

// Caught by no-misused-promises:
if (fetchData()) { ... } // Error! Promise is always truthy

// Fix:
if (await fetchData()) { ... }
```

### Nullish Coalescing
```typescript
// Caught by prefer-nullish-coalescing:
const value = input || 'default'; // Problem: '' and 0 fall through!

// Fix — only replaces null/undefined:
const value = input ?? 'default';
```

### Optional Chaining
```typescript
// Caught by prefer-optional-chain:
const name = user && user.profile && user.profile.name;

// Fix:
const name = user?.profile?.name;
```

## Custom Rules for AI Codegen Guardrails

Add these to catch specific AI-generated anti-patterns:

```js
// Detect Zod .parse() (throws) vs .safeParse() (returns Result)
'no-restricted-syntax': [
  'error',
  {
    selector: 'CallExpression[callee.property.name="parse"][callee.object.name=/Schema$/]',
    message: 'Use .safeParse() instead of .parse() for graceful error handling',
  },
  {
    selector: 'TSEnumDeclaration:not([const=true])',
    message: 'Use string literal unions or const enums instead of regular enums',
  },
  {
    selector: 'CatchClause:empty',
    message: 'Empty catch blocks hide errors. Handle or re-throw.',
  },
]
```

## Type Coverage Enforcement

Install `typescript-coverage-report` to enforce minimum type coverage:

```bash
npm install --save-dev typescript-coverage-report
```

```json
// package.json
{
  "scripts": {
    "type-coverage": "typescript-coverage-report --threshold 95"
  }
}
```

Target: **≥ 95% type coverage** in production codebases.

## Pre-Commit Hook Configuration

```json
// .husky/pre-commit
npm run type-check && npm run lint
```

```json
// package.json
{
  "scripts": {
    "type-check": "tsc --noEmit",
    "lint": "eslint . --ext .ts,.tsx --max-warnings 0"
  }
}
```

`--max-warnings 0` ensures warnings are treated as errors in CI.
