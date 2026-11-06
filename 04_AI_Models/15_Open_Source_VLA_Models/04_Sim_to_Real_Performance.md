# 开源 VLA：OpenVLA、π0.5、GR00T N1.6/N1.7 — 仿真到现实迁移

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### OpenVLA
论文在多个真实机器人任务上评估，仓库预训练混合含约970K轨迹；任务、本体和训练分布决定泛化，不能摘一项成功率代表工厂全天运行。[openvla](#openvla)[openvla-paper](#openvla-paper)
### π0.5
研究宣称开放世界、长时程泛化；openpi 提供 LIBERO/DROID等 checkpoint与评估入口。仿真成功率、真实双臂任务与未见环境性能属于不同证据。[pi05](#pi05)[openpi](#openpi)
### GR00T
N1.6/N1.7 仓库包括 RoboCasa、LIBERO、SimplerEnv 与真实G1线索；先确定checkpoint是否经目标本体微调，再判断零样本。[gr00t-n16](#gr00t-n16)[nv-gr00t](#nv-gr00t)
### 比较方法
本轮不做跨论文成功率榜单，因为任务、本体、试验次数、对象、初始位置及人工干预不同。统一测试应报告成功/总次数、失败分类、介入率、恢复耗时和置信区间，并区分语义理解、动作输出和机械执行失败。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md](../../01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md)
- [01_Compute_Chips/02_Intel/04_AI_Capabilities.md](../../01_Compute_Chips/02_Intel/04_AI_Capabilities.md)
- [01_Compute_Chips/05_Rockchip/04_AI_Capabilities.md](../../01_Compute_Chips/05_Rockchip/04_AI_Capabilities.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/03_AI_Model_Integration.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/03_AI_Model_Integration.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="openvla"></a> **openvla**：[官方/作者原文](https://raw.githubusercontent.com/openvla/openvla/main/README.md)｜[本地归档](REFERENCES.md#legacy-46401c1b519322c8)｜抓取UTC日期 2026-11-03。
- <a id="openvla-paper"></a> **openvla-paper**：[官方/作者原文](https://arxiv.org/html/2406.09246v3)｜[本地归档](REFERENCES.md#legacy-eae40e7a4f090282)｜抓取UTC日期 2026-11-03。
- <a id="pi05"></a> **pi05**：[官方/作者原文](https://www.pi.website/blog/pi05)｜[本地归档](REFERENCES.md#legacy-c0cf02e6ae6984f3)｜抓取UTC日期 2026-11-03。
- <a id="openpi"></a> **openpi**：[官方/作者原文](https://raw.githubusercontent.com/Physical-Intelligence/openpi/main/README.md)｜[本地归档](REFERENCES.md#legacy-84ef98c9061878e4)｜抓取UTC日期 2026-11-03。
- <a id="gr00t-n16"></a> **gr00t-n16**：[官方/作者原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/n1d6/README.md)｜[本地归档](REFERENCES.md#legacy-883a82eef8c408fc)｜抓取UTC日期 2026-11-03。
- <a id="nv-gr00t"></a> **nv-gr00t**：[官方/作者原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/README.md)｜[本地归档](REFERENCES.md#legacy-ad24537e8616b70d)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
