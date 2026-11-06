# 全栈整机：宇树科技、智元机器人、优必选 — 核心零部件供应链

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 宇树
G1参数披露低惯量PMSM、双编码器、三指Dex3-1（可选触觉）、深度相机+LiDAR；这些证明部件类型，不能证明所有部件完全自研或指定供应商。标准/EDU关节数、扭矩与附件不同。[unitree-g1](#unitree-g1)
### 智元
AgiBot World采集平台介绍移动双臂、6DoF手、视觉触觉硬件；这是数据采集硬件说明，不是全部量产系列的供应BOM。[agibot-go1](#agibot-go1)
### 优必选
官网整机产品定位不能直接给出减速器、电机、灵巧手/传感器供应比例。[ubtech](#ubtech)
### 待核实比例
三家的自研/外采比例、国产化率、绿的谐波/汇川/鸣志/因时/奥比等供应关系均需SKU级技术资料、公告或采购证明。自研算法、关节设计、零件制造和整机装配是不同层次，避免用“全栈自研”给所有部件填100%。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md](../../01_Compute_Chips/01_NVIDIA/06_Robot_Integration.md)
- [02_Core_Components/10_Actuators_and_Reducers/05_Market_Position.md](../../02_Core_Components/10_Actuators_and_Reducers/05_Market_Position.md)
- [02_Core_Components/12_Dexterous_Hands/01_Hardware_Specs.md](../../02_Core_Components/12_Dexterous_Hands/01_Hardware_Specs.md)
- [04_AI_Models/16_Domestic_Open_Source_Models/01_Model_Architecture.md](../../04_AI_Models/16_Domestic_Open_Source_Models/01_Model_Architecture.md)
- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../../05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="unitree-g1"></a> **unitree-g1**：[官方/作者原文](https://www.unitree.com/g1)｜[本地归档](REFERENCES.md#legacy-a3cc1c668e3bab25)｜抓取UTC日期 2026-11-03。
- <a id="agibot-go1"></a> **agibot-go1**：[官方/作者原文](https://raw.githubusercontent.com/OpenDriveLab/AgiBot-World/main/README.md)｜[本地归档](REFERENCES.md#legacy-f37440765f4db2fd)｜抓取UTC日期 2026-11-03。
- <a id="ubtech"></a> **ubtech**：[官方/作者原文](https://www.ubtrobot.com/)｜[本地归档](REFERENCES.md#legacy-2c01c36c8e4dfdf1)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
