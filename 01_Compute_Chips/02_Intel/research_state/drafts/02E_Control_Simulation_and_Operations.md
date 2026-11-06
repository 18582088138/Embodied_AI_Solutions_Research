# 02E Intel 实时控制、仿真与运行维护

Intel 的执行端不是一个由 AI 推理直达电机的统一 runtime，而是 ROS 操作参考应用、PLCopen/EtherCAT 实时控制库与可观测工具协作。本文追踪其任务、消息、共享内存和总线交接，同时审查模拟环境与真实执行的边界。Suite 使用固定归档源码对象，edge-ai-libraries 使用本次取得的树对象 e5dcdcc705a9；没有编译这些代码、绑定网卡或操纵本体。

## ROS 操作参考链与动作契约

RVC 是 Jazzy 视觉抓取参考应用：RealSense 图像/点云进入 perception，旋转框与三维姿态进入 oriented grasp，状态机组织 search、track、approach、grasp、transfer、release，MoveIt 2 Servo 将 waypoint 转为 Cartesian velocity，再由 UR 驱动连接 UR5e 和 Robotiq。文档把 ADBSCAN 和 VLA controller 标为 roadmap；不能把独立 π0.5 示例拼成 RVC 已交付的端到端策略。文档关于同进程零拷贝仅支持感知模块内的设计目标，没有证明驱动到推理到硬件全链共享缓冲。[[Intel02E_Manip]] [[Intel02E_RVC]]

| 配置对象 | 官方参考值/接口 | 解决的约束 | 不能推导的结果 |
|---|---|---|---|
| Servo输入 | delta_twist_cmds、speed_units | 速度单位与动作类型 | 任意VLA输出自动兼容 |
| Servo发布 | publish_period=0.002秒 | 配置发布间隔 | 实测500Hz或电机伺服500Hz |
| 超时 | incoming_command_timeout=0.1秒 | 旧指令处理门槛 | 认证急停响应时间 |
| 碰撞检查 | check_collisions、60Hz配置 | planning scene检查 | 完整危险消除 |
| 本体反馈 | joint_states、UR标定 | 关节/坐标一致 | 跨UR型号无条件通用 |

RVC 的 ee_link、base_link、joint order、TCP 偏置及机器人标定是动作意义的一部分。其示教器坐标与 quaternion 变换是这套参考装配的规则，移植需要验证 frame 链，不能当任意 UR/ROS 坐标公式。更换相机还需 XACRO 外参、z_threshold、ordered PointCloud2 和 optical frame；更换夹爪需 URDF、active joint 与新的 TCP。复建流程是 colcon 构建、RViz/vision/state-machine 分别启动，最后由本体 External Control 程序接受控制；这些步骤体现硬件驱动责任，本文未执行。[[Intel02E_RVC]]

## PLCopen、任务与推理是三种周期

RTmotion 提供 C++ PLCopen function block，依赖示例固定 Ruckig v0.9.2，可按 generic Linux、PREEMPT 或 Xenomai 构建。评估程序反复触发 MC_MoveRelative，文档所列一毫秒 cycle 是示例调度周期，并非所有 SKU、axis 数、策略模型和伺服系统的 WCET 保证。它将 motion function block 与轨迹生成资产分离，适合已有工业控制逻辑迁移；相较 GPU 内核，优势位于控制语义与实时任务组织而非矩阵算力。[[Intel02E_Motion]]

Robot Motion Control Task 用 libectask 创建 EtherCAT task、处理 ENI 拓扑及自定义共享内存回调，libinference 包装 OpenVINO 与 RL 类。示例设左臂、右臂、腿三个 task，ENI 文件和 CPU affinity 分别配置。虽然介绍页突出 NPU，实际 robot_rl_ov.yaml 的 inference_device 是 CPU，模型是 stand.onnx；README 安装 OpenVINO 2026.1.0。这一路不能直接沿用 Suite 2025.3 包集合，也不能将介绍页的 NPU 叙述当默认配置。stand.onnx 的模型卡、训练数据许可、真实腿部稳定失败分母未在这些文件中取得，文档宣称稳定站立只作为厂商描述。[[Intel02E_Gateway]] [[Intel02E_TaskIntro]] [[Intel02E_RLConfig]]

调用推理 callback 的频率、trajectory interpolation、EtherCAT cyclic task 和驱动器内部 servo 必须分别计量。将 inference 放入实时 task 后，只要模型首帧编译、内存分配、设备排队或 fallback 超时，原控制裕量就会变化；注册 callback 不等于证明时限。厂商提供的 NPU IRQ affinity 示例需要按实际 PCI 设备、CPU 编号与 RT/BE 划分调整，不能复制掩码到另一 SKU。可复建验收应固定模型hash、shape、精度、driver/compiler、ENI/PDO、轴数与周期，测输入年龄、整段推理和循环尾部裕量，并注入超时及设备失联。[[Intel02E_Gateway]] [[Intel02E_RT]]

## 内存隔离和总线调度

RT Data Agent 的 block ring buffer 有固定 block 数与最大块大小，每次读写不跨 block，单个 named buffer 只允许一个 producer 和一个 consumer；init/open/read/write/close 构成生命周期。其 lockless 机制把实时数据采集与 Python agent、数据库、Grafana 的慢消费分开，但不是多生产者通用动作总线。文档的 shm_blkbuf_full 返回说明还存在文字歧义，需以实现和测试为准。分析上必须定义 buffer full 时丢弃、重试或停止策略，并带序列号/时间戳；否则监控画面正常也可能显示陈旧样本。这里的固定块大小既是有界内存条件，也是 payload 格式/容量约束。[[Intel02E_Agent]] [[Intel02E_Shared]]

IgH EtherCAT 路径区分 native igb/igc/mGBE 和 generic 驱动；native 支持列举 I210/I211/I225/I226 等 NIC，generic 经过常规网络栈，不能由板上有 Ethernet 就声称同等实时性能。内核路线使用 DKMS 与 sysconfig 的 MAC/REBIND_NICS/DEVICE_MODULES；DPDK 路线在 PREEMPT RT 用户态保留 IgH API，通过 VFIO 绑定端口和 ecrt.conf 配置，master 随应用 lib call 启动，诊断工具需要先有应用。PDO/SDO、CoE/SoE/DC 支持是协议能力，不能替代目标 ENI、从站和线缆拓扑验证。[[Intel02E_EtherCAT]]

![官方EtherCAT时间定义]( [[FIG:Intel02E_TimingFig]] )

原图明确输入 Tin、计算 Tcalc、输出 Tout、执行 Texec 与完整循环 Tcycle，并画 expected/actual 和 jitter；没有数值测量。因此它支持按链路分解时延，不能提供本平台 P99 或 WCET。实时视觉还将 CPU 发令 T0、IO 触发 T1 和 CMOS 成像 T2 分开，曝光生成期间的确定性需要相机和 time-aware IO 一同成立。OS 调优用 isolcpus、rcu_nocbs、nohz_full、IRQ 与 CAT/cache 分配减少干扰，Series 2/3 的 E-core 配置存在区别；CPUID 拓扑、BIOS 和芯片支持必须核对。锁 turbo 与功耗/温度相关，文档也提示可靠性代价，不能视为免费性能。[[Intel02E_TimingFig]] [[Intel02E_EtherCAT]] [[Intel02E_RT]]

## 仿真、性能观测与恢复

Suite 当前总览以 Ubuntu 24.04/Jazzy/Gazebo Harmonic 为主，MuJoCo 用于另一类具身动力学流程；Gazebo、ros_gz、MuJoCo 是上游平台，并非 Intel 自研物理引擎。use_sim_time 使消息、TF、轨迹共享 /clock，但虚拟时间暂停或慢于壁钟时，仿真时间延迟与真实吞吐仍要双独立记录。headless 关闭 GUI 不保证摄像头 rendering 已消失，Mock Hardware 更没有接触和传感器噪声，适合验证通信状态机。[[Intel02E_Sim]]

Pick & Place 页面开头和末尾仍注明 Humble/Gazebo Classic 已测试，同时添加 Jazzy 安装标签；不能只凭标签断言 Harmonic 已完整验收。更关键的是物体位置通过 Gazebo get_entity_state 获取，绕过 perception。双 UR5 与 TurtleBot3 的协调只能支持 Nav2/MoveIt2/namespace/状态机编排演示。页面还说明顺序 spawn 是为了避免 controller manager 改变 gzserver namespace；建议 CycloneDDS 针对该演示观察到的稳定性问题，不构成所有 DDS 的通用排名。[[Intel02E_PickSim]]

Robotics System Profiler 保存 session_info、graph_timing.csv、resource_usage 与 GPU log，远程 graph 通过 DDS peer discovery、资源通过 SSH 采样。文档线程模式约百分之五至十、PID 约百分之二至三开销缺完整测量条件，需做有/无 profiler 对照。自动输入输出延迟关联不能代替带 trace ID 的逐请求因果追踪；pidstat 百分之一百表示一个核，不能把二千百分比误读为整机利用率。Grafana 的延迟颜色阈值、五秒 scrape 只是仪表配置，不是控制 deadline。[[Intel02E_Profiler]] [[Intel02E_Commands]] [[Intel02E_Grafana]]

Pick benchmark 规定稳定三十秒后采样一百二十秒，二十五次是默认运行次数而非已完成试验；本文没有实测数据。KVM 指南提供 VT-d/VFIO、iGPU/USB 直通、QEMU/libvirt 和匹配 vmlinux 的 dump 分析。直通资源的宿主/guest 所有权、重启重新绑定和日志上下文都要保留；virsh destroy 是强制断电，不是回退事务。已取得资料支持制作/运行镜像、观测、崩溃定位，但没有完整 OTA 签名版本事务、双槽回退和在动机器人安全恢复证据。选型时，Intel 控制库便于保留 PLCopen/ENI 资产；换平台仍须重验网卡、IRQ、共享缓冲及本体 SDK。Apache 标识的应用源码与 IgH、Ruckig、仿真资产、固件及模型许可分别处理。[[Intel02E_Benchmark]] [[Intel02E_KVM]]
