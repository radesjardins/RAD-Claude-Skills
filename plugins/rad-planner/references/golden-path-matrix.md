# Golden Path: AI-Native Technology Selection Matrix

AI models perform best with strongly typed, highly opinionated, and extensively documented frameworks that have massive presence in their training data. TypeScript is the non-negotiable default -- its strict type safety acts as a continuous feedback loop that catches up to 40% of logical errors during code generation.

## AI-Native Proficiency Tiers

### Primary Tier (Highest AI Accuracy)
| Technology | Why AI Excels | Best For |
|-----------|---------------|----------|
| **TypeScript** | Strict types = continuous error detection, massive training corpus | Everything (non-negotiable default) |
| **Next.js 14-15** | Enforces standard file structures, clear boundaries, reduces hallucinations | Full-stack web apps, SSR/SSG |
| **FastAPI** | Pydantic models auto-generate docs, type-safe contracts | Python APIs, ML backends |

### Secondary Tier (Strong Predictability)
| Technology | Why AI Excels | Best For |
|-----------|---------------|----------|
| **Go** | Minimal syntactic ambiguity, robust stdlib, near-C++ speeds | High-throughput microservices |
| **Rust** | Compiler-enforced safety, clear error messages guide AI | Systems programming, performance-critical |
| **NestJS** | Opinionated structure, decorator patterns | Enterprise Node.js APIs |
| **Tailwind CSS** | Utility-first = predictable output, no custom CSS hallucinations | All frontend styling |
| **Astro** | File-based routing, island architecture, clear boundaries | Content sites, documentation |

### Niche/Legacy Tier (High Hallucination Risk)
| Technology | Risk Factor | Mitigation |
|-----------|-------------|------------|
| **Ruby on Rails** | Magic methods, convention-over-configuration confuses LLMs | Pin exact versions, provide explicit examples |
| **Django** | Implicit ORM behavior, complex middleware chains | Strict type hints, explicit queryset annotations |
| **PHP 8** | Historical baggage in training data mixes old/new patterns | Use strict_types, modern PHP only |
| **jQuery** | AI may suggest it when vanilla JS or modern frameworks are better | Explicitly exclude in CLAUDE.md |

### Data/AI Tier (Domain Dominance)
| Technology | Why AI Excels | Best For |
|-----------|---------------|----------|
| **Python** | Dominant in ML/data training data | Data processing, ML pipelines |
| **SQL** | Extremely well-represented, high accuracy | All database operations |
| **pgvector** | Integrated vector search, no sidecar needed | AI memory, embeddings, RAG |

## Project-Type Decision Matrix

### Startups and MVPs ("Modern Standard")
**Goal:** Maximum speed, end-to-end type safety, seamless deployment

| Layer | Recommended | Alternative | Avoid |
|-------|------------|-------------|-------|
| Frontend | Next.js + TypeScript | Astro (content-heavy) | CRA, vanilla React |
| Backend | Node.js (via Next.js API routes) | FastAPI (if Python needed) | Express without TypeScript |
| Database | PostgreSQL | Supabase (managed Postgres) | MongoDB (for relational data) |
| ORM | Drizzle or Prisma | - | Raw SQL for CRUD apps |
| Styling | Tailwind CSS | - | CSS-in-JS, SASS |
| Auth | Auth.js / Supabase Auth | Clerk | Custom auth (unless required) |
| Deployment | Vercel / Coolify | Railway | Manual Docker without CI |

**Why:** T3 Stack provides end-to-end type safety -- if AI changes a schema, the IDE highlights every affected component.

### AI-Native and Data-Intensive Applications
**Goal:** Heavy LLM integration, ML ecosystem, RAG pipelines

| Layer | Recommended | Alternative | Avoid |
|-------|------------|-------------|-------|
| Frontend | React or Svelte | Astro (docs/dashboard) | Heavy SPA frameworks |
| Backend | Python (FastAPI) | Node.js + LangChain.js | Flask without type hints |
| Database | PostgreSQL + pgvector | - | Separate vector DB sidecar |
| ML Framework | PyTorch / Transformers | TensorFlow | Custom from scratch |
| API Contracts | Pydantic models | Zod (if Node.js) | Untyped JSON |

**Why:** FastAPI natively handles the Python ML ecosystem while auto-generating API docs through Pydantic models.

### Enterprise Applications and High-Performance Microservices
**Goal:** Long-term stability, strict governance, high throughput

| Layer | Recommended | Alternative | Avoid |
|-------|------------|-------------|-------|
| Frontend | Angular or Vue (Nuxt) | Next.js (if team knows React) | Svelte (smaller ecosystem) |
| Backend | Go or .NET | Java Spring Boot | Node.js (for CPU-intensive) |
| Database | PostgreSQL + Redis | MySQL (if existing) | NoSQL as primary |
| API Style | gRPC (internal) + REST (external) | GraphQL (if client-driven) | REST-only for microservices |
| Orchestration | Kubernetes | Docker Compose (small scale) | Manual deployment |

**Why:** Go provides exceptional throughput with simple syntax that makes AI code reviews straightforward.

### Universal Database Default
For 80% of new projects: **PostgreSQL**
- JSONB support for NoSQL-like flexibility
- pgvector for integrated AI memory (vector storage)
- No architectural brittleness of maintaining separate vector DB
- Mature, well-documented, AI generates accurate SQL

## Stack Evaluation Checklist

When evaluating a stack recommendation, verify:

- [ ] All components are in Primary or Secondary tier (or have explicit justification)
- [ ] TypeScript is used wherever possible
- [ ] Database choice matches data access patterns (relational vs. document vs. vector)
- [ ] Framework has active maintenance and recent releases
- [ ] Team has experience or framework has strong learning resources
- [ ] Deployment target is compatible with chosen stack
- [ ] No Niche/Legacy tier choices without explicit user requirement
- [ ] API contracts are type-safe end-to-end

## When to Search for Updated Information

Always verify with Context7 or web search when:
- User mentions a specific framework version (check if latest)
- Recommending deployment platforms (pricing/features change frequently)
- Evaluating new frameworks not in training data
- Comparing performance benchmarks (results change with releases)
- Checking library compatibility with specific framework versions
