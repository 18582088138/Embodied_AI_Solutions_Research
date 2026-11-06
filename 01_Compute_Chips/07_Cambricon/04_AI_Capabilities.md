# 寒武纪 Cambricon — AI 能力

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 公开计算工具
NeuWare与MagicMind提供训练/推理开发、跨框架图转换、量化和动态形状等能力说明；PyTorch/MLU适配可作为模型迁移入口，但每个SKU的算子/版本需验证。[cambricon-neuware](#cambricon-neuware)[cambricon-magicmind](#cambricon-magicmind)[cambricon-torch](#cambricon-torch)
### 端侧边界
MLU220-SOM16TOPS INT8/8GB，M.2卡8TOPS，与云端训练卡能力不同。尚未取得OpenVLA/π0.5/GR00T完整220端侧部署、动作质量或功耗实测。[cambricon-mlu220-som](#cambricon-mlu220-som)[cambricon-mlu220-m2](#cambricon-mlu220-m2)
视觉主干、注意力、动作采样、回退层和内存分别核验；NeuWare“云边端一体”并不证明所有MLOps、OTA或机器人控制都已交付。CANN/RKNN/MindSpore与MLU也不天然互通。

## 联动报告

- [04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md](../../04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md)
- [05_Software_and_OS/20_Full_Stack_Cloud_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/20_Full_Stack_Cloud_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="cambricon-neuware"></a> **cambricon-neuware**：[官方/作者原文](https://www.cambricon.com/index.php?m=content&c=index&a=lists&catid=71)｜[本地归档](REFERENCES.md#legacy-b2602f3ca42cd59e)｜抓取UTC日期 2026-11-03。
- <a id="cambricon-magicmind"></a> **cambricon-magicmind**：[官方/作者原文](https://www.cambricon.com/index.php?m=content&c=index&a=lists&catid=378)｜[本地归档](REFERENCES.md#legacy-507ef5f6358a433f)｜抓取UTC日期 2026-11-03。
- <a id="cambricon-torch"></a> **cambricon-torch**：[官方/作者原文](https://raw.githubusercontent.com/Cambricon/torch_mlu/master/README.md)｜[本地归档](REFERENCES.md#legacy-437d0b3bb443dbeb)｜抓取UTC日期 2026-11-03。
- <a id="cambricon-mlu220-som"></a> **cambricon-mlu220-som**：[官方/作者原文](https://www.cambricon.com/index.php?m=content&c=index&a=lists&catid=56)｜[本地归档](REFERENCES.md#legacy-5596ebfce51310b1)｜抓取UTC日期 2026-11-03。
- <a id="cambricon-mlu220-m2"></a> **cambricon-mlu220-m2**：[官方/作者原文](https://www.cambricon.com/index.php?m=content&c=index&a=lists&catid=57)｜[本地归档](REFERENCES.md#legacy-1bd739a38b050b37)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
