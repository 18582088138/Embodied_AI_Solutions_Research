# 机器人操作系统：ROS 2、AGIROS、智元灵渠 — 架构与通信机制

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### ROS 2
ROS 2是机器人中间件/工具生态，需要Linux/RTOS等底层OS。RMW抽象允许DDS实现等中间件选择，QoS与通信拓扑影响时延。官方实时教程强调调度、内存锁定与避免阻塞等条件；不能把普通Ubuntu+ROS2宣称为微秒级硬实时。[ros-middleware-rst](#ros-middleware-rst)[ros-realtime-rst](#ros-realtime-rst)
Jazzy官方发布资料可核验发行版与平台生命周期；工程应锁定发行版。[ros-release-rst](#ros-release-rst)
### AGIROS、智元灵渠
本轮未获得AGIROS明确产品主体/版本和灵渠OS完整公开架构。AimRT属于智元关联的公开运行时项目，不能自动等同于灵渠全部OS实现。其仓库可以作为运行时线索，不将其性能视为灵渠正式规格。[agibot-aimrt](#agibot-aimrt)[aimrt-readme-cn](#aimrt-readme-cn)
### 补充：TROS
TROS官方基于ROS2 Foxy/Humble扩展、BPU封装和零拷贝，是具体芯片生态整合例子。[horizon-tros-doc](#horizon-tros-doc)
云边端协同需协议、网络超时、状态同步与离线运行策略，不能让云端网络波动直接决定安全关节控制。

### 本轮处理

对无法定位可靠公开资料的具微科技、AGIROS、格物，已按用户指示注明后本轮跳过；保留位置不代表已验证该产品或主体。

## 联动报告

- [02_Core_Components/10_Actuators_and_Reducers/03_Software_Drivers.md](../../02_Core_Components/10_Actuators_and_Reducers/03_Software_Drivers.md)
- [02_Core_Components/11_Sensors_and_Vision/03_Software_Drivers.md](../../02_Core_Components/11_Sensors_and_Vision/03_Software_Drivers.md)
- [02_Core_Components/12_Dexterous_Hands/03_Software_Drivers.md](../../02_Core_Components/12_Dexterous_Hands/03_Software_Drivers.md)
- [04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md](../../04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md)
- [01_Compute_Chips/08_Horizon_Robotics/02_Software_Stack.md](../../01_Compute_Chips/08_Horizon_Robotics/02_Software_Stack.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="ros-middleware-rst"></a> **ros-middleware-rst**：[官方/作者原文](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Concepts/Intermediate/About-Different-Middleware-Vendors.rst)｜[本地归档](REFERENCES.md#legacy-fccd19391452e633)｜抓取UTC日期 2026-11-03。
- <a id="ros-realtime-rst"></a> **ros-realtime-rst**：[官方/作者原文](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Tutorials/Demos/Real-Time-Programming.rst)｜[本地归档](REFERENCES.md#legacy-61efa0be808b0c40)｜抓取UTC日期 2026-11-03。
- <a id="ros-release-rst"></a> **ros-release-rst**：[官方/作者原文](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Releases/Release-Jazzy-Jalisco.rst)｜[本地归档](REFERENCES.md#legacy-750d3b1f468ea2e5)｜抓取UTC日期 2026-11-03。
- <a id="agibot-aimrt"></a> **agibot-aimrt**：[官方/作者原文](https://raw.githubusercontent.com/AimRT/AimRT/main/README.md)｜[本地归档](REFERENCES.md#legacy-c18a4a38d0f903b5)｜抓取UTC日期 2026-11-03。
- <a id="aimrt-readme-cn"></a> **aimrt-readme-cn**：[官方/作者原文](https://raw.githubusercontent.com/AimRT/AimRT/main/README.zh_CN.md)｜[本地归档](REFERENCES.md#legacy-d8e51d23b8ff5283)｜抓取UTC日期 2026-11-03。
- <a id="horizon-tros-doc"></a> **horizon-tros-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/tros.md)｜[本地归档](REFERENCES.md#legacy-2374b38a6f876a21)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
