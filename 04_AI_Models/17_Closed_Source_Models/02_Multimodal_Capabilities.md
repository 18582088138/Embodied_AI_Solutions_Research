# 闭源模型：Helix、Gemini Robotics — 多模态能力

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### Helix
初代系统使用机载图像、机器人状态与语言，经语义latent传递至高频动作策略；控制腕、手指、躯干与头部。官方文章没有证明模型可通用接入任意外部触觉/六维力设备。[helix](#helix)
### Gemini Robotics
技术报告覆盖图像、语言与机器人动作，以及ER的多视角对应、3D框、抓取/轨迹推理。推理能力和物理执行能力必须分别评估；不把基础Gemini支持的所有模态自动继承到所有Robotics版本。[gemini-paper](#gemini-paper)
### 系统联动
闭源接口若不公开状态/action schema，适配灵巧手、底盘和力传感器需要厂商协作。重点询证输入频率、相机校准、状态同步、动作单位、超时和异常返回。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md](../../01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/05_SWOT_Analysis.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/05_SWOT_Analysis.md)
- [05_Software_and_OS/20_Full_Stack_Cloud_Platforms/03_AI_Model_Integration.md](../../05_Software_and_OS/20_Full_Stack_Cloud_Platforms/03_AI_Model_Integration.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="helix"></a> **helix**：[官方/作者原文](https://www.figure.ai/news/helix)｜[本地归档](REFERENCES.md#legacy-54a85d2ae7b0a4d8)｜抓取UTC日期 2026-11-03。
- <a id="gemini-paper"></a> **gemini-paper**：[官方/作者原文](https://arxiv.org/html/2503.20020v1)｜[本地归档](REFERENCES.md#legacy-b41ca8130e23b33e)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
