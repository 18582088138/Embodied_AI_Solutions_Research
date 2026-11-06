# 摩尔线程 Moore Threads — 软件栈

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 官方工具路线
torch_musa 是 PyTorch 的 MUSA 适配项目，官网列 MUSA SDK 等开发工具；模型使用需固定 MUSA、驱动和 PyTorch 版本。[moore-musa](#moore-musa)[moorethreads](#moorethreads)
### 驱动与接口
与 CUDA 的源码迁移关系不等于二进制即插即用。ROS 2 可在主机组织感知/动作流程，PCIe AI 卡本身不提供所有相机/工业总线接口；EtherCAT、CAN-FD 与 MIPI 由主机或外部板负责。
缺口：机器人专用 Runtime、完整 VLA 编译/转换流程、BSP 与工业驱动支持矩阵。

## 联动报告

- [04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md](../../04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="moore-musa"></a> **moore-musa**：[官方/作者原文](https://raw.githubusercontent.com/MooreThreads/torch_musa/main/README.md)｜[本地归档](REFERENCES.md#legacy-3f88f35d1f10f01a)｜抓取UTC日期 2026-11-03。
- <a id="moorethreads"></a> **moorethreads**：[官方/作者原文](https://www.mthreads.com/)｜[本地归档](REFERENCES.md#legacy-044615b4e08a41c9)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
