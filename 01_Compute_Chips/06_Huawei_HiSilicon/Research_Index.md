# Huawei / HiSilicon 具身智能平台调研总索引

数据截止2026-11-05。01—09及02A—02E、08A—08C共17篇研究正文已完成公开资料、源码/模型卡、许可、图源和归档检查。仅01已获用户审阅批准；其余完成表示调研与自检完成，不代替用户批准、设备测试或商业放行。01原文SHA256核对未变，历史08_Proprietary_Technologies.md保留，正式08以本索引链接为准。

## 按01—09阅读

|章节|正文|有效正文汉字|引用项|官方图|检查/证据|
|---|---|---|---|---|---|
|01|[硬件平台](01_Hardware_Platform.md)|8039|13|2|[检查](research_state/archive_qa/01_Hardware_Platform_quality.json) / [证据](research_state/evidence/01_Hardware_Platform.json)|
|02|[软件栈总览](02_Software_Stack.md)|2537|61|1|[检查](research_state/archive_qa/02_Software_Stack_quality.json) / [证据](research_state/evidence/02_Software_Stack.json)|
|03|[传感器接入](03_Sensor_Integration.md)|2468|14|2|[检查](research_state/archive_qa/03_Sensor_Integration_quality.json) / [证据](research_state/evidence/03_Sensor_Integration.json)|
|04|[AI能力与模型地图](04_AI_Capabilities.md)|2563|28|1|[检查](research_state/archive_qa/04_AI_Capabilities_quality.json) / [证据](research_state/evidence/04_AI_Capabilities.json)|
|05|[仿真环境](05_Simulation_Environment.md)|2324|14|1|[检查](research_state/archive_qa/05_Simulation_Environment_quality.json) / [证据](research_state/evidence/05_Simulation_Environment.json)|
|06|[机器人本体适配](06_Robot_Integration.md)|1995|15|1|[检查](research_state/archive_qa/06_Robot_Integration_quality.json) / [证据](research_state/evidence/06_Robot_Integration.json)|
|07|[生态建设](07_Ecosystem.md)|1900|22|1|[检查](research_state/archive_qa/07_Ecosystem_quality.json) / [证据](research_state/evidence/07_Ecosystem.json)|
|08|[核心技术护城河](08_Core_Technology_Moat.md)|2080|38|1|[检查](research_state/archive_qa/08_Core_Technology_Moat_quality.json) / [证据](research_state/evidence/08_Core_Technology_Moat.json)|
|09|[SWOT与条件选型](09_SWOT_Analysis.md)|3005|18|1|[检查](research_state/archive_qa/09_SWOT_Analysis_quality.json) / [证据](research_state/evidence/09_SWOT_Analysis.json)|

## 独立深度专题

[02专题索引](02_Topics_Index.md)提供五篇软件专题的机制与交接说明。

|专题|内容|字数/来源/图|核查入口|
|---|---|---|---|
|[02A_Ascend_CANN_Runtime](02A_Ascend_CANN_Runtime.md)|ATC/OM、AscendCL内存与异步/动态档位|2265 / 9 / 1|[检查](research_state/archive_qa/02A_Ascend_CANN_Runtime_quality.json) / [证据](research_state/evidence/02A_Ascend_CANN_Runtime.json) / [去重](research_state/archive_qa/02A_Ascend_CANN_Runtime_dedup.json)|
|[02B_Framework_Model_Deployment](02B_Framework_Model_Deployment.md)|TorchNPU、MindSpore Lite、YOLO和vLLM支持边界|2363 / 18 / 1|[检查](research_state/archive_qa/02B_Framework_Model_Deployment_quality.json) / [证据](research_state/evidence/02B_Framework_Model_Deployment.json) / [去重](research_state/archive_qa/02B_Framework_Model_Deployment_dedup.json)|
|[02C_HiSilicon_BSP_MPP_NPU](02C_HiSilicon_BSP_MPP_NPU.md)|BSP/MPP、旧NNIE与多执行域/媒体许可|2229 / 16 / 3|[检查](research_state/archive_qa/02C_HiSilicon_BSP_MPP_NPU_quality.json) / [证据](research_state/evidence/02C_HiSilicon_BSP_MPP_NPU.json) / [去重](research_state/archive_qa/02C_HiSilicon_BSP_MPP_NPU_dedup.json)|
|[02D_Robot_Integration_Operations](02D_Robot_Integration_Operations.md)|旧本体示例、消息/坐标/动作时效与运维|2380 / 11 / 1|[检查](research_state/archive_qa/02D_Robot_Integration_Operations_quality.json) / [证据](research_state/evidence/02D_Robot_Integration_Operations.json) / [去重](research_state/archive_qa/02D_Robot_Integration_Operations_dedup.json)|
|[02E_CloudRobo_Development_Platform](02E_CloudRobo_Development_Platform.md)|CloudRobo资源/权限、R2C生命周期、ROS2部署链|2772 / 15 / 1|[检查](research_state/archive_qa/02E_CloudRobo_Development_Platform_quality.json) / [证据](research_state/evidence/02E_CloudRobo_Development_Platform.json) / [去重](research_state/archive_qa/02E_CloudRobo_Development_Platform_dedup.json)|
|[08A_Ascend_Execution_Compilation](08A_Ascend_Execution_Compilation.md)|昇腾执行/编译、模型内存和机制对标|1817 / 13 / 1|[检查](research_state/archive_qa/08A_Ascend_Execution_Compilation_quality.json) / [证据](research_state/evidence/08A_Ascend_Execution_Compilation.json) / [去重](research_state/archive_qa/08A_Ascend_Execution_Compilation_dedup.json)|
|[08B_HiSilicon_Media_Memory](08B_HiSilicon_Media_Memory.md)|海思媒体帧/缓存、专用引擎及当前源码路径|1854 / 11 / 2|[检查](research_state/archive_qa/08B_HiSilicon_Media_Memory_quality.json) / [证据](research_state/evidence/08B_HiSilicon_Media_Memory.json) / [去重](research_state/archive_qa/08B_HiSilicon_Media_Memory_dedup.json)|
|[08C_CloudRobo_Action_Learning](08C_CloudRobo_Action_Learning.md)|CloudRobo动作/资产血缘、RLinf/Wan学习对照|2116 / 14 / 1|[检查](research_state/archive_qa/08C_CloudRobo_Action_Learning_quality.json) / [证据](research_state/evidence/08C_CloudRobo_Action_Learning.json) / [去重](research_state/archive_qa/08C_CloudRobo_Action_Learning_dedup.json)|

## 主要发现与使用边界

Huawei/HiSilicon能力分布于昇腾模型执行、海思视觉前端和CloudRobo云开发三层，三者不同设备与交付对象必须分别验收。服务器Atlas A2/910B不等于200I A2/310B；海思专用HNR/DPU不能视为任意模型可用通算力。

CloudRobo已有SO101/PI05、UR5e残差强化及Q25路径的具体开发实践，并公开R2C JSON/YAML生效与ROS2队列规则。RLinf增加第三方910B/CANN9.1.1、CPU OSMesa及Wan世界模型学习路线，仍无310B或海思端侧同条件支持证明。

09的TCO区分平台、模型、仿真、训练、存储/网络、本体及维护；50000/10000元仅为官方计费示例，不是正式现行报价。未获得市场份额、连续在岗规模和可归因ROI，不从合作/演示补数。数据出境按已归档监管原文及项目数据流判断，安全云功能不能代替机器人功能安全。

## 资料、复核与版本修订

[整套有效资料集合](REFERENCES.md)覆盖104项联合有效来源；[02联合61项](REFERENCES.md)、[08联合38项](REFERENCES.md)、[09资料](REFERENCES.md)复用唯一URL registry。HTML/PDF/源码/模型卡原件保留metadata和哈希，静态依赖缺失按实际状态披露，未保证动态登录、交互或像素级离线完整。

[最终联合去重运行](research_state/archive_qa/final_union_dedup.json)与[最终整套审计](research_state/archive_qa/final_package_audit.json)记录实际检查与请求统计。[排除/失败/待取件清单](research_state/evidence/final_rejected_and_pending.json)区别原文未披露、未取得、访问限制与版本不适用。

后续新证据已小范围补入02、04、05，原报告、前后哈希和修订基线存于[修订记录](research_state/revisions)。main/master快照与提交SHA/tag表述已统一核对。各篇最初基线和逐章检查保留；最终审计使用整套完成后的冻结基线，验证当前文件及资料一致性，不能替代最初保护基线。

仍需取得当前目标SKU正式手册/SDK/商业许可、准确模型与资产版本、同条件并发/热/闭环失效测试、正式价格/交期/生命周期、客户任务与运营收益及逐案区域政策分类。公开调研至此完成，工程和商业放行仍以项目实测与合同为准。
