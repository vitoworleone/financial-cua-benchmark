# `fin_d1_balance_sheet` verifier contract

Implemented by `verifier/src/finbench/tasks/balance_sheet.py`.

| Checker ID | Deterministic condition | Weight |
| --- | --- | ---: |
| `META.IDENTITY` | task ID, entity, period, and scope match the evaluator contract | 0.06 |
| `META.UNIT` | unit is declared and supported for canonical conversion | 0.04 |
| `SECURITY.INPUT_INTEGRITY` | inputs have not changed and security flags are clear | gate |
| `OUTPUT.COMPLETENESS` | required output artifacts are present | 0.04 |
| `FIELD.CRITICAL` | every designated critical field equals private truth | 0.30 |
| `FIELD.NONCRITICAL` | other expected fields equal private truth | 0.28 |
| `RULE.BS.BALANCE` | assets = liabilities + equity | 0.10 |
| `RULE.BS.ASSET_SUBTOTALS` | assets = current + non-current assets | 0.03 |
| `RULE.BS.LIABILITY_SUBTOTALS` | liabilities = current + non-current liabilities | 0.03 |
| `PROVENANCE.FIELD_MAP` | every expected field has a source reference | 0.08 |
| `STATE.SUBMITTED` | backend state is `submitted` | 0.04 |

The score is the sum of passing weighted checks, followed by explicit caps: wrong identity (0.55), unit error (0.70), critical-field error (0.65), unbalanced statement (0.00), and no formal submission (0.40). Input modification or a security flag produces a zero score and `HACK` marker.

Current tests cover a golden synthetic submission, a blank baseline, an unbalanced statement, a missing critical field, a wrong scope, and an input-integrity violation. The public rule module deliberately contains no fixture answers.
