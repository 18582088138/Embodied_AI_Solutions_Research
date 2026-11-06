# 地平线 / 地瓜机器人 D-Robotics — 硬件平台

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 主体与规格
本目录保留附件中的地平线名称，机器人开发平台证据来自 D-Robotics（地瓜机器人）；不把汽车征程芯片产品线直接当作机器人 RDK。[horizon-s100-doc](#horizon-s100-doc)[horizon-tros-doc](#horizon-tros-doc)
RDK S100/S100P 文档分别列 S100E 1.5GHz、12GB LPDDR5、80 TOPS 和 S100P 2.0GHz、24GB、128 TOPS；共有六核 A78AE、四核 R52+ MCU 域、Nash BPU 与 Mali-G78AE。精度口径未在本轮概述完整注明，应索取测试定义。[horizon-s100-doc](#horizon-s100-doc)
### 功耗与形态
文档提供开发板/扩展接口并链接特定场景功耗表，本轮未下载该表，因此不估算统一 TDP。制程、存储 SKU、散热及工业温度范围待硬件手册确认。

## 联动报告

- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../../05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md)
- [04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md](../../04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md)
- [02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md](../../02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="horizon-s100-doc"></a> **horizon-s100-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs_s/01_Quick_start/01_hardware_introduction/01_rdk_s100.md)｜[本地归档](../../_Evidence/horizon-s100-doc.txt)｜抓取UTC日期 2026-11-03。
- <a id="horizon-tros-doc"></a> **horizon-tros-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/tros.md)｜[本地归档](../../_Evidence/horizon-tros-doc.txt)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
