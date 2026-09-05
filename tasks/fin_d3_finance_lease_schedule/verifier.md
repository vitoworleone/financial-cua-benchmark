# `fin_d3_finance_lease_schedule` verifier contract

Implemented by `verifier/src/finbench/tasks/lease_schedule.py`. Configuration is supplied as a `LeasePolicy`; instance truth is supplied at runtime through `GroundTruth`.

| Checker ID | Deterministic condition | Weight |
| --- | --- | ---: |
| `META.IDENTITY` | task, entity, period, and scope match | 0.06 |
| `META.UNIT` | reporting unit is supported | 0.04 |
| `SECURITY.INPUT_INTEGRITY` | source hash and security flags are clean | gate |
| `OUTPUT.COMPLETENESS` | required output artifacts exist | 0.04 |
| `CONVENTION.ACT360` | convention is ACT/360 and policy rate is finite and positive | 0.05 |
| `PERIOD.COMPLETENESS` | all expected periods appear in sequence | 0.08 |
| `PERIOD.DATES_AND_DAYS` | payment dates and actual day counts reconcile | 0.12 |
| `RULE.ACT360_INTEREST` | each period's interest is recomputed from policy | 0.17 |
| `RULE.PRINCIPAL_INTEREST_SPLIT` | cash = interest + principal | 0.10 |
| `RULE.PERIOD_ROLLFORWARD` | opening/closing principal rolls forward and residual converges | 0.15 |
| `RULE.TOTALS_AND_RESIDUAL` | submitted totals equal calculated and evaluator values | 0.10 |
| `PROVENANCE.FIELD_MAP` | schedule and derived totals point to permitted sources | 0.05 |
| `STATE.SUBMITTED` | final backend state is `submitted` | 0.04 |

An invalid convention, incomplete schedule, incorrect dates/days, incorrect ACT/360 interest, broken roll-forward, or totals failure is a zero-score hard failure. Formal non-submission caps the score at 0.40. Protected-input mutation or a security flag returns zero and marks the result as a hack.

The test fixture is deliberately fictional and contains three periods only. It covers a golden result, wrong convention, an incorrect-but-still-arithmetically-balanced interest/principal split, and input mutation.
