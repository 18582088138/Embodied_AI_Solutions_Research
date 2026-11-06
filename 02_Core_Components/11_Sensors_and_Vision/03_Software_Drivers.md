# 传感器与视觉：奥比中光、柯力传感、速腾聚创 — 软件驱动

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 奥比中光：直接证据较强
Orbbec SDK v2 列 Linux x64（Ubuntu 20.04/22.04/24.04）、ARM64（Jetson Orin 系列及 Thor）测试平台；公开 ROS 2 wrapper 有相机、点云和配置参数，SDK 主体采用 MIT 并包含第三方许可。[orbbec-sdk](#orbbec-sdk)[orbbec-ros2](#orbbec-ros2)
“ARM64”不等于所有国产 SoC 已验证；RK/S100/昇腾主机须检查 BSP、USB、固件和版本。ROS 2 wrapper 与某发行版编译成功也不能替代稳定性验收。
### 柯力传感
未找到本轮可验证的 ROS 2 SDK、公开 API 和固件支持矩阵。应索取采集器协议、时间戳、滤波、单位、坐标系与零漂校准工具。
### 速腾聚创
RoboSense 官方 rslidar_sdk README 明确 ROS 2、colcon、点云消息以及 Humble 帧率问题的排查路径。列表还包含旧发行版，应选当前维护版本，而非照抄旧命令。[robosense-driver](#robosense-driver)
AC1 需要单独核验其 SDK/API 与所有算法下载状态。[robosense-ac1](#robosense-ac1)

## 联动报告

- [01_Compute_Chips/01_NVIDIA/03_Sensor_Integration.md](../../01_Compute_Chips/01_NVIDIA/03_Sensor_Integration.md)
- [01_Compute_Chips/02_Intel/03_Sensor_Integration.md](../../01_Compute_Chips/02_Intel/03_Sensor_Integration.md)
- [01_Compute_Chips/05_Rockchip/03_Sensor_Integration.md](../../01_Compute_Chips/05_Rockchip/03_Sensor_Integration.md)
- [05_Software_and_OS/18_Robot_Operating_Systems/02_Hardware_Abstraction.md](../../05_Software_and_OS/18_Robot_Operating_Systems/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="orbbec-sdk"></a> **orbbec-sdk**：[官方/作者原文](https://raw.githubusercontent.com/orbbec/OrbbecSDK_v2/main/README.md)｜[本地归档](REFERENCES.md#legacy-15e3eb17ad4d0050)｜抓取UTC日期 2026-11-03。
- <a id="orbbec-ros2"></a> **orbbec-ros2**：[官方/作者原文](https://raw.githubusercontent.com/orbbec/OrbbecSDK_ROS2/main/README.MD)｜[本地归档](REFERENCES.md#legacy-d2cf2aa00788ad77)｜抓取UTC日期 2026-11-03。
- <a id="robosense-driver"></a> **robosense-driver**：[官方/作者原文](https://raw.githubusercontent.com/RoboSense-LiDAR/rslidar_sdk/main/README.md)｜[本地归档](REFERENCES.md#legacy-7209d0e0feff9f35)｜抓取UTC日期 2026-11-03。
- <a id="robosense-ac1"></a> **robosense-ac1**：[官方/作者原文](https://www.robosense.ai/en/IncrementalComponents/AC1)｜[本地归档](REFERENCES.md#legacy-16d6f04426aed7a1)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
