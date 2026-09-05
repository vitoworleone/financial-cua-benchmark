# 任务包

每个任务包包含两类文档：

```text
task.md        # Agent 的业务目标、输入、交付物和任务约束
verifier.md    # 检查器、公式、评分和业务红线
```

已提供三个完整示例：

- [`fin_d1_balance_sheet`](fin_d1_balance_sheet/task.md)：企业资产负债表填报；
- [`fin_d2_cash_flow`](fin_d2_cash_flow/task.md)：现金流量表填报；
- [`fin_d3_finance_lease_schedule`](fin_d3_finance_lease_schedule/task.md)：融资租赁 ACT/360 摊还表复核。

所有任务遵循相同结构：业务目标、可见输入、最终交付物、可验证不变量、来源映射与提交状态。
