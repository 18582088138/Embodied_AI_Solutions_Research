# 04 AI能力与模型地图

研究截止2026年11月5日。本章结论是：华为已有可定位到模型资产、训练命令、动作映射和真机接入的CloudRobo路线；昇腾端侧与海思视觉SoC的可部署模型集合则必须另行验证。平台预置“昇腾适配版本”不是每个模型都支持Atlas 200I A2的保证。官方产品介绍PDF版本01、发布日期2026-11-02提供云平台边界；具体实践比总体宣传更适合判断交付成熟度。[CloudRobo_ProductPDF](https://support.huaweicloud.com/productdesc-cloudrobo/CloudRobo%20%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D-pdf.pdf)（[本地原件](../../../reference_metrial/documents/CloudRobo_Pro--522f065088effec2/document.pdf)）

## 任务分类与证据等级

语言模型主要做任务分解、工具调用和文本推理，多模态模型负责图像/视频理解；它们输出的文字和空间描述还需转换成可执行技能。视觉检测、深度、定位输出目标或地图；VLA输出动作，导航策略输出路径；强化学习产生策略修正；传统IK、MPC与轨迹优化属于控制链非学习方法。不能用语言基准分数推算抓取成功率，也不能把三维grounding等同有尺度的SLAM地图。

|任务|代表模型/算法|当前平台证据|必须补验|
|---|---|---|---|
|语言/VLM/agent|Qwen3-VL-4B-Instruct|StarVLA实践下载基模型；作者模型卡|工具调用约束、目标端侧runtime|
|2D视觉|YOLO，ResNet，DBNet/CRNN|旧Ascend示例、Ultralytics第三方Ascend集成|具体模型权重/精度/预处理|
|3D/深度/定位|双目匹配、SLAM/重建路线|DV500 DPU硬件规格，未取得端到端模型报告|标定、尺度、里程计和实际误差|
|VLA/操作|PI0、PI05、PI0FAST、SmolVLA、WALL-OSS、XVLA、ACT|CloudRobo命名资产和操作实践|资产revision、参数量、实际设备|
|导航/运动|CloudRobo-VLN-Track|官方Q25 ROS2实践|地图/障碍保护、并发延迟|
|强化/模仿学习|PI05基础策略+残差RL，LeRobot|UR5E真机强化开发流程|样本数、收敛和实机收益|
|世界模型/全身策略|视频预测、接触/全身控制研究类别|未取得本平台具体交付与模型卡|模型/本体版本、算子与闭环实证|

此分类的空白是证据缺口，不是断言该厂商不存在相应能力。海思Hi3519AV200的8.1TOPS中仅2.5TOPS开放，HNR占用5.6TOPS不可当通用VLA资源；DV500的双目DPU亦不是任意3D神经网络加速器。[HiSilicon_Hi3519AV200](https://www.hisilicon.com/cn/products/smart-vision/machine-vision/hi3519av200)（[本地原件](../../../reference_metrial/webpages/HiSilicon_Hi35--387e661a1427ecf6/index.html)） [HiSilicon_Hi3519DV500](https://www.hisilicon.com/cn/products/smart-vision/machine-vision/hi3519dv500)（[本地原件](../../../reference_metrial/webpages/HiSilicon_Hi35--fb9339639d9cd3da/index.html)） [Ultralytics_Ascend_Doc](https://raw.githubusercontent.com/ultralytics/ultralytics/c4e0ba9310ca5c567adb2b02f351f4d721557c71/docs/en/integrations/ascend.md)（[本地原件](../../../reference_metrial/data/Ultralytics_Ascend--a1db7fce7f18dedb/content.md)）

## 可定位模型与许可

|模型/精确标识|输入与输出|作者资料/许可|平台关系|
|---|---|---|---|
|openvla/openvla-7b|指令+相机，7维末端增量|模型卡MIT；970K机器人episodes|作者CUDA示例；本次无A2优化实证|
|Qwen/Qwen3-VL-4B-Instruct|文字、图像、视频→文本/结构描述|模型卡Apache-2.0|官方StarVLA准备流程引用|
|StarVLA/Qwen3-VL-4B-Instruct-Action|扩展2048动作token的语言logits|继承基模型许可；无机器人head/checkpoint|训练初始化资产，不能直接操控|
|physical-intelligence/fast|连续动作chunk↔离散token|模型卡Apache-2.0；DCT依赖scipy|官方StarVLA流程下载组件|
|LeRobot-PI05-Base|本体状态、双图、prompt→50×6动作示例|平台资产许可/权重revision未取得|预置训练、云部署、SO101调试|
|CloudRobo-VLN-Track|图像+指令上下文→8×4路径点|自研服务，权重/训练数据未取得|官方本体实践，云服务|

以上作者仓库和HF卡均保存2026-11-05原始快照；main链接不是不可变revision。本次归档的是说明/许可，没有下载大模型权重、核验权重哈希或运行trust_remote_code。OpenVLA卡明确代码及checkpoints为MIT，但其Llama-2基底与Open-X各组件数据的义务不能因此忽略；机器人数据并不是一个自动统一的MIT包。Qwen模型卡推荐源码安装Transformers，甚至保留“4.57.0尚未发布”的说明，因此不能把页面采集日期当作所有安装说明同步更新。[OpenVLA_ModelCard](https://huggingface.co/openvla/openvla-7b/raw/main/README.md)（[本地原件](../../../reference_metrial/data/OpenVLA_ModelCard--4cd08e83fb86afd1/content.md)） [Qwen3VL_ModelCard](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct/raw/main/README.md)（[本地原件](../../../reference_metrial/data/Qwen3VL_ModelCard--353ba8bf7970d2bd/content.md)） [StarVLA_ModelCard](https://huggingface.co/StarVLA/Qwen3-VL-4B-Instruct-Action/raw/main/README.md)（[本地原件](../../../reference_metrial/data/StarVLA_ModelCard--bd72b64742a52f43/content.md)） [FAST_ModelCard](https://huggingface.co/physical-intelligence/fast/raw/main/README.md)（[本地原件](../../../reference_metrial/data/FAST_ModelCard--7b5f67fbd3b10ae3/content.md)）

LeRobot v0.5.1代码许可主体Apache-2.0，另有派生模块通知；其许可不自动覆盖相机固件、飞特SDK、平台R2C SDK和训练数据。Physical Intelligence的openpi仓库提供模型及开发路径，但平台的LeRobot转换资产不能仅凭名字等同作者原始权重、JAX实现或精度。PI05的参数量/资产revision在本次公开实践中未完整披露，应由导出的config及manifest确认。[LeRobot_README_051](https://raw.githubusercontent.com/huggingface/lerobot/v0.5.1/README.md)（[本地原件](../../../reference_metrial/data/LeRobot_README_051--166aefbe24a5fba2/content.md)） [LeRobot_License_051](https://raw.githubusercontent.com/huggingface/lerobot/v0.5.1/LICENSE)（[本地原件](../../../reference_metrial/data/LeRobot_License_05--e62ae236f246ce5d/content.txt)） [OpenPI_README](https://raw.githubusercontent.com/Physical-Intelligence/openpi/main/README.md)（[本地原件](../../../reference_metrial/data/OpenPI_README--93ae0cec36eeb1cd/content.md)）

## VLA架构与动作交接

OpenVLA将DINOv2和SigLIP视觉特征接入Llama-2系语言骨干，预测归一化的末端增量：x、y、z、roll、pitch、yaw、gripper。执行前必须使用本体/数据集的统计量反归一化；未经IK、frame转换和限位验证，不能把这七个数直接写SO101的六个关节。模型卡也明确未见过的本体和场景不保证零样本泛化，应采集演示微调。作者示例使用BF16、cuda:0、可选FlashAttention2，仅证明作者路线，不能据此推导CANN具有该kernel。[OpenVLA_ModelCard](https://huggingface.co/openvla/openvla-7b/raw/main/README.md)（[本地原件](../../../reference_metrial/data/OpenVLA_ModelCard--4cd08e83fb86afd1/content.md)）

StarVLA的Action initializer保留Qwen参数并扩展token embedding/output词表，新增token ID为151669—153716。它没有动作维度、归一化、horizon、本体或评测结果；必须训练动作语义并配对同一tokenizer。官方CloudRobo准备示例通过modality.json建立8维state、7维action、双图和task_index映射，state含pad而action不含pad；配置历史state索引−16至−1、动作索引0至7。该索引说明训练样本抽取方式，不能称为8Hz或16秒。[CloudRobo_StarVLA](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0072.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_Star--8d9b312e2d5356a6/index.html)） [StarVLA_ModelCard](https://huggingface.co/StarVLA/Qwen3-VL-4B-Instruct-Action/raw/main/README.md)（[本地原件](../../../reference_metrial/data/StarVLA_ModelCard--bd72b64742a52f43/content.md)）

FAST使用DCT压缩动作序列再转离散token，作者推荐预归一化到[−1,1]的一秒chunk。解码必须恢复time_horizon和action_dim；如果帧率、关节顺序或归一化变化，即使token能解码，也可能得到错误轨迹。作者的示例batch256、50×14是示意数组，不是华为平台吞吐测量。[FAST_ModelCard](https://huggingface.co/physical-intelligence/fast/raw/main/README.md)（[本地原件](../../../reference_metrial/data/FAST_ModelCard--7b5f67fbd3b10ae3/content.md)）

PI05平台实践的r2c.json则输入float32六关节位置、两路uint8图像与PROMPT，输出chunk_size=50、shape=[6]的关节位置。max_iter_num=60、max_run_time=5为该例配置；页面未充分解释时间单位及二者先后优先级，本章不据此声称5秒实时截止或3000动作必定执行。chunk长度不等于策略频率，关节位置动作也必须核实单位、归一化和下层插值。[CloudRobo_Pretrained](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0003.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_Pret--b5692b0c250db726/index.html)） [CloudRobo_CustomModel](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0063.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_Cust--5ae8198484173dda/index.html)）

## 数据—训练—部署—评测闭环

![CloudRobo官方产品架构（PDF物理第5页）](../../../reference_metrial/derived/figures/04_cloudrobo_architecture.png)

图中OBS/SWR、CCE/ModelArts与R2C连接说明平台整合资产、算力和机器人。它支持工作流关系，不能证明训练与仿真全由昇腾NPU执行，也不能证明图上的“发布”已向自有资产开放；正文仍写敬请期待。

官方Notebook列有PI0/PI05/SmolVLA的FFT与LoRA，PI0FAST/WALL-OSS/XVLA的FFT资产下载示例，asset_id可用于定位对象。应把资产ID、导出时间、README、配置、权重哈希、数据统计和镜像digest连成实验单；ID自身不替代不可变版本。PI05示例命令使用单进程accelerate、BF16、gradient checkpointing、offline W&B、训练60steps与20steps保存。这是上手流程，缺batch、设备内存、吞吐和收敛指标，不能称正式性能基准。[CloudRobo_NotebookModels](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0071.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_Note--98c113a13752203d/index.html)） [CloudRobo_TrainAlgorithm](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0037.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_Trai--0224f097e5474a8f/index.html)）

自定义模型流程具体注册ARM镜像、ASCEND/CPU类型与ASCEND_SNT9B规格，操作模型要求r2c.json，并约束OBS路径、单文件30GB、最多100文件和深度10。这是镜像资产与平台规格的标记，不是端侧310B适配矩阵。在线服务“运行中”后才调测，任务成功还须独立观察。官方SO101仿真ACT例并未发布具有完整分母的成功率benchmark。[CloudRobo_CustomModel](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0063.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_Cust--5ae8198484173dda/index.html)） [CloudRobo_BestPractice](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0001.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_Best--c4fa57de5f73616b/index.html)）

残差RL路线冻结BC基础策略，学习逐步修正并允许人类接管，依赖UR5E、正面和腕部RealSense、大寰夹爪、Ubuntu和LeRobot v3数据。厂商称可改善分布偏移和最后一厘米，但未取得统一基线/样本量/完成率数值。冻结策略和有限残差不能代替碰撞保护；系统仍需明确接管优先级、残差幅度和观测时效。[CloudRobo_ResidualOverview](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0019.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_Resi--51dc4befe0b86566/index.html)）

## 资源与性能判断

分析：7B参数以BF16仅权重约14GB十进制，4B约8GB；尚未计视觉骨干差异、KV、激活、工作区、双图、runtime及OS。INT8/INT4可降低权重存储，但不能用除以二/四直接证明端侧运行，必须验证算子、scale、敏感层和任务精度。A2的4/8/12GB不同档位应逐一测量，不合并成“大模型可用”的结论。vLLM Ascend FAQ明确200I A2(310B)尚不支持且无计划；服务器Atlas A2的支持不能移用。[VLLM_Ascend_FAQ](https://raw.githubusercontent.com/vllm-project/vllm-ascend/4a29682d1d8fa89df63a45dc4df2a2a8068984ff/docs/source/faqs.md)（[本地原件](../../../reference_metrial/data/VLLM_Ascend_FAQ--f20d548af3f05045/content.md)）

建议复建时分别测首次加载、预处理、模型推理、RPC、动作排队与机器人完成时间，记录模型/权重revision、batch、分辨率、精度、设备、功率、warmup、样本及P50/P99。再用遮挡、目标移动、网络抖动、相机丢帧和热稳态检查动作年龄。并发导航服务能接收多机器人请求，不代表每台机器人均满足截止时间；VLN文档只给图像≥1Hz要求和8路径点接口，未给吞吐或安全实时保证。[CloudRobo_VLN](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0074.html)（[本地原件](../../../reference_metrial/webpages/CloudRobo_VLN--8a29cdc042132589/index.html)）

本章公开证据足以选择原型路线；不足以批准量产模型。世界模型、全身策略、具体HF权重与目标板卡的同条件评测仍是待取件项。CloudRobo网页正文可读但静态依赖缺失，保留partial_static；最佳实践合订PDF下载失败，未作为有效来源，引用上述已读单页与完整产品PDF。


## 参考资料与原件

下列资料按 2026-11-05 核验时点使用；抓取日期不是发布日期。源码固定到 URL 中的提交 SHA，代表该快照，不保证所有发行包包含相同实现。未运行安装脚本、模型或设备。

| 来源 | 原文 / 本地原件 | 版本与归档边界 |
|---|---|---|
| CloudRobo_ProductPDF | [CloudRobo_ProductPDF](https://support.huaweicloud.com/productdesc-cloudrobo/CloudRobo%20%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D-pdf.pdf) / [原件](../../../reference_metrial/documents/CloudRobo_Pro--522f065088effec2/document.pdf) | 文档01，2026-11-02；完整20页PDF；采集 UTC 2026-11-04T16:53:04.019493+00:00；complete_static |
| CloudRobo_Pretrained | [CloudRobo_Pretrained](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0003.html) / [原件](../../../reference_metrial/webpages/CloudRobo_Pret--b5692b0c250db726/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:52:12.666576+00:00；partial_static |
| CloudRobo_CustomModel | [CloudRobo_CustomModel](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0063.html) / [原件](../../../reference_metrial/webpages/CloudRobo_Cust--5ae8198484173dda/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:52:27.137172+00:00；partial_static |
| CloudRobo_NotebookModels | [CloudRobo_NotebookModels](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0071.html) / [原件](../../../reference_metrial/webpages/CloudRobo_Note--98c113a13752203d/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:55:53.247719+00:00；partial_static |
| CloudRobo_TrainAlgorithm | [CloudRobo_TrainAlgorithm](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0037.html) / [原件](../../../reference_metrial/webpages/CloudRobo_Trai--0224f097e5474a8f/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:55:58.816438+00:00；partial_static |
| CloudRobo_StarVLA | [CloudRobo_StarVLA](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0072.html) / [原件](../../../reference_metrial/webpages/CloudRobo_Star--8d9b312e2d5356a6/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:52:47.647560+00:00；partial_static |
| CloudRobo_ResidualOverview | [CloudRobo_ResidualOverview](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0019.html) / [原件](../../../reference_metrial/webpages/CloudRobo_Resi--51dc4befe0b86566/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:56:01.075479+00:00；partial_static |
| CloudRobo_VLN | [CloudRobo_VLN](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0074.html) / [原件](../../../reference_metrial/webpages/CloudRobo_VLN--8a29cdc042132589/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:52:51.987369+00:00；partial_static |
| CloudRobo_BestPractice | [CloudRobo_BestPractice](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0001.html) / [原件](../../../reference_metrial/webpages/CloudRobo_Best--c4fa57de5f73616b/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:50:49.765509+00:00；partial_static |
| OpenVLA_ModelCard | [OpenVLA_ModelCard](https://huggingface.co/openvla/openvla-7b/raw/main/README.md) / [原件](../../../reference_metrial/data/OpenVLA_ModelCard--4cd08e83fb86afd1/content.md) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:56:12.940869+00:00；complete_static |
| Qwen3VL_ModelCard | [Qwen3VL_ModelCard](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct/raw/main/README.md) / [原件](../../../reference_metrial/data/Qwen3VL_ModelCard--353ba8bf7970d2bd/content.md) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:56:13.885468+00:00；complete_static |
| StarVLA_ModelCard | [StarVLA_ModelCard](https://huggingface.co/StarVLA/Qwen3-VL-4B-Instruct-Action/raw/main/README.md) / [原件](../../../reference_metrial/data/StarVLA_ModelCard--bd72b64742a52f43/content.md) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:56:14.800488+00:00；complete_static |
| FAST_ModelCard | [FAST_ModelCard](https://huggingface.co/physical-intelligence/fast/raw/main/README.md) / [原件](../../../reference_metrial/data/FAST_ModelCard--7b5f67fbd3b10ae3/content.md) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:56:15.676961+00:00；complete_static |
| OpenPI_README | [OpenPI_README](https://raw.githubusercontent.com/Physical-Intelligence/openpi/main/README.md) / [原件](../../../reference_metrial/data/OpenPI_README--93ae0cec36eeb1cd/content.md) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:56:18.462904+00:00；complete_static |
| LeRobot_README_051 | [LeRobot_README_051](https://raw.githubusercontent.com/huggingface/lerobot/v0.5.1/README.md) / [原件](../../../reference_metrial/data/LeRobot_README_051--166aefbe24a5fba2/content.md) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:56:19.389546+00:00；complete_static |
| LeRobot_License_051 | [LeRobot_License_051](https://raw.githubusercontent.com/huggingface/lerobot/v0.5.1/LICENSE) / [原件](../../../reference_metrial/data/LeRobot_License_05--e62ae236f246ce5d/content.txt) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:56:20.670298+00:00；complete_static |
| Ultralytics_Ascend_Doc | [Ultralytics_Ascend_Doc](https://raw.githubusercontent.com/ultralytics/ultralytics/c4e0ba9310ca5c567adb2b02f351f4d721557c71/docs/en/integrations/ascend.md) / [原件](../../../reference_metrial/data/Ultralytics_Ascend--a1db7fce7f18dedb/content.md) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:25:01.762950+00:00；complete_static |
| VLLM_Ascend_FAQ | [VLLM_Ascend_FAQ](https://raw.githubusercontent.com/vllm-project/vllm-ascend/4a29682d1d8fa89df63a45dc4df2a2a8068984ff/docs/source/faqs.md) / [原件](../../../reference_metrial/data/VLLM_Ascend_FAQ--f20d548af3f05045/content.md) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:24:59.633656+00:00；complete_static |
| HiSilicon_Hi3519DV500 | [HiSilicon_Hi3519DV500](https://www.hisilicon.com/cn/products/smart-vision/machine-vision/hi3519dv500) / [原件](../../../reference_metrial/webpages/HiSilicon_Hi35--fb9339639d9cd3da/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T15:55:55.988547+00:00；complete_static |
| HiSilicon_Hi3519AV200 | [HiSilicon_Hi3519AV200](https://www.hisilicon.com/cn/products/smart-vision/machine-vision/hi3519av200) / [原件](../../../reference_metrial/webpages/HiSilicon_Hi35--387e661a1427ecf6/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T15:55:51.885466+00:00；complete_static |

[主张和图源核验](../../evidence/04_AI_Capabilities.json)。各引用保存原始响应、哈希及 metadata；静态归档不承诺动态交互或像素级复现。
