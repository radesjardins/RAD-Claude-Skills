# rad-planner fixtures

End-to-end test fixtures for the v4.0 validators. Two fixtures, each exercising a different validator path:

- **`standard-project/`** — a realistic healthy v4.0 project. All four validators should pass cleanly. Use this as a reference for what `/plan` M6 output looks like when everything's working.
- **`intentionally-broken/`** — a deliberately broken project that triggers each validator's failure detection. Use this to verify the validators are catching what they should.

These fixtures are not Python tests — they're scripted markdown files that the validators read. Run validators against them manually:

```bash
# Against the good fixture (everything should pass)
cd plugins/rad-planner
python3 scripts/plan-lint.py fixtures/standard-project/docs/planning/current.md
python3 scripts/status-validator.py fixtures/standard-project/docs/status.md
python3 scripts/doc-redundancy.py fixtures/standard-project
python3 scripts/doc-contradiction.py fixtures/standard-project

# Against the broken fixture (each validator should flag specific issues)
python3 scripts/plan-lint.py fixtures/intentionally-broken/docs/planning/current.md
python3 scripts/status-validator.py fixtures/intentionally-broken/docs/status.md
python3 scripts/doc-redundancy.py fixtures/intentionally-broken
python3 scripts/doc-contradiction.py fixtures/intentionally-broken
```

## standard-project

Theme: Wayfinder, a weather-aware trip planning tool for outdoor enthusiasts. Represents a mid-flight v4.0 project at the start of milestone M2 (activity-constraint engine), with M1 complete.

**Project state captured:**

- Operating manual (`CLAUDE.md`): full Constitution + Operational sections; Claude-only scope
- Strategic docs: `vision.md`, `architecture.md`, `docs/decisions/0001-use-typescript-strict.md`
- Planning: `planning/current.md` with M2 in progress (1 of 5 acceptance criteria complete)
- Status: `status.md` populated from a recent /wrapup
- Config: `.rad/profile` with `mode = mentor`, `agent_scope = claude_only`

**Expected validator output:** all four pass cleanly. No issues, no warnings, exit 0.

**Acceptable variations:** `doc-redundancy` may surface LOW findings for adjacent-but-not-identical content; those are informational, not errors. The validator's MEDIUM threshold catches actual duplication.

## intentionally-broken

A minimal broken project. Deliberately exercises specific validator failure paths so the validators' detection logic is testable.

**Built-in failures:**

| Validator | Flagged issue | Severity |
|---|---|---|
| `plan-lint` | Missing required sections (`Stop conditions`, `Notes for the next session`) | CRITICAL |
| `plan-lint` | Acceptance criteria using bullets instead of checkboxes | HIGH |
| `plan-lint` | Vague phrases in acceptance criteria ("Verify it works", "Test it manually") | HIGH |
| `plan-lint` | Vague phrases in validation commands ("tbd", "should work") | HIGH |
| `plan-lint` | Suspiciously short Objective | MEDIUM |
| `status-validator` | Missing 5 of 8 required sections | HIGH |
| `status-validator` | Vague validation results ("should pass", "looks good"; no backticked commands) | HIGH |
| `doc-redundancy` | Same non-goal verbatim in `vision.md` AND `current.md` | MEDIUM (similarity=1.0) |
| `doc-contradiction` | `vision.md` non-goal "Not building native mobile apps for v1" overlaps with `current.md` AC "Native mobile app onboarding flow works for v1 users" | LOW (overlap≈0.44) |

**Expected exit codes:**

- `plan-lint`: 1 (CRITICAL + HIGH)
- `status-validator`: 1 (HIGH)
- `doc-redundancy`: 1 (MEDIUM)
- `doc-contradiction`: 0 (always advisory)

## Coverage notes

The fixtures focus on **mechanical validator behavior**. They don't (and can't) test the conversational `/plan` workflow itself — that's covered by manual exploration during real project use.

For the four entry points × three agent scopes × two modes (24 combinations), each fixture represents one slice:

- `standard-project`: improvement-entry-flavored, `claude_only`, `mentor` mode
- `intentionally-broken`: shape-agnostic — exists to exercise validator failure detection

If you want to test other combinations (e.g., codex-only or pivot-entry-shaped state), copy `standard-project` and adjust. The validators don't care about agent scope or mode (those are M0 discovery concerns); they care about doc structure and content.

## Updating fixtures

When validators change (new checks, new thresholds), re-run them against both fixtures and update either the fixture content or this README's expected-output table. The fixtures are a regression check: if the broken fixture stops failing, or the standard one starts failing, something in the validators drifted.
