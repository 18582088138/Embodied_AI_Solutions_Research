# 闭源模型：Helix、Gemini Robotics — 仿真到现实迁移

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### Helix
初代官方披露约500小时遥操作数据、训练集物体与测试物体分开、上半身操作与协作演示。文章中的“可处理大量新物体”是厂商实验说明；未提供本轮可复现的统一任务成功/总次数，不能与开放模型榜单直接比较。[helix](#helix)
### Gemini Robotics
论文展示跨物体/环境/指令泛化、少至100条示范的部分新任务适配和新本体迁移。100条不是任意任务的保证；ER零样本代码生成与VLA少样本执行是不同实验。[gemini-paper](#gemini-paper)
### 验证要求
应取得相同任务协议、演示数据、人工接管、故障恢复、长期稳定性与更新回归。闭源系统需要黑盒验收/可审计日志，公开视频无法代替采购现场测试。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md](../../01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/05_SWOT_Analysis.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/05_SWOT_Analysis.md)
- [05_Software_and_OS/20_Full_Stack_Cloud_Platforms/03_AI_Model_Integration.md](../../05_Software_and_OS/20_Full_Stack_Cloud_Platforms/03_AI_Model_Integration.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="helix"></a> **helix**：[官方/作者原文](https://www.figure.ai/news/helix)｜[本地归档](REFERENCES.md#legacy-54a85d2ae7b0a4d8)｜抓取UTC日期 2026-11-03。
- <a id="gemini-paper"></a> **gemini-paper**：[官方/作者原文](https://arxiv.org/html/2503.20020v1)｜[本地归档](REFERENCES.md#legacy-b41ca8130e23b33e)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
