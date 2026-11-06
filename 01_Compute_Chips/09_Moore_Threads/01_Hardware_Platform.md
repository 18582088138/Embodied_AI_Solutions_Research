# 摩尔线程 Moore Threads — 硬件平台

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 可核实产品线
官网导航列 MTT S5000/S4000/S3000 等计算产品及 KUAE、SGX5000、AICUBE/AIBOOK 等形态；torch_musa 提供软件适配入口。[moorethreads](#moorethreads)[moore-musa](#moore-musa)
### 指标与定位
本轮未取得明确机器人低功耗 SOM 数据手册，不把服务器 GPU 卡当作 Jetson 类端侧模块。各 SKU 的 FP 精度/稀疏算力、GPU 架构、显存、制程、TDP、主机 CPU 和冷却要求待核实。
适合先区分训练服务器、边缘站或本体端侧，再判断体积、电池和接口限制。

## 联动报告

- [04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md](../../04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="moorethreads"></a> **moorethreads**：[官方/作者原文](https://www.mthreads.com/)｜[本地归档](REFERENCES.md#legacy-044615b4e08a41c9)｜抓取UTC日期 2026-11-03。
- <a id="moore-musa"></a> **moore-musa**：[官方/作者原文](https://raw.githubusercontent.com/MooreThreads/torch_musa/main/README.md)｜[本地归档](REFERENCES.md#legacy-3f88f35d1f10f01a)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
