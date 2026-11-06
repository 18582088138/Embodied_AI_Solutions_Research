# Arm（IP/架构层） — 独有技术与生态

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 差异化技术
Arm ISA、应用核/实时核设计和 AI 内核优化构成架构生态价值；Thor 与 S100 的不同 CPU 核配置表明 IP 可服务不同计算/实时角色。[arm-kleidi](#arm-kleidi)[nv-thor](#nv-thor)[horizon-s100-doc](#horizon-s100-doc)
### 边界
宽温、抗振、制程、NPU 能力、相机同步和云平台是实现厂商的工程属性。指令扩展可用性必须按 CPU 核与软件检查，不将最新架构特性泛化至旧 A55/A76。
专利授权和商业条款需要合同或专利检索，本轮只给技术层定位。

## 联动报告

- [01_Compute_Chips/01_NVIDIA/01_Hardware_Platform.md](../01_NVIDIA/01_Hardware_Platform.md)
- [01_Compute_Chips/05_Rockchip/01_Hardware_Platform.md](../05_Rockchip/01_Hardware_Platform.md)
- [01_Compute_Chips/08_Horizon_Robotics/01_Hardware_Platform.md](../08_Horizon_Robotics/01_Hardware_Platform.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="arm-kleidi"></a> **arm-kleidi**：[官方/作者原文](https://raw.githubusercontent.com/ARM-software/kleidiai/main/README.md)｜[本地归档](REFERENCES.md#legacy-585ef73974890ad3)｜抓取UTC日期 2026-11-03。
- <a id="nv-thor"></a> **nv-thor**：[官方/作者原文](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-thor/)｜[本地归档](REFERENCES.md#legacy-e6cfb35621d04e69)｜抓取UTC日期 2026-11-03。
- <a id="horizon-s100-doc"></a> **horizon-s100-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs_s/01_Quick_start/01_hardware_introduction/01_rdk_s100.md)｜[本地归档](REFERENCES.md#legacy-81916d180f6f510f)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
