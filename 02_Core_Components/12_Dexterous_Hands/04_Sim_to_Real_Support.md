# 灵巧手与微型传动：兆威机电、因时机器人、强脑科技 — 仿真支持

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 已核实与未核实
本轮未获得三家厂商公开的完整高保真 Isaac/MJCF 接触模型。RH56DFX 的自由度/关节数与抓握指标可帮助建模，但不能单靠这些还原欠驱动耦合、摩擦和力反馈。[inspire-rh56](#inspire-rh56)
### 分厂商建模重点
兆威：齿轮比、背隙、效率、线缆/微型传动弹性；因时：6 控制轴与12关节的耦合、RS485 延迟与力分辨；强脑：先取得 Revo 的执行器布局与触觉 API，再谈高保真。[zhaowei](#zhaowei)[brainco](#brainco)
### 效率与精度
抓取预训练可用简化指尖碰撞/耦合关节；精密插接、柔性物操作与安全接触需辨识摩擦、接触面积、指尖柔性和迟滞。在现实中测试不同材料、载荷与磨损后再给 Sim-to-Real 结论。

## 联动报告

- [04_AI_Models/16_Domestic_Open_Source_Models/02_Multimodal_Capabilities.md](../../04_AI_Models/16_Domestic_Open_Source_Models/02_Multimodal_Capabilities.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="inspire-rh56"></a> **inspire-rh56**：[官方/作者原文](https://www.inspire-robots.com/dexterous%20hands/rh56dfx-series/)｜[本地归档](REFERENCES.md#legacy-048caa50510225b7)｜抓取UTC日期 2026-11-03。
- <a id="zhaowei"></a> **zhaowei**：[官方/作者原文](https://www.zwgearbox.com/)｜[本地归档](REFERENCES.md#legacy-12d134da176b0264)｜抓取UTC日期 2026-11-03。
- <a id="brainco"></a> **brainco**：[官方/作者原文](https://www.brainco.tech/)｜[本地归档](REFERENCES.md#legacy-d0371d5f125e2103)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
