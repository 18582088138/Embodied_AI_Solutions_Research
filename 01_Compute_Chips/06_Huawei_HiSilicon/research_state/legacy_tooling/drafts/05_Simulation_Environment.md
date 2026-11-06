# 05 仿真环境与合成数据

截至2026-11-05，华为云CloudRobo已提供可操作的仿真开发、轨迹生产和模型评测流程。官方文档直接出现MetaEngine Editor、O3DE prefab、ROS2 Humble、MoveIt/RViz及Robot Importer，证据强于“支持仿真”的产品页。但没有取得引擎完整版本、底层物理求解器配置或同条件性能测量，不把它写成已验证所有本体的专属物理引擎。海思NNIE的指令/模型功能仿真属于神经网络开发工具，不是接触、动力学和相机仿真。{{CloudRobo_SimScene}} {{HiSilicon_DV300_SVP_PDF}}

## 平台关系和开放范围

|路线|交付内容|硬件/资源关系|当前证据边界|
|---|---|---|---|
|CloudRobo预置资产评测|ACT/SO101、场景、任务集、回放|公共或专属仿真资源池|公测申请，不是无条件可用|
|CloudRobo自定义本体|URDF→prefab→MoveIt→轨迹/评测|仅专属池，需购买仿真单元/服务|固定底盘pnp，单/双臂|
|第三方开源机器人描述|UR5e示例工程、ROS2描述/配置包|开发环境、OBS、机器人资产|代码与mesh许可分别待核|
|海思NNIE仿真|网络功能/指令验证|DV300旧SDK工具链|不含机器人physics|
|RLinf Ascend/LIBERO|指定开放模型训练、MuJoCo CPU渲染|910B/CANN9.1.1＋OSMesa|第三方作者路线；非310B支持|
|RLinf Wan世界模型|RGB/动作生成下一观测及奖励|另有world/VAE/reward模型及MindIE-SD依赖|学习环境；不能替代接触物理和真机评估|

“轮式人形”作为双臂构型示例出现，不等于轮式底盘移动、腿部平衡或全身RL已经开放。产品介绍中的双足/人形应用场景是定位说明，具体开放范围以自定义实践为准。{{CloudRobo_SimOverview}} {{CloudRobo_ProductPDF}}

## 从模型描述到可控制资产

{{FIG:CloudRobo_SimOverview}}

此官方图支持工程构建、导入、场景、轨迹、数据、训练、部署、评测的先后关系，没有物理精度或sim-to-real成绩。工程至少包含description、config、gripper_controller、metadata.json、机器人yaml、prefab与robot_profile.yaml。description封装URDF、mesh、launch/RViz；config定义规划组、controller和运动限制；metadata声明必须录制的话题。模型能在RViz显示不等于碰撞或控制配置正确，缺mesh、断开的joint tree及错误package://路径要在导入前解决。{{CloudRobo_SimConfig}} {{CloudRobo_SimImport}}

Robot Importer生成UrdfImporter资产与origin prefab；后处理用机器人yaml给fixed_base、init_joints、控制topic及相机组件补全，避免进入Play时机器人坍塌。fixed_base必须是articulation根节点，不能选中间link。tool_link要在实际指尖末端且轴向符合规划约定；双臂各有独立tool_link。这里示例坐标不能复制给不同夹爪，需用已标定TCP和实际URDF验证。{{CloudRobo_SimScene}}

运动规划组中一个Chain+KDL对应单臂，两个对应双臂；躯干/夹爪用关节组，不能额外配成第三条Chain并期待脚本识别。ROS2 Controllers与MoveIt Controllers的名称、关节顺序一致，输出FollowJointTrajectory。补丁脚本加入OMPL和Pilz，并生成robot_profile.yaml；改动原配置后应重新生成派生产物，不手改内部字段。默认加速度5.0需依真实关节规格调整，YAML数值类型double亦影响ROS参数加载。默认值只是样例，不是该本体安全限值或控制带宽。{{CloudRobo_SimScene}}

夹爪mimic关系当前需展开为独立关节，由controller同步映射；平移式与旋转式关节的width语义不能混同。文档给线性k*x+b开闭映射，模型评测的UR5e例则将两手指位置和乘1250映射0—100，逆向每手指除2500。代码注释仍出现“米”描述，但计算输出是缩放数值，应以正文和实际公式解释，不能把100当100米。映射必须与训练数据处理一致，还需验证非对称手指、饱和和误差。{{CloudRobo_SimEvaluation}}

## 场景、物理与性能

碰撞简化脚本支持decompose与quality high，文档建议先检查AssetProcessor无错、主要link碰撞范围合理和Play帧率，再apply。分析：简化凸包减少接触计算，但可能改变狭缝、抓持和碰撞边界；视觉上稳定或FPS改善都不证明接触力准确。没有取得质量/惯量校验、摩擦、solver iterations、time step、接触容差等完整配置，尤其不能据此评估精密插孔和柔顺控制。{{CloudRobo_SimScene}}

场景通过Movable/Target分类，物品添加ROS2 Frame、抓取/放置位姿和英文任务描述。位姿不可达时应检查IK和坐标，而非盲目增加模型训练数据。算法可规划且执行是轨迹生成的基础，但规划成功、仿真完成与真机完成仍是三个指标。模型控制评测不一定执行同一MoveIt规划链，因此必须分别核对数据生产和策略运行使用的controller。{{CloudRobo_SimTrajectory}}

公开文档没有可对比Isaac Sim、MuJoCo或Gazebo的同硬件physics步率、机器人并行数、render开销和ROS延迟测试。不能宣称“仿真全昇腾加速”或单靠更多NPU获得更高FPS。产品架构明确评测/数据由CCE、训练由ModelArts资源支撑，具体仿真计算资源SKU和CPU/GPU分工要看资源池交付。{{CloudRobo_ProductPDF}}

## 相机、时钟与数据生产

腕部和外部ROS2 Camera Sensor示例均为640×480、10Hz，Frame Name与/camera_image_color话题需一致，RViz检查实际视角。此配置是目标频率，不是physics step或实时达成频率。后续取得O3DE上游ROS2 Gem明确发布/clock并支持非实时仿真时间及/tf、/tf_static；它证明上游机制存在，尚不能确认目标CloudRobo项目的use_sim_time设置、多tick同步、曝光/rolling shutter、畸变及噪声配置。10Hz渲染数据不能直接当真机30Hz策略训练数据而不做时间重采样。{{O3DE_ROS2_Gem}}

轨迹以ros2bag输出，metadata记录关节状态、命令、FollowJointTrajectory反馈与双图。修改metadata后必须刷新/保存task_definition_config.json，才能录制新列表；只修改文件不刷新界面可能造成相机缺失。将bag转LeRobot v3时应检查采样时刻、episode边界、动作与状态错位、归一化统计和失败标签。单条轨迹约一分钟、环境拉起10—15分钟是文档估计，缺硬件/场景统计，不能视为benchmark。专属池轨迹数量1—500、默认3；不是500台并行机器人。{{CloudRobo_SimTrajectory}}

文档可配置Box Shape增广范围、全局随机和预览；范围过大会产生大量不可达失败。这支持物体位置随机化，不证明纹理、光源、质量、摩擦、相机噪声及网络抖动都已统一随机化。应保存随机种子与资产revision，在真实留出场景验证。照片逼真不保证动力学准确，预置可见材质也不证明LiDAR/Radar响应可复现。

## 后续发现：第三方910B训练与世界模型环境

07/08C取得RLinf作者文档，明确Ascend容器agentic-rlinf0.4-maniskill_libero-cann9.1.1对应910B、Ubuntu22.04、arm64/amd64和主机driver映射。LIBERO在Ascend路径用MUJOCO_GL=osmesa与PYOPENGL_PLATFORM=osmesa作CPU渲染，环境并行数因此还受CPU资源限制。不能将NPU训练算力当图形/physics步率，也不能将此路线外推310B和海思SoC。模型、训练、推理rollout及环境可分配到不同资源，复建必须分别记录设备和并发。{{RLinf_Ascend_Container}} {{RLinf_OSMesa_Setup}}

RLinf Wan环境使用初始帧、256×256 RGB、7维动作及chunk8，需要world-model、VAE和reward权重；没有腕部图或本体proprioception。冻结世界模型生成下一观测和奖励，是模型化学习环境，不能替代质量/摩擦/碰撞求解。作者策略表体现指定LIBERO协议下训练前后差异，不是910B仿真速度或sim-to-real收益。Ascend另依赖MindIE-SD兼容组合；优化导入失败可fallback，默认runner.val_check_interval=-1/only_eval=False关闭物理仿真评估，应另开启独立验证并检查策略数值。世界模型误差及奖励漏洞可能放大策略偏差，需要真实/物理留出评测。{{RLinf_Wan_Guide}}

这些文档补齐第三方开放路线，不能称华为自研引擎或CloudRobo与RLinf全部组合已认证。RLinf代码Apache2.0不统一覆盖世界模型、策略权重、LIBERO资产和数据许可。{{RLinf_License}}

## 评测与sim-to-real门槛

官方ACT/SO101实践单任务一场景，公共1—10次、专属1—50次，timeout0—300秒；任务集当前列LIBERO四类，每类十子任务。seed0—10000支持指定场景重现，不能保证跨引擎/驱动bitwise相同。回放有失败/成功区分，但未公开完整成功率分母与测量条件。长耗时回放阈值原文“平均时间75%”存在解释疑义，不能擅自改为P75。{{CloudRobo_BestPractice}}

自定义机器人评测先测连通性，测试时长0.01—300秒，r2c-client RUNNING只证明进程/配置加载；Observation incomplete会skip tick，接口错误与模型能力错误必须分开。文档中的关节名、image key和input_features错误展示有助定位，不能把无报错直接称策略有效。再进入效果评测，记录成功尝试数、失败原因和时长，之后做真实相机标定、系统辨识、负载/摩擦测量与留出任务。{{CloudRobo_SimEvaluation}}

引擎、平台服务、资产/mesh、代码和数据许可分别取件；官方示例仓库API本次受robots限制，未取得源码许可，不用其他路径绕限制。最佳实践合订PDF超过下载器大小限制，未保存截断件；单页正文及官方图已归档，网页静态依赖缺失如实保留partial_static。本次未购买资源或运行仿真，结论是文献和接口核验，不是训练复现与实机迁移验证。
