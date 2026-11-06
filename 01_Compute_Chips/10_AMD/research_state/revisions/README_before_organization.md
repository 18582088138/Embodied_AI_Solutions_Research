# AMD 具身智能软硬件平台调研

资料截止：2026-11-04。01—09中文Markdown及02A—02E、08A—08C独立专题已完成。用户已授权连续完成04—09，本轮报告完成检查，等待整体审阅；完成记录不等于用户批准。

按章节阅读，技术机制可从02/08专题深入，模型与真机证据分别见04/06。

- [01 硬件平台](01_Hardware_Platform.md)
- [02 软件栈总览](02_Software_Stack.md)
- [02 软件独立专题目录](02_Topics_Index.md)
- [03 传感器接入](03_Sensor_Integration.md)
- [04 AI能力与模型地图](04_AI_Capabilities.md)
- [05 仿真环境](05_Simulation_Environment.md)
- [06 机器人本体适配](06_Robot_Integration.md)
- [07 生态与量产责任](07_Ecosystem.md)
- [08 核心技术护城河总览](08_Core_Technology_Moat.md)
- [08A CDNA4/GPU数值、内存与执行](08A_GPU_Memory_and_Execution.md)
- [08B XDNA/IRON数值与显式数据流](08B_XDNA_Numerics_and_Dataflow.md)
- [08C Versal数据流、实时、安全与生命周期](08C_Versal_Dataflow_RealTime_and_Lifecycle.md)
- [09 SWOT、成本与条件选型](09_SWOT_Analysis.md)

资料与核验入口：

- [唯一资料归档](reference_metrial/index.html)
- [08总览及全部专题联合资料](reference_metrial/08_core/index.html)
- [09选型资料](reference_metrial/09_selection/index.html)
- [整体交付检查](reference_metrial/derived/qa/04_09_delivery_review.json)
- [章节状态](research_state/progress.json)
- [TCO假设与计算](research_state/depth_09/tco_calculations.json)
- [财报/法规原文取得缺口](research_state/depth_09/external_evidence_gaps.json)

04—09及08三个专题的原文、图源/哈希、主张核验、基线与最终零网络请求复用记录均保留。08联合索引包含56份来源，使用共享registry，没有每章重复下载同一原件。

限制：部分HTML静态依赖缺失，不能保证像素或动态交互完整；本轮新增IRON独立指南、财报和法规入口的robots核查连接失败，未作为有效引用。目标BSP/模型全图、实机并发/热稳定/P99/WCET、安全证书与运营ROI尚需目标系统证明。本文未安装SDK、训练/刷板、接本体或开展现场测试。

01—03及既有02软件专题与04开始前SHA256基线一致。本轮仅新增获授权报告/资料/证据并更新本目录和状态文件。
