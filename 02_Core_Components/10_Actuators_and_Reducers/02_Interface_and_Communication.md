# 执行器与减速器：绿的谐波、汇川技术、鸣志电器 — 接口与通信

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 绿的谐波
纯机械减速器通过法兰、轴、轴承与电机连接，不具备 EtherCAT/CAN-FD。只有含控制器的关节模组才能讨论总线，必须确认具体型号和驱动器。
### 汇川技术
应索取伺服系列的 EtherCAT/CANopen/脉冲等版本、CiA402/对象字典、周期与同步支持。本轮首页不足以验证具体协议，不能把公司具备工业自动化业务推导为所有关节支持 CAN-FD。[inovance2](#inovance2)
### 鸣志电器
官网导航列 EtherCAT、EtherNet/IP、CANopen、Modbus/RTU 产品路径；这是产品线范围，不能说明每个驱动器同时支持全部协议。**CANopen 与 CAN-FD 不是同义词。**[moons2](#moons2)
### 对接算力平台
Intel/NVIDIA/RK/S100 主机需通过主站软件、网卡或 CAN 控制器/收发器与驱动器连接；核对电源、电平、隔离、端子、急停/使能与时钟同步。机械供应商关系与电子驱动器关系分开建图。

## 联动报告

- [01_Compute_Chips/02_Intel/02_Software_Stack.md](../../01_Compute_Chips/02_Intel/02_Software_Stack.md)
- [01_Compute_Chips/08_Horizon_Robotics/02_Software_Stack.md](../../01_Compute_Chips/08_Horizon_Robotics/02_Software_Stack.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="inovance2"></a> **inovance2**：[官方/作者原文](https://www.inovance.com/)｜[本地归档](REFERENCES.md#legacy-ba5b20a44bdb39b9)｜抓取UTC日期 2026-11-03；仅主体/导航级证据。
- <a id="moons2"></a> **moons2**：[官方/作者原文](https://www.moons.com.cn/)｜[本地归档](REFERENCES.md#legacy-c3d246b18ed6d14d)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
