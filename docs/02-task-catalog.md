# 任务总表

## 统计口径

财务会计赛道包含 **20 个标准 Benchmark 任务**。另有一个融资租赁摊还表案例适配器，它服务于实例化 schedule 复核，不计入第 21 个通用任务。

债券承做赛道现有 6 个任务设计，围绕真实承做材料的提取、核验、勾稽与初稿准备展开。

## 赛道 A：财务会计 20 个标准任务

| ID | 难度 | 任务 | 核心能力 |
| --- | --- | --- | --- |
| `fin_d1_balance_sheet` | D1 | 资产负债表填报 | 概念映射、单位、期间、表内平衡、提交状态 |
| `fin_d1_income_statement` | D1 | 分步式利润表填报 | 分层利润构建、精度、当前/比较期间 |
| `fin_d2_cash_flow` | D2 | 现金流量表填报 | 直接/间接法、滚动、跨表核对 |
| `fin_d2_three_statements` | D2 | 三大报表勾稽 | 多交付物依赖与跨表一致性 |
| `fin_d2_equity_changes` | D2 | 所有者权益变动表 | 列滚动、OCI、母公司/少数股东处理 |
| `fin_d2_bank_reconciliation` | D2 | 银行存款余额调节 | 账面/银行项目、未达项与最终平衡 |
| `fin_d2_iit_settlement` | D2 | 个人所得税汇算清缴 | 多源汇总与政策约束重算 |
| `fin_d2_stamp_duty_surcharges` | D2 | 印花税及附加税费申报 | 税基、政策适用性、申报产物 |
| `fin_d3_ar_aging_ecl` | D3 | 应收账款账龄与 ECL | 账龄分桶、组合 ECL、可追溯性 |
| `fin_d3_bank_provision` | D3 | 银行减值准备与资本充足率 | 不良构成、拨备、RWA、资本指标 |
| `fin_d3_cit_annual` | D3 | 企业所得税汇算清缴 | 会计税务差异、亏损与优惠 |
| `fin_d3_finance_lease` | D3 | 融资租赁会计处理 | 实际利率法与期间滚动 |
| `fin_d3_fund_nav` | D3 | 基金净值估值 | 持仓估值、应计、单位净值 |
| `fin_d3_insurance` | D3 | 保险合同与偿付能力 | 准备金、监管指标、滚动 |
| `fin_d3_lvat_liquidation` | D3 | 土地增值税清算 | 项目汇总与超率累进 |
| `fin_d3_related_party` | D3 | 关联方与合并调整 | 关系图谱、交易、抵销 |
| `fin_d3_securities` | D3 | 证券自营与持仓估值 | 公允价值、资管隔离、陈旧价格识别 |
| `fin_d3_vat_filing` | D3 | 增值税纳税申报 | 发票、销项/进项、留抵 |
| `fin_d4_consolidation_selfcheck` | D4 | 合并报表自查 | 抵销、少数股东权益、商誉、异常修复 |
| `fin_d4_financial_instruments` | D4 | 金融工具分类与计量 | 业务模式、SPPI、摊余成本与公允价值 |

## 独立案例适配器

| ID | 定位 | 当前处理方式 |
| --- | --- | --- |
| `fin_d3_finance_lease_schedule` | 配置化 ACT/360 租赁摊还表复核 | 由实例化条款、现金流和计息约定驱动的通用 schedule Verifier |

## 赛道 B：债券承做工作流设计

| ID | 任务 | 主要输出 | 预期验证方式 |
| --- | --- | --- | --- |
| `bond_t1_financial_summary` | 审计报告到财务摘要 | 财务摘要与来源注释 | 字段真值、计算、来源指针、人工会计复核 |
| `bond_t2_workpaper_completeness` | 工作底稿完整性检查 | 缺失材料清单与复核队列 | 文件/元数据匹配、必需覆盖度、人工充分性判断 |
| `bond_t3_prospectus_consistency` | 募集说明书与财务摘要一致性核对 | 一致性问题表 | 字段/期间/单位比较、人工披露判断 |
| `bond_t4_feedback_reply` | 交易所反馈回复底稿 | 回复初稿与披露清单 | 数值真值、结构、证据映射、受约束文本复核 |
| `bond_t5_abs_asset_reconciliation` | ABS 资产合同、发票与回款勾稽 | 资产核验表与异常项 | 记录关联、计算、异常覆盖、专家复核 |
| `bond_t6_market_ranking` | 承销市场排名与文字披露 | 排名表与市场描述 | 确定性排序/公式、来源可追溯、人工市场解释 |
