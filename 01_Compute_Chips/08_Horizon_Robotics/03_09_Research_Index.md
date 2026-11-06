# Horizon / D-Robotics：03—09调研审阅入口

截止2026-11-05，按03→09顺序完成。本轮交付七章及08的三个独立专题，共十篇研究正文；每篇均保留官方URL、本地原件、图源、关键主张审阅和独立检查。01已获用户批准，02已完成待审阅；本轮03—09完成待审阅，未代记批准。

| 报告 | 正文有效汉字 | 引用数 | 官方图数 | 核验 |
|---|---|---|---|---|
| [03_Sensor_Integration：传感器接入](03_Sensor_Integration.md) | 1817 | 11 | 3 | [pass](research_state/qa/03_Sensor_Integration_check.json) |
| [04_AI_Capabilities：AI模型与部署](04_AI_Capabilities.md) | 2132 | 25 | 2 | [pass](research_state/qa/04_AI_Capabilities_check.json) |
| [05_Simulation_Environment：仿真与验证](05_Simulation_Environment.md) | 1977 | 9 | 1 | [pass](research_state/qa/05_Simulation_Environment_check.json) |
| [06_Robot_Integration：机器人本体适配](06_Robot_Integration.md) | 2170 | 14 | 1 | [pass](research_state/qa/06_Robot_Integration_check.json) |
| [07_Ecosystem：生态与量产支持](07_Ecosystem.md) | 2262 | 28 | 1 | [pass](research_state/qa/07_Ecosystem_check.json) |
| [08_Core_Technology_Moat：核心技术护城河总览](08_Core_Technology_Moat.md) | 2067 | 22 | 1 | [pass](research_state/qa/08_Core_Technology_Moat_check.json) |
| [08A_Compute_Compilation_and_Quantization：量化与编译专题](08A_Compute_Compilation_and_Quantization.md) | 2093 | 15 | 2 | [pass](research_state/qa/08A_Compute_Compilation_and_Quantization_check.json) |
| [08B_Sensor_Memory_and_Time：共享内存与时间专题](08B_Sensor_Memory_and_Time.md) | 2214 | 13 | 2 | [pass](research_state/qa/08B_Sensor_Memory_and_Time_check.json) |
| [08C_Real_Time_Trust_and_Lifecycle：实时/可信启动/生命周期专题](08C_Real_Time_Trust_and_Lifecycle.md) | 2211 | 16 | 1 | [pass](research_state/qa/08C_Real_Time_Trust_and_Lifecycle_check.json) |
| [09_SWOT_Analysis：SWOT与条件选型](09_SWOT_Analysis.md) | 3317 | 23 | 1 | [pass](research_state/qa/09_SWOT_Analysis_check.json) |

## 资料、专题与归档

[01硬件样章](01_Hardware_Platform.md) · [02软件专题导航](02_Topics_Index.md) · [08专题导航](08_Topics_Index.md)

[资料总入口](REFERENCES.md) · [08联合集合（43份）](REFERENCES.md) · [03—09联合清单](research_state/manifests/Horizon_03_09_union.json) · [最终审计](research_state/qa/03_09_final_audit.json) · [零网络复用](research_state/qa/03_09_union_last_run.json)

联合引用去重后99份，归档状态{'complete_static': 95, 'partial_static': 4}；23个动态正文页面由已归档官方JS离线渲染，原件/文本/HTML哈希复核一致。图共15次引用，12个不同图像哈希，均实际打开检查。结构通过不等于事实自动证明、动态交互完整或实机性能已验收。

partial_static来源为：Horizon_JD_Journey6P_DesignIn、Horizon_DRobotics_Funding_Relation、H08_Isaac_Safety、H09_Reports_Index。缺失依赖逐页记录，正文引用明确边界；财报目录仅为检索入口，官方嵌入报告未取得，不作财务数字证据。失败模型卡/候选保留为取得记录，不参与支持关键结论。

## 主要结论与待补证据

S600具备可追踪的VLA/VLM部署、媒体/内存和MCU协同路线，值得按具体任务进行概念验证。量化质量、观察时间与buffer寿命、真实动作契约、热稳态并发和失败恢复决定其实际价值；TOPS、模型毫秒数和伙伴名单不能替代闭环效果。

本轮保留S100/S600同步SKU冲突、EtherCAT周期日志冲突、当前miniboot无内建回滚与旧稿差异，以及5.1.1和OE/TROS绑定版本问题。商业BSP/MCAL、模型权重/数据许可、安全手册/WCET、有效报价/PCN/EOL与具体本体运营收益仍需补齐。

09给出科研、操作、AMR、固定视觉、消费、工业和安全应用的条件选型，以及带单位与假设的TCO模型。厂商50%覆盖率无分母不当份额；京东征程6P定点与未来部署预测不当已交付；政策按真实公众服务与数据处理链判断，未作具体项目法律或贸易适用保证。

本轮未安装SDK、运行模型/仿真容器、烧写固件或测试机器人；未申请商业NDA资料。研究结论和建议验证动作均与实测结果分开。

[进度与待核验状态](research_state/progress.json)；01、02及旧08稿哈希保护通过，旧03—07、09稿备份保存在research_state/history。
