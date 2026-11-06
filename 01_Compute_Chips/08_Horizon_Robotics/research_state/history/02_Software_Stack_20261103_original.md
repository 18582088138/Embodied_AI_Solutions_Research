# 地平线 / 地瓜机器人 D-Robotics — 软件栈

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### TROS 与 BPU
TogetheROS.Bot 基于 ROS 2 Foxy/Humble 通信核心扩展，提供 hobot dnn 推理封装、进程间零拷贝等；x86 模拟器只能体验部分图片回灌功能，并不模拟完整硬件。[horizon-tros-doc](#horizon-tros-doc)[horizon-zerocopy](#horizon-zerocopy)
### 工业通信与部署
RDK X5 官方 CAN 文档描述 CAN 使用与配置；X5 硬件文档列 CAN FD 接口。S100 提供独立 MCU 域及扩展 CAN 引脚，但控制域引脚有无不代表载板已包含全部收发器。[horizon-can](#horizon-can)[horizon-x5-doc](#horizon-x5-doc)[horizon-s100-doc](#horizon-s100-doc)
BPU 模型须匹配编译器/Runtime、量化与算子支持。EtherCAT 主站及 AGIROS 集成尚未核实，不由网口或 ROS 2 支持推导。

## 联动报告

- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../../05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md)
- [04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md](../../04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md)
- [02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md](../../02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="horizon-tros-doc"></a> **horizon-tros-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/tros.md)｜[本地归档](../../_Evidence/horizon-tros-doc.txt)｜抓取UTC日期 2026-11-03。
- <a id="horizon-zerocopy"></a> **horizon-zerocopy**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/05_tros_dev/zero_copy.md)｜[本地归档](../../_Evidence/horizon-zerocopy.txt)｜抓取UTC日期 2026-11-03。
- <a id="horizon-can"></a> **horizon-can**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/07_Advanced_development/01_hardware_development/rdk_x5/can.md)｜[本地归档](../../_Evidence/horizon-can.txt)｜抓取UTC日期 2026-11-03。
- <a id="horizon-x5-doc"></a> **horizon-x5-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/01_Quick_start/hardware_introduction/rdk_x5.md)｜[本地归档](../../_Evidence/horizon-x5-doc.txt)｜抓取UTC日期 2026-11-03。
- <a id="horizon-s100-doc"></a> **horizon-s100-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs_s/01_Quick_start/01_hardware_introduction/01_rdk_s100.md)｜[本地归档](../../_Evidence/horizon-s100-doc.txt)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
