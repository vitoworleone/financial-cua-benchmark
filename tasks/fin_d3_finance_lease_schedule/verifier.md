# `fin_d3_finance_lease_schedule` Verifier 合同

实现位置：`verifier/src/finbench/tasks/lease_schedule.py`。版本化计息约定由 `LeasePolicy` 注入，实例真值在运行时由 `GroundTruth` 提供；每个 Checker ID 的中文含义见[校验项说明](../../docs/04-checker-guide.md)。

| 校验项 | 校验内容 | 业务意义 | 权重 |
| --- | --- | --- | ---: |
| `META.IDENTITY` | 任务、主体、期间和口径一致 | 确保摊还表属于指定融资租赁合同和报告期间 | 0.06 |
| `META.UNIT` | 报告单位受支持 | 防止本金、利息和付款额因单位错误整体失真 | 0.04 |
| `SECURITY.INPUT_INTEGRITY` | 来源哈希和安全标记通过 | 确保付款安排和起租信息未被改写，计算过程合规 | 门禁 |
| `OUTPUT.COMPLETENESS` | 必要输出产物齐全 | 确保可交付的 schedule、提交清单和说明均完整 | 0.04 |
| `CONVENTION.ACT360` | 使用 ACT/360，且利率有限、为正 | 明确计息口径；错用 ACT/365 等约定会系统性改变利息 | 0.05 |
| `PERIOD.COMPLETENESS` | 全部预期期次连续出现 | 防止漏期、重复期或期次错位使整张摊还表失效 | 0.08 |
| `PERIOD.DATES_AND_DAYS` | 付款日期和实际天数可复算 | 防止手填天数错误，确保每期计息期间准确 | 0.12 |
| `RULE.ACT360_INTEREST` | 每期利息按政策重算 | 验证实际利率法的核心利息计算，而非只相信填报结果 | 0.17 |
| `RULE.PRINCIPAL_INTEREST_SPLIT` | 现金 = 利息 + 本金 | 验证每笔实收款被正确拆分为利息和本金 | 0.10 |
| `RULE.PERIOD_ROLLFORWARD` | 本金逐期滚动，残值收敛 | 验证前后期余额连续，且最终本金处理正确 | 0.15 |
| `RULE.TOTALS_AND_RESIDUAL` | 提交汇总同时等于计算值和正确值 | 防止逐期正确但汇总错误，或汇总与最终余额矛盾 | 0.10 |
| `PROVENANCE.FIELD_MAP` | schedule 和派生汇总具有来源映射 | 支持对付款、利息与最终余额逐项复核 | 0.05 |
| `STATE.SUBMITTED` | 最终后端状态为 `submitted` | 确保任务完成的是正式提交，而非只生成一张本地表 | 0.04 |

错误计息约定、期次不完整、日期/天数错误、ACT/360 利息错误、本金滚动失败或汇总失败，均触发 0 分硬失败；未正式提交时最高 0.40。输入被修改或触发安全标记时，结果为 0 分并标记 `HACK`。

测试 fixture 是刻意构造的虚构三期案例，覆盖 golden、错误计息约定、利息错但仍表面平衡的还本付息拆分，以及输入篡改。
