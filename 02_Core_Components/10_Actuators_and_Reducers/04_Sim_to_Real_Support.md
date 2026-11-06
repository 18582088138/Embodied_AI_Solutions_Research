# 执行器与减速器：绿的谐波、汇川技术、鸣志电器 — 仿真支持

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 厂商公开模型状态
三家厂商的高保真关节 MJCF/USD 模型、完整摩擦/效率曲线与电机热模型，本轮均未核实公开可下载。绿的谐波的减速器 CAD 也不能替代可训练的动力学模型；汇川/鸣志电机与驱动器参数须与实际组合一致。[moons2](#moons2)
### 建模路线
机械层：质量、惯量、传动比、回差、弹性与摩擦。电控层：电流/扭矩环、速度限制、饱和、采样与总线延迟。结构层：法兰/负载、线缆与热降额。MuJoCo/Isaac Lab 可承载不同模型，但工具可用不等于厂商模型已高保真。[mujoco](#mujoco)[isaaclab](#isaaclab)
### 精度与效率
大量训练可用简化关节和随机化摩擦/延迟；接触操作、精度验收与热稳定性需要辨识或硬件在环。先记录静摩擦/反驱/连续扭矩测试，再判断是否足够支持 Sim-to-Real。

## 联动报告

- [01_Compute_Chips/02_Intel/02_Software_Stack.md](../../01_Compute_Chips/02_Intel/02_Software_Stack.md)
- [01_Compute_Chips/08_Horizon_Robotics/02_Software_Stack.md](../../01_Compute_Chips/08_Horizon_Robotics/02_Software_Stack.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="moons2"></a> **moons2**：[官方/作者原文](https://www.moons.com.cn/)｜[本地归档](REFERENCES.md#legacy-c3d246b18ed6d14d)｜抓取UTC日期 2026-11-03。
- <a id="mujoco"></a> **mujoco**：[官方/作者原文](https://raw.githubusercontent.com/google-deepmind/mujoco/main/README.md)｜[本地归档](REFERENCES.md#legacy-49e6c5a3a40d667c)｜抓取UTC日期 2026-11-03。
- <a id="isaaclab"></a> **isaaclab**：[官方/作者原文](https://raw.githubusercontent.com/isaac-sim/IsaacLab/main/README.md)｜[本地归档](REFERENCES.md#legacy-6c130dd52b00304e)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
