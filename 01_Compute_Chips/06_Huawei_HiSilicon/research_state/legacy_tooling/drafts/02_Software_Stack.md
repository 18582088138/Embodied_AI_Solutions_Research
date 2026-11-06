# 02 华为/海思具身智能软件栈总览

数据截止2026-11-05；本章已经完成五个独立深度专题及资料核验。核心判断是：昇腾模块的CANN/框架部署链、海思视觉SoC的BSP/MPP/SVP链、机器人控制和运维，以及CloudRobo云开发是不同交付层。公开原件能支持具体模型部署入口、旧机器人示例与云模型/动作接口，却不足以证明所有当前SKU已有统一机器人全栈、任意VLA或实时控制认证。选型必须按完整SKU、发行包、模型和本体契约验证。

## 1. 阅读路线与软件边界

五篇逐篇完成：{{REPORT:02A_Ascend_CANN_Runtime}} 研究ATC/OM、AscendCL对象生命周期、buffer/异步/动态档位；{{REPORT:02B_Framework_Model_Deployment}} 研究TorchNPU、MindSpore Lite、YOLO导出/runtime及vLLM支持排除；{{REPORT:02C_HiSilicon_BSP_MPP_NPU}} 研究板级包、视频流水线、NNIE量化/分段、多执行域和二进制许可；{{REPORT:02D_Robot_Integration_Operations}} 研究真实示例收发、坐标/时间/动作契约、控制分层与运维；{{REPORT:02E_CloudRobo_Development_Platform}}补齐本轮后续章节发现的云资源/权限、模型注册、R2C配置生效、ROS2队列和回退机制。它们分别保留主张记录、基线、质量检查和零网络去重运行；总览用于选择路径，具体API和限制以专题原文为准。

| 软件域 | 公开证据与作用 | 对应硬件边界 | 本轮成熟度 | 未解决项 |
|---|---|---|---|---|
| CANN/ATC/AscendCL | 目标编译OM、资源和推理执行 | Ascend目标后缀；旧310示例另标 | 官方代码与第三方当前链路 | A2准确包/驱动/固件矩阵 |
| TorchNPU | PyTorch算子/设备/图/分布式适配 | 兼容表含310B等系列 | 官方项目固定提交 | 每模型算子及图功能实测 |
| MindSpore Lite | Converter、Context、Model、predict | Ascend provider与CPU backup | 官方API固定提交 | A2发行包/动态模式矩阵 |
| YOLO Ascend后端 | ONNX→ATC→OM+metadata→InferSession | 文档列310B1/B4目标 | 第三方项目维护的明确路径 | 输入链及准确率/性能复现 |
| vLLM-Ascend | 服务器LLM服务、图/KV管理 | A2/A3服务器及实验310P | 项目FAQ具体支持表 | 明确不支持200I A2/310B |
| 海思BSP/MPP/SVP | 镜像/驱动、媒体、专用AI | 每SoC和板号分开 | 官方旧教材+上游/社区实现 | 当前型号完整SDK和商业权限 |
| 机器人控制 | 本体SDK、消息/坐标、运动执行 | 旧200DK+PC+指定本体 | 教学示例和集成分析 | 当前本体交付/安全/运维验证 |
| CloudRobo/R2C | 工作空间、OBS/SWR、CCE/ModelArts及观测/动作映射 | 云训练/部署与本体端侧分开 | 官方开发/真机接口实践 | SDK/资产许可、准确资源及闭环性能 |

## 2. 两条端侧数据链与一个服务器分支

昇腾检测路线可追到 {{Ultralytics_Ascend_Doc}}、{{Ultralytics_Ascend_Exporter}} 和 {{Ultralytics_Ascend_Backend}}：YOLO产生ONNX，ATC编译静态NCHW、FP16、具体SoC的OM，目录保存metadata，InferSession执行，输入经过CPU NumPy。默认imgsz640、batch1、opset17和quantize16是该后端快照设置，不能当所有CANN统一上限。第三方文档把310B4/310B1映射到8T/20T开发平台，但没有替代01缺失的准确料号和内存SKU证据。

{{ACL_ModelProcess}}、{{ACL_SampleProcess}}、{{ACL_Async_ModelProcess}} 则提供更底层的资源解释：工作区/权重区、modelId/描述符、dataset和buffer、context/stream、同步执行与异步回调各有生命周期。包装器不等于真实内存，提交不等于输出完成；本体控制必须在数据完成且时间有效时消费结果。{{ACL_Dynamic_README}} 的CANN≥5.0.4/Atlas200DK/Atlas300档位用例是旧310参考，不当当前A2动态输入验收。

海思视觉路线依据 {{HiSilicon_DV300_SDK_PDF}} 和 {{HiSilicon_DV300_Media_PDF}}：板级SDK启动和加载驱动，Sensor→VI/ISP→VPSS→推理或编码/网络分支，SYS/VB/MMZ负责相应资源。{{HiSilicon_DV300_SVP_PDF}} 的旧NNIE通过Caffe/RuyiStudio量化WK，支持分段由CPU补缺失层；WK与昇腾OM不同。{{HiView_3403_VPSS}} 揭示当前社区3403的stride、格式、物理映射、VGS/IVE转换和帧释放，但算法库及目标商业包未完整取得，不能称全系列官方NPU SDK已验证。

硬件引擎也不能只看总TOPS：{{HiSilicon_Hi3519AV200}} 的HNR5.6T保留不开放，通用AI预算应按开放2.5T；{{HiSilicon_Hi3403V100}} 双引擎精度不同，仍需目标调度/算子证据；{{HiSilicon_Hi3516CV610}} 的128MB与产品轻量VLM宣称不能推导通用大VLA。Linux/OpenHarmony/LiteOS支持方向还需要具体发行包，{{OH_DV300_README}} 的DV300约束不能替代CV610端口证明。

服务器分支依据 {{VLLM_Ascend_FAQ}}：支持“Atlas A2”主要指910B服务器/训练系列，200I A2（310B）明确未支持且未计划。图捕获尺寸、KV cache、preemption及TTFT/TPOT调优能帮助服务器服务容量设计，不能作为机载模块模型性能或控制频率。远程规划增加观测上传、网络、排队和下游约束链，必须另测端到端时间。

CloudRobo是新增云开发分支。官方产品架构连接工作空间资产与OBS存储、SWR镜像、CCE数据/评测、ModelArts训练及R2C本体接口，平台本身无数据存储。SO101/PI05链已有LeRobot v0.5.1、双图/六关节、训练资产和在线服务步骤；自定义镜像ASCEND_SNT9B不是310B端侧支持证据。r2c.json在服务详情、新部署、模型OBS目录和训练终态的读取范围不同，修改OBS后重启现存服务不会更新映射。云模型输出chunk，经ROS2适配器映射回本体，动作执行频率和云policy/控制器/伺服分别验收。{{CloudRobo_ProductPDF}} {{CloudRobo_R2C_Protocol}} {{CloudRobo_MetaEngineAdapter}}

{{FIG:CloudRobo_ProductPDF}}

官方架构图支持云开发对象交接，不证明所有步骤由同一加速器运行，也不证明端侧A2已搭载在示例机器人。IAM/委托、资产血缘和资源配额可减少协作混乱，但模型权重、镜像digest、映射、端侧YAML及标定仍应成组冻结。费用有开发平台、仿真、模型和独立资源项，预算/供应/监管详见{{REPORT:09_SWOT_Analysis}}，不能用体验额度或教学示例价格当项目成本。{{CloudRobo_BillingPDF}}

## 3. 版本、工具与开发调优

{{TorchNPU_Compatibility}} 推荐安装包2.14/PyTorch2.14/CANN9.2.X，并列26.2.0与CANN9.2.0配套；{{Ascend_Pytorch_README}} 的2.12+CANN9.1.0只是安装例。{{TorchNPU_Version}} 构建列表含2.13—2.16，{{TorchNPU_Support}} 的2.15/2.16为未来计划。源树、安装包、产品版本、维护状态和未来规划必须分开，不能用“最新”概括。固定提交仓库可核验这些表，但本轮没有下载目标CANN实际发行包，门户/公告归档空壳未纳入证据。

MindStudio在旧示例中提供IDE入口，TorchNPU README列profiling、日志和通信WatchDog；海思旧教材列proc/debug dump、HiBurn和RuyiStudio。它们能定位模型、媒体或系统问题，不能仅凭工具名宣称端到端机器人可观测性齐备。调优须同时记录CPU前后处理、NPU、搬运、video/ISP、队列和控制反馈；编译日志、模型加载与独立算子profiling分别验证，不能只报告设备执行核时间。

| 验收对象 | 应固定/记录的内容 | 触发重新验证的变化 | 不能替代的证据 |
|---|---|---|---|
| 平台包 | SKU/板号、OS/BSP、驱动/固件/runtime | 升级、换载板/容量 | 合同支持和电气规范 |
| 模型图 | 网络/权重/编译参数/目标/metadata哈希 | shape、精度、算子、标签改变 | 目标准确率及任务成功 |
| 输入链 | 原始格式、stride、标定、frame/time | sensor/ISP/padding改变 | 相机真值/时序测量 |
| 并发运行 | 内存、队列、编码/网络/日志负载 | 新任务和后台负载 | 持续温度/功率和尾时延 |
| 动作端 | 单位、关节顺序、有效期、反馈 | 本体/控制模式改变 | 可执行性与失效响应 |

## 4. 许可、成熟度和选择条件

{{Ascend_Samples_License}} 为Apache2，但教学README非商业说明保留；{{Ascend_Pytorch_License}} 为多贡献者BSD式代码许可，{{TorchNPU_Docs_License}} 为CC BY4.0；{{MindSpore_License}}、{{VLLM_Ascend_License}} 为Apache2，{{Ultralytics_License}} 为AGPL3。代码、权重、数据、文档、CANN/算子包、固件和本体SDK分别核验，开源框架不自动授权全部二进制和量产模型。{{OH_Media_EULA}} 的旧DV300媒体库仅授权开发板内部开发/测试，未授予制造/销售/分发含该软件产品；目标商业授权仍需单独取得，不外推所有当前合同。

{{Ascend_Robot_Arm_README}}、{{Ascend_Robot_Chess_README}} 和 {{Ascend_Robot_Car_README}} 证明特定旧200DK机器人示例存在；没有证明当前A2统一ROS2、本体安全或量产运营。{{Ascend_Robot_Arm_Code}} 的每5帧触发是计数，不是5Hz，反投影代码也与README总公式不同。{{HiSilicon_AcademyPDF}} 说明获取CV610/BSP/MPP课程和HiSupport/FAE途径，不能据课程目录声称接口手册已取得。

对固定视觉节点，可优先评估海思硬件图像流水线和轻量推理，成立条件是合法目标SDK、sensor驱动和并发验证；对A2轻量检测，可优先验证当前第三方静态OM路径；对服务器大模型服务，按vLLM具体硬件列表选择；对多模态机器人策略，先确定注意力/状态缓存/动作头和本体契约，再测框架路径；云开发可评估CloudRobo独立资源、模型与本体接口，仍需取得SDK/资产许可及真实任务验收。没有同模型同输入同功率测试，本文不输出与NVIDIA的倍数、成本或开发效率排名。03的真实传感器/同步研究和06的具体本体研究与这些路线衔接。

## 5. 归档与质量边界

本章引用联合集合覆盖总览及02A—02E；每篇正文满足有效汉字底线，表格最多5列，官方图逐张打开，PNG/SVG/PDF保留原件及衍生哈希。HTML保存原始响应和识别到的依赖；CloudRobo网页部分静态依赖缺失，按partial_static披露，静态归档不证明动态登录/交互完整。CANN当前门户、公告正文占位和海思资料列表动态目录已排除有效证据，原始registry状态未改写，访问限制不能推断厂商没有资料。

本章核验是公开文献、源码、许可和归档结构，未运行NPU、模型、容器或机器人。剩余缺口包括当前A2准确安装组合、新海思SDK/API与商业授权、传递依赖和模型许可、目标模型/传感器性能、实时和安全控制、量产支持。质量检查通过不等于事实自动正确或实机达标；这些边界在逐篇claim_review和manual_review中保存。
