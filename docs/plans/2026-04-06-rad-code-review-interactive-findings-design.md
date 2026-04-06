# rad-code-review — Interactive Findings Management Design

**Date:** 2026-04-06
**Status:** Approved for implementation
**Version target:** v2.1 addition

---

## Goal

Add an interactive findings management layer to the end-of-review flow. Users can accept findings as intentional (persisted to `.ucrconfig.yml`), filter to new findings only (compared against `.ucr/history/`), and get a guided numbered menu instead of a free-text command interface.

---

## Context

The existing plugin already has:
- Finding IDs (UCR-NNN format) on every finding
- `.ucrconfig.yml` with a full `accepted_risks` schema (id, description, justification, owner, reviewed_date, expires, finding_match)
- `.ucr/history/` report storage with automatic history comparison in the report
- A fixed 4-option menu at Step 10 of `orchestrate-review.md`

What's missing is the interactive layer: users can't act on findings from within the review session to update `.ucrconfig.yml`, and the history comparison is informational only (not filterable).

---

## Design

### Numbered Interactive Menu (replaces current Step 10 menu)

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

---

### Accept Findings Handler

**Option 4 — Accept specific findings:**

1. Prompt: `Which findings would you like to accept? Enter UCR IDs separated by commas.`
2. Validate IDs exist in current report. If any ID is invalid, list the invalid ones and re-prompt.
3. Prompt: `Optional: add a brief note on why these are intentional? Press Enter to skip.`
4. Write each accepted finding to `.ucrconfig.yml` under `accepted_risks`:

```yaml
- id: "ucr-NNN-[kebab-slug-from-title]"
  description: "[finding title verbatim from report]"
  justification: "[user note, or 'Accepted by reviewer on YYYY-MM-DD — no justification provided']"
  owner: "self"
  reviewed_date: "YYYY-MM-DD"    # today's date
  expires: "YYYY-MM-DD"          # exactly 1 year from today
  finding_match: "[2-3 key terms from finding title]"
```

5. Confirm:
```
Accepted N findings and added to .ucrconfig.yml.
These won't affect your release verdict in future reviews.

Note: accepted risks expire 2027-04-06 and will be re-flagged for re-evaluation.
You can adjust the expiry in .ucrconfig.yml.
```

**Option 5 — Accept all minor:**

Same flow, skips ID prompt. Applies to all Minor-severity findings in current report.
Single optional justification note covers all of them.

---

### Show New Only Handler

**Option 6:**

1. Read `.ucr/history/`, find most recent report file (by filename timestamp).
2. Extract all finding IDs from that report.
3. Filter current findings to those NOT in the previous report.
4. Display:

```
Filtering to new findings only (comparing against YYYY-MM-DD-scope-strictness.md)

Previously reviewed: N findings
Already known:       N  (not shown)
New this review:     N

─────────────────────────────────────────
[findings list, new only]
─────────────────────────────────────────

What would you like to do?
[same numbered menu, scoped to these findings]
```

**Edge cases:**
- No previous report → `No previous review found. Showing all findings.` (no crash)
- Scope mismatch between runs → note: `Previous review used [scope] scope. Comparison may show false positives.`
- All findings are new → show all, note `All findings are new since your last review.`

---

### First-Run `.ucrconfig.yml` Creation

Triggered when: user accepts any findings AND no `.ucrconfig.yml` exists.

```
No .ucrconfig.yml found in this project. Want me to create one?

It will store your accepted findings and let you configure exclusions,
custom rules, and review defaults. Future reviews load it automatically.

1. Yes, create it
2. No thanks — accept for this session only
```

**If yes:**
1. Create `.ucrconfig.yml` from the template at `templates/ucrconfig-template.yml`
2. Populate `accepted_risks` with the accepted findings
3. Prompt:
```
Created .ucrconfig.yml in your project root.

  1. Add .ucrconfig.yml to .gitignore
  2. Leave it as-is (I'll decide later)
```

**If no:**
- Note accepted findings in the session report under "Accepted This Session (not persisted)"
- Do not create `.ucrconfig.yml`
- Accepted findings will reappear on next review

---

## Files Changed

| File | Change |
|------|--------|
| `plugins/rad-code-review/skills/rad-code-review/workflows/orchestrate-review.md` | Step 10: replace 4-option menu with new numbered menu + accept handler + show-new-only handler + first-run `.ucrconfig.yml` prompt |
| `plugins/rad-code-review/ROADMAP.md` | Add interactive findings management to v2.1 |

No other files change. All infrastructure (`.ucrconfig.yml` schema, `.ucr/history/`, finding IDs, template) already exists.

---

## Success Criteria

- [ ] Step 10 shows the new 6-option numbered menu
- [ ] Option 4 prompts for IDs, validates them, prompts for optional justification, writes to `.ucrconfig.yml`
- [ ] Option 5 accepts all minor findings with a single optional justification
- [ ] Option 6 reads history, filters to new findings, handles all edge cases gracefully
- [ ] First-run prompt triggers when accepting findings with no `.ucrconfig.yml` present
- [ ] `.gitignore` offer works correctly
- [ ] ROADMAP.md updated
- [ ] Accepted findings that are invalid IDs are caught and re-prompted, not silently ignored
