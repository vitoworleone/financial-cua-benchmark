"""Deterministic verifier for a normalized cash-flow filing task."""

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


class CashFlowVerifier:
    task_id = "fin_d2_cash_flow"

    def run(self, sub: Submission, truth: GroundTruth) -> VerificationResult:
        checks: list[CheckResult] = [check_metadata(sub, truth), check_unit(sub)]
        integrity, hacked = check_input_integrity(sub, truth)
        checks.append(integrity)
        checks.append(check_artifacts(sub, truth))
        critical, ordinary = check_fields(sub, truth)
        checks.extend((critical, ordinary))

        def value(name: str) -> float | None:
            return normalize_money(sub.fields.get(name), sub.unit)

        operating, investing, financing, net_change = (value(name) for name in ("operating_cash_flow", "investing_cash_flow", "financing_cash_flow", "net_change_in_cash"))
        flow_ok = all(v is not None for v in (operating, investing, financing, net_change)) and abs(net_change - (operating + investing + financing)) <= 0.01
        checks.append(CheckResult("RULE.CF.NET_CHANGE", PASS if flow_ok else FAIL, 0.09, "net_change=operating+investing+financing", red_line=not flow_ok))

        opening, closing = value("opening_cash"), value("closing_cash")
        rollforward_ok = all(v is not None for v in (opening, net_change, closing)) and abs(closing - (opening + net_change)) <= 0.01
        checks.append(CheckResult("RULE.CF.CASH_ROLLFORWARD", PASS if rollforward_ok else FAIL, 0.07, "closing=opening+net_change", red_line=not rollforward_ok))

        checks.append(check_provenance(sub, truth))
        checks.append(check_submission_state(sub))
        return finish(
            self.task_id,
            checks,
            caps=(
                ("WRONG_IDENTITY", checks[0].status != PASS, 0.55),
                ("UNIT_ERROR", checks[1].status != PASS, 0.70),
                ("MISSING_CRITICAL_FIELD", critical.status != PASS, 0.65),
                ("BROKEN_CASH_FLOW", not flow_ok or not rollforward_ok, 0.0),
                ("NOT_SUBMITTED", checks[-1].status != PASS, 0.40),
            ),
            is_hack=hacked,
        )
