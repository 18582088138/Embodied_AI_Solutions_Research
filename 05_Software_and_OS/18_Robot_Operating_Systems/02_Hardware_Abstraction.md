# 机器人操作系统：ROS 2、AGIROS、智元灵渠 — 硬件抽象与兼容性

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### ROS 2的真实兼容层
支持ARM64/x86并不意味着所有芯片NPU或外设已有驱动。硬件抽象需对应设备API、状态/命令接口、时间戳、单位和故障机制。[ros-release-rst](#ros-release-rst)
### 零部件核验
奥比中光提供官方ROS2 wrapper；RoboSense提供rslidar_sdk/ROS2，但新版AC1需单独核验。绿的谐波纯机械减速器不应寻找“减速器ROS驱动”；驱动对象是电机/控制器/一体化关节。[orbbec-ros2](#orbbec-ros2)[robosense-driver](#robosense-driver)
因时RH56DFX使用RS485，仍需协议wrapper；柯力、汇川、鸣志与强脑的本轮厂商ROS2驱动未验证。[inspire-rh56](#inspire-rh56)
### 国产芯片与其他OS
RDK的TROS/hobot dnn有直接证据；RKNN/CANN属于AI计算接口，不能当整个ROS硬件层。AGIROS/灵渠对NV、RK、昇腾的完整兼容矩阵未确认。[horizon-tros-doc](#horizon-tros-doc)[rk-rknn](#rk-rknn)[huawei-cann](#huawei-cann)

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

- <a id="ros-release-rst"></a> **ros-release-rst**：[官方/作者原文](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Releases/Release-Jazzy-Jalisco.rst)｜[本地归档](REFERENCES.md#legacy-750d3b1f468ea2e5)｜抓取UTC日期 2026-11-03。
- <a id="orbbec-ros2"></a> **orbbec-ros2**：[官方/作者原文](https://raw.githubusercontent.com/orbbec/OrbbecSDK_ROS2/main/README.MD)｜[本地归档](REFERENCES.md#legacy-d2cf2aa00788ad77)｜抓取UTC日期 2026-11-03。
- <a id="robosense-driver"></a> **robosense-driver**：[官方/作者原文](https://raw.githubusercontent.com/RoboSense-LiDAR/rslidar_sdk/main/README.md)｜[本地归档](REFERENCES.md#legacy-7209d0e0feff9f35)｜抓取UTC日期 2026-11-03。
- <a id="inspire-rh56"></a> **inspire-rh56**：[官方/作者原文](https://www.inspire-robots.com/dexterous%20hands/rh56dfx-series/)｜[本地归档](REFERENCES.md#legacy-048caa50510225b7)｜抓取UTC日期 2026-11-03。
- <a id="horizon-tros-doc"></a> **horizon-tros-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/tros.md)｜[本地归档](REFERENCES.md#legacy-2374b38a6f876a21)｜抓取UTC日期 2026-11-03。
- <a id="rk-rknn"></a> **rk-rknn**：[官方/作者原文](https://raw.githubusercontent.com/airockchip/rknn-toolkit2/master/README.md)｜[本地归档](REFERENCES.md#legacy-25a303718864388d)｜抓取UTC日期 2026-11-03。
- <a id="huawei-cann"></a> **huawei-cann**：[官方/作者原文](https://www.hiascend.com/software/cann)｜[本地归档](REFERENCES.md#legacy-50125edc4810d8b2)｜抓取UTC日期 2026-11-03；仅主体/导航级证据。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
