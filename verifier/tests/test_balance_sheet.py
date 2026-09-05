from finbench import BalanceSheetVerifier, GroundTruth, Submission


TRUTH = GroundTruth(
    task_id="fin_d1_balance_sheet",
    entity_id="SYNTHETIC_HOLDCO",
    reporting_period="2025-12-31",
    scope="consolidated",
    fields={
        "current_assets": 2_300_000,
        "noncurrent_assets": 2_700_000,
        "total_assets": 5_000_000,
        "current_liabilities": 600_000,
        "noncurrent_liabilities": 1_400_000,
        "total_liabilities": 2_000_000,
        "total_equity": 3_000_000,
    },
    critical_fields=frozenset({"total_assets", "total_liabilities", "total_equity"}),
    required_artifacts=frozenset({"submission_manifest.json", "processing_notes.md"}),
    input_hashes={"input/canonical_balance_sheet.json": "synthetic-hash"},
)


def golden_submission(**changes):
    data = dict(
        task_id="fin_d1_balance_sheet",
        entity_id="SYNTHETIC_HOLDCO",
        reporting_period="2025-12-31",
        scope="consolidated",
        unit="元",
        backend_state="submitted",
        fields=dict(TRUTH.fields),
        provenance={key: f"input/canonical_balance_sheet.json#/{key}" for key in TRUTH.fields},
        output_artifacts={"submission_manifest.json": True, "processing_notes.md": True},
        input_hashes={"input/canonical_balance_sheet.json": "synthetic-hash"},
    )
    data.update(changes)
    return Submission(**data)


def test_golden_submission_passes():
    result = BalanceSheetVerifier().run(golden_submission(), TRUTH)
    assert result.reportable_score == 1.0
    assert result.passed


def test_two_wrong_fields_that_still_balance_do_not_pass():
    fields = dict(TRUTH.fields, current_assets=2_400_000, noncurrent_assets=2_600_000)
    result = BalanceSheetVerifier().run(golden_submission(fields=fields), TRUTH)
    assert not result.passed
    assert any(check.checker_id == "FIELD.NONCRITICAL" and check.status == "FAIL" for check in result.checks)


def test_tampered_input_is_a_zero_score_hack():
    result = BalanceSheetVerifier().run(
        golden_submission(input_hashes={"input/canonical_balance_sheet.json": "tampered"}),
        TRUTH,
    )
    assert result.is_hack
    assert result.reportable_score == 0.0
