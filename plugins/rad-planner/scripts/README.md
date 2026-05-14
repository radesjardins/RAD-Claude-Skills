# rad-planner scripts

Mechanical validators that complement the `/plan` SKILL.md prompts with deterministic checks an LLM can miss. v4.0 scripts target the canonical doc structure from `docs/doc-conventions.md` (planning/current.md, status.md, vision.md, etc.); v3.0 targeted `tasks.md` (a DAG that has retired in v4.0).

All scripts are pure Python 3.8+ stdlib. No `pip install` required.

The validators surface candidates for user review. They are invoked from `/plan` M6 (post-write validation) and can be run standalone for spot-checks.

## plan-lint.py

Validates `docs/planning/current.md` against the canonical template.

```bash
python3 scripts/plan-lint.py --mode sections docs/planning/current.md     # required-section presence
python3 scripts/plan-lint.py --mode checklist docs/planning/current.md   # field-level checks
python3 scripts/plan-lint.py --mode status docs/planning/current.md      # AC progress
python3 scripts/plan-lint.py --mode all docs/planning/current.md         # sections + checklist
python3 scripts/plan-lint.py --mode all docs/planning/current.md --json  # machine-readable
```

**What `sections` catches:**

- Missing required sections (Objective, Current milestone, Acceptance criteria, Validation commands, Stop conditions, Notes for the next session)
- Empty required sections (or sections containing only template-placeholder content like `[Single clear outcome]`)
- Missing recommended sections (Why this matters, Non-goals, Planned changes, Open questions, Risks) — surfaced as LOW

**What `checklist` catches:**

- Acceptance criteria written as bullets instead of `- [ ]` checkboxes (progress untrackable)
- Vague language in acceptance criteria and validation commands ("verify it works", "should work", "tbd", "looks right", etc.)
- Validation commands that don't look runnable (no backticked command, too short to plausibly be a real check)
- Empty Stop conditions or Notes for the next session

**Exit codes:** `0` clean (or only MEDIUM/LOW warnings), `1` CRITICAL or HIGH issues present, `2` script error.

## status-validator.py

Validates `docs/status.md` against the canonical schema in `docs/status-md-schema.md`.

```bash
python3 scripts/status-validator.py --mode freshness docs/status.md       # mtime vs git HEAD
python3 scripts/status-validator.py --mode sections docs/status.md        # 8-section presence
python3 scripts/status-validator.py --mode evidence docs/status.md        # validation results evidence-based
python3 scripts/status-validator.py --mode read_order docs/status.md      # restart read-order has files
python3 scripts/status-validator.py --mode all docs/status.md --json      # everything + freshness
```

**Freshness thresholds (canonical):**

- `fresh`: < 2 days AND < 5 commits since last status update
- `stale`: > 7 days OR > 20 commits since last status update
- `moderate`: in between

Falls back to file mtime if git isn't available (not in a git repo, no commits yet).

**What `sections` catches:** missing or silently-empty status sections. Empty sections should explicitly say "No data this session — last run YYYY-MM-DD" rather than be blank.

**What `evidence` catches:** vague phrases in Latest validation results ("should pass", "tests pass" without command, "looks good") and missing backticked commands.

**What `read_order` catches:** "If restarting from scratch" section missing or has no file references — this section is load-bearing for `/startup`.

**Exit codes:** `0` clean or freshness-only mode, `1` HIGH issues present, `2` script error.

## doc-redundancy.py

Cross-doc duplicate detection. Compares bullet items and headings across the canonical doc set (`vision.md`, `architecture.md`, `roadmap.md`, `planning/current.md`, `decisions/NNNN-*.md`) using Jaccard token similarity.

```bash
python3 scripts/doc-redundancy.py /path/to/project
python3 scripts/doc-redundancy.py /path/to/project --threshold 0.6
python3 scripts/doc-redundancy.py /path/to/project --json
```

**Severity:**

- `MEDIUM` — similarity ≥ 0.85 (likely duplicate content)
- `LOW` — similarity in [threshold, 0.85) (related content; user judgment)

**What this catches:** the failure mode that drove the planner-first inversion — same non-goals listed verbatim in vision.md AND current.md, same architectural pattern in architecture.md AND a related ADR, etc. Each item should have one canonical home; others should reference rather than copy.

**What this does NOT catch:** semantic equivalence with different wording. "We don't support mobile" vs "Mobile is out of scope" won't match. That's the contradiction validator's softer-recall territory.

**Exit codes:** `0` clean or only LOW findings, `1` any MEDIUM finding, `2` script error.

## doc-contradiction.py

Cross-doc disagreement detection. Flags potential contradictions between docs that should agree.

```bash
python3 scripts/doc-contradiction.py /path/to/project
python3 scripts/doc-contradiction.py /path/to/project --threshold 0.4
python3 scripts/doc-contradiction.py /path/to/project --json
```

**v4.0 check:** `vision.md` non-goals vs `planning/current.md` acceptance criteria — is the plan doing things vision says we won't do?

**Approach:** tokenize both with simple plural stemming, strip negation words from non-goals (so the substantive concept can be matched), compute Jaccard. Flag pairs above threshold for user review.

**Severity is always MEDIUM or LOW** — never CRITICAL/HIGH. The validator surfaces signals; the user judges whether each is a real contradiction or unrelated overlap.

**What this does NOT catch:** semantic contradictions that don't share vocabulary. "We don't optimize for scale" vs "Auth must handle 10k concurrent users" won't match on tokens. That needs natural-language reasoning.

**Future v4.x checks:** architecture.md canonical patterns vs decisions/*.md ADRs; planning/current.md milestone vs status.md last-completed.

**Exit codes:** `0` always (findings are advisory), `2` script error.

## validate-json.py

Validates a JSON payload against a JSON Schema (the rad-planner subagent contracts at `references/subagent-prompts/*.schema.json`). Unchanged from v3.0.

```bash
python3 scripts/validate-json.py <schema.json> <data.json>
echo "$AGENT_OUTPUT" | python3 scripts/validate-json.py <schema> -
python3 scripts/validate-json.py <schema> agent-output.md --extract-from-markdown
python3 scripts/validate-json.py <schema> output.json --json
```

The dispatching skills use this to verify subagent JSON output against the documented contract before consuming it. On failure they re-prompt once with the validation errors before falling back to markdown parsing.

**Exit codes:** `0` valid, `1` invalid, `2` script error.

## Where these get invoked

`/plan` M6 (Doc Creation) runs `plan-lint`, `status-validator`, `doc-redundancy`, and `doc-contradiction` after writing the doc set. Validator results land in the terminal M6 checkpoint under `validator_results`.

`validate-json` is invoked from `/plan` Phase 2 (after `stack-advisor` returns) and Phase 4 (after `risk-assessor` returns) — though these phases retire in v4.0 if/when M5's `--lite` complexity routing makes them optional.

All scripts can be run standalone outside the `/plan` workflow for spot checks during development.

## What these scripts deliberately do NOT do

- **Do not judge plan quality.** Mechanical checks only. "Is this validation command sensible?" is still the LLM's or user's job.
- **Do not catch semantic contradictions.** Token-overlap detection can't model "we say X" vs "we say not-X with different vocabulary." A future v4.x iteration may add lightweight NL reasoning; v4.0 is mechanical.
- **Do not auto-fix.** They report; the user (or a downstream skill invocation) decides what to change.
- **Do not validate the JSON Schemas themselves.** If you edit a `.schema.json`, sanity-check it manually.
