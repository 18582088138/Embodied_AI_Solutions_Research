# 全栈开发与云：华为云、Microsoft Azure — SWOT 分析

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 华为云
优势：通用AI开发服务可支持国内训练/模型管理路线；短板：本轮具身专属产品定义、端侧兼容和服务成本证据不足。[huawei-cloudmodelarts](#huawei-cloudmodelarts)
### Azure
优势：设备消息和数字孪生服务文档清晰；短板：机器人控制、VLA、传感器/执行器适配需自行集成，不能将通用服务组合命名为现成Azure Robotics套件。[azure-iot](#azure-iot)[azure-digitaltwins](#azure-digitaltwins)
### 适用场景
适合训练/数据/任务/遥测后台。低时延现场控制由端侧承担，跨区域数据传输、网络故障、费用、服务生命周期和退出迁移需项目评估。
本轮没有同任务云成本、SLA或量产客户验收数据；不做价格排名或平台成熟度打分。

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
