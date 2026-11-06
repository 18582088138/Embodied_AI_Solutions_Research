from rk_work import *
records={
'03_Sensor_Integration':[
('RK03_Camera','Hardware interface / Full Mode / Split Mode','default firmware only enables the MIPI_CSI0 camera','AIO3588JD4；CSI0/1共享I2C；Kernel5.10示例','双摄需切换驱动和DTS；非全部SoC路数保证'),
('RK03_Camera','IQ Files','isp20 xml configuration are not suitable for isp3x even after transfer','ISP3x JSON/IQ与目标sensor','格式转换不等于适配'),
('RK03_IMX415','Detailed parameters / Hardware connection','3840x2160/60fps; RAW10/RAW12; 30pins','相机模组规格，非板端实测','功耗/SNR/WDR TBD；需lane/驱动匹配'),
('RK03_V4L2_Buffer','Buffer Flags / sequence / timestamp','The driver decides at which part of the frame and with which clock the timestamp is taken','V4L2规范；非BSP实测','时钟/事件/sequence/ERROR均需检查'),
('RK03_OrbbecTime','Timestamp Types / Select Host Clock / Common Pitfalls','Global timestamps are available only on devices that support them','frame/system/global；Linux monotonic usesCLOCK_MONOTONIC_RAW','0不可用，global映射保留曝光事件；重同步不连续'),
('RK03_RPLIDARCode','work_loop / publish_scan','start_scan_time = this->now(); grabScanDataHq; end_scan_time = this->now()','ROS2分支静态快照，未取得commit','围绕SDK调用计时，不是逐点硬件采样时间'),
('RK03_RPLIDAR','ROS 2 Usage','Firefly ROC-RK3588S-PC running Ubuntu 22.04 and ROS 2 Humble','C1 UART460800bps；扫描8—12Hz','特定伙伴示例；无融合/导航成功率')],
'04_AI_Capabilities':[
('RK04_PiConfig','Pi0Config','action_dim: int = 32; action_horizon: int = 50','作者通用默认；pi05离散state与adaRMSNorm','不替代Rockchip优化模型配置'),
('RK04_PiModel','embed_prefix / sample_actions','num_steps = 10; dt = -1.0 / num_steps','JAX作者实现，prefix KV然后flow迭代','非RK1828编译源码/实测'),
('RK04_DroidPolicy','DroidInputs / DroidOutputs','Only return the first 8 dims','DROID两图+7关节+夹爪；padding/mask','不等于机器人32DOF或通用8维命令'),
('Rockchip_Multicard_2026','02 VLA不止于高算力','π0.5 VLA模型已可在RK1828平台上实现5 FPS以上','针对性优化，未披露模型配置/统计/功耗','厂商宣称；不能推导闭环/P99/伺服/成功率'),
('RK04_RAFT','简介 / 1.7 / 3.2','commit ID:6068c1a26f84f8132de10f60b2bc0ce61568e085','160×240，iters循环与5D转4D补丁；文档示例616.32ms','非统计基准；视差需标定转深度'),
('RK04_Qwen3VL','2模型裁剪 / 4分辨率 / 6常见问题','prune_mode默认关闭；KV Int4精度可能下降','shape32倍数；ONNX external data；重建仅特定配置','不泛化SpeedUP或全模型免精度损失'),
('RK02_00_RKNN3_SDK_Release_Notes_V1.2.0','p12-17','Vision latency and LLM were tested independently','RK3588性能模式PCIe/RK182X NPU1GHz；W4A16G32精度表','模型精度/阶段基准不当机器人任务')],
'05_Simulation_Environment':[
('RK05_GazeboInstall','Binary Installation / page banner','Harmonic binaries are provided for Ubuntu Jammy (22.04) and Ubuntu Noble (24.04)','Harmonic为较旧仍支持LTS；2023-09至2029-05','未验证Rockchip ARM/Mali/BSP或Humble组合'),
('RK05_GazeboROS','ros_gz_bridge / Launch manually','support is limited to only certain message types','方向@/[/]，队列、lazy、消息类型','网络桥非零拷贝/闭环保证'),
('RK05_GazeboSensor','Preliminaries / IMU','When adding a plugin ... default plugins are not loaded','SDF1.9；example IMU update_rate1','教学设置，非真实传感器同步/安全'),
('RK05_Mujoco','Model instances / Options','MJB ... version-specific','mjSpec/mjModel/mjData；CPU C与GPU后端分开','保留源资产，不能推出RK NPU物理加速'),
('RK05_MujocoCompute','General framework / Numerical integration / Soft contact','M dv/dt + c = tau + J^T f','timestep、执行器、积分、接触求解依赖模型','视觉真实不等于动力学/真实泛化'),
('RK05_OpenpiLibero','Results','π0.5 @ 30k ... Average 96.85','作者pi05_libero仿真checkpoint','非RK1828优化模型真实成功率'),
('RK05_LIBERO','Datasets / Task / License','130 tasks; Codebase MIT; Datasets CC BY4.0','固定初始状态/sparse reward；旧CUDA依赖','不同任务/依赖/数据许可分开')],
'06_Robot_Integration':[
('Rockchip_Robotics_2026','末组产品原图右上展牌','优必选 悟空AlphaMini2；芯片RK3566','2026活动原图；已打开全图和放大局部','芯片厂商展牌绑定；未取得OEM BOM或全部代际适配'),
('Rockchip_Robotics_2026','末组产品原图左上展牌','卧安 KATA Friends；芯片RK3576','芯片厂商原图，未补读模糊细字','展示对象，非独立客户验收/量产统计'),
('Rockchip_Robotics_2026','多形态产品 / 数据结构光视觉','Lumistar TERO PRO小型网球发球机；松延动力轻量化人形','正文未给精确芯片/人形SKU','不补齐具体BOM/步态/控制归因'),
('Rockchip_Robotics_2026','数据、结构光、视觉','RK3588+RV1126B；Wi-Fi TSF；RK3572双目深度25fps','厂商方案宣称；无同步误差/shape/成功率','非相机同步曝光或所有透明材质鲁棒性'),
('Rockchip_Multicard_2026','02 VLA方案','RK3588搭配RK1828 ... 轨迹规划、关节控制和结果校验','展会demo与应用探索','本体/模型/测量/商业收益未取得'),
('RK06_Controller','Introduction','powered by ... RK3588','EC-R3588RT产品文档','与关联载板页RK3588S叙述冲突，待BOM确认'),
('RK06_ControllerBoard','Introduction','RK3588S','ROC-RK3588-RT页静态快照','RT名字不等于RT内核或WCET')]
}
for stem,rows in records.items():
 f=s/'evidence'/f'{stem}.json';v=json.loads(f.read_text(encoding='utf-8'));ids=v['source_ids'];extra=[]
 for n,loc,quote,conditions,finding in rows:
  assert n in ids,n
  c=claim(n,loc,quote,conditions,finding,'事实/厂商宣称/分析；具体分类见正文');c['original_excerpt']=quote;extra.append(c)
 v['claim_review']=extra
 v['manual_review']['coverage']='已核验关键主张并记录精确API/章节/页码及原文片段；正文列出未取得交付物和分析边界。'
 f.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
print('key claim audit:',list(records))
