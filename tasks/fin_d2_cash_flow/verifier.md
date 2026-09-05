# `fin_d2_cash_flow` Verifier 合同

实现位置：`verifier/src/finbench/tasks/cash_flow.py`。

| Checker ID | 确定性条件 | 权重 |
| --- | --- | ---: |
| `META.IDENTITY` | 任务 ID、主体、期间、口径一致 | 0.06 |
| `META.UNIT` | 单位已声明且受支持 | 0.04 |
| `SECURITY.INPUT_INTEGRITY` | 输入哈希与安全标记通过 | 门禁 |
| `OUTPUT.COMPLETENESS` | 必要输出产物齐全 | 0.04 |
| `FIELD.CRITICAL` | 指定关键现金字段等于私有真值 | 0.30 |
| `FIELD.NONCRITICAL` | 其他预期字段等于私有真值 | 0.28 |
| `RULE.CF.NET_CHANGE` | 净变动 = 经营 + 投资 + 筹资 | 0.09 |
| `RULE.CF.CASH_ROLLFORWARD` | 期末现金 = 期初现金 + 净变动 | 0.07 |
| `PROVENANCE.FIELD_MAP` | 每个预期字段有来源映射 | 0.08 |
| `STATE.SUBMITTED` | 后端状态为 `submitted` | 0.04 |

错主体上限 0.55，错单位上限 0.70，关键字段错误上限 0.65，任一现金桥失败为 0，未提交上限 0.40。输入篡改或访问评测器状态则为 0 分并标为 `HACK`。

合成测试覆盖 golden、空白状态和现金桥断裂。源设计中的直接/间接法勾稽、汇率影响、非现金事项和受限资金政策，只有在拥有独立公开合成 fixture 后才会纳入。
