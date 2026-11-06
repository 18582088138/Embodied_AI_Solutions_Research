import sys,pathlib,json
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from curation import inputs,figure
stem='05_Simulation_Environment'
rows=[
('AMD05_Genesis_Blog','gs.init(backend=gs.vulkan)','AMD教程选择Vulkan','初始化','事实','2026-02-09，Ubuntu24.04/Max示例','不证明ROCm物理后端'),
('AMD05_Genesis_Blog','dt=0.01','时间步设置','Scene','事实','教程设置','120step仅对应1.2秒模拟时间'),
('AMD05_Genesis_Blog','without going through the physics solver','直接写DOF绕过物理','Control Joint Position','事实','set_dofs_position','与PD运动分开'),
('AMD05_Genesis_Blog','controller torques','step控制动力学链','Start the Simulation','事实','教学场景','生成力矩、接触、积分，不是实机验证'),
('AMD05_Genesis_Blog','n_envs = 9','九环境示例','Parallel Simulation','事实','build batch9','没有吞吐benchmark'),
('AMD05_Genesis_Blog','Each environment has its own robot state','独立state共享kernel','Parallel Simulation','事实','batch场景','需独立reset/done/动作'),
('AMD05_Genesis_Repo','Quadrants lowers Python kernel code','编译后端分层','Compiler','事实','当前主分支','不追溯套给旧教程'),
('AMD05_Genesis_Repo','Apache-2.0 license','上游许可标记','README','事实','主仓代码','资产/extra许可另核'),
('AMD05_Genesis_Docs','pip install genesis-world','当前安装包','Getting started','事实','当前文档','需冻结版本'),
('AMD05_Mujoco_Overview','MuJoCo','MuJoCo上游路线','Overview','事实','stable归档','不作为AMD实测'),
('Model05_NVIDIA_08_DEEP_MUJOCO_MJX','Nvidia and AMD GPUs','MJX-JAX支持AMD','MJX Implementations','事实','上游文档','不是MJX-Warp支持'),
('Model05_NVIDIA_08_DEEP_MUJOCO_MJX','specifically for NVIDIA GPUs','Warp针对NVIDIA','MJX Implementations','事实','MJX-Warp','不套AMD'),
('Model05_NVIDIA_08_DEEP_MUJOCO_MJX','mjx.put_model','设备模型转换','Minimal example','事实','JAX','与CPU状态对象分开'),
('Model05_NVIDIA_08_DEEP_MUJOCO_MJX','650K, 1.8M, 950K and 2.7M','单humanoid吞吐四值','Performance','厂商宣称','M3Max/3995WX/A100/8芯片TPU不同batch','非AMD GPU性能或同条件排序'),
('Model05_NVIDIA_08_DEEP_MUJOCO_COMPUTATION','complementarity can be violated','接触近似','Physical realism and soft contacts','事实','convex contact','不是物理真值'),
('Model05_NVIDIA_08_DEEP_MUJOCO_COMPUTATION','Euler-integrated filters diverge','filter时间常数边界','Stateful actuators','事实','t<h','filterexact稳定不证明全系统稳定'),
('AMD05_Gazebo_Docs','May, 2029','Harmonic支持日期','页头','事实','Gazebo项目','不是AMD BSP生命周期'),
('AMD05_Gazebo_Sensors','<update_rate>1</update_rate>','IMU教程1Hz','IMU sensor','事实','教程','不套真实IMU'),
('AMD05_Gazebo_Sensors','Not all the tags are supported','标签支持有差别','sensor tags','事实','Harmonic','逐传感器核验'),
('AMD05_Gazebo_ROS','bridge','ROS需要桥接','ROS integration','事实','ros_gz','消息和方向需匹配'),
('AMD05_Gazebo_Migration','Classic','Classic迁移','migration guide','事实','Classic到Gazebo','旧包不自动兼容'),
('KRS_Install','2022.1','KRS旧工具链','Installation','事实','该安装说明','不称当前EDF兼容'),
('AMD05_AUP_Repo','Learning','AUP教学入口','README','事实','公开仓库','不证明量产SLA'),
('AMD05_O3DE_Concepts','gazebo_msgs','组件外部消息依赖','组件说明','事实','25.05起，ROS发行版条件','依赖缺失时禁用'),
('AMD05_O3DE_Concepts','ROS2FrameComponent is a representation','frame时空关系','Frames','事实','26.05文档','TF2与namespace需匹配'),
('AMD05_O3DE_Import','Fix URDF','URDF修复入口','Importer','事实','当前文档','兼容不等于惯量正确'),
('AMD05_O3DE_Import','prefab','资产生成','Importer','事实','source/product链','图示product可能失败'),
('AMD05_O3DE_Physics','PhysX','物理引擎','Physics','事实','O3DE','不推所有GPU插件兼容'),
('AMD05_O3DE_Materials','Multiply: The product','材料combine','Physics materials','事实','接触材料','不等于PBR'),
('AMD05_O3DE_Materials','available with PhysX 5.1 enabled only','柔顺接触版本','Compliant Contact','事实','PhysX5.1 enabled','需匹配部署版本'),
('AMD05_O3DE_Time','/O3DE/ROS2/ClockType','三种clock','Simulation Time Settings','事实','ROS2 Gem','需统一use_sim_time'),
('AMD05_O3DE_Time','Does not allow to adjust the time at runtime','实时clock不能调','Realtime Clock','事实','realtime','与simulation clock分开'),
('AMD05_RGL_Repo','CUDA and OptiX','RGL依赖','Description','事实','RGL库','不能认定AMD可用'),
('AMD05_RGL_Repo','they have not been fully tested yet','新build未充分测','build table','事实','development2510及更新','expected不等已验证'),
('AMD05_O3DE_Robotics','robotics','产业引擎定位','industry page','事实','公开介绍','不采用性能推广作为AMD测量'),
('AMD06_XArm_Sim2Real','ROCm implementation','特定ROCm Warp实现','Hardware and Software','事实','2026-09-29，MI300X/MI355X','随案例补丁，不泛化上游支持'),
('AMD06_XArm_Sim2Real','queried at 40 Hz','真实策略调用40Hz','Policy Controller Architecture','事实','RyzenAI300，ONNX小MLP','非servo频率，无成功分母'),
('AMD06_XArm_Sim2Real','orientation-aware caging','XArm6奖励适配','Environment Details','事实','可变夹爪方向','不是纯视觉VLA'),
('AMD06_XArm_JAX','AMD Radeon RX 7900 XTX','JAX教程测试GPU','installation','事实','Ubuntu24.04/ROCm7.2','与后续MI训练分开'),
('AMD06_XArm_JAX','maxhullvert','mesh简化','Asset Creation','事实','XArm7','小范围Jacobian不外推大扰动')]
inputs(stem,'05_simulation',rows,dict(coverage='路线关系、资产/physics/render/sensor/ROS/学习与SDG分别研究；完整训练和实物迁移为缺口。',versions_and_measurements='旧Vulkan教程与新World、MJX-JAX与Warp、Classic11与Harmonic、O3DE26.05与插件版本分别核对；四平台吞吐保留完整条件。',maturity_and_licenses='演示、上游支持与生产验收分开；源码/二进制/资产/数据许可分别约束，资产未全取得。',figures_opened='已实际打开3张Genesis原图及2张O3DE截图；确认URDF默认惯量提示和mesh product失败，图不证明吞吐。'))
for slug,s,m in [('scene','AMD05_Genesis_Blog','Scene_content.png'),('entity','AMD05_Genesis_Blog','Entity.png'),('parallel','AMD05_Genesis_Blog','parallel.png'),('urdf_fix','AMD05_O3DE_Import','URDF_fixing_result.png'),('mesh_list','AMD05_O3DE_Import','URDF_importer_mesh_list.png'),('xarm_controller','AMD06_XArm_Sim2Real','controller_pipeline.png')]:figure('05',slug,s,m,True)
d=pathlib.Path(__file__).parent
meta={s:dict(title=s.replace('AMD05_','').replace('Model05_NVIDIA_08_DEEP_','MuJoCo ').replace('_',' '),version=('2026-02-09 AMD教程，Ubuntu24.04' if s=='AMD05_Genesis_Blog' else '官方归档快照；正文标注组件/版本，采集时间不等发布时间')) for s,*_ in rows}
(d/'source_meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
