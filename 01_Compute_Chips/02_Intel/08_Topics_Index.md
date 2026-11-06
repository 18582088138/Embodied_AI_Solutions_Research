# Intel 08 核心技术专题索引

总览建立条件选型地图，三个专题分别追踪编译与内存、实时控制、策略数据与部署契约。完成代表文献和源码核验，不代表实机验收。

- [08_Core_Technology_Moat.md](08_Core_Technology_Moat.md)：总览：优势成立条件、机制对标、系统证据缺口。
- [08A_Heterogeneous_Compilation_and_Data_Residency.md](08A_Heterogeneous_Compilation_and_Data_Residency.md)：A：算子分区、动态shape、USM/Remote Tensor、缓存与ONNX Runtime对标。
- [08B_Real_Time_Isolation_and_Control.md](08B_Real_Time_Isolation_and_Control.md)：B：实时核隔离、CAT、MPC线程、共享内存寿命与控制失效。
- [08C_Policy_Data_and_Deployment_Contracts.md](08C_Policy_Data_and_Deployment_Contracts.md)：C：状态快照、关节标定、模型双文件更换与runtime交接。

模型产物由A进入C，C的时间戳和动作契约必须满足B的控制预算；任何单项优化均不能替代闭环任务和危险响应验证。

联合资料含44个唯一引用来源，42 complete_static、2 partial_static。最后联合复用运行网络请求为0；缺失静态依赖仍存在，不保证动态交互离线复现。

- [08联合资料目录](REFERENCES.md)
- [联合去重记录](research_state/archive_qa/08_Core_Union_dedup_last_run.json)
- [08_Core_Technology_Moat检查](research_state/archive_qa/08_Core_Technology_Moat_quality.json)；[主张证据](research_state/evidence/08_Core_Technology_Moat.json)。
- [08A_Heterogeneous_Compilation_and_Data_Residency检查](research_state/archive_qa/08A_Heterogeneous_Compilation_and_Data_Residency_quality.json)；[主张证据](research_state/evidence/08A_Heterogeneous_Compilation_and_Data_Residency.json)。
- [08B_Real_Time_Isolation_and_Control检查](research_state/archive_qa/08B_Real_Time_Isolation_and_Control_quality.json)；[主张证据](research_state/evidence/08B_Real_Time_Isolation_and_Control.json)。
- [08C_Policy_Data_and_Deployment_Contracts检查](research_state/archive_qa/08C_Policy_Data_and_Deployment_Contracts_quality.json)；[主张证据](research_state/evidence/08C_Policy_Data_and_Deployment_Contracts.json)。

全部四篇逐篇检查pass并完成图像复核；逐篇复用网络请求均0。尚未取得准确SKU的CAT能力/RDT规格正文、真实并发尾延迟与WCET、双产物故障注入/回退、跨样本原子快照和真实闭环收益。旧08_Proprietary_Technologies.md保留为历史稿，不纳入本轮验收。用户审阅状态：待审阅。
