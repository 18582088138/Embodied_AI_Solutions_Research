# 垂直场景整机：云深处、傅利叶、具微科技 — 算力平台选型

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 云深处
官网列绝影X30、Lite3、山猫M20/S10等；本轮未取得各型号“大脑/小脑”SoC与GPU SKU。四足/轮足运动控制与高级感知可能分域，但这是架构分析，不能填未经证实的Intel/Orin/国产芯片。[deeprobotics](#deeprobotics)
### 傅利叶
FFTAI官方组织存在GR1/GR2/N1/M4等本体与client/模型/仿真仓库；本轮没有公开一致的量产板卡BOM。模型仓库或LeRobot CUDA依赖不能直接证明每个整机内置GPU。[fourier-index](#fourier-index)[fourier-client](#fourier-client)[fourier-lerobot](#fourier-lerobot)
### 具微科技
附件给出公司名，本轮尝试的jvrobot入口仅114字节空内容，无法确认网址归属与产品主体；不以猜测网址作为公司证据。整机、芯片、控制器全部待身份核验。
### 评估建议
巡检/康复/操作各有功耗、温度、防护、控制周期与可靠性要求，应按具体产品和交付配置比较。

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
- <a id="fourier-client"></a> **fourier-client**：[官方/作者原文](https://raw.githubusercontent.com/FFTAI/fourier-grx-client/main/README.md)｜[本地归档](REFERENCES.md#legacy-86c414591546d952)｜抓取UTC日期 2026-11-03。
- <a id="fourier-lerobot"></a> **fourier-lerobot**：[官方/作者原文](https://raw.githubusercontent.com/FFTAI/fourier-lerobot/main/README.md)｜[本地归档](REFERENCES.md#legacy-ad17fb6d02ea5152)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
