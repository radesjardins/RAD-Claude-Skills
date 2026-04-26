# Tasks — URL Shortener API

Machine-readable task list for the example plan. Pass this to `scripts/plan-lint.py` to see the validators run on a real, valid plan.

### Phase 1: Scaffold (Milestone M1)

- [ ] **[PENDING]** S1: Initialize project + TypeScript strict
  - **Objective:** package.json, tsconfig.json with strict mode, scripts for dev/build/test
  - **Dependencies:** None
  - **Priority:** High
  - **Complexity:** 2
  - **Definition of Done:** `npm run build` exits 0; `tsc --noEmit` passes
  - **Validation:** `npm run build && npx tsc --noEmit`
  - **Rollback:** `git clean -fd && git checkout -- .`
  - **Test Strategy:** No tests yet; validate by running build

- [ ] **[PENDING]** S2: Boot Fastify with health endpoint
  - **Objective:** Minimal server.ts listening on PORT, GET /healthz returning {status:"ok"}
  - **Dependencies:** [S1]
  - **Priority:** High
  - **Complexity:** 2
  - **Definition of Done:** `curl localhost:3000/healthz` returns `{"status":"ok"}`
  - **Validation:** `node --test __tests__/health.test.ts`
  - **Rollback:** `git checkout -- src/server.ts package.json`
  - **Test Strategy:** fastify.inject() asserting 200 + body shape

- [ ] **[PENDING]** S3: PostgreSQL connection + Drizzle schema
  - **Objective:** urls table with id, code, original_url, url_hash, click_count, created_at
  - **Dependencies:** [S1]
  - **Priority:** High
  - **Complexity:** 4
  - **Definition of Done:** Migration applies cleanly to a fresh DB; Drizzle client resolves
  - **Validation:** `npx drizzle-kit migrate && npm run db:smoke`
  - **Rollback:** `npx drizzle-kit drop && git checkout -- migrations/ src/db/`
  - **Test Strategy:** Integration insert+select; mocks NOT used for DB

### Phase 2: Core Service (Milestone M2)

- [ ] **[PENDING]** S4: Shortener service — code generation + persistence
  - **Objective:** generateCode returns existing code if hash matches, else creates new with nanoid(8)
  - **Dependencies:** [S3]
  - **Priority:** High
  - **Complexity:** 5
  - **Definition of Done:** Pure-function tests pass; DB integration test confirms idempotency
  - **Validation:** `npx vitest run __tests__/services/shortener.test.ts`
  - **Rollback:** `git checkout -- src/services/shortener.ts __tests__/services/`
  - **Test Strategy:** Unit (mocked DB) for code gen; integration (real DB) for idempotency. Edge cases: empty URL, URL > 2048 chars, unicode URL.

- [ ] **[PENDING]** S5: POST /shorten route
  - **Objective:** Zod-validate body, call service, return {code, short_url}
  - **Dependencies:** [S4]
  - **Priority:** High
  - **Complexity:** 3
  - **Definition of Done:** 201 on valid URL; 400 on invalid; 200 on duplicate within 24h
  - **Validation:** `npx vitest run __tests__/routes/shorten.test.ts`
  - **Rollback:** `git checkout -- src/routes/shorten.ts src/server.ts`
  - **Test Strategy:** fastify.inject() — happy path, malformed body, duplicate idempotency, oversized URL

- [ ] **[PENDING]** S6: GET /:code redirect + GET /:code/stats
  - **Objective:** Lookup by code, 302 to original + increment counter; stats returns {clicks, created_at}
  - **Dependencies:** [S4]
  - **Priority:** High
  - **Complexity:** 4
  - **Definition of Done:** Unknown code → 404; valid → 302 with Location; stats → 200 with click count
  - **Validation:** `npx vitest run __tests__/routes/redirect.test.ts`
  - **Rollback:** `git checkout -- src/routes/redirect.ts src/server.ts`
  - **Test Strategy:** fastify.inject() for both. Edge cases: nonexistent code, special chars, 0-click stats.

### Phase 3: Concurrency Hardening (Milestone M3)

- [ ] **[PENDING]** S7: Atomic click counter (race fix)
  - **Objective:** Replace SELECT/UPDATE with UPDATE ... RETURNING original_url single-call
  - **Dependencies:** [S6]
  - **Priority:** High
  - **Complexity:** 5
  - **Definition of Done:** 100 concurrent redirects yield count=100 (no lost updates)
  - **Validation:** `npx vitest run __tests__/concurrency/click-counter.test.ts`
  - **Rollback:** `git checkout -- src/services/shortener.ts src/routes/redirect.ts`
  - **Test Strategy:** Promise.all of 100 redirects against same code, assert final count exactly 100. Real DB only.

- [ ] **[PENDING]** S8: URL hash idempotency under concurrent shorten
  - **Objective:** INSERT ... ON CONFLICT (url_hash) DO NOTHING RETURNING code
  - **Dependencies:** [S4, S7]
  - **Priority:** High
  - **Complexity:** 4
  - **Definition of Done:** 50 concurrent shorten calls for same URL yield 1 row + 50 identical responses
  - **Validation:** `npx vitest run __tests__/concurrency/shorten-idempotency.test.ts`
  - **Rollback:** `git checkout -- src/services/shortener.ts`
  - **Test Strategy:** Promise.all of 50 POST /shorten with same URL, assert one code, one DB row.

### Phase 4: Deploy (Milestone M4)

- [ ] **[PENDING]** S9: Dockerfile + docker-compose for local dev
  - **Objective:** Multi-stage build, compose with Postgres
  - **Dependencies:** [S2, S3]
  - **Priority:** Medium
  - **Complexity:** 3
  - **Definition of Done:** `docker compose up` brings API + DB up; healthz returns 200
  - **Validation:** `docker compose up -d && sleep 5 && curl -f localhost:3000/healthz && docker compose down`
  - **Rollback:** `git checkout -- Dockerfile docker-compose.yml .dockerignore && docker compose down -v`
  - **Test Strategy:** Smoke — healthz only

- [ ] **[PENDING]** S10: CI smoke test (GitHub Actions)
  - **Objective:** PR pipeline runs build + lint + test + docker compose smoke
  - **Dependencies:** [S5, S6, S7, S8, S9]
  - **Priority:** Medium
  - **Complexity:** 3
  - **Definition of Done:** PR CI green on clean commit; fails on intentional regression
  - **Validation:** Push no-op commit; CI completes <5min, all jobs green
  - **Rollback:** `git rm .github/workflows/ci.yml`
  - **Test Strategy:** Mutation — comment out click-counter UPDATE, push to feature branch, confirm CI catches it
