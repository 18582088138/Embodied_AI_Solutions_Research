# 07 生态、伙伴与交付责任

截至2026-11-05，Huawei/HiSilicon生态可分成昇腾训练部署、海思视觉/BSP、华为云具身开发、本体/传感器和渠道交付几层。伙伴和开源代码的价值是缩短适配距离，不能据其标签推导目标SKU量产认证、供货或已商业运营。关键是明确谁维护编译器、谁交付BSP、谁修正动作接口、谁承担本地保修与版本回退。

## 代表参与者和实际分工

|参与者|提供内容|实际交接对象|本次确认程度|
|---|---|---|---|
|华为Ascend/PyTorch|torch_npu适配与版本矩阵|PyTorch/CANN/driver/firmware|固定提交文档，需目标设备复建|
|MindSpore|框架与Lite模型接口|MindIR、target/provider、CPU备援|源码接口，不保证任意模型|
|Ultralytics|第三方Ascend导出/后端|ONNX→ATC→OM、metadata|AGPL软件路径，需模型许可|
|华为云CloudRobo|资产、训练、仿真、部署、R2C|OBS/SWR、CCE/ModelArts、本体配置|官方功能与实践，公测/专属池条件|
|RLinf作者社区|具身/agent RL基础设施|模型、环境、rollout/actor调度|作者Ascend矩阵与教程，非海思端侧|
|HIVIEW/Openhisilicon|核心板/底板、BSP/MPP/AI/ISP集成|buffer、视频、Web/流媒体/升级|第三方自述与源码，合同待取|
|OpenHarmony社区|HiSilicon HDI、驱动、板级工程|SoC目录、board/vendor与SDK|DV300等明确对象，许可分层|
|LeRobot/本体厂商|数据/策略/标定、机器人执行|joint/camera/action/本体SDK|具体SO101/UR5e/Q25实践|

昇腾与海思不是同一推理runtime家族；将torch_npu模型移到海思NPU仍需转换、算子和数据接口适配。CloudRobo在线模型也不自动生成端侧OM/WK。上述分工由原文和实现支撑。{{Ascend_Pytorch_README}} {{TorchNPU_Compatibility}} {{MindSpore_Lite_README}} {{Ultralytics_Ascend_Doc}} {{CloudRobo_ProductPDF}}

## 开源框架生态与版本责任

TorchNPU的README安装例与COMPATIBILITY推荐矩阵可能不是同一发布组合，必须按正式包、PyTorch、CANN和维护表锁定，构建支持与计划支持分开。MindSpore Lite存在CPU backup机制，但fallback可改变时延与功耗；让模型能启动只是起点。Ultralytics把310B1/310B4对应20/8TOPS A2的内容属于第三方集成线索，不能替代采购SKU确认。其源码AGPL-3.0还需与商业分发方式一起审核，不能因芯片SDK闭源就忽略应用代码义务。{{TorchNPU_Compatibility}} {{MindSpore_Lite_README}} {{Ultralytics_Ascend_Doc}} {{Ultralytics_License}}

RLinf作者README在采集快照列OpenVLA-OFT、GR00T N1.5、OpenPI、StarVLA与DreamZero的Ascend CANN支持，其他新模型更新不等于矩阵每一行都有Ascend验证。OpenPI教程把LIBERO/ManiSkill跨后端和MetaWorld/CALVIN总体示例分开；StarVLA具体路径固定上游starVLA-v1.6、aarch64源码构建decord、匹配torch_npu并跳过CUDA flash-attention，LIBERO使用OSMesa CPU渲染。训练NPU兼容不等于物理与渲染在NPU执行。{{RLinf_README}} {{RLinf_OpenPI_Guide}} {{RLinf_StarVLA_Guide}}

Wan世界模型教程还有更具体依赖：MindIE-SD需另装并匹配CANN/PyTorch，导入attention/rotary相关算子，失败时警告并保留原diffsynth实现。当前路线用世界模型直接生成观测，Ascend配置关闭仿真器评估，需要另行验证策略数值行为。作者的一般结果表不能直接标为Ascend性能。RLinf代码许可Apache-2.0，模型/世界模型、VAE、奖励网络、初始化数据和仿真资产仍各有许可；README main是采集快照，未固定revision，不作为生产版本锁。{{RLinf_Wan_Guide}} {{RLinf_License}}

这项后续发现补充04/05的证据地图：世界模型已有第三方Ascend训练路线；仍没有取得200I A2/海思端侧交付，也没有证明CloudRobo使用同一RLinf实现。CloudRobo残差数据格式与RLinf一致仅支持数据接口联系，不能据此称双方全部版本、模型和算子统一认证。{{CloudRobo_ResidualDebug}}

## 海思集成商与板级生态

HIVIEW作者明确提供Hardware customization、System building、AI algorithm与ISP tuning服务，核心板+底板可定制；README列CV610、DV500、3403板图和BSP/MPP、编码、RTSP/WebRTC、ONVIF、UVC、SVP功能。对于视频传感器前端，这能减少协议和界面工程；对于机器人还需添加ROS时间戳、动作协议和故障降级。功能清单是作者自述，不能称海思官方认证或跨型号相同能力。{{HiView_README}}

{{FIG:HiView_ArchitectureImage}}

图显示BSP注册/事件、CODEC配置、RTSPS SDP/RTP、WEBS控制/WS和Upgrade交互，支持模块职责说明，不提供网络安全或视频时延实测。升级箭头不证明有签名、双分区、断电恢复、反回滚或密钥管理。3403 VPSS源码展示frame/stride/MMZ/释放路径，集成仍须查BSP、sensor驱动、ISP参数、交叉编译器和每个依赖许可。本轮固定提交目录没有全仓统一LICENSE，局部依赖许可不能授予整个方案的商用权。{{HiView_3403_VPSS}}

OpenHarmony官方仓库区分Hi3516DV300 Taurus、Hi3518EV300 Aries、Hi3861 Pegasus等SoC/board关系；不能由DV300端口推导CV610 OpenHarmony4.1具体BSP已开源。驱动GPLv2和媒体EULA义务也不同，已取得2021媒体包限制开发板内部开发/测试，不授予制造售卖分发；新商业SDK要取得新合同，不能将旧许可扩大为当前所有产品统一禁商用。{{OH_HiSilicon_README}} {{OH_Driver_License}} {{OH_Media_EULA}}

## 渠道、培训与本地支持

|官方列示渠道|相关授权类别|区域/选型含义|
|---|---|---|
|淇诺/华强、思尼克|包含智慧视觉等多类|中国大陆/香港；逐SKU询价|
|深圳科通|智慧视觉、媒体、感知、模拟|不能按类别保证所有芯片现货|
|力源/鼎芯/帕太|包含智慧视觉等|确认法人、销售与FAE责任|
|云汉芯城|线上多类；线下范围另列|线上/线下授权范围不同|

以上是海思官网当前渠道正文，不记录或联络个人联系人，不提交采购表单。类别授权不是工业板卡认证、MOQ、单价或交期。供应商应提供准确料号、批次、授权链、可追溯发票、替代料/PCN及样品到量产支持方式。{{HiSilicon_BuyChannels}}

海思学堂2024宣传PDF列1.0已有50+课程，覆盖CV610硬件/BSP/MPP/SVP_NPU、DV500调优及MCU入门；2.0用户认证、3.0自助问答是规划。HiSupport注册用户访问，不能把课程列表当本次已取得SDK手册或所有培训免费公开。官网开发中心本次抓取只有JavaScript提示，排除为有效正文；应向FAE索取目标SKU正式资料与培训版本。{{HiSilicon_AcademyPDF}}

## 从原型到量产的交付约束

原型阶段应固定计算板、相机、模型及本体的最小可工作组合；量产阶段还需sensor/ISP标定批次、产测夹具、刷机脚本、序列号/密钥管理、镜像签名、OTA回退、坏板替换和散热一致性。开源样例降低入门工作量，却不能替代这些职责。应让芯片/模组商负责硬件与BSP、集成商负责视频/模型链路、本体商负责控制与保护、云商负责服务/IAM与日志，各自明确缺陷响应和升级兼容窗口。

国产化分析要分层：品牌/开发团队所在地、芯片IP与制造封装、OS/toolchain、runtime二进制、模型权重、相机和机器人SDK、镜像/数据服务分别确认。当前实践明确使用RealSense、UR5e、Python、PyTorch/LeRobot、ROS2/O3DE和开源模型；因此不能由华为品牌推出全系统国产化率或自主可控比例。对关键外部依赖应准备版本冻结、替代接口和离线恢复，并核实替代件的真实性能。

本次没有完整社区活跃度计数，不使用Stars/贡献者数推导采用率。正式选型要求供货/PCN/EOL、当地保修/备件、SDK许可、驱动与算子维护周期，以及云资源区域/配额/SLA的书面证据。静态资料能支撑责任划分，不能承诺现货、认证和成本收益；CloudRobo网页缺失依赖按partial_static归档。
