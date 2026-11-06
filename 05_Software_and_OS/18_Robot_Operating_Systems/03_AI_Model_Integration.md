# 机器人操作系统：ROS 2、AGIROS、智元灵渠 — AI 模型集成

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### ROS 2
可将感知、策略服务、状态估计和控制节点组合，但不原生“自带OpenVLA/GO-1”。模型服务必须公开输入/输出schema、动作块长度、同步、QoS和超时，底层控制器执行限幅/碰撞/接触约束。[ros-middleware-rst](#ros-middleware-rst)
### 可复用集成路径
openpi提供远程WebSocket推理；GR00T要求把Policy接到目标控制器；宇树VLA提供model server/client。因此ROS2是编排桥梁，模型和控制驱动仍需项目实现。[openpi](#openpi)[gr00t-n16](#gr00t-n16)[unitree-unifolm](#unitree-unifolm)
### AGIROS、灵渠和TROS
前两者本轮未取得通用VLA调度/端到端部署API；AimRT不能替代未披露产品规格。TROS的BPU封装是真实集成线索，但尚不能证明大型VLA完整动作链支持。[agibot-aimrt](#agibot-aimrt)[horizon-tros-doc](#horizon-tros-doc)
待验证：推理线程隔离、动作插值、过期动作拒绝、模型切换和安全回退。

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

- <a id="ros-middleware-rst"></a> **ros-middleware-rst**：[官方/作者原文](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Concepts/Intermediate/About-Different-Middleware-Vendors.rst)｜[本地归档](REFERENCES.md#legacy-fccd19391452e633)｜抓取UTC日期 2026-11-03。
- <a id="openpi"></a> **openpi**：[官方/作者原文](https://raw.githubusercontent.com/Physical-Intelligence/openpi/main/README.md)｜[本地归档](REFERENCES.md#legacy-84ef98c9061878e4)｜抓取UTC日期 2026-11-03。
- <a id="gr00t-n16"></a> **gr00t-n16**：[官方/作者原文](https://raw.githubusercontent.com/NVIDIA/Isaac-GR00T/n1d6/README.md)｜[本地归档](REFERENCES.md#legacy-883a82eef8c408fc)｜抓取UTC日期 2026-11-03。
- <a id="unitree-unifolm"></a> **unitree-unifolm**：[官方/作者原文](https://raw.githubusercontent.com/unitreerobotics/unifolm-vla/main/README.md)｜[本地归档](REFERENCES.md#legacy-b68dedabc807e98f)｜抓取UTC日期 2026-11-03。
- <a id="agibot-aimrt"></a> **agibot-aimrt**：[官方/作者原文](https://raw.githubusercontent.com/AimRT/AimRT/main/README.md)｜[本地归档](REFERENCES.md#legacy-c18a4a38d0f903b5)｜抓取UTC日期 2026-11-03。
- <a id="horizon-tros-doc"></a> **horizon-tros-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/tros.md)｜[本地归档](REFERENCES.md#legacy-2374b38a6f876a21)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
