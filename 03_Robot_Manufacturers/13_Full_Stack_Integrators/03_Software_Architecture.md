# 全栈整机：宇树科技、智元机器人、优必选 — 软件架构

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 宇树
Unitree SDK2与ROS2仓库提供DDS通信/状态命令集成；UnifoLM-VLA-0提供模型训练、服务器/客户端路径。ROS2支持不说明底层所有控制器运行Linux，公开模型也不必然是量产固件默认策略。[unitree-sdk](#unitree-sdk)[unitree-ros](#unitree-ros)[unitree-unifolm](#unitree-unifolm)
### 智元
GO-1/GO-1 Air的模型与数据、AimRT运行时公开；灵渠OS架构、所有本体控制链和VLA默认部署方式本轮未核实。AimRT、ROS2和灵渠不是可以无证据互换的名称。[agibot-go1](#agibot-go1)[agibot-aimrt](#agibot-aimrt)
### 优必选
官网有整机线索，Thinker权重/OS/中间件/云边部署细节仍未取得公开资料。[ubtech](#ubtech)
### 集成判断
高层语言/视觉模型与低层平衡、IK、轨迹、阻抗和伺服需要明确时间尺度；云端只作低频协调时仍需本地失联回退。正式架构应给数据流、时钟、控制周期与安全边界。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md](../../01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md)
- [02_Core_Components/10_Actuators_and_Reducers/05_Market_Position.md](../../02_Core_Components/10_Actuators_and_Reducers/05_Market_Position.md)
- [02_Core_Components/12_Dexterous_Hands/01_Hardware_Specs.md](../../02_Core_Components/12_Dexterous_Hands/01_Hardware_Specs.md)
- [04_AI_Models/16_Domestic_Open_Source_Models/01_Model_Architecture.md](../../04_AI_Models/16_Domestic_Open_Source_Models/01_Model_Architecture.md)
- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../../05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="unitree-sdk"></a> **unitree-sdk**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/README.md)｜[本地归档](REFERENCES.md#legacy-aacc6d52f84bed1f)｜抓取UTC日期 2026-11-03。
- <a id="unitree-ros"></a> **unitree-ros**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unitree_ros2/master/README.md)｜[本地归档](REFERENCES.md#legacy-0a3718637a1b0cd4)｜抓取UTC日期 2026-11-03。
- <a id="unitree-unifolm"></a> **unitree-unifolm**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unifolm-vla/main/README.md)｜[本地归档](REFERENCES.md#legacy-b68dedabc807e98f)｜抓取UTC日期 2026-11-03。
- <a id="agibot-go1"></a> **agibot-go1**：[官方/作者原文](https://raw.githubusercontent.com/OpenDriveLab/AgiBot-World/main/README.md)｜[本地归档](REFERENCES.md#legacy-f37440765f4db2fd)｜抓取UTC日期 2026-11-03。
- <a id="agibot-aimrt"></a> **agibot-aimrt**：[官方/作者原文](https://raw.githubusercontent.com/AimRT/AimRT/main/README.md)｜[本地归档](REFERENCES.md#legacy-c18a4a38d0f903b5)｜抓取UTC日期 2026-11-03。
- <a id="ubtech"></a> **ubtech**：[官方/作者原文](https://www.ubtrobot.com/)｜[本地归档](REFERENCES.md#legacy-2c01c36c8e4dfdf1)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
