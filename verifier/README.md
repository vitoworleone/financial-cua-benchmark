# Verifier refactor workspace

This package is a clean verifier implementation for the public repository. It is an adaptation of the original project's design—not a copy of its legacy modules. In particular, production rule code contains no source-workspace paths, real contract identifiers, or instance-specific golden answers.

## What has been migrated

| Task | What the verifier checks | Test boundary |
| --- | --- | --- |
| `fin_d1_balance_sheet` | Required fields, entity/period/unit, provenance, artifact state, balance equation, asset and liability subtotals, and score caps | Fully synthetic fixtures |
| `fin_d2_cash_flow` | Required fields, entity/period/unit, provenance, artifact state, net-cash-change bridge, opening/closing cash bridge, and score caps | Fully synthetic fixtures |
| `fin_d3_finance_lease_schedule` | Configurable ACT/360 convention, actual days, interest, principal/interest split, period roll-forward, residual, totals, provenance, and submission state | Fully synthetic three-period fixture |

The two modules intentionally exercise the reusable core before more task families are brought across. They demonstrate the expected migration pattern:

1. define only reusable task rules in `src/finbench/tasks/`;
2. keep golden values and adversarial states inside tests or an explicit synthetic development fixture;
3. use a named checker result for each documented condition; and
4. express business-critical failures through transparent score caps rather than hidden heuristics.

## Run the current tests

From this directory in PowerShell:

```powershell
$env:PYTHONPATH = 'src'
python -m pytest -q
```

The current suite contains ten synthetic tests and passes without access to the original workspace.

## Remaining refactor work

- add the shared checker library and task-base composition API only after their public contracts are tested;
- keep the 20 standard tasks distinct from the extra case-based finance-lease adapter;
- rebuild policy-heavy, institution-specific, and reconciliation tasks using the same fixture boundary;
- replace the path-bound finance-lease implementation with a configurable adapter and synthetic public case;
- add documented adversarial probes per migrated task; and
- introduce a registry and evaluation runner only when the release tiers are defined.
