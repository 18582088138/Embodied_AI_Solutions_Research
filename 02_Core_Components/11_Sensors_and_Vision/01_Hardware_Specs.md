# 传感器与视觉：奥比中光、柯力传感、速腾聚创 — 硬件规格

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 奥比中光
Gemini 335 官方页：主动/被动双目、深度最高 1280×800@30fps、RGB 1920×1080@30fps、深度 FOV 90°×65°、最佳距离 0.26–3m、USB3 Type-C、IMU/触发、97g、平均功耗 <3W。精度指标为 2m、指定 ROI 下空间 RMSE ≤1.5%；不能解释为全距离绝对误差 ≤1.5%。[orbbec-gemini335](#orbbec-gemini335)
### 柯力传感
官网握手/访问失败，未拿到六维力、称重或触觉产品的现行数据手册。量程、过载、非线性、迟滞、串扰、温漂、带宽、重量和 IP 等级均待验证，不把称重传感器的工业经验外推到机器人腕部六维力性能。
### 速腾聚创
AC1 官方页称固态深度+RGB+IMU、时间/空间同步、深度 FOV 120°×60°、RGB 144°×78°、最长 70m、100klux 抗日光及 -20~60℃。1cm@1σ 是 5m 内的测距精度条件；不能与相机 RMSE 百分比直接排行。[robosense-ac1](#robosense-ac1)
其他型号 Airy/E1 等在官网产品线可见，但本轮未逐型号核验规格。[robosense](#robosense)

## 联动报告

- [01_Compute_Chips/01_NVIDIA/03_Sensor_Integration.md](../../01_Compute_Chips/01_NVIDIA/03_Sensor_Integration.md)
- [01_Compute_Chips/02_Intel/03_Sensor_Integration.md](../../01_Compute_Chips/02_Intel/03_Sensor_Integration.md)
- [01_Compute_Chips/05_Rockchip/03_Sensor_Integration.md](../../01_Compute_Chips/05_Rockchip/03_Sensor_Integration.md)
- [05_Software_and_OS/18_Robot_Operating_Systems/02_Hardware_Abstraction.md](../../05_Software_and_OS/18_Robot_Operating_Systems/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="orbbec-gemini335"></a> **orbbec-gemini335**：[官方/作者原文](https://www.orbbec.com/products/stereo-vision-camera/gemini-335/)｜[本地归档](REFERENCES.md#legacy-75ab3e6053df8d2a)｜抓取UTC日期 2026-11-03。
- <a id="robosense-ac1"></a> **robosense-ac1**：[官方/作者原文](https://www.robosense.ai/en/IncrementalComponents/AC1)｜[本地归档](REFERENCES.md#legacy-16d6f04426aed7a1)｜抓取UTC日期 2026-11-03。
- <a id="robosense"></a> **robosense**：[官方/作者原文](https://www.robosense.ai/en)｜[本地归档](REFERENCES.md#legacy-d77c36c05230024c)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
