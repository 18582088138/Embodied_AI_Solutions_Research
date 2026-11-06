# 闭源模型：Helix、Gemini Robotics — 生态与微调

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### Helix
初代发布说明使用开放骨干，但整体策略、训练数据和端侧系统并未作为通用可下载开源产品发布。开放上游VLM不能把整体Helix改判为开放模型。[helix](#helix)
### Gemini Robotics
论文提供技术/基准研究线索，核心策略仍需合作/服务权限；第三方微调、数据保留、授权范围和端侧运行须核验现行条款。[gemini-paper](#gemini-paper)
### 商业与生态取舍
潜在优点是模型与本体协同优化、减少第三方自行搭建；代价是接口/数据/硬件/版本依赖以及复现受限。微调是否开放、算力成本、数据所有权、SLA与退出迁移路径需要合同级证据。
本轮不提供未经核实的商业报价、开放申请资格或2026最新服务承诺。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md](../../01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/05_SWOT_Analysis.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/05_SWOT_Analysis.md)
- [05_Software_and_OS/20_Full_Stack_Cloud_Platforms/03_AI_Model_Integration.md](../../05_Software_and_OS/20_Full_Stack_Cloud_Platforms/03_AI_Model_Integration.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="helix"></a> **helix**：[官方/作者原文](https://www.figure.ai/news/helix)｜[本地归档](REFERENCES.md#legacy-54a85d2ae7b0a4d8)｜抓取UTC日期 2026-11-03。
- <a id="gemini-paper"></a> **gemini-paper**：[官方/作者原文](https://arxiv.org/html/2503.20020v1)｜[本地归档](REFERENCES.md#legacy-b41ca8130e23b33e)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
