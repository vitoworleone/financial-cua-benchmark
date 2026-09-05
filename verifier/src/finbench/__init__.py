"""Public verifier primitives for the Financial CUA Benchmark.

The package intentionally contains no holdout input, instance-specific truth,
or local machine paths. Synthetic fixtures belong in ``tests/``.
"""

from .contracts import GroundTruth, Submission
from .tasks.balance_sheet import BalanceSheetVerifier
from .tasks.cash_flow import CashFlowVerifier
from .tasks.lease_schedule import LeasePolicy, LeaseScheduleVerifier

__all__ = ["BalanceSheetVerifier", "CashFlowVerifier", "GroundTruth", "LeasePolicy", "LeaseScheduleVerifier", "Submission"]
