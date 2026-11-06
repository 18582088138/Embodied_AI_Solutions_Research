# 全栈整机：宇树科技、智元机器人、优必选 — SWOT 与技术栈

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 宇树：证据最具体的本体链
技术栈：G1/G1 EDU → 基础八核CPU（品牌未披露）/EDU可选Orin → PMSM/双编码器、Dex3-1、深度相机/LiDAR（来源比例未知） → SDK2/DDS与ROS2接入 → UnifoLM-VLA-0（公开项目，量产默认部署未知）。[unitree-g1](#unitree-g1)[unitree-sdk](#unitree-sdk)[unitree-ros](#unitree-ros)[unitree-unifolm](#unitree-unifolm)
优势：可追溯硬件/SDK/模型链；短板：配置差异、未披露BOM与工业验收数据。适合科研/操作开发，生产需另外验证。
### 智元
技术栈：本体产品 → 算力SKU未知 → 数据平台双臂/手/触觉（量产BOM未知） → AimRT公开线索/灵渠待证 → GO-1/Air。优势是模型/数据/运行时协同，短板是开源资产许可与量产配置映射待证。[agibot](#agibot)[agibot-go1](#agibot-go1)[agibot-aimrt](#agibot-aimrt)
### 优必选
技术栈：Walker S2/S1等 → 芯片待证 → 零部件比例待证 → OS/控制链待证 → Thinker独立模型状态待证。工业定位明确，集成成熟度仍需现场验收与BOM/软件文件。[ubtech](#ubtech)
### 机会与风险
工业操作、服务与研究有需求；环境泛化、长期可靠性、维护成本、模型许可和供应链是共同风险。完整链有未知项时，不得画成全部已验证关系。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md](../../01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md)
- [02_Core_Components/10_Actuators_and_Reducers/05_Market_Position.md](../../02_Core_Components/10_Actuators_and_Reducers/05_Market_Position.md)
- [02_Core_Components/12_Dexterous_Hands/01_Hardware_Specs.md](../../02_Core_Components/12_Dexterous_Hands/01_Hardware_Specs.md)
- [04_AI_Models/16_Domestic_Open_Source_Models/01_Model_Architecture.md](../../04_AI_Models/16_Domestic_Open_Source_Models/01_Model_Architecture.md)
- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../../05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="unitree-g1"></a> **unitree-g1**：[官方/作者原文](https://www.unitree.com/g1)｜[本地归档](REFERENCES.md#legacy-a3cc1c668e3bab25)｜抓取UTC日期 2026-11-03。
- <a id="unitree-sdk"></a> **unitree-sdk**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unitree_sdk2/main/README.md)｜[本地归档](REFERENCES.md#legacy-aacc6d52f84bed1f)｜抓取UTC日期 2026-11-03。
- <a id="unitree-ros"></a> **unitree-ros**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unitree_ros2/master/README.md)｜[本地归档](REFERENCES.md#legacy-0a3718637a1b0cd4)｜抓取UTC日期 2026-11-03。
- <a id="unitree-unifolm"></a> **unitree-unifolm**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unifolm-vla/main/README.md)｜[本地归档](REFERENCES.md#legacy-b68dedabc807e98f)｜抓取UTC日期 2026-11-03。
- <a id="agibot"></a> **agibot**：[官方/作者原文](https://www.agibot.com/)｜[本地归档](REFERENCES.md#legacy-3f79ba5681fd4208)｜抓取UTC日期 2026-11-03。
- <a id="agibot-go1"></a> **agibot-go1**：[官方/作者原文](https://raw.githubusercontent.com/OpenDriveLab/AgiBot-World/main/README.md)｜[本地归档](REFERENCES.md#legacy-f37440765f4db2fd)｜抓取UTC日期 2026-11-03。
- <a id="agibot-aimrt"></a> **agibot-aimrt**：[官方/作者原文](https://raw.githubusercontent.com/AimRT/AimRT/main/README.md)｜[本地归档](REFERENCES.md#legacy-c18a4a38d0f903b5)｜抓取UTC日期 2026-11-03。
- <a id="ubtech"></a> **ubtech**：[官方/作者原文](https://www.ubtrobot.com/)｜[本地归档](REFERENCES.md#legacy-2c01c36c8e4dfdf1)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
