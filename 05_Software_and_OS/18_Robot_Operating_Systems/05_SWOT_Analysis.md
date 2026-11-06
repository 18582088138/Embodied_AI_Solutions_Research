# 机器人操作系统：ROS 2、AGIROS、智元灵渠 — SWOT 分析

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### ROS 2
优势：开放通信抽象、跨平台资料与第三方驱动链可追溯。[ros-middleware-rst](#ros-middleware-rst)[orbbec-ros2](#orbbec-ros2)[robosense-driver](#robosense-driver)
短板：实时性、驱动与功能安全由系统集成保证，发行版/QoS/内核增加维护复杂度。适合科研与多供应商系统，但生产需建立明确的实时/故障测试。
### AGIROS、灵渠
潜在价值是本体/算力/模型整合；本轮公开产品主体、架构和接口不足，不作成熟度分数或性能排行。AimRT公开不是全部OS已开源的证明。[agibot-aimrt](#agibot-aimrt)
### TROS补充
优势是RDK/BPU/ROS组合与零拷贝文档明确，短板是专用加速器/发行版依赖及大型VLA尚需核验。[horizon-tros-doc](#horizon-tros-doc)[horizon-zerocopy](#horizon-zerocopy)
### 商业策略
开源中间件不排除驱动、部署工具或安全产品收费；许可必须按代码、数据、二进制和服务分别确认。

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
- <a id="orbbec-ros2"></a> **orbbec-ros2**：[官方/作者原文](https://raw.githubusercontent.com/orbbec/OrbbecSDK_ROS2/main/README.MD)｜[本地归档](REFERENCES.md#legacy-d2cf2aa00788ad77)｜抓取UTC日期 2026-11-03。
- <a id="robosense-driver"></a> **robosense-driver**：[官方/作者原文](https://raw.githubusercontent.com/RoboSense-LiDAR/rslidar_sdk/main/README.md)｜[本地归档](REFERENCES.md#legacy-7209d0e0feff9f35)｜抓取UTC日期 2026-11-03。
- <a id="agibot-aimrt"></a> **agibot-aimrt**：[官方/作者原文](https://raw.githubusercontent.com/AimRT/AimRT/main/README.md)｜[本地归档](REFERENCES.md#legacy-c18a4a38d0f903b5)｜抓取UTC日期 2026-11-03。
- <a id="horizon-tros-doc"></a> **horizon-tros-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/tros.md)｜[本地归档](REFERENCES.md#legacy-2374b38a6f876a21)｜抓取UTC日期 2026-11-03。
- <a id="horizon-zerocopy"></a> **horizon-zerocopy**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/05_tros_dev/zero_copy.md)｜[本地归档](REFERENCES.md#legacy-77744a5eeb0e6338)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
