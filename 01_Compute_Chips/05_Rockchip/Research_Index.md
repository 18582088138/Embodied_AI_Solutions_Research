# Rockchip 具身智能平台调研总索引

截至2026-11-05，按01→09顺序完成公开文献、官方原件、API和源码静态研究。01为已审阅样章；02—09及必要专题依据用户“继续后面全部内容的调研”连续完成，研究完成不代用户批准或实机验收。

交付9章主报告、02的5篇专题、08的3篇专题，共17篇研究正文；实际引用联合清单含139个registry来源（按来源名称计，规范URL另由registry去重），有效正文汉字合计44305。每篇正文达到1500有效汉字底线并通过结构/归档检查，图像逐张核查；全部引用联合复用运行为零网络请求。

| 报告 | 内容与读法 | 有效汉字 | 原件 | 图 | 检查/证据/去重 |
| --- | --- | --- | --- | --- | --- |
| [01_Hardware_Platform](01_Hardware_Platform.md) | 已审阅样章：芯片/板卡、规格与供应 | 7727 | 29 | 7 | [检查](research_state/archive_qa/01_Hardware_Platform_quality.json)；[证据](research_state/evidence/01_Hardware_Platform.json)；[去重](research_state/archive_qa/01_Hardware_Platform_dedup_last_run.json) |
| [02_Software_Stack](02_Software_Stack.md) | 软件总览与链路交接 | 1711 | 14 | 1 | [检查](research_state/archive_qa/02_Software_Stack_quality.json)；[证据](research_state/evidence/02_Software_Stack.json)；[去重](research_state/archive_qa/02_Software_Stack_dedup_last_run.json) |
| [02A_BSP_Multimedia](02A_BSP_Multimedia.md) | BSP、多媒体、GPU与buffer | 2927 | 19 | 1 | [检查](research_state/archive_qa/02A_BSP_Multimedia_quality.json)；[证据](research_state/evidence/02A_BSP_Multimedia.json)；[去重](research_state/archive_qa/02A_BSP_Multimedia_dedup_last_run.json) |
| [02B_RKNN2_Compiler_Runtime](02B_RKNN2_Compiler_Runtime.md) | RKNN2编译/量化/runtime | 2549 | 14 | 3 | [检查](research_state/archive_qa/02B_RKNN2_Compiler_Runtime_quality.json)；[证据](research_state/evidence/02B_RKNN2_Compiler_Runtime.json)；[去重](research_state/archive_qa/02B_RKNN2_Compiler_Runtime_dedup_last_run.json) |
| [02C_RKLLM](02C_RKLLM.md) | RKLLM模型与多模态会话 | 2419 | 12 | 1 | [检查](research_state/archive_qa/02C_RKLLM_quality.json)；[证据](research_state/evidence/02C_RKLLM.json)；[去重](research_state/archive_qa/02C_RKLLM_dedup_last_run.json) |
| [02D_RKNN3_RK182X](02D_RKNN3_RK182X.md) | RKNN3协处理器/Server | 1985 | 8 | 1 | [检查](research_state/archive_qa/02D_RKNN3_RK182X_quality.json)；[证据](research_state/evidence/02D_RKNN3_RK182X.json)；[去重](research_state/archive_qa/02D_RKNN3_RK182X_dedup_last_run.json) |
| [02E_ROS_Control_Operations](02E_ROS_Control_Operations.md) | ROS/AMP/实时/OTA | 2024 | 15 | 0 | [检查](research_state/archive_qa/02E_ROS_Control_Operations_quality.json)；[证据](research_state/evidence/02E_ROS_Control_Operations.json)；[去重](research_state/archive_qa/02E_ROS_Control_Operations_dedup_last_run.json) |
| [03_Sensor_Integration](03_Sensor_Integration.md) | 采集、带宽、标定与时间 | 1855 | 12 | 1 | [检查](research_state/archive_qa/03_Sensor_Integration_quality.json)；[证据](research_state/evidence/03_Sensor_Integration.json)；[去重](research_state/archive_qa/03_Sensor_Integration_dedup_last_run.json) |
| [04_AI_Capabilities](04_AI_Capabilities.md) | 模型地图、VLA/视觉部署边界 | 2261 | 12 | 1 | [检查](research_state/archive_qa/04_AI_Capabilities_quality.json)；[证据](research_state/evidence/04_AI_Capabilities.json)；[去重](research_state/archive_qa/04_AI_Capabilities_dedup_last_run.json) |
| [05_Simulation_Environment](05_Simulation_Environment.md) | 仿真、训练与sim-to-real | 1970 | 10 | 1 | [检查](research_state/archive_qa/05_Simulation_Environment_quality.json)；[证据](research_state/evidence/05_Simulation_Environment.json)；[去重](research_state/archive_qa/05_Simulation_Environment_dedup_last_run.json) |
| [06_Robot_Integration](06_Robot_Integration.md) | 产品绑定、演示与运营边界 | 2454 | 8 | 2 | [检查](research_state/archive_qa/06_Robot_Integration_quality.json)；[证据](research_state/evidence/06_Robot_Integration.json)；[去重](research_state/archive_qa/06_Robot_Integration_dedup_last_run.json) |
| [07_Ecosystem](07_Ecosystem.md) | 伙伴分工、产线、保修与开放性 | 2339 | 24 | 1 | [检查](research_state/archive_qa/07_Ecosystem_quality.json)；[证据](research_state/evidence/07_Ecosystem.json)；[去重](research_state/archive_qa/07_Ecosystem_dedup_last_run.json) |
| [08_Core_Technology_Moat](08_Core_Technology_Moat.md) | 跨机制价值与条件判断 | 2108 | 16 | 1 | [检查](research_state/archive_qa/08_Core_Technology_Moat_quality.json)；[证据](research_state/evidence/08_Core_Technology_Moat.json)；[去重](research_state/archive_qa/08_Core_Technology_Moat_dedup_last_run.json) |
| [08A_Quantization_Compiler](08A_Quantization_Compiler.md) | GRQ/格式/映射/插件/精度 | 2014 | 10 | 1 | [检查](research_state/archive_qa/08A_Quantization_Compiler_quality.json)；[证据](research_state/evidence/08A_Quantization_Compiler.json)；[去重](research_state/archive_qa/08A_Quantization_Compiler_dedup_last_run.json) |
| [08B_Memory_Coprocessor_Multicard](08B_Memory_Coprocessor_Multicard.md) | DRAM/KV/多卡/队列/链路 | 2257 | 10 | 1 | [检查](research_state/archive_qa/08B_Memory_Coprocessor_Multicard_quality.json)；[证据](research_state/evidence/08B_Memory_Coprocessor_Multicard.json)；[去重](research_state/archive_qa/08B_Memory_Coprocessor_Multicard_dedup_last_run.json) |
| [08C_Perception_RealTime_Trust](08C_Perception_RealTime_Trust.md) | ISP/时间/实时/可信与安全边界 | 2256 | 16 | 1 | [检查](research_state/archive_qa/08C_Perception_RealTime_Trust_quality.json)；[证据](research_state/evidence/08C_Perception_RealTime_Trust.json)；[去重](research_state/archive_qa/08C_Perception_RealTime_Trust_dedup_last_run.json) |
| [09_SWOT_Analysis](09_SWOT_Analysis.md) | 商业分级、TCO、政策与条件选型 | 3449 | 25 | 1 | [检查](research_state/archive_qa/09_SWOT_Analysis_quality.json)；[证据](research_state/evidence/09_SWOT_Analysis.json)；[去重](research_state/archive_qa/09_SWOT_Analysis_dedup_last_run.json) |

[02专题索引](02_Topics_Index.md)；[08专题索引](08_Topics_Index.md)；[全部原件归档](REFERENCES.md)；[最终引用联合清单](research_state/manifests/Rockchip_01_09_Union.json)；[最终零网络去重](research_state/archive_qa/01_09_Union_dedup_last_run.json)；[最终审计](research_state/archive_qa/Final_Research_Audit.json)；[研究状态](research_state/progress.json)。

## 主要结论与限制

Rockchip形成SoC视觉/控制与RK182X语言/多模态协处理器的组合路线，RKNN工具、ISP/多媒体、伙伴板卡和工业文档提供可复用工程入口。其价值成立于模型受支持、精度与数据年龄合格、控制/保护独立验证、BSP与供应责任明确；当前证据不能给全面性能排名或机器人ROI。

软件重点版本为RKNN2/Zoo2.5.0、RKLLM1.3.1、RKNN3手册1.2.0。板商BSP、模型commit和运行库需单独锁定。RKNN3多卡为显式分段与主机队列转发，分页模型本版request_num只支持1；模型阶段benchmark与VLA演示FPS不是完整闭环/P99/WCET或任务成功率。

未进行SDK安装、模型运行、板端/机器人测试、下单或key烧写。完整BSP/TRM、实际DRAM带宽、并发热稳定与能耗、VLA完整配置和留出任务结果、功能安全、逐料号PCN/EOL/含税交期与现场合同仍需项目证据。HTML依赖缺损逐原件披露，动态交互/视频不保证完整。旧08_Proprietary_Technologies.md保持历史占位，当前08入口为08_Core_Technology_Moat.md。

财报官方目录/API已取得，但上交所三季报/半年报/年度摘要请求返回浏览器校验页，已拒收；个人信息保护法候选URL404。上述失败资料不计入有效引用，不引用收入/利润/市场份额数字。政策采用已取得的生成式AI办法原文，有限范围不代表完整当期法律/出海审查。[09未取得原件记录](research_state/archive_qa/09_unobtained_sources.json)。
