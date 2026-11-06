# 摩尔线程 Moore Threads — AI 能力

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 框架证据
torch_musa 提供 PyTorch/MUSA 路线，适合测试视觉/Transformer 算子迁移。完整 VLA 需额外验证 FlashAttention、动作采样、Flow Matching/扩散、精度和调度。[moore-musa](#moore-musa)
### 国产生态与生命周期
本轮未找到指定 OpenVLA/π0.5/GR00T 在明确 MTT SKU 上完整端侧性能证据；MUSA 不自动等价 CANN/MindSpore/BPU/RKNN。训练服务器支持也不能推导低功耗本体支持。
可结合通用模型仓库/任务调度构建 MLOps，但自动监控与 OTA 要看系统产品。最低内存、延迟、功耗和闭环任务结果全部待模型级实测。

## 联动报告

- [04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md](../../04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="moore-musa"></a> **moore-musa**：[官方/作者原文](https://raw.githubusercontent.com/MooreThreads/torch_musa/main/README.md)｜[本地归档](REFERENCES.md#legacy-3f88f35d1f10f01a)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
