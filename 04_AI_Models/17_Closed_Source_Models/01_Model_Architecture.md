# 闭源模型：Helix、Gemini Robotics — 模型架构

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### Helix：明确限定初代发布
Figure官方初代Helix文章披露双系统：System2约7B VLM负责语义/场景、7–9Hz；System1约80M视觉动作transformer、200Hz，输出35DoF上半身相关控制。不能将该架构/频率直接继承到后续同名版本。[helix](#helix)
### Gemini Robotics：VLA与ER分开
2025技术报告基于Gemini2.0，分别介绍直接控制机器人动作的Gemini Robotics与空间/时序推理的Gemini Robotics-ER。ER的代码/轨迹推理不能当作高频VLA策略；总参数、全部骨干与训练配方未公开。[gemini-paper](#gemini-paper)
### 版本要求
本轮未完整覆盖两家2026所有后续版本，不声称以上是截至2026-11-03的最终最新版。闭源模型需记录服务名称、发布日期、API/端侧交付方式与具体合同版本。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md](../../01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/05_SWOT_Analysis.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/05_SWOT_Analysis.md)
- [05_Software_and_OS/20_Full_Stack_Cloud_Platforms/03_AI_Model_Integration.md](../../05_Software_and_OS/20_Full_Stack_Cloud_Platforms/03_AI_Model_Integration.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="helix"></a> **helix**：[官方/作者原文](https://www.figure.ai/news/helix)｜[本地归档](REFERENCES.md#legacy-54a85d2ae7b0a4d8)｜抓取UTC日期 2026-11-03。
- <a id="gemini-paper"></a> **gemini-paper**：[官方/作者原文](https://arxiv.org/html/2503.20020v1)｜[本地归档](REFERENCES.md#legacy-b41ca8130e23b33e)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
