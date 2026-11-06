# 02A 昇腾 CANN、ATC 与 AscendCL 运行时

本专题回答机载推理如何从训练图变成设备任务，以及为什么能编译、能加载和能持续闭环是三层不同验收。数据截止 2026-11-05。事实依据固定提交的华为 Ascend/samples 原码及 Ultralytics 实现；旧样例只说明其版本接口，不构成 Atlas 200I A2 的完整适配或实时性能证明。

## 1. 编译与执行分工

{{ACL_ResNet_README}} 将开发环境与带昇腾处理器的运行环境分开。其 ATC 示例把 Caffe 网络、权重转换为 OM，设置框架、目标 SoC、输入格式和输入/输出类型。开发程序可链接 stub 库完成构建，运行时必须加载真实 runtime 及其依赖；x86 编译成功并不意味着 ARM 程序可运行。跨架构时还需 AArch64 软件包、交叉编译器及目标 ABI。OM 编译目标与应用 ELF 的 CPU 架构是两项分别管理的条件。

ATC 的价值是把框架描述转换成目标设备可执行模型；它不能自动证明全部算子、动态维度、精度或前后处理语义均保持。旧样例 `--framework=0` 表示 Caffe，`--soc_version=Ascend310` 不可照抄给 310B。当 ONNX 用于当前端侧链路时，{{Ultralytics_Ascend_Exporter}} 实际传入 `--framework=5`、`--input_format=NCHW`、`--input_shape=images:batch,channels,height,width`、用户指定的 `--soc_version` 和 `--precision_mode=force_fp16`。该函数本身固化静态 shape；不是任意 ONNX 图的动态推理工具，也没有在这里实现 INT8 标定。

| 层次 | 实际产物或对象 | 要解决的问题 | 不能据此认定 |
|---|---|---|---|
| 原始图 | 网络、权重、输入名称/shape | 算子和数值语义 | 任意目标 SoC 可编译 |
| ATC 编译 | 目标 SoC 的 OM | 图转换、目标执行产物 | 可跨芯片后缀复用 |
| 应用构建 | CPU ELF、头文件和库依赖 | ABI、链接和路径 | stub 链接等于驱动可用 |
| 模型加载 | modelId、描述符、工作区/权重区 | 分配资源、解释 I/O | 剩余内存足够多模型并发 |
| 执行和后处理 | dataset、device buffer、分类结果 | 数据搬运、推理及解释输出 | 真实相机端到端时延 |

模型编译、固件、驱动、runtime 和算子包应固定成一个可重现组合，升级其中任一项后重新验证加载、算子覆盖和数值误差。这个工程判断来自多个层次相互依赖，并非厂商承诺所有版本都存在相同兼容规则。当前 CANN 门户浏览器能见动态内容，但本次归档主体为导航；公告候选也只归档了正文占位，均不作为有效版本证据，本文不据此宣称已核验最新 CANN 发布包。

## 2. 一个模型的完整对象生命周期

{{ACL_SampleProcess}} 的初始化顺序为 `aclInit`→`aclrtSetDevice`→`aclrtCreateContext`→`aclrtCreateStream`→`aclrtGetRunMode`。Context 与 Stream 是运行时对象；创建 Stream 不会把后面的同步 `aclmdlExecute` 自动改成异步。示例通过 run mode 判断程序处于 Host 还是 Device 分支，影响输出是否需要设备到主机复制。不能把这些语义简化为“所有 A2 应用必经 PCIe”；模块内运行的真实共享/拷贝路径仍需目标 SDK 和载板条件。

{{ACL_ModelProcess}} 先 `aclmdlQuerySize` 获取模型工作区和权重区大小，分别 `aclrtMalloc`，再 `aclmdlLoadFromFileWithMem`。随后创建描述符并 `aclmdlGetDesc`，从描述符读取 I/O 大小，创建 dataset 并加入 data buffer。此例只有一个输入，`CreateInput` 明确检查输入 buffer 字节数与模型描述符相等；字节数相等仍不能保证 RGB/BGR、归一化和通道布局正确。机器人 RGB、深度、关节状态多输入策略必须逐输入查验类型、顺序、单位及时间戳，不可复用这个单图分类契约。

数据包装器与真实存储必须区分：此例输入内存由 SampleProcess 分配，ModelProcess 的 `DestroyInput` 销毁包装器和 dataset，外层再释放输入存储；输出内存则由 ModelProcess 分配并在 `DestroyOutput` 释放。把包装器销毁当内存释放会泄漏；让调用方和模型对象都释放同一地址会造成错误。正文解释的是本例所有权，不给所有 AscendCL 封装一律相同的所有权结论。

执行使用 `aclmdlExecute`。Host 分支通过 `aclrtMallocHost` 和 `aclrtMemcpy(...DEVICE_TO_HOST)` 获取结果；分类后处理把输出解读成 float 并取 top5，依赖编译命令的 FP32 输出。换成检测头、FP16 或多输出模型时不能保持这段强制转换。正常清理包括销毁 dataset/buffer、卸载模型、释放工作区/权重区，以及 stream/context/device/ACL 的释放。生产封装还需统一处理部分初始化失败、异常中断和资源释放顺序；仓库示例不等于已经验证全部故障分支。

{{FIG:ACL_FirstApp_Figure}}

图为华为样例仓的 firstapp 官方原图，透明底已铺白色以保留黑色文字。可见输入犬图→ResNet50 模型→top5 分类输出；它支持“输入、模型和后处理相分离”的阅读，不能证明相机采集、ROS 接口、吞吐或任何 A2 性能。图中置信度仅是单样例输出，不是数据集精度。

## 3. 异步、队列与动态输入

{{ACL_Async_ModelProcess}} 在 `ExecuteAsync` 中向指定 Stream 提交 `aclmdlExecuteAsync`，输入输出从内存池领取；按回调间隔维护 dataset 映射，`aclrtLaunchCallback` 执行输出处理后归还内存池，另有 `aclrtSynchronizeStream`。它揭示关键条件：提交返回时输出未必完成，buffer 必须存活到消费结束。多 stream 的生产者/消费者也不能仅靠 CPU 提交顺序保证可见性，需要目标版本支持的同步机制；本文未取得版本化事件 API 手册，因此不虚构跨流事件调用细节。

该旧示例不是完整实时任务调度器。生产系统应分析最大在途任务数、输入/输出池容量、回调耗时、残余批次及异常回收，并验证所有提交路径是否释放。摄像机持续产生新帧时，盲目加深队列可提高表面吞吐，却使动作依据过期观测。对交互操作可采用有界队列并丢弃旧观测；录像或完整数据集回放则可能需要保留全部帧。两者策略不同，应记录实际丢帧及观测年龄，不能把同步等待时间排除后只报告 NPU 核时间。

{{ACL_Dynamic_README}} 的动态 dims 用例要求 CANN≥5.0.4，声明在 Atlas200DK/Atlas300 测试；ATC 目标为 Ascend310，预置 batch/空间维度组合。README 的功能说明和实际命令布局应结合读：命令使用 `ND`、`Placeholder:-1,-1,-1,3` 并列出具体 dims 档位，不能只按文字描述推断任意 NCHW 动态支持。该机制是指定可执行档位，并非不受约束地把任何分辨率交给模型。当前 A2 每一种动态模式、档位数量、内存分配和算子限制仍须对目标版本核验。

| 场景 | 影响机制（分析） | 验证动作 | 边界 |
|---|---|---|---|
| 固定 RGB 检测 | 静态 shape 简化内存及数据契约 | 固定 batch、resize 和 padding | 不推导大模型可部署 |
| 多相机异步推理 | 队列积压改变观测时效 | 记录帧号、提交/完成/动作时刻 | 吞吐不等于及时性 |
| 多模态策略 | I/O 和算子覆盖更复杂 |逐 tensor 检查名称、类型和模态对齐 | 单图示例不能证明支持 |
| 动态输入 | 编译档位影响执行和容量 | 每档位数值/峰值内存/切换测试 | 旧 310 档位不代表 310B |

## 4. 技术对标、许可与放行条件

从机制看，ATC/OM 与 NVIDIA TensorRT 的目标编译部署解决相近痛点：降低框架到设备执行的适配成本；但本轮没有归档并测试同一模型的双方版本，不列性能排名或参数等价映射。迁移时要重新处理算子、精度、布局、动态输入和前后处理；把后端换掉而保留测试样本及契约比直接替换文件扩展名可靠。AscendCL 的显式生命周期能让 C++ 应用控制资源，但代价是开发者承担内存和同步正确性。Python InferSession 可减少封装代码；{{Ultralytics_Ascend_Backend}} 实际仍把 tensor 转为 `im.cpu().numpy()` 再调用 infer，不能称为从相机 DMA 到 NPU 的已证实零拷贝。

{{Ascend_Samples_License}} 为 Apache 2.0，适用于仓库代码的相应条款；动态示例 README 另写“学习参考，非商业目的”，应保留这项使用说明并在商业集成前澄清，而不自行扩展或撤销 LICENSE 权利。CANN 工具、runtime、驱动、固件、下载权重和图片不因代码开源就自动具有同许可。本文未取得目标 CANN 二进制完整许可及发行包，对再分发和量产维护不做已核验判断。

放行应以完整 SKU、板号、系统、固件/驱动/CANN/算子包、应用和 OM 哈希为起点，运行目标模型的固定输入一致性、每一输入档位、长时间资源稳定、取消/重启和并发相机测试。测量须分别报告预处理、搬运、NPU、后处理与动作发布，记录 batch、shape、精度、warmup、样本、温度和功率，以及平均/P99等统计。P99 也不能当 WCET。本轮只做文献与源码核验，没有实机数据；峰值 TOPS 和分类成功日志不能替代上述放行证据。
