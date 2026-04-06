# rad-code-review Interactive Findings Management — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the fixed 4-option end-of-review menu in orchestrate-review.md with a numbered interactive menu that lets users accept findings to `.ucrconfig.yml`, filter to new-only findings, and get guided prompts for fixes.

**Architecture:** Two markdown workflow files change. Step 10 of `orchestrate-review.md` gets a new menu and inline handlers for accept (options 4-5) and show-new-only (option 6). Fix options (1-3) continue delegating to the existing `offer-fixes.md` workflow. ROADMAP.md gets a v2.1 entry for this feature.

**Tech Stack:** Markdown workflow files, YAML (`.ucrconfig.yml`), bash (git commands in workflow)

---

## Files Modified

| File | Lines affected | What changes |
|------|---------------|--------------|
| `plugins/rad-code-review/skills/rad-code-review/workflows/orchestrate-review.md` | Step 10 (~line 689 to ~line 734) | Replace 4-option menu with 6-option numbered menu + accept handlers + show-new-only handler + first-run `.ucrconfig.yml` prompt |
| `plugins/rad-code-review/ROADMAP.md` | v2.1 section | Add interactive findings management bullet |

---

## Task 1: Replace Step 10 in orchestrate-review.md

**Files:**
- Modify: `plugins/rad-code-review/skills/rad-code-review/workflows/orchestrate-review.md`

- [ ] **Step 1: Read the current file**

  Read `plugins/rad-code-review/skills/rad-code-review/workflows/orchestrate-review.md` in full.
  Locate `## Step 10: Present Findings to User`. It currently ends with a 4-option menu block:
  ```
  What would you like to do?
  1. View full findings (by severity or by category)
  2. Apply fixes — choose preset:
  ...
  4. Generate report and apply fixes
  ```
  Note the exact line numbers of the `Then ask:` paragraph and the menu code block — this is what gets replaced.

- [ ] **Step 2: Replace the menu and add handlers**

  Keep everything in Step 10 up to and including the summary display block (finding summary table, release verdict, top findings). Replace ONLY the `Then ask:` paragraph and the menu code block that follows it with the full content below.

  Replace from `Then ask:` to the end of Step 10 with:

  ````markdown
  Then display the interactive menu:

  ```
  What would you like to do?

  Fix Findings
    1. Fix all blockers
    2. Fix specific findings          (I'll ask which UCRs)
    3. Get details on a finding       (I'll ask which one)

  Accept Findings  ← marks as intentional; won't affect verdict, tracked in .ucrconfig.yml
    4. Accept specific findings       (I'll ask which UCRs)
    5. Accept all minor findings

  View
    6. Show new findings only         (compares against your previous review)

  Or type a UCR ID directly (e.g. UCR-003), or ask me anything about the findings.
  ```

  ### Option 1: Fix all blockers
  Load and execute `${UCR_DIR}/workflows/offer-fixes.md` with preset `blockers`.

  ### Option 2: Fix specific findings
  Prompt: `Which UCR IDs would you like to fix? Enter IDs separated by commas (e.g. UCR-001, UCR-003).`
  Load and execute `${UCR_DIR}/workflows/offer-fixes.md` with the specified IDs.

  ### Option 3: Get details on a finding
  Prompt: `Which UCR ID would you like more details on?`
  Display the full finding entry for that ID: description, evidence, impact, recommendation, and references.
  Return to the menu.

  ### Option 4: Accept specific findings

  Prompt:
  ```
  Which findings would you like to accept? Enter UCR IDs separated by commas.
  (e.g. UCR-004, UCR-007)
  ```

  Validate that each provided ID exists in the current report's findings list.
  If any ID is not found, respond:
  ```
  These IDs were not found in the current report: UCR-XXX
  Please check the finding IDs above and try again.
  ```
  Re-prompt until all IDs are valid or the user cancels.

  Then prompt:
  ```
  Optional: add a brief note on why these are intentional?
  This helps future-you remember the reasoning.
  (e.g. "auth handled by upstream middleware", "intentional for MVP scope")
  Press Enter to skip.
  ```

  Capture the justification (or use `"Accepted by reviewer on {today} — no justification provided"` if skipped).

  Compute dates:
  - `reviewed_date` = today in ISO 8601 format (YYYY-MM-DD)
  - `expires` = exactly one year from today in ISO 8601 format

  For each accepted finding ID, build a `.ucrconfig.yml` entry:
  ```yaml
  - id: "{finding-id-lowercased}-{kebab-slug-of-first-5-words-of-title}"
    description: "{verbatim finding title from report}"
    justification: "{user note or default justification string}"
    owner: "self"
    reviewed_date: "{today}"
    expires: "{one year from today}"
    finding_match: "{2-3 key terms extracted from finding title, space-separated}"
  ```

  **Check for `.ucrconfig.yml`:**

  ```bash
  ls .ucrconfig.yml 2>/dev/null
  ```

  **If `.ucrconfig.yml` does NOT exist**, prompt:
  ```
  No .ucrconfig.yml found in this project. Want me to create one?

  It will store your accepted findings and let you configure exclusions,
  custom rules, and review defaults. Future reviews load it automatically.

    1. Yes, create it
    2. No thanks — accept for this session only
  ```

  If user chooses **1 (Yes)**:
  - Read `${UCR_DIR}/templates/ucrconfig-template.yml`
  - Write it to `.ucrconfig.yml` in the repository root
  - Append the accepted findings entries under the `accepted_risks:` key
  - Then prompt:
    ```
    Created .ucrconfig.yml in your project root.

      1. Add .ucrconfig.yml to .gitignore
      2. Leave it as-is (I'll decide later)
    ```
  - If user chooses **1**: run `echo ".ucrconfig.yml" >> .gitignore` (append only if not already present — check first with grep)
  - Confirm: `.ucrconfig.yml added to .gitignore`

  If user chooses **2 (No thanks)**:
  - Do not create `.ucrconfig.yml`
  - Note the accepted findings in the session output:
    ```
    Accepted for this session only (not persisted):
    {list of accepted finding IDs and titles}
    These will reappear in your next review.
    ```
  - Return to menu.

  **If `.ucrconfig.yml` DOES exist**:
  - Read the file
  - Append the new entries under `accepted_risks:`
  - Write the updated file back

  Confirm acceptance:
  ```
  Accepted {N} findings and added to .ucrconfig.yml.
  These won't affect your release verdict in future reviews.

  Note: accepted risks expire {expires date} and will be re-flagged for
  re-evaluation. You can adjust the expiry in .ucrconfig.yml.
  ```

  Return to menu.

  ### Option 5: Accept all minor findings

  Identify all findings with severity `minor` in the current report.

  If no minor findings exist:
  ```
  No minor findings in this review.
  ```
  Return to menu.

  Otherwise, list them:
  ```
  Found {N} minor findings:
  {list of UCR IDs and titles}

  Optional: add a brief note on why these are intentional? Press Enter to skip.
  ```

  Capture justification (same default as Option 4 if skipped).

  Apply the same `.ucrconfig.yml` write logic as Option 4 (check exists, create if not, append entries, offer `.gitignore`).

  Confirm:
  ```
  Accepted {N} minor findings and added to .ucrconfig.yml.
  Note: accepted risks expire {expires date}.
  ```

  Return to menu.

  ### Option 6: Show new findings only

  ```bash
  ls -t .ucr/history/*.md 2>/dev/null | head -1
  ```

  **If no previous report exists**:
  ```
  No previous review found for this project. Showing all findings.
  ```
  Return to menu without filtering.

  **If a previous report exists**:
  - Read the most recent report file from `.ucr/history/`
  - Extract all UCR IDs present in that report (grep for `UCR-[0-9]+` pattern)
  - Identify the scope and strictness used in the previous report from its filename (format: `YYYY-MM-DD-{scope}-{strictness}.md`)
  - Filter current findings to those whose ID does NOT appear in the previous report

  If the previous report used a different scope than the current review, note:
  ```
  Note: previous review used {previous_scope} scope. This review used {current_scope}.
  Comparison may not be exact.
  ```

  Display:
  ```
  Filtering to new findings only (comparing against {previous_report_filename})

  Previously reviewed: {total_previous} findings
  Already known:       {matched} (not shown)
  New this review:     {new_count}

  ─────────────────────────────────────────
  {new findings only, formatted as: [SEVERITY] UCR-NNN — Title}
  ─────────────────────────────────────────
  ```

  If all findings are new:
  ```
  All {N} findings are new since your last review.
  ```

  If no new findings:
  ```
  No new findings since your last review. All {N} findings were present
  in the previous report.
  ```

  Redisplay the menu scoped to the new findings (options 1-5 operate on the filtered set).

  ### UCR ID typed directly
  If the user types a UCR ID (matches pattern `UCR-[0-9]+`), display the full finding detail for that ID (same as Option 3). Return to menu.

  ### Free text / question
  Answer the question using the current findings as context. Return to menu.

  ### Exit
  If the user types "done", "exit", "quit", or presses Enter with no input, proceed to Step 11 (Fix Application) if fixes were requested, or Step 12 (Report Generation).
  ````

- [ ] **Step 3: Verify the edit**

  Read the updated `orchestrate-review.md`. Confirm:
  - The old 4-option menu (`View full findings`, `Apply fixes`, `Generate full report`, `Generate report and apply fixes`) is gone
  - The new 6-option menu is present
  - All 6 option handlers are present (Options 1-6, UCR ID direct, free text, exit)
  - The existing summary display block (finding summary table, release verdict, top findings) is unchanged above the new menu

- [ ] **Step 4: Commit**

  ```bash
  git add plugins/rad-code-review/skills/rad-code-review/workflows/orchestrate-review.md
  git commit -m "feat(rad-code-review): add interactive findings management to Step 10

  - Numbered 6-option menu replaces fixed 4-option menu
  - Option 4: accept specific findings -> writes to .ucrconfig.yml
  - Option 5: accept all minor findings
  - Option 6: show new findings only (compares against .ucr/history/)
  - First-run .ucrconfig.yml creation with .gitignore offer
  - Expiry auto-set to 1 year with user notification
  - Invalid UCR ID validation with re-prompt
  - Edge cases: no previous report, scope mismatch, no minor findings"
  ```

---

## Task 2: Update ROADMAP.md

**Files:**
- Modify: `plugins/rad-code-review/ROADMAP.md`

- [ ] **Step 1: Read the current ROADMAP.md**

  Read `plugins/rad-code-review/ROADMAP.md`. Locate the `## v2.1 (planned)` section. It currently lists:
  - Threat model mode
  - API contract review
  - Schema/migration review
  - Infra/deploy config deep review

- [ ] **Step 2: Add the new bullet**

  Add the following as the FIRST bullet under `## v2.1 (planned)`, before the existing entries:

  ```markdown
  - **Interactive findings management** — Numbered end-of-review menu with accept, fix, and filter options. Accept specific findings or all minor findings as intentional; they are persisted to `.ucrconfig.yml` with expiry dates and optional justification notes. Show-new-only mode filters the current report against `.ucr/history/` to surface only findings introduced since the last review. First-run `.ucrconfig.yml` creation with optional `.gitignore` integration.
  ```

- [ ] **Step 3: Verify**

  Read the updated ROADMAP.md. Confirm the new bullet is the first entry under v2.1 and existing bullets are unchanged.

- [ ] **Step 4: Commit**

  ```bash
  git add plugins/rad-code-review/ROADMAP.md
  git commit -m "docs(rad-code-review): add interactive findings management to v2.1 roadmap"
  ```

---

## Task 3: Push

- [ ] **Step 1: Push to remote**

  ```bash
  git push origin main
  ```

  Expected: `main -> main` with the two new commits listed.

- [ ] **Step 2: Verify**

  ```bash
  git log --oneline -5
  ```

  Expected: two new commits visible at the top:
  - `docs(rad-code-review): add interactive findings management to v2.1 roadmap`
  - `feat(rad-code-review): add interactive findings management to Step 10`
