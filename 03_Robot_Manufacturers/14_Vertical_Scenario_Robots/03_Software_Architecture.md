# 垂直场景整机：云深处、傅利叶、具微科技 — 软件架构

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 云深处
本轮官网没有足够OS/ROS2/VLA默认部署细节；运动技能、巡检应用与通用VLA须分开，不把演示自主行动称为已有大型操作模型。[deeprobotics](#deeprobotics)
### 傅利叶
fourier-grx-client、Models、MuJoCo与LeRobot相关库为本体软件/仿真/学习接口线索；需按GR1/GR2/N1和分支确认，不能把组织全部仓库拼成单一量产软件栈。[fourier-client](#fourier-client)[fourier-models](#fourier-models)[fourier-mujoco](#fourier-mujoco)[fourier-lerobot](#fourier-lerobot)
### 具微科技
主体和产品未经核实，OS、中间件与VLA均待证。
### 云边端设计
巡检可云端管理任务/报告、端侧导航/状态机、控制域运动；康复需力控和人机安全；操作平台需动作块/手部映射。上述为场景架构建议，非厂商功能承诺。

### 本轮处理

对无法定位可靠公开资料的具微科技、AGIROS、格物，已按用户指示注明后本轮跳过；保留位置不代表已验证该产品或主体。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md](../../01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md)
- [02_Core_Components/11_Sensors_and_Vision/05_Market_Position.md](../../02_Core_Components/11_Sensors_and_Vision/05_Market_Position.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md)
- [04_AI_Models/15_Open_Source_VLA_Models/04_Sim_to_Real_Performance.md](../../04_AI_Models/15_Open_Source_VLA_Models/04_Sim_to_Real_Performance.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="deeprobotics"></a> **deeprobotics**：[官方/作者原文](https://www.deeprobotics.cn/)｜[本地归档](REFERENCES.md#legacy-9af2c02a881ce0f9)｜抓取UTC日期 2026-11-03。
- <a id="fourier-client"></a> **fourier-client**：[官方/作者原文](https://raw.githubusercontent.com/FFTAI/fourier-grx-client/main/README.md)｜[本地归档](REFERENCES.md#legacy-86c414591546d952)｜抓取UTC日期 2026-11-03。
- <a id="fourier-models"></a> **fourier-models**：[官方/作者原文](https://raw.githubusercontent.com/FFTAI/Wiki-GRx-Models/master/README.md)｜[本地归档](REFERENCES.md#legacy-d90f8d484041b74f)｜抓取UTC日期 2026-11-03。
- <a id="fourier-mujoco"></a> **fourier-mujoco**：[官方/作者原文](https://raw.githubusercontent.com/FFTAI/Wiki-GRx-Mujoco/FourierN1/README.md)｜[本地归档](REFERENCES.md#legacy-8b2bfc857be41db0)｜抓取UTC日期 2026-11-03。
- <a id="fourier-lerobot"></a> **fourier-lerobot**：[官方/作者原文](https://raw.githubusercontent.com/FFTAI/fourier-lerobot/main/README.md)｜[本地归档](REFERENCES.md#legacy-ad17fb6d02ea5152)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
