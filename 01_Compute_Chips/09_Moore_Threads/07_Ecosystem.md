# 摩尔线程 Moore Threads — 生态建设

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 公开生态
MUSA SDK/torch_musa 与 KUAE 等计算形态构成国产 GPU 生态入口；机器人专项软件与外设伙伴仍需补证。[moorethreads](#moorethreads)[moore-musa](#moore-musa)
### 商业和自主可控
适合评估国内训练/推理基础设施，量产机器人需看端侧模组、供货、驱动维护和总拥有成本。设计、制造、封装、显存和软件依赖应拆分检查。
不提供未经核验的机器人装机占比、成本优势或国产替代率；这些需要独立行业数据、报价和客户证据。

## 联动报告

- [04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md](../../04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="moorethreads"></a> **moorethreads**：[官方/作者原文](https://www.mthreads.com/)｜[本地归档](REFERENCES.md#legacy-044615b4e08a41c9)｜抓取UTC日期 2026-11-03。
- <a id="moore-musa"></a> **moore-musa**：[官方/作者原文](https://raw.githubusercontent.com/MooreThreads/torch_musa/main/README.md)｜[本地归档](REFERENCES.md#legacy-3f88f35d1f10f01a)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
