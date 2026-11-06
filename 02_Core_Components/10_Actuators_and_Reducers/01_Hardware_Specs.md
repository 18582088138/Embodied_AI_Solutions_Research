# 执行器与减速器：绿的谐波、汇川技术、鸣志电器 — 硬件规格

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 绿的谐波
应按机械谐波减速器、机电一体化关节分开调研；不能对机械减速器填 NPU 算力或通信协议。本轮两个官网入口均返回网关超时，未得到现行型号、额定/峰值扭矩、回差、寿命、重量和 IP 等级，暂列为待取样/待索取规格。
### 汇川技术
官网首页确认公司主体，但本轮没有可读伺服产品手册。交流伺服、低压驱动、工业控制器和一体化关节是不同选型，暂不填写传闻型号参数。[inovance2](#inovance2)
### 鸣志电器
官网列步进、低压/交流伺服、闭环步进、MDX+ 集成式伺服、直线执行产品及 IP65 电机线索；防护等级不能推广到全系列。精确扭矩、响应时间与重量需逐 SKU 数据手册。[moons2](#moons2)
### 共同评估口径
记录额定/峰值扭矩、持续热负荷、传动比、回差、扭转刚度、反驱性、效率、惯量、编码器与制动器。峰值扭矩不能当长期输出，减速器精度也不能直接代表整机末端精度。

## 联动报告

- [01_Compute_Chips/02_Intel/02_Software_Stack.md](../../01_Compute_Chips/02_Intel/02_Software_Stack.md)
- [01_Compute_Chips/08_Horizon_Robotics/02_Software_Stack.md](../../01_Compute_Chips/08_Horizon_Robotics/02_Software_Stack.md)
- [03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md](../../03_Robot_Manufacturers/13_Full_Stack_Integrators/02_Core_Component_Supply_Chain.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="inovance2"></a> **inovance2**：[官方/作者原文](https://www.inovance.com/)｜[本地归档](REFERENCES.md#legacy-ba5b20a44bdb39b9)｜抓取UTC日期 2026-11-03；仅主体/导航级证据。
- <a id="moons2"></a> **moons2**：[官方/作者原文](https://www.moons.com.cn/)｜[本地归档](REFERENCES.md#legacy-c3d246b18ed6d14d)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
