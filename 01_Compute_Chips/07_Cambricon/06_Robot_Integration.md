# 寒武纪 Cambricon — 机器人本体适配

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 整机终端
本轮没有获得指定整机采用具体 MLU SKU 的公开技术栈。AI 计算市场应用不等于机器人本体集成。[cambricon](#cambricon)
### 控制判断
若用于云端/边缘站推理，本体仍需本地状态估计和安全控制；网络动作块必须有超时、限幅和回退。逆运动学、全身规划、顺应控制属于额外的软件和本体能力，不能从加速器品牌推导。
缺口：机器人参考设计、低延迟通信、控制周期和物理安全认证。

## 联动报告

- [04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md](../../04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md)
- [05_Software_and_OS/20_Full_Stack_Cloud_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/20_Full_Stack_Cloud_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="cambricon"></a> **cambricon**：[官方/作者原文](https://www.cambricon.com/)｜[本地归档](REFERENCES.md#legacy-da6ed1e6ee3b0489)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
