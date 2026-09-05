# `fin_d3_finance_lease_schedule` Verifier 合同

实现位置：`verifier/src/finbench/tasks/lease_schedule.py`。版本化计息约定由 `LeasePolicy` 注入，实例真值在运行时由 `GroundTruth` 提供。

| Checker ID | 确定性条件 | 权重 |
| --- | --- | ---: |
| `META.IDENTITY` | 任务、主体、期间和口径一致 | 0.06 |
| `META.UNIT` | 报告单位受支持 | 0.04 |
| `SECURITY.INPUT_INTEGRITY` | 来源哈希和安全标记通过 | 门禁 |
| `OUTPUT.COMPLETENESS` | 必要输出产物齐全 | 0.04 |
| `CONVENTION.ACT360` | 使用 ACT/360，且利率有限、为正 | 0.05 |
| `PERIOD.COMPLETENESS` | 全部预期期次连续出现 | 0.08 |
| `PERIOD.DATES_AND_DAYS` | 付款日期和实际天数可复算 | 0.12 |
| `RULE.ACT360_INTEREST` | 每期利息按政策重算 | 0.17 |
| `RULE.PRINCIPAL_INTEREST_SPLIT` | 现金 = 利息 + 本金 | 0.10 |
| `RULE.PERIOD_ROLLFORWARD` | 本金逐期滚动，残值收敛 | 0.15 |
| `RULE.TOTALS_AND_RESIDUAL` | 提交汇总同时等于计算值和评测器值 | 0.10 |
| `PROVENANCE.FIELD_MAP` | schedule 和派生汇总具有来源映射 | 0.05 |
| `STATE.SUBMITTED` | 最终后端状态为 `submitted` | 0.04 |

错误计息约定、期次不完整、日期/天数错误、ACT/360 利息错误、本金滚动失败或汇总失败，均触发 0 分硬失败；未正式提交时最高 0.40。输入被修改或触发安全标记时，结果为 0 分并标记 `HACK`。

测试 fixture 是刻意构造的虚构三期案例，覆盖 golden、错误计息约定、利息错但仍表面平衡的还本付息拆分，以及输入篡改。
