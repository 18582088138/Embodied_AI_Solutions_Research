# 仿真与训练：Isaac Sim/Isaac Lab、格物、MuJoCo — 硬件抽象与兼容性

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### Isaac平台
检查具体版本GPU/驱动、USD资产、关节控制接口与ROS桥接；端侧Jetson部署与仿真工作站支持是两套要求。不能从NVIDIA模型可部署推导所有Isaac版本可在Jetson运行。[nv-isaac](#nv-isaac)[isaaclab](#isaaclab)
### MuJoCo
MJCF/URDF和执行器模型帮助定义本体，但真实ROS驱动、CAN/EtherCAT采集不自动包含在模型中。傅利叶公开Models/MuJoCo库说明存在本体资产路径，仍需核对版本与参数。[mujoco](#mujoco)[fourier-models](#fourier-models)[fourier-mujoco](#fourier-mujoco)
### 零部件与国产芯片
减速器的背隙/刚度、灵巧手耦合、相机噪声/曝光与六维力漂移需模型化。RK、昇腾、BPU、MUSA的训练与运行后端兼容分别核验；公开框架适配不等于仿真GPU内核可用。
格物的资产、硬件桥接与芯片支持均待正式资料。

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
- <a id="fourier-models"></a> **fourier-models**：[官方/作者原文](https://raw.githubusercontent.com/FFTAI/Wiki-GRx-Models/master/README.md)｜[本地归档](REFERENCES.md#legacy-d90f8d484041b74f)｜抓取UTC日期 2026-11-03。
- <a id="fourier-mujoco"></a> **fourier-mujoco**：[官方/作者原文](https://raw.githubusercontent.com/FFTAI/Wiki-GRx-Mujoco/FourierN1/README.md)｜[本地归档](REFERENCES.md#legacy-8b2bfc857be41db0)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
