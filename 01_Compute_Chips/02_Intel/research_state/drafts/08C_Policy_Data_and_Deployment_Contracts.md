# Intel 08C — 策略数据、部署契约与可复建能力

截止2026-11-05。Studio源码固定b38bff4a9e6d，Suite固定1b0b22a2964f，PhysicalAI runtime和模型卡按各归档对象读取。研究对象是从示范到实际动作的工程契约，不把训练UI或导出成功当机器人验收。

## 痛点：相同权重为何会输出错误动作

策略依赖相机名字、颜色顺序、关节顺序/单位、任务提示、数据归一化和动作队列。编译器能读懂图，并不证明运行时把正确观测送入，也不证明输出对应这台机器的关节。Intel/PhysicalAI路线把这些信息放入数据schema、导出manifest、处理器和runtime配置，有机会减少迁移时隐式约定，但这些机制是开放工程资产，不构成算法独占。[[Intel02C_Runtime_Manifest]]、[[Intel02F_ExportCode]]

| 交接层 | 精确对象 | 需要随包保存 | 错误传播机制 | 放行证据 |
|---|---|---|---|---|
| 示范采集 | FeatureSpec/Store/episode | 相机shape、joint_names、时间 | 顺序错或跨帧混合改变训练标签 | 时间同步与完整episode检查 |
| 训练与微调 | stats、frame transform、checkpoint | 校准、统计量、模型配置 | 单位/符号错导致错误或clamp | 真实数据归一化往返与留出任务 |
| 导出 | manifest、IR/Torch、tokenizer | 输入输出名、runner、处理器 | 图能跑却routing错或缺资产 | 包完整性和数值/动作回归 |
| 运行 | PolicySource/Execution/ActionQueue | device、阈值、fps、动作契约 | 积压旧chunk、停止滞后 | 年龄/超期/异常执行测量 |
| 更新 | 版本目录、模型与配对文件 | 校验和、兼容与回退 | 两文件不同代、旧队列混用 | 断电/重启/回退注入测试 |

## 数据一致性与时间戳并非天然原子

Studio Store每会话一个共享块、每feature独立timestamp，joint vector float64、图像uint8，布局按8字节对齐。FeatureSpec要求关节名及顺序完全一致，所需相机存在且shape相同；额外相机可允许。它阻止一类结构错配，却不检查关节单位、摄像头外参和所有观测属于同一时刻。读到shape正确的数组不代表物理含义正确。[[Intel02F_Store]]

源码明确读写无锁，值先写、时间戳最后写，读者先读stamp，允许混合两个相邻样本；NaN用于未写feature。`read`复制并不能消除复制时并发写造成的混合。该策略可能适合宽容的最新状态展示，但高动态精细操作和训练标签一致性需要独立验证，不能把一tick差异一律视为可接受。应记录各feature的测量/命令时间、跨相机跨度、观测年龄和缺帧处理；如果要求严格快照，应在产品实现和验收层解决，本文未修改源码。

示范数据还需保存成功/失败、接管、任务起止和中断原因，避免只挑成功轨迹掩盖分布偏差。训练与验证按物体/场景/操作者切分，不能让同一轨迹相邻帧泄漏到留出集；导出中grace移动若排除，不应把录制前后过渡误记为模型任务完成。数据许可、现场隐私和视频资产需独立于Apache代码许可处理。[[Intel02F_Recording]]、[[Intel02F_Export]]

## 具体模型：SO101单位、符号与统计量

MolmoAct2的SO100/101发布checkpoint用旧LeRobot约定：身体关节为degree，shoulder_lift反号，shoulder_lift/elbow_flex偏移90度。PhysicalAI驱动身体关节按校准tick范围归一化到[-100,100]，夹爪为[0,100]。文档给出每关节scale为`(range_max-range_min)/200*360/4095`，先做sign×scale×runtime＋offset再按checkpoint统计归一化，输出反向变换。不能把归一化数直接当角度，也不能只改观测不改动作目标。[[Intel04_MolmoAct2]]

scale来自单臂校准，嵌入Torch处理器和OV manifest；换另一台臂的范围要重新导出。启用adapt并复制pretrained统计时无calibration会报错，其他路径可能警告后把runtime单位当degree，后者不是正确适配。旧版本若转换样本未转换stats，训练目标可能clamp，改最终manifest不能恢复丢掉的信号，需要重训。这里的“零样本”也要求本体校准、frame匹配与合适起始姿态，不能推广成任意机械臂开箱通用。

LoRA导出将adapter合并到一次性副本而不改活训练模型，仍需保存base revision、adapter与最终权重校验和。Lightning checkpoint含配置但不含tokenizer文件，OpenVINO导出需要所引用tokenizer资产；只有checkpoint不足以在离线新机器复建。权重卡及数据许可未全部取得，不能因源码支持该模型就判定全资产可商用。[[Intel04_MolmoAct2]]

## 导出产物及原子更新的边界

ExportablePolicyMixin从schema生成batch1样本，scalar保持零维，string用示例prompt；没有schema则调用方需提供真实样本。它还处理OV单输出无名时设output1、多alias输入收敛到配置名字。确定命名有利于runtime routing，但重命名只解决接口键，不能证明forward是推理动作而非训练loss。需要核实际输入数量、shape、噪声/去噪循环、输出动作维度及state reset。[[Intel02F_ExportCode]]

manifest描述已构建的政策包，workflow config描述运行前的流程，不能互换。IR还依赖配对bin、统计safetensors、处理器及必要tokenizer；旧how-to的metadata命名与现行manifest漂移要按实际包读取。Torch、ONNX、OpenVINO和ExecuTorch后端能力按策略分别声明；导出mix-in默认只Torch，库总后端表不能覆盖每个模型。[[Intel02C_Runtime_Manifest]]、[[Intel02F_ExportCode]]

INT8_SYM后处理先把压缩IR写入同文件系统临时目录，释放可能映射bin的OV对象，再以Path.replace依次换xml和bin。这避免跨文件系统移动和删除正在映射的文件，但两个replace分别原子，不是xml/bin配对的单事务；分析上存在第一次替换后、第二次替换前异常或并发读取的窗口。源码注释“atomically replace originals”不能扩写成完整包断电回退保证。量产应先完成全包、校验和及数值回归，再以版本目录/指针方式切换并保留旧包，实际策略队列也需切代。[[Intel02F_Hooks]]

## Runtime与Studio的实际交接

![Studio官方模型格式界面]([[FIG:Intel02F_Figure]])

已打开原图，包含ACT、Torch/OpenVINO/ONNX/ExecuTorch下载卡和文件大小/精度字段；它支持界面产物入口，不证明不同文件的速度、数值等价或任务成功。图上训练时长和大小是展示样例，缺测试配置，本文不作benchmark。[[Intel02F_Figure]]

runtime export源码明确Studio自身不运行在physicalai.runtime之上，只写用户下载的配方；迁移不是“导出原进程”。配方包含SharedRobot/SharedCamera，RGB、validate_on_connect与不覆盖相机设置，默认fps30；未接本体时可保留stored port并标CHANGE_ME，不能拿导出成功当新主机设备连接通过。device来自导出机，到新机需核对加速器。相同robot name在同主机碰撞锁也需考虑会话隔离。[[Intel02F_RuntimeExport]]

PolicySource组合InferenceModel、Sync/AsyncExecution和ChunkedActionQueue，LerpSmoother默认5帧；阈值及消费策略影响过渡延迟。Runtime每tick只看到一个动作，可插值为更多硬件命令但不增加推理。stop在tick之间生效，慢读取/推理的当前tick仍完成并发送；stop保留硬件与callback以便再次run，disconnect才最终释放，失败connect有局部回滚。这里的生命周期清晰，但没有独立急停时限，HIL接管与下游看门狗要另验。[[Intel02C_Runtime_Loop]]

## 可复建优势、对标与放行

多后端和开放schema有利于复用任务数据、权重与外设抽象，相比只提供单个engine，能解释模型到动作的全过程。LeRobot/上游模型也提供数据和frame处理器，不能称Intel独占此机制；真正可积累的是目标机器校准、分区/压缩、异常恢复和任务回归的组合知识。迁移后端仍需重新编译、重测数值和动作质量。[[Intel04_MolmoAct2]]、[[Intel02F_Lib]]

正式包应记录源码/子模块、权重/数据revision、校准、schema、压缩参数、编译器/driver及目标SKU，并分别测留出数据数值、仿真任务、真实本体任务和热稳态故障。SnapFlow有明确seed/分母与独立延迟流程，但设备H100不是Intel端侧，不拿蒸馏结果填补这些环节。本文支持可复建机制判断，尚缺严格快照、成对更新事务、目标本体闭环与生产维护验证，不能将UI/导出接口描述为已完成的量产MLOps保障。[[Intel02F_Benchmark]]
