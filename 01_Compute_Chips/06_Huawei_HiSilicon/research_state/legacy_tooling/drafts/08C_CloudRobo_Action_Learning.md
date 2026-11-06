# 08C CloudRobo动作契约、资产血缘与学习闭环

本专题的核心是具身开发的接口和状态问题：相机/关节观测必须以模型理解的格式输入，输出动作必须以本体可执行的语义下发，训练产物与部署服务必须有明确版本。CloudRobo的公开R2C协议、MetaEngine适配器和开发流程提供了可检查的机制；RLinf作为第三方Ascend学习生态补充对照，不能称全部为华为自研或双方全部组合已认证。

## 架构和双向数据流

{{FIG:CloudRobo_ProductPDF}}

官方架构连接工作空间、资产、OBS/SWR、CCE/ModelArts与R2C。其优势来自减少数据、模型、仿真和真机之间的人工交接，而不是保证单个kernel领先。资产血缘、权限和资源配额是平台功能，实际复现实验还需镜像digest、模型/数据哈希、配置和本体版本；空间内可见对象不等于不可变交付物。{{CloudRobo_ProductPDF}}

MetaEngine适配器的上行是ROS2订阅→streams→device_to_r2c→Observations→session.publish_observations→Zenoh→云；下行Actions经Zenoh、r2c_to_device、命令dict和adapter.send_action路由回ROS2。真实与仿真只需相同ROS接口这一抽象可减少重复适配，但相同消息类型不保证动力学、时延、噪声和保护条件相同。{{CloudRobo_MetaEngineAdapter}}

R2C模型映射的STATE要求一维shape、数值dtype、非空values，并通过@{name}按names查索引；VISUAL按color/depth和相机名解码；PROMPT目前只允许一个，前端task有其生效规则。output_features当前只允许一个item，模型输出[chunk_size,N]按列映射到本体关节/末端。输入shape一致只能发现部分错误，关节顺序和单位若错而数组仍合法，模型仍可能输出危险轨迹。{{CloudRobo_R2C_Protocol}}

官方协议说明视觉类型处提PNG，示例解析却用jpeg_to_ndarray，Q25又明确JPEG编码。应把声明的图像类型、实际编码与decoder分开验证，不能断言所有R2C图像固定PNG。示例还出现joint_5重复、name/names等不一致，不能直接复制成可运行配置；按目标SDK及真实消息校验，不由研究报告擅自修正官方原件。{{CloudRobo_R2C_Protocol}} {{CloudRobo_VLN}}

## 生命周期：配置何时生效

|修改位置|原文生效范围|版本管理动作|
|---|---|---|
|模型服务详情上传|只对该模型服务|记录服务ID与新配置哈希|
|新部署页面上传|只对本次部署，原资产保留|绑定本次服务版本|
|模型资产OBS目录|部署时读取，现存服务重启也不更新|重建/明确更新已部署服务|
|数据资产OBS目录|训练终态获取；缺时可能复制源模型配置|冻结训练结束前的配置与血缘|

这组规则解释一个常见失效：权重更新了、映射文件仍是旧版，或者修改OBS后误认为重启服务已生效。训练成功、手动终止或失败等终态都涉及读取配置，产物存在不能当训练收敛。应将权重、数据归一化、r2c.json、端侧YAML和transformer作为一组受版本控制的发布资产，并先dry_run核验。{{CloudRobo_R2C_Protocol}}

max_iter_num是推理调用次数，max_run_time是分钟，任一达到即停止。默认stop_condition为100次/10分钟，而真机调试前端和示例常为60次/5分钟；这些是不同层配置，不能称统一硬实时截止。最大300000次/300分钟是协议配置上限，不是吞吐指标。此前PI05实践的单位未知项可据此关闭，但仍需核验实际服务与端侧停止状态。{{CloudRobo_R2C_Protocol}}

## 动作队列、对齐与观测年龄

MetaEngine SDK文档中publish_hz既是动作执行频率，也控制观测发布检查，建议10—30Hz；不能与云policy-call、ROS控制器或电机伺服频率等同。action_response_timeout_s超时可重发观测；max_enqueue_actions_per_chunk裁剪入队数量，−1全部采用；enable_action_chunk_alignment控制chunk对齐，async_request默认关闭。它们改变等待与轨迹连续性，需要组合测量，不是各开关越多越快。{{CloudRobo_MetaEngineAdapter}}

分析：chunk覆盖时长约为实际执行步数/执行频率，前提是无跳步、无插值差异且频率确实达到；推理时延超过可消费的剩余chunk时可能停顿，反之大量排队可能执行过期动作。动作id与观测id对应能帮助追溯，但跨设备时间戳还需时钟定义。相机和关节多流同步为可选observation_sync/message_filters，不应把未开启同步的streams默认为同曝光时刻。

订阅qos参数在该配置是队列深度，max_update_hz限频、store_raw_message保留相机消息；不能把整数qos=10当已核验DDS reliability/durability完整策略。init_joints连接后会主动摆位，dry_run用于只发观测；真实本体重连是否重复摆位必须检验。网络断开、退出、暂停和回home的控制语义及下游buffer要分别验证，本体保护与云服务可用性无直接等价关系。{{CloudRobo_MetaEngineAdapter}}

## 转换器与学习闭环的失效点

平行夹爪例通过entry-point注册IValueTransformer子类，无需fork SDK；内置重名优先，因此插件名应唯一。输入两手指位移和乘1250、输出每指除2500，与训练数据的0—100缩放配对。元数据名称、单位与映射代码共同决定动作语义，不能只按shape匹配。服务RUNNING可能仅表示配置加载；Observation incomplete会跳tick，正确机器人动作还需连通性和效果两阶段检验。{{CloudRobo_SimEvaluation}}

残差RL冻结基础BC，逐步修正、记录干预标志和当前/下一观测，这有机会减少action chunk的开环误差。成立条件是基础策略足够可行、残差幅度/奖励正确、接管和观测足够及时。官方称冻结策略形成隐性约束，不是形式化安全保证。成功保存/失败丢弃的采集流程也会改变数据分布；训练集质量提升不能证明真实任务失败率下降。{{CloudRobo_ResidualOverview}} {{CloudRobo_ResidualDebug}}

## 开放学习路线对照：RLinf

RLinf把env、rollout、actor放到共享、分离或重叠的设备位置，pipeline_stage_num可让环境与推理重叠；优势要在三者负载相匹配时才成立。OpenPI文档明确network action_horizon与env执行action_chunk不同：pi0_libero网络50、pi05_libero网络10的例子，环境常只执行5步。不能把CloudRobo PI05的50步输出直接搬到RLinf某个checkpoint，必须对照TrainConfig与权重。{{RLinf_OpenPI_Guide}}

RLinf Ascend容器明确CANN9.1.1-910B、arm64/amd64、Ubuntu22.04构建参数，host driver要暴露给容器。LIBERO在Ascend路线使用OSMesa CPU渲染，环境并行数受CPU资源限制；这已补齐04/05先前第三方世界模型路线证据，仍不证明310B或海思端侧可用。StarVLA作者路径固定v1.6与QwenOFT基模型，不能等同CloudRobo的Qwen3 initializer。{{RLinf_Ascend_Container}} {{RLinf_OSMesa_Setup}} {{RLinf_StarVLA_Guide}}

Wan路线从初始帧和7维动作生成256×256 RGB，以奖励分类器输出作为学习信号，没有真实physics reset、腕部图或本体proprioception。初始化数据和world-model/VAE/reward三个权重缺一不可；训练中的模型幻觉或奖励漏洞可能被策略利用，必须用独立真实/物理环境验证。{{RLinf_Wan_Guide}}

|作者Wan结果|Spatial|Object|Goal|解释|
|---|---|---|---|---|
|OpenVLA-OFT LoRA基线|61.2%|36.7%|48.2%|作者原表|
|RLinf-GRPO+Wan|77.5%|77.9%|60.1%|对应任务/采样协议|
|差值（分析）|16.3百分点|41.2百分点|11.9百分点|不是平台加速倍数|

原文给task×trial、do_sample=True、temperature=1.6、夹爪初始打开和冻结world model；“1500 environments、10 tasks×150 trials”的跨suite分母仍需核对实验manifest。本章只保留原表，不把结果归因到Ascend硬件。Ascend Wan依赖另装MindIE-SD，导入失败可fallback，默认关闭仿真器评估，且需独立验证策略数值。{{RLinf_Wan_Guide}}

## 护城河与验收条件

CloudRobo可积累的优势是受管理的模型/数据/本体配置和可复查工作流，RLinf开放路线可降低算法迁移成本，两者仍有服务依赖、适配和许可边界。平台文档的IAM、委托、租户隔离和日志属于云安全功能；默认权限、HTTPS配置、证书与训练数据合法性要客户负责，不等同机器人功能安全。{{CloudRobo_ProductPDF}} {{RLinf_License}}

选型时先做接口往返验证，再测观测年龄、重连/重复动作、chunk切换、配置更新/回退、错误输入和真实失败数据闭环。记录policy-call、动作执行、controller和伺服四层频率及P99，要求边缘控制器在云故障下执行可验收降级。本次公开资料支持机制分析，未给同条件吞吐/成功率与商业节省；网页partial_static、SDK包/资产许可未取得项如实保留。
