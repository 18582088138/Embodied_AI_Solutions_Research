# 寒武纪 Cambricon — 仿真环境

调研日期：2026-11-03（Asia/Shanghai）｜版本：首轮公开资料研究｜结论状态：含未披露/待验证项

## 研究发现

### 证据边界
现有官网与 torch_mlu 不证明官方机器人物理引擎或 Isaac Sim 渲染支持。[cambricon](#cambricon)[cambricon-torch](#cambricon-torch)
### 推荐验证
仿真工作站与 MLU 训练/部署机器可以分工；核对强化学习训练框架与 MLU 算子的覆盖，不将“支持 PyTorch”理解成所有仿真 GPU 后端可用。[isaaclab](#isaaclab)[mujoco](#mujoco)
缺口：高保真场景生成、域随机化工具、官方本体资产及从仿真迁移到寒武纪端侧设备的任务结果。

## 联动报告

- [04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md](../../04_AI_Models/16_Domestic_Open_Source_Models/03_Hardware_Deployment.md)
- [05_Software_and_OS/20_Full_Stack_Cloud_Platforms/02_Hardware_Abstraction.md](../../05_Software_and_OS/20_Full_Stack_Cloud_Platforms/02_Hardware_Abstraction.md)

交叉引用用于关联主题；只有正文或[关系图谱](../../knowledge-graph.json)中标为已验证的关系才代表实际采用/支持，不代表全部量产配置。

## 来源与证据边界

- <a id="cambricon"></a> **cambricon**：[官方/作者原文](https://www.cambricon.com/)｜[本地归档](REFERENCES.md#legacy-da6ed1e6ee3b0489)｜抓取UTC日期 2026-11-03。
- <a id="cambricon-torch"></a> **cambricon-torch**：[官方/作者原文](https://raw.githubusercontent.com/Cambricon/torch_mlu/master/README.md)｜[本地归档](REFERENCES.md#legacy-437d0b3bb443dbeb)｜抓取UTC日期 2026-11-03。
- <a id="isaaclab"></a> **isaaclab**：[官方/作者原文](https://raw.githubusercontent.com/isaac-sim/IsaacLab/main/README.md)｜[本地归档](REFERENCES.md#legacy-6c130dd52b00304e)｜抓取UTC日期 2026-11-03。
- <a id="mujoco"></a> **mujoco**：[官方/作者原文](https://raw.githubusercontent.com/google-deepmind/mujoco/main/README.md)｜[本地归档](REFERENCES.md#legacy-49e6c5a3a40d667c)｜抓取UTC日期 2026-11-03。

厂商性能/数据规模属于其公开报告；本研究没有进行实机、模型运行或客户验收测试。未取得数据不等于该能力不存在。判断与推荐遵循[研究方法](../../METHODOLOGY.md)。
