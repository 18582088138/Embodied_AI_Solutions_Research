# 传感器与视觉：奥比中光、柯力传感、速腾聚创 — 接口与通信

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 奥比中光
Gemini 335 是 USB3 Type-C 供电/数据、支持触发与 IMU；335Lg/Le 等变体不能继承 335 的连接规格，应独立核验。多设备同步需使用正确固件、触发连接与 SDK 时间策略。[orbbec-gemini335](#orbbec-gemini335)[orbbec-timestamp](#orbbec-timestamp)
### 柯力传感
力传感器可能包含原始模拟信号、采集板或数字接口，必须按交付 SKU 确认；本轮未验证 EtherCAT/CAN-FD 版本，暂不写支持。
### 速腾聚创
rslidar_sdk 支持点云接收与 ROS/ROS 2 路线，但该包的传统 LiDAR 支持范围不能自动涵盖新 AC1。AC1 官网页介绍 AC Studio/Viewer 和同步融合生态，具体接口与驱动另行索取。[robosense-driver](#robosense-driver)[robosense-ac1](#robosense-ac1)
### 算力协同
检查 USB 带宽、网口 MTU/多播、PTP、GMSL 解串、DMA 与共享 Hub；按采样时刻同步，主机收到消息的时间不足以支撑动态融合。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/03_Sensor_Integration.md](../../01_Compute_Chips/01_NVIDIA/03_Sensor_Integration.md)
- [01_Compute_Chips/02_Intel/03_Sensor_Integration.md](../../01_Compute_Chips/02_Intel/03_Sensor_Integration.md)
- [01_Compute_Chips/05_Rockchip/03_Sensor_Integration.md](../../01_Compute_Chips/05_Rockchip/03_Sensor_Integration.md)
- [05_Software_and_OS/18_Robot_Operating_Systems/02_Hardware_Abstraction.md](../../05_Software_and_OS/18_Robot_Operating_Systems/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="orbbec-gemini335"></a> **orbbec-gemini335**：[官方/作者原文](https://www.orbbec.com/products/stereo-vision-camera/gemini-335/)｜[本地归档](REFERENCES.md#legacy-75ab3e6053df8d2a)｜抓取UTC日期 2026-11-03。
- <a id="orbbec-timestamp"></a> **orbbec-timestamp**：[官方/作者原文](https://raw.githubusercontent.com/orbbec/OrbbecSDK_v2/main/docs/tutorial/timestamp.md)｜[本地归档](REFERENCES.md#legacy-45721b25506da462)｜抓取UTC日期 2026-11-03。
- <a id="robosense-driver"></a> **robosense-driver**：[官方/作者原文](https://raw.githubusercontent.com/RoboSense-LiDAR/rslidar_sdk/main/README.md)｜[本地归档](REFERENCES.md#legacy-7209d0e0feff9f35)｜抓取UTC日期 2026-11-03。
- <a id="robosense-ac1"></a> **robosense-ac1**：[官方/作者原文](https://www.robosense.ai/en/IncrementalComponents/AC1)｜[本地归档](REFERENCES.md#legacy-16d6f04426aed7a1)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
