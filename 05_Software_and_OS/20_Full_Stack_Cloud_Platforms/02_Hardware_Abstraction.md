# 全栈开发与云：华为云、Microsoft Azure — 硬件抽象与兼容性

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 华为云
ModelArts云端服务与CANN/端侧BSP是不同层；云训练资源支持不能自动证明NV、RK、昇腾机器人板的模型/驱动兼容。[huawei-cloudmodelarts](#huawei-cloudmodelarts)[huawei-cann](#huawei-cann)
### Azure
IoT Hub提供设备连接/消息接口，并不自带所有相机、关节和NPU驱动。Digital Twins描述实体关系，不能替代硬件抽象或物理模型。[azure-iot](#azure-iot)[azure-digitaltwins](#azure-digitaltwins)
### 系统职责
本地ROS/API适配传感器与执行器，边端agent完成身份、缓冲与模型更新，云端管理数据/任务。每种芯片的模型格式、量化和硬件驱动需独立核验。
未取得两家统一的国产零部件驱动列表、全栈机器人SOM兼容表或最新专属机器人服务生命周期。

## 联动报告

- [01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md](../../01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md)
- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../18_Robot_Operating_Systems/01_Architecture_and_Communication.md)
- [04_AI_Models/17_Closed_Source_Models/05_Ecosystem_and_Fine_tuning.md](../../04_AI_Models/17_Closed_Source_Models/05_Ecosystem_and_Fine_tuning.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="huawei-cloudmodelarts"></a> **huawei-cloudmodelarts**：[官方/作者原文](https://support.huaweicloud.com/intl/en-us/productdesc-modelarts/modelarts_01_0001.html)｜[本地归档](REFERENCES.md#legacy-a4a721ba59b280fc)｜抓取UTC日期 2026-11-03。
- <a id="huawei-cann"></a> **huawei-cann**：[官方/作者原文](https://www.hiascend.com/software/cann)｜[本地归档](REFERENCES.md#legacy-50125edc4810d8b2)｜抓取UTC日期 2026-11-03；仅主体/导航级证据。
- <a id="azure-iot"></a> **azure-iot**：[官方/作者原文](https://learn.microsoft.com/en-us/azure/iot-hub/about-iot-hub)｜[本地归档](REFERENCES.md#legacy-134c34a2ceb1644d)｜抓取UTC日期 2026-11-03。
- <a id="azure-digitaltwins"></a> **azure-digitaltwins**：[官方/作者原文](https://learn.microsoft.com/en-us/azure/digital-twins/overview)｜[本地归档](REFERENCES.md#legacy-f5cb89d4772f3d3b)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
