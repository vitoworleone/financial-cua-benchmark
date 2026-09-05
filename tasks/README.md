# 任务包

本目录采用中文优先的任务合同。已经完成规范化的示范任务：

- [`fin_d1_balance_sheet`](fin_d1_balance_sheet/task.md)：资产负债表填报；
- [`fin_d2_cash_flow`](fin_d2_cash_flow/task.md)：现金流量表填报；
- [`fin_d3_finance_lease_schedule`](fin_d3_finance_lease_schedule/task.md)：配置化融资租赁案例适配器。

三者均对应 `verifier/` 中的明确 checker ID 与纯合成测试；它们**不代表**浏览器运行环境、私有测试集或模型跑分已经公开。

其余源任务在完成同样的审阅之前，只在 [`catalog.yaml`](catalog.yaml) 中记录状态。

每个迁移完成的任务包应包含：

```text
task.md        # Agent 可见任务合同和可观察产物
verifier.md    # checker ID、评分、封顶、红线与对抗状态
SKILL.md       # 可公开复用的领域知识与操作边界（如适用）
```

任务包不得包含实例答案、hidden truth 位置、本机路径，也不得把只有文档设计的任务写成已经端到端运行。
