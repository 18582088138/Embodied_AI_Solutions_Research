# 闭源模型：Helix、Gemini Robotics — 硬件部署与算力需求

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### Helix
官方初代文章披露双低功耗机载GPU，S1/S2分GPU运行，并以共享latent/异步架构衔接；未披露GPU厂商具体SKU、内存或瓦数。不能从“嵌入式GPU”推断必为Orin，也不能把200Hz写成7B完整模型推理频率。[helix](#helix)
### Gemini Robotics
论文不提供可供第三方自由部署的最低端侧TOPS、完整权重或所有硬件支持列表；服务与端侧交付需按具体版本/合作协议确认。没有TensorRT/RKNN/CANN等通用部署承诺。[gemini-paper](#gemini-paper)
### 适配判断
Helix最明确的匹配对象是Figure自身双GPU控制系统；Gemini Robotics以论文展示/合作本体为依据。第三方平台映射目前均需厂商授权与接口证明。
两者最低内存、持续功耗、端到端p99延迟和授权费用本轮未取得；不以开放模型的数据代填。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md](../../01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/05_SWOT_Analysis.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/05_SWOT_Analysis.md)
- [05_Software_and_OS/20_Full_Stack_Cloud_Platforms/03_AI_Model_Integration.md](../../05_Software_and_OS/20_Full_Stack_Cloud_Platforms/03_AI_Model_Integration.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="helix"></a> **helix**：[官方/作者原文](https://www.figure.ai/news/helix)｜[本地归档](REFERENCES.md#legacy-54a85d2ae7b0a4d8)｜抓取UTC日期 2026-11-03。
- <a id="gemini-paper"></a> **gemini-paper**：[官方/作者原文](https://arxiv.org/html/2503.20020v1)｜[本地归档](REFERENCES.md#legacy-b41ca8130e23b33e)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
