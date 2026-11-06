# 仿真与训练：Isaac Sim/Isaac Lab、格物、MuJoCo — 架构与通信机制

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### Isaac Sim / Isaac Lab
Isaac Sim提供物理/传感仿真与合成数据，Isaac Lab在其上组织机器人学习工作流；训练循环、仿真步长和ROS消息周期分别记录。离线仿真中的高速度不能解释为现实的微秒级通信承诺。[nv-isaac](#nv-isaac)[isaaclab](#isaaclab)
### MuJoCo
MuJoCo是通用物理引擎，支持机器人动力学与接触建模，不是开箱即用的云边端机器人OS或网络主站。[mujoco](#mujoco)
### “格物”
本轮没有核实附件“格物”的主体/正式产品/版本。InternUtopia仓库是另一个具身仿真项目，不能仅凭中文名称相近将其改名或等同格物。[agibot-sim](#agibot-sim)
### 协同建议
仿真训练服务器、模型仓库和端侧执行分工；动作回放和硬件在环需独立测时间、网络和故障恢复。

### 本轮处理

对无法定位可靠公开资料的具微科技、AGIROS、格物，已按用户指示注明后本轮跳过；保留位置不代表已验证该产品或主体。

## 联动报告

- [04_AI_Models/15_Open_Source_VLA_Models/04_Sim_to_Real_Performance.md](../../04_AI_Models/15_Open_Source_VLA_Models/04_Sim_to_Real_Performance.md)
- [02_Core_Components/10_Actuators_and_Reducers/04_Sim_to_Real_Support.md](../../02_Core_Components/10_Actuators_and_Reducers/04_Sim_to_Real_Support.md)
- [02_Core_Components/12_Dexterous_Hands/04_Sim_to_Real_Support.md](../../02_Core_Components/12_Dexterous_Hands/04_Sim_to_Real_Support.md)
- [03_Robot_Manufacturers/14_Vertical_Scenario_Robots/03_Software_Architecture.md](../../03_Robot_Manufacturers/14_Vertical_Scenario_Robots/03_Software_Architecture.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="nv-isaac"></a> **nv-isaac**：[官方/作者原文](https://developer.nvidia.com/isaac/sim)｜[本地归档](REFERENCES.md#legacy-dd9e0b266d5780c1)｜抓取UTC日期 2026-11-03。
- <a id="isaaclab"></a> **isaaclab**：[官方/作者原文](https://raw.githubusercontent.com/isaac-sim/IsaacLab/main/README.md)｜[本地归档](REFERENCES.md#legacy-6c130dd52b00304e)｜抓取UTC日期 2026-11-03。
- <a id="mujoco"></a> **mujoco**：[官方/作者原文](https://raw.githubusercontent.com/google-deepmind/mujoco/main/README.md)｜[本地归档](REFERENCES.md#legacy-49e6c5a3a40d667c)｜抓取UTC日期 2026-11-03。
- <a id="agibot-sim"></a> **agibot-sim**：[官方/作者原文](https://raw.githubusercontent.com/InternRobotics/InternUtopia/main/README.md)｜[本地归档](REFERENCES.md#legacy-6225c272a4eaaf45)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
