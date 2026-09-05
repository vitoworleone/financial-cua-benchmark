# 融资租赁 ACT/360 摊还表复核 / Finance-lease schedule review

```yaml
task_id: fin_d3_finance_lease_schedule
task_version: 0.1.0-public-refactor
track: financial_accounting
kind: configurable_case_adapter
status: verifier_refactored_synthetic_tests_only
```

## Purpose

The Agent reviews and submits an effective-interest amortization schedule for a finance lease. Unlike a fixed client case, this task is an adapter: every instance injects its own de-identified lease start date, payment dates, cash flows, annual rate, and release policy. The public verifier retains only the calculation rules.

## Public task contract

The Agent receives an approved schedule source, the permitted source range, a versioned convention such as `ACT/360`, reporting metadata, a target template, and read-only source hashes. It must produce a structured schedule with each period's opening principal, actual days, cash paid, interest, principal, closing principal, totals, provenance, and submitted state.

For a given period:

```text
interest = round(opening principal × annual rate × actual days / 360, 2)
principal = cash paid − interest
closing principal = opening principal − principal
```

The initial opening balance, each payment, and the final residual come from the instance; they are not built into the verifier.

## Observable requirements

- periods must be consecutively numbered and match the instance's payment-date sequence;
- day counts must be recomputed from the start date and prior payment date;
- each interest, principal, and closing balance must reconcile;
- aggregate cash, interest, principal, and ending principal must reconcile to the submitted schedule and private truth;
- each submitted schedule and total must have a provenance reference; and
- the final backend state must be `submitted`.

## Boundary and release status

The public package has a generic deterministic verifier and a fictitious three-period synthetic test. It does not include any original workbook, actual payment schedule, client identifier, or local path. It is a case adapter beside—not inside—the 20-task standard catalog, and it does not imply release of a private evaluation instance.
