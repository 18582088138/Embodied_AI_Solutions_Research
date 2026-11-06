# Intel 06 — 本体适配、客户采用与交付证据

截止2026-11-05。技术蓝图采用Suite固定对象1b0b22a2964f；客户案例主要依据Intel发布于2026-05-20的公告，归档时网页图片带后续时间参数，不能把采集日当首次发布日。未接触客户、运行机器人或审计收益。[[Intel06_CustomerCases]]

## 具体对象与成熟度

| 公司/本体 | 计算平台 | 任务与链条 | 原文状态 | 时间/收益口径 | 主要缺口 |
|---|---|---|---|---|---|
| Sensory AI Ella | Core Ultra Series3，未列SKU | 视觉/语言/运动与三agent，咖啡服务 | 公告称已全面切换，取消独显 | 2026-05-20；Computex预告最高200杯/小时 | 门店台数、稳定吞吐、故障率与TCO数值 |
| Trossen机械臂/研究套件 | Series3，未列SKU | 食品、制造与机器学习研究 | 当年开始测试 | 同公告用户评价，无量化任务结果 | 正式量产型号、BSP和合同 |
| Circulus Pibo/工作站与人形 | Series3，未列SKU | HRI、本地AI、模块化OS | 公告称OS运行 | 离线/隐私为厂商定位 | 哪个本体代际、任务/安全测试 |
| Oversonic RoBee及centaur | 公告称机内Series3、取消独显 | 制造pick/place、康复交互 | 公告称构建部署 | 训练仍用独显；无台数/临床结果 | SKU、本体型号代际、许可与运营暴露 |
| Clearpath Jackal J100 | 换装AAEON UP Nexus WCL Edge | D435i→SLAM/Nav2→底盘 | Intel限定组合validated blueprint | 固定对象技术配置 | 其他主机及原装电脑未验证 |
| UR5e＋Robotiq2F-85 | Series3主机，未限定具体SKU | USB相机→抓取/Servo→UR driver | Stationary toolkit参考设计 | 配置/步骤，非商业验收 | 任务成功率、动态误差、安全评估 |

对应原文：[[Intel06_CustomerCases]]、[[Intel06_Jackal]]、[[Intel06_URBlueprint]]。上述名单不包含未取得对应公告的Pudu、Keenon或UBTECH；没有以其他品牌报道推定其采用。市场采用名单也不等于Series3机器人装机份额。

## Ella：采用证据与收益机制

Intel公告引用Sensory AI创始人Keith Tan，描述旧架构Intel CPU＋独显，独显成本很高；发布Series3后已切换到Intel-only。具体SKU、独显型号、两代BOM、模型与功率没有给出，所以本文只把取消独显作为客户采用陈述，不能计算节省比例、续航或投资回收期。开头医院凌晨咖啡叙事没有给医院名称、在岗台数或观察记录，不能充当现场验收。[[Intel06_CustomerCases]]

三agent分为Avatar客户交互、Ella门店业务模式、Guardian系统健康推理；卡杯异常由agent解释，确定性orchestrator命令手臂执行恢复。这个责任分工说明业务推理不直接等于伺服闭环，恢复的危险检测、权限限制和执行验证仍需另交付。200杯/小时原文使用“will”预告Computex展示，缺饮品组合、连续运行时长、维护/补料时间与失败分母。即使演示达到该值，也不能作为全天运营或任意菜单上限。降低TCO目前是厂商与客户宣称，尚无审计数据。

## Trossen、Circulus和Oversonic：不混同本体代际

Trossen的证据到测试阶段，其架构师称x86框架覆盖和CPU/iGPU性能有利开发。没有同条件机器人benchmark，不能把“与Jetson等价I/O”的引述变成接口逐项验收或算力排名。技术样例ALOHA是另一条有明确输入和配置的路线，也不能反向证明Trossen所有新机械臂已量产采用相同SKU。[[Intel06_CustomerCases]]、[[Intel02C_RTC_README]]

Circulus公告列Pibo社交机器人与企业AI工作站，称开放OS在Series3运行，但未把每个产品代际与处理器逐项对应。文中“zero-latency”“guarantees security”属于宣传，物理延迟不可能据文字被判定为零，离线运行也没有证明软件认证或数据治理。应验收识别时延、断网行为、日志保留、身份权限与危险响应。[[Intel06_CustomerCases]]

Oversonic公告介绍制造操作及医疗康复，引述机内转向Series3而训练用独显。这样可以确认训练/部署分工，不应写成训练也无需GPU。公告未列每款RoBee/centaur、芯片SKU与交付台数，更未证明医疗有效性和当地合规。不能把公司历史部署、全部机队数量或累计康复活动归因这代芯片。其采购尽调应索取具体序列号、软硬件版本、服务场景、维护责任及任务数据。

![Intel公告中的Oversonic RoBee原图]([[FIG:Intel06_RoBeeFigure]])

图已打开核验，支持本体外观及展台展示；不支持内部芯片型号、八小时续航、认证或在岗数量。页面归档缺12项静态依赖，正文与该图片成功取得，视频与动态交互未完整归档。[[Intel06_CustomerCases]]

## Jackal：载板替换并非任意x86兼容

蓝图明确验证Jackal J100换装UP Nexus WCL Edge、Ubuntu24.04、Jazzy和Clearpath软件，搭配D435i；原装电脑及其他板不在验证范围。初次bring-up要求更新MCU固件并先备份默认系统/保留SSD。主机换板若没有匹配底盘MCU协议、供电、散热与网络，操作系统能启动也不能说明本体适配。[[Intel06_Jackal]]

robot.yaml须绑定底盘序列、主机名/IP、ROS namespace、domain_id、工作区和相机真实序列。Intel教程建议根namespace，Clearpath默认可以另有namespace；机队部署必须重新设计域隔离，避免多台根话题互串。示例RealSense v4.54.1/librealsense2.55.0日志属于旧示例，不能当当前BKC版本。感知将相机与惯性/轮速映射到统一frame，导航输出交给底盘控制器；定位漂移、急停和通信失效仍需实测，不从validated标签推导安全等级。

## UR5e：完整动作交接与故障条件

参考配置包含专用千兆以太网、URCap External Control的主机地址/50002端口、Robotiq URCap、USB高速相机与每臂工厂标定抽取。标定文件需交给描述和driver，相机外参为以米/rad定义的world/base_link变换；例中TCP偏移0.174m仅适用于该夹爪配置。替换相机、工具或安装方式要重标定、重设点云裁剪和碰撞几何，不能机械套示例坐标。[[Intel06_URBlueprint]]

RVC把RotateBBList/三维姿态交给抓取选择和状态机，再由delta_twist_cmds及UR driver发往控制箱。示例planning_frame为base_link、ee_frame为ee_link，输出为Float64MultiArray；publish_period0.002s、collision_check_rate60Hz、incoming_timeout0.1s分别是发布、碰撞检查和失联参数，不是统一500Hz控制或100ms内完成危险停机保证。上游不再写指令还可能留有下游缓存。UR控制器本身的伺服周期与保护反应需要控制箱文档及集成实测。[[Intel02E_RVC]]

该教程给教导器到ROS的符号/四元数换算，绑定其工位frame；应以TF链和独立标定点验算，不能作为UR全系列坐标公理。VLA controller和ADBSCAN在此页标Roadmap，不能写入已经交付的RVC功能清单。机型的安全认证也不自动覆盖整机工位、视觉模型和生成式任务编排。

## 人形与研究臂的放行证据

Robotmctask可把左右臂和腿分三个EtherCAT task，ENI定义各网络，共享内存交接关节状态。文档称NPU站立示例，固定yaml却默认CPU执行stand.onnx，CPU affinity11/12/13是该示例配置。必须核验本体关节顺序、角度/扭矩单位、减速比、零点、限幅、看门狗与动作周期；未取得站立模型训练卡、真实本体型号和失效统计，不能宣称任意人形全身平衡已验收。[[Intel02E_TaskIntro]]、[[Intel02E_RLConfig]]

ALOHA RTC教程区分real_aloha与mujoco_aloha，动作归一化stats、camera_num及chunk需随训练冻结；默认50Hz为动作消费设置。正式放行应依次保存仿真接口测试、目标本体低速执行、负载/障碍/断网异常、热稳定并发与客户现场数据。业务结果必须含尝试次数、任务定义、人工介入、暴露小时和维护停机，才能解释计算平台对收益的作用。本文已建立技术与客户采用链条，仍未取得这些整机验收数据。
