# 国产开源模型：智元GO-1、宇树UnifoLM-VLA-0、优必选Thinker — 多模态能力

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### GO-1
论文使用多视角图像/语言与动作expert；AgiBot World数据平台介绍含视觉触觉硬件、6DoF手和移动双臂。传感器在采集平台存在不代表所有GO-1 checkpoint原生输入触觉，应检查schema/模型encoder。[go1-architecture](#go1-architecture)[agibot-go1](#agibot-go1)
### UnifoLM-VLA-0
官方说明提升2D/3D空间语义与操作泛化，源码包含Qwen2.5-VL和状态/动作通道；README称单策略完成12类实机任务。该说明未给完整可比成功率，也不能推导已融合任意六维力传感器。[unitree-unifolm](#unitree-unifolm)[unitree-config2](#unitree-config2)
### Thinker
触觉、力觉、视觉/语言输入与动作形式均待官方文档核验；目前不借整机产品宣传替代模型证据。[ubtech](#ubtech)
### 端侧联动
要把传感器同步、手部自由度、绝对/相对动作和坐标系写入数据规范。GO-1团队特别指出采集—执行一致性可能比单纯模型精度更影响落地。[go1-blog](#go1-blog)

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
- <a id="unitree-unifolm"></a> **unitree-unifolm**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unifolm-vla/main/README.md)｜[本地归档](REFERENCES.md#legacy-b68dedabc807e98f)｜抓取UTC日期 2026-11-03。
- <a id="unitree-config2"></a> **unitree-config2**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unifolm-vla/main/src/unifolm_vla/config/training/unifolm_vla_train.yaml)｜[本地归档](REFERENCES.md#legacy-045fc669a11f7200)｜抓取UTC日期 2026-11-03。
- <a id="ubtech"></a> **ubtech**：[官方/作者原文](https://www.ubtrobot.com/)｜[本地归档](REFERENCES.md#legacy-2c01c36c8e4dfdf1)｜抓取UTC日期 2026-11-03。
- <a id="go1-blog"></a> **go1-blog**：[官方/作者原文](https://opendrivelab.com/OpenGO1/)｜[本地归档](REFERENCES.md#legacy-b07c975a8dc39e79)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
