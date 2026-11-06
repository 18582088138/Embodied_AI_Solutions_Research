# 地平线 / 地瓜机器人 D-Robotics — SWOT 分析

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 优势
- S100 公布 BPU 与实时控制域的同平台设计。[horizon-s100-doc](#horizon-s100-doc)
- TROS/BPU 封装、零拷贝和 CAN 文档公开。[horizon-tros-doc](#horizon-tros-doc)[horizon-zerocopy](#horizon-zerocopy)[horizon-can](#horizon-can)
- 硬件与软件资料可以支撑国内机器人原型验证。
### 劣势、机会与风险
劣势：大型 VLA 算子/内存/动作头尚需验证；工具链迁移与第三方驱动有工作量。机会：国内移动机器人、感知与控制协同、小型端侧策略。风险：混淆地平线汽车业务和地瓜机器人，误读 TOPS 或锁步能力。
### 适用建议
作为国产端侧 PoC 优先候选之一；大型 VLA 先验证完整模型而非只跑视觉网络。

## 联动报告

- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../../05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md)
- [04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md](../../04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md)
- [02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md](../../02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="horizon-s100-doc"></a> **horizon-s100-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs_s/01_Quick_start/01_hardware_introduction/01_rdk_s100.md)｜[本地归档](../../_Evidence/horizon-s100-doc.txt)｜抓取UTC日期 2026-11-03。
- <a id="horizon-tros-doc"></a> **horizon-tros-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/tros.md)｜[本地归档](../../_Evidence/horizon-tros-doc.txt)｜抓取UTC日期 2026-11-03。
- <a id="horizon-zerocopy"></a> **horizon-zerocopy**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/05_tros_dev/zero_copy.md)｜[本地归档](../../_Evidence/horizon-zerocopy.txt)｜抓取UTC日期 2026-11-03。
- <a id="horizon-can"></a> **horizon-can**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/07_Advanced_development/01_hardware_development/rdk_x5/can.md)｜[本地归档](../../_Evidence/horizon-can.txt)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
