# 02 软件栈专题索引

截至2026-11-05。总览与5篇专题完成公开文献/API研究及逐篇检查；未执行SDK安装、板端测试或机器人验收。01已审阅，其余由用户明确授权连续研究。

| 报告 | 研究对象/交接 | 正文汉字 | 原件数 | 图 | 验证 |
| --- | --- | --- | --- | --- | --- |
| [02_Software_Stack](02_Software_Stack.md) | 能力/接口与版本总图；模型到传感器/动作的缺口 | 1711 | 14 | 1 | [检查](research_state/archive_qa/02_Software_Stack_quality.json)；[证据](research_state/evidence/02_Software_Stack.json)；[基线](research_state/baselines/02_Software_Stack_before.json)；[去重](research_state/archive_qa/02_Software_Stack_dedup_last_run.json) |
| [02A_BSP_Multimedia](02A_BSP_Multimedia.md) | kernel/DTS→MPP/RGA/GPU→buffer；stride、DMA与所有权 | 2927 | 19 | 1 | [检查](research_state/archive_qa/02A_BSP_Multimedia_quality.json)；[证据](research_state/evidence/02A_BSP_Multimedia.json)；[基线](research_state/baselines/02A_BSP_Multimedia_before.json)；[去重](research_state/archive_qa/02A_BSP_Multimedia_dedup_last_run.json) |
| [02B_RKNN2_Compiler_Runtime](02B_RKNN2_Compiler_Runtime.md) | 源图→校准→.rknn→张量；量化、输出布局与版本 | 2549 | 14 | 3 | [检查](research_state/archive_qa/02B_RKNN2_Compiler_Runtime_quality.json)；[证据](research_state/evidence/02B_RKNN2_Compiler_Runtime.json)；[基线](research_state/baselines/02B_RKNN2_Compiler_Runtime_before.json)；[去重](research_state/archive_qa/02B_RKNN2_Compiler_Runtime_dedup_last_run.json) |
| [02C_RKLLM](02C_RKLLM.md) | 视觉/音频embedding→语言会话；缓存、callback与分段计时 | 2419 | 12 | 1 | [检查](research_state/archive_qa/02C_RKLLM_quality.json)；[证据](research_state/evidence/02C_RKLLM.json)；[基线](research_state/baselines/02C_RKLLM_before.json)；[去重](research_state/archive_qa/02C_RKLLM_dedup_last_run.json) |
| [02D_RKNN3_RK182X](02D_RKNN3_RK182X.md) | 主机代理→协处理器；GRQ、多卡、分页、队列与语法 | 1985 | 8 | 1 | [检查](research_state/archive_qa/02D_RKNN3_RK182X_quality.json)；[证据](research_state/evidence/02D_RKNN3_RK182X.json)；[基线](research_state/baselines/02D_RKNN3_RK182X_before.json)；[去重](research_state/archive_qa/02D_RKNN3_RK182X_dedup_last_run.json) |
| [02E_ROS_Control_Operations](02E_ROS_Control_Operations.md) | ROS消息→实时域→EtherCAT；资源划分、OTA/签名 | 2024 | 15 | 0 | [检查](research_state/archive_qa/02E_ROS_Control_Operations_quality.json)；[证据](research_state/evidence/02E_ROS_Control_Operations.json)；[基线](research_state/baselines/02E_ROS_Control_Operations_before.json)；[去重](research_state/archive_qa/02E_ROS_Control_Operations_dedup_last_run.json) |

实际交接包括固件/DTS、dma-buf与布局、模型/词表/embedding、context/session、frame/time与动作单位；最终本体契约未取得。版本重点：RKNN2 2.5.0、RKLLM1.3.1、RKNN3手册1.2.0与Firefly1.1.0部署样例独立。完整BSP、模型commit/权重授权、并发热稳定/P99/WCET、动作成功率和量产维护仍需补齐。

[联合归档目录](REFERENCES.md)；[联合清单](research_state/manifests/Rockchip_02_Union.json)；[联合零网络去重记录](research_state/archive_qa/02_Union_dedup_last_run.json)。HTML静态依赖缺损逐原件记录，动态/视频不保证完整。
