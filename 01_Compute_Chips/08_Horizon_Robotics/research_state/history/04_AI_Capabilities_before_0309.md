# 地平线 / 地瓜机器人 D-Robotics — AI 能力

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 异构计算定位
TROS 的 hobot dnn 支持 BPU 模型推理封装；S100 的应用 CPU、BPU 与 R52+ 控制域适合分工设计，但控制策略仍需开发。[horizon-tros-doc](#horizon-tros-doc)[horizon-s100-doc](#horizon-s100-doc)
### VLA 与国产工具链
本轮没有取得 OpenVLA/π0.5/GR00T 或 GO-1 在 S100 上完整动作链的官方部署证明。128 TOPS 不代表任何 Transformer 可无损编译；需核验注意力、动态形状、扩散/Flow Matching 与内存带宽。
BPU 工具链是本平台专用，不因国产属性就兼容 CANN/RKNN。MLOps 可在服务器训练、BPU 转换与边端回归中构建，自动模型监控/OTA 的产品范围待验证。

## 联动报告

- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../../05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md)
- [04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md](../../04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md)
- [02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md](../../02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="horizon-tros-doc"></a> **horizon-tros-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/tros.md)｜[本地归档](../../_Evidence/horizon-tros-doc.txt)｜抓取UTC日期 2026-11-03。
- <a id="horizon-s100-doc"></a> **horizon-s100-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs_s/01_Quick_start/01_hardware_introduction/01_rdk_s100.md)｜[本地归档](../../_Evidence/horizon-s100-doc.txt)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
