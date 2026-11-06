# 02 软件专题索引

研究截止2026-11-05。各篇为公开资料核验，未实施刷机、云上传、模型或机器人测量。用户已授权连续03—09；完成不等于用户审阅批准。

## [02A_Linux_BSP_and_Execution_Domains](02A_Linux_BSP_and_Execution_Domains.md)

系统镜像、执行域、固件及OTA绑定。资料数8，官方图1，结构检查pass。关键版本与证据缺口在各篇正文列出；共享registry保留原件与缺失依赖。

[证据](research_state/evidence/02A_Linux_BSP_and_Execution_Domains.json)｜[检查](research_state/archive_qa/02A_Linux_BSP_and_Execution_Domains_quality.json)｜[去重记录](research_state/archive_qa/02A_Linux_BSP_and_Execution_Domains_dedup_last_run.json)

## [02B_QNN_SNPE_Compilation_and_Runtime](02B_QNN_SNPE_Compilation_and_Runtime.md)

图编译、量化、context及tensor生命周期。资料数6，官方图1，结构检查pass。关键版本与证据缺口在各篇正文列出；共享registry保留原件与缺失依赖。

[证据](research_state/evidence/02B_QNN_SNPE_Compilation_and_Runtime.json)｜[检查](research_state/archive_qa/02B_QNN_SNPE_Compilation_and_Runtime_quality.json)｜[去重记录](research_state/archive_qa/02B_QNN_SNPE_Compilation_and_Runtime_dedup_last_run.json)

## [02C_AI_Hub_and_Generative_AI_Deployment](02C_AI_Hub_and_Generative_AI_Deployment.md)

云模型流程、Genie会话与KV缓存。资料数8，官方图1，结构检查pass。关键版本与证据缺口在各篇正文列出；共享registry保留原件与缺失依赖。

[证据](research_state/evidence/02C_AI_Hub_and_Generative_AI_Deployment.json)｜[检查](research_state/archive_qa/02C_AI_Hub_and_Generative_AI_Deployment_quality.json)｜[去重记录](research_state/archive_qa/02C_AI_Hub_and_Generative_AI_Deployment_dedup_last_run.json)

## [02D_Perception_Multimedia_and_ROS](02D_Perception_Multimedia_and_ROS.md)

视频caps、预处理、DMA与检测元数据。资料数10，官方图1，结构检查pass。关键版本与证据缺口在各篇正文列出；共享registry保留原件与缺失依赖。

[证据](research_state/evidence/02D_Perception_Multimedia_and_ROS.json)｜[检查](research_state/archive_qa/02D_Perception_Multimedia_and_ROS_quality.json)｜[去重记录](research_state/archive_qa/02D_Perception_Multimedia_and_ROS_dedup_last_run.json)

## [02E_Robotics_Control_Simulation_and_Operations](02E_Robotics_Control_Simulation_and_Operations.md)

ROS消息、运动/仿真及部署运维。资料数15，官方图1，结构检查pass。关键版本与证据缺口在各篇正文列出；共享registry保留原件与缺失依赖。

[证据](research_state/evidence/02E_Robotics_Control_Simulation_and_Operations.json)｜[检查](research_state/archive_qa/02E_Robotics_Control_Simulation_and_Operations_quality.json)｜[去重记录](research_state/archive_qa/02E_Robotics_Control_Simulation_and_Operations_dedup_last_run.json)

## [02F_RB6_Cloud_AI_100_Stack](02F_RB6_Cloud_AI_100_Stack.md)

QPC、PCIe运行时、InferenceSet与缓冲归还。资料数6，官方图1，结构检查pass。关键版本与证据缺口在各篇正文列出；共享registry保留原件与缺失依赖。

[证据](research_state/evidence/02F_RB6_Cloud_AI_100_Stack.json)｜[检查](research_state/archive_qa/02F_RB6_Cloud_AI_100_Stack_quality.json)｜[去重记录](research_state/archive_qa/02F_RB6_Cloud_AI_100_Stack_dedup_last_run.json)

## [02_Software_Stack](02_Software_Stack.md)

跨栈版本和模型到动作契约总览。资料数19，官方图1，结构检查pass。关键版本与证据缺口在各篇正文列出；共享registry保留原件与缺失依赖。

[证据](research_state/evidence/02_Software_Stack.json)｜[检查](research_state/archive_qa/02_Software_Stack_quality.json)｜[去重记录](research_state/archive_qa/02_Software_Stack_dedup_last_run.json)

## 交接与复建

系统→驱动与固件；模型→源码/库/DLC/context或QPC；相机→caps和buffer；推理→tensor与元数据；ROS→encoding、frame与原始采集时间；控制→关节/单位、horizon和失效契约。各层兼容须用目标板发行矩阵确认，不能以同名SDK或单个demo替代闭环证明。

[联合资料清单](research_state/manifests/Qualcomm_02_union.json)｜[联合去重](research_state/archive_qa/02_union_dedup_last_run.json)
