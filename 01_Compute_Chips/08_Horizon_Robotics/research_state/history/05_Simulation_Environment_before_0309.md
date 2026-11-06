# 地平线 / 地瓜机器人 D-Robotics — 仿真环境

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 官方模拟器边界
TROS 文档明示 x86 模拟器提供图片回灌和部分功能体验；该工具用于算法开发验证，不能等同于高保真关节/接触物理仿真。[horizon-tros-doc](#horizon-tros-doc)
### Sim-to-Real 路线
可在 MuJoCo/Isaac Lab 工作站训练，再把策略转到 BPU/CPU；须测量观测预处理、动作归一化、控制域延迟和量化后的行为。[mujoco](#mujoco)[isaaclab](#isaaclab)
缺口：官方本体物理资产、生成式场景/合成数据平台，以及 S100 上完整 VLA 或全身策略的实机迁移数据。

## 联动报告

- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../../05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md)
- [04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md](../../04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md)
- [02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md](../../02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="horizon-tros-doc"></a> **horizon-tros-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/tros.md)｜[本地归档](../../_Evidence/horizon-tros-doc.txt)｜抓取UTC日期 2026-11-03。
- <a id="mujoco"></a> **mujoco**：[官方/作者原文](https://raw.githubusercontent.com/google-deepmind/mujoco/main/README.md)｜[本地归档](../../_Evidence/mujoco.txt)｜抓取UTC日期 2026-11-03。
- <a id="isaaclab"></a> **isaaclab**：[官方/作者原文](https://raw.githubusercontent.com/isaac-sim/IsaacLab/main/README.md)｜[本地归档](../../_Evidence/isaaclab.txt)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
