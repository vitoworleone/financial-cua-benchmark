# Python Verifier

`verifier/` 是金融 CUA Benchmark 的确定性评分实现，使用 Python 标准库和 `pytest`。

## 已实现任务

| 任务 | 主要检查 |
| --- | --- |
| `fin_d1_balance_sheet` | 报表字段、单位、主体/期间/口径、资产负债权益平衡、小计、来源与提交状态 |
| `fin_d2_cash_flow` | 现金流字段、现金净变动、期初期末滚动、来源与提交状态 |
| `fin_d3_finance_lease_schedule` | ACT/360、实际天数、利息、本金拆分、期间滚动、汇总与提交状态 |

## 代码结构

```text
src/finbench/contracts.py  # 提交物、真值、检查结果和评分结果的数据合同
src/finbench/core.py       # 数值归一化、通用检查与评分聚合
src/finbench/tasks/        # 任务级 Verifier
tests/                     # 正确、错误和安全场景测试
```

## 运行方式

在仓库根目录执行：

```powershell
python -m pytest
```

测试覆盖正确提交、未完成状态、关键公式错误、元数据错误和输入完整性问题。
