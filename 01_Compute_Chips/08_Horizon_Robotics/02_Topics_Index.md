# 02 软件栈专题索引

数据截止：2026-11-05。第02章为总览＋五篇独立专题，按02A→02E完成；检查通过是结构/归档与人工文献核验完成，不是SDK安装或机器人实机验收。当前等待用户审阅，第03章未启动。

[软件栈总览](02_Software_Stack.md) · [联合资料集合](REFERENCES.md)

## 阅读与交接关系

|专题|研究对象|核心机制|交接契约|主要证据缺口|
|---|---|---|---|---|
|[02A_BSP_and_Lifecycle](02A_BSP_and_Lifecycle.md)|Ubuntu/BSP、启动、热与OTA|rootfs/deb、配置优先级、AVB、分区恢复|软件镜像/分区、固件和版本集|商业源码包；miniboot回滚文档冲突|
|[02B_BPU_Compiler_and_Runtime](02B_BPU_Compiler_and_Runtime.md)|OE/BPU与LLM/VLA|march、校准、stride、任务/缓存、组件编译|HBM、tensor、tokenizer、norm_stats|型号和测量条件；真实动作链未闭合|
|[02C_HUCP_and_Multimedia](02C_HUCP_and_Multimedia.md)|媒体/hbmem/GPU/VDSP|帧布局、queue/pool、所有权、rpmsg启停|frame、内存引用、完成/释放事件|Sunrise混代API；组合零复制/P99未测|
|[02D_MCU_and_Industrial_Communication](02D_MCU_and_Industrial_Communication.md)|MCU/FreeRTOS与工业通信|固件启停、IPC配置、CAN、SOEM状态机|ELF/BIN、IPC包、PDO、时钟与期限|企业静态库；EtherCAT周期日志冲突；WCET未测|
|[02E_TogetheROS_and_Robot_Pipeline](02E_TogetheROS_and_Robot_Pipeline.md)|TROS与应用集成|loaned message/QoS、异步乱序、模型封装|Header、感知/动作消息、frame与本体映射|Jazzy5.1.0绑定与BSP5.1.1差异；S600完整链未测|

建议先读总览版本矩阵，再按专题核对。02A交付镜像/包与恢复边界；02B交付目标模型及数值/张量契约；02C将帧和内存交给推理；02D接收具有单位、期限和状态的控制请求；02E把设备能力封装到ROS消息和应用。它们是工程交接关系，不表示五篇中的独立sample已经形成一台验证过的机器人。

## 逐篇核查入口

|文件|正文有效汉字|来源数|官方图数|检查|最终复用|
|---|---|---|---|---|---|
|02A_BSP_and_Lifecycle|2288|11|2|[检查JSON](research_state/qa/02A_BSP_and_Lifecycle_check.json)|[零网络记录](research_state/qa/02A_BSP_and_Lifecycle_last_run.json)|
|02B_BPU_Compiler_and_Runtime|2768|22|2|[检查JSON](research_state/qa/02B_BPU_Compiler_and_Runtime_check.json)|[零网络记录](research_state/qa/02B_BPU_Compiler_and_Runtime_last_run.json)|
|02C_HUCP_and_Multimedia|2389|12|2|[检查JSON](research_state/qa/02C_HUCP_and_Multimedia_check.json)|[零网络记录](research_state/qa/02C_HUCP_and_Multimedia_last_run.json)|
|02D_MCU_and_Industrial_Communication|2246|10|2|[检查JSON](research_state/qa/02D_MCU_and_Industrial_Communication_check.json)|[零网络记录](research_state/qa/02D_MCU_and_Industrial_Communication_last_run.json)|
|02E_TogetheROS_and_Robot_Pipeline|2542|18|2|[检查JSON](research_state/qa/02E_TogetheROS_and_Robot_Pipeline_check.json)|[零网络记录](research_state/qa/02E_TogetheROS_and_Robot_Pipeline_last_run.json)|

来源数为每篇使用数，会跨专题复用，不能相加当作独立资料数量。官方图共10张独立衍生图，总览复用其中2张，全部实际打开核验；旧S100图只用于对应机制，不能推导S600规格或性能。

## 证据、基线与归档

- 02_Software_Stack：[证据](research_state/evidence/02_Software_Stack.json) · [开始基线](research_state/baselines/02_Software_Stack_before.json)
- 02A_BSP_and_Lifecycle：[证据](research_state/evidence/02A_BSP_and_Lifecycle.json) · [开始基线](research_state/baselines/02A_BSP_and_Lifecycle_before.json)
- 02B_BPU_Compiler_and_Runtime：[证据](research_state/evidence/02B_BPU_Compiler_and_Runtime.json) · [开始基线](research_state/baselines/02B_BPU_Compiler_and_Runtime_before.json)
- 02C_HUCP_and_Multimedia：[证据](research_state/evidence/02C_HUCP_and_Multimedia.json) · [开始基线](research_state/baselines/02C_HUCP_and_Multimedia_before.json)
- 02D_MCU_and_Industrial_Communication：[证据](research_state/evidence/02D_MCU_and_Industrial_Communication.json) · [开始基线](research_state/baselines/02D_MCU_and_Industrial_Communication_before.json)
- 02E_TogetheROS_and_Robot_Pipeline：[证据](research_state/evidence/02E_TogetheROS_and_Robot_Pipeline.json) · [开始基线](research_state/baselines/02E_TogetheROS_and_Robot_Pipeline_before.json)

[总览检查](research_state/qa/02_Software_Stack_check.json) · [联合清单](research_state/manifests/Horizon_02_union.json) · [联合最终去重](research_state/qa/02_union_last_run.json) · [当前状态](research_state/progress.json)

动态OE/LLM入口是JS空壳，正文通过归档官方JS在全网络阻断浏览器中离线渲染，保存原件/路由/渲染HTML/提取文本及哈希；空壳本身不作语义来源。联合集合同时保留入口/脚本/静态图片等呈现依赖。GitHub仓库呈现资源有1项缺失，公开内容与固定commit资料已取得，不保证动态交互或像素级复现。ROS上游挑战页、空内容ReID实例未列入有效证据。

## 本章结论的使用范围

可据此规划BSP、模型、媒体、ROS和控制域开发及供应商交付清单。未取得完整商业SDK/许可依赖审计、目标板并发与热稳定实测、控制WCET和安全手册、VLA到本体的状态/动作契约。官方单次VLA耗时不证明控制/伺服频率或真实任务成功率；仿真与图片回灌不证明真实接触和泛化。
