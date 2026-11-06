# 02D Intel ROS 感知、空间计算与导航

本篇解释从图像、深度与点云到地图、路径和底盘速度的接口。研究采用归档的固定 Robotics AI Suite 源码对象；Jazzy 与 Humble 示例分别看待。Intel 的价值集中于 OpenVINO 节点、空间计算加速和导航组件，ROS 2、DDS、Nav2 与本体驱动各自承担不同职责。教程可复建的步骤属于文献证据，本研究没有安装包、回放 rosbag 或运行底盘。

## 数据流与责任边界

![官方AMR架构]( [[FIG:Intel02D_AMR_Fig]] )

图来自 Suite 官方 AMR 架构。蓝色表示 Intel 提供或优化的组件，绿色为开源组件，灰色为用户提供；实线为数据流，虚线为反馈。WanderingMapper 产生探索地图，GoalCatcher 把前沿转换为 NavigateToPose 目标，Nav2 的 planner、controller、costmaps、BT 再生成 cmd_vel。图上 CPU/iGPU/NPU 是计算目标标注，并非全部模块同时运行的验收结果；底盘驱动和硬件仍需集成。[[Intel02D_AMR_Fig]] [[Intel02D_Nav2]]

| 环节 | 输入/对象 | 输出与交接 | Intel增量 | 验证条件 |
|---|---|---|---|---|
| 检测 | image、模型IR、标签 | detected_objects、可视化图像 | OpenVINO节点 | device、预处理、消息时间戳 |
| 空间计算 | 点云、queue、索引 | 过滤点云、邻域与分割 | PCL/FLANN oneAPI | 同context、有限坐标、容量 |
| 定位建图 | RGB-D、CameraInfo、TF | pose、2D/3D地图 | Collab SLAM、FastMapping | 内参、深度单位、地图版本 |
| 路径规划 | costmap、start/goal | nav_msgs/Path | ITS插件 | 路网有效、动态障碍条件 |
| 执行动作 | path、局部costmap、里程计 | cmd_vel与底盘反馈 | 接入Nav2参考应用 | 控制器、本体、停止责任 |

## 检测包装、同步与背压

Object Detection 教程下载 MobileNet SSD 并转换 IR，设备选项为 CPU/GPU/NPU。实际 launch 的默认值为 GPU，修改 YAML 的 engine、输入图片和标签路径后启动 openvino_node 与 rviz2；Jazzy 分支还设置 Fast CDR/Fast RTPS 的 LD_PRELOAD。源码说明这是特定 ROS 动态库组合的配置，不应不加验证地套入任意新版 DDS。节点发布被重映射的检测与显示话题，不能由设备参数推导出相机 DMA 到 NPU 的零拷贝路径。[[Intel02D_Detection]] [[Intel02D_Launch]]

Multi-camera 文档提供一至四路 USB/GMSL 和 YOLOv8 示例，并使用 pyproject、uv.lock 管理环境。路数说明属于演示配置，载板桥接、相机驱动与带宽仍是前提。文档出现 `.config/config_camera.json` 与命令 `config/config_camera.json` 的差别，Humble 命令末尾还有 `.jsony`；这些是实际保留的复建障碍，本研究未默默修正后声称运行成功。[[Intel02D_Multicam]]

YOLO 的 ImageSync 源码将 RGB 和 depth 按 header.stamp 放入优先队列，默认配对容差为十毫秒，匹配时消费两帧，否则丢弃较早的一侧。此容差仅是软件配对门槛，并不证明曝光硬同步。更值得审查的是：一侧长期缺失时，另一侧队列没有明确容量截断，超过一千个对象只打印提示；resolve 在插入锁释放后执行。分析上，多线程 callback 是否可能并发访问队列取决于 executor/callback group，需在真实节点配置中核对，不能只靠局部 mutex 宣称线程安全或有界内存。[[Intel02D_ImageSync]]

ROS QoS 的 sensor data profile 倾向 best effort 和较小队列，目的是及时收到近期样本；best effort 发布者与 reliable 订阅者不兼容。deadline 事件和 lifespan 过期丢弃可辅助监测，但不保证从曝光到控制的最大数据年龄。executor 用 wait set 感知可用队列，过载时调度不等于消息 FIFO；MultiThreadedExecutor 的并行性由 callback group 约束。集成时应分别记录曝光、接收、推理开始/完成、地图更新时间与动作提交时间，设置旧观测拒绝、队列上限和故障响应。[[Intel02D_ROS_QoS]] [[Intel02D_ROS_Executors]]

## PCL 与 FLANN：加速成立在对象和生命周期上

PCL oneAPI 文档绑定 PCL 1.15、oneAPI 2026.1 及 SYCL 2020/Level Zero，区分 standalone extension 与 full integrated 构建。`setQueue(sycl::queue&)` 允许调用方复用持久队列；PointCloudDev 与后续算法需要处于同一 context。使用 icpx 与 -fsycl、导出的 CMake target，解决的痛点是点云过滤、分割等计算重复调度以及中间数据搬运。每帧创建 queue、反复回传 host 容器或小点云派发，都可能吞掉 kernel 收益。官方关于点数交叉区的建议需要目标机复测，而非固定平台阈值。[[Intel02D_PCL]]

FLANN 的对象是三维 KD-tree，不是任意维度向量数据库：buildIndex 建树，knnSearch 与 radiusSearch 查询；L2 的 radius 按平方距离传递。非三维、NaN/Inf、非法半径等输入需按其约束处理。普通 radius 查询可先计数再分配 CSR 输出，驻留 `radiusSearchResident` 则预分配 query、indices、counts、scratch，以 max_neighbors 明确每行容量，避免逐帧嵌套 host 容器分配。队列能共享并不意味着索引和 Matrix 能无锁写入。共享物理内存减少离散 GPU 的 PCIe 搬运因素，仍需核对 USM 类型、同步、布局和 ROS 序列化。[[Intel02D_FLANN]]

| 厂商FLANN测量摘录 | 点数 | queries/k | CPU中位ms | GPU中位ms | 可推导范围 |
|---|---|---|---|---|---|
| Google Benchmark 1.9.5 | 100K | 16384/8 | 21.859 | 15.623 | 此查询工作负载 |
| Google Benchmark 1.9.5 | 100K | 65536/32 | 230.066 | 132.764 | 此查询工作负载 |

原文泛称 Iris Xe/Arc 平台，没有给这两行完整 CPU/GPU SKU、功耗、warmup、采样数量和 ROS 包含范围，因此只能保留厂商表值，不能归因到 Core Ultra 358H，也不能与其他厂商的导航 benchmark 排名。PCL 与 FLANN 文档的 APT 示例还指向 wheeljack 内部域并使用 trusted=yes，与公开安装指南的源及签名配置不同。这是公开供货和文档一致性的证据缺口；本研究未访问内部源或执行该配置。[[Intel02D_FLANN]] [[Intel02D_PCL]]

## 定位、地图和规划不能各自替代闭环

ORB GPU 提供 Level Zero 与 C-for-Metal kernel，分 OpenCV 和 OpenCV-free 实现；同一个对象接多相机须相同分辨率，不同尺寸需不同对象。教程里的 host time 示例缺完整硬件和统计定义，本文不据此排名。Collaborative SLAM 的双机器人和多相机教程实际以录制 bag 回放；多相机部分将独立 tracker 的 pose 做 Kalman 松耦合融合，并说明其他部分尚未 ready。更明确的适配限制是 AVX2 与 GPU Level Zero 包的 IMU 功能存在问题，使用 IMU 时教程要求 SSE-only 版本；bag 也缺 use_odom 所需话题。GPU 使用率图仅说明使用设备，不能证明精度、完整 IMU 融合或并发机队可靠性。[[Intel02D_ORB]] [[Intel02D_CollabSLAM]]

FastMapping 文档解释 Morton 索引、chunked memory pool、projective mapping、bfusion 与 MapManager，通过深度、CameraInfo 和 TF 产生地图；16UC1 深度用毫米，32FC1 用米。复用 depth_info 的多相机要求相同光学分辨率和内参，错误单位或 TF 会把快速建图变成快速生成错误障碍。GroundFloor 输入深度或 LiDAR 点云，输出 labeled_points 和 obstacle_points，LiDAR 需要 remap `/input/points`。标签到 costmap 的层配置、地图新鲜度和真实障碍漏检还需另测，分类为地面不代表可通行安全认证。[[Intel02D_FastMap]] [[Intel02D_GroundFloor]]

ITS 的 PRM/DRM 路网、双向搜索和轨迹平滑降低重复全图搜索成本；源码 configure 读取 costmap 与 global frame，createPlan 锁 costmap、生成或读取 road_map.txt，校验 start/goal 后返回 Path；越界、占障碍或未找到路径时返回空路径。当前 Jazzy 签名接收取消回调但实现中未使用，取消时效需要单独验收。build_road_map_once 与持久路网意味着必须管理地图变化后的失效条件，文档明确不支持 continuous replanning。厂商二十至三十倍针对一千节点地图的规划比较，不是任务成功率；expected_planner_frequency=20 是配置，不能写成实测二十赫兹导航。[[Intel02D_ITS]] [[Intel02D_ITS_Code]]

重定位示例在 Gazebo 中临时禁用传感器再恢复，适合测试流程入口，缺现场恢复时延、失败分母和危险响应证据。机制比较上，Intel 的 PCL/FLANN oneAPI 可迁移标准点云与查询资产，Nav2 插件可保留 ROS action/path 契约；迁移到 CUDA 空间计算或其他厂商节点时需重做 kernel、buffer、设备同步和消息桥接验证，不能认为同话题名使零拷贝自然成立。放行建议是在同一 rosbag、地图和目标机上测检测精度、建图误差、规划时间、观测年龄与整机任务结果，并注入单相机断流、NaN 点云、DDS 不兼容、路网陈旧及取消请求。代码文件有 Apache-2.0 标识，第三方库、bag 数据、模型与底盘 SDK 仍分别核许可。[[Intel02D_Relocalize]] [[Intel02D_ImageSync]]
