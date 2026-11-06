# Intel 04 — AI能力与模型地图

研究截止：2026-11-05。本文按任务与部署证据分类；Suite采用固定源码对象1b0b22a2964f，Studio采用b38bff4a9e6d，模型卡main是归档时快照。未安装模型、未执行训练或本体评测。

## 任务地图与支持层级

Intel的能力是把上游模型、OpenVINO插件、数据工具和控制组件衔接起来。语言生成、视觉定位、动作生成、轨迹求解属于不同契约。模型名字出现在库中，证明维护者提供相应实现；后端表写CPU/GPU/NPU，不能证明每个策略在每个SKU都编译通过。需要按模型版本、输入形状、精度、插件、驱动和机器人逐条验收。[[Intel02F_Lib]]

| 任务 | 精确对象与模态 | 参数/动作范围 | Intel证据层级 | 模型/资料入口 | 尚缺证据 |
|---|---|---|---|---|---|
| 语言推理/工具规划 | Phi-4-mini-instruct，文本 | 图标注3.8B；卡含128K上下文 | JAKA代码生成部署教程，INT8 OV产物 | [[Intel04_PhiMini]]；[[Intel02C_LLM]] | 长上下文资源/闭环成功率 |
| 语言/agent | Qwen3-8B，文本 | 卡为8.2B，原生32768上下文 | 同教程可替换INT8模型路径 | [[Intel04_Qwen3]] | thinking模式时限与安全执行 |
| 2D分割/语义检索 | SAM、CLIP ViT-B | 官方图91M/149M为图示口径 | 独立encoder/predictor与CLIP IR路径 | [[Intel02C_LLM]] | MobileSAM文件名与SAM版本需锁定 |
| 检测/3D定位 | YOLO与ORB、PCL、FastMapping | 检测框/点云/地图，不是动作 | ROS组件/教程、CPU或GPU优化路径 | [[Intel02D_Detection]]；[[Intel02D_FastMap]] | 目标场景精度、漂移和数据年龄 |
| 非学习控制 | MPC、IK、MoveIt轨迹 | 状态、约束→轨迹/控制量 | 参考管线，非基础模型 | [[Intel04_MPC]] | 接触参数、求解上限和真实安全 |

上表把三维环境表示与模型分开：ORB特征、点云搜索和体素融合不是VLA，也不会因定位可用而自动生成稳定操作。传感器标定、深度失效和运动补偿直接改变策略观测分布，必须继承03的数据契约。

| 操作策略 | 架构与输入/输出 | 具体配置/范围 | 部署证据 | 权重/数据许可边界 |
|---|---|---|---|---|
| ACT | CVAE训练、视觉Transformer→动作chunk | 示例4相机、chunk100；50示范episode | act-ov，CPU/GPU eval；OV2025.2 | 教程链接checkpoint；未取得压缩包内许可，不能作商用授权 |
| Diffusion Policy | 图像或低维→迭代去噪动作 | Push-T四checkpoint，8.96M—262.71M | OV2024.6；encoder与UNet IR，仿真 | 上游代码/数据应独立核对，文件名分数非Intel实测 |
| RDT-1B | SigLIP＋T5＋动作DiT；语言/3视角/状态 | 主干1B，预测64动作；卡示例14维、25Hz | Suite CPU/GPU，MuJoCo 400步任务 | 卡声明代码/权重/微调数据MIT；预训练46数据集及编码器另核 |
| π0.5 LeRobot | PaliGemma前缀＋flow动作expert | 多视角/语言/离散状态；连续动作chunk | 转换、RTC和ALOHA调用教程 | pi05_base卡为Gemma；不是仅按LeRobot代码许可处理 |
| SmolVLA base | SmolVLM2-500M骨干＋flow动作 | 多视角/状态/可选语言，horizon按checkpoint | Studio库实现；本轮无该策略Intel设备实测 | 卡Apache-2.0，数据授权须按数据集 |

对应原文：[[Intel02C_ACT]]、[[Intel02C_DP]]、[[Intel02C_RDT]]、[[Intel04_RDTCard]]、[[Intel02C_Pi05_ModelCard]]、[[Intel04_SmolVLA]]。ACT命令含`--weight 640`，是原文拼写；不静默改成已验证CLI。Diffusion Policy的0.967等是checkpoint命名内test_mean_score，Push-T奖励是最大形状重叠，不能当真实抓取成功率。

## 动作模型的三条深入路径

ACT把逐帧回归改为整段动作预测，减少误差逐步累积，并可用temporal aggregation融合重叠chunk。训练时CVAE编码示范差异，推理的潜变量处理及聚合必须固定。模型导出要求相机数量、分辨率、chunk、hidden_dim、kl_weight与训练一致；相机从一台改四台会改变视觉特征和输入图。示例batch8是命令配置，不能认作实时推理batch或八台机器人并行。动作chunk100也不代表100Hz，下层每tick消费几个动作、旧chunk是否过期决定闭环效果。[[Intel02C_ACT]]

RDT使用统一物理动作空间减少跨数据集格式差异，但目标本体仍需填入对应状态、掩码和动作分量。语言可以预计算embedding，降低在线成本；这不包括语音识别或动态指令生成。其1B参数是动作模型口径，T5-XXL和SigLIP的权重、activation与缓存要额外计入内存。模型卡一方面介绍广泛机械臂兼容，另一方面明确未见本体的embodiment gap，建议小数据微调；因此“通用动作格式”与“零样本通用本体”不能互换。Suite两项任务使用ACT的MuJoCo资产并评估50轨迹的命令，是可复建入口，不是本研究执行的结果。[[Intel04_RDTCard]]、[[Intel02C_RDT]]

π0.5的视觉/文本前缀与动作expert通过flow matching从噪声生成连续动作，RTC用旧chunk未执行尾部约束新chunk前缀，缓解异步推理后的等待与跳变。RTC IR增加`prev_chunk_left_over`和`prefix_weights`；首次调用可传零。相机数、chunk尺寸、动作归一化stats必须与checkpoint相配，IR仍需源配置与tokenizer。教程默认fps50、RTC horizon45是消费计划的配置，不是模型每秒50次完成推理，更不是电机伺服频率。缓存动作还可能因新障碍而变陈旧，需要年龄上限及取消契约。[[Intel02C_RTC_README]]

pi05_base卡只包含flow动作head，原作的subtask prediction、action tokenization和RL部分未包含。现有LeRobot `forward(batch)`用于训练loss，而推理应走select_action/sample_actions路径；旧转换wrapper若导出forward且依赖actions输入，不能因IR生成就判定动作图正确。要核验输出名、shape、噪声与去噪步数、随机数固定是否改变分布，再检查真实数据上的动作误差和任务成功。INT8权重压缩不等于全图INT8 activation，也不能从文件缩小推出更省整机电。[[Intel02C_Pi05_ModelCard]]、[[Intel02C_ExportCode]]、[[Intel02C_LeRobot_PI05_Source]]

## 新策略、世界模型与资源竞争

Studio库还列MolmoAct2、RLDX-1、XR0、Cosmos3，不把名称清单补写成统一NPU支持表。MolmoAct2有`allenai/MolmoAct2-LIBERO`入口，norm_tag解析相机、状态、动作、horizon及控制元数据；Lightning checkpoint不打包tokenizer，旧SO101 frame转换若只改样本而未改统计量，训练信号可能被clamp，需重训，改manifest无法恢复。该例体现模型迁移需要单位和统计数据契约，而不只算子兼容。其完整权重卡和训练数据许可本轮尚未归档，不作全资产许可结论。[[Intel04_MolmoAct2]]

Cosmos3在此是World Action Model的策略实现，含DiT/VAE/action heads与rectified flow；多相机拼成单canvas而非任意token流。默认chunk32，DROID为8维且夹爪反转，ALOHA为14维。Studio默认task_description＋256分辨率，而已发布DROID策略条件为augmented_json＋480，fps15、chunk32虽一致，提示词与视觉分布仍不同。其CPU/XPU/CUDA接口声明不证明OpenVINO NPU可完整执行；视频生成、场景合成和真实物理预测能力也不能由该策略接口推断。RLDX-1/XR0仅按库登记层级收录，精确权重、参数、许可与Intel完整推理结果保留未知。[[Intel04_Cosmos3]]、[[Intel02F_Lib]]

## 官方架构与性能应怎样读

![Intel官方LLM机器人代码生成架构]([[FIG:Intel04_LLMPipelineFigure]])

图原件来自固定Suite；已打开核验。左侧ASR/LLM/视觉与MoveIt是非实时域，右侧共享内存、PLCopen、RTmotion与总线属于另一执行层。图标注Whisper/NPU等候选分工比正文FunASR部署步骤更宽，不能拿图替代逐模型编译记录。图里的SAM ViT-B也不自动解决教程mobilesam_helper命名差异。LLM生成代码必须限制调用集合、参数、坐标frame和工作空间，轨迹规划成功后仍需控制器与安全保护放行。[[Intel04_LLMPipelineFigure]]、[[Intel02C_LLM]]

SnapFlow官方报告给出teacher 1941/2000、20k student 1951/2000，分别97.05%与97.55%，相差0.5个百分点；单seed42不能证明显著改善。H100 PCIe上Torch导出、batch1，5次warmup后100次合成输入chunk，中位175.4ms→58.9ms，包含前后处理，排除render、网络、加载、机器人I/O。它支持蒸馏减少去噪步数的研究路径，不支持Intel加速2.98倍；训练停在27647步，没有30k结果。[[Intel02F_Benchmark]]

部署验证应固定采集→清洗/标注→示范数据版本→训练权重→压缩→目标编译→动作适配→回放与实机监测。CPU同时承担ROS、预处理、求解和运行时回退，iGPU还可能渲染仿真与视觉，NPU有shape/算子/driver边界；必须测并发热稳态下的观测年龄、chunk deadline miss、P99与任务成功/人工介入。规划代码生成、模型延迟和实际操作成功分别存档。本文没有同条件Intel/NVIDIA闭环结果，无法给加速排名、内存最低配置或安全结论。
