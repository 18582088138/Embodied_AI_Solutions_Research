# 国产开源模型：智元GO-1、宇树UnifoLM-VLA-0、优必选Thinker — 模型架构

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 智元 GO-1
AgiBot World论文描述：InternVL2.5-2B骨干、潜在动作模型（LAM）、24层潜在规划器、扩散动作expert，经历潜在动作、规划、真实动作训练阶段。2B是骨干规模，不能当包含planner/expert的完整参数数。[go1-architecture](#go1-architecture)
仓库2025-09-19公开GO-1、GO-1 Air；Air不含Latent Planner。开源GO-1与博客提到GO-1-Pro须分开，不能默认Pro所有模块已公开。[agibot-go1](#agibot-go1)[go1-blog](#go1-blog)
### 宇树 UnifoLM-VLA-0
README记录2026-01-29训练/推理/权重发布；官方配置为Qwen2.5-VL相关骨干、action/state维度16、动作窗口16，源码调用Flow Matching动作头。示例路径和维度是训练配置，可能需按目标checkpoint修改。[unitree-unifolm](#unitree-unifolm)[unitree-config2](#unitree-config2)[unitree-architecture](#unitree-architecture)
未单独统计完整参数量。
### 优必选 Thinker
本轮优必选官网可确认整机产品线，但未获取Thinker的独立技术报告、官方权重仓库或许可证。保留附件目标，**不将其判定为已验证开源VLA**。[ubtech](#ubtech)

## 联动报告

- [01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md](../../01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md)
- [01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md](../../01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md)
- [01_Compute_Chips/08_Horizon_Robotics/04_AI_Capabilities.md](../../01_Compute_Chips/08_Horizon_Robotics/04_AI_Capabilities.md)
- [02_Core_Components/12_Dexterous_Hands/03_Software_Drivers.md](../../02_Core_Components/12_Dexterous_Hands/03_Software_Drivers.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/03_Software_Architecture.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/03_Software_Architecture.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="go1-architecture"></a> **go1-architecture**：[官方/作者原文](https://arxiv.org/html/2503.06669v2)｜[本地归档](REFERENCES.md#legacy-a838486a4507a0d0)｜抓取UTC日期 2026-11-03。
- <a id="agibot-go1"></a> **agibot-go1**：[官方/作者原文](https://raw.githubusercontent.com/OpenDriveLab/AgiBot-World/main/README.md)｜[本地归档](REFERENCES.md#legacy-f37440765f4db2fd)｜抓取UTC日期 2026-11-03。
- <a id="go1-blog"></a> **go1-blog**：[官方/作者原文](https://opendrivelab.com/OpenGO1/)｜[本地归档](REFERENCES.md#legacy-b07c975a8dc39e79)｜抓取UTC日期 2026-11-03。
- <a id="unitree-unifolm"></a> **unitree-unifolm**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unifolm-vla/main/README.md)｜[本地归档](REFERENCES.md#legacy-b68dedabc807e98f)｜抓取UTC日期 2026-11-03。
- <a id="unitree-config2"></a> **unitree-config2**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unifolm-vla/main/src/unifolm_vla/config/training/unifolm_vla_train.yaml)｜[本地归档](REFERENCES.md#legacy-045fc669a11f7200)｜抓取UTC日期 2026-11-03。
- <a id="unitree-architecture"></a> **unitree-architecture**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unifolm-vla/main/src/unifolm_vla/model/framework/unifolm_vla.py)｜[本地归档](REFERENCES.md#legacy-c288256e6b4e3c60)｜抓取UTC日期 2026-11-03。
- <a id="ubtech"></a> **ubtech**：[官方/作者原文](https://www.ubtrobot.com/)｜[本地归档](REFERENCES.md#legacy-2c01c36c8e4dfdf1)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
