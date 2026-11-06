# 国产开源模型：智元GO-1、宇树UnifoLM-VLA-0、优必选Thinker — 仿真到现实迁移

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### GO-1
论文与开源材料同时覆盖仿真/真实场景；团队博客称少于200条折衣演示可迁移到新本体。这是作者实验条件，不能推广为任意任务/机器人都只需200条数据。[go1-architecture](#go1-architecture)[go1-blog](#go1-blog)
### UnifoLM-VLA-0
README称单策略完成12类复杂操作，但本轮未取得逐任务试验数、成功率、人工干预和未见对象清单。公开可视化是能力线索，不等于可重复量化评估。[unitree-unifolm](#unitree-unifolm)
### Thinker
未获取可以区分仿真、零样本、少样本与现场量产的模型评估；维持待核实。[ubtech](#ubtech)
### 共同风险
动作数据质量、延迟、左右手坐标、控制器实现与机械一致性影响迁移。建议先回放演示验证采集/执行一致，再做开环预测与实机闭环，最后测长时运行和失败恢复。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md](../../01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md)
- [01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md](../../01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md)
- [01_Compute_Chips/08_Horizon_Robotics/04_AI_Capabilities.md](../../01_Compute_Chips/08_Horizon_Robotics/04_AI_Capabilities.md)
- [02_Core_Components/12_Dexterous_Hands/03_Software_Drivers.md](../../02_Core_Components/12_Dexterous_Hands/03_Software_Drivers.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/03_Software_Architecture.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/03_Software_Architecture.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="go1-architecture"></a> **go1-architecture**：[官方/作者原文](https://arxiv.org/html/2503.06669v2)｜[本地归档](REFERENCES.md#legacy-a838486a4507a0d0)｜抓取UTC日期 2026-11-03。
- <a id="go1-blog"></a> **go1-blog**：[官方/作者原文](https://opendrivelab.com/OpenGO1/)｜[本地归档](REFERENCES.md#legacy-b07c975a8dc39e79)｜抓取UTC日期 2026-11-03。
- <a id="unitree-unifolm"></a> **unitree-unifolm**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unifolm-vla/main/README.md)｜[本地归档](REFERENCES.md#legacy-b68dedabc807e98f)｜抓取UTC日期 2026-11-03。
- <a id="ubtech"></a> **ubtech**：[官方/作者原文](https://www.ubtrobot.com/)｜[本地归档](REFERENCES.md#legacy-2c01c36c8e4dfdf1)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
