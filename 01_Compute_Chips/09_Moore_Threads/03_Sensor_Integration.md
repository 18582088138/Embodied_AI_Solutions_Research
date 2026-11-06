# 摩尔线程 Moore Threads — 传感器接入

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 集成路线
MUSA/PyTorch 适配说明 AI 计算路径，不证明原生 ISP、GMSL2、ToF 或 IMU 接口。[moore-musa](#moore-musa)
### 同步和融合
服务器/边缘站方案一般由主机 USB/网络/采集卡接入传感器，再上传 GPU；本体端侧若使用另有模组，应索取其硬件图。此处是候选架构分析而非实测事实。
融合须检查硬件采样时间、PTP、PCIe 拷贝、解码、预处理和队列；共享 CPU/显卡还会影响延迟。
缺口：产品级高速采集、ISP、相机伙伴与跨传感器同步实测。

## 联动报告

- [04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md](../../04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="moore-musa"></a> **moore-musa**：[官方/作者原文](https://raw.githubusercontent.com/MooreThreads/torch_musa/main/README.md)｜[本地归档](REFERENCES.md#legacy-3f88f35d1f10f01a)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
