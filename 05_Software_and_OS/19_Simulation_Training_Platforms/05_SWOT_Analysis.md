# 仿真与训练：Isaac Sim/Isaac Lab、格物、MuJoCo — SWOT 分析

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### Isaac Sim / Lab
优势：感知仿真、训练与NVIDIA部署生态有联动路径；短板：硬件/驱动/资产依赖、学习成本和物理参数辨识仍在。适合视觉和GPU训练密集项目。[nv-isaac](#nv-isaac)[isaaclab](#isaaclab)
### MuJoCo
优势：开放物理引擎、便于动力学与控制迭代；短板：场景资产、感知数据和生产控制集成需另配。适合控制研究、参数辨识和快速仿真。[mujoco](#mujoco)
### 格物
公开证据不足以评分；主体和交付形态未确认，不将其他平台成果算入其生态。
### 商业与风险
开源引擎与商业资产/托管服务许可不同；训练效果需要真实本体与相同任务验收。高保真渲染不是接触物理正确性的保证。

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

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
