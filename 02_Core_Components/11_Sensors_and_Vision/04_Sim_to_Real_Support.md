# 传感器与视觉：奥比中光、柯力传感、速腾聚创 — 仿真支持

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 奥比中光
可用深度/RGB、内参外参与噪声校准构建传感器模型，但本轮未核实 Gemini 335 厂商提供完整、校准后的 USD/Isaac 插件。SDK 驱动不是物理传感器仿真模型。[orbbec-sdk](#orbbec-sdk)[orbbec-gemini335](#orbbec-gemini335)
### 柯力传感
六维力仿真需要传感器坐标、串扰/偏置、饱和、滤波、温漂和安装柔性，本轮没有厂商提供的公开高保真模型。
### 速腾聚创
AC1 官方页宣传数据/算法生态，但数据集区域仍含“将提供”表述；不能将页面入口视为数据已可下载。传统扫描 LiDAR 仿真也不能自动代表 AC1 固态深度模式。[robosense-ac1](#robosense-ac1)
### 迁移方法
先用理想相机/力传感器快速训练，再加入曝光/飞点/反光/时延、扫描和零漂随机化。针对透明、镜面、黑色物体和快速运动单独做现实压力测试；高保真模型以标定数据为依据。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/03_Sensor_Integration.md](../../01_Compute_Chips/01_NVIDIA/03_Sensor_Integration.md)
- [01_Compute_Chips/02_Intel/03_Sensor_Integration.md](../../01_Compute_Chips/02_Intel/03_Sensor_Integration.md)
- [01_Compute_Chips/05_Rockchip/03_Sensor_Integration.md](../../01_Compute_Chips/05_Rockchip/03_Sensor_Integration.md)
- [05_Software_and_OS/18_Robot_Operating_Systems/02_Hardware_Abstraction.md](../../05_Software_and_OS/18_Robot_Operating_Systems/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="orbbec-sdk"></a> **orbbec-sdk**：[官方/作者原文](https://raw.githubusercontent.com/orbbec/OrbbecSDK_v2/main/README.md)｜[本地归档](REFERENCES.md#legacy-15e3eb17ad4d0050)｜抓取UTC日期 2026-11-03。
- <a id="orbbec-gemini335"></a> **orbbec-gemini335**：[官方/作者原文](https://www.orbbec.com/products/stereo-vision-camera/gemini-335/)｜[本地归档](REFERENCES.md#legacy-75ab3e6053df8d2a)｜抓取UTC日期 2026-11-03。
- <a id="robosense-ac1"></a> **robosense-ac1**：[官方/作者原文](https://www.robosense.ai/en/IncrementalComponents/AC1)｜[本地归档](REFERENCES.md#legacy-16d6f04426aed7a1)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
