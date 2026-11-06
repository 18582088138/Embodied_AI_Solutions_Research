# 05 仿真环境与合成数据

截至2026-11-05，华为云CloudRobo已提供可操作的仿真开发、轨迹生产和模型评测流程。官方文档直接出现MetaEngine Editor、O3DE prefab、ROS2 Humble、MoveIt/RViz及Robot Importer，证据强于“支持仿真”的产品页。但没有取得引擎完整版本、底层物理求解器配置或同条件性能测量，不把它写成已验证所有本体的专属物理引擎。海思NNIE的指令/模型功能仿真属于神经网络开发工具，不是接触、动力学和相机仿真。[CloudRobo_SimScene](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0054.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_SimS--86a564346774003e/index.html)） [HiSilicon_DV300_SVP_PDF](https://www.hisilicon.com/dam/asset/view/4ef2e012655a4aae8c80619b8cfd093f.pdf/download)（[本地原件](../../../reference_metrial/documents/HiSilicon_DV3--8b4b0448c818638c/document.pdf)）

## 平台关系和开放范围

|路线|交付内容|硬件/资源关系|当前证据边界|
|---|---|---|---|
|CloudRobo预置资产评测|ACT/SO101、场景、任务集、回放|公共或专属仿真资源池|公测申请，不是无条件可用|
|CloudRobo自定义本体|URDF→prefab→MoveIt→轨迹/评测|仅专属池，需购买仿真单元/服务|固定底盘pnp，单/双臂|
|第三方开源机器人描述|UR5e示例工程、ROS2描述/配置包|开发环境、OBS、机器人资产|代码与mesh许可分别待核|
|海思NNIE仿真|网络功能/指令验证|DV300旧SDK工具链|不含机器人physics|

“轮式人形”作为双臂构型示例出现，不等于轮式底盘移动、腿部平衡或全身RL已经开放。产品介绍中的双足/人形应用场景是定位说明，具体开放范围以自定义实践为准。[CloudRobo_SimOverview](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0056.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_SimO--c41c4d38b76d89b5/index.html)） [CloudRobo_ProductPDF](https://support.huaweicloud.com/productdesc-cloudrobo/CloudRobo%20%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D-pdf.pdf)（[本地原件](../../../reference_metrial/documents/CloudRobo_Pro--522f065088effec2/document.pdf)）

## 从模型描述到可控制资产

![官方自定义机器人仿真开发流程](../../../reference_metrial/_registry/assets/images/d52c4746aa32a851b5e0172a.png)

此官方图支持工程构建、导入、场景、轨迹、数据、训练、部署、评测的先后关系，没有物理精度或sim-to-real成绩。工程至少包含description、config、gripper_controller、metadata.json、机器人yaml、prefab与robot_profile.yaml。description封装URDF、mesh、launch/RViz；config定义规划组、controller和运动限制；metadata声明必须录制的话题。模型能在RViz显示不等于碰撞或控制配置正确，缺mesh、断开的joint tree及错误package://路径要在导入前解决。[CloudRobo_SimConfig](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0052.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_SimC--90d1e31c1d0016f8/index.html)） [CloudRobo_SimImport](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0053.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_SimI--547c06d0d7c62063/index.html)）

Robot Importer生成UrdfImporter资产与origin prefab；后处理用机器人yaml给fixed_base、init_joints、控制topic及相机组件补全，避免进入Play时机器人坍塌。fixed_base必须是articulation根节点，不能选中间link。tool_link要在实际指尖末端且轴向符合规划约定；双臂各有独立tool_link。这里示例坐标不能复制给不同夹爪，需用已标定TCP和实际URDF验证。[CloudRobo_SimScene](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0054.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_SimS--86a564346774003e/index.html)）

运动规划组中一个Chain+KDL对应单臂，两个对应双臂；躯干/夹爪用关节组，不能额外配成第三条Chain并期待脚本识别。ROS2 Controllers与MoveIt Controllers的名称、关节顺序一致，输出FollowJointTrajectory。补丁脚本加入OMPL和Pilz，并生成robot_profile.yaml；改动原配置后应重新生成派生产物，不手改内部字段。默认加速度5.0需依真实关节规格调整，YAML数值类型double亦影响ROS参数加载。默认值只是样例，不是该本体安全限值或控制带宽。[CloudRobo_SimScene](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0054.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_SimS--86a564346774003e/index.html)）

夹爪mimic关系当前需展开为独立关节，由controller同步映射；平移式与旋转式关节的width语义不能混同。文档给线性k*x+b开闭映射，模型评测的UR5e例则将两手指位置和乘1250映射0—100，逆向每手指除2500。代码注释仍出现“米”描述，但计算输出是缩放数值，应以正文和实际公式解释，不能把100当100米。映射必须与训练数据处理一致，还需验证非对称手指、饱和和误差。[CloudRobo_SimEvaluation](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0057.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_SimE--ed5202e058aafdf3/index.html)）

## 场景、物理与性能

碰撞简化脚本支持decompose与quality high，文档建议先检查AssetProcessor无错、主要link碰撞范围合理和Play帧率，再apply。分析：简化凸包减少接触计算，但可能改变狭缝、抓持和碰撞边界；视觉上稳定或FPS改善都不证明接触力准确。没有取得质量/惯量校验、摩擦、solver iterations、time step、接触容差等完整配置，尤其不能据此评估精密插孔和柔顺控制。[CloudRobo_SimScene](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0054.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_SimS--86a564346774003e/index.html)）

场景通过Movable/Target分类，物品添加ROS2 Frame、抓取/放置位姿和英文任务描述。位姿不可达时应检查IK和坐标，而非盲目增加模型训练数据。算法可规划且执行是轨迹生成的基础，但规划成功、仿真完成与真机完成仍是三个指标。模型控制评测不一定执行同一MoveIt规划链，因此必须分别核对数据生产和策略运行使用的controller。[CloudRobo_SimTrajectory](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0055.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_SimT--5b5e7f2ba9864e13/index.html)）

公开文档没有可对比Isaac Sim、MuJoCo或Gazebo的同硬件physics步率、机器人并行数、render开销和ROS延迟测试。不能宣称“仿真全昇腾加速”或单靠更多NPU获得更高FPS。产品架构明确评测/数据由CCE、训练由ModelArts资源支撑，具体仿真计算资源SKU和CPU/GPU分工要看资源池交付。[CloudRobo_ProductPDF](https://support.huaweicloud.com/productdesc-cloudrobo/CloudRobo%20%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D-pdf.pdf)（[本地原件](../../../reference_metrial/documents/CloudRobo_Pro--522f065088effec2/document.pdf)）

## 相机、时钟与数据生产

腕部和外部ROS2 Camera Sensor示例均为640×480、10Hz，Frame Name与/camera_image_color话题需一致，RViz检查实际视角。此配置是目标频率，不是physics step或实时达成频率；未取得/clock、use_sim_time、多tick同步、曝光/rolling shutter、畸变及噪声模型的完整说明。10Hz渲染数据不能直接当真机30Hz策略训练数据而不做时间重采样。

轨迹以ros2bag输出，metadata记录关节状态、命令、FollowJointTrajectory反馈与双图。修改metadata后必须刷新/保存task_definition_config.json，才能录制新列表；只修改文件不刷新界面可能造成相机缺失。将bag转LeRobot v3时应检查采样时刻、episode边界、动作与状态错位、归一化统计和失败标签。单条轨迹约一分钟、环境拉起10—15分钟是文档估计，缺硬件/场景统计，不能视为benchmark。专属池轨迹数量1—500、默认3；不是500台并行机器人。[CloudRobo_SimTrajectory](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0055.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_SimT--5b5e7f2ba9864e13/index.html)）

文档可配置Box Shape增广范围、全局随机和预览；范围过大会产生大量不可达失败。这支持物体位置随机化，不证明纹理、光源、质量、摩擦、相机噪声及网络抖动都已统一随机化。应保存随机种子与资产revision，在真实留出场景验证。照片逼真不保证动力学准确，预置可见材质也不证明LiDAR/Radar响应可复现。

## 评测与sim-to-real门槛

官方ACT/SO101实践单任务一场景，公共1—10次、专属1—50次，timeout0—300秒；任务集当前列LIBERO四类，每类十子任务。seed0—10000支持指定场景重现，不能保证跨引擎/驱动bitwise相同。回放有失败/成功区分，但未公开完整成功率分母与测量条件。长耗时回放阈值原文“平均时间75%”存在解释疑义，不能擅自改为P75。[CloudRobo_BestPractice](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0001.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_Best--c4fa57de5f73616b/index.html)）

自定义机器人评测先测连通性，测试时长0.01—300秒，r2c-client RUNNING只证明进程/配置加载；Observation incomplete会skip tick，接口错误与模型能力错误必须分开。文档中的关节名、image key和input_features错误展示有助定位，不能把无报错直接称策略有效。再进入效果评测，记录成功尝试数、失败原因和时长，之后做真实相机标定、系统辨识、负载/摩擦测量与留出任务。[CloudRobo_SimEvaluation](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0057.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_SimE--ed5202e058aafdf3/index.html)）

引擎、平台服务、资产/mesh、代码和数据许可分别取件；官方示例仓库API本次受robots限制，未取得源码许可，不用其他路径绕限制。最佳实践合订PDF超过下载器大小限制，未保存截断件；单页正文及官方图已归档，网页静态依赖缺失如实保留partial_static。本次未购买资源或运行仿真，结论是文献和接口核验，不是训练复现与实机迁移验证。


## 参考资料与原件

下列资料按 2026-11-05 核验时点使用；抓取日期不是发布日期。源码固定到 URL 中的提交 SHA，代表该快照，不保证所有发行包包含相同实现。未运行安装脚本、模型或设备。

| 来源 | 原文 / 本地原件 | 版本与归档边界 |
|---|---|---|
| CloudRobo_ProductPDF | [CloudRobo_ProductPDF](https://support.huaweicloud.com/productdesc-cloudrobo/CloudRobo%20%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D-pdf.pdf) / [原件](../../../reference_metrial/documents/CloudRobo_Pro--522f065088effec2/document.pdf) | 文档01，2026-11-02；完整20页PDF；采集 UTC 2026-11-04T16:53:04.019493+00:00；complete_static |
| CloudRobo_SimOverview | [CloudRobo_SimOverview](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0056.html) / [原件](../../../reference_metrial/webpages/CloudRobo_SimO--c41c4d38b76d89b5/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:59:45.094397+00:00；partial_static |
| CloudRobo_SimConfig | [CloudRobo_SimConfig](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0052.html) / [原件](../../../reference_metrial/webpages/CloudRobo_SimC--90d1e31c1d0016f8/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:59:48.746329+00:00；partial_static |
| CloudRobo_SimImport | [CloudRobo_SimImport](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0053.html) / [原件](../../../reference_metrial/webpages/CloudRobo_SimI--547c06d0d7c62063/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:59:53.803186+00:00；partial_static |
| CloudRobo_SimScene | [CloudRobo_SimScene](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0054.html) / [原件](../../../reference_metrial/webpages/CloudRobo_SimS--86a564346774003e/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:59:58.817931+00:00；partial_static |
| CloudRobo_SimTrajectory | [CloudRobo_SimTrajectory](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0055.html) / [原件](../../../reference_metrial/webpages/CloudRobo_SimT--5b5e7f2ba9864e13/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T17:00:39.643474+00:00；partial_static |
| CloudRobo_SimEvaluation | [CloudRobo_SimEvaluation](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0057.html) / [原件](../../../reference_metrial/webpages/CloudRobo_SimE--ed5202e058aafdf3/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T17:01:04.460075+00:00；partial_static |
| CloudRobo_BestPractice | [CloudRobo_BestPractice](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0001.html) / [原件](../../../reference_metrial/webpages/CloudRobo_Best--c4fa57de5f73616b/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:50:49.765509+00:00；partial_static |
| HiSilicon_DV300_SVP_PDF | [HiSilicon_DV300_SVP_PDF](https://www.hisilicon.com/dam/asset/view/4ef2e012655a4aae8c80619b8cfd093f.pdf/download) / [原件](../../../reference_metrial/documents/HiSilicon_DV3--8b4b0448c818638c/document.pdf) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:31:10.189959+00:00；complete_static |

[主张和图源核验](../../evidence/05_Simulation_Environment.json)。各引用保存原始响应、哈希及 metadata；静态归档不承诺动态交互或像素级复现。
