# Decision-Class Heuristics — depth-of-planning recommendation

rad-planner v4.9+ uses these heuristics at M0.5 to recommend a planning depth (shallow / standard / deep) before the user confirms or overrides. The framework's rule: **plan deeply only when the decision changes architecture, cost, UX flow, user trust, or product identity.**

This is a heuristic, not a classifier. It misfires ~20% of the time. The user always has the final say at M0.5.

## The five decision classes that warrant deep planning

| Class | Definition | Examples |
|---|---|---|
| **Architecture** | Changes the system's shape, component boundaries, or core data flow | Splitting a monolith, swapping a database, introducing a service boundary, changing the schema, switching deployment model |
| **Cost** | Changes what the project costs to run or who pays | Provider migration, pricing tier introduction, monetization model change, cost-of-goods structure |
| **UX flow** | Changes how a user accomplishes their core task end-to-end | Onboarding redesign, navigation restructure, primary flow rewrite, multi-step process change |
| **User trust** | Changes anything affecting security, privacy, billing, or auth | Auth model change, data retention policy, billing logic, PII handling, encryption-at-rest |
| **Product identity** | Changes what the product fundamentally is or who it's for | Pivot, audience repositioning, vision update, target-user shift |

Anything in these five classes → recommend **deep** unless the user pre-overrides.

## What warrants standard depth

Standard M1–M5 conversation is the default. Use when:

- A new milestone within an existing plan
- Feature additions that don't change architecture / cost / UX flow / trust / identity
- Medium-sized refactors within one module
- Doc-set updates that affect more than one canonical file
- Any work where the agent or user wants the M1–M5 discipline even though it's not strictly architecturally load-bearing

When in doubt between shallow and standard → standard. The cost of one extra conversation turn is low; the cost of an undocumented small change is "it adds up over a project."

## What warrants shallow

Shallow skips M1–M5 entirely. Update `current.md` with the change in-place. Use when:

- Cosmetic copy fixes (button labels, microcopy, error messages — when they don't change semantics)
- Minor layout tweaks (spacing, alignment, color within an existing theme)
- Single-file micro-refactors (extract a function, rename a variable, inline a constant)
- Doc-only updates that don't affect canonical strategic docs
- Test additions or test-only changes
- Comment/documentation fixes in code

**Never shallow when:** the change touches `lib/auth/`, billing/pricing modules, security boundaries, schema files, or anything mentioned in the operating manual's Hard boundaries.

## Cue patterns — utterance keywords

The heuristic scans the user's invocation utterance for keyword signals. Patterns are case-insensitive and match anywhere in the utterance.

### Shallow cues

```
fix typo
typo in
rename button
button label
tweak (copy|label|wording|text)
adjust (layout|spacing|alignment|color|margin|padding)
update (copy|wording|text|microcopy)
small fix
quick fix
cosmetic
polish
tighten (wording|copy|text)
```

### Deep cues

```
redesign
rewrite (auth|pricing|billing|schema|architecture)
pivot
new (pricing|tier|billing|business model)
change (auth|data model|schema|architecture)
refactor (everything|the whole|all of)
introduce (a new|new) (service|module|package|database)
swap (database|provider|framework)
SSO
multi-tenant
GDPR|HIPAA|compliance
```

### Default → standard

Anything that doesn't match shallow OR deep cues defaults to standard.

## Cue patterns — state signals

Used when utterance keywords are ambiguous:

| State signal | Suggests |
|---|---|
| Utterance mentions only files in `app/` UI directory | shallow likely |
| Utterance mentions `lib/auth/`, `lib/billing/`, schema files, or migrations | deep likely |
| Existing milestone is mid-flight AND utterance describes additions to it | standard |
| Existing milestone is mid-flight AND utterance describes scope changes | deep |
| Greenfield (no `docs/planning/current.md`) | standard or deep (lean standard unless deep cues fire) |
| User has invoked `--auto` | depth still classifies, but only controls whether risk-assessor runs at M4 |

## Cue patterns — vision.md non-goals match

If the utterance describes work that matches a `vision.md` non-goal, the heuristic offers **parking** as a fourth option in M0.5 alongside the depth choices:

> "This sounds like the 'social features' non-goal from `vision.md`. Three options:
> 1. Confirm it's still a non-goal — close the conversation
> 2. Park for later — append to `docs/planning/parked.md`
> 3. Promote — remove from non-goals and plan it deeply (vision change is itself a deep decision)"

## Rendering the recommendation

The M0.5 surface adds one line after "Or you could start with":

```
**Recommended depth:** {shallow|standard|deep} — {one-sentence rationale citing the dominant cue}
```

Rationale should be specific and grounded:

- ✅ "Looks like a copy-only fix to the signup button label; no auth, schema, or pricing impact"
- ✅ "Mentions rewriting `lib/auth/` — this is a user-trust change, recommending deep with the risk-assessor pass at M4"
- ❌ "Inferred shallow" (no rationale)
- ❌ "Standard depth recommended" (no cue cited)

## When the heuristic is wrong

- **User can override at M0.5** by naming a different depth in their reply ("Standard please" / "Deep — run risk-assessor" / "Shallow is fine")
- **User can pre-override with `--depth`** flag on invocation
- **Misfire rate is real.** ~20% of recommendations will be wrong. Surface this honestly in the rationale when the cue is weak ("Weak signal — falling back to standard; override with --depth if you have a stronger read")

## What does NOT belong in this heuristic

- **No ML/embedding-based classification.** Pure keyword + state + file-scope pattern matching only. Stays pure-stdlib.
- **No project-specific learned thresholds.** The heuristic is universal; per-project tuning happens via `--depth` flag overrides, not via state tracking.
- **No confidence score on the surface.** The user sees the depth + the one-sentence rationale; they decide whether the heuristic is right for their case.

## Cross-reference

This heuristic is part of the build-readiness gate alignment. The full design rationale is in `C:\Dev\plans\2026-05-16-rad-planner-anti-drift-design.md` (Wave 4 / M6).
