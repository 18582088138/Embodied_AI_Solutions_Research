# 08专题导航与验收

截止2026-11-05。总览与三个专题均完成公开资料核验、逐图查看和结构/归档检查；待用户审阅。没有进行SDK安装或实机测试。

| 报告 | 机制与交接 | 主要边界 | 检查 |
|---|---|---|---|
| [08_Core_Technology_Moat](08_Core_Technology_Moat.md) | 能力/证据地图、优势与可替代性 | 同条件任务/商业闭包未取得 | [pass](research_state/qa/08_Core_Technology_Moat_check.json) |
| [08A_Compute_Compilation_and_Quantization](08A_Compute_Compilation_and_Quantization.md) | 模型→校准→HBIR/HBO/HBM→UCP任务 | 质量/shape/核数/版本绑定 | [pass](research_state/qa/08A_Compute_Compilation_and_Quantization_check.json) |
| [08B_Sensor_Memory_and_Time](08B_Sensor_Memory_and_Time.md) | 采样→共享buffer→张量→消息/策略 | 所有权/cache/回调寿命；同步SKU冲突 | [pass](research_state/qa/08B_Sensor_Memory_and_Time_check.json) |
| [08C_Real_Time_Trust_and_Lifecycle](08C_Real_Time_Trust_and_Lifecycle.md) | 有界指令→MCU→故障恢复/更新 | WCET/安全认证/密钥/商业源码未完成 | [pass](research_state/qa/08C_Real_Time_Trust_and_Lifecycle_check.json) |

## 资料与版本边界

[08联合资料集合](REFERENCES.md) · [联合引用清单](research_state/manifests/Horizon_08_union.json) · [零网络复用记录](research_state/qa/08_union_last_run.json)

联合集合覆盖总览及A/B/C实际引用和图源，共43份登记资料；H08_Isaac_Safety正文有效、两项静态依赖缺失。动态手册正文由已归档JS离线渲染，各篇证据JSON保存页面URL与原件/正文/HTML哈希。集合是检索入口，详细动态正文链接位于各篇引用。

S6005.1.1与OE/TROS5.1.0绑定说明仍需成套回归。S100同步正文不能直接套S600；旧miniboot回退描述与当前直写机制冲突已保留。源码、二进制、权重/数据及IP许可分别核查，商业包未取得。

[旧08稿（保留）](08_Proprietary_Technologies.md)；未改名或删除。当前研究以新总览与三个专题为准。
