# 地平线 / 地瓜机器人 D-Robotics — 独有技术与生态

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 技术组合
Nash BPU、应用核+R52+ 控制域与 TROS/hobot dnn/零拷贝形成差异化组合，重点在感知与实时域协同。[horizon-s100-doc](#horizon-s100-doc)[horizon-tros-doc](#horizon-tros-doc)[horizon-zerocopy](#horizon-zerocopy)
### 工程边界
零拷贝降低部分消息搬运，不保证任意网络负载下微秒级端到端时延。锁步控制核是硬件能力线索，认证和安全软件仍需单独证据。
未核验独占机器人云、专属数据集或全部专利壁垒；高抗振、宽温与量产可靠性应按产品级文件判断。

## 联动报告

- [05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md](../../05_Software_and_OS/18_Robot_Operating_Systems/01_Architecture_and_Communication.md)
- [04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md](../../04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md)
- [02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md](../../02_Core_Components/10_Actuators_and_Reducers/02_Interface_and_Communication.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="horizon-s100-doc"></a> **horizon-s100-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs_s/01_Quick_start/01_hardware_introduction/01_rdk_s100.md)｜[本地归档](REFERENCES.md#legacy-81916d180f6f510f)｜抓取UTC日期 2026-11-03。
- <a id="horizon-tros-doc"></a> **horizon-tros-doc**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/tros.md)｜[本地归档](REFERENCES.md#legacy-2374b38a6f876a21)｜抓取UTC日期 2026-11-03。
- <a id="horizon-zerocopy"></a> **horizon-zerocopy**：[官方/作者原文](https://raw.githubusercontent.com/D-Robotics/rdk_doc/main/docs/05_Robot_development/05_tros_dev/zero_copy.md)｜[本地归档](REFERENCES.md#legacy-77744a5eeb0e6338)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
