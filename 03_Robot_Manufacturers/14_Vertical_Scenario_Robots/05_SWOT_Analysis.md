# 垂直场景整机：云深处、傅利叶、具微科技 — SWOT 与技术栈

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 云深处
技术栈：X30/Lite3/M20等 → 算力未知 → 关节/传感SKU与自研比例未知 → OS/控制链待证 → 通用VLA待证。产品场景布局明确；工业可靠性和真实成本需要验收材料，不能给未知部分评级。[deeprobotics](#deeprobotics)
### 傅利叶
技术栈：GR系列等 → 算力未知 → 本体/硬件仓库线索（量产BOM未知） → client与MuJoCo/LeRobot接口 → 默认VLA未知。优势是公开本体开发入口；短板是型号/分支与量产配置映射需进一步确认。[fourier-index](#fourier-index)[fourier-client](#fourier-client)[fourier-models](#fourier-models)[fourier-mujoco](#fourier-mujoco)
### 具微科技
身份未核实，整机—芯片—部件—OS—VLA均保留未知；不以同名公司或域名猜测构建技术栈。
### 场景建议
云深处按工业巡检/移动任务尽调；傅利叶将康复业务与人形开发分别评估。机会是明确的场景需求，风险为定制交付、维护、人机安全及模型泛化；最终推荐须明确产品和现场指标。

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
- <a id="fourier-models"></a> **fourier-models**：[官方/作者原文](https://raw.githubusercontent.com/FFTAI/Wiki-GRx-Models/master/README.md)｜[本地归档](REFERENCES.md#legacy-d90f8d484041b74f)｜抓取UTC日期 2026-11-03。
- <a id="fourier-mujoco"></a> **fourier-mujoco**：[官方/作者原文](https://raw.githubusercontent.com/FFTAI/Wiki-GRx-Mujoco/FourierN1/README.md)｜[本地归档](REFERENCES.md#legacy-8b2bfc857be41db0)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
