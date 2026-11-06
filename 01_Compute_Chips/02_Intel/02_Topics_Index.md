# 02 Intel 软件专题索引

截止2026-11-05；第02章已完成文献/源码及归档检查，等待用户审阅。01已通过审阅；03—09未推进。

建议先阅读[软件栈总览](02_Software_Stack.md)，再按以下顺序进入专题。正文包含官方URL、本地原件表、官方图与验证边界。

| 专题 | 研究对象 | 主要机制/产物交接 | 版本与证据缺口 |
|---|---|---|---|
| [02A 系统、BSP与执行域](02A_System_BSP_and_Execution.md) | 系统、BSP与执行域 | loader→用户态runtime→kernel→firmware；镜像/包交接 | Suite2025.3与通用新版驱动分开；载板BSP仍需正式交付 |
| [02B 转换、量化与异构推理](02B_OpenVINO_Compilation_and_Heterogeneous_Runtime.md) | 转换、量化与异构推理 | Model→CompiledModel→InferRequest；AUTO/HETERO、remote tensor/cache | NPU动态shape/CIP版本条件；zero-copy与fallback需目标实测 |
| [02C VLA与PhysicalAI运行](02C_Physical_AI_Model_Pipelines.md) | VLA与PhysicalAI运行 | manifest/stats/pre-post→chunk→Execution/Queue→RobotRuntime | 旧pi05 forward语义、LeRobot未锁；停止与急停不同 |
| [02D ROS感知、空间计算与导航](02D_ROS_Perception_and_Navigation.md) | ROS感知、空间计算与导航 | Image/PointCloud2→TF/map→Nav2 Path/cmd_vel；queue/context | ITS不支持continuous replanning；IMU包限制与内部APT示例 |
| [02E 实时控制、仿真与运维](02E_Control_Simulation_and_Operations.md) | 实时控制、仿真与运维 | RVC/Servo、PLCopen、ENI/PDO、shared ring buffer、session日志 | 控制周期仅配置；Pick仿真绕过感知；无完整OTA回退证据 |
| [02F Studio数据与训练](02F_Physical_AI_Studio_Data_and_Training.md) | Studio数据与训练 | LeRobot episode→checkpoint→export/manifest→runtime bundle；远程job | store可混样；grace move不导出；SnapFlow测量在H100 |

## 检查与归档入口

每篇研究正文至少1500有效汉字，逐篇保存SHA256基线、证据JSON、质量检查及零网络复用记录。检查通过只确认结构与归档；没有安装SDK、训练、模型转换或本体测试。

| 文件 | 有效汉字 | 引用数 | 官方图 | 检查 | 证据 | 去重记录 |
|---|---|---|---|---|---|---|
| [02_Software_Stack](02_Software_Stack.md) | 1993 | 41 | 1 | [pass](research_state/archive_qa/02_Software_Stack_quality.json) | [JSON](research_state/evidence/02_Software_Stack.json) | [0网络](research_state/archive_qa/02_Software_Stack_dedup_last_run.json) |
| [02A_System_BSP_and_Execution](02A_System_BSP_and_Execution.md) | 2029 | 14 | 1 | [pass](research_state/archive_qa/02A_System_BSP_and_Execution_quality.json) | [JSON](research_state/evidence/02A_System_BSP_and_Execution.json) | [0网络](research_state/archive_qa/02A_System_BSP_and_Execution_dedup_last_run.json) |
| [02B_OpenVINO_Compilation_and_Heterogeneous_Runtime](02B_OpenVINO_Compilation_and_Heterogeneous_Runtime.md) | 2604 | 24 | 1 | [pass](research_state/archive_qa/02B_OpenVINO_Compilation_and_Heterogeneous_Runtime_quality.json) | [JSON](research_state/evidence/02B_OpenVINO_Compilation_and_Heterogeneous_Runtime.json) | [0网络](research_state/archive_qa/02B_OpenVINO_Compilation_and_Heterogeneous_Runtime_dedup_last_run.json) |
| [02C_Physical_AI_Model_Pipelines](02C_Physical_AI_Model_Pipelines.md) | 2206 | 24 | 1 | [pass](research_state/archive_qa/02C_Physical_AI_Model_Pipelines_quality.json) | [JSON](research_state/evidence/02C_Physical_AI_Model_Pipelines.json) | [0网络](research_state/archive_qa/02C_Physical_AI_Model_Pipelines_dedup_last_run.json) |
| [02D_ROS_Perception_and_Navigation](02D_ROS_Perception_and_Navigation.md) | 1872 | 17 | 1 | [pass](research_state/archive_qa/02D_ROS_Perception_and_Navigation_quality.json) | [JSON](research_state/evidence/02D_ROS_Perception_and_Navigation.json) | [0网络](research_state/archive_qa/02D_ROS_Perception_and_Navigation_dedup_last_run.json) |
| [02E_Control_Simulation_and_Operations](02E_Control_Simulation_and_Operations.md) | 1743 | 18 | 1 | [pass](research_state/archive_qa/02E_Control_Simulation_and_Operations_quality.json) | [JSON](research_state/evidence/02E_Control_Simulation_and_Operations.json) | [0网络](research_state/archive_qa/02E_Control_Simulation_and_Operations_dedup_last_run.json) |
| [02F_Physical_AI_Studio_Data_and_Training](02F_Physical_AI_Studio_Data_and_Training.md) | 1929 | 17 | 1 | [pass](research_state/archive_qa/02F_Physical_AI_Studio_Data_and_Training_quality.json) | [JSON](research_state/evidence/02F_Physical_AI_Studio_Data_and_Training.json) | [0网络](research_state/archive_qa/02F_Physical_AI_Studio_Data_and_Training_dedup_last_run.json) |

引用联合清单覆盖总览和六篇专题，共112个有效资料名称，原件通过[唯一registry](REFERENCES.md)管理；[02专题集合](REFERENCES.md)复用原件，非第二套下载。

- [联合资料清单](research_state/manifests/Intel_02_Software_Union.json)
- [联合去重证据](research_state/archive_qa/02_Software_Union_dedup_last_run.json)
- [官方图来源与视觉复核](research_state/figures_02.json)
- [章节续接状态](research_state/progress.json)

## 完整链与剩余验证

视觉链交接模型IR、图像/点云buffer、ROS消息/TF/map、Path/cmd_vel或grasp/Servo；策略链交接示教/统计量、checkpoint、manifest与tokenizer、chunk/队列、关节/时间契约。两条链在OS驱动、设备、内存、控制与观测层汇合，独立demo没有被当作一个已测系统。

关键待验收项为逐SKU编译/driver/firmware组合、旧pi05推理入口、NPU并发尾延迟、队列/样本一致性、下游停止、历史仿真迁移、真实任务分母及更新回退。供货和许可按代码、固件、模型、数据、资产、本体SDK分别核对；性能条件不完整或测试在其他硬件的结果均保留边界。

联合清单含111个唯一URL（112个引用名称，其中同URL别名复用）；111个名称complete_static、1个partial_static。部分归档为 Intel_ARK_Core5320（产品页静态依赖缺失，以registry为准），不影响已核正文，但不承诺离线交互或像素级一致。
