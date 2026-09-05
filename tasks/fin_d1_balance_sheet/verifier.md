# `fin_d1_balance_sheet` Verifier 合同

实现位置：`verifier/src/finbench/tasks/balance_sheet.py`。

| Checker ID | 确定性条件 | 权重 |
| --- | --- | ---: |
| `META.IDENTITY` | 任务 ID、主体、期间和口径与评测合同一致 | 0.06 |
| `META.UNIT` | 单位已声明且可以转换为 canonical 单位 | 0.04 |
| `SECURITY.INPUT_INTEGRITY` | 输入未变更，安全标记为空 | 门禁 |
| `OUTPUT.COMPLETENESS` | 必要输出产物齐全 | 0.04 |
| `FIELD.CRITICAL` | 所有关键字段等于私有真值 | 0.30 |
| `FIELD.NONCRITICAL` | 其余预期字段等于私有真值 | 0.28 |
| `RULE.BS.BALANCE` | 资产 = 负债 + 权益 | 0.10 |
| `RULE.BS.ASSET_SUBTOTALS` | 资产 = 流动资产 + 非流动资产 | 0.03 |
| `RULE.BS.LIABILITY_SUBTOTALS` | 负债 = 流动负债 + 非流动负债 | 0.03 |
| `PROVENANCE.FIELD_MAP` | 每个预期字段有来源映射 | 0.08 |
| `STATE.SUBMITTED` | 后端状态为 `submitted` | 0.04 |

通过检查器权重求基础分后，依次应用透明封顶：错主体/口径上限 0.55，单位错误上限 0.70，关键字段错误上限 0.65，报表不平衡为 0，未正式提交上限 0.40。修改输入或触发安全标记，直接得到 0 分并标注 `HACK`。

测试覆盖合成 golden、空白初始状态、报表不平衡、遗漏关键字段、错口径和输入完整性违规；生产规则模块不包含任何 fixture 答案。
