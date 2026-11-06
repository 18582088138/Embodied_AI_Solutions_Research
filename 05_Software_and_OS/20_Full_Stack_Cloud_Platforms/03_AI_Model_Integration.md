# 全栈开发与云：华为云、Microsoft Azure — AI 模型集成

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 云端与本体分工
云可训练/托管策略或提供高层语义，本体实时层执行安全动作；远程VLA需要规定观察压缩、时间戳、action chunk有效期、队列与网络失联回退。[huawei-cloudmodelarts](#huawei-cloudmodelarts)[azure-iot](#azure-iot)
### 公开可复用机制
openpi有WebSocket远程推理；宇树VLA有model server/client。这是开源项目的远程架构证据，不是华为云/Azure提供原生产品认证。[openpi](#openpi)[unitree-unifolm](#unitree-unifolm)
### 支持范围
未取得两家“开箱即用支持OpenVLA/GO-1/Helix/Gemini Robotics”的官方全栈部署清单。闭源模型还需API访问/合同授权。
服务可部署容器、模型是否可编译、数据许可合规、端侧闭环性能需逐项确认。

## 联动报告

- [01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md](../../01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md)
- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../18_Robot_Operating_Systems/01_Architecture_and_Communication.md)
- [04_AI_Models/17_Closed_Source_Models/05_Ecosystem_and_Fine_tuning.md](../../04_AI_Models/17_Closed_Source_Models/05_Ecosystem_and_Fine_tuning.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="huawei-cloudmodelarts"></a> **huawei-cloudmodelarts**：[官方/作者原文](https://support.huaweicloud.com/intl/en-us/productdesc-modelarts/modelarts_01_0001.html)｜[本地归档](REFERENCES.md#legacy-a4a721ba59b280fc)｜抓取UTC日期 2026-11-03。
- <a id="azure-iot"></a> **azure-iot**：[官方/作者原文](https://learn.microsoft.com/en-us/azure/iot-hub/about-iot-hub)｜[本地归档](REFERENCES.md#legacy-134c34a2ceb1644d)｜抓取UTC日期 2026-11-03。
- <a id="openpi"></a> **openpi**：[官方/作者原文](https://raw.githubusercontent.com/Physical-Intelligence/openpi/main/README.md)｜[本地归档](REFERENCES.md#legacy-84ef98c9061878e4)｜抓取UTC日期 2026-11-03。
- <a id="unitree-unifolm"></a> **unitree-unifolm**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unifolm-vla/main/README.md)｜[本地归档](REFERENCES.md#legacy-b68dedabc807e98f)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
