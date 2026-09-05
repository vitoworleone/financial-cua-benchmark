# 企业资产负债表填报 / Balance-sheet filing

```yaml
task_id: fin_d1_balance_sheet
task_version: 0.2.0-public-refactor
track: financial_accounting
difficulty: D1
status: verifier_refactored_synthetic_tests_only
environment_status: adapter_contract_only
```

## Purpose

The Agent transfers a canonical balance sheet into a target reporting form, preserves entity, period, reporting scope and unit, then leaves an observable submitted final state. This task evaluates controlled filing work; it does not ask the Agent to derive accounting policy or extract statements from a PDF.

## Public task contract

The runtime must provide a de-identified entity, reporting period, `separate` or `consolidated` scope, declared display unit, canonical source values, target-field guide, read-only input manifest, and an output location. The Agent must:

1. choose the required entity, period, scope and unit;
2. populate every applicable target field without replacing undisclosed values with zero;
3. retain a field-to-source mapping for each submitted field;
4. save and submit through the approved environment interface; and
5. record only genuine exceptions in its processing notes.

The public contract never exposes golden field values, verifier paths, or a score threshold.

## Observable deliverables

| Deliverable | Minimum observable evidence |
| --- | --- |
| Filed form | Final backend-readable field values and `submitted` state |
| Submission manifest | Concept/field/source-pointer mapping for every applicable field |
| Processing notes | Actual ambiguity, unit, or environment issue—or an explicit no-exception note |
| Input integrity | Original source hashes remain unchanged |

## Business invariants

After normalization to yuan, the form must satisfy:

```text
total assets = total liabilities + total equity
total assets = current assets + non-current assets
total liabilities = current liabilities + non-current liabilities
```

Internal balance is necessary but insufficient: independently wrong fields that happen to balance must still fail truth and provenance checks.

## Evaluation boundary

The refactored Python verifier currently covers metadata, unit recognition, input integrity flags, required artifacts, critical/non-critical field truth, the three equations, provenance, submission state, and transparent caps. See [verifier contract](verifier.md).

Its tests use only synthetic values and a state object; there is no released browser runner, hidden benchmark split, or Agent leaderboard. A future environment adapter must expose the same observable state without changing the task contract.
