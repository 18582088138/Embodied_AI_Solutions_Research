# 地平线 / 地瓜机器人 D-Robotics — 机器人本体适配

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 硬件协同价值
S100 将应用核、BPU 与 R52+ MCU 域放在同一平台，并提供控制域扩展接口，可减少某些双板系统的互连复杂度；这是硬件设计判断，不是量产整机成本实测。[horizon-s100-doc](#horizon-s100-doc)
### 控制与安全
任务规划/感知可在主域、控制可在 MCU 域设计；须验证域间 IPC、时钟、实时操作系统、控制周期、独立急停和安全边界。DCLS/Split-Lock 设计不自动赋予整机安全等级。
本轮未核实指定整机在何型号上运行何 VLA，也未确认官方逆运动学、全身轨迹或顺应控制的完整组合。

## 联动报告

- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../../05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md)
- [04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md](../../04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md)
- [02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md](../../02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="horizon-s100-doc"></a> **horizon-s100-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs_s/01_Quick_start/01_hardware_introduction/01_rdk_s100.md)｜[本地归档](../../_Evidence/horizon-s100-doc.txt)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
