# 02E CloudRobo云开发平台、R2C与ROS2部署链

本专题补齐02的软件域：CloudRobo把数据、模型、镜像、算法、仿真与机器人接入组织到工作空间，不是端侧CANN的替代品，也没有证据表明它自动给每款A2或海思SoC交付机器人SDK。本章截至2026-11-05，以产品文档01（2026-11-02）、具体开发实践和R2C协议解释可复建链；未登录创建资源、安装SDK、运行容器或驱动机器人。与{{REPORT:08C_CloudRobo_Action_Learning}}的技术比较相衔接，本篇着重开发对象、依赖、配置、部署与运维。

## 平台对象与服务分工

{{FIG:CloudRobo_ProductPDF}}

图为官方产品PDF物理第5页，已经打开检查。它把具身广场、工作空间、空间资产、资源池和本体分开。平台宣称能提高开发效率与成果复用，但图没有效率测量、目标设备时延或工业认证。自有资产发布具身广场仍有“敬请期待”限制，不能将箭头当作所有账号当前可用的功能。{{CloudRobo_ProductPDF}} {{CloudRobo_Functions}}

|对象/服务|职责与数据|开发时需要保存|交接边界|
|---|---|---|---|
|工作空间/资产中心|逻辑资源、数据/模型/场景及过程态血缘|workspace、asset_id、revision和权限|逻辑隔离不等于物理独占|
|OBS|数据、模型备份和快照|桶/区域、对象版本、清单/哈希|CloudRobo本身无存储能力|
|SWR|训练/部署/评测镜像|架构、digest、运行依赖和许可|镜像注册不证明端侧支持|
|CCE|数据准备和模型评测资源|集群、节点规格、namespace及配额|与训练资源分开|
|ModelArts|模型训练资源|训练规格、镜像、参数/输出路径|训练成功不等于策略达标|
|R2C/机器人|观测映射、模型服务和动作交接|device/service ID、证书、JSON/YAML|控制器保护和伺服仍需本体交付|
|CTS/IAM|操作审计、身份、委托与权限|事件保留/导出策略及授权范围|不是机器人闭环任务日志|

服务关系见产品PDF物理19—20页。复现资产不应只有一个模型ID：还应记录数据归一化、训练参数、权重、镜像digest、tokenizer、动作头、仿真资产及本体标定。平台血缘能减少人工交接，但在镜像可变tag、OBS覆盖写或外部依赖更新时，ID仍不能替代不可变哈希。{{CloudRobo_ProductPDF}}

共享池配额表列CCE 64CPU/128GiB、ModelArts NPU4、仿真单元32CPU/72GiB/GPU2，含义是指定资源配额，不是每个训练任务、每台机器人或永久免费额度。专属池可被多个工作空间共享，单个空间的任务仍受池容量和排队影响。用户应区分配额、申请资源、实际分配、并发占用和计费时长；“资源可见”不证明此刻可启动。{{CloudRobo_ProductPDF}}

## 身份、权限和证书生命周期

控制台通过REST风格API并使用Token认证。官方页给出cloudrobo:asset:create权限例，IAM控制之外还有委托与工作空间；后台操作OBS前使用委托取得临时凭据，不保存用户Token。页内称管理员新建用户在没有细粒度策略时默认具有CloudRobo所有权限，应按该说明主动核对实际租户配置，不把新账号假设为最小权限。{{CloudRobo_AccessControl}}

Notebook远程SSH使用密钥对。真机接入另从平台下载证书bundle并填YAML的相机、串口与机器人身份；身份有效、设备在线、观测完整、模型运行、动作正确是不同验收状态。需要记录证书有效期、换证、撤销、丢失恢复及多机器人身份隔离；公开实践不足以证明所有这些过程自动完成。操作审计也应外部留存：产品PDF的控制台最近7天日志不是长期任务追踪保证。数据、模型和证书备份不能直接混在可分享资产里。{{CloudRobo_RealInference}} {{CloudRobo_ProductPDF}}

## 一条具体开发—部署链

以SO101/PI05为可定位例：先固定LeRobot v0.5.1、本体标定和双RGB相机，采集数据或订阅SO101-PlacePenHolder-Sim-Dataset；Notebook下载LeRobot-PI05-Base与数据，训练算法在ModelArts资源执行，再将输出模型/镜像注册为平台资产，部署在线服务，通过R2C把当前观测送入策略、将动作送回本体。平台转换版不能仅凭名称等同作者原始JAX权重。该链的每段有开发步骤，本次没有实机复建证明。{{CloudRobo_NotebookModels}} {{CloudRobo_TrainAlgorithm}} {{CloudRobo_Pretrained}} {{CloudRobo_RealInference}}

PI05训练例accelerate单进程、BF16、gradient checkpointing、60steps/20steps保存是上手配置；没有batch、设备内存、吞吐、收敛或任务成功分母。FFT/LoRA训练方式按平台资产选择；PI0/PI05/SmolVLA与PI0FAST/WALL-OSS/XVLA支持项不同，不能把一个选项泛化到所有模型。产物评测需要独立留出数据及本体任务，而不是看作业终态。{{CloudRobo_NotebookModels}} {{CloudRobo_TrainAlgorithm}}

注册自定义模型时，文档的ARM镜像、ASCEND/CPU类型及ASCEND_SNT9B标记是云平台配置；不是Atlas200I A2/310B或海思端侧的适配认证。OBS模型目录单文件30GB、最多100文件、深度10是导入约束，既不代表可用内存也不代表吞吐。部署前锁定运行架构、CANN/PyTorch配套、模型输入输出、r2c.json和启动命令，记录镜像/模型哈希，再确认服务配置和日志。{{CloudRobo_CustomModel}}

## R2C模型契约与配置生效

STATE要求一维shape、数值dtype和非空values；按names查找关节后映射对应列。VISUAL分color/depth并按相机key取解码数据；PROMPT当前只允许一个。输出仅一个item，动作矩阵是chunk×N，按列映射关节或末端状态。PI05实践六关节float32、双图uint8、50×6输出是特定资产例，不能移到OpenVLA的七维末端增量或其他本体。{{CloudRobo_R2C_Protocol}} {{CloudRobo_Pretrained}}

协议示例有name/names、joint_5重复及PNG说明与JPEG转换器不一致，研究应保存原件并记录冲突。通过实际观测和配置验证名称、单位、数据类型、通道、编码和动作顺序，不能只验证数组长度。错误单位仍能得到合法float32数组，类型检查不会自动识别物理错误。

|更新位置|文档规定的生效范围|部署动作|
|---|---|---|
|服务详情上传映射|仅当前模型服务|保存服务ID及配置哈希|
|新部署页面上传|仅本次部署，原资产保留|绑定本次发布单|
|模型OBS目录r2c.json|部署时读取；重启现存服务不更新|显式更新/重建并核验服务|
|数据OBS目录r2c.json|训练终态读取；缺时复制源模型配置|固定训练终态前的配置和来源|

这解释了模型与接口可能错版的机制：修改OBS并重启服务不意味着使用新映射，训练产物也可能继承源模型配置。上线时将权重、归一化、映射、YAML和transformer成组保存，回退必须回退整组。max_iter_num表示调用次数、max_run_time表示分钟，停止为或逻辑；协议默认100次/10分钟，例60次/5分钟，配置上限300000次/300分钟。云停止条件、端侧max_duration_s秒和控制器停机是不同层。{{CloudRobo_R2C_Protocol}}

## ROS2适配器、队列和同步

MetaEngine上行：ROS2订阅→streams→device_to_r2c→Observations→session.publish_observations→Zenoh→云。下行：Actions→Zenoh→r2c_to_device→命令dict→adapter.send_action→ROS2发布器/服务/动作。ROS2 JointState、Image、Float64MultiArray和FollowJointTrajectory具有不同语义，不能把路径或关节数组直接当电机指令。{{CloudRobo_MetaEngineAdapter}}

O3DE上游ROS2 Gem本身原生作为ROS2节点，无需额外桥接，支持/clock非实时仿真时间、/tf与/tf_static、namespace及动态生成机器人。这是引擎通信机制；R2C仍承担ROS2和云观测/动作之间的语义转换。相同ROS接口减少适配层，却不使真实机器人与仿真具备相同摩擦、观测年龄或危险响应。上游文档无桥接性能优势为机制宣称，没有CloudRobo链路毫秒实测。{{O3DE_ROS2_Gem}} {{CloudRobo_MetaEngineAdapter}}

适配器要求ROS2 Humble/Ubuntu22.04或Jazzy/24.04、Python≥3.10，rclpy和一致ROS_DOMAIN_ID；message_filters仅在启用多流同步时依赖。publish_hz建议10—30Hz，同时控制动作执行和观测检查；不是云policy频率或伺服频率。subscriptions的qos整数是队列深度，不是完整DDS可靠性策略；max_update_hz限频，store_raw_message对图像编码重要。应另记录各消息header、曝光时间、接收时间和观测ID。{{CloudRobo_MetaEngineAdapter}}

action_response_timeout_s等待超时可重发观测；max_enqueue_actions_per_chunk=-1全部入队，enable_action_chunk_alignment默认false，async_request默认false。队列长度、请求重发和chunk对齐改变连续性及动作年龄，要共同测量。init_joints可在连接后主动摆位，dry_run仅用于只发观测联调；重连是否再次摆位、旧动作是否仍缓存，需要以指定SDK和本体确认。退出客户端不自动证明控制器停止。

transformer将streams字段与动作字段双向转换，可通过IValueTransformer插件扩展，内置同名优先。夹爪两指求和乘1250、逆转换每指除2500的例子依赖训练0—100缩放，不能用于所有夹爪。通道key、frame、单位、顺序、归一化与安全限位应一起做往返测试。ROS2话题通了只能确认通信，模型输出与真实动作效果需要分别确认。{{CloudRobo_SimEvaluation}}

## 版本、许可、费用与可复建验收

|层|本轮可定位组合|仍需取得|
|---|---|---|
|官方云文档|产品01/2026-11-02；协议/适配网页采集快照|服务版本、区域和租户功能表|
|SO101依赖|LeRobot v0.5.1；R2C0.1.62文档示例|SDK包、发行记录/许可证及哈希|
|仿真适配|Humble22.04/Jazzy24.04、Python≥3.10|实际O3DE/MetaEngine构建及资产版本|
|训练/部署|平台asset_id、ASCEND_SNT9B镜像标记|权重、CANN/driver/镜像digest与算子表|
|端侧执行|本体配置与模型服务接口|310B/海思目标发行包和实际闭环性能|

LeRobot v0.5.1主体Apache2.0并带派生通知；O3DE本页文档CC BY4.0。它们不授予R2C二进制、云服务、预训练资产、数据或本体SDK的统一许可。CloudRobo samples仓库API被robots拒绝，未取得源码/许可证，不称开源SDK已核验。自定义镜像中的第三方依赖仍需逐项审计。{{LeRobot_License_051}} {{O3DE_ROS2_Gem}}

与本地CANN链比较，CloudRobo可提供空间、血缘、云资源和机器人接口管理；本地链较直接暴露设备和内存，但需要团队自建数据/部署运维。两种机制覆盖不同问题，没有同条件工时、成本或性能测试不作效率排名。CloudRobo开发平台/模型/仿真按包年包月，CCE纳管的ELB另按需；预算和资源释放详见{{REPORT:09_SWOT_Analysis}}。{{CloudRobo_BillingPDF}} {{CloudRobo_BillingManagement}}

可复建放行依次是资产清单/权限核对，输入输出静态验证，dry_run消息往返，仿真动作及独立评测，再真机标定/保护和留出任务；最后检查弱网、重连、重复观测、配置更新/回退、断流及热稳定。独立保存每次尝试、失败、接管和任务结果，测policy-call、动作执行、控制器及伺服层各自频率及P99。平台操作日志不能代替这些任务数据。网页部分静态依赖缺失如实披露；架构PDF和协议原文支持机制研究，不能替代实机、云合同或量产认证。
