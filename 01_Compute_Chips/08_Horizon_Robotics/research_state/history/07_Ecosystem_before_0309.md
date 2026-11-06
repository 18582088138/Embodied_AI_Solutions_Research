# 地平线 / 地瓜机器人 D-Robotics — 生态建设

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 文档与开发
RDK 官方公开文档仓库包含硬件、CAN、TROS 和零拷贝教程；可追溯程度高于仅有发布新闻的候选平台。[horizon-s100-doc](#horizon-s100-doc)[horizon-can](#horizon-can)[horizon-tros-doc](#horizon-tros-doc)
### 国产生态与量产
机器人业务主体和汽车业务线应分别评价；不能用征程汽车装机量代替 RDK 机器人份额。自主可控仍需核查 Arm IP、制造、存储和运行时组件。
缺口：正式量产 SOM 生命周期、批量价格、驱动器/传感器合作矩阵和指定客户验收数据。可先以公开工具完成集成 PoC，再确认产业供货。

## 联动报告

- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../../05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md)
- [04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md](../../04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md)
- [02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md](../../02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="horizon-s100-doc"></a> **horizon-s100-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs_s/01_Quick_start/01_hardware_introduction/01_rdk_s100.md)｜[本地归档](../../_Evidence/horizon-s100-doc.txt)｜抓取UTC日期 2026-11-03。
- <a id="horizon-can"></a> **horizon-can**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/07_Advanced_development/01_hardware_development/rdk_x5/can.md)｜[本地归档](../../_Evidence/horizon-can.txt)｜抓取UTC日期 2026-11-03。
- <a id="horizon-tros-doc"></a> **horizon-tros-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/tros.md)｜[本地归档](../../_Evidence/horizon-tros-doc.txt)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
