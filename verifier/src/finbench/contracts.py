"""Public data contracts shared by deterministic task verifiers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


PASS = "PASS"
FAIL = "FAIL"
BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class Submission:
    """Agent-visible final state captured by an environment adapter.

    ``fields`` are canonical task fields. ``provenance`` maps a field name to
    the source pointer used by the Agent. ``input_hashes`` are the hashes that
    the Agent observed when it started; a mismatch with the initial snapshot
    is evidence of protected-input mutation.
    """

    task_id: str
    entity_id: str
    reporting_period: str
    scope: str
    unit: str
    backend_state: str
    fields: Mapping[str, Any] = field(default_factory=dict)
    provenance: Mapping[str, str] = field(default_factory=dict)
    output_artifacts: Mapping[str, bool] = field(default_factory=dict)
    input_hashes: Mapping[str, str] = field(default_factory=dict)
    security_flags: Mapping[str, bool] = field(default_factory=dict)


@dataclass(frozen=True)
class GroundTruth:
    """Verifier-only expected state for one controlled development instance."""

    task_id: str
    entity_id: str
    reporting_period: str
    scope: str
    fields: Mapping[str, Any]
    critical_fields: frozenset[str]
    required_artifacts: frozenset[str]
    input_hashes: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class CheckResult:
    checker_id: str
    status: str
    weight: float
    detail: str
    red_line: bool = False


@dataclass(frozen=True)
class VerificationResult:
    task_id: str
    base_score: float
    reportable_score: float
    passed: bool
    is_hack: bool
    caps_applied: tuple[str, ...]
    checks: tuple[CheckResult, ...]
