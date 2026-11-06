# Intel 具身智能软硬件平台全套审阅索引

数据截止：2026-11-05（Asia/Shanghai）。01—09已完成文献、官方图和源码核验；本轮连续完成03—09及08A/B/C，保留01、02和原专题索引。完成不代表用户批准，当前仅01有用户批准记录，02及03—09待审阅。

## 按01—09阅读

- [01_Hardware_Platform.md](01_Hardware_Platform.md)：硬件与采购：逐SKU、芯片/载板/整机、接口、功率与供货边界。
- [02_Software_Stack.md](02_Software_Stack.md)：软件总览：系统/BSP、OpenVINO、策略、ROS、控制、Studio交接。
- [03_Sensor_Integration.md](03_Sensor_Integration.md)：传感器：接线、时间戳、buffer、带宽、同步和背压。
- [04_AI_Capabilities.md](04_AI_Capabilities.md)：AI模型：LLM/VLM/VLA、动作表示、量化部署与性能条件。
- [05_Simulation_Environment.md](05_Simulation_Environment.md)：仿真：Gazebo/MuJoCo、时间步、传感器误差与迁移缺口。
- [06_Robot_Integration.md](06_Robot_Integration.md)：本体与商业案例：Ella、Oversonic等公告及Jackal/UR5e适配。
- [07_Ecosystem.md](07_Ecosystem.md)：生态与量产：伙伴分工、载板、BIOS服务、交付和维护。
- [08_Core_Technology_Moat.md](08_Core_Technology_Moat.md)：技术总览：异构编译/驻留、实时隔离、策略部署契约。
- [09_SWOT_Analysis.md](09_SWOT_Analysis.md)：SWOT与选型：IFR2026、Q3财报、TCO情景及场景放行矩阵。

## 深度专题与资料

- [02专题索引](02_Topics_Index.md)：六篇软件专题及联合归档。
- [08专题索引](08_Topics_Index.md)：异构编译和数据驻留、实时隔离和控制、策略数据和部署契约三篇。
- [项目唯一资料库](REFERENCES.md)；[02软件资料集合](REFERENCES.md)；[08核心技术集合](REFERENCES.md)。
- [最终审计记录](research_state/archive_qa/03_09_Final_Audit.json)；[进度与审阅状态](research_state/progress.json)。

## 本轮验收记录

- [03_Sensor_Integration检查](research_state/archive_qa/03_Sensor_Integration_quality.json)：pass，1733有效汉字，17引用，1图；[证据](research_state/evidence/03_Sensor_Integration.json)；[零网络复用记录](research_state/archive_qa/03_Sensor_Integration_dedup_last_run.json)。
- [04_AI_Capabilities检查](research_state/archive_qa/04_AI_Capabilities_quality.json)：pass，1924有效汉字，20引用，1图；[证据](research_state/evidence/04_AI_Capabilities.json)；[零网络复用记录](research_state/archive_qa/04_AI_Capabilities_dedup_last_run.json)。
- [05_Simulation_Environment检查](research_state/archive_qa/05_Simulation_Environment_quality.json)：pass，1743有效汉字，15引用，1图；[证据](research_state/evidence/05_Simulation_Environment.json)；[零网络复用记录](research_state/archive_qa/05_Simulation_Environment_dedup_last_run.json)。
- [06_Robot_Integration检查](research_state/archive_qa/06_Robot_Integration_quality.json)：pass，1877有效汉字，7引用，1图；[证据](research_state/evidence/06_Robot_Integration.json)；[零网络复用记录](research_state/archive_qa/06_Robot_Integration_dedup_last_run.json)。
- [07_Ecosystem检查](research_state/archive_qa/07_Ecosystem_quality.json)：pass，1943有效汉字，21引用，1图；[证据](research_state/evidence/07_Ecosystem.json)；[零网络复用记录](research_state/archive_qa/07_Ecosystem_dedup_last_run.json)。
- [08A_Heterogeneous_Compilation_and_Data_Residency检查](research_state/archive_qa/08A_Heterogeneous_Compilation_and_Data_Residency_quality.json)：pass，1898有效汉字，18引用，1图；[证据](research_state/evidence/08A_Heterogeneous_Compilation_and_Data_Residency.json)；[零网络复用记录](research_state/archive_qa/08A_Heterogeneous_Compilation_and_Data_Residency_dedup_last_run.json)。
- [08B_Real_Time_Isolation_and_Control检查](research_state/archive_qa/08B_Real_Time_Isolation_and_Control_quality.json)：pass，2022有效汉字，7引用，1图；[证据](research_state/evidence/08B_Real_Time_Isolation_and_Control.json)；[零网络复用记录](research_state/archive_qa/08B_Real_Time_Isolation_and_Control_dedup_last_run.json)。
- [08C_Policy_Data_and_Deployment_Contracts检查](research_state/archive_qa/08C_Policy_Data_and_Deployment_Contracts_quality.json)：pass，1993有效汉字，12引用，1图；[证据](research_state/evidence/08C_Policy_Data_and_Deployment_Contracts.json)；[零网络复用记录](research_state/archive_qa/08C_Policy_Data_and_Deployment_Contracts_dedup_last_run.json)。
- [08_Core_Technology_Moat检查](research_state/archive_qa/08_Core_Technology_Moat_quality.json)：pass，2086有效汉字，22引用，1图；[证据](research_state/evidence/08_Core_Technology_Moat.json)；[零网络复用记录](research_state/archive_qa/08_Core_Technology_Moat_dedup_last_run.json)。
- [09_SWOT_Analysis检查](research_state/archive_qa/09_SWOT_Analysis_quality.json)：pass，3284有效汉字，19引用，1图；[证据](research_state/evidence/09_SWOT_Analysis.json)；[零网络复用记录](research_state/archive_qa/09_SWOT_Analysis_dedup_last_run.json)。

本轮10篇正文共20,503有效汉字，106个唯一registry来源标识（91 complete_static、15 partial_static）。来源标识/资料数量不是独立研究机构数量或事实强度评分。所有正文图均有实际查看记录。部分网页呈现依赖缺失，正文有效，不保证视频/登录/动态交互离线复现。结构与归档检查不自动证明实机性能或商业收益。

## 重要结论与缺口

Intel的可评估价值在x86/ROS工程资产、集成异构推理和已有本体蓝图；优势依赖准确系统内存/驱动、算子覆盖、热稳定和任务接口。取消独显是特定客户公告，不能推广到所有模型。H100上的SnapFlow时延不是Intel测试；cyclictest示例不是72小时结果；策略调用、伺服频率与真实任务成功率分别核验。

未取得目标系统报价、逐P/N生命周期/SLA、满路传感器并发与长期任务指标，不能给Intel机器人份额、TCO排名或ROI。IFR2026统计提供不同机器人类别市场分母；CCPG财报名称不提供机器人单独收入。欧盟机械逐条法规与GDPR原文空白挑战不纳有效引用，委员会说明可归档；中国法规全文和端侧SKU出口分类仍待取得。08的RDT规格正文、原子状态/双产物回退故障验收也未闭环。各篇正文保留版本、许可与成熟度边界。

旧08_Proprietary_Technologies.md保留为历史稿，不纳本轮验收；旧09在research_state/revisions保留。正式量产、安全/医疗适用、供货与财务收益需由项目方取得目标系统和合同证据。
