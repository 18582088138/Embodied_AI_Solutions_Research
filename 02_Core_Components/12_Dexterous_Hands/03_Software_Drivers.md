# 灵巧手与微型传动：兆威机电、因时机器人、强脑科技 — 软件驱动

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 厂商公开证据
兆威机电：本轮未取得公开 ROS 2 API/驱动。
因时：有公开 RH56DFX 规格，但本轮未获取可验证的厂商维护 ROS 2 wrapper、寄存器/API 与固件版本文档。[inspire-rh56](#inspire-rh56)
强脑：官网有 Revo 产品线，但未抓到可读 SDK/许可。[brainco](#brainco)
### 驱动交付要求
必须索取位置/速度/力命令、反馈单位、关节耦合矩阵、左右手坐标、故障码和急停策略；ROS 2 驱动还应说明状态发布、QoS、重连与安全限幅。社区包能演示不代表厂商长期维护。
### 模型集成
VLA 需要记录绝对/相对动作、夹持量、力阈值和控制周期。将手部控制状态写入数据集，否则模型在训练与执行中的动作空间可能不一致。

## 联动报告

- [04_AI_Models/16_Domestic_Open_Source_Models/02_Multimodal_Capabilities.md](../../04_AI_Models/16_Domestic_Open_Source_Models/02_Multimodal_Capabilities.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="inspire-rh56"></a> **inspire-rh56**：[官方/作者原文](https://www.inspire-robots.com/dexterous%20hands/rh56dfx-series/)｜[本地归档](REFERENCES.md#legacy-048caa50510225b7)｜抓取UTC日期 2026-11-03。
- <a id="brainco"></a> **brainco**：[官方/作者原文](https://www.brainco.tech/)｜[本地归档](REFERENCES.md#legacy-d0371d5f125e2103)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
