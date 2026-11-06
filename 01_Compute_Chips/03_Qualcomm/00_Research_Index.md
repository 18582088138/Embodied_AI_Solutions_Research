# Qualcomm具身智能软硬件平台：研究总索引

资料截止：2026-11-05（Asia/Shanghai）。九章及九篇专题已完成公开资料研究。01维持已审阅版本；02—09及专题为完成待审阅，未代用户批准。研究交付为中文Markdown，统一归档原文与可取得的依赖。

## 建议阅读顺序

先读02软件总览掌握交接关系，再按03—07查看传感器、模型、仿真、本体与交付证据；08解释机制和条件，09形成采购与试点判断。需要复建时进入02六篇与08三篇专题。

## 01—09章节

- [01 硬件平台](01_Hardware_Platform.md)：已审阅，原版本保留。
- [02 软件栈总览](02_Software_Stack.md)：完成待审阅。
- [03 传感器、时钟与数据路径](03_Sensor_Integration.md)：完成待审阅。
- [04 AI能力与模型地图](04_AI_Capabilities.md)：完成待审阅。
- [05 仿真与真实交接](05_Simulation_Environment.md)：完成待审阅。
- [06 机器人本体适配与收益证据](06_Robot_Integration.md)：完成待审阅。
- [07 生态与量产交付](07_Ecosystem.md)：完成待审阅。
- [08 核心技术护城河](08_Core_Technology_Moat.md)：完成待审阅。
- [09 SWOT、TCO与条件选型](09_SWOT_Analysis.md)：完成待审阅。

## 02软件专题

[软件专题索引](02_Topics_Index.md)解释各专题交接、版本矩阵和未取得项。

- [02A Linux BSP与执行域](02A_Linux_BSP_and_Execution_Domains.md)
- [02B QNN／SNPE编译及runtime](02B_QNN_SNPE_Compilation_and_Runtime.md)
- [02C AI Hub与生成式部署](02C_AI_Hub_and_Generative_AI_Deployment.md)
- [02D 多媒体、感知与ROS](02D_Perception_Multimedia_and_ROS.md)
- [02E 机器人控制、仿真与运维](02E_Robotics_Control_Simulation_and_Operations.md)
- [02F RB6／Cloud AI 100独立栈](02F_RB6_Cloud_AI_100_Stack.md)

## 08机制专题

[核心技术专题索引](08_Topics_Index.md)汇总证据与机制边界。

- [08A 异构编译、量化与缓存](08A_Heterogeneous_Compilation.md)
- [08B 传感器、共享内存与同步](08B_Sensor_Memory_Pipeline.md)
- [08C 实时、安全域及更新边界](08C_Real_Time_Safety_Domains.md)

旧08_Proprietary_Technologies.md为保留的历史稿，本轮以08_Core_Technology_Moat及08A／B／C为交付依据。

## 主要结论及使用边界

Qualcomm的可核能力是目标芯片与BSP绑定的模型编译、多媒体数据路径及伙伴集成组合。选型收益成立需要算子／shape／校准匹配，传感器观测新鲜，以及动作与下层控制的失效契约。模型目录、组件时延、缓存文件和本体合作声明分别支持不同层级的结论，不能拼成已经验收的机器人闭环。

IRB10有厂商报告的产品级集成进展，NEURA有IQ10合作计划；精确本体BOM、在岗台数与任务收益尚有缺口。IQ10 planned SIL3不能作为已完成认证；通用PREEMPT_RT、DMA-BUF和Gunyah文档也不证明目标BSP全部启用。NITROS按2026-09-21的官方deprecated更新处理。09价格是归档快照，IFR行业量不等于芯片份额，TCO示例是假设计算。

部分网页静态依赖未取得，未承诺离线交互或像素一致。欧盟法规原始入口返回空正文，已从有效引用排除；政策章采用欧委会解释页并保留法条核验缺口。未取得的资料与未披露的信息分别标明。未实施刷机、训练、模型推理、机器人或安全认证测试。

## 原文、证据与审计入口

- [最终审阅与逐篇检查汇总](research_state/final_review.md)
- [审阅／授权及后续状态](research_state/progress.json)
- [项目唯一资料registry](REFERENCES.md)；每篇报告末尾提供原URL与本地原件。
- [最终全套检查记录](research_state/archive_qa/final_audit.json)；逐章历史QA和开始基线均保留。
- [全套引用复用去重记录](research_state/archive_qa/final_union_dedup_last_run.json)
- [排除的空正文法规候选](research_state/evidence/excluded_candidates_final.json)
- [02联合专题归档复用记录](research_state/archive_qa/02_union_dedup_last_run.json)
- [08联合专题归档复用记录](research_state/archive_qa/08_union_dedup_last_run.json)
