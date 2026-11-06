# 地平线 / 地瓜机器人 D-Robotics — 传感器接入

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 接口证据
RDK X5 文档给出两路 MIPI CSI 相机、USB/千兆以太网及摄像头配置；S100 文档包含相机扩展板与丰富 I/O。[horizon-x5-doc](#horizon-x5-doc)[horizon-s100-doc](#horizon-s100-doc)
### 时间同步与低拷贝
TROS 进程间零拷贝优化消息传输，并不自动让不同设备同一时钟采样。相机曝光、IMU 时钟、LiDAR 扫描和 BPU 预处理仍需同步/标定。[horizon-zerocopy](#horizon-zerocopy)
可用 USB/网络传感器需额外检查驱动 ARM64、内核与 Runtime；本轮未得到 Orbbec/RoboSense 所有型号在 S100 上的官方测试矩阵。
缺口：GMSL2 解串支持、ISP 精确配置、硬件触发/PTP 和多传感器满载误差。

## 联动报告

- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../../05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md)
- [04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md](../../04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md)
- [02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md](../../02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="horizon-x5-doc"></a> **horizon-x5-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/01_Quick_start/hardware_introduction/rdk_x5.md)｜[本地归档](../../_Evidence/horizon-x5-doc.txt)｜抓取UTC日期 2026-11-03。
- <a id="horizon-s100-doc"></a> **horizon-s100-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs_s/01_Quick_start/01_hardware_introduction/01_rdk_s100.md)｜[本地归档](../../_Evidence/horizon-s100-doc.txt)｜抓取UTC日期 2026-11-03。
- <a id="horizon-zerocopy"></a> **horizon-zerocopy**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/05_tros_dev/zero_copy.md)｜[本地归档](../../_Evidence/horizon-zerocopy.txt)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
