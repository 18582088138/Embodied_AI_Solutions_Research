# 02 软件专题索引

本章总览与六篇专题已完成独立检查，等待用户审阅；未开始03。本章采集窗口2026-11-04—11-05，已批准的01保留。

- [02软件栈总览](02_Software_Stack.md)
- [联合官方资料索引](REFERENCES.md)

| 专题 | 核心机制与边界 | 独立检查 | 最终复用 |
|---|---|---|---|
| [CPU内核：KleidiAI与ACL](02A_CPU_KleidiAI_ACL.md) | packing与prepare/run，计量含/不含项 | [pass](research_state/archive_qa/02A_CPU_KleidiAI_ACL_quality.json) | [0网络请求](research_state/archive_qa/02A_CPU_KleidiAI_ACL_dedup_last_run.json) |
| [Ethos：Vela/TFLM/CMSIS与FVP部署](02B_Ethos_Vela_CMSIS.md) | command stream/base地址/arena；Vela与driver原件取得受限 | [pass](research_state/archive_qa/02B_Ethos_Vela_CMSIS_quality.json) | [0网络请求](research_state/archive_qa/02B_Ethos_Vela_CMSIS_dedup_last_run.json) |
| [BSP、实时与多域通信](02C_BSP_Multidomain.md) | remoteproc/RPMsg、cache、RT、boot及回退 | [pass](research_state/archive_qa/02C_BSP_Multidomain_quality.json) | [0网络请求](research_state/archive_qa/02C_BSP_Multidomain_dedup_last_run.json) |
| [Jetson：TensorRT、Isaac与ROS部署](02D_Jetson_ROS_Deployment.md) | engine/profile与动态batch；buffer迁移与版本差异 | [pass](research_state/archive_qa/02D_Jetson_ROS_Deployment_quality.json) | [0网络请求](research_state/archive_qa/02D_Jetson_ROS_Deployment_dedup_last_run.json) |
| [TI：TIDL校准、IO、多核与ROS](02E_TI_TIDL.md) | net/io与共享pool、复制开销、层边界抢占 | [pass](research_state/archive_qa/02E_TI_TIDL_quality.json) | [0网络请求](research_state/archive_qa/02E_TI_TIDL_dedup_last_run.json) |
| [S100：Nash编译、UCP、TROS与MCU](02F_S100_BPU.md) | HBM/stride/cache/异步task；function-call抢占与企业源码 | [pass](research_state/archive_qa/02F_S100_BPU_quality.json) | [0网络请求](research_state/archive_qa/02F_S100_BPU_dedup_last_run.json) |

专题原件共享唯一registry；联合清单覆盖总览与全部专题，不以最后一篇代替整章。静态依赖缺失逐表披露，动态正文模块与抽取文本明确区分；这些检查不替代事实语义审计、法律审计或板卡/机器人实测。

- [联合去重记录（82份，0网络请求）](research_state/archive_qa/02_Software_Depth_Union_dedup_last_run.json)
- [最终基线保护与专题审计](research_state/archive_qa/02_Software_Depth_final_audit.json)

本章引用：82份，72份完整静态归档、10份有部分呈现依赖缺失；8张不同官方图已逐张核验。动态模块原件保留，不承诺交互完整。
