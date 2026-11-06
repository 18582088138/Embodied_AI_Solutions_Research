# 02 软件栈专题索引

数据截止：2026-11-05（Asia/Shanghai）。01已审阅；02总览与五专题研究完成，待用户审阅。03—09仍为此前首轮简报，本次未修改或启动。

[02软件栈总览](02_Software_Stack.md)

| 专题 | 研究对象与核心机制 | 交接关系及版本/证据缺口 |
|---|---|---|
| [NeuWare/BANG与运行时](02A_NeuWare_BANG_and_Runtime.md) | descriptor/stride、tile与workspace、异步queue | 补算子→模型runtime；当前x86/SDK要求不能套220 |
| [MagicMind编译与量化](02B_MagicMind_Compilation_and_Quantization.md) | Parser→Builder/Calibrator→Model/Context | 模型→序列化产物；220参数/实际候选分叉，转换工具缺口 |
| [PyTorch与分布式训练](02C_PyTorch_Backend_and_Distributed_Training.md) | PrivateUse1、CPU回退、CNCL事件与allocator保护 | 训练checkpoint→可支持的导出；torch2.1路线不混vLLM2.9 |
| [视觉流水线与机器人交接](02D_CNStream_EasyDK_and_Robot_Handoff.md) | frame/buffer、队列背压、Request/Discard、profile | 视觉结果→自定义消息；旧220与新CE3226分开，BSP/ROS/动作未知 |
| [vLLM与云端运维](02E_vLLM_and_Cloud_Operations.md) | 插件/hijack、KV页/scale、K8s分配与硬件指标 | 文本→业务；开发快照、有效配置、CLI冲突与SLA缺口 |

## 独立证据与检查

每篇≥1500有效汉字；官方图已逐图打开，02E未取得专用架构图，明确采用代码/配置证据。单篇检查与去重记录对应其完成时点；总览合法更新后，最终专题复查不使用旧baseline，原始baseline保留并另做全章哈希审计。结构检查不等实机或语义自动证明。

| 文件 | 主张/图源记录 | 起始基线 | 最终结构检查 | 零网络去重记录 |
|---|---|---|---|---|
| [02_Software_Stack](02_Software_Stack.md) | [evidence](research_state/evidence/02_Software_Stack.json) | [baseline](research_state/baselines/02_Software_Stack_before.json) | [quality](research_state/archive_qa/02_Software_Stack_quality.json) | [last_run](research_state/archive_qa/02_Software_Stack_dedup_last_run.json) |
| [02A_NeuWare_BANG_and_Runtime](02A_NeuWare_BANG_and_Runtime.md) | [evidence](research_state/evidence/02A_NeuWare_BANG_and_Runtime.json) | [baseline](research_state/baselines/02A_NeuWare_BANG_and_Runtime_before.json) | [quality](research_state/archive_qa/02A_NeuWare_BANG_and_Runtime_quality.json) | [last_run](research_state/archive_qa/02A_NeuWare_BANG_and_Runtime_dedup_last_run.json) |
| [02B_MagicMind_Compilation_and_Quantization](02B_MagicMind_Compilation_and_Quantization.md) | [evidence](research_state/evidence/02B_MagicMind_Compilation_and_Quantization.json) | [baseline](research_state/baselines/02B_MagicMind_Compilation_and_Quantization_before.json) | [quality](research_state/archive_qa/02B_MagicMind_Compilation_and_Quantization_quality.json) | [last_run](research_state/archive_qa/02B_MagicMind_Compilation_and_Quantization_dedup_last_run.json) |
| [02C_PyTorch_Backend_and_Distributed_Training](02C_PyTorch_Backend_and_Distributed_Training.md) | [evidence](research_state/evidence/02C_PyTorch_Backend_and_Distributed_Training.json) | [baseline](research_state/baselines/02C_PyTorch_Backend_and_Distributed_Training_before.json) | [quality](research_state/archive_qa/02C_PyTorch_Backend_and_Distributed_Training_quality.json) | [last_run](research_state/archive_qa/02C_PyTorch_Backend_and_Distributed_Training_dedup_last_run.json) |
| [02D_CNStream_EasyDK_and_Robot_Handoff](02D_CNStream_EasyDK_and_Robot_Handoff.md) | [evidence](research_state/evidence/02D_CNStream_EasyDK_and_Robot_Handoff.json) | [baseline](research_state/baselines/02D_CNStream_EasyDK_and_Robot_Handoff_before.json) | [quality](research_state/archive_qa/02D_CNStream_EasyDK_and_Robot_Handoff_quality.json) | [last_run](research_state/archive_qa/02D_CNStream_EasyDK_and_Robot_Handoff_dedup_last_run.json) |
| [02E_vLLM_and_Cloud_Operations](02E_vLLM_and_Cloud_Operations.md) | [evidence](research_state/evidence/02E_vLLM_and_Cloud_Operations.json) | [baseline](research_state/baselines/02E_vLLM_and_Cloud_Operations_before.json) | [quality](research_state/archive_qa/02E_vLLM_and_Cloud_Operations_quality.json) | [last_run](research_state/archive_qa/02E_vLLM_and_Cloud_Operations_dedup_last_run.json) |

## 原件、集合与复建入口

[六篇引用联合清单](research_state/manifests/Cambricon_02_Software_Stack.json)；[02专题联合集合](REFERENCES.md)；[项目唯一资料registry](REFERENCES.md)。各正文参考表列原URL与本地原件，集合复用canonical归档，未使用refresh。

[全章完成审计](research_state/archive_qa/02_chapter_audit.json)；[联合集合去重记录](research_state/archive_qa/02_union_dedup_last_run.json)；[研究续接状态](research_state/progress.json)。

已归档官方HTML、PDF、源码/配置及可取得依赖；PDF抽取文本和完整页图存derived，原件不改写。partial_static页面有缺依赖，失败API页面未作为正文证据。单文件complete_static不代表include、子模块、镜像、权重、SDK和数据全部取得。

后续验收需先取得精确SKU的SDK/BSP与许可，再冻结模型、目标产物、布局/scale、库ABI与消息/动作契约；分别测试数值、动态输入、并发、观测年龄、云端请求和更新回滚。本轮没有设备、模型或机器人运行结果。

本次停在02审阅，待用户明确继续03。
