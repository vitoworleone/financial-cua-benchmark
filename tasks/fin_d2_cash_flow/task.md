# 现金流量表填报 / Cash-flow filing

```yaml
task_id: fin_d2_cash_flow
task_version: 0.2.0-public-refactor
track: financial_accounting
difficulty: D2
status: verifier_refactored_synthetic_tests_only
environment_status: adapter_contract_only
```

## Purpose

The Agent completes a normalized cash-flow reporting form from supplied canonical amounts. It must preserve metadata and units, produce a submitted state, and maintain the primary cash bridges. The current public refactor focuses on directly observable, deterministic invariants; it does not yet claim a full direct-method/indirect-method browser task release.

## Public task contract

The instance provides a de-identified entity, reporting period, scope, unit, canonical input, target-field guide, required output artifacts and read-only input hashes. The Agent must:

1. select the specified entity, period, scope and unit;
2. file the operating, investing, financing, net-change, opening-cash and closing-cash fields;
3. preserve source mapping for every expected field;
4. submit through the approved environment; and
5. avoid altering input materials or using evaluator-only state.

## Business invariants

```text
net change in cash = operating + investing + financing cash flow
closing cash = opening cash + net change in cash
```

All arithmetic is performed after canonical unit normalization. In a later full task package, any exchange-rate effect and direct/indirect-method bridge will be explicit fields rather than silently absorbed into these equations.

## Evaluation boundary

The clean verifier validates final state, not a prescribed click sequence. It checks input integrity, metadata, unit, artifacts, field truth, both cash bridges, provenance and submission. Tests are synthetic; no claim is made yet about a released hidden set, an end-to-end CUA environment, or model performance. See [verifier contract](verifier.md).
