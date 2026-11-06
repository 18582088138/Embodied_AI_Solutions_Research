# 寒武纪 Cambricon — SWOT 分析

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 优势
- MLU220-SOM/M.2有明确INT8算力、功耗和接口规格。[cambricon-mlu220-som](#cambricon-mlu220-som)[cambricon-mlu220-m2](#cambricon-mlu220-m2)
- NeuWare/MagicMind给出云边端/图编译和多精度路线。[cambricon-neuware](#cambricon-neuware)[cambricon-magicmind](#cambricon-magicmind)
- 可纳入国产边缘推理及训练平台迁移评估。[cambricon-torch](#cambricon-torch)
### 劣势、机会与风险
劣势：边缘产品时效/供货、最新工具对220兼容、完整VLA和本体驱动缺证。机会：固定视觉/轻量边缘模型、国产服务器算法迁移。风险：把旧边缘规格或云端训练能力外推到大型端侧VLA。
### 适用建议
220可列轻量边缘推理候选，先核验生命周期/工具版本；大型VLA需实测，不以16TOPS或云边端口号代替。

## 联动报告

- [04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md](../../04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md)
- [05_Software_and_OS/20_Full_Stack_Cloud_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/20_Full_Stack_Cloud_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="cambricon-mlu220-som"></a> **cambricon-mlu220-som**：[官方/作者原文](https://www.cambricon.com/index.php?m=content&c=index&a=lists&catid=56)｜[本地归档](REFERENCES.md#legacy-5596ebfce51310b1)｜抓取UTC日期 2026-11-03。
- <a id="cambricon-mlu220-m2"></a> **cambricon-mlu220-m2**：[官方/作者原文](https://www.cambricon.com/index.php?m=content&c=index&a=lists&catid=57)｜[本地归档](REFERENCES.md#legacy-1bd739a38b050b37)｜抓取UTC日期 2026-11-03。
- <a id="cambricon-neuware"></a> **cambricon-neuware**：[官方/作者原文](https://www.cambricon.com/index.php?m=content&c=index&a=lists&catid=71)｜[本地归档](REFERENCES.md#legacy-b2602f3ca42cd59e)｜抓取UTC日期 2026-11-03。
- <a id="cambricon-magicmind"></a> **cambricon-magicmind**：[官方/作者原文](https://www.cambricon.com/index.php?m=content&c=index&a=lists&catid=378)｜[本地归档](REFERENCES.md#legacy-507ef5f6358a433f)｜抓取UTC日期 2026-11-03。
- <a id="cambricon-torch"></a> **cambricon-torch**：[官方/作者原文](https://raw.githubusercontent.com/Cambricon/torch_mlu/master/README.md)｜[本地归档](REFERENCES.md#legacy-437d0b3bb443dbeb)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
