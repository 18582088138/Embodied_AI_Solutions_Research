# 仿真与训练：Isaac Sim/Isaac Lab、格物、MuJoCo — AI 模型集成

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### VLA评估链
GR00T仓库提供LIBERO、RoboCasa、SimplerEnv等路径；openpi提供LIBERO/DROID示例。仿真benchmark可能使用目标任务微调checkpoint，应先核验训练/测试重叠。[nv-gr00t](#nv-gr00t)[openpi](#openpi)
### 控制接口
连接视觉、语言、状态、动作与仿真执行器，记录action horizon、相对/绝对坐标、控制周期、关节限制与重置协议。OpenVLA自回归与Flow Matching动作块的调度方式不同。[openvla](#openvla)[openpi](#openpi)
### 平台边界
MuJoCo不自带通用VLA权重；Isaac Lab不是所有模型自动可部署工具。格物尚未获取可验证VLA调度API。训练图像、控制器回放与真正Sim-to-Real迁移分别验收。
未测国产芯片上的端到端训练/策略部署性能。

### 本轮处理

对无法定位可靠公开资料的具微科技、AGIROS、格物，已按用户指示注明后本轮跳过；保留位置不代表已验证该产品或主体。

## 联动报告

- [04_AI_Models/15_Open_Source_VLA_Models/04_Sim_to_Real_Performance.md](../../04_AI_Models/15_Open_Source_VLA_Models/04_Sim_to_Real_Performance.md)
- [02_Core_Components/10_Actuators_and_Reducers/04_Sim_to_Real_Support.md](../../02_Core_Components/10_Actuators_and_Reducers/04_Sim_to_Real_Support.md)
- [02_Core_Components/12_Dexterous_Hands/04_Sim_to_Real_Support.md](../../02_Core_Components/12_Dexterous_Hands/04_Sim_to_Real_Support.md)
- [03_Robot_Manufacturers/14_Vertical_Scenario_Robots/03_Software_Architecture.md](../../03_Robot_Manufacturers/14_Vertical_Scenario_Robots/03_Software_Architecture.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="nv-gr00t"></a> **nv-gr00t**：[官方/作者原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/README.md)｜[本地归档](REFERENCES.md#legacy-ad24537e8616b70d)｜抓取UTC日期 2026-11-03。
- <a id="openpi"></a> **openpi**：[官方/作者原文](https://raw.githubusercontent.com/Physical-Intelligence/openpi/main/README.md)｜[本地归档](REFERENCES.md#legacy-84ef98c9061878e4)｜抓取UTC日期 2026-11-03。
- <a id="openvla"></a> **openvla**：[官方/作者原文](https://raw.githubusercontent.com/openvla/openvla/main/README.md)｜[本地归档](REFERENCES.md#legacy-46401c1b519322c8)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
