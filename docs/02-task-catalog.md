# Task catalog

## Catalog convention

The financial-accounting suite contains **20 standard benchmark tasks**. A separate finance-lease case module exists for an instance-specific schedule verification scenario; it is not counted as a twenty-first general task.

The bond-underwriting track currently contains six task designs. They are part of the public design catalog, not yet claims of completed runnable verifier implementations.

## Track A — Financial accounting: 20 standard tasks

| ID | Difficulty | Task | Core capability |
| --- | --- | --- | --- |
| `fin_d1_balance_sheet` | D1 | Balance-sheet filing | concept mapping, units, periods, statement balance, submission state |
| `fin_d1_income_statement` | D1 | Income-statement filing | staged profit construction, precision, current/comparative periods |
| `fin_d2_cash_flow` | D2 | Cash-flow statement | direct/indirect method, rollforward, cross-statement checks |
| `fin_d2_three_statements` | D2 | Three-statement package | multi-deliverable dependency and cross-statement consistency |
| `fin_d2_equity_changes` | D2 | Statement of changes in equity | column rollforward, OCI, parent/NCI treatment |
| `fin_d2_bank_reconciliation` | D2 | Bank reconciliation | book/bank items, unreconciled differences, balanced final state |
| `fin_d2_iit_settlement` | D2 | Individual income-tax settlement | multi-source aggregation and policy-bounded recomputation |
| `fin_d2_stamp_duty_surcharges` | D2 | Stamp duty and surcharge filing | tax base, policy applicability, filing outputs |
| `fin_d3_ar_aging_ecl` | D3 | AR aging and ECL | aging buckets, collective ECL, traceability |
| `fin_d3_bank_provision` | D3 | Bank provisions and capital adequacy | NPL composition, provisions, RWA, capital ratios |
| `fin_d3_cit_annual` | D3 | Annual corporate income-tax filing | accounting-to-tax adjustments, losses, incentives |
| `fin_d3_finance_lease` | D3 | Finance-lease amortized cost | effective-interest method and period rollforward |
| `fin_d3_fund_nav` | D3 | Fund NAV calculation | position valuation, accruals, NAV per unit |
| `fin_d3_insurance` | D3 | Insurance and solvency reporting | reserves, regulatory ratios, rollforward |
| `fin_d3_lvat_liquidation` | D3 | Land appreciation tax liquidation | project aggregation and progressive bracket logic |
| `fin_d3_related_party` | D3 | Related-party and consolidation adjustments | relationship graph, transactions, elimination |
| `fin_d3_securities` | D3 | Securities business and holding valuation | position fair value, fund separation, stale-price detection |
| `fin_d3_vat_filing` | D3 | VAT and surcharge filing | invoices, output/input VAT, carryover |
| `fin_d4_consolidation_selfcheck` | D4 | Consolidation self-check and repair | eliminations, NCI, goodwill, injected-anomaly resolution |
| `fin_d4_financial_instruments` | D4 | Financial-instrument classification and measurement | business model, SPPI, amortized cost vs. fair value |

## Case-based verification module

| ID | Role | Current treatment |
| --- | --- | --- |
| `fin_d3_finance_lease_hengyang_guansheng` | Instance-specific ACT/360 lease-schedule verifier | Refactor into a generic, configurable finance-lease case adapter; remove embedded local path and case identifiers before migration |

## Track B — Bond underwriting workflow designs

| ID | Task | Primary output | Intended verification model |
| --- | --- | --- | --- |
| `bond_t1_financial_extraction` | Extract three statements and produce a normalized financial summary | financial summary + source notes | field truth, calculations, source pointers, human accounting review |
| `bond_t2_workpaper_completeness` | Match received materials to a workpaper index | missing-materials list + review queue | file/metadata match, required coverage, human material-sufficiency review |
| `bond_t3_cross_document_consistency` | Check financial figures across disclosure draft and workpapers | consistency-issues table | field/period/unit comparison, human disclosure judgment |
| `bond_t4_feedback_reply` | Prepare a feedback-response draft and disclosure checklist | response draft + checklist | numerical truth, structure, evidence map, constrained text review |
| `bond_t5_abs_asset_check` | Match ABS assets, contracts, invoices, and cash receipts | asset-check table + exceptions | record linkage, calculation, exception coverage, expert asset review |
| `bond_t6_market_analysis` | Build underwriting ranking and market-summary materials from export data | ranking table + market narrative | deterministic ranking/formulas, source traceability, human market interpretation |

## Status rules

The catalog describes task intent and does not, by itself, claim every task is ready for model evaluation. A future machine-readable `catalog.yaml` will carry per-task fields for `spec_status`, `verifier_status`, `instance_status`, `test_status`, and `release_tier`.
