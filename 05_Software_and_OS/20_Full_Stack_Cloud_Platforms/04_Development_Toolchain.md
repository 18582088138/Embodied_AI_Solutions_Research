# 全栈开发与云：华为云、Microsoft Azure — 开发工具链

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 华为云
ModelArts提供AI开发服务入口，具体数据管理、标注、训练资源、部署与计费按现行版本/区域确认；不能把通用功能写成完整机器人低代码工具。[huawei-cloudmodelarts](#huawei-cloudmodelarts)
### Azure
IoT Hub设备连接和Digital Twins建模可服务遥测/资产关系；VLA数据录制、动作标注、机器人仿真和硬件调试需另配工具。[azure-iot](#azure-iot)[azure-digitaltwins](#azure-digitaltwins)
### 端云数据链
建议记录多相机、IMU、力、关节状态、动作、时间戳、模型/固件版本与事件日志，结合LeRobot等schema进行回放和微调。[lerobot](#lerobot)
未进行云部署或计费实测；区域支持、服务配额、SLA和低代码产品状态待官方文档核验。

## 联动报告

- [01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md](../../01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md)
- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../18_Robot_Operating_Systems/01_Architecture_and_Communication.md)
- [04_AI_Models/17_Closed_Source_Models/05_Ecosystem_and_Fine_tuning.md](../../04_AI_Models/17_Closed_Source_Models/05_Ecosystem_and_Fine_tuning.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="huawei-cloudmodelarts"></a> **huawei-cloudmodelarts**：[官方/作者原文](https://support.huaweicloud.com/intl/en-us/productdesc-modelarts/modelarts_01_0001.html)｜[本地归档](REFERENCES.md#legacy-a4a721ba59b280fc)｜抓取UTC日期 2026-11-03。
- <a id="azure-iot"></a> **azure-iot**：[官方/作者原文](https://learn.microsoft.com/en-us/azure/iot-hub/about-iot-hub)｜[本地归档](REFERENCES.md#legacy-134c34a2ceb1644d)｜抓取UTC日期 2026-11-03。
- <a id="azure-digitaltwins"></a> **azure-digitaltwins**：[官方/作者原文](https://learn.microsoft.com/en-us/azure/digital-twins/overview)｜[本地归档](REFERENCES.md#legacy-f5cb89d4772f3d3b)｜抓取UTC日期 2026-11-03。
- <a id="lerobot"></a> **lerobot**：[官方/作者原文](https://raw.githubusercontent.com/huggingface/lerobot/main/README.md)｜[本地归档](REFERENCES.md#legacy-cdde66013990b290)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
