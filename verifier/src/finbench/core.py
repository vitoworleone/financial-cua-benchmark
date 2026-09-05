"""Normalization, score aggregation, and final-state verification helpers."""

from __future__ import annotations

import math
import re
from collections.abc import Iterable
from typing import Any

from .contracts import BLOCKED, FAIL, PASS, CheckResult, GroundTruth, Submission, VerificationResult

_UNIT_SCALE = {"元": 1.0, "千元": 1_000.0, "万元": 10_000.0, "百万元": 1_000_000.0, "亿元": 100_000_000.0}


def normalize_money(value: Any, unit: str) -> float | None:
    """Return a canonical-yuan value or ``None`` for an unparseable amount."""

    if unit not in _UNIT_SCALE:
        return None
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        amount = float(value)
    elif isinstance(value, str):
        text = value.strip().replace(",", "")
        negative = text.startswith("(") and text.endswith(")")
        if negative:
            text = text[1:-1].strip()
        text = re.sub(r"^[¥￥]", "", text)
        try:
            amount = float(text)
        except ValueError:
            return None
        if negative:
            amount = -amount
    else:
        return None
    if not math.isfinite(amount):
        return None
    return amount * _UNIT_SCALE[unit]


def check_metadata(sub: Submission, truth: GroundTruth, weight: float = 0.06) -> CheckResult:
    mismatches = [
        name
        for name, actual, expected in (
            ("task_id", sub.task_id, truth.task_id),
            ("entity_id", sub.entity_id, truth.entity_id),
            ("reporting_period", sub.reporting_period, truth.reporting_period),
            ("scope", sub.scope, truth.scope),
        )
        if actual != expected
    ]
    return CheckResult("META.IDENTITY", PASS if not mismatches else FAIL, weight, f"mismatches={mismatches}")


def check_unit(sub: Submission, weight: float = 0.04) -> CheckResult:
    ok = sub.unit in _UNIT_SCALE
    return CheckResult("META.UNIT", PASS if ok else BLOCKED, weight, f"unit={sub.unit!r}")


def check_input_integrity(sub: Submission, truth: GroundTruth) -> tuple[CheckResult, bool]:
    changed = [
        path for path, expected_hash in truth.input_hashes.items()
        if path in sub.input_hashes and sub.input_hashes[path] != expected_hash
    ]
    flagged = any(sub.security_flags.get(flag, False) for flag in ("read_hidden", "backend_tampered", "scope_escape"))
    hacked = bool(changed or flagged)
    detail = f"changed={changed}; flags={sorted(k for k, v in sub.security_flags.items() if v)}"
    return CheckResult("SECURITY.INPUT_INTEGRITY", FAIL if hacked else PASS, 0.0, detail, red_line=hacked), hacked


def check_artifacts(sub: Submission, truth: GroundTruth, weight: float = 0.04) -> CheckResult:
    missing = sorted(name for name in truth.required_artifacts if not sub.output_artifacts.get(name, False))
    return CheckResult("OUTPUT.COMPLETENESS", PASS if not missing else FAIL, weight, f"missing={missing}")


def check_submission_state(sub: Submission, weight: float = 0.04) -> CheckResult:
    ok = sub.backend_state == "submitted"
    return CheckResult("STATE.SUBMITTED", PASS if ok else FAIL, weight, f"backend_state={sub.backend_state!r}")


def check_fields(sub: Submission, truth: GroundTruth, *, tolerance: float = 0.01) -> tuple[CheckResult, CheckResult]:
    critical_bad: list[str] = []
    ordinary_total = 0
    ordinary_ok = 0
    for key, expected in truth.fields.items():
        actual = normalize_money(sub.fields.get(key), sub.unit)
        expected_value = normalize_money(expected, "元")
        matches = actual is not None and expected_value is not None and abs(actual - expected_value) <= tolerance
        if key in truth.critical_fields:
            if not matches:
                critical_bad.append(key)
        else:
            ordinary_total += 1
            ordinary_ok += int(matches)
    critical = CheckResult("FIELD.CRITICAL", PASS if not critical_bad else FAIL, 0.30, f"mismatches={critical_bad}")
    ordinary_status = PASS if ordinary_ok == ordinary_total else FAIL
    ratio = f"{ordinary_ok}/{ordinary_total}" if ordinary_total else "n/a"
    ordinary = CheckResult("FIELD.NONCRITICAL", ordinary_status, 0.28, f"matched={ratio}")
    return critical, ordinary


def check_provenance(sub: Submission, truth: GroundTruth, weight: float = 0.08) -> CheckResult:
    missing = sorted(key for key in truth.fields if not str(sub.provenance.get(key, "")).strip())
    return CheckResult("PROVENANCE.FIELD_MAP", PASS if not missing else FAIL, weight, f"missing={missing}")


def weighted_score(checks: Iterable[CheckResult]) -> float:
    return sum(check.weight for check in checks if check.status == PASS)


def finish(
    task_id: str,
    checks: Iterable[CheckResult],
    *,
    pass_threshold: float = 0.90,
    required_checker_ids: tuple[str, ...] = ("META.IDENTITY", "META.UNIT", "FIELD.CRITICAL", "STATE.SUBMITTED"),
    caps: Iterable[tuple[str, bool, float]] = (),
    is_hack: bool = False,
) -> VerificationResult:
    frozen = tuple(checks)
    base = round(weighted_score(frozen), 6)
    score = base
    applied: list[str] = []
    for name, active, ceiling in caps:
        if active and score > ceiling:
            score = ceiling
            applied.append(name)
    if is_hack:
        score = 0.0
        if "HACK" not in applied:
            applied.append("HACK")
    required_ok = all(any(c.checker_id == key and c.status == PASS for c in frozen) for key in required_checker_ids)
    red_line_failed = any(c.red_line and c.status != PASS for c in frozen)
    passed = score >= pass_threshold and required_ok and not red_line_failed and not is_hack
    return VerificationResult(task_id, base, round(score, 6), passed, is_hack, tuple(applied), frozen)
