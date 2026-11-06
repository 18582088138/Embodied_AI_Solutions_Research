# 开源 VLA：OpenVLA、π0.5、GR00T N1.6/N1.7 — 多模态能力

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### OpenVLA
原版核心输入为图像/语言、输出机器人动作，跨本体动作归一化需选正确统计键；不能因视觉输入可见物体接触就宣称原生触觉/六维力融合。[openvla](#openvla)[openvla-paper](#openvla-paper)
### π0.5
包含多视角视觉、语言与机器人状态的策略路线，支持动作块和高层语义；具体摄像头数量、state/action 维度随配置。openpi 的公开样例不能证明任意触觉数据即插即用。[openpi](#openpi)
### GR00T N1.6/N1.7
采用视觉/语言及本体状态建模，N1.7 强调人类视频预训练和相对末端动作表征。触觉/力觉需要检查数据 schema、编码器和训练覆盖，不从“多模态”名称推断。[gr00t-n16](#gr00t-n16)[nv-gr00t](#nv-gr00t)
### 数据协同
相机时间戳、力传感器坐标系与关节命令一致性决定数据质量。对因时等灵巧手需区分控制轴与关节数，并核验模型手部动作映射。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md](../../01_Compute_Chips/01_NVIDIA/04_AI_Capabilities.md)
- [01_Compute_Chips/02_Intel/04_AI_Capabilities.md](../../01_Compute_Chips/02_Intel/04_AI_Capabilities.md)
- [01_Compute_Chips/05_Rockchip/04_AI_Capabilities.md](../../01_Compute_Chips/05_Rockchip/04_AI_Capabilities.md)
- [05_Software_and_OS/19_Simulation_Training_Platforms/03_AI_Model_Integration.md](../../05_Software_and_OS/19_Simulation_Training_Platforms/03_AI_Model_Integration.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="openvla"></a> **openvla**：[官方/作者原文](https://raw.githubusercontent.com/openvla/openvla/main/README.md)｜[本地归档](REFERENCES.md#legacy-46401c1b519322c8)｜抓取UTC日期 2026-11-03。
- <a id="openvla-paper"></a> **openvla-paper**：[官方/作者原文](https://arxiv.org/html/2406.09246v3)｜[本地归档](REFERENCES.md#legacy-eae40e7a4f090282)｜抓取UTC日期 2026-11-03。
- <a id="openpi"></a> **openpi**：[官方/作者原文](https://raw.githubusercontent.com/Physical-Intelligence/openpi/main/README.md)｜[本地归档](REFERENCES.md#legacy-84ef98c9061878e4)｜抓取UTC日期 2026-11-03。
- <a id="gr00t-n16"></a> **gr00t-n16**：[官方/作者原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/n1d6/README.md)｜[本地归档](REFERENCES.md#legacy-883a82eef8c408fc)｜抓取UTC日期 2026-11-03。
- <a id="nv-gr00t"></a> **nv-gr00t**：[官方/作者原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/README.md)｜[本地归档](REFERENCES.md#legacy-ad24537e8616b70d)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
