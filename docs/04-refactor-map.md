# Source-to-target refactor map

This is an internal migration map for the clean repository. It records adaptation decisions rather than instructing a bulk copy.

| Source asset | Value | Main issue | Target action |
| --- | --- | --- | --- |
| `tasks/financial_20/*/task.md` | Complete task contracts | Most declare `documentation_only_not_runnable`; one case is inconsistent | Normalize metadata and publish as specifications with evidence labels |
| `tasks/financial_20/*/SKILL.md` | Domain knowledge and task boundaries | Need terminology/style pass and cross-linking | Migrate after task catalog IDs and public release policy are stable |
| `tasks/financial_20/*/verifier.md` | Rich verifier design, caps, adversarial states | Must be reconciled with actual implementation | Treat as canonical intent; add implementation-status block per task |
| `financial_20_verifiers/contracts.py` | Verifier data model | Public/private data separation needs review | Refactor into public typed interfaces |
| `financial_20_verifiers/core.py` | Shared normalization and scoring | Needs packaging, configuration, and safer defaults review | Refactor with tests before migration |
| `financial_20_verifiers/checkers.py` | Reusable deterministic checker library | Must verify all checker contracts against docs | Migrate checker by checker with tests |
| `financial_20_verifiers/taskbase.py` | Checker/cap composition model | Needs immutable task configuration and typing cleanup | Retain design, revise API |
| `financial_20_verifiers/registry.py` | Task discovery/CLI | Registers 21 IDs while describing 20; injects runtime configuration | Rewrite around `standard` and `case` registries |
| `financial_20_verifiers/tasks/fin_d*.py` | Per-task executable logic | Production modules embed `GOLDEN_FIELDS` / policy fixtures | Split rules from fixtures; migrate in priority order |
| `selftest.py`, `adversarial.py` | C3/C4 and adversarial evidence | Depend on production-embedded golden fixtures | Rebuild as explicit synthetic test fixtures |
| `instance_gen.py` | Workspace generation concept | May fabricate inputs from golden fields | Replace with source-driven or explicitly synthetic instance builders |
| finance-lease case module | High-fidelity instance and ACT/360 verifier | Absolute local path, real identifier, embedded payments | Generic configurable adapter and synthetic fixture completed; original real instance remains outside this repository |
| workspace manifests / ground truth | Instance-level execution assets | Test integrity and answer leakage | Do not migrate until release tiers are designed |
| bond-underwriting research | Domain workflow and six task designs | Existing task cards lack final task-package / executable verifier separation | Build as Track B after Track A public contract stabilizes |

## Migration order

1. Establish package boundaries and machine-readable catalog.
2. Refactor the shared contracts/core/checkers/task-base layer with synthetic tests.
3. Migrate two representative standard tasks: balance sheet and cash flow. **Completed for a synthetic, adapter-contract scope**: the shared core, public task contracts, and six unit tests are now present in `verifier/` and `tasks/`.
4. Migrate a policy-heavy task and a financial-institution task to prove abstraction quality.
5. Rebuild the finance-lease case as a configurable adapter, not a path-bound script. **Completed for the generic ACT/360 rule and fictitious synthetic fixture; no real instance was migrated.**
6. Migrate the remaining standard task rules, their specifications, and their synthetic development fixtures.
7. Convert the six bond-underwriting designs into the same task-package contract.
8. Only then establish public development and private holdout release tiers, benchmark runner, and result reporting.

## Non-negotiable refactor rules

- No production task-rule module may embed an instance-specific answer, local absolute path, client identifier, or input dataset.
- Tests must be able to generate synthetic golden, initial, and adversarial cases without importing private/holdout assets.
- The public catalog counts 20 standard tasks; case adapters are labelled separately.
- A task document may not claim a runnable environment or Agent result without a reproducible artifact.
- Every migrated task must retain an explicit link between documented success conditions and implemented checker IDs.
