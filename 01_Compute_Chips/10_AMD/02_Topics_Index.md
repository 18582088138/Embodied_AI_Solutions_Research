# AMD 02 软件栈专题索引与审阅入口

研究截止：2026-11-04。五篇补深专题已完成，等待用户审阅。研究方法参考 NVIDIA 08 的总览/专题组织：从原理和数据流追到 API、配置或源码，说明优化为什么成立，再核对官方测量、对标对象、版本/许可和失效条件。原 01、原 02 与 README 保留。

## 1. 按 02A—02E 阅读

| 独立文件 | 核心机制与实现细节 | 阅读时关注的边界 |
|---|---|---|
| [GPU执行、图编译与模型部署](02A_GPU_Execution_and_Deployment.md) | HIP线程/warp与release scope；Graph模板/实例/捕获及graph-safe库；SOMA跨stream；attention与TunableOp；MIGraphX shape/target/.mxr与拷贝；vLLM KV与prefill/decode。 | 四类“图”消除的开销不同；GPU可见性选择不是隔离；Instinct/Radeon/端侧SKU兼容分别核验。 |
| [Ryzen AI NPU编译、量化与异构推理](02B_RyzenAI_Compilation_and_Quantization.md) | XINT8/A8W8/A16W8/BF16的数值边界；校准reader与SmoothQuant；AutoSearch反馈/停止条件；CPU/NPU分区；context/cache失效；Analyzer时钟和许可。 | 支持算子不等全部留在NPU；通用Quark文档不替代平台包；1.9/1.8和参数命名冲突保留。 |
| [Versal编译器、张量布局与VART runtime](02C_Versal_Compiler_and_Runtime.md) | VAIML passes与CPU-partition产物；AIE chaining/L2/DDR；DP/TP与batch；HCWNC4/8地址/stride；scale贯穿编译和前后处理；异步job、DMA内存与custom op双注册。 | 同名VAI EP不等Ryzen ABI；ORT/VART产物不自由交换；HW布局、DMA可达性和job生命周期同时成立才可能少拷贝。 |
| [EDF/BSP、SHEL与多执行域](02D_EDF_BSP_and_Execution_Domains.md) | XSA→SDT→Lopper→MACHINE/DTS；domain合并规则；carveout/vring/payload；Yocto多配置固件依赖；remoteproc/RPMsg装卸；segmented/DFX；源版本和更新维护责任。 | 评估镜像不保证custom board；共享内存/RTOS不自动形成缓存一致或WCET；OSPI A/B不等完整产品OTA服务。 |
| [ROS加速、追踪与端到端系统集成](02E_ROS_Acceleration_and_System_Integration.md) | ament/colcon/firmware三pillar；HLS展开与入口带宽；四种感知graph及官方测量；host/kernel源码帧关联与背压；tracing扰动；RT分层；VART→ROS契约和Buffer迁移对标。 | stream只绕开特定中间payload；ROS触发和主机拷贝仍在；历史时延表不能当控制频率或完整硬实时证明。 |

## 2. 五篇怎样连接成软件链

下面是依据专题整理的分析映射，不能把所有软件合成一个跨芯片通用SDK。硬件目标与部署路线先选定，再决定编译器、runtime和系统接口；模型源、编译产物、运行对象、传感器/动作语义是不同交接层。

| 链路层次 | 对应专题 | 交接时必须保留的对象 |
|---|---|---|
| GPU训练/推理部署 | [GPU执行、图编译与模型部署](02A_GPU_Execution_and_Deployment.md) | 框架/ROCm/HIP/库与GPU版本，shape、设备target、Graph依赖、KV/workspace及诊断记录 |
| Ryzen端侧NPU | [Ryzen AI NPU编译、量化与异构推理](02B_RyzenAI_Compilation_and_Quantization.md) | ONNX/校准评估集、量化配置、EP分区、模型context、绑定driver和cache失效规则 |
| Versal端侧AIE | [Versal编译器、张量布局与VART runtime](02C_Versal_Compiler_and_Runtime.md) | 编译JSON/overlay、.rai或目录、CPU/HW tensor metadata、量化参数、buffer/job与custom op |
| Adaptive SoC系统构建 | [EDF/BSP、SHEL与多执行域](02D_EDF_BSP_and_Execution_Domains.md) | XSA/SDT/domain YAML、DTS/machine、recipe/commit、boot/PL/ELF/rootfs与装载状态 |
| ROS感知与业务接口 | [ROS加速、追踪与端到端系统集成](02E_ROS_Acceleration_and_System_Integration.md) | frame/epoch、时间基准、标定/布局、producer-consumer同步、期限、过期/排空和降级契约 |

软件执行模型与本体控制接口之间仍需具体集成证据。运动、仿真/学习、数据编排和运维的既有平台范围见原 02 总览；本轮没有把第三方理论可运行路线改写为 AMD 自有、量产或本体已验证的交付能力。新 Robotics Software Suite 尚未取得唯一 release，不用旧 KRS 填补该对象。

[原 02 软件栈总览](02_Software_Stack.md) · [已审阅的 01 硬件平台](01_Hardware_Platform.md)

## 3. 本轮值得优先审阅的技术结论

1. [GPU执行、图编译与模型部署](02A_GPU_Execution_and_Deployment.md)：Graph减提交开销、编译器优化张量图、attention减少中间物化、在线服务管理KV，各有不同对象和瓶颈。不能把某一优化开关推广成整模型固定收益。
2. [Ryzen AI NPU编译、量化与异构推理](02B_RyzenAI_Compilation_and_Quantization.md)：量化不仅降低位宽，还改变scale、图模式、边界转换及评估成本；编译cache跨EP/driver禁复用，版本升级必须有明确重建路径。
3. [Versal编译器、张量布局与VART runtime](02C_Versal_Compiler_and_Runtime.md)：官方布局图文件名与图内dtype存在差异，已按实际标签解释；wait返回JOB_PENDING时不能回收buffer，异步示例重复旧batch也不等20张新帧。
4. [EDF/BSP、SHEL与多执行域](02D_EDF_BSP_and_Execution_Domains.md)：固件、device tree与rootfs的一致性由构建依赖和实际装载共同确认。退出host测试不等停RPU；参考发行的长期维护责任仍需产品团队/OSV承担。
5. [ROS加速、追踪与端到端系统集成](02E_ROS_Acceleration_and_System_Integration.md)：KV260示例纯offload的Mean由91.48降至85.80ms，integrated为66.82ms；26.96%为时延降低。源码进一步显示raw触发、固定尺寸、阻塞读回与early-return风险，收益与正确性须同时验证。

上述数字只适用于对应文档的官方测试条件；各专题记录条件和缺项。NVIDIA对标用机制与迁移资产比较，没有相同模型、功耗、BSP与测量口径时不给平台性能排名。

## 4. 资料、图源与检查记录

[02 专题联合资料库（81份，逐份目录）](REFERENCES.md) · [联合资料清单](research_state/manifests/AMD_02_software_depth_all.json) · [逐份来源/归档状态](REFERENCES.md)

| 专题 | 正文汉字 | 来源条目 | 官方图 | 主张核验 | 检查记录 |
|---|---|---|---|---|---|
| 02A | 3362 | 19 | 4 | 28 | [结构/归档](research_state/archive_qa/02A_GPU_Execution_and_Deployment_quality.json) · [主张/图源](research_state/evidence/02A_GPU_Execution_and_Deployment.json) · [来源目录](research_state/depth_02/02A_GPU_Execution_and_Deployment_sources.json) |
| 02B | 2978 | 16 | 3 | 27 | [结构/归档](research_state/archive_qa/02B_RyzenAI_Compilation_and_Quantization_quality.json) · [主张/图源](research_state/evidence/02B_RyzenAI_Compilation_and_Quantization.json) · [来源目录](research_state/depth_02/02B_RyzenAI_Compilation_and_Quantization_sources.json) |
| 02C | 2822 | 21 | 5 | 36 | [结构/归档](research_state/archive_qa/02C_Versal_Compiler_and_Runtime_quality.json) · [主张/图源](research_state/evidence/02C_Versal_Compiler_and_Runtime.json) · [来源目录](research_state/depth_02/02C_Versal_Compiler_and_Runtime_sources.json) |
| 02D | 2424 | 14 | 3 | 30 | [结构/归档](research_state/archive_qa/02D_EDF_BSP_and_Execution_Domains_quality.json) · [主张/图源](research_state/evidence/02D_EDF_BSP_and_Execution_Domains.json) · [来源目录](research_state/depth_02/02D_EDF_BSP_and_Execution_Domains_sources.json) |
| 02E | 3791 | 15 | 3 | 48 | [结构/归档](research_state/archive_qa/02E_ROS_Acceleration_and_System_Integration_quality.json) · [主张/图源](research_state/evidence/02E_ROS_Acceleration_and_System_Integration.json) · [来源目录](research_state/depth_02/02E_ROS_Acceleration_and_System_Integration_sources.json) |

五篇合计15377有效正文汉字、18张正文表、18幅官方图和169项主张记录；跨篇引用计85条，按URL去重为81份。数字只描述材料规模，不替代研究深度或语义正确性。

每篇自动检查均通过，图已实际打开查看；主张记录保留原文短引、上下文、版本和成立条件。最后联合导出覆盖五篇全部引用，复用运行的网络请求为0，失败材料未进入有效清单。原 01、原 02、README 与五篇正文的基线哈希一致。

[联合复用证明](research_state/archive_qa/02_software_depth_all_dedup_last_run.json) · [联合索引/集合核对](research_state/archive_qa/02_software_depth_all_review.json)

归档有36份complete_static、45份partial_static；后者已取得有效正文，但仍有图片/样式/外链等依赖缺失。下载器冻结可执行script，未承诺动态交互或像素级完整；原响应、可读HTML/PDF、metadata、图源/衍生哈希均保留在唯一registry下。NVIDIA已有2026-11-03原响应用于对标，导入过程和日期在相应来源记录中区分。

## 5. 仍需产品资料或实机补齐的证据

关键缺口是新AMD Robotics Software Suite/X199的准确软件发行与逐SKU支持；Ryzen文档/包/driver的一致性；Versal容器内完整custom-op约束；KRS历史benchmark的commit、分辨率、样本/warmup、功率及P99；stream的完整连接、帧关联与异常恢复；跨CPU/GPU/NPU/DDR/network的热稳态并发、观测年龄和动作期限；安装二进制/firmware/模型权重/数据与本体SDK的具体许可和维护责任。下载失败与官方未披露分开记录。

本轮完成的是文献、API/源码、图和归档核验；未安装SDK、接受EULA、跑模型、刷板或测机器人闭环。五篇各提供可复建验证方案。状态保持02待审阅，03传感器接入尚未开始，继续顺序仍为03→09。
