# Task packages

Two task contracts have now been normalized as reference migrations:

- [`fin_d1_balance_sheet`](fin_d1_balance_sheet/task.md)
- [`fin_d2_cash_flow`](fin_d2_cash_flow/task.md)
- [`fin_d3_finance_lease_schedule`](fin_d3_finance_lease_schedule/task.md) (configurable case adapter)

They describe the public Agent contract and link to the exact checker IDs implemented in `verifier/`. They are **not** claims that a browser environment, hidden evaluation set, or model run is already released. The remaining source specifications stay represented in [`catalog.yaml`](catalog.yaml) until they receive the same review.

Every migrated task will contain:

```text
task.md        # Agent-visible task contract and observable outputs
SKILL.md       # public, reusable domain knowledge and operational boundary
verifier.md    # checker IDs, scoring, caps, red lines, adversarial states
```

The task package must not include instance-specific golden truth, hidden answer locations, local machine paths, or a claim that a documentation-only task has been run end to end.
