# 垂直场景整机：云深处、傅利叶、具微科技 — 核心零部件供应链

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 云深处
官网产品线证明四足/轮足布局，但没有完整关节、减速器、电机、LiDAR/深度相机和手部供应名单。自研关节比例/外采比例、国产化率不填推测数字。[deeprobotics](#deeprobotics)
### 傅利叶
官方组织含本体模型、硬件与手部/执行器SDK线索，可作为下一步工程资料入口；开源模型不证明关节制造及传感器100%自研。[fourier-index](#fourier-index)[fourier-models](#fourier-models)
### 具微科技
主体未确认，暂无可验证零部件/供应链来源。
### 联动验证
分别记录减速器设计/制造、电机、编码器、驱动器、灵巧手控制、传感ASIC与本体装配；和绿的谐波/汇川/鸣志/奥比/柯力/速腾的实际关系需要官方双边技术/采购证据。风险评估看备件、校准、交期与批量一致性。

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
- <a id="fourier-index"></a> **fourier-index**：[官方/作者原文](https://api.github.com/orgs/FFTAI/repos?per_page=100)｜[本地归档](REFERENCES.md#legacy-cb239fcb9857ceed)｜抓取UTC日期 2026-11-03。
- <a id="fourier-models"></a> **fourier-models**：[官方/作者原文](https://raw.githubusercontent.com/FFTAI/Wiki-GRx-Models/master/README.md)｜[本地归档](REFERENCES.md#legacy-d90f8d484041b74f)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
