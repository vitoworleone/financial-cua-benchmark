"""Configurable ACT/360 finance-lease schedule verifier.

The verifier contains calculation rules only. Deal terms, payment dates, cash
flows, and expected totals are supplied per evaluation instance through
``GroundTruth``; no client workbook, contract identifier, or answer schedule
is embedded in this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from math import isfinite
from typing import Any, Mapping

from ..contracts import FAIL, PASS, CheckResult, GroundTruth, Submission, VerificationResult
from ..core import check_artifacts, check_input_integrity, check_metadata, check_submission_state, check_unit, finish


@dataclass(frozen=True)
class LeasePolicy:
    """Versioned calculation convention supplied by the task configuration."""

    annual_rate: float
    day_count_convention: str = "ACT/360"
    day_count_denominator: int = 360
    monetary_tolerance: float = 0.01
    residual_tolerance: float = 0.01


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return number if isfinite(number) else None


def _rows(sub: Submission) -> list[Mapping[str, Any]]:
    value = sub.fields.get("periods")
    return [row for row in value if isinstance(row, Mapping)] if isinstance(value, list) else []


class LeaseScheduleVerifier:
    """Verify a submitted effective-interest schedule under a fixed convention."""

    task_id = "fin_d3_finance_lease_schedule"

    def __init__(self, policy: LeasePolicy) -> None:
        self.policy = policy

    def run(self, sub: Submission, truth: GroundTruth) -> VerificationResult:
        checks: list[CheckResult] = [check_metadata(sub, truth), check_unit(sub)]
        integrity, hacked = check_input_integrity(sub, truth)
        checks.append(integrity)
        checks.append(check_artifacts(sub, truth))

        convention_ok = (
            self.policy.day_count_convention == "ACT/360"
            and self.policy.day_count_denominator == 360
            and self.policy.annual_rate > 0
            and isfinite(self.policy.annual_rate)
        )
        checks.append(CheckResult("CONVENTION.ACT360", PASS if convention_ok else FAIL, 0.05, "requires ACT/360 with a finite positive annual rate", red_line=not convention_ok))

        rows = _rows(sub)
        expected_rows = truth.fields.get("periods")
        expected_rows = expected_rows if isinstance(expected_rows, list) else []
        period_numbers = [row.get("period_no") for row in rows]
        complete = len(rows) == len(expected_rows) and period_numbers == list(range(1, len(expected_rows) + 1))
        checks.append(CheckResult("PERIOD.COMPLETENESS", PASS if complete else FAIL, 0.08, f"submitted={len(rows)}; expected={len(expected_rows)}", red_line=not complete))

        start = truth.fields.get("lease_start_date")
        dates_ok = bool(start) and len(rows) == len(expected_rows)
        previous_date: date | None = None
        try:
            previous_date = date.fromisoformat(str(start))
            for row, expected in zip(rows, expected_rows):
                payment_date = date.fromisoformat(str(row.get("payment_date")))
                expected_date = str(expected.get("payment_date"))
                actual_days = row.get("days")
                dates_ok = dates_ok and payment_date.isoformat() == expected_date and actual_days == (payment_date - previous_date).days
                previous_date = payment_date
        except (TypeError, ValueError):
            dates_ok = False
        checks.append(CheckResult("PERIOD.DATES_AND_DAYS", PASS if dates_ok else FAIL, 0.12, "payment dates and actual days match the instance", red_line=not dates_ok))

        interest_bad: list[int] = []
        split_bad: list[int] = []
        rollforward_bad: list[int] = []
        expected_opening = _number(truth.fields.get("opening_principal"))
        for row in rows:
            period = int(row.get("period_no", 0) or 0)
            opening, days, interest = _number(row.get("opening_principal")), _number(row.get("days")), _number(row.get("interest"))
            cash, principal, closing = _number(row.get("cash_paid")), _number(row.get("principal")), _number(row.get("closing_principal"))
            if None in (opening, days, interest) or expected_opening is None:
                interest_bad.append(period)
            else:
                calculated_interest = round(opening * self.policy.annual_rate * days / self.policy.day_count_denominator, 2)
                if abs(interest - calculated_interest) > self.policy.monetary_tolerance:
                    interest_bad.append(period)
            if None in (cash, interest, principal) or abs(cash - interest - principal) > self.policy.monetary_tolerance:
                split_bad.append(period)
            if None in (opening, principal, closing, expected_opening) or abs(opening - expected_opening) > self.policy.monetary_tolerance or abs(closing - (opening - principal)) > self.policy.monetary_tolerance:
                rollforward_bad.append(period)
            if closing is not None:
                expected_opening = closing

        interest_ok = complete and not interest_bad
        split_ok = complete and not split_bad
        residual_ok = complete and not rollforward_bad and expected_opening is not None and abs(expected_opening) <= self.policy.residual_tolerance
        checks.append(CheckResult("RULE.ACT360_INTEREST", PASS if interest_ok else FAIL, 0.17, f"bad_periods={interest_bad}", red_line=not interest_ok))
        checks.append(CheckResult("RULE.PRINCIPAL_INTEREST_SPLIT", PASS if split_ok else FAIL, 0.10, f"bad_periods={split_bad}"))
        checks.append(CheckResult("RULE.PERIOD_ROLLFORWARD", PASS if residual_ok else FAIL, 0.15, f"bad_periods={rollforward_bad}; ending={expected_opening}", red_line=not residual_ok))

        total_keys = ("total_cash", "total_interest", "total_principal", "ending_principal")
        calculated = {
            "total_cash": sum(_number(row.get("cash_paid")) or 0.0 for row in rows),
            "total_interest": sum(_number(row.get("interest")) or 0.0 for row in rows),
            "total_principal": sum(_number(row.get("principal")) or 0.0 for row in rows),
            "ending_principal": _number(rows[-1].get("closing_principal")) if rows else None,
        }
        totals_bad = [
            key for key in total_keys
            if _number(sub.fields.get(key)) is None
            or _number(truth.fields.get(key)) is None
            or calculated[key] is None
            or abs(_number(sub.fields.get(key)) - calculated[key]) > self.policy.monetary_tolerance
            or abs(_number(sub.fields.get(key)) - _number(truth.fields.get(key))) > self.policy.monetary_tolerance
        ]
        checks.append(CheckResult("RULE.TOTALS_AND_RESIDUAL", PASS if complete and not totals_bad else FAIL, 0.10, f"mismatches={totals_bad}", red_line=bool(totals_bad)))

        provenance_keys = ("periods", "total_interest", "ending_principal")
        missing_provenance = [key for key in provenance_keys if not str(sub.provenance.get(key, "")).strip()]
        checks.append(CheckResult("PROVENANCE.FIELD_MAP", PASS if not missing_provenance else FAIL, 0.05, f"missing={missing_provenance}", red_line=bool(missing_provenance)))
        checks.append(check_submission_state(sub))
        return finish(
            self.task_id,
            checks,
            required_checker_ids=(
                "META.IDENTITY",
                "META.UNIT",
                "CONVENTION.ACT360",
                "PERIOD.COMPLETENESS",
                "RULE.ACT360_INTEREST",
                "RULE.PERIOD_ROLLFORWARD",
                "RULE.TOTALS_AND_RESIDUAL",
                "STATE.SUBMITTED",
            ),
            caps=(
                ("WRONG_IDENTITY", checks[0].status != PASS, 0.55),
                ("WRONG_CONVENTION", not convention_ok, 0.0),
                ("INCOMPLETE_OR_INVALID_SCHEDULE", not complete or not dates_ok or not interest_ok or not residual_ok, 0.0),
                ("NOT_SUBMITTED", checks[-1].status != PASS, 0.40),
            ),
            is_hack=hacked,
        )
