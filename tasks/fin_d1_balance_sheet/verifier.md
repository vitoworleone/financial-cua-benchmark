# `fin_d1_balance_sheet` Verifier 合同

实现位置：`verifier/src/finbench/tasks/balance_sheet.py`。通用术语可先阅读[校验项说明](../../docs/04-checker-guide.md)。

| 校验项 | 校验内容 | 业务意义 | 权重 |
| --- | --- | --- | ---: |
| `META.IDENTITY` | 任务 ID、主体、期间和口径与任务合同一致 | 防止在错误主体或错误报表上完成填报 | 0.06 |
| `META.UNIT` | 单位已声明且可以转换为 canonical 单位 | 防止元、千元、万元混用造成整体金额错误 | 0.04 |
| `SECURITY.INPUT_INTEGRITY` | 输入未变更，安全标记为空 | 证明结果来自规定材料和合规操作 | 门禁 |
| `OUTPUT.COMPLETENESS` | 必要输出产物齐全 | 交付物完整，便于复核和留痕 | 0.04 |
| `FIELD.CRITICAL` | 所有关键字段等于正确值 | 确保资产总计等关键业务结果准确 | 0.30 |
| `FIELD.NONCRITICAL` | 其余预期字段等于正确值 | 确保明细填报完整、准确 | 0.28 |
| `RULE.BS.BALANCE` | 资产 = 负债 + 权益 | 检查资产负债表的核心平衡关系 | 0.10 |
| `RULE.BS.ASSET_SUBTOTALS` | 资产 = 流动资产 + 非流动资产 | 检查资产分类汇总完整性 | 0.03 |
| `RULE.BS.LIABILITY_SUBTOTALS` | 负债 = 流动负债 + 非流动负债 | 检查负债分类汇总完整性 | 0.03 |
| `PROVENANCE.FIELD_MAP` | 每个预期字段有来源映射 | 让复核人能够追溯每个数字 | 0.08 |
| `STATE.SUBMITTED` | 后端状态为 `submitted` | 区分正式提交与仅保存草稿 | 0.04 |

通过检查器权重求基础分后，依次应用透明封顶：错主体/口径上限 0.55，单位错误上限 0.70，关键字段错误上限 0.65，报表不平衡为 0，未正式提交上限 0.40。修改输入或触发安全标记，直接得到 0 分并标注 `HACK`。

测试覆盖合成 golden、空白初始状态、报表不平衡、遗漏关键字段、错口径和输入完整性违规；生产规则模块不包含任何 fixture 答案。
