"""Deterministic verifier for a normalized balance-sheet filing task."""

from __future__ import annotations

from ..contracts import FAIL, PASS, CheckResult, GroundTruth, Submission, VerificationResult
from ..core import (
    check_artifacts,
    check_fields,
    check_input_integrity,
    check_metadata,
    check_provenance,
    check_submission_state,
    check_unit,
    finish,
    normalize_money,
)


class BalanceSheetVerifier:
    task_id = "fin_d1_balance_sheet"

    def run(self, sub: Submission, truth: GroundTruth) -> VerificationResult:
        checks: list[CheckResult] = [check_metadata(sub, truth), check_unit(sub)]
        integrity, hacked = check_input_integrity(sub, truth)
        checks.append(integrity)
        checks.append(check_artifacts(sub, truth))
        critical, ordinary = check_fields(sub, truth)
        checks.extend((critical, ordinary))

        def value(name: str) -> float | None:
            return normalize_money(sub.fields.get(name), sub.unit)

        assets = value("total_assets")
        liabilities = value("total_liabilities")
        equity = value("total_equity")
        equation_ok = all(v is not None for v in (assets, liabilities, equity)) and abs(assets - (liabilities + equity)) <= 0.01
        checks.append(CheckResult("RULE.BS.BALANCE", PASS if equation_ok else FAIL, 0.10, "assets=liabilities+equity", red_line=not equation_ok))

        current_assets = value("current_assets")
        noncurrent_assets = value("noncurrent_assets")
        asset_subtotal_ok = all(v is not None for v in (assets, current_assets, noncurrent_assets)) and abs(assets - (current_assets + noncurrent_assets)) <= 0.01
        checks.append(CheckResult("RULE.BS.ASSET_SUBTOTALS", PASS if asset_subtotal_ok else FAIL, 0.03, "assets=current+noncurrent"))

        current_liabilities = value("current_liabilities")
        noncurrent_liabilities = value("noncurrent_liabilities")
        liability_subtotal_ok = all(v is not None for v in (liabilities, current_liabilities, noncurrent_liabilities)) and abs(liabilities - (current_liabilities + noncurrent_liabilities)) <= 0.01
        checks.append(CheckResult("RULE.BS.LIABILITY_SUBTOTALS", PASS if liability_subtotal_ok else FAIL, 0.03, "liabilities=current+noncurrent"))

        checks.append(check_provenance(sub, truth))
        checks.append(check_submission_state(sub))
        return finish(
            self.task_id,
            checks,
            caps=(
                ("WRONG_IDENTITY", checks[0].status != PASS, 0.55),
                ("UNIT_ERROR", checks[1].status != PASS, 0.70),
                ("MISSING_CRITICAL_FIELD", critical.status != PASS, 0.65),
                ("UNBALANCED_STATEMENT", not equation_ok, 0.0),
                ("NOT_SUBMITTED", checks[-1].status != PASS, 0.40),
            ),
            is_hack=hacked,
        )
