# `fin_d2_cash_flow` verifier contract

Implemented by `verifier/src/finbench/tasks/cash_flow.py`.

| Checker ID | Deterministic condition | Weight |
| --- | --- | ---: |
| `META.IDENTITY` | task ID, entity, period, and scope match | 0.06 |
| `META.UNIT` | unit is declared and supported | 0.04 |
| `SECURITY.INPUT_INTEGRITY` | input hashes and security flags are clean | gate |
| `OUTPUT.COMPLETENESS` | required output artifacts are present | 0.04 |
| `FIELD.CRITICAL` | designated cash fields equal private truth | 0.30 |
| `FIELD.NONCRITICAL` | remaining expected fields equal private truth | 0.28 |
| `RULE.CF.NET_CHANGE` | net change = operating + investing + financing | 0.09 |
| `RULE.CF.CASH_ROLLFORWARD` | closing cash = opening cash + net change | 0.07 |
| `PROVENANCE.FIELD_MAP` | every expected field has source mapping | 0.08 |
| `STATE.SUBMITTED` | backend state is `submitted` | 0.04 |

The weighted score is capped for wrong identity (0.55), unit error (0.70), missing or wrong critical fields (0.65), either broken cash bridge (0.00), and no submission (0.40). Input modification or evaluator-state access returns zero and marks the run as a hack.

Synthetic tests cover golden and blank states plus a broken cash bridge. The richer source design—direct/indirect-method reconciliation, foreign-exchange effects, non-cash disclosures, and restricted-cash policy—will be added only after those data contracts and checks have their own public synthetic fixtures.
