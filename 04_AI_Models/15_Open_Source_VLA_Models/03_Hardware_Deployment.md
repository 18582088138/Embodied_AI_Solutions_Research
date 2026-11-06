# 开源 VLA：OpenVLA、π0.5、GR00T N1.6/N1.7 — 硬件部署与算力需求

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### OpenVLA：推荐 GPU 路线，最低 TOPS 未成立
原版7B参数仅BF16权重理论约14GB（7×10^9×2字节，十进制），尚未计激活、视觉编码、缓存、ROS及并发感知。这是容量估算，**不是运行最低内存**。仓库支持量化/LoRA路线，LoRA示例为A100 80GB、说明小GPU约27GB起；不把微调内存当推理要求。[openvla](#openvla)
Orin 64GB 可列为待测试候选，不声称原版已经达到任意闭环频率；8GB Nano 不因67TOPS就自动可承载原版。
### π0.5：CUDA 基线与 OpenVINO 迁移
openpi 官方估算推理 >8GB、LoRA >22.5GB、全参微调 >70GB，分别示例 RTX4090、RTX4090、A100/H100。这是仓库特定实现估算，不是所有端侧板最低要求。[openpi](#openpi)
Intel 官方提供 ONNX/OpenVINO/NNCF 转换；CPU benchmark 命令与随机输入对比尚非 NPU 全模型或实机任务验收。[intel-pi05](#intel-pi05)
### GR00T：版本化性能
N1.6 分支 torch.compile 表：Thor 105ms/9.5Hz、RTX4090 44ms/22.8Hz；N1.7 主线宣称 TensorRT Thor约28Hz（batch-1 LIBERO/MAXN）。环境和版本不同，不能直接将差异归因硬件提升。[gr00t-n16](#gr00t-n16)[nv-gr00t](#nv-gr00t)
N1.7 推理建议16GB+；微调40GB+。[nv-gr00t](#nv-gr00t)
### 国产芯片
本轮没有三模型完整 RKNN/CANN/BPU/MUSA/MLU 原生部署证据。可列移植候选，但必须检查动作头、算子、量化质量和完整闭环。所有平台的功耗与p95/p99延迟未实測。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md](../../01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md)
- [01_Compute_Chips/02_Intel/04_AI_Capabilities.md](../../01_Compute_Chips/02_Intel/04_AI_Capabilities.md)
- [01_Compute_Chips/05_Rockchip/04_AI_Capabilities.md](../../01_Compute_Chips/05_Rockchip/04_AI_Capabilities.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/03_AI_Model_Integration.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/03_AI_Model_Integration.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="openvla"></a> **openvla**：[官方/作者原文](https://raw.githubusercontent.com/openvla/openvla/main/README.md)｜[本地归档](REFERENCES.md#legacy-46401c1b519322c8)｜抓取UTC日期 2026-11-03。
- <a id="openpi"></a> **openpi**：[官方/作者原文](https://raw.githubusercontent.com/Physical-Intelligence/openpi/main/README.md)｜[本地归档](REFERENCES.md#legacy-84ef98c9061878e4)｜抓取UTC日期 2026-11-03。
- <a id="intel-pi05"></a> **intel-pi05**：[官方/作者原文](https://developer.robotics.intel.com/development-stack/ai_resources/openvino/pi05-optimization/)｜[本地归档](REFERENCES.md#legacy-f909b858f4fd1b24)｜抓取UTC日期 2026-11-03。
- <a id="gr00t-n16"></a> **gr00t-n16**：[官方/作者原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/n1d6/README.md)｜[本地归档](REFERENCES.md#legacy-883a82eef8c408fc)｜抓取UTC日期 2026-11-03。
- <a id="nv-gr00t"></a> **nv-gr00t**：[官方/作者原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/README.md)｜[本地归档](REFERENCES.md#legacy-ad24537e8616b70d)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
