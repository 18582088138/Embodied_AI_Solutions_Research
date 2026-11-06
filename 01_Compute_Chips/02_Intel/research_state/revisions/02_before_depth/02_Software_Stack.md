# Intel — 软件栈

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 开发栈
Robotics AI Suite 组织 ROS 2、感知/导航、运动控制和 Physical AI 相关工作流；OpenVINO 是模型优化与推理工具，CPU/GPU/NPU 的实际支持需核对模型算子和设备插件。[intel-robotics](#intel-robotics)[intel-openvino](#intel-openvino)
π0.5 官方教程展示 PyTorch → ONNX → OpenVINO IR → NNCF INT8 权重压缩，并给出 benchmark_app CPU 示例。[intel-pi05](#intel-pi05)
### 接口与部署判断
EtherCAT 主站、运动网关与实时配置属于整机的软件/网卡组合；MIPI/GMSL 则依主板或采集卡。x86 平台有 PCIe/USB 扩展便利，但不能把每个 Core Ultra 机器都视为相同 I/O 能力。
固定 Ubuntu、ROS、OpenVINO、Python 和固件版本，再检验驱动和模型转换；未完成本轮全 SKU 的硬件兼容矩阵。

## 联动报告

- [04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md](../../04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md)
- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../../05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md)
- [02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md](../../02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="intel-robotics"></a> **intel-robotics**：[官方/作者原文](https://raw.githubusercontent.com/open-edge-platform/robotics-ai-suite/main/README.md)｜[本地归档](../../_Evidence/intel-robotics.txt)｜抓取UTC日期 2026-11-03。
- <a id="intel-openvino"></a> **intel-openvino**：[官方/作者原文](https://docs.openvino.ai/2026/index.html)｜[本地归档](../../_Evidence/intel-openvino.txt)｜抓取UTC日期 2026-11-03。
- <a id="intel-pi05"></a> **intel-pi05**：[官方/作者原文](https://developer.robotics.intel.com/development-stack/ai_resources/openvino/pi05-optimization/)｜[本地归档](../../_Evidence/intel-pi05.txt)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
