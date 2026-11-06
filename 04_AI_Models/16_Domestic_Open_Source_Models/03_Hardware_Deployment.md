# 国产开源模型：智元GO-1、宇树UnifoLM-VLA-0、优必选Thinker — 硬件部署与算力需求

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### GO-1
开源训练/微调路径、LIBERO样例和权重入口已确认；本轮未找到官方明确的Jetson最低内存、p99延迟或功耗。推荐先用与仓库依赖相容的NVIDIA GPU复现，再测试Thor/Orin或迁移平台。[agibot-go1](#agibot-go1)
### UnifoLM-VLA-0
README推荐CUDA12.4/Python3.10.18，提供model server和real eval client，是CUDA基线证据；不是BPU/CANN/RKNN原生兼容证据。模型与机器人可分服务器/客户端，须记录网络延迟与超时。[unitree-unifolm](#unitree-unifolm)
### Thinker
参数、部署芯片、最小内存与延迟未核实，不能从优必选某款整机的算力模块反推Thinker要求。[ubtech](#ubtech)
### 国产硬件匹配
本轮三模型未取得指定昇腾、S100、RK3588、MLU或MTT上的官方完整动作链实测。国产模型与国产芯片适配关系需编译器/算子/动作头证据，而不是根据国籍推断。
测试建议统一相机数、分辨率、action horizon、batch=1、量化、功率模式、并发感知、成功率与温升。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md](../../01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md)
- [01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md](../../01_Compute_Chips/06_Huawei_HiSilicon/04_AI_Capabilities.md)
- [01_Compute_Chips/08_Horizon_Robotics/04_AI_Capabilities.md](../../01_Compute_Chips/08_Horizon_Robotics/04_AI_Capabilities.md)
- [02_Core_Components/12_Dexterous_Hands/03_Software_Drivers.md](../../02_Core_Components/12_Dexterous_Hands/03_Software_Drivers.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/03_Software_Architecture.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/03_Software_Architecture.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="agibot-go1"></a> **agibot-go1**：[官方/作者原文](https://raw.githubusercontent.com/OpenDriveLab/AgiBot-World/main/README.md)｜[本地归档](REFERENCES.md#legacy-f37440765f4db2fd)｜抓取UTC日期 2026-11-03。
- <a id="unitree-unifolm"></a> **unitree-unifolm**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unifolm-vla/main/README.md)｜[本地归档](REFERENCES.md#legacy-b68dedabc807e98f)｜抓取UTC日期 2026-11-03。
- <a id="ubtech"></a> **ubtech**：[官方/作者原文](https://www.ubtrobot.com/)｜[本地归档](REFERENCES.md#legacy-2c01c36c8e4dfdf1)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
