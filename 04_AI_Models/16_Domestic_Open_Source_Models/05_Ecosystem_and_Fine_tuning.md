# 国产开源模型：智元GO-1、宇树UnifoLM-VLA-0、优必选Thinker — 生态与微调

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### GO-1
仓库已提供权重、GO-1/Air和微调入口，AgiBot World称100机器人采集1M+轨迹/100+场景；论文给217任务。仓库明确数据与代码均为CC BY-NC-SA 4.0，**NC限制意味着不能把整个数据/权重生态视为无条件商业可用**，须逐资产检查许可。[agibot-go1](#agibot-go1)[go1-architecture](#go1-architecture)
### UnifoLM-VLA-0
训练、推理、数据转换与checkpoint发布已记录，官方仓库不等于完整上游模型许可已排除。此次LICENSE直接入口404，需核验实际许可文件、HF model card及Qwen/其他上游条款。[unitree-unifolm](#unitree-unifolm)
### Thinker
本轮未确认可下载模型、训练代码、数据、许可证或官方维护仓库，因此目录标题描述的是调研目标，并非已开源的分类结论。[ubtech](#ubtech)
### 评估建议
优先选择能复现模型、核对数据schema且许可适合目标用途的项目。社区规模未做固定时间统计；开源程度按代码、权重、数据、训练配方四项分别登记。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md](../../01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md)
- [01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md](../../01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md)
- [01_Compute_Chips/08_Horizon_Robotics/04_AI_Capabilities.md](../../01_Compute_Chips/08_Horizon_Robotics/04_AI_Capabilities.md)
- [02_Core_Components/12_Dexterous_Hands/03_Software_Drivers.md](../../02_Core_Components/12_Dexterous_Hands/03_Software_Drivers.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/03_Software_Architecture.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/03_Software_Architecture.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="agibot-go1"></a> **agibot-go1**：[官方/作者原文](https://raw.githubusercontent.com/OpenDriveLab/AgiBot-World/main/README.md)｜[本地归档](REFERENCES.md#legacy-f37440765f4db2fd)｜抓取UTC日期 2026-11-03。
- <a id="go1-architecture"></a> **go1-architecture**：[官方/作者原文](https://arxiv.org/html/2503.06669v2)｜[本地归档](REFERENCES.md#legacy-a838486a4507a0d0)｜抓取UTC日期 2026-11-03。
- <a id="unitree-unifolm"></a> **unitree-unifolm**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unifolm-vla/main/README.md)｜[本地归档](REFERENCES.md#legacy-b68dedabc807e98f)｜抓取UTC日期 2026-11-03。
- <a id="ubtech"></a> **ubtech**：[官方/作者原文](https://www.ubtrobot.com/)｜[本地归档](REFERENCES.md#legacy-2c01c36c8e4dfdf1)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
