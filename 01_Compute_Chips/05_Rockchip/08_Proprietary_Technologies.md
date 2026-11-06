# 瑞芯微 Rockchip — 独有技术与生态

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 差异化组合
RK3588 的多媒体/ISP、高速 I/O 与三核 NPU，加上 RKNN/RKLLM，构成成本敏感嵌入式 AI 的技术组合。[rk3588](#rk3588)[rk-rknn](#rk-rknn)[rk-llm](#rk-llm)
### 工程边界
RKLLM 的多模态运行路径值得评估，但并未提供通用全身控制或动作生成接口。多核 NPU 性能利用率依模型切分、带宽和算子；峰值算力不能代替流水线延迟。
宽温、抗振、实时确定性和专属云平台未取得统一芯片级承诺；需看工业板卡产品文件。未对专利作独占性判断。

## 联动报告

- [04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md](../../04_AI_Models/15_Open_Source_VLA_Models/03_Hardware_Deployment.md)
- [05_Software_and_OS/18_Robot_Operating_Systems/02_Hardware_Abstraction.md](../../05_Software_and_OS/18_Robot_Operating_Systems/02_Hardware_Abstraction.md)
- [02_Core_Components/11_Sensors_and_Vision/03_Software_Drivers.md](../../02_Core_Components/11_Sensors_and_Vision/03_Software_Drivers.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="rk3588"></a> **rk3588**：[官方/作者原文](https://www.rock-chips.com/a/en/products/RK35_Series/2022/0926/1660.html)｜[本地归档](REFERENCES.md#legacy-73f573c2d6db595d)｜抓取UTC日期 2026-11-03。
- <a id="rk-rknn"></a> **rk-rknn**：[官方/作者原文](https://raw.githubusercontent.com/airockchip/rknn-toolkit2/master/README.md)｜[本地归档](REFERENCES.md#legacy-25a303718864388d)｜抓取UTC日期 2026-11-03。
- <a id="rk-llm"></a> **rk-llm**：[官方/作者原文](https://raw.githubusercontent.com/airockchip/rknn-llm/main/README.md)｜[本地归档](REFERENCES.md#legacy-076b3673843a058b)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
