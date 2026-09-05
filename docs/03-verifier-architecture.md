# Verifier architecture

## Design target

The verifier must distinguish a plausible file from a completed financial task. It should evaluate the final observable state and preserve diagnostic evidence.

```text
submission + final environment state + initial snapshot
        + policy + hidden truth + upstream versions
                              ↓
                         preflight gates
                              ↓
                   normalization and checker set
                              ↓
                  weighted base score + hard caps
                              ↓
       reward.json + scoring_detail.json + canonical summary hash
```

## Layers to preserve during refactor

| Layer | Responsibility | Refactor decision |
| --- | --- | --- |
| Contracts | typed submission, ground truth, policy, initial snapshot, checks, reward | keep concept; review public/private boundaries |
| Core | normalization, preflight, hack detection, score aggregation, canonical outputs | keep concept; remove unsafe defaults and document interfaces |
| Checkers | reusable field truth, equations, completeness, metadata, provenance, state checks | retain after test-driven cleanup |
| Task base | task checker table, caps, red lines, pass threshold | retain; make immutable registry configuration explicit |
| Registry | task discovery, CLI, required deliverables | rewrite to separate the 20 standard tasks from case adapters |
| Task modules | task-specific rule graph, weights, caps, policy requirements | migrate one task at a time; remove embedded fixture truth |
| Fixtures/tests | golden, initial, adversarial mutations, synthetic raw inputs | move out of production modules into explicit test/development packages |
| Case adapters | high-fidelity source-layout parsing and instance policy | rebuild with configuration and synthetic or deliberately released inputs |

## Checker categories

### 1. Preflight

Checks task/version, policy applicability, upstream manifests, input integrity, entity/period/scope, unit readability, and environment adapter availability. Infrastructure failure must be visible as infrastructure failure, not silently counted as model failure.

### 2. External truth

Compares submitted fields with hidden or independently recomputed expected values. Critical concepts are scored separately from noncritical fields.

### 3. Internal consistency

Recomputes equations from the submission itself: statement balance, subtotal, rollforward, tax formula, capital ratio, or other task-specific relationships. This catches inconsistencies but never replaces truth comparison: two wrong fields can still balance.

### 4. Provenance and deliverables

Requires the declared output files, concept-to-field mapping, source pointers, and actual submitted state. “The document says submitted” is not proof that the backend state is submitted.

### 5. Security and anti-hack gates

Protected-input mutation, hidden-truth access, backend tampering, scope escape, or PII injection are hard failures. A correct-looking result obtained through a prohibited path is not a successful task.

## Score semantics

The score must expose both a diagnostic base score and the reportable score after caps:

```text
base score = sum(PASS checker weights)
reportable score = apply_caps(base score, triggered gates)
```

Typical caps include wrong entity/scope, wrong unit, missing critical fields, failed red-line equation, no structured state, and no actual submission. A pass requires the threshold *and* required critical gates.

## Why fixtures must leave task modules

The legacy engine stores `GOLDEN_FIELDS` and, in some cases, policy/data fixtures directly in task modules. This is useful for self-tests, but it creates two problems in a public benchmark:

1. production verifier imports contain answer-like data and can make the release boundary ambiguous;
2. instance generation can fall back to fabricating input from golden fields, reversing the correct direction of task construction.

The refactor must use this structure instead:

```text
verifier/
  finbench/
    core/              # no task answers
    tasks/             # task rules; no instance values
  tests/
    fixtures/          # synthetic golden/initial/adversarial data
  dev_instances/       # explicit public development instances
```

## Evidence labels for current code

The current engine has passed a local C3/C4 self-test for 21 registered modules: golden fixture scores `1.0`, initial fixture scores `0.0`. Five representative task families have adversarial probes. These are meaningful engineering signals, but they are not yet Agent leaderboard results or proof that all GUI/task environments are runnable end to end.
