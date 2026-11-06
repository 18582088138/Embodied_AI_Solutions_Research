# 02 Intel 具身智能软件栈总览

截止 2026-11-05。本章沿系统驱动、异构推理、策略运行、感知导航、实时执行与数据训练六条路径展开，专题各自提供源码/API、官方图、本地原件与检查记录。Intel 的平台价值是把 x86 主机、CPU/iGPU/NPU、ROS 和工业控制接口组织成可集成的组件集合。公开材料仍有版本漂移、未闭环的模型转换语义和量产运维缺口，不能将组件可下载等同整机已验收。

本章为文献和源码调研，未安装 SDK、转换模型、训练策略或测试机器人。01 已审阅内容及 03—09 文件保持不变；本章完成后等待审阅，不开始 03。专题索引提供全部正文与证据入口。

## 软件能力和供应责任地图

![Intel官方Suite六层架构]( [[FIG:Intel02_Architecture]] )

原图将应用、参考机器人、AI/ROS组件、系统基础与 Intel 硬件分层；蓝色为 Intel 提供/优化，绿色为上游开源，灰色是用户本体、传感器和数据。它能说明接口协作，不能证明全部组合在任意芯片、功率和板卡上同时验收。准确版本和供应责任以安装指南、组件发行及本体资料为准。[[Intel02_Architecture]]

| 层次 | 主要软件 | Intel角色 | 交付/交接对象 | 边界 |
|---|---|---|---|---|
| 系统 | Suite安装、Image Composer、GPU/NPU驱动 | 配置组织、驱动/计算runtime | ISO/raw、内核、固件、包清单 | 板卡BSP与量产镜像仍需锁版 |
| 推理 | OpenVINO、NNCF、oneAPI | 图转换、目标执行与空间计算优化 | IR/XML/BIN、tensor、cache、queue | 设备/shape/量化路径分别验证 |
| 策略运行 | PhysicalAI、RTC样例 | 动作队列与模型接口 | manifest、stats、chunk、runtime YAML | stop与硬件保护不同 |
| 感知导航 | OpenVINO节点、PCL/FLANN、SLAM、ITS | 算法/节点提供或优化 | Image/PointCloud2、TF、map、Path | DDS/Nav2、本体驱动来自上游/集成方 |
| 操作控制 | RVC、RTmotion、Robotmctask、IgH优化 | 状态机/PLCopen/实时任务集成 | waypoint、JointTrajectory、ENI/PDO | 每本体、NIC、周期单独验收 |
| 数据与运维 | Studio、Profiler、KVM | 示教/训练导出、观测与部署指导 | dataset、checkpoint、bundle、session log | 多租户、OTA事务、认证证据不足 |

ROS 2、Nav2、MoveIt 2、Gazebo、MuJoCo、Lightning 和 LeRobot 是上游技术；Intel 的包装、适配或优化不使它们成为独占平台。相机、本体、末端执行器与数据属于用户和伙伴责任。RVC 的 VLA controller/ADBSCAN 标 roadmap，不能当已交付功能；Studio library 的模型类存在与 UI 支持范围、每设备优化验证又是三件不同的事。[[Intel02E_RVC]] [[Intel02F_Lib]] [[Intel02F_Deployment]]

## 可复建版本矩阵必须按路线分开

| 路线 | 归档依据/版本 | 绑定对象 | 当前不能混用 |
|---|---|---|---|
| Suite手动安装 | Ubuntu24.04/Jazzy；OpenVINO2025.3.0、oneAPI2026.1.* | 四个OpenVINO/ROS包pin | 通用OpenVINO2026新增API |
| 旧π0.5导出 | OpenVINO2025.4、NNCF2.19、ONNX1.20 | 修改过的噪声/时间、未锁LeRobot | 当前推理入口与历史forward |
| Robotmctask | OpenVINO2026.1.0、Ruckig0.9.2 | ENI、task、stand.onnx | Suite基础2025.3包组 |
| Studio与Runtime | 独立动态源码快照 | Python依赖、manifest、runtime配置 | 所有main视作一个稳定release |
| 仿真 | 总览Harmonic/Jazzy；Pick教程Classic/Humble已测试 | ros_gz、插件、clock、namespace | Jazzy安装标签当Harmonic验收 |

Suite 固定原件对象为 1b0b22a2964f，Studio 为 b38bff4a9e6d，edge-control 为 e5dcdcc705a9；表中是已归档代码对象，非统一发布日期或整套发行编号。OpenVINO、驱动、PhysicalAI、LeRobot 动态资料分别冻结于参考表的采集时间。将 CPU PCI ID、OS/kernel、BIOS、GPU/NPU driver/compiler/firmware、ROS/RMW、模型 revision、编译属性和最终产物 hash 放入同一复建记录，才可解释“昨天可运行、今天编译失败”。[[Intel02A_Install]] [[Intel02C_Pi05_Export]] [[Intel02E_Gateway]] [[Intel02F_StudioReadme]] [[Intel02E_PickSim]]

Core Ultra Series 2/3 的 Suite 配置列 AMR、固定臂、人形，Core Series 3 只列前两者；不能以 CPU 家族名自动复制人形参考配置。GPU计算经 OpenCL/Level Zero loader、NEO 和 i915/xe DRM；NPU 经 plugin、loader、用户态驱动/compiler、intel_vpu、firmware。设备节点存在或驱动支持某芯片仅回答底层就绪，不回答模型算子、闭环延迟和固件/BKC 一致。[[Intel02A_Configurations]] [[Intel02A_NPU_Overview]]

## 从源模型到传感器和动作的两条链

视觉检测路线：模型/标签→转换 IR→显式设备编译→图像预处理→OpenVINO inference request→检测消息→costmap 或 grasp。launch 默认 GPU，并将 engine、输入/标签路径写入 YAML；CPU/GPU/NPU 参数说明候选目标，不证明 DMA 可达性和端到端零拷贝。PCL/FLANN 以 SYCL queue、同 context 的点云与驻留查询缓冲降低重复分配/搬运，仍需检查 ROS 序列化、图像/点云布局和每阶段同步。[[Intel02D_Launch]] [[Intel02D_PCL]] [[Intel02D_FLANN]]

策略路线：environment/示教 episode→LeRobot v3→数据统计/训练 checkpoint→选真实 policy 推理入口→export 和可选权重压缩→完整 manifest/model/tokenizer/stats 包→目标设备执行→ActionQueue→本体关节映射/反归一化→控制器。Studio 提供这条资产交接，Runtime 接收 bundle 与部署 YAML，两者用途不同。最需要审查的旧 π0.5 wrapper 调用 forward 并把 actions 作为输入，而当前 LeRobot forward 是训练损失路径；历史 revision 未锁，故本文既不把它写成已验证动作图，也不武断断言历史输出都相同。独立 RTC patch 替换 sample_actions 不能自动修复旧转换教程。[[Intel02F_Recording]] [[Intel02F_ExportCode]] [[Intel02C_ExportCode]] [[Intel02C_LeRobot_PI05_Source]] [[Intel02C_RTC_Patch]]

NNCF compress_weights 与 activation 校准量化不同；INT8权重不等于 W8A8。export hook 修改 XML/BIN 后必须重新保存 hash 和动作误差对照。AUTO 默认不纳入 NPU，并可通过 CPU startup/runtime fallback 改变执行设备；精度测试应先显式选择目标设备，再测试回退与并发。HETERO 通过 affinity/query_model 划子图、中间 tensor 交接，分区开销可能使局部加速失效。当前 NPU Compiler-In-Plugin 和 bounded dynamic shape 支持有2026版本、硬件及驱动条件，不能倒套 Suite2025.3。[[Intel02B_Weight]] [[Intel02B_AUTO]] [[Intel02B_HETERO]] [[Intel02B_NPU]]

IR 是模型表达，编译 cache 是目标依赖产物，不能替代源模型或跨driver/设备通用文件。CPU共享RAM、USM、remote tensor 也不能自动保证全部buffer共享：NPU远程CPU内存要求指针/size四KB对齐，存活至请求及tensor销毁；GPU context、layout、同步和queue同样是前提。生命周期错误可表现为偶发帧错、结果污染或热负载下失败，光看平均推理毫秒无法发现。[[Intel02B_RemoteNPU]] [[Intel02B_RemoteGPU]] [[Intel02B_Cache]]

## 闭环时序、停止与可观测性

ROS传感器 QoS、executor 和软件同步决定观测什么时候被消费。ImageSync 的十毫秒配对门槛不证明曝光硬同步；单侧缺失的队列边界需要审查。FastMapping 的毫米/米深度单位、CameraInfo/TF 决定地图意义；ITS 的持久路网需要失效管理，文档不支持连续重规划。Path 成功、控制器可执行、真实任务完成必须分别测。[[Intel02D_ImageSync]] [[Intel02D_FastMap]] [[Intel02D_ITS]]

Runtime policy调用、chunk消费、插值命令、EtherCAT周期和电机servo是不同速率。RTC通过前缀约束延续队列，不能使后台线程变成硬实时。RobotRuntime stop 在tick之间生效，当前tick仍可能发动作；Studio无control保持最后action，导出还省略grace move。RVC的0.002秒publish与0.1秒timeout、一毫秒RTmotion循环都是配置/样例，不是整机频率或急停认证。应建立独立期限、旧观测拒绝和下游保护。[[Intel02C_Runtime_Loop]] [[Intel02C_Runtime_Modes]] [[Intel02F_Sessions]] [[Intel02E_RVC]] [[Intel02E_Motion]]

Profiler 记录消息、资源、GPU和session配置，有助于发现CPU/GPU/控制干扰；处理延迟关联与图表阈值不能代替因果trace或WCET。仿真必须分别记sim clock和wall clock。Pick仿真绕过视觉从Gazebo取得物体位置，SnapFlow性能报告又在H100 Torch上测量，都不能当Intel真实抓取效果。实时调优、cache隔离、IRQ与VFIO是减少干扰的机制，需要准确芯片与拓扑条件；ISO/raw和KVM生命周期并没有提供完整OTA双槽/事务回退证据。[[Intel02E_Profiler]] [[Intel02E_PickSim]] [[Intel02F_Benchmark]] [[Intel02E_RT]] [[Intel02A_ImageComposer]] [[Intel02E_KVM]]

## 条件选型与交付缺口

分析：已有x86/ROS、PLCopen与ENI资产的团队，可先复用标准数据和动作接口，再选Intel优化节点；重迁CUDA空间计算、其他runtime或本体SDK时，需重做kernel/buffer、预后处理、graph/cache与控制接口验证。没有同条件测量时，本章只比较机制和迁移资产，不给性能排名。公开代码可审查，优势成立在版本锁定、数据契约和观测闭环完整的条件下；多个main分支、旧教程与新组件混装会使这一优势失效。

目前实质缺口包括旧π0.5导出动作语义、NPU/模型逐SKU编译和并发尾延迟、部分内部APT示例的公开可获取性、历史仿真到当前版本的验收、Studio共享store样本一致性、真实本体失败/介入率及OTA恢复事务。代码Apache/MIT不自动覆盖模型Gemma条款、示教/训练数据、固件、第三方库和本体SDK。可复建放行顺序是锁版/SBOM→原模型与导出数值对齐→目标设备冷/热启动→传感器时间/布局→动作单位与坐标→队列/超时/停止注入→仿真留出→本体热稳态任务→更新恢复。当前报告提供这套验证依据和缺口，未替代现场测试与供应商正式交付责任。[[Intel02C_Pi05_ModelCard]] [[Intel02D_PCL]] [[Intel02F_Store]] [[Intel02F_Update]]
