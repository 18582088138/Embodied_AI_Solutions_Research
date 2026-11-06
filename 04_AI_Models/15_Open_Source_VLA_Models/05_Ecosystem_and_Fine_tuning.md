# 开源 VLA：OpenVLA、π0.5、GR00T N1.6/N1.7 — 生态与微调

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### OpenVLA
代码与预训练权重许可分开：仓库提醒权重继承底层 Llama Community License 限制，不能因代码是宽松协议就认定全部权重无条件商用。支持LoRA、数据格式/归一化与全参训练路径。[openvla](#openvla)
### π0.5/openpi
openpi 仓库许可证为 Apache-2.0，但仍需独立检查checkpoint、训练数据和第三方模型条款；有 JAX/PyTorch、数据转换、远程 WebSocket 推理与微调配置。[openpi](#openpi)[openpi-license](#openpi-license)
### GR00T
N1.7 主线声明 Apache-2.0 商用许可并提供权重/参考代码；N1.6 代码许可与权重/data条款仍按目标资产单独检查。N1.7称使用20K小时EgoScale视频预训练，数量是开发方说明，并不证明数据可全部下载。[nv-gr00t](#nv-gr00t)[gr00t-n16](#gr00t-n16)
### 社区成熟度
本轮未采集固定时刻star/贡献者/issue响应统计，不给主观“最活跃”排名。更应评价维护版本、可复现训练、数据许可、目标本体示例和模型回归。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md](../../01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md)
- [01_Compute_Chips/02_Intel/04_AI_Capabilities.md](../../01_Compute_Chips/02_Intel/04_AI_Capabilities.md)
- [01_Compute_Chips/05_Rockchip/04_AI_Capabilities.md](../../01_Compute_Chips/05_Rockchip/04_AI_Capabilities.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/03_AI_Model_Integration.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/03_AI_Model_Integration.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="openvla"></a> **openvla**：[官方/作者原文](https://raw.githubusercontent.com/openvla/openvla/main/README.md)｜[本地归档](REFERENCES.md#legacy-46401c1b519322c8)｜抓取UTC日期 2026-11-03。
- <a id="openpi"></a> **openpi**：[官方/作者原文](https://raw.githubusercontent.com/Physical-Intelligence/openpi/main/README.md)｜[本地归档](REFERENCES.md#legacy-84ef98c9061878e4)｜抓取UTC日期 2026-11-03。
- <a id="openpi-license"></a> **openpi-license**：[官方/作者原文](https://raw.githubusercontent.com/Physical-Intelligence/openpi/main/LICENSE)｜[本地归档](REFERENCES.md#legacy-5f6c9f60e1f50352)｜抓取UTC日期 2026-11-03。
- <a id="nv-gr00t"></a> **nv-gr00t**：[官方/作者原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/README.md)｜[本地归档](REFERENCES.md#legacy-ad24537e8616b70d)｜抓取UTC日期 2026-11-03。
- <a id="gr00t-n16"></a> **gr00t-n16**：[官方/作者原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/n1d6/README.md)｜[本地归档](REFERENCES.md#legacy-883a82eef8c408fc)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
