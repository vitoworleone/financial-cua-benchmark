from copy import deepcopy

from finbench import GroundTruth, LeasePolicy, LeaseScheduleVerifier, Submission


def truth() -> GroundTruth:
    return GroundTruth(
        task_id="fin_d3_finance_lease_schedule",
        entity_id="DEMO_LESSOR",
        reporting_period="2025-10-01",
        scope="separate",
        fields={
            "lease_start_date": "2025-01-01",
            "opening_principal": 100_000.00,
            "periods": [
                {"payment_date": "2025-04-01"},
                {"payment_date": "2025-07-01"},
                {"payment_date": "2025-10-01"},
            ],
            "total_cash": 105_080.41,
            "total_interest": 5_080.41,
            "total_principal": 100_000.00,
            "ending_principal": 0.00,
        },
        critical_fields=frozenset(),
        required_artifacts=frozenset({"submission_manifest.json", "reconciliation_notes.md"}),
        input_hashes={"input/demo_schedule.csv": "sha256-demo"},
    )


def golden() -> Submission:
    periods = [
        {"period_no": 1, "payment_date": "2025-04-01", "days": 90, "opening_principal": 100_000.00, "cash_paid": 35_000.00, "interest": 2_500.00, "principal": 32_500.00, "closing_principal": 67_500.00},
        {"period_no": 2, "payment_date": "2025-07-01", "days": 91, "opening_principal": 67_500.00, "cash_paid": 35_000.00, "interest": 1_706.25, "principal": 33_293.75, "closing_principal": 34_206.25},
        {"period_no": 3, "payment_date": "2025-10-01", "days": 92, "opening_principal": 34_206.25, "cash_paid": 35_080.41, "interest": 874.16, "principal": 34_206.25, "closing_principal": 0.00},
    ]
    return Submission(
        task_id="fin_d3_finance_lease_schedule",
        entity_id="DEMO_LESSOR",
        reporting_period="2025-10-01",
        scope="separate",
        unit="元",
        backend_state="submitted",
        fields={"periods": periods, "total_cash": 105_080.41, "total_interest": 5_080.41, "total_principal": 100_000.00, "ending_principal": 0.00},
        provenance={"periods": "input/demo_schedule.csv#/payments", "total_interest": "derived:ACT/360", "ending_principal": "derived:periods/3"},
        output_artifacts={"submission_manifest.json": True, "reconciliation_notes.md": True},
        input_hashes={"input/demo_schedule.csv": "sha256-demo"},
    )


def test_synthetic_act360_schedule_scores_one():
    result = LeaseScheduleVerifier(LeasePolicy(annual_rate=0.10)).run(golden(), truth())
    assert result.passed
    assert result.reportable_score == 1.0


def test_act365_policy_is_a_hard_failure():
    result = LeaseScheduleVerifier(LeasePolicy(annual_rate=0.10, day_count_convention="ACT/365", day_count_denominator=365)).run(golden(), truth())
    assert not result.passed
    assert result.reportable_score == 0.0
    assert "WRONG_CONVENTION" in result.caps_applied


def test_wrong_interest_cannot_be_hidden_by_a_balanced_schedule():
    submission = deepcopy(golden())
    periods = [dict(row) for row in submission.fields["periods"]]
    periods[1]["interest"] = 1_700.00
    periods[1]["principal"] = 33_300.00
    altered = Submission(**{**submission.__dict__, "fields": {**submission.fields, "periods": periods}})
    result = LeaseScheduleVerifier(LeasePolicy(annual_rate=0.10)).run(altered, truth())
    assert not result.passed
    assert result.reportable_score == 0.0


def test_input_mutation_is_marked_as_hack():
    submission = golden()
    altered = Submission(**{**submission.__dict__, "input_hashes": {"input/demo_schedule.csv": "mutated"}})
    result = LeaseScheduleVerifier(LeasePolicy(annual_rate=0.10)).run(altered, truth())
    assert result.is_hack
    assert result.reportable_score == 0.0
