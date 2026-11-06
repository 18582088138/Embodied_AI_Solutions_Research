# 全栈开发与云：华为云、Microsoft Azure — 架构与通信机制

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 华为云
ModelArts官方产品描述确认AI开发/训练/部署管理路线；此次附件所指“具身智能云服务”专属入口404，未取得正式产品名/版本/机器人API，不能把ModelArts通用AI能力全部当具身专属套件。[huawei-cloudmodelarts](#huawei-cloudmodelarts)
### Microsoft Azure
IoT Hub负责设备消息/管理，Digital Twins提供数字孪生建模服务；后者不是接触物理仿真引擎。两者可以成为机器人云后台组件，但并不证明存在统一、现行“Azure Robotics”产品。[azure-iot](#azure-iot)[azure-digitaltwins](#azure-digitaltwins)
### 时延边界
云网络不能无条件保证微秒级实时控制。适合训练、遥测、任务下发、远程协助和模型更新；本地执行器闭环需保持独立保护、断网可控和动作超时。

## 联动报告

- [01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md](../../01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md)
- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../18_Robot_Operating_Systems/01_Architecture_and_Communication.md)
- [04_AI_Models/17_Closed_Source_Models/05_Ecosystem_and_Fine_tuning.md](../../04_AI_Models/17_Closed_Source_Models/05_Ecosystem_and_Fine_tuning.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="huawei-cloudmodelarts"></a> **huawei-cloudmodelarts**：[官方/作者原文](https://support.huaweicloud.com/intl/en-us/productdesc-modelarts/modelarts_01_0001.html)｜[本地归档](REFERENCES.md#legacy-a4a721ba59b280fc)｜抓取UTC日期 2026-11-03。
- <a id="azure-iot"></a> **azure-iot**：[官方/作者原文](https://learn.microsoft.com/en-us/azure/iot-hub/about-iot-hub)｜[本地归档](REFERENCES.md#legacy-134c34a2ceb1644d)｜抓取UTC日期 2026-11-03。
- <a id="azure-digitaltwins"></a> **azure-digitaltwins**：[官方/作者原文](https://learn.microsoft.com/en-us/azure/digital-twins/overview)｜[本地归档](REFERENCES.md#legacy-f5cb89d4772f3d3b)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
