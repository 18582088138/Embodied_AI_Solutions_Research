# 开源 VLA：OpenVLA、π0.5、GR00T N1.6/N1.7 — 模型架构

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### OpenVLA
OpenVLA 是约 7B 参数 VLA，原版使用视觉表征与 Llama 系语言骨干，自回归生成离散动作 token；不要与后来的 OFT 动作块/并行解码变体混用。论文与仓库提供结构、训练和模型入口。[openvla](#openvla)[openvla-paper](#openvla-paper)
### π0.5
openpi 提供 π0.5 模型与训练/推理代码；公开实现声明当前只支持 Flow Matching 动作头。层级任务分解、动作块和开放世界泛化是 π0.5 研究重点，公开代码不应被解释为所有论文训练组件均完全复现。[openpi](#openpi)[pi05](#pi05)
本轮未单独核验所有 checkpoint 的总参数统计，不给一个未经代码统计的统一精确值。
### GR00T：固定版本再比较
N1.6 分支描述约3B模型、内部 Cosmos-Reason-2B 变体和32层 DiT动作头；当前 N1.7 主线描述 Cosmos-Reason2-2B/Qwen3-VL 与16层动作头、相对末端动作空间。主线迁移说明对旧版本的简述与 N1.6 分支描述不完全一致，应以目标 checkpoint 配置核验，不能拼接两版结构。[gr00t-n16](#gr00t-n16)[nv-gr00t](#nv-gr00t)

## 联动报告

- [01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md](../../01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md)
- [01_Compute_Chips/02_Intel/04_AI_Capabilities.md](../../01_Compute_Chips/02_Intel/04_AI_Capabilities.md)
- [01_Compute_Chips/05_Rockchip/04_AI_Capabilities.md](../../01_Compute_Chips/05_Rockchip/04_AI_Capabilities.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/03_AI_Model_Integration.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/03_AI_Model_Integration.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="openvla"></a> **openvla**：[官方/作者原文](https://raw.githubusercontent.com/openvla/openvla/main/README.md)｜[本地归档](REFERENCES.md#legacy-46401c1b519322c8)｜抓取UTC日期 2026-11-03。
- <a id="openvla-paper"></a> **openvla-paper**：[官方/作者原文](https://arxiv.org/html/2406.09246v3)｜[本地归档](REFERENCES.md#legacy-eae40e7a4f090282)｜抓取UTC日期 2026-11-03。
- <a id="openpi"></a> **openpi**：[官方/作者原文](https://raw.githubusercontent.com/Physical-Intelligence/openpi/main/README.md)｜[本地归档](REFERENCES.md#legacy-84ef98c9061878e4)｜抓取UTC日期 2026-11-03。
- <a id="pi05"></a> **pi05**：[官方/作者原文](https://www.pi.website/blog/pi05)｜[本地归档](REFERENCES.md#legacy-c0cf02e6ae6984f3)｜抓取UTC日期 2026-11-03。
- <a id="gr00t-n16"></a> **gr00t-n16**：[官方/作者原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/n1d6/README.md)｜[本地归档](REFERENCES.md#legacy-883a82eef8c408fc)｜抓取UTC日期 2026-11-03。
- <a id="nv-gr00t"></a> **nv-gr00t**：[官方/作者原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/README.md)｜[本地归档](REFERENCES.md#legacy-ad24537e8616b70d)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
