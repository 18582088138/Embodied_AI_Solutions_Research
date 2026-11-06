# NVIDIA：核心技术护城河

NVIDIA在具身智能中的核心技术护城河，是端侧计算、优化工具、传感器入口、机器人工作流和工业安全工程的协同。单项技术并不全部独有：AMD也支持FP4和GPU Graphs，TI也有DSP/ISP和隔离MCU安全域，MuJoCo提供GPU仿真，ROS 2原生Buffer正在替代NITROS特定传输。更难替换的是客户围绕特定硬件积累的kernel、量化/校准数据、模型部署配置、相机驱动、标定、物理资产、回归与安全材料。[Datasheet Thor Full v1 5](https://developer.nvidia.com/downloads/assets/embedded/secure/jetson/thor/docs/jetson-thor-series-modules-datasheet_ds-11945-001.pdf) [AMD ROCm官方精度支持矩阵](https://rocm.docs.amd.com/en/latest/reference/precision-support.html) [AMD HIP官方Graphs](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_runtime_api/hipgraph.html) [Texas Instruments TDA4VM官方数据手册](https://www.ti.com/lit/ds/symlink/tda4vm.pdf) [Google DeepMind MuJoCo MJX官方文档](https://mujoco.readthedocs.io/en/stable/mjx.html) [Isaac ROS Buffer Migration](https://nvidia-isaac-ros.github.io/concepts/rosidl_buffer/nitros_migration.html)

本章改名为“核心技术护城河”，并拆为总览与三个详细专题。每项技术按原理/架构、优势、官方参数或性能条件、适用场景、限制及对标展开；不以峰值算力或开源品牌数代替机器人结果。资料采集于2026年11月3—4日，版本差异保留在正文及metadata，本轮未执行设备测试或认证。

## 1. 阅读入口与技术范围

| 文档 | 深入研究的技术点 | 主要比较对象 |
|---|---|---|
| [专题A：计算与部署](08A_Compute_and_Deployment.md) | NVFP4两级缩放与准确率、CUDA执行/计算强度/Graphs、TRT tactic/强类型/profile/plugin、Thor一致性/IPC/DLA边界 | AMD HIP/ROCm、Intel OpenVINO |
| [专题B：传感与隔离](08B_Sensing_and_Isolation.md) | PVA分块DMA/Context、SIPL/HSB协议、带宽/观测年龄、原生Buffer、MIG/MPS、Secure Boot/OP-TEE/加密/ratcheting | TI DSP/视觉引擎、ROS原生通信、AMD SR-IOV、通用TEE/存储加密 |
| [专题C：仿真、控制与安全](08C_Simulation_Control_and_Safety.md) | USD/RTX材质/多时钟、Sim官方KPI、Newton接触、cuRobo算法/原论文分位数/kernel表、数据链、OSMO、IGX安全响应 | MuJoCo/MJX、MoveIt/Tesseract、OpenPI/LeRobot、Argo、TI安全域 |

专题的对标不等于推荐一对一替换。AMD CDNA4的数据中心FP4与Thor端侧模组不是同功耗/形态；SR-IOV和MIG也不是同一资源抽象；生成式世界模型与物理接触求解器更不是同一种性能任务。比较应先固定问题层次，再核对目标硬件与条件。

## 2. 技术护城河地图：机制、收益与替换成本

| 技术 | 已验证机制 | 优势成立的场景 | 主要迁移资产 | 官方证据 |
|---|---|---|---|---|
| Blackwell Tensor Core/FP4 | 低精度矩阵执行、量化权重及混合精度 | 大模型和矩阵密集多模态 | 校准集、精度路径与kernel | [Datasheet Thor Full v1 5](https://developer.nvidia.com/downloads/assets/embedded/secure/jetson/thor/docs/jetson-thor-series-modules-datasheet_ds-11945-001.pdf) [TensorRT官方显式量化](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-explicit-quantization.html) |
| CUDA/Graphs | SIMT、stream/event、重复图提交 | 大量并行运算与短kernel流水线 | kernel、同步、Graphs与性能日志 | [CUDA编程模型与线程层级](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html) [CUDA Graphs官方文档](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html) |
| TensorRT | 目标设备构建、融合、engine/context | 需要稳定可复建的端侧推理 | 模型源、插件、构建和runtime版本 | [TensorRT构建、运行与对象生命周期](https://docs.nvidia.com/deeplearning/tensorrt/latest/architecture/how-trt-works.html) [TensorRT官方支持矩阵](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html) |
| SoC内存/驻留 | 共享DRAM及CUDA内存API | 大模型、缓存和相机buffer共存 | 分配/所有权/同步及带宽预算 | [CUDA内存模型文档](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/understanding-memory.html) [Datasheet Thor Full v1 5](https://developer.nvidia.com/downloads/assets/embedded/secure/jetson/thor/docs/jetson-thor-series-modules-datasheet_ds-11945-001.pdf) |
| PVA/VPI | 独立VLIW SIMD视觉引擎和库算法 | 规则视觉、前处理与GPU负载分离 | PVA程序、数据流和恢复策略 | [PVA SDK 2.10.1处理器与编程架构](https://docs.nvidia.com/pva/sdk/2.10.1/architecture.html) [VPI 4.1算法与平台说明](https://docs.nvidia.com/vpi/index.html) |
| SIPL/HSB | CoE或RoCE接收、驱动和metadata | 长线高分辨率、多传感器 | sensor driver、桥接和时间同步 | [Jetson SIPL Camera over Ethernet架构](https://docs.nvidia.com/jetson/archives/r39.2.1/DeveloperGuide/SD/CameraDevelopment/SIPLFramework/SIPL-for-L4T/CoE/CoE-Solution-Overview.html) [Holoscan Sensor Bridge 2.7架构与示例](https://docs.nvidia.com/holoscan/sensor-bridge/2-7-latest/applications/architecture) |

表中收益均有匹配条件：矩阵峰值不覆盖全部算子，Graphs不自动适应所有动态计算，TensorRT engine不是通用模型文件，PVA也不是大VLA的替代执行器。官方能力存在与客户任务获得收益之间，需要应用证据。具体参数、处理器结构和限制见对应专题。

| 技术 | 已验证机制 | 优势成立的场景 | 主要迁移资产 | 官方证据 |
|---|---|---|---|---|
| rosidl::Buffer/CUDA backend | 标准消息、GPU数组存储、VMM/IPC | 同host/GPU/user的兼容节点链路 | conversion、handle与fallback处理 | [Isaac ROS原生Buffer概念文档](https://nvidia-isaac-ros.github.io/concepts/rosidl_buffer/index.html) [Isaac ROS官方CUDA buffer backend](https://nvidia-isaac-ros.github.io/concepts/rosidl_buffer/cuda_buffer_backend.html) |
| MIG/MPS | 硬件profile分区/静态计算配额 | 多模型争用管理 | UUID/profile、资源预算与恢复 | [Jetson R39.2.1官方MIG配置指南](https://docs.nvidia.com/jetson/archives/r39.2.1/DeveloperGuide/SD/MiG.html) [Isaac ROS CUDA MPS静态GPU分区](https://nvidia-isaac-ros.github.io/concepts/gpu_partitioning/index.html) |
| Isaac Sim/Lab/Newton | 资产、渲染、物理、学习环境 | 大量可控测试与训练 | USD/动力学、奖励、随机化和验证集 | [Isaac官方仿真参考架构](https://docs.isaacsim.omniverse.nvidia.com/latest/introduction/reference_architecture.html) [Isaac官方Hydroelastic接触](https://docs.isaacsim.omniverse.nvidia.com/latest/physics/hydroelastic_contact.html) [GitHub IsaacLab README](https://raw.githubusercontent.com/isaac-sim/IsaacLab/main/README.md) |
| cuRobo | 并行seed、轨迹优化与滚动MPC | GPU规划、多候选重规划 | 机器人描述、碰撞场景与控制接口 | [cuRoboV2运动规划教程](https://nvlabs.github.io/curobo/latest/getting-started/motion_planning.html) [cuRoboV2 Reactive/MPC教程](https://nvlabs.github.io/curobo/latest/getting-started/reactive_control.html) |
| GR00T/Cosmos | 条件动作生成、视觉/世界模型和部署优化 | 数据/模型迭代及端侧VLA | 本体数据、权重、量化和回归 | [GR00T官方部署与基准](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/scripts/deployment/README.md) [Cosmos Page](https://developer.nvidia.com/cosmos) |
| OSMO | 多后端任务DAG和输入/输出依赖 | 跨训练、仿真及HIL的重复流程 | YAML、容器和backend运维 | [OSMO_README官方资料](https://raw.githubusercontent.com/NVIDIA/OSMO/main/README.md) |
| IGX/SEP与工业可靠性 | FSI/sMCU、错误传播、环境规格 | 工业、人机协作及安全材料要求 | 安全设计、证据包与维护合同 | [Product Brief IGX Thor Safety](https://developer.download.nvidia.com/assets/igx/robotics-product-brief-igx-thor-safety-4473375.pdf) [Jetson官方FAQ](https://developer.nvidia.com/embedded/faq) |

其中Buffer容器和backend架构是ROS 2原生机制，NITROS正在弃用，意味着部分通信绑定正在减少。Newton、Lab等开放代码也不是独占知识产权。MIG管理GPU资源，但不是整机安全证书；IGX安全基础与普通Jetson不能因同名Thor而合并。护城河评价必须区分客户工程沉淀、专有runtime/驱动、开放接口和社区共同维护资产。[Isaac ROS Buffer Migration](https://nvidia-isaac-ros.github.io/concepts/rosidl_buffer/nitros_migration.html) [Newton代码许可](https://raw.githubusercontent.com/newton-physics/newton/main/LICENSE.md) [Jetson Linux 39 2 1 License](https://developer.nvidia.com/downloads/embedded/L4T/r39_Release_v2.1/release/Tegra_Software_License_Agreement-Tegra-Linux.txt) [Product Brief IGX Thor Safety](https://developer.download.nvidia.com/assets/igx/robotics-product-brief-igx-thor-safety-4473375.pdf)

## 3. 性能证据能支持什么结论

Thor T5000标称FP4 sparse 2070TFLOPS，dense为1035TFLOPS；两者相差来自稀疏口径，不能当成两个模型实测。128GB和273GB/s是容量及带宽，系统、模型、cache、相机和workspace共享，不代表全部可用于权重。[Datasheet Thor Full v1 5](https://developer.nvidia.com/downloads/assets/embedded/secure/jetson/thor/docs/jetson-thor-series-modules-datasheet_ds-11945-001.pdf)

最接近VLA部署的公开例子是GR00T N1.7-LIBERO libero_10，Thor MAXN+jetson_clocks、batch1、两路256×256相机、四次去噪、horizon40、32DiT blocks。官方中位数完整TRT为76.8ms，联合优化加mixed NVFP4为35.6ms；计时含预处理与动作解码、排除RPC，三轮共60次计时。它支持“这套配置中联合软硬件优化有效”，不支持“FP4单项提升2.16倍”“机器人伺服28Hz”或“任务成功率提高”。[GR00T官方部署与基准](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/scripts/deployment/README.md)

HSB的1微秒同步描述是正确PTP配置下的时间戳对齐，MIG示例的12/6SM是profile，PVA的32像素SIMD是指令宽度。把这些不同单位的数值拼成一个“实时性指数”没有意义。每项技术的验收应选适合的对象：推理测median/P99与精度，传感测frame age/丢包/曝光同步，控制测任务和执行时序，安全按危险分析、诊断覆盖和安全响应证明。[HSB 2.7 metadata与延迟测量](https://docs.nvidia.com/holoscan/sensor-bridge/2-7-latest/applications/latency) [Jetson R39.2.1官方MIG配置指南](https://docs.nvidia.com/jetson/archives/r39.2.1/DeveloperGuide/SD/MiG.html) [PVA SDK 2.10.1处理器与编程架构](https://docs.nvidia.com/pva/sdk/2.10.1/architecture.html) [Product Brief IGX Thor Safety](https://developer.download.nvidia.com/assets/igx/robotics-product-brief-igx-thor-safety-4473375.pdf)

新增证据进一步限定了技术优势：NVFP4每16值共享FP8 scale并叠加张量级FP32，编码有scale开销；Thor full coherency不保证managed allocation当前自动启用GPU缓存；VPI基准剔除两端各5%后取median，不能作WCET。cuRobo2023原论文Orin60W mean0.22秒、98百分位1.34秒，当前V2和Thor仍需独立测量。Isaac Sim官方表中的L40多卡也没有使所有KPI单调增加。详细官方图、条件及表格分别保存在A、B、C专题。[NVIDIA NVFP4官方低精度推理文章](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/) [CUDA官方Tegra内存、一致性与跨引擎互操作应用说明](https://docs.nvidia.com/cuda/cuda-for-tegra-appnote/index.html) [VPI官方算法性能与测量说明](https://docs.nvidia.com/vpi/algo_performance.html) [cuRobo原始论文：并行碰撞无关运动生成](https://arxiv.org/pdf/2310.17274) [Isaac Sim官方性能基准与场景条件](https://docs.isaacsim.omniverse.nvidia.com/latest/reference_material/benchmarks.html)

## 4. 对标后的优势与短板

NVIDIA的可确认优势是Thor已有机器人模型部署原文，CUDA/TensorRT与传感器、仿真、规划、安全产品路径连接；客户能够复用更多围绕同一平台的示例与工具。对应短板是深度使用专用kernel、PVA、序列化engine、BSP和安全软件后，换硬件时需要重建和重新验证，迁移成本不会由保留ONNX文件全部解决。[GR00T官方部署与基准](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/scripts/deployment/README.md) [Jetson Linux 39 2 1 License](https://developer.nvidia.com/downloads/embedded/L4T/r39_Release_v2.1/release/Tegra_Software_License_Agreement-Tegra-Linux.txt)

对标材料显示单项能力已有替代：AMD HIP有SIMT/stream/Graphs，OpenVINO有设备编译和异构子图，TI有DSP/视觉加速和隔离MCU，MuJoCo/MJX有不同硬件的GPU仿真，MoveIt与Argo分别提供规划插件和Kubernetes工作流。不存在可靠共同条件的机器人性能/成本排名时，应比较接口、支持范围及复建工作，而不编造“全面领先”或“落后几年”。[AMD HIP官方编程模型](https://rocm.docs.amd.com/projects/HIP/en/latest/understand/programming_model.html) [AMD HIP官方Graphs](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_runtime_api/hipgraph.html) [Intel OpenVINO 2025官方异构执行](https://docs.openvino.ai/2025/openvino-workflow/running-inference/inference-devices-and-modes/hetero-execution.html) [Texas Instruments TDA4VM官方数据手册](https://www.ti.com/lit/ds/symlink/tda4vm.pdf) [Google DeepMind MuJoCo MJX官方文档](https://mujoco.readthedocs.io/en/stable/mjx.html) [MoveIt官方运动规划架构](https://moveit.picknik.ai/main/doc/concepts/motion_planning.html) [Argo Workflows官方架构](https://argo-workflows.readthedocs.io/en/latest/architecture/)

本轮没有取得逐技术专利清单、地域、有效期和侵权对比，不用猜测专利数量证明护城河。开源代码许可也不覆盖权重、数据、纹理、Kit及加速二进制。客户应保留业务状态、坐标系、数据schema、标定、原始模型、训练与校准集、验证日志；将平台特定实现作为可重建模块，而不只交付一个演示容器。[GR00T License](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/LICENSE) [Isaac Lab官方代码许可](https://raw.githubusercontent.com/isaac-sim/IsaacLab/main/LICENSE) [Isaac Sim官方代码及附加组件许可](https://raw.githubusercontent.com/isaac-sim/IsaacSim/main/LICENSE)

## 5. 独立参考归档及证据缺口

本章参考资料独立保存在[08专题资料索引](REFERENCES.md)。每份材料子目录包含HTML/原件、原始响应、metadata与已下载的样式、图片和字体。资料通过统一download_materials.py下载并共享项目URL registry，重叠材料用本地硬链接复用，不重新抓取。官方PDF渲染图保留原件和变换记录。

部分网页静态依赖受robots、失效资源或动态功能限制，见metadata；页面正文可核验不等于在线像素级或交互完全一致。ROS官网挑战页面不作正文证据，GitHub API补采被robots核验阻止时不填Stars/提交估值，HF未取得的权重卡不补造许可。来源和性能条件可复查，设备安装、实机、故障注入和安全认证未执行。


## 参考资料与本地原文

本报告依据11月3日采集的快照及11月4日逐方向补充取得的官方网页、代码仓库、API和文档。资料由统一下载工具归档到本项目的reference_metrial；多个方向共享同一URL的已校验文件。网页保留HTML和依赖，部分资源受robots规则、失效链接或动态交互限制影响时，按metadata如实标明。采集时点、版本和原始响应哈希可在各资料目录内核对。

08专题材料独立保存在reference_metrial/08_core；以下链接指向该专题目录中的原文。HTML及依赖通过本地硬链接共享存储，规范URL登记仍在项目公共registry。

| 官方资料 | 原始URL | 本地原文 | 归档情况 |
|---|---|---|---|
| NVIDIA_Datasheet_Thor_Full_v1_5 | [官方原文](https://developer.nvidia.com/downloads/assets/embedded/secure/jetson/thor/docs/jetson-thor-series-modules-datasheet_ds-11945-001.pdf) | [document.pdf](REFERENCES.md#ref-e0ae09b175a34eac) | 原件已归档 |
| NVIDIA_08_DEEP_ROCM_PRECISION | [官方原文](https://rocm.docs.amd.com/en/latest/reference/precision-support.html) | [index.html](REFERENCES.md#ref-a7f14d8cfd9297f5) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_08_DEEP_HIP_GRAPH | [官方原文](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_runtime_api/hipgraph.html) | [index.html](REFERENCES.md#ref-0077a3438456f5e6) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_08_DEEP_TI_TDA4 | [官方原文](https://www.ti.com/lit/ds/symlink/tda4vm.pdf) | [document.pdf](REFERENCES.md#ref-3e2afc59421db651) | 原件已归档 |
| NVIDIA_08_DEEP_MUJOCO_MJX | [官方原文](https://mujoco.readthedocs.io/en/stable/mjx.html) | [index.html](REFERENCES.md#ref-63a58dbcc0c84e67) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_Isaac_ROS_Buffer_Migration | [官方原文](https://nvidia-isaac-ros.github.io/concepts/rosidl_buffer/nitros_migration.html) | [index.html](REFERENCES.md#ref-a74b452c91c23559) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_08_DEEP_TRT_QUANT | [官方原文](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-explicit-quantization.html) | [index.html](REFERENCES.md#ref-f47c2746e3737567) | 静态HTML依赖完整；动态功能另验 |
| NVIDIA_02_CUDA_MODEL | [官方原文](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html) | [index.html](REFERENCES.md#ref-ff852ad994d3a602) | 静态HTML依赖完整；动态功能另验 |
| NVIDIA_02_CUDA_GRAPH | [官方原文](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html) | [index.html](REFERENCES.md#ref-64fc09301027cc35) | 静态HTML依赖完整；动态功能另验 |
| NVIDIA_02_TRT_WORK | [官方原文](https://docs.nvidia.com/deeplearning/tensorrt/latest/architecture/how-trt-works.html) | [index.html](REFERENCES.md#ref-9df325c2c44e3de5) | 静态HTML依赖完整；动态功能另验 |
| NVIDIA_TensorRT_Support_Matrix | [官方原文](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html) | [index.html](REFERENCES.md#ref-3b68f26af8646cbc) | 静态HTML依赖完整；动态功能另验 |
| NVIDIA_02_CUDA_MEMORY | [官方原文](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/understanding-memory.html) | [index.html](REFERENCES.md#ref-453cf4bfa7cf193e) | 静态HTML依赖完整；动态功能另验 |
| NVIDIA_02_PVA_ARCH2 | [官方原文](https://docs.nvidia.com/pva/sdk/2.10.1/architecture.html) | [index.html](REFERENCES.md#ref-782050b23c55b756) | 静态HTML依赖完整；动态功能另验 |
| NVIDIA_02_VPI_ROOT | [官方原文](https://docs.nvidia.com/vpi/index.html) | [index.html](REFERENCES.md#ref-eaae6e470379dc47) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_02_SIPL_COE | [官方原文](https://docs.nvidia.com/jetson/archives/r39.2.1/DeveloperGuide/SD/CameraDevelopment/SIPLFramework/SIPL-for-L4T/CoE/CoE-Solution-Overview.html) | [index.html](REFERENCES.md#ref-acc0a9a82b614a53) | 静态HTML依赖完整；动态功能另验 |
| NVIDIA_02_HSB_ARCH | [官方原文](https://docs.nvidia.com/holoscan/sensor-bridge/2-7-latest/applications/architecture) | [index.html](REFERENCES.md#ref-766974539088b048) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_02_BUFFER_DOC | [官方原文](https://nvidia-isaac-ros.github.io/concepts/rosidl_buffer/index.html) | [index.html](REFERENCES.md#ref-e9167f78686d3ef7) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_08_DEEP_BUFFER_CUDA | [官方原文](https://nvidia-isaac-ros.github.io/concepts/rosidl_buffer/cuda_buffer_backend.html) | [index.html](REFERENCES.md#ref-cc587411e9c9d2c8) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_08_MIG | [官方原文](https://docs.nvidia.com/jetson/archives/r39.2.1/DeveloperGuide/SD/MiG.html) | [index.html](REFERENCES.md#ref-85895374c012ed38) | 静态HTML依赖完整；动态功能另验 |
| NVIDIA_02_MPS_DOC | [官方原文](https://nvidia-isaac-ros.github.io/concepts/gpu_partitioning/index.html) | [index.html](REFERENCES.md#ref-1fd266641b8a8d14) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_05_SIM_ARCH | [官方原文](https://docs.isaacsim.omniverse.nvidia.com/latest/introduction/reference_architecture.html) | [index.html](REFERENCES.md#ref-f74626edcba85090) | 静态HTML依赖完整；动态功能另验 |
| NVIDIA_05_HYDRO | [官方原文](https://docs.isaacsim.omniverse.nvidia.com/latest/physics/hydroelastic_contact.html) | [index.html](REFERENCES.md#ref-ee558d6613a45451) | 静态HTML依赖完整；动态功能另验 |
| NVIDIA_GitHub_IsaacLab_README | [官方原文](https://raw.githubusercontent.com/isaac-sim/IsaacLab/main/README.md) | [content.md](REFERENCES.md#ref-5af037b6c4754936) | 原件已归档 |
| NVIDIA_06_MOTION | [官方原文](https://nvlabs.github.io/curobo/latest/getting-started/motion_planning.html) | [index.html](REFERENCES.md#ref-174f05f5e8477c6a) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_06_REACTIVE | [官方原文](https://nvlabs.github.io/curobo/latest/getting-started/reactive_control.html) | [index.html](REFERENCES.md#ref-3021d836689af1c1) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_GR00T_Deployment_Guide | [官方原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/scripts/deployment/README.md) | [content.md](REFERENCES.md#ref-af6435cdb176784f) | 原件已归档 |
| NVIDIA_Cosmos_Page | [官方原文](https://developer.nvidia.com/cosmos) | [index.html](REFERENCES.md#ref-558f642be571ac1f) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_08_OSMO_README | [官方原文](https://raw.githubusercontent.com/NVIDIA/OSMO/main/README.md) | [content.md](REFERENCES.md#ref-594757da33ea4f5a) | 原件已归档 |
| NVIDIA_Product_Brief_IGX_Thor_Safety | [官方原文](https://developer.download.nvidia.com/assets/igx/robotics-product-brief-igx-thor-safety-4473375.pdf) | [document.pdf](REFERENCES.md#ref-b71ae712d56c26cb) | 原件已归档 |
| NVIDIA_Developer_Page_Jetson_FAQ | [官方原文](https://developer.nvidia.com/embedded/faq) | [index.html](REFERENCES.md#ref-7c29d52f2f676227) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_05_NEWTON_LICENSE | [官方原文](https://raw.githubusercontent.com/newton-physics/newton/main/LICENSE.md) | [content.md](REFERENCES.md#ref-aac65d531df3ffee) | 原件已归档 |
| NVIDIA_Jetson_Linux_39_2_1_License | [官方原文](https://developer.nvidia.com/downloads/embedded/L4T/r39_Release_v2.1/release/Tegra_Software_License_Agreement-Tegra-Linux.txt) | [content.txt](REFERENCES.md#ref-5394e70b58c257fd) | 原件已归档 |
| NVIDIA_03_HSB_LATENCY | [官方原文](https://docs.nvidia.com/holoscan/sensor-bridge/2-7-latest/applications/latency) | [index.html](REFERENCES.md#ref-66135574a9b2eb3d) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_08_DEEP_NVIDIA_NVFP4_BLOG | [官方原文](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/) | [index.html](REFERENCES.md#ref-bdc20768416189cc) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_08_DEEP_CUDA_TEGRA | [官方原文](https://docs.nvidia.com/cuda/cuda-for-tegra-appnote/index.html) | [index.html](REFERENCES.md#ref-e1e2a9f4bcacf89e) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_08_DEEP_VPI_PERF | [官方原文](https://docs.nvidia.com/vpi/algo_performance.html) | [index.html](REFERENCES.md#ref-0ad58187dddda198) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_08_DEEP_CUROBO_PAPER | [官方原文](https://arxiv.org/pdf/2310.17274) | [document.pdf](REFERENCES.md#ref-d323f34db075b715) | 原件已归档 |
| NVIDIA_08_DEEP_SIM_BENCHMARKS | [官方原文](https://docs.isaacsim.omniverse.nvidia.com/latest/reference_material/benchmarks.html) | [index.html](REFERENCES.md#ref-b07ba7136a8df329) | 静态HTML依赖完整；动态功能另验 |
| NVIDIA_08_DEEP_HIP_MODEL | [官方原文](https://rocm.docs.amd.com/projects/HIP/en/latest/understand/programming_model.html) | [index.html](REFERENCES.md#ref-b375803d7ee408be) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_08_DEEP_OV_HETERO | [官方原文](https://docs.openvino.ai/2025/openvino-workflow/running-inference/inference-devices-and-modes/hetero-execution.html) | [index.html](REFERENCES.md#ref-c57744c4f30d3ed2) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_08_DEEP_MOVEIT_PLANNING | [官方原文](https://moveit.picknik.ai/main/doc/concepts/motion_planning.html) | [index.html](REFERENCES.md#ref-151b94198154c1f6) | 静态HTML依赖完整；动态功能另验 |
| NVIDIA_08_DEEP_ARGO_ARCH | [官方原文](https://argo-workflows.readthedocs.io/en/latest/architecture/) | [index.html](REFERENCES.md#ref-44e30ae8eb3205be) | 静态呈现依赖部分缺失；见metadata |
| NVIDIA_GR00T_License | [官方原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/LICENSE) | [content.txt](REFERENCES.md#ref-9d9946c66ea15cdb) | 原件已归档 |
| NVIDIA_GitHub_IsaacLab_License | [官方原文](https://raw.githubusercontent.com/isaac-sim/IsaacLab/main/LICENSE) | [content.txt](REFERENCES.md#ref-8d3916d73175f044) | 原件已归档 |
| NVIDIA_GitHub_IsaacSim_License | [官方原文](https://raw.githubusercontent.com/isaac-sim/IsaacSim/main/LICENSE) | [content.txt](REFERENCES.md#ref-1c21a8f4920bb953) | 原件已归档 |

以上技术事实与官方测量保持条件和版本边界。本调研未执行设备安装、模型训练、机器人实机测试或客户验收；文中的集成路线和选型门槛属于分析建议。公开资料未披露的交期、报价、最坏情况时延与认证结果不作推断。
