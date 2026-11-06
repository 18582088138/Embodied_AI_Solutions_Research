# 全栈整机：宇树科技、智元机器人、优必选 — 算力平台选型

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 宇树
G1官方页披露基础八核CPU，不披露芯片品牌；G1 EDU高算力模块提供“多品牌型号，如Orin”等选项。因此“G1全系标配Orin”不成立。VLA官方仓库推荐CUDA12.4，并支持远程model server，不证明所有推理都在本体端。[unitree-g1](#unitree-g1)[unitree-unifolm](#unitree-unifolm)
### 智元
公开整机官网、GO-1与AimRT构成软件/数据生态线索；本轮未取得各A/G系列“大脑/小脑”具体SKU与电控BOM。GR00T示例涉及智元本体，不能因此推导所有智元标配NVIDIA。[agibot](#agibot)[agibot-go1](#agibot-go1)[agibot-aimrt](#agibot-aimrt)[gr00t-n16](#gr00t-n16)
### 优必选
官网可确认Walker S2/S1等产品，未取得通用“大脑/小脑”芯片清单和按型号的Thinker部署证据。[ubtech](#ubtech)
### 选型理由
可以分析内存/功耗/实时域/接口需求，但未经访谈或技术文件的理由标为分析建议，不替厂商编造决策。控制MCU、GPU、传感处理器和云服务器分别核验。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md](../../01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md)
- [02_Core_Components/10_Actuators_and_Reducers/05_Market_Position.md](../../02_Core_Components/10_Actuators_and_Reducers/05_Market_Position.md)
- [02_Core_Components/12_Dexterous_Hands/01_Hardware_Specs.md](../../02_Core_Components/12_Dexterous_Hands/01_Hardware_Specs.md)
- [04_AI_Models/16_Domestic_Open_Source_Models/01_Model_Architecture.md](../../04_AI_Models/16_Domestic_Open_Source_Models/01_Model_Architecture.md)
- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../../05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="unitree-g1"></a> **unitree-g1**：[官方/作者原文](https://www.unitree.com/g1)｜[本地归档](REFERENCES.md#legacy-a3cc1c668e3bab25)｜抓取UTC日期 2026-11-03。
- <a id="unitree-unifolm"></a> **unitree-unifolm**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unifolm-vla/main/README.md)｜[本地归档](REFERENCES.md#legacy-b68dedabc807e98f)｜抓取UTC日期 2026-11-03。
- <a id="agibot"></a> **agibot**：[官方/作者原文](https://www.agibot.com/)｜[本地归档](REFERENCES.md#legacy-3f79ba5681fd4208)｜抓取UTC日期 2026-11-03。
- <a id="agibot-go1"></a> **agibot-go1**：[官方/作者原文](https://raw.githubusercontent.com/OpenDriveLab/AgiBot-World/main/README.md)｜[本地归档](REFERENCES.md#legacy-f37440765f4db2fd)｜抓取UTC日期 2026-11-03。
- <a id="agibot-aimrt"></a> **agibot-aimrt**：[官方/作者原文](https://raw.githubusercontent.com/AimRT/AimRT/main/README.md)｜[本地归档](REFERENCES.md#legacy-c18a4a38d0f903b5)｜抓取UTC日期 2026-11-03。
- <a id="gr00t-n16"></a> **gr00t-n16**：[官方/作者原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/n1d6/README.md)｜[本地归档](REFERENCES.md#legacy-883a82eef8c408fc)｜抓取UTC日期 2026-11-03。
- <a id="ubtech"></a> **ubtech**：[官方/作者原文](https://www.ubtrobot.com/)｜[本地归档](REFERENCES.md#legacy-2c01c36c8e4dfdf1)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
