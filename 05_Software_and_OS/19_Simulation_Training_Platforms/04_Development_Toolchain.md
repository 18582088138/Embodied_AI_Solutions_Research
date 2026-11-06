# 仿真与训练：Isaac Sim/Isaac Lab、格物、MuJoCo — 开发工具链

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### Isaac
仿真、学习和资产工具链有官方入口，但数据标注/合成许可与各版本插件仍需检查。生成场景要核实碰撞几何、尺度、材质及摩擦，而不是只看视觉效果。[nv-isaac](#nv-isaac)[isaaclab](#isaaclab)
### MuJoCo
公开仓库和模型工具适合动力学快速迭代；外部数据录制/标注/云调度需要另接项目工具。[mujoco](#mujoco)
### 数据与回归
LeRobot提供数据/训练工具，可与策略仓库配合；傅利叶模型与MuJoCo路径可作为本体测试起点。[lerobot](#lerobot)[fourier-models](#fourier-models)[fourier-mujoco](#fourier-mujoco)
### 格物
低代码、标注、模型资产、云训练和调试功能尚未验证。后续应取得官方版本、API文档、许可证和可下载样例，再评估完整开发效率。

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
- <a id="lerobot"></a> **lerobot**：[官方/作者原文](https://raw.githubusercontent.com/huggingface/lerobot/main/README.md)｜[本地归档](REFERENCES.md#legacy-cdde66013990b290)｜抓取UTC日期 2026-11-03。
- <a id="fourier-models"></a> **fourier-models**：[官方/作者原文](https://raw.githubusercontent.com/FFTAI/Wiki-GRx-Models/master/README.md)｜[本地归档](REFERENCES.md#legacy-d90f8d484041b74f)｜抓取UTC日期 2026-11-03。
- <a id="fourier-mujoco"></a> **fourier-mujoco**：[官方/作者原文](https://raw.githubusercontent.com/FFTAI/Wiki-GRx-Mujoco/FourierN1/README.md)｜[本地归档](REFERENCES.md#legacy-8b2bfc857be41db0)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
