# Benchmark positioning

## The problem

Many AI evaluations stop at whether a model can produce a plausible answer, a filled-looking document, or a screenshot that appears successful. Financial work requires stronger evidence. A valid output must use the right entity, period, scope, unit, policy version, field mapping, arithmetic relationship, source traceability, and final submission state.

The benchmark therefore asks a narrower but operational question:

> Can an Agent move a controlled financial work environment from a known initial state to a correct, observable, reviewable final state without changing protected inputs or bypassing the intended boundary?

## What this benchmark is and is not

| This benchmark is | This benchmark is not |
| --- | --- |
| A task, state, and verifier design for financial CUA / Agent evaluation | An investment, audit, tax, legal, underwriting, or regulatory decision system |
| A deterministic scoring architecture for checkable financial outputs | A generic LLM-as-judge benchmark for polished narrative text |
| A way to assess human-in-the-loop preparation work | Evidence that an Agent may issue professional conclusions or submit to real systems |
| A public methodology plus a controlled release strategy | A repository that publishes every answer, test instance, or golden state |

## Task-design unit

Each task must define the same contract before implementation begins:

```text
Intent
→ Agent-visible inputs and constraints
→ Reproducible initial state
→ Required observable outputs and state transition
→ Hidden gold state / independently computed truth
→ Deterministic verifier and explicit human-review boundary
```

This avoids a common failure mode: task instructions, setup scripts, golden answers, and verifiers are written independently and then silently disagree.

## Evidence levels

Every public claim is classified as one of these levels:

| Label | Meaning |
| --- | --- |
| `design` | Task, verifier, or protocol has been specified but not run as an end-to-end benchmark |
| `implemented` | Code exists and can be inspected or unit-tested |
| `self-tested` | Golden/initial or other controlled self-tests have passed |
| `adversarially-probed` | Defined error mutations have been executed and checked |
| `agent-evaluated` | A documented Agent run produced a reportable result |

The repository must never promote an asset to a higher level without a corresponding reproducible artifact.
