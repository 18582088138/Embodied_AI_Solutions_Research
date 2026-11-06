# 02E ROS、实时控制与部署运维

研究截止2026-11-05。本篇把模型输出继续追到消息、调度域、总线和升级事务，依据 Firefly/Rockchip 适配文档；这是伙伴交付路线，不是全部 Rockchip 板卡共享的实时保证。未取得指定机器人闭环工程、硬实时 WCET 或安全认证。本文实际读取页面及其静态图片：本组页面的图片主要是站点导航，关键机制以官方文字框图、配置和表格呈现，因此不拿无关装饰图补成控制架构。未进行刷机、烧录密钥或电机操作。

## 一、ROS 安装与消息契约的交接

Firefly 安装条件是 ARM64、Ubuntu22.04 Jammy、ROS2 Humble Desktop，RViz/RQt 还依赖 GLX/OpenGL。不能从 RViz 可运行推出 GPU 深度学习加速，也不能把 Debian12 RK182X 主机说明替换成同一 ROS 安装矩阵。安装验证包含 source setup、ros2 doctor、RViz 检查，talker/listener 只证明样例通信。目标模型与 rknn3.service、驱动、设备树必须另验。[RK02_ROS](https://community.t-firefly.com/en/docs/software/industry-robot/ROS2/ros2-install-opengl)（[本地原件](REFERENCES.md#ref-74cead783219a4cf)) [RK02_ROS_Verify](https://community.t-firefly.com/en/docs/software/industry-robot/ROS2/ros2-verify-installation)（[本地原件](REFERENCES.md#ref-f6e371a0ee0f496a)) [RK02_ROS_Comm](https://community.t-firefly.com/en/docs/software/industry-robot/ROS2/ros2-test-communication)（[本地原件](REFERENCES.md#ref-ae652eb249a274bb))

分析上的完整桥接是相机 buffer→模型预处理→推理输出→携带采集时间/frame_id 的感知消息→规划或动作适配→控制器。数组要定义 dtype、尺寸、归一化、坐标系、类别顺序、关节顺序与单位，不能只把浮点输出发布到 topic。语言结果需校验对象/技能白名单、世界状态和超时，再交给动作执行。当前文档未提供一份把 RKNN/RKLLM 输出与指定本体关节契约贯通的官方工程，本文不把独立 demo 拼接为验证过的闭环。

队列应按任务定义：相机可采用有限深度和丢弃过期帧，动作命令则要区分丢弃、合并、取消与完成确认。可靠传输可能积压旧观测，低丢包不等于低数据年龄。应同时记录 acquisition、推理开始/结束、消息发布、控制接收与实际关节反馈时刻；ROS timestamp 若来自各设备本地时钟需标定时钟关系。推理 TPS 不等于 policy-call，更不等于 controller 或驱动器伺服频率。这些是系统分析与验收要求，当前伙伴安装文档没有测出端到端分布。

## 二、PREEMPT_RT：可抢占机制与证据边界

PREEMPT_RT 通过 rt_mutex 替代可睡眠锁、线程化大部分中断及 RCU 回调，减少不可抢占路径；它保留 Linux 驱动/库生态，仍需检查具体 BSP 驱动的长临界区。Firefly 以 RK3588 为例，明确补丁需匹配内核，示例路径含 kernel6.1.118 与基于特定 Rockchip commit 的 rt36 补丁；不能根据文件名将任意主线 RT 补丁直接施加到任何 BSP。构建组合包含 rockchip_rt.config 与目标 itx3588j 镜像。[RK02_RT_Preempt](https://community.t-firefly.com/en/docs/software/industry-robot/RT-Linux/rtlinux-preempt-rt)（[本地原件](REFERENCES.md#ref-38c6142c135a686a))

官方测试命令 cyclictest -c0 -m -t -a -p99 -D12h 中 p99 是线程优先级99，不是 P99 延迟统计。运行12小时也只是测试时长，不自动得出 WCET。页面“通常微秒级”是通用描述，没有指定板卡温度、CPU/NPU/DMA/网络负载、最大延迟表及失败样本，不能报告为实测指标。验证应加入 NPU多模型、ISP录像、存储刷写和网口流量，检查 IRQ亲和、锁页、缺页、频率/热降频；比较均值、分位数、观察到的最大值和丢周期，保留无法穷举的异常条件。对外部 MCU/RTOS 的机制比较是减少 Linux 共享调度干扰，但增加通信与状态一致性维护，没有同条件测试不下“更实时”的绝对结论。

## 三、AMP：划分资源而非仅绑核

AMP 让 Linux、RT-Thread/HAL 裸机占不同核，默认无 hypervisor，U-Boot 装载启动远端固件，RPMsg/RPMsg-Lite 以共享内存与核间中断通信。其收益来自执行域划分；无虚拟化并不等于 DDR、时钟、电源和外设故障隔离。SDK 包含 device/rockchip 的 defconfig/ITS、kernel rockchip_amp.c 与 DTS、hal、rtos、u-boot、rkbin 和工具链；源码目录与二进制交付责任各自存在。[RK02_AMP](https://community.t-firefly.com/en/docs/software/industry-robot/AMP/amp-overview)（[本地原件](REFERENCES.md#ref-c4a45aaffd3431e6)) [RK02_AMP_Structure](https://community.t-firefly.com/en/docs/software/industry-robot/AMP/amp-sdk-structure)（[本地原件](REFERENCES.md#ref-b8d11e251a4e4afa))

| 资源 | 配置一致性 | 失效机制 | 放行检查 |
| --- | --- | --- | --- |
| CPU | Linux SMP 与远端核互斥 | 同核双重管理 | 检查启动/热插拔配置 |
| 私有内存 | DTS reserved-memory、ITS地址、linker一致 | Linux/CMA覆盖固件 | 核对地址和大小 |
| 共享内存 | RPMsg区域一致，不重叠显示/NPU/CMA | 覆盖/旧缓存 | 校验buffer所有权与同步 |
| 外设/IRQ/pin | 一个系统主动管理，路由/IOMUX匹配 | 双驱动/中断丢失 | 确认DTS禁用和远端配置 |
| 时钟/电源 | Linux保留远端使用域 | Linux误关无consumer域 | 空闲/休眠/恢复压力测试 |

这些条件由伙伴资源规划明确列出；绑定一个 CPU 核而未预留内存、IRQ 和时钟不构成 AMP 完整配置。调试需 Linux 与远端双 UART，不能跨板照抄针脚。RPMsg 消息还需应用层序列号、状态时间、命令有效期、确认与独立看门狗；当前页面没有给出指定本体的异常处理协议，需开发和失效注入验证。[RK02_AMP_Prereq](https://community.t-firefly.com/en/docs/software/industry-robot/AMP/amp-prerequisites)（[本地原件](REFERENCES.md#ref-7859770da31383a7))

## 四、EtherCAT：驱动、状态机与控制责任

伙伴路线基于 IgH：应用经 libethercat.so/ecrt_*→/dev/EtherCAT0→ec_master.ko→ec_generic 或专用网卡驱动→从站。专用网口传二层帧，一般不设 IP，不应同时受 NetworkManager/DHCP 管理。PDO 是周期过程数据，SDO 是非周期参数，DC 是分布式时钟；不要把 EtherCAT DC 与普通传感器 PTP 对时混为同一时钟域。INIT/PREOP/SAFEOP/OP 状态机描述通信状态，OP 不是安全认证。[RK02_EtherCAT](https://community.t-firefly.com/en/docs/software/industry-robot/EtherCAT/ethercat-overview-2)（[本地原件](REFERENCES.md#ref-6a7a5c1a9d8cffba))

编译必须使用已配置的目标 kernel、匹配工具链与模块版本，generic 构建选项不代表 Rockchip stmmac 实时适配已取得。文档要求先参考 SDK 特有 master/stmmac 修改，冻结 tag/commit；用户态工具能运行但没有 /dev/EtherCAT0 时，应查模块而非仅重装 CLI。所谓“支持 EtherCAT”要落到准确网卡、驱动分支、从站 ESI、PDO映射、周期和 DC误差。本文没有取得全负载周期误差、网络拓扑与目标伺服实测。[RK02_EtherCAT_Build](https://community.t-firefly.com/en/docs/software/industry-robot/EtherCAT/ethercat-build-install)（[本地原件](REFERENCES.md#ref-974bab78cbb46482))

官方准备页明确正常通信不代表电机安全，应核对控制字、模式、位置/速度/力矩单位及退出/断链/错误态的安全输出。这是工程调试要求，不能拿示例目标值驱动真实机构。上层进程停止写命令时，下层可能继续保持旧设定，必须确认驱动器 watchdog、制动和硬件急停独立生效。[RK02_EtherCAT_Preparation](https://community.t-firefly.com/en/docs/software/industry-robot/EtherCAT/ethercat-preparation)（[本地原件](REFERENCES.md#ref-8c42f6b3ba4f0541))

## 五、OTA 与可信启动：升级是事务

Linux Recovery 流程为下载 update.img→updateEngine 写 misc 标志→重启 Recovery→按 package-file 写分区→回 Normal。若包存在 userdata，不应同次覆盖承载包的 userdata。例子 partition mask0xFFFC00 与某些 SDK默认0x3FFC00 存在版本差异，需读当前源码/帮助；掩码不能跨 BSP 盲用。先全刷并验目标固件，再制作升级包；检查保留数据、U-Boot/kernel/rootfs/驱动与 Recovery 日志。[RK02_OTA_Linux](https://community.t-firefly.com/en/docs/software/other/OTA/ota-linux)（[本地原件](REFERENCES.md#ref-ccf3f3086d29b250))

Android A/B 写非活动槽，重启和健康检查后确认成功，重复启动失败可退回；Virtual A/B 使用快照但增加临时空间和 merge要求。差分包严格绑定源固件；配置 BOARD_USES_AB_IMAGE、U-Boot CONFIG_ANDROID_AB 与分区 slotselect 要一致。A/B 解决系统写入/启动回退，但模型、词表、标定、控制参数和 KV缓存也要纳入版本事务；否则系统回退而模型未回退仍可能不兼容。升级健康检查应包含传感器与 NPU加载、控制通道、安全静止状态，不能仅检查HTTP在线。[RK02_OTA](https://community.t-firefly.com/en/docs/software/other/OTA/ota-overview)（[本地原件](REFERENCES.md#ref-f4f11c46a83ce360)) [RK02_OTA_Android](https://community.t-firefly.com/en/docs/software/other/OTA/ota-android)（[本地原件](REFERENCES.md#ref-b74204037a5761bf))

SecureBoot 的 kernel6.1 示例配置含 FIT签名、OP-TEE/RPMB、DM_VERITY，并要求 USE_EXTBOOT=n；仅列 config 不证明整机密钥链与存储已经验证。伙伴说明当前 rollback-index不支持；签名认证来源不能直接证明防回滚。RK_SECURITY_BURN_KEY 涉及一次性烧录，生产必须先验证恢复路径和密钥管理；本文没有执行这种操作。若 U-Boot已签而 kernel未签，文档称校验失败后进 loader。[RK02_SecureBoot](https://community.t-firefly.com/en/docs/software/other/SecureBoot/secureboot-overview)（[本地原件](REFERENCES.md#ref-6a0f17927bb8ae3c)) [RK02_Secure_Config](https://community.t-firefly.com/en/docs/software/other/SecureBoot/secureboot-config)（[本地原件](REFERENCES.md#ref-0e3551cfe884717f))

运维交付需要确定 BSP许可清单、内核/模块源码义务、IgH与RTOS授权、闭源固件和本体SDK许可；本篇伙伴指南未给出完整可再分发包与维护期限。验收应冻结物料/固件/模型哈希，验证断电升级、坏包、槽切换、驱动回归、远端核失联、消息过期和传感器重连。结果未取得时列为待测，不能用文档的默认配置宣称无人值守量产可靠性。


## 参考资料与本地原文

采集时间逐项列出；移动分支及无版本网页仅代表此次快照。HTML 保留正文与可取得静态依赖，动态交互、视频及缺失依赖不保证完整。未进行目标板安装或实机性能验证。

| 来源 | 原 URL | 本地原件 | 采集 UTC | 归档状态 |
| --- | --- | --- | --- | --- |
| RK02_ROS | [原文](https://community.t-firefly.com/en/docs/software/industry-robot/ROS2/ros2-install-opengl) | [归档](REFERENCES.md#ref-74cead783219a4cf) | 2026-11-04T16:37:46.890138+00:00 | partial_static；缺失依赖 2 |
| RK02_ROS_Verify | [原文](https://community.t-firefly.com/en/docs/software/industry-robot/ROS2/ros2-verify-installation) | [归档](REFERENCES.md#ref-f6e371a0ee0f496a) | 2026-11-04T16:40:31.154894+00:00 | partial_static；缺失依赖 2 |
| RK02_ROS_Comm | [原文](https://community.t-firefly.com/en/docs/software/industry-robot/ROS2/ros2-test-communication) | [归档](REFERENCES.md#ref-ae652eb249a274bb) | 2026-11-04T16:41:51.681375+00:00 | partial_static；缺失依赖 2 |
| RK02_RT_Preempt | [原文](https://community.t-firefly.com/en/docs/software/industry-robot/RT-Linux/rtlinux-preempt-rt) | [归档](REFERENCES.md#ref-38c6142c135a686a) | 2026-11-04T16:40:23.281062+00:00 | partial_static；缺失依赖 2 |
| RK02_AMP | [原文](https://community.t-firefly.com/en/docs/software/industry-robot/AMP/amp-overview) | [归档](REFERENCES.md#ref-c4a45aaffd3431e6) | 2026-11-04T16:37:42.803549+00:00 | partial_static；缺失依赖 2 |
| RK02_AMP_Structure | [原文](https://community.t-firefly.com/en/docs/software/industry-robot/AMP/amp-sdk-structure) | [归档](REFERENCES.md#ref-b8d11e251a4e4afa) | 2026-11-04T16:40:25.673549+00:00 | partial_static；缺失依赖 2 |
| RK02_AMP_Prereq | [原文](https://community.t-firefly.com/en/docs/software/industry-robot/AMP/amp-prerequisites) | [归档](REFERENCES.md#ref-7859770da31383a7) | 2026-11-04T16:41:47.418007+00:00 | partial_static；缺失依赖 2 |
| RK02_EtherCAT | [原文](https://community.t-firefly.com/en/docs/software/industry-robot/EtherCAT/ethercat-overview-2) | [归档](REFERENCES.md#ref-6a7a5c1a9d8cffba) | 2026-11-04T16:37:44.948392+00:00 | partial_static；缺失依赖 2 |
| RK02_EtherCAT_Build | [原文](https://community.t-firefly.com/en/docs/software/industry-robot/EtherCAT/ethercat-build-install) | [归档](REFERENCES.md#ref-974bab78cbb46482) | 2026-11-04T16:41:42.729970+00:00 | partial_static；缺失依赖 2 |
| RK02_EtherCAT_Preparation | [原文](https://community.t-firefly.com/en/docs/software/industry-robot/EtherCAT/ethercat-preparation) | [归档](REFERENCES.md#ref-8c42f6b3ba4f0541) | 2026-11-04T16:40:27.995472+00:00 | partial_static；缺失依赖 2 |
| RK02_OTA_Linux | [原文](https://community.t-firefly.com/en/docs/software/other/OTA/ota-linux) | [归档](REFERENCES.md#ref-ccf3f3086d29b250) | 2026-11-04T16:41:38.657971+00:00 | partial_static；缺失依赖 2 |
| RK02_OTA | [原文](https://community.t-firefly.com/en/docs/software/other/OTA/ota-overview) | [归档](REFERENCES.md#ref-f4f11c46a83ce360) | 2026-11-04T16:37:48.693383+00:00 | partial_static；缺失依赖 2 |
| RK02_OTA_Android | [原文](https://community.t-firefly.com/en/docs/software/other/OTA/ota-android) | [归档](REFERENCES.md#ref-b74204037a5761bf) | 2026-11-04T16:40:33.388088+00:00 | partial_static；缺失依赖 2 |
| RK02_SecureBoot | [原文](https://community.t-firefly.com/en/docs/software/other/SecureBoot/secureboot-overview) | [归档](REFERENCES.md#ref-6a0f17927bb8ae3c) | 2026-11-04T16:37:50.466010+00:00 | partial_static；缺失依赖 2 |
| RK02_Secure_Config | [原文](https://community.t-firefly.com/en/docs/software/other/SecureBoot/secureboot-config) | [归档](REFERENCES.md#ref-0e3551cfe884717f) | 2026-11-04T16:40:35.448148+00:00 | partial_static；缺失依赖 2 |

[证据记录](research_state/evidence/02E_ROS_Control_Operations.json)；[本章开始前哈希基线](research_state/baselines/02E_ROS_Control_Operations_before.json)。检查和去重记录由专题索引汇总。
