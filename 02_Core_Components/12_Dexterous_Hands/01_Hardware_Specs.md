# 灵巧手与微型传动：兆威机电、因时机器人、强脑科技 — 硬件规格

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 兆威机电
官方微型传动站点提供产品/生产信息入口，但本轮未取得指定灵巧手型号的数据手册。微型齿轮箱、驱动总成与整手是不同交付层级，暂不填独立自由度、力传感和整手负载。[zhaowei](#zhaowei)
### 因时机器人
RH56DFX-2L/2R 官方规格：6 自由度、12 手指关节、540g、24V±10%、RS485、重复定位 ±0.20mm、抓握力分辨率 0.50N、拇指最大抓握力 15N、四指 10N；带腕 DFXW 版本为 6+2 自由度、650g。不能把 12 关节数写成 12 独立驱动自由度。[inspire-rh56](#inspire-rh56)
### 强脑科技
官网列 Revo1/Revo2/Revo3 仿生灵巧手及脑机接口/仿生肢体产品；本轮 Revo2 页面返回相同动态页面内容，未取得可读整手参数。[brainco](#brainco)[brainco-revo2](#brainco-revo2)
跨产品比较需额外记录反驱性、指尖力、速度、重复性、触觉覆盖、寿命、指尖可换性与防护，而非只比关节数。

## 联动报告

- [04_AI_Models/16_Domestic_Open_Source_Models/02_Multimodal_Capabilities.md](../../04_AI_Models/16_Domestic_Open_Source_Models/02_Multimodal_Capabilities.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="zhaowei"></a> **zhaowei**：[官方/作者原文](https://www.zwgearbox.com/)｜[本地归档](REFERENCES.md#legacy-12d134da176b0264)｜抓取UTC日期 2026-11-03。
- <a id="inspire-rh56"></a> **inspire-rh56**：[官方/作者原文](https://www.inspire-robots.com/dexterous%20hands/rh56dfx-series/)｜[本地归档](REFERENCES.md#legacy-048caa50510225b7)｜抓取UTC日期 2026-11-03。
- <a id="brainco"></a> **brainco**：[官方/作者原文](https://www.brainco.tech/)｜[本地归档](REFERENCES.md#legacy-d0371d5f125e2103)｜抓取UTC日期 2026-11-03。
- <a id="brainco-revo2"></a> **brainco-revo2**：[官方/作者原文](https://www.brainco.tech/zh-CN/products/revo2)｜[本地归档](REFERENCES.md#legacy-4ef6ef4436dffd7a)｜抓取UTC日期 2026-11-03；仅主体/导航级证据。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
