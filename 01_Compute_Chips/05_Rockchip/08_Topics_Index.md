# 08 核心技术专题索引

截至2026-11-05。总览与三篇独立专题逐篇完成文献/API/源码静态核验、官方图复核、报告检查和零网络去重；未进行板端或机器人实机测试。

| 报告 | 研究对象 | 有效汉字 | 原件 | 图 | 检查与归档 |
| --- | --- | --- | --- | --- | --- |
| [08_Core_Technology_Moat](08_Core_Technology_Moat.md) | 跨机制价值、证据层次和条件选型 | 2108 | 16 | 1 | [检查](research_state/archive_qa/08_Core_Technology_Moat_quality.json)；[证据](research_state/evidence/08_Core_Technology_Moat.json)；[基线](research_state/baselines/08_Core_Technology_Moat_before.json)；[去重](research_state/archive_qa/08_Core_Technology_Moat_dedup_last_run.json) |
| [08A_Quantization_Compiler](08A_Quantization_Compiler.md) | 数值格式、GRQ block误差、混合映射、CPU插件、精度 | 2014 | 10 | 1 | [检查](research_state/archive_qa/08A_Quantization_Compiler_quality.json)；[证据](research_state/evidence/08A_Quantization_Compiler.json)；[基线](research_state/baselines/08A_Quantization_Compiler_before.json)；[去重](research_state/archive_qa/08A_Quantization_Compiler_dedup_last_run.json) |
| [08B_Memory_Coprocessor_Multicard](08B_Memory_Coprocessor_Multicard.md) | DRAM、tensor同步、KV页、分段/队列与链路分析 | 2257 | 10 | 1 | [检查](research_state/archive_qa/08B_Memory_Coprocessor_Multicard_quality.json)；[证据](research_state/evidence/08B_Memory_Coprocessor_Multicard.json)；[基线](research_state/baselines/08B_Memory_Coprocessor_Multicard_before.json)；[去重](research_state/archive_qa/08B_Memory_Coprocessor_Multicard_dedup_last_run.json) |
| [08C_Perception_RealTime_Trust](08C_Perception_RealTime_Trust.md) | ISP/IQ、时间、RT锁/AMP、EtherCAT、模型/启动保护 | 2256 | 16 | 1 | [检查](research_state/archive_qa/08C_Perception_RealTime_Trust_quality.json)；[证据](research_state/evidence/08C_Perception_RealTime_Trust.json)；[基线](research_state/baselines/08C_Perception_RealTime_Trust_before.json)；[去重](research_state/archive_qa/08C_Perception_RealTime_Trust_dedup_last_run.json) |

[08联合资料目录](REFERENCES.md)；[联合引用清单](research_state/manifests/Rockchip_08_Union.json)；[联合去重记录](research_state/archive_qa/08_Union_dedup_last_run.json)。

关键版本为RKNN3 V1.2.0；RKNN2、RKLLM与板商BSP独立，不能统一称为同一版本。尚未取得物理DRAM带宽、完整kernel/tactic/格式、VLA同条件精度与闭环数据、功能安全和长期维护合同。旧08_Proprietary_Technologies.md只保留历史占位，当前研究入口为08_Core_Technology_Moat.md。
