# 执行器与减速器：绿的谐波、汇川技术、鸣志电器 — 软件驱动

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 厂商证据
绿的谐波：本轮未得到公开维护的 ROS 2 驱动或关节 API。
汇川技术：官网入口可读，但未抓到可验证的 ROS 2 包、工业总线主站库或调试手册。[inovance2](#inovance2)
鸣志电器：公开产品导航可帮助定位伺服与总线版本，未取得具体 ROS 2 驱动证据。[moons2](#moons2)
### 软件适配判断
ROS 2 驱动常由整机或系统集成商编写；厂商的 Windows 调试软件、EtherCAT ESI 文件、CAN 对象字典与 ROS 2 驱动分别交付。通用 ros2_control 框架不自动生成设备接口。
采购应索取寄存器/对象字典、固件版本、回零/限位、单位和符号约定、故障码及 SDK 许可；现场测量多轴并发周期、超时与恢复。不能把某社区 demo 的单轴运行写成厂商量产维护承诺。

## 联动报告

- [01_Compute_Chips/02_Intel/02_Software_Stack.md](../../01_Compute_Chips/02_Intel/02_Software_Stack.md)
- [01_Compute_Chips/08_Horizon_Robotics/02_Software_Stack.md](../../01_Compute_Chips/08_Horizon_Robotics/02_Software_Stack.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="inovance2"></a> **inovance2**：[官方/作者原文](https://www.inovance.com/)｜[本地归档](REFERENCES.md#legacy-ba5b20a44bdb39b9)｜抓取UTC日期 2026-11-03；仅主体/导航级证据。
- <a id="moons2"></a> **moons2**：[官方/作者原文](https://www.moons.com.cn/)｜[本地归档](REFERENCES.md#legacy-c3d246b18ed6d14d)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
