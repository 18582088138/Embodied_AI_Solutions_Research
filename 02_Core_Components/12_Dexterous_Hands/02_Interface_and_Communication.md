# 灵巧手与微型传动：兆威机电、因时机器人、强脑科技 — 接口与通信

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 兆威机电
若交付齿轮箱/微型传动，接口是机械与电机；若交付整手，需单独获得控制器和协议。本轮未验证 EtherCAT/CAN-FD 或 ROS 对接。[zhaowei](#zhaowei)
### 因时机器人
RH56DFX 官方列 RS485，不是 Ethernet/CAN-FD。可经主机 USB-RS485/串口或工业网关接入；帧协议、寻址、同步与校验须从手册核验。不能将其他系列通信能力继承给 DFX。[inspire-rh56](#inspire-rh56)
### 强脑科技
Revo 系列控制器、总线、电源与触觉通道尚未获取规格；不能因其脑机接口业务推断机器人手一定采用某种 EEG/EMG 控制或已支持 EtherCAT。[brainco](#brainco)
### 算力协同
端侧 VLA 动作维度与手的独立控制轴需映射，主机/网关测量请求—反馈时延；通信速率、动作更新频率、内部伺服频率分别记录。

## 联动报告

- [04_AI_Models/16_Domestic_Open_Source_Models/02_Multimodal_Capabilities.md](../../04_AI_Models/16_Domestic_Open_Source_Models/02_Multimodal_Capabilities.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="zhaowei"></a> **zhaowei**：[官方/作者原文](https://www.zwgearbox.com/)｜[本地归档](REFERENCES.md#legacy-12d134da176b0264)｜抓取UTC日期 2026-11-03。
- <a id="inspire-rh56"></a> **inspire-rh56**：[官方/作者原文](https://www.inspire-robots.com/dexterous%20hands/rh56dfx-series/)｜[本地归档](REFERENCES.md#legacy-048caa50510225b7)｜抓取UTC日期 2026-11-03。
- <a id="brainco"></a> **brainco**：[官方/作者原文](https://www.brainco.tech/)｜[本地归档](REFERENCES.md#legacy-d0371d5f125e2103)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
