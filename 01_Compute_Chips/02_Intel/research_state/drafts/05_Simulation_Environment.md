# Intel 05 — 仿真环境、时间与迁移验证

截止2026-11-05；Suite固定对象1b0b22a2964f。本文核验文档、场景片段和补丁，没有启动仿真器。Intel提供集成管线、适配与样例，上游Gazebo、MuJoCo及OCS2分别承担仿真和求解，不据此称Intel拥有独占物理引擎。[[Intel02E_Sim]]

## 可用路线及实际验证层级

| 路线 | 版本与对象 | 模块/产物 | 可验证问题 | 无法直接证明 |
|---|---|---|---|---|
| Gazebo通用栈 | 总览Harmonic＋Jazzy＋Ubuntu24.04 | 世界、刚体、传感器、ros_gz | ROS话题、TF、导航与控制交接 | 所有旧world均采用相同求解器 |
| PicknPlace | 两UR5＋TurtleBot3＋输送带 | 状态机、Nav2、MoveIt、真值物体位置 | 多机任务编排与命名空间 | 视觉检测质量/真实抓取收益 |
| wandering | TurtleBot3 Waffle RGB-D | 点云融合、ADBSCAN、RTAB-Map、Nav2 | 探索、成本地图和障碍生命周期 | 真实反光/遮挡/里程计误差鲁棒性 |
| RVC | UR5e＋Robotiq2F-85＋D415光学frame | 合成图像/点云→抓取→Servo | 感知与控制接口组合 | D415测距误差或本体功能安全 |
| ACT/RDT | ACT pinMuJoCo3.2.6；双臂任务 | 示范episode、相机、动作评估 | 模仿学习与仿真奖励 | 硬件驱动和sim-to-real泛化 |
| ACT→MPC | OCS2＋MuJoCo2.3.7插件路线 | 策略轨迹→MPC/MRT→控制 | 感知与动作频率间衔接 | 等同ACT独立环境或安全认证 |
| Mock hardware | 无真实物理/接触 | 驱动内部关节反馈与RViz | 状态机与轨迹消息测试 | 摩擦、惯量、碰撞后的执行 |

原文：[[Intel05_Basic]]、[[Intel05_Wandering]]、[[Intel05_RVCSim]]、[[Intel02C_ACT]]、[[Intel02C_RDT]]、[[Intel04_MPC]]。Mock模式反馈通常不会重现负载和通讯延迟，适合作为最早的接口测试，而非物理正确性的替代。

## 场景与物理参数：不能跨文件拼接

`multi_robot_world.world`为SDF1.6，含ODE quick solver、150迭代、max_step_size0.001s、real_time_update_rate1000及目标real_time_factor1，还写cfm、erp和接触修正参数。这是文件配置；默认Gazebo launch指向另一`no_roof_small_warehouse`路径，总览写DART/Harmonic。因此不能认定所下载的world就是默认运行场景，不能从1ms推出实测千赫兹，也不能把旧ODE字段当Harmonic后端完整生效证明。需要保存启动后的解析world、实际physics插件及参数日志。[[Intel05_MultiWorld]]、[[Intel05_GazeboLaunch]]、[[Intel02E_Sim]]

名为camera.xacro的文件实际内容是SDF1.8，普通camera类型，640×480、R8G8B8、30Hz，水平视场1.3962634rad、裁剪0.02—300，图像高斯噪声均值0/标准差0.007，使用ogre2 sensors插件。不能因文件位于UR相机目录就称其为完整D415深度模型；它没有在这段源码中建立双目视差、结构光、深度置信度或温漂机制。噪声数值的物理标定来源也未取得。设置无GUI不会关闭这类相机生成所需的离屏渲染，GPU仍可能与推理争用。[[Intel05_Camera]]

MuJoCo适配补丁新增红块、插销、蓝槽的free joint和geom，能核到frictionloss0.01、部分geom摩擦`1 0.005 0.0001`、槽体`1 0.05 0.001`、condim4及接触solimp/solref。这些值影响接触阻力和约束收敛；相同视觉材质不代表相同真实接触。补丁修改ActuatorCommand，配置里出现publish_rate100，需要区分插件发布周期、求解步与动作消费周期。单补丁没有提供整个被补丁子模块的最终物理步长及每个相机频率，必须锁定子模块和应用后的产物才能复建。[[Intel05_MujocoPatch1]]

## 时间、桥接与多机编排

固定launch用`/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock`把仿真时钟桥到ROS。节点启用use_sim_time后，TF查询、轨迹插值与消息header才有同一时间基准；暂停、复位或加速仿真时，时间可能停止或回跳。超时、速率统计和CPU占用要明确用哪个时钟。总览称性能分析按仿真timestamp，无法据此判断所有工具的执行计时都用仿真时钟；主机真实耗时必须另记单调时钟，否则慢主机仍可能表现为“仿真内无延迟”。[[Intel05_GazeboLaunch]]、[[Intel02E_Sim]]

若物理以1ms步进、相机目标30Hz，分析上每帧约跨33.33物理tick；采样应由调度器处理非整数关系，不能强行认为每33步精确发布。模型几十毫秒完成推理时，策略观测已跨多个物理步。需要记录传感器生成时刻、桥接发布时刻、策略开始/结束、动作被仿真器消费的tick和队列年龄，测相位与累积延迟，而非仅看话题平均频率。该例为分析，本文没有测得调度抖动。

旧PicknPlace教程明确Humble/Gazebo Classic已测，却同页含Jazzy安装标签；新版基础介绍又写ros_gz路径。旧教程对多个控制器在gzserver内变更全局namespace的风险采用串行spawn和namespace reset插件。Cyclone DDS建议来自该多节点场景的观察，不证明FastDDS普遍更差。节点数量、participant布局和QoS要随实际版本复核。[[Intel02E_PickSim]]、[[Intel05_Basic]]

wandering把LaserScan与深度点云同步、变换到base_link后体素下采样，ADBSCAN障碍送成本地图；RTAB-Map生成map→odom，frontier探索发送NavigateToPose。障碍padding和timeout会直接改变安全距离及过期障碍残留。仿真中时间一致不能掩盖真实相机与LiDAR不同曝光/时钟域，迁移前应注入丢帧、延迟、TF暂缺与地图失效，而不是只复现一条无遮挡路线。[[Intel05_Wandering]]

## 官方场景图与测量条件

![Suite官方PicknPlace场景截图]([[FIG:Intel05_SimFigure]])

已实际打开原图，能看到两臂、输送带、AMR、RViz和Gazebo统计栏。它支持场景构成和可视化入口；截图里的FPS/real-time factor仅某一瞬间，缺硬件、时长和采样方法，不能成为benchmark。物体位置直接来自Gazebo get_entity_state，未经过相机检测；所以搬运流程完成也不能计入感知模型成功率。[[Intel05_SimFigure]]、[[Intel02E_PickSim]]

系统profiler提供先稳定30秒、采样120秒和多轮参数的脚本流程；不是本文跑出的结果。比较需锁定场景资产、机器人数量、物理步、渲染分辨率/模式、GPU驱动、CPU/RAM/OS、并发模型及测量窗口，分别报告物理real-time factor、图像帧率、ROS数据年龄和任务完成时间。SnapFlow的LIBERO成功与推理延迟分开测，后者排除仿真/渲染；不得与Gazebo整体吞吐直接比较。[[Intel02E_Benchmark]]、[[Intel02F_Benchmark]]

## 合成数据与sim-to-real放行

现有资料证明可生成示范episode和合成图像，可在仿真训练/评估ACT等策略；未取得这套目标硬件的系统性域随机化分布、系统辨识报告、真实留出任务与迁移成功率。没有这些证据不说明上游引擎不能做，而是不能归为Intel已交付验证。建议先辨识质量、惯量、关节阻尼、夹爪死区、通讯延迟与相机误差，再随机化可测范围；不能用任意宽随机数替代物理标定。

验证分三层：接口层检查frame/单位/消息和复位清队列；物理层检查接触、负载、碰撞模型和求解收敛；迁移层在真实未见物体、光照、摆放和网络条件下记录尝试数、成功、人工介入及危险响应。仿真与真实数据应共享任务定义，但分别统计。代码许可、MuJoCo/Gazebo二进制、UR/Robotiq机器人描述、Fuel外链资产、checkpoint和数据分别核对；当前归档场景片段没有下载所有外链mesh/模型，不声称完整可运行场景包。默认launch和MPC子模块尚需安装产物复建验证，本文的结论停在源码与文档层。
