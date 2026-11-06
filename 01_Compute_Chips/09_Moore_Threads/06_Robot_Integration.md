# 摩尔线程 Moore Threads — 机器人本体适配

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 终端证据
本轮未得到指定机器人采用 MTT GPU 的完整技术栈证据；官网产品应用分类不能代替整机 SKU/BOM。[moorethreads](#moorethreads)
### 运动与交互
训练/边缘 GPU 站可服务任务理解与策略生成，但本体仍需本地控制、安全和掉线回退。逆运动学、全身控制和顺应控制的软件支持要按库/设备测量，不能从 PyTorch 支持自动推导。[moore-musa](#moore-musa)
缺口：RRD、关节控制网关、确定性延迟和标杆客户任务验收。

## 联动报告

- [04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md](../../04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="moorethreads"></a> **moorethreads**：[官方/作者原文](https://www.mthreads.com/)｜[本地归档](REFERENCES.md#legacy-044615b4e08a41c9)｜抓取UTC日期 2026-11-03。
- <a id="moore-musa"></a> **moore-musa**：[官方/作者原文](https://raw.githubusercontent.com/MooreThreads/torch_musa/main/README.md)｜[本地归档](REFERENCES.md#legacy-3f88f35d1f10f01a)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
