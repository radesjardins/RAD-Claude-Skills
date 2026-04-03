# RAD TypeScript Plugin

Production-grade TypeScript standards for strict-mode architecture, type safety, API boundary defense, error handling, and AI codegen guardrails.

Built from **34 curated sources** including official TypeScript 4.9–5.7 docs, the TSConfig reference, Zod documentation, neverthrow/errore error handling libraries, Fastify type providers, and community best practices. The core mental model is drawn from a custom technical standards document: *"Technical Standards for Production-Grade TypeScript: A Comprehensive Guide to Strict-Mode Architecture and API Integrity."*

---

## Features

### 6 Specialized Skills

| Skill | Triggers On |
|-------|------------|
| `typescript-strict-mode` | tsconfig setup, compiler flags, strict options |
| `typescript-type-patterns` | narrowing, discriminated unions, unknown/never/satisfies |
| `typescript-error-handling` | Result types, neverthrow, error classification |
| `typescript-api-safety` | parse-don't-validate, Zod at boundaries, Fastify type providers |
| `typescript-modern-features` | TS 4.9–5.7 features, satisfies, const type params, inferred predicates |
| `typescript-anti-patterns` | code review, AI codegen audit, anti-pattern identification |

### 1 Autonomous Agent

| Agent | Purpose |
|-------|---------|
| `typescript-reviewer` | Autonomous TypeScript code review against production standards |

---

## Installation

```bash
# Install via marketplace
cc --add-plugin rad-typescript

# Or clone and install locally
cc --plugin-dir /path/to/rad-typescript
```

---

## Core Principles Enforced

### 1. Strict Mode is Non-Negotiable

Every production TypeScript project requires, at minimum:
```json
{
  "strict": true,
  "noUncheckedIndexedAccess": true,
  "exactOptionalPropertyTypes": true,
  "noImplicitOverride": true,
  "verbatimModuleSyntax": true
}
```

### 2. Zero-Any Policy

`any` is never acceptable in production code. `unknown` + type guard or Zod schema is always the correct alternative.

### 3. Parse, Don't Validate

All data crossing an API or File System boundary must be parsed using a Zod schema with `.safeParse()`. Type assertions on external data are a critical code smell.

### 4. Errors Are Values

Expected failures should be communicated through function return types (Result pattern), not thrown exceptions. The `neverthrow` and `errore` libraries provide the infrastructure for this.

### 5. Discriminant-First Unions

All union types that model distinct states should include a literal `kind` or `type` discriminant. Exhaustiveness is enforced with `assertNever`.

### 6. Satisfies Over Annotation

Configuration objects use `satisfies` instead of type annotations to maintain both type validation and literal type specificity.

### 7. Engineering Backpressure Against AI Anti-Patterns

AI assistants systematically introduce `any`, `!`, `as`, and silent `catch {}` blocks. The plugin's skills and agent are calibrated to catch and correct these specific patterns.

---

## Source Knowledge Base

This plugin was built from the following sources (via NotebookLM "TypeScript Reference" notebook):

**Official TypeScript Documentation**
- TSConfig Reference (typescriptlang.org)
- TypeScript Narrowing Handbook
- TypeScript Object Types
- TypeScript Modules
- TypeScript 4.9, 5.0, 5.5, 5.7 Release Notes

**Libraries & Frameworks**
- Zod (zod.dev) — runtime validation
- Fastify TypeScript Reference — type providers
- neverthrow — Result type library
- errore — Errors as values library

**Community & Best Practices**
- Effective TypeScript Principles in 2025 (Dennis O'Keeffe)
- TypeScript Best Practices (testomat.io)
- Enums vs Union Types (OneUptime)
- Monorepo Type Sharing patterns (multiple sources)
- How to use TypeScript strict mode + ESLint to catch AI mistakes (Reddit/webdev)

**Internal Standards**
- "Technical Standards for Production-Grade TypeScript: A Comprehensive Guide to Strict-Mode Architecture and API Integrity" — custom markdown document

---

## Usage Examples

### Strict Mode Setup
Ask: *"Configure TypeScript strict mode for my new Node.js project"*
→ `typescript-strict-mode` skill loads and provides the complete production tsconfig

### Type Pattern Help
Ask: *"How do I model loading/success/error states as a discriminated union?"*
→ `typescript-type-patterns` skill loads with discriminated union patterns

### Error Handling
Ask: *"How should I handle errors from my database layer without using try/catch?"*
→ `typescript-error-handling` skill loads with neverthrow Result patterns

### API Safety
Ask: *"How do I safely parse and type the body of this Fastify endpoint?"*
→ `typescript-api-safety` skill loads with Zod + Fastify type provider setup

### Modern Features
Ask: *"What's the satisfies operator and when should I use it over type annotation?"*
→ `typescript-modern-features` skill loads with satisfies explanation and examples

### Code Review
Say: *"Review my TypeScript code for production readiness"*
→ `typescript-reviewer` agent runs autonomous audit

---

## Author

RAD — Built from curated NotebookLM research, 2026.
