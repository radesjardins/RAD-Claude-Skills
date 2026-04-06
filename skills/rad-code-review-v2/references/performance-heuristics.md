# Performance Profiling Heuristics

This document provides grep-able detection patterns for common performance anti-patterns. Each pattern includes what to search for, how to verify it from code, the severity when violated, and example bad/good code.

These patterns are designed for static analysis during code review. They detect structural anti-patterns, not measured performance — a flagged pattern may be acceptable in a low-traffic path but critical in a hot path.

---

## 1. N+1 Queries

**Description**: A database query executed inside a loop, resulting in N+1 total queries instead of 1 batched query. The most common performance anti-pattern in web applications.

**Detection heuristic**:
- Find loop constructs: `.map(`, `.forEach(`, `for (`, `for...of`, `for...in`, `while (`
- Inside each loop body, search for database calls:
  - **ORM methods**: `.findOne(`, `.findById(`, `.findUnique(`, `.get(`, `.query(`, `.fetch(`, `.load(`
  - **Raw query methods**: `db.query(`, `connection.execute(`, `cursor.execute(`, `pool.query(`
  - **Prisma**: `prisma.*.find`, `prisma.*.update`, `prisma.*.delete` inside loops
  - **Sequelize**: `Model.findOne`, `Model.findByPk` inside loops
  - **SQLAlchemy**: `session.query(`, `session.execute(` inside loops
  - **GORM**: `db.First(`, `db.Find(`, `db.Where(` inside loops

**Grep patterns**:
```
# JavaScript/TypeScript — ORM call inside .map/.forEach
\.map\(.*\n.*\.(findOne|findById|findUnique|findFirst|query|execute)
\.forEach\(.*\n.*\.(findOne|findById|findUnique|findFirst|query|execute)

# Python — query inside for loop
for .* in .*:\n.*session\.(query|execute|get)
for .* in .*:\n.*\.objects\.(get|filter|first)

# Go — query inside for range
for .* range .*\{\n.*\.Query(|\.QueryRow(|\.Exec(
```

**Severity**: Moderate in low-volume paths. Major in request handlers, API endpoints, or list/dashboard views.

**Example of bad code**:
```javascript
// N+1: one query per user to get their latest order
const users = await prisma.user.findMany();
const usersWithOrders = await Promise.all(
  users.map(async (user) => {
    const latestOrder = await prisma.order.findFirst({
      where: { userId: user.id },
      orderBy: { createdAt: 'desc' },
    });
    return { ...user, latestOrder };
  })
);
```

**Example of correct code**:
```javascript
// Single query with include/join
const usersWithOrders = await prisma.user.findMany({
  include: {
    orders: {
      orderBy: { createdAt: 'desc' },
      take: 1,
    },
  },
});
```

---

## 2. Unnecessary Re-renders (React)

**Description**: React components re-rendering when they don't need to, typically caused by unstable references in props, missing memoization, or incorrect dependency arrays.

**Detection heuristic**:

### 2a: Object/Array Literals in JSX Props
- Find JSX attributes with inline object or array literals: `prop={{...}}`, `prop={[...]}`
- These create a new reference on every render, defeating React.memo and causing child re-renders
- Exception: `style={{...}}` on native DOM elements (not custom components) is a minor concern

**Grep patterns**:
```
# Inline object in JSX prop (not style on DOM element)
<[A-Z]\w+.*\s\w+=\{\{
# Inline array in JSX prop
<[A-Z]\w+.*\s\w+=\{\[
```

### 2b: Inline Function Definitions in JSX
- Find inline arrow functions in JSX props: `onClick={() => ...}`, `onChange={(e) => ...}`
- Creates a new function reference on every render
- Only flag in components that render frequently or pass to memoized children

**Grep pattern**:
```
<[A-Z]\w+.*\s\w+=\{(\([^)]*\)|[a-z]\w*)\s*=>
```

### 2c: Missing/Wrong useEffect Dependency Arrays
- Find `useEffect` without a dependency array (runs on every render)
- Find `useEffect` with `[]` that references variables from the component scope (stale closure)

**Grep patterns**:
```
# useEffect with no dependency array
useEffect\(\s*\(\)\s*=>\s*\{[^}]*\}\s*\)
# useEffect with empty array — flag for manual review if body references outer variables
useEffect\(\s*\(\)\s*=>\s*\{[^}]*\},\s*\[\]\s*\)
```

### 2d: Non-memoized Context Value
- Find `<Context.Provider value={{...}}>` with inline object — re-renders all consumers on every render

**Grep pattern**:
```
Provider\s+value=\{\{
```

**Severity**: Minor for individual instances. Moderate if multiple patterns combine in a frequently-rendered component (list items, table rows, form fields).

---

## 3. Unbounded List Rendering

**Description**: Rendering an entire collection without pagination, virtualization, or limits. Causes DOM bloat, slow initial render, and high memory usage.

**Detection heuristic**:
- Find `.map()` rendering in JSX/TSX that maps over a data array
- Check if the source array is bounded: does it come from a query with `LIMIT`, from paginated API response, or from a fixed-size dataset?
- Flag when: the array could be arbitrarily large (all users, all orders, all logs)

**Grep patterns**:
```
# JSX map rendering
\{.*\.map\(\s*\([^)]*\)\s*=>\s*[(<]
# Combined with database query without LIMIT
\.findMany\(\s*\{[^}]*\}\s*\)  # Prisma without take/skip
\.find\(\s*\{[^}]*\}\s*\)       # Mongoose without limit
Model\.objects\.all\(\)          # Django without [:N]
```

**Severity**: Moderate for user-facing lists. Major for admin/dashboard views that could have thousands of entries.

**Example of bad code**:
```typescript
// All logs, unbounded
const logs = await prisma.auditLog.findMany();
return (
  <ul>
    {logs.map(log => <LogEntry key={log.id} log={log} />)}
  </ul>
);
```

**Example of correct code**:
```typescript
// Paginated with virtualization
const logs = await prisma.auditLog.findMany({
  take: 50,
  skip: page * 50,
  orderBy: { createdAt: 'desc' },
});
return (
  <VirtualList items={logs} renderItem={(log) => <LogEntry log={log} />} />
);
```

---

## 4. Synchronous Blocking in Request Handlers

**Description**: Using synchronous I/O operations (file reads, child process execution, network requests) inside HTTP request handlers. Blocks the event loop (Node.js) or thread (other languages), degrading throughput for all concurrent requests.

**Detection heuristic**:
- Find synchronous I/O calls inside route handlers or middleware:

**Grep patterns**:
```
# Node.js synchronous I/O
readFileSync|writeFileSync|mkdirSync|readdirSync|statSync|unlinkSync
existsSync  # only in request handlers — fine in startup/config
execSync|spawnSync
# Python synchronous in async context
requests\.get|requests\.post  # in async def or route handler
urllib\.request\.urlopen
open\(.*\)\.read\(\)  # in async route handler
```

**Severity**: Major in request handlers. Minor in startup/initialization code. Critical if the synchronous call processes user input (command injection + blocking).

**Example of bad code**:
```javascript
app.get('/api/report', (req, res) => {
  // Blocks the entire event loop while reading file
  const data = fs.readFileSync(`./reports/${req.params.id}.json`, 'utf8');
  // Blocks again while running external tool
  const result = execSync(`generate-pdf ${req.params.id}`);
  res.json({ data: JSON.parse(data), pdf: result.toString() });
});
```

**Example of correct code**:
```javascript
app.get('/api/report', async (req, res) => {
  const [data, result] = await Promise.all([
    fs.promises.readFile(`./reports/${sanitize(req.params.id)}.json`, 'utf8'),
    execAsync(`generate-pdf ${sanitize(req.params.id)}`),
  ]);
  res.json({ data: JSON.parse(data), pdf: result.stdout });
});
```

---

## 5. Missing Pagination

**Description**: Database queries that fetch all matching records without `LIMIT`/`OFFSET`, cursor, or other bounding mechanism. Works in development with small datasets, causes memory exhaustion and timeouts in production.

**Detection heuristic**:
- Find "select all" query patterns without bounds:

**Grep patterns**:
```
# SQL without LIMIT
SELECT\s+.*\s+FROM\s+\w+\s*(WHERE[^;]*)?\s*;  # no LIMIT keyword
# Prisma findMany without take
\.findMany\(\s*(\{\s*where:|\{\s*orderBy:|\{\s*include:|\{\s*select:|\{\s*\})  # no take/skip
\.findMany\(\s*\)  # completely unbounded
# Sequelize findAll without limit
\.findAll\(\s*\{(?!.*limit)  # findAll without limit option
# Django objects.all without slicing
\.objects\.all\(\)  # without [:]
\.objects\.filter\([^)]*\)(?!\[)  # filter without slice
# Mongoose find without limit
\.find\(\s*\{[^}]*\}\s*\)(?!\.limit)  # find without .limit()
```

**Severity**: Moderate for read-only endpoints. Major for endpoints that serialize and return all records (memory + network + client processing). Critical for data export endpoints without streaming.

---

## 6. Bundle Bloat Indicators

**Description**: Importing entire libraries when tree-shakeable submodule imports exist, or including heavy dependencies for trivial functionality.

**Detection heuristic**:

### 6a: Whole-Library Imports
```
# lodash (entire library vs tree-shakeable)
import _ from 'lodash'          # BAD: imports entire 70KB+ library
import { get } from 'lodash'    # ALSO BAD: still imports entire library with some bundlers
import get from 'lodash/get'    # GOOD: imports only the function

# moment.js (entire library with all locales)
import moment from 'moment'     # BAD: 300KB+ with locales, use date-fns or dayjs
require('moment')               # BAD

# AWS SDK v2 vs v3
import AWS from 'aws-sdk'                    # BAD: imports entire SDK
import { S3Client } from '@aws-sdk/client-s3' # GOOD: modular v3 import

# Material UI
import { Button } from '@mui/material'  # BAD: may import entire package
import Button from '@mui/material/Button' # GOOD: direct path import

# Icons
import * as Icons from 'lucide-react'    # BAD: imports all icons
import { Search } from 'lucide-react'    # GOOD: tree-shakeable named import
```

### 6b: Heavy Dependencies for Trivial Tasks
Flag if these packages are in dependencies (check package.json):
- `moment` — use `date-fns` or `dayjs` (both tree-shakeable, much smaller)
- `lodash` (full) — use `lodash-es` or individual `lodash/*` imports
- `jquery` — in a modern framework project, this is almost always unnecessary
- `underscore` — superseded by native ES6+ methods

**Severity**: Minor for individual imports. Moderate if the bundle size materially impacts load time (check if the project has any bundle size budget or Core Web Vitals targets).

---

## 7. Missing Caching

**Description**: Expensive computations or I/O operations repeated on every request/render without caching results.

**Detection heuristic**:
- Find expensive operations called in request handlers without caching:
  - External API calls to services with slow response times
  - Database queries for rarely-changing reference data (countries, categories, config)
  - File reads for static configuration
  - Crypto operations (hashing, signing) on the same data repeatedly

**Grep patterns**:
```
# Repeatedly fetching reference data
app\.(get|post)\(.*\n.*fetch\(['"]https://.*api  # External API in handler without cache
# React: expensive computation without useMemo
const \w+ = .*\.filter\(.*\.map\(  # chain of array operations without memoization
```

**Severity**: Minor for low-traffic paths. Moderate for per-request external API calls. Major if the missing cache causes rate limiting from an external service.

---

## 8. Missing Database Indexes

**Description**: Database queries that filter or sort on columns without indexes, causing full table scans.

**Detection heuristic**:
- Find `WHERE` clause columns and `ORDER BY` columns in queries
- Cross-reference with migration files to check if indexes exist on those columns
- Common missing indexes:
  - Foreign key columns (many ORMs don't auto-index these)
  - Columns used in `WHERE` filters (status, type, email, createdAt)
  - Columns used in `ORDER BY` (createdAt, updatedAt, sortOrder)
  - Columns used in `UNIQUE` constraints (should have unique index)

**Grep patterns**:
```
# Find columns used in WHERE
WHERE\s+\w+\.\w+\s*=          # equality filter
WHERE\s+\w+\s*=                # equality filter (no table prefix)
# Find columns used in ORDER BY
ORDER BY\s+\w+\.\w+           # ordered column
# Prisma where clauses
where:\s*\{\s*\w+:              # Prisma filter field
orderBy:\s*\{\s*\w+:            # Prisma sort field
```

**Severity**: Minor for small tables (<1000 rows). Moderate for medium tables (1K-100K). Major for large tables (100K+) or for columns used in frequently-called queries.

**Note**: This check has lower confidence from static analysis alone. The reviewer should flag it as "Possible" unless table size can be inferred from context (user tables in a SaaS app are likely large).

---

## Detection Priority

When reviewing for performance, check in this order:

1. **N+1 queries** (most common, highest impact, easy to verify)
2. **Missing pagination** (second most common, causes production incidents)
3. **Synchronous blocking** (event loop killers, easy to grep)
4. **Bundle bloat indicators** (affects every user on every page load)
5. **Unbounded list rendering** (DOM performance, memory usage)
6. **Unnecessary re-renders** (cumulative impact, harder to verify statically)
7. **Missing caching** (depends on traffic patterns)
8. **Missing indexes** (needs migration/schema cross-reference)
