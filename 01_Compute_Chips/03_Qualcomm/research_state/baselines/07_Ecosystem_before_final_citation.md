# 07｜Qualcomm生态：伙伴分工、开源资产与量产责任

Qualcomm机器人生态的价值需要按工程责任拆开判断。芯片与runtime解决计算执行，模组和载板伙伴承担电气与系统适配，传感器伙伴提供采集器件及wrapper，本体团队仍负责动力学、控制和业务验收。伙伴标识数量不能替代同一目标SKU的BSP、驱动、模型、维护和量产交付矩阵。本章使用截止2026-11-05的公开正文；不能把历史RB5生态清单直接当成IQ10的现成能力。

## 一、主要角色与交接资产

| 角色／代表 | 可核交付或路径 | 与下游交接 | 当前边界 |
|---|---|---|---|
| Qualcomm | QLI、QNN／SNPE、IM SDK、QIR、AI Hub | BSP、固件、图产物、tensor、ROS消息 | 各发行线版本不同 |
| Thundercomm | 模组／开发板、OS定制、硬件设计制造 | 载板、电气、定制BSP及服务合同 | 服务能力不等于每SKU免费交付 |
| Arduino／认证SOM伙伴 | VENTUNO Q、App Lab、Works with Arduino路线 | 容器／应用、MCU sketch与RPC | 原型到量产仍需板级验收 |
| Orbbec | Gemini335L及QIR示例wrapper | USB、图像、深度及IMU topic | 特定模式与硬件版本 |
| NEURA | 本体与具身软件合作 | 计划参考架构／runtime接口 | IQ10逐代际BOM未取得 |
| 开源社区 | qrb_ros_simulation、AI Hub Models、LeRobot | 资产、Python、模型与数据格式 | 开源许可不覆盖所有权重和固件 |

## 二、Thundercomm：从计算板到工程服务

官方机器人解决方案页明确介绍Android、Ubuntu、Embedded Linux的OS定制，完整硬件设计咨询及制造服务，并列vSLAM、路径规划、目标跟踪和AI识别集成。这支持其作为系统集成和量产工程伙伴的角色；服务页的“最高可靠性”等宣传没有可比测量。其平台表包含旧Snapdragon及QRB5165产品和旧Android版本，因此是服务范围与历史资产线索，不能由表格推导每个产品都支持QLI1.6或QIR2.4。[TC_Robotics_Services 原文](https://www.thundercomm.com/solution/robotics/)｜[本地原件](../../reference_metrial/webpages/TC_Robotics_Services--058bea497f0ab588/index.html)

IRB10把这一服务能力延伸到IQ10机器人参考平台，7月公告又给出星尘智能集成宣称。对于本体团队，可减少自行设计高速载板、Bring-up和固件适配的工作，但减少多少成本必须在合同与验收中量化。可复建交接至少应包含PCB／连接器版本、SoM SKU、设备树overlay、刷机包哈希、驱动和固件包、主机工具版本、模型编译产物及原模型配置。若SDK某部分需要授权账户，应在项目启动前确认下载和再分发权限，避免开发样机能跑、量产工厂无法部署。[TC_IRB10_Launch 原文](https://www.thundercomm.com/turbox-irb10-launches-at-embedded-world-2026/)｜[本地原件](../../reference_metrial/webpages/TC_IRB10_Launch--dc6accab2b42cd74/index.html) [TC_IRB10_WAIC 原文](https://www.thundercomm.com/turbox-irb10-waic/)｜[本地原件](../../reference_metrial/webpages/TC_IRB10_WAIC--d87b3aecbca07fa5/index.html)

RB5开发套件页面写明EOL为2026年6月，这仅适用于该套件，不能写成QRB5165芯片全部停产。套件EOL会影响研究设备补购、传感器配件和镜像恢复路线；仍需索取SoM、载板、摄像头和无线配件各自PCN／备件方案。旧教程和96Boards扩展生态可用于历史项目维护，却不是新项目供货保证。本文未取得正式最后采购日、保修期及每个备件库存，不能由页面Buy Now入口认定现货。[TC_RB5_Kit 原文](https://www.thundercomm.com/product/qualcomm-robotics-rb5-development-kit/)｜[本地原件](../../reference_metrial/webpages/TC_RB5_Kit--334f80d91fbbc8df/index.html)

## 三、Arduino、SECO与Toradex：应用迁移和板级变化

Arduino的VENTUNO Q页面明确介绍Works with Arduino认证SOM路线，列SECO IQ8及Toradex Aquila伙伴，并宣称App Lab应用迁移无需改代码。这是应用层可移植性目标，不会自动解决载板的PHY、相机连接、MCU引脚和热设计差异。MPU上的容器可以复用，MCU固件、设备树和RPC协议则需核对版本；容器内安装同名Python包也不保证Host上的NPU驱动ABI一致。[Arduino_Ventuno 原文](https://www.arduino.cc/product-ventuno-q)｜[本地原件](../../reference_metrial/webpages/Arduino_Ventuno--4c389d446211ac9a/index.html)

本轮通过官方检索定位并在浏览器读取Toradex Aquila IQ8产品页及其BSP支持、product brief链接。但统一下载器检查Toradex robots时遇到403或不可用，采用fail-closed，三项未取得有效归档；SECO早前链接亦未取得有效正文。因此本文不以其详细规格、供货年或通用LTS年数建立采购结论。可继续核验的入口为Toradex官方产品页（失败登记TD_Aquila_IQ8）和官方BSP支持策略（失败登记TD_BSP_Support）。检索失败不是厂商没有维护承诺；应取得允许归档的正式资料或采购合同，再锁定样品／量产状态、支持分支及责任范围。

Arduino页面自身Ubuntu、Zephyr与Debian coming soon状态也需保留，不能把未来Debian当作已交付镜像；预订入口与FAQ可购买描述并存，确切供货时间须询价。App Lab集成AI Hub、Edge Impulse及本地模型可降低试用门槛，但涉及云编译或训练时应另核数据去向与账户许可。公开页面提到GenieX开源runtime，旧Genie API资料不能替代对GenieX源码和具体App Lab版本的核验。

## 四、传感器与ROS社区：开放接口的实际成本

Orbbec QIR示例给出Gemini335L的USB接入、udev安装和ROS wrapper，深度配准、RGBD及IMU模式有具体配置。它帮助减少相机接入代码，仍须控制相机固件、曝光和USB带宽。空间配准与软件帧配对不证明多传感器PTP；机器人集成还需外参、frame与时间年龄。雷达、触觉和关节力矩驱动在本轮未取得相同深度的交付资料，不能按伙伴目录推导已经支持。[QC_QIR_Orbbec_MD 原文](https://docs.qualcomm.com/bundle/publicresource/80-70022-265/topics/orbbec-camera_5_2_8.md)｜[本地原件](../../reference_metrial/data/QC_QIR_Orbbec_MD--0b8df5b0e3f41df5/content.md)

![官方图：Orbbec ROS示例输出](../../reference_metrial/derived/figures/QC_QIR_Orbbec.png)

官方图已实际打开核验，展示Orbbec样例的RGB、深度及相关topic输出。它证明样例的软件路径，不证明任意相机固件、多机同步或机器人现场可靠性。完整原图从已归档官方Markdown中提取，未重绘。

QIR桥接和qrb_ros_simulation仓库提供CPU图像与底层buffer、仿真消息及控制接口之间的路径。Host仿真和Device应用通过ROS协作，可让算法开发与目标设备交接，但GitHub main快照会变化，Fuel与mesh资产不一定随代码归档。版本冻结应把仓库commit、ROS发行版、容器digest、资产许可证与下载清单一起管理。QIR部分代码的authorized users限制也说明“用了ROS”不等于整套源码公开。[QC_QIR_Bridge_MD 原文](https://docs.qualcomm.com/bundle/publicresource/80-70022-265/topics/ros-gst-bridge.md)｜[本地原件](../../reference_metrial/data/QC_QIR_Bridge_MD--1b03f7595198d6d4/content.md) [QC_QRB_Simulation_Repo 原文](https://github.com/qualcomm-qrb-ros/qrb_ros_simulation)｜[本地原件](../../reference_metrial/webpages/QC_QRB_Simulation_Repo--1c10ea4d28a57d3c/index.html)

AI Hub Models提供模型封装、导出和demo，LeRobot提供机器人接口与数据格式，两者作用不同：前者可帮助模型映射到目标backend，后者处理数据与策略训练部署。开源代码、模型权重、训练数据和商业runtime分别核许可；例如公开Python不能赋予受限制权重的商业使用权。本文不统计Stars或提交活跃度，因为没有固定时点的系统统计，更不会用Stars解释采用率。[QC_AIHub_Models_Repo 原文](https://github.com/qualcomm/ai-hub-models)｜[本地原件](../../reference_metrial/webpages/QC_AIHub_Models_Repo--f2f0b5d0785d46a2/index.html) [HF_LeRobot_Repo 原文](https://github.com/huggingface/lerobot)｜[本地原件](../../reference_metrial/webpages/HF_LeRobot_Repo--f41f68c5cf0cb6c7/index.html)

## 五、从原型到量产的责任矩阵

| 阶段 | 应冻结／取得资产 | 责任建议 | 风险触发 |
|---|---|---|---|
| 原型 | SDK包、目标镜像、传感器固件 | 板卡＋软件伙伴 | sample接口或软件变更 |
| 产测 | 烧录权限、校准、序号、密钥与恢复 | OEM＋制造方 | 下载授权、密钥丢失 |
| 在岗 | 签名更新、兼容矩阵、回退和日志 | OEM＋运维服务方 | 断电、网络中断、模型失配 |
| 维护 | PCN/EOL、漏洞窗口、备件、保修 | 各层供应商写入合同 | 芯片可买但软件停止维护 |

QLI的OSTree升级有分区、HLOS／Non-HLOS和版本约束。伙伴的云FOTA产品名不能证明目标机器人具备原子回退；需要对BSP与应用、MCU与模型分别验证兼容和断电恢复。日志记录模型／镜像哈希、观测年龄、动作有效期与故障码，才能定位现场问题；不能只依赖远程桌面。[QC_QIR_Upgrade_MD 原文](https://docs.qualcomm.com/bundle/publicresource/80-70022-265/topics/upgrade_individual_sdk.md)｜[本地原件](../../reference_metrial/data/QC_QIR_Upgrade_MD--7a2843583034db1b/content.md)

本轮未取得跨伙伴统一的IQ10生产BSP支持周期、当地维修时效、工业环境验收和保修条款。选择伙伴应以能交付并长期维护的资产和合同为依据，而非共同Logo。NEURA计划中的Neuraverse生命周期与开发市场可构成未来机会，但仍是合作公告的预期，不能替代已经可下载的接口及服务SLA。[NEURA_Qualcomm_Collaboration 原文](https://neura-robotics.com/neura-qualcomm-collaboration/)｜[本地原件](../../reference_metrial/webpages/NEURA_Qualcomm_Collabo--351500d7acaf3f85/index.html)


## 参考资料与归档边界

采集截止：2026-11-05（Asia/Shanghai）。原件通过项目统一下载器登记；官方 Markdown 是厂商提供的原始正文，保留嵌入 SVG/图片数据。HTML 静态壳不作为正文证据。网页依赖缺失按 metadata 记录；不承诺离线交互或像素一致。未执行硬件刷写、模型推理或机器人测试。

| 登记名称 | 版本／适用边界 | 原始资料 | 本地归档 |
|---|---|---|---|
| TC_Robotics_Services | 正文版本及采集时点见本文；未认定为最新 | [原文](https://www.thundercomm.com/solution/robotics/) | [原件](../../reference_metrial/webpages/TC_Robotics_Services--058bea497f0ab588/index.html) |
| TC_IRB10_Launch | 正文版本及采集时点见本文；未认定为最新 | [原文](https://www.thundercomm.com/turbox-irb10-launches-at-embedded-world-2026/) | [原件](../../reference_metrial/webpages/TC_IRB10_Launch--dc6accab2b42cd74/index.html) |
| TC_IRB10_WAIC | 正文版本及采集时点见本文；未认定为最新 | [原文](https://www.thundercomm.com/turbox-irb10-waic/) | [原件](../../reference_metrial/webpages/TC_IRB10_WAIC--d87b3aecbca07fa5/index.html) |
| TC_RB5_Kit | 正文版本及采集时点见本文；未认定为最新 | [原文](https://www.thundercomm.com/product/qualcomm-robotics-rb5-development-kit/) | [原件](../../reference_metrial/webpages/TC_RB5_Kit--334f80d91fbbc8df/index.html) |
| Arduino_Ventuno | 正文版本及采集时点见本文；未认定为最新 | [原文](https://www.arduino.cc/product-ventuno-q) | [原件](../../reference_metrial/webpages/Arduino_Ventuno--4c389d446211ac9a/index.html) |
| QC_QIR_Orbbec_MD | 正文版本及采集时点见本文；未认定为最新 | [原文](https://docs.qualcomm.com/bundle/publicresource/80-70022-265/topics/orbbec-camera_5_2_8.md) | [原件](../../reference_metrial/data/QC_QIR_Orbbec_MD--0b8df5b0e3f41df5/content.md) |
| QC_QIR_Bridge_MD | 正文版本及采集时点见本文；未认定为最新 | [原文](https://docs.qualcomm.com/bundle/publicresource/80-70022-265/topics/ros-gst-bridge.md) | [原件](../../reference_metrial/data/QC_QIR_Bridge_MD--1b03f7595198d6d4/content.md) |
| QC_QRB_Simulation_Repo | 正文版本及采集时点见本文；未认定为最新 | [原文](https://github.com/qualcomm-qrb-ros/qrb_ros_simulation) | [原件](../../reference_metrial/webpages/QC_QRB_Simulation_Repo--1c10ea4d28a57d3c/index.html) |
| QC_AIHub_Models_Repo | 正文版本及采集时点见本文；未认定为最新 | [原文](https://github.com/qualcomm/ai-hub-models) | [原件](../../reference_metrial/webpages/QC_AIHub_Models_Repo--f2f0b5d0785d46a2/index.html) |
| HF_LeRobot_Repo | 正文版本及采集时点见本文；未认定为最新 | [原文](https://github.com/huggingface/lerobot) | [原件](../../reference_metrial/webpages/HF_LeRobot_Repo--f41f68c5cf0cb6c7/index.html) |
| QC_QIR_Upgrade_MD | 正文版本及采集时点见本文；未认定为最新 | [原文](https://docs.qualcomm.com/bundle/publicresource/80-70022-265/topics/upgrade_individual_sdk.md) | [原件](../../reference_metrial/data/QC_QIR_Upgrade_MD--7a2843583034db1b/content.md) |
| NEURA_Qualcomm_Collaboration | 正文版本及采集时点见本文；未认定为最新 | [原文](https://neura-robotics.com/neura-qualcomm-collaboration/) | [原件](../../reference_metrial/webpages/NEURA_Qualcomm_Collabo--351500d7acaf3f85/index.html) |
