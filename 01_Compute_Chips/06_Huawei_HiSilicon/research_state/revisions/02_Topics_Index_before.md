# 02 软件栈专题索引

数据截止2026-11-05。总览与四篇专题均完成文献、原码、许可、图源与归档检查；完成不代表目标硬件已实测。用户追加授权继续剩余全部章节，下一步按03—09顺序推进。

[02软件栈总览](../../02_Software_Stack.md)先给路径选择和版本/成熟度矩阵；下面按机制阅读。


## 02A_Ascend_CANN_Runtime

[专题正文](../../02A_Ascend_CANN_Runtime.md)：ATC→OM、stub与真实runtime、context/stream、model descriptor/dataset及内存所有权；同步/异步完成、队列和动态档位。旧310官方样例作为API参考，当前310B目标不能直接套用。

2265有效正文汉字；9项来源；1张官方图；检查pass。[主张/图源](../evidence/02A_Ascend_CANN_Runtime.json)；[结构归档检查](../../reference_metrial/derived/qa/02A_Ascend_CANN_Runtime_quality.json)；[专题去重复用](../../reference_metrial/derived/qa/02A_Ascend_CANN_Runtime_dedup.json)。

## 02B_Framework_Model_Deployment

[专题正文](../../02B_Framework_Model_Deployment.md)：TorchNPU设备/算子和图接入、构建/发行/维护版本分别判断；MindSpore Lite转换与CPU backup；YOLO静态FP16部署到InferSession；vLLM对200I A2的明确排除，AGPL/Apache/BSD/CCBY等许可分开。

2363有效正文汉字；18项来源；1张官方图；检查pass。[主张/图源](../evidence/02B_Framework_Model_Deployment.json)；[结构归档检查](../../reference_metrial/derived/qa/02B_Framework_Model_Deployment_quality.json)；[专题去重复用](../../reference_metrial/derived/qa/02B_Framework_Model_Deployment_dedup.json)。

## 02C_HiSilicon_BSP_MPP_NPU

[专题正文](../../02C_HiSilicon_BSP_MPP_NPU.md)：BSP/OSDRV、VI/ISP/VPSS/VENC、SYS/VB/MMZ及cached buffer；旧NNIE Caffe/WK、CPU分段与RuyiStudio，当前3403第三方帧代码；OpenHarmony DV300端口与媒体EULA边界。

2229有效正文汉字；16项来源；3张官方图；检查pass。[主张/图源](../evidence/02C_HiSilicon_BSP_MPP_NPU.json)；[结构归档检查](../../reference_metrial/derived/qa/02C_HiSilicon_BSP_MPP_NPU_quality.json)；[专题去重复用](../../reference_metrial/derived/qa/02C_HiSilicon_BSP_MPP_NPU_dedup.json)。

## 02D_Robot_Integration_Operations

[专题正文](../../02D_Robot_Integration_Operations.md)：旧200DK+D435+Dobot和下棋/小车示例的真实分工；帧ID/曝光时刻、坐标反投影、动作期限、策略与伺服分层；容器主机依赖、并发观测、模型配置升级与OTA回退条件。

2380有效正文汉字；11项来源；1张官方图；检查pass。[主张/图源](../evidence/02D_Robot_Integration_Operations.json)；[结构归档检查](../../reference_metrial/derived/qa/02D_Robot_Integration_Operations_quality.json)；[专题去重复用](../../reference_metrial/derived/qa/02D_Robot_Integration_Operations_dedup.json)。

## 联合资料与使用方法

[本章有效资料集合](../../reference_metrial/02_software_depth/index.html)覆盖总览及所有专题联合46项引用，使用同一URL registry；collection仅建立复用视图。[最终联合去重记录](../../reference_metrial/derived/qa/02_Software_Stack_dedup.json)保留实际请求统计，不用refresh模拟复用。[排除候选日志](../evidence/02_rejected_candidates.json)保留空壳动态页，不将HTTP200等同有效正文。

旧2021教材、2023样例仓和2026框架固定提交分别限定版本；代码、模型、资料及SDK的许可证不互相替代。官方图讲解可用来理解分层与流程，不能当同条件性能比较。所有专题声明未开展实机/本体测试；量产所需包、许可、并发性能和失效条件仍待实际验证。
