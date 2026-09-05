from finbench import CashFlowVerifier, GroundTruth, Submission


TRUTH = GroundTruth(
    task_id="fin_d2_cash_flow",
    entity_id="SYNTHETIC_MANUFACTURER",
    reporting_period="2025-12-31",
    scope="consolidated",
    fields={
        "operating_cash_flow": 800_000,
        "investing_cash_flow": -300_000,
        "financing_cash_flow": 100_000,
        "net_change_in_cash": 600_000,
        "opening_cash": 1_000_000,
        "closing_cash": 1_600_000,
    },
    critical_fields=frozenset({"net_change_in_cash", "closing_cash"}),
    required_artifacts=frozenset({"submission_manifest.json", "reconciliation_notes.md"}),
)


def golden_submission(**changes):
    data = dict(
        task_id="fin_d2_cash_flow",
        entity_id="SYNTHETIC_MANUFACTURER",
        reporting_period="2025-12-31",
        scope="consolidated",
        unit="元",
        backend_state="submitted",
        fields=dict(TRUTH.fields),
        provenance={key: f"input/cash_flow.json#/{key}" for key in TRUTH.fields},
        output_artifacts={"submission_manifest.json": True, "reconciliation_notes.md": True},
    )
    data.update(changes)
    return Submission(**data)


def test_golden_submission_passes():
    result = CashFlowVerifier().run(golden_submission(), TRUTH)
    assert result.reportable_score == 1.0
    assert result.passed


def test_broken_rollforward_is_a_hard_failure():
    fields = dict(TRUTH.fields, closing_cash=1_500_000)
    result = CashFlowVerifier().run(golden_submission(fields=fields), TRUTH)
    assert not result.passed
    assert result.reportable_score == 0.0


def test_unsubmitted_output_is_capped():
    result = CashFlowVerifier().run(golden_submission(backend_state="draft"), TRUTH)
    assert not result.passed
    assert result.reportable_score <= 0.40
