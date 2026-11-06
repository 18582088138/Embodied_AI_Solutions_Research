# 机器人操作系统：ROS 2、AGIROS、智元灵渠 — 开发工具链

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### ROS 2
官方教程、colcon工作流、话题/服务工具与录制回放生态支撑开发；实时调试需测量调度与内存行为。低代码不是ROS2默认能力，GUI产品/商业平台需另行确认。[ros-realtime-rst](#ros-realtime-rst)[ros-release-rst](#ros-release-rst)
### 数据与监控
LeRobot提供示范数据/训练/评估工具，GR00T和openpi有数据schema与微调流程；机器人录制还需统一相机、关节、手部、力传感器时钟，避免只录视频。[lerobot](#lerobot)[nv-gr00t](#nv-gr00t)[openpi](#openpi)
### 其他平台
AimRT公开运行时仓库为智元相关工具线索；AGIROS、灵渠的低代码、标注、监控及许可未核实。TROS文档有零拷贝/开发示例，可评估BPU相关调试。[agibot-aimrt](#agibot-aimrt)[horizon-zerocopy](#horizon-zerocopy)
应固定软件/固件/模型版本并保留失败数据和回滚路径。

### 本轮处理

对无法定位可靠公开资料的具微科技、AGIROS、格物，已按用户指示注明后本轮跳过；保留位置不代表已验证该产品或主体。

## 联动报告

- [02_Core_Components/10_Actuators_and_Reducers/03_Software_Drivers.md](../../02_Core_Components/10_Actuators_and_Reducers/03_Software_Drivers.md)
- [02_Core_Components/11_Sensors_and_Vision/03_Software_Drivers.md](../../02_Core_Components/11_Sensors_and_Vision/03_Software_Drivers.md)
- [02_Core_Components/12_Dexterous_Hands/03_Software_Drivers.md](../../02_Core_Components/12_Dexterous_Hands/03_Software_Drivers.md)
- [04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md](../../04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md)
- [01_Compute_Chips/08_Horizon_Robotics/02_Software_Stack.md](../../01_Compute_Chips/08_Horizon_Robotics/02_Software_Stack.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="ros-realtime-rst"></a> **ros-realtime-rst**：[官方/作者原文](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Tutorials/Demos/Real-Time-Programming.rst)｜[本地归档](REFERENCES.md#legacy-61efa0be808b0c40)｜抓取UTC日期 2026-11-03。
- <a id="ros-release-rst"></a> **ros-release-rst**：[官方/作者原文](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Releases/Release-Jazzy-Jalisco.rst)｜[本地归档](REFERENCES.md#legacy-750d3b1f468ea2e5)｜抓取UTC日期 2026-11-03。
- <a id="lerobot"></a> **lerobot**：[官方/作者原文](https://raw.githubusercontent.com/huggingface/lerobot/main/README.md)｜[本地归档](REFERENCES.md#legacy-cdde66013990b290)｜抓取UTC日期 2026-11-03。
- <a id="nv-gr00t"></a> **nv-gr00t**：[官方/作者原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/main/README.md)｜[本地归档](REFERENCES.md#legacy-ad24537e8616b70d)｜抓取UTC日期 2026-11-03。
- <a id="openpi"></a> **openpi**：[官方/作者原文](https://raw.githubusercontent.com/Physical-Intelligence/openpi/main/README.md)｜[本地归档](REFERENCES.md#legacy-84ef98c9061878e4)｜抓取UTC日期 2026-11-03。
- <a id="agibot-aimrt"></a> **agibot-aimrt**：[官方/作者原文](https://raw.githubusercontent.com/AimRT/AimRT/main/README.md)｜[本地归档](REFERENCES.md#legacy-c18a4a38d0f903b5)｜抓取UTC日期 2026-11-03。
- <a id="horizon-zerocopy"></a> **horizon-zerocopy**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/05_tros_dev/zero_copy.md)｜[本地归档](REFERENCES.md#legacy-77744a5eeb0e6338)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
