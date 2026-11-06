# 08 核心技术护城河总览

本章截至2026-11-05的判断是：Huawei/HiSilicon可用技术积累并不集中在一个通用“具身芯片”上，而分布于昇腾模型执行、海思媒体前端与华为云开发闭环。三者结合可减少适配工作，但公开证据不能证明它们天然组成同一端到端机器人产品。本章把“功能存在”“机制可解释”“实际性能/业务收益成立”分成不同证据层。

正式深度专题为[08A_Ascend_Execution_Compilation](../../../../08A_Ascend_Execution_Compilation.md)、[08B_HiSilicon_Media_Memory](../../../../08B_HiSilicon_Media_Memory.md)、[08C_CloudRobo_Action_Learning](../../../../08C_CloudRobo_Action_Learning.md)。既有08_Proprietary_Technologies.md浅版保留为历史文件，未替用户删除或改名，也不作为本轮完成成果。

## 技术与证据地图

|技术层|解决痛点|核心对象|可确认结论|缺失证据|
|---|---|---|---|---|
|昇腾编译/执行|模型落到目标计算设备|OM、模型内存、dataset、stream|存在完整加载/执行/回收样例|A2目标模型时延/并发/量化精度|
|海思媒体/专用处理|相机与视频持续处理|VI/ISP/VPSS、buffer、NPU/HNR/DPU|模块分工、专用算力和缓存路径|当前SDK细节、整链功耗/热稳定|
|CloudRobo开发闭环|数据/模型/本体接口分散|资产、镜像、r2c.json/YAML、服务ID|配置映射和生效边界可核查|SDK许可、实际闭环与量产状态|
|第三方Ascend学习|开放模型/环境迁移|RLinf actor/rollout/env、910B容器|特定CANN训练路线可定位|端侧支持、同硬件结果、商业收益|

护城河在本文是可积累、可复用的工程能力分析，不是未经检索的专利独占、市场领先或安全认证结论。来源分别为固定ACL代码、DV300文档、当前产品页和CloudRobo协议。[ACL_ModelProcess](https://raw.githubusercontent.com/Ascend/samples/fc2aea93e48be8f8cee51d0c6c1b13a08155f83a/cplusplus/level2_simple_inference/1_classification/resnet50_imagenet_classification/src/model_process.cpp)（[本地原件](../../../../reference_metrial/data/ACL_ModelProcess--4773c545724ea61b/content.cpp)） [HiSilicon_DV300_Media_PDF](https://www.hisilicon.com/dam/asset/view/2a1c6e800feb43f4a8a31f8bcdcdc84a.pdf/download)（[本地原件](../../../../reference_metrial/documents/HiSilicon_DV3--35a27bc010e9b7ba/document.pdf)） [CloudRobo_R2C_Protocol](https://support.huaweicloud.com/sdkreference-cloudrobo/cloudrobo_03_0005.html)（[本地原件](../../../../reference_metrial/webpages/CloudRobo_R2C_--0d6d7a9901ad30ed/index.html)） [RLinf_Ascend_Container](https://raw.githubusercontent.com/RLinf/RLinf/main/docs/source-en/rst_source/examples/embodied/_ascend_libero.rst)（[本地原件](../../../../reference_metrial/data/RLinf_Ascend_Conta--dc5d74c5151ec519/content.rst)）

## 三层交接为何比峰值更重要

传感器输出到媒体buffer，再到模型tensor，最后到机器人action，是三个语义不同的边界。视频分辨率与模型shape之间常有裁剪/缩放/颜色转换；物理/虚拟地址和stride之间有可达性及缓存条件；模型输出坐标、归一化与本体动作之间有frame、单位、关节顺序和控制约束。一个边界处理错误，即使芯片算力足够，也可能产生正确格式但错误语义的动作。

昇腾样例输入wrapper不拥有外层输入存储，输出内存则由模型类管理。海思媒体frame的释放需等待消费者完成。CloudRobo把模型特征映射与机器人配置分开，状态名、图像key和动作列要逐项配对。三者机制共同说明“数据对象生命周期”是实际部署资产；它们不共享同一种内存或执行模型，不能用同一抽象抹平。[ACL_ModelProcess](https://raw.githubusercontent.com/Ascend/samples/fc2aea93e48be8f8cee51d0c6c1b13a08155f83a/cplusplus/level2_simple_inference/1_classification/resnet50_imagenet_classification/src/model_process.cpp)（[本地原件](../../../../reference_metrial/data/ACL_ModelProcess--4773c545724ea61b/content.cpp)） [CloudRobo_R2C_Protocol](https://support.huaweicloud.com/sdkreference-cloudrobo/cloudrobo_03_0005.html)（[本地原件](../../../../reference_metrial/webpages/CloudRobo_R2C_--0d6d7a9901ad30ed/index.html)）

![CloudRobo官方产品架构（PDF物理第5页）](../../../../reference_metrial/derived/figures/04_cloudrobo_architecture.png)

官方图连接资产/算力与本体，用于理解工作流；不是硬件框图，也不证明图中每一步采用同一加速器。OBS承担存储，SWR承担镜像，CCE承担数据/评测资源，ModelArts承担训练资源。这意味着平台可复用团队权限和数据流程，同时也引入独立服务费用、区域可用性和权限责任。[CloudRobo_ProductPDF](https://support.huaweicloud.com/productdesc-cloudrobo/CloudRobo%20%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D-pdf.pdf)（[本地原件](../../../../reference_metrial/documents/CloudRobo_Pro--522f065088effec2/document.pdf)）

## 优势的成立条件与失效条件

昇腾编译部署的优势需要模型主要算子有高效实现、shape配置适合、权重/工作区可驻留且版本组合稳定。若输入不断变化、模型需要未适配kernel、CPU fallback过多或频繁重新编译，工程收益可能缩小。OM是编译产物，不是跨设备通用权重；必须同时保存工具链与目标设备。对标TensorRT同样有builder/runtime和engine/context边界，但公开机制不能证明两平台加速倍数。[NVIDIA_TensorRT_Objects](https://docs.nvidia.com/deeplearning/tensorrt/latest/architecture/how-trt-works.html)（[本地原件](../../../../reference_metrial/webpages/TensorRT_Objec--9df325c2c44e3de5/index.html)）

海思媒体优势适用于固定视觉、编解码、画质和小模型前端，当数据格式、sensor/ISP调优与buffer配置已验证时，可以减少应用CPU处理及重复集成。专用算力同时构成限制：Hi3519AV200的HNR保留5.6TOPS不能借给通用模型，DPU也不能被当任意三维模型引擎。复杂VLA可能更受内存和算子限制，而非视频接口数量限制。[HiSilicon_Hi3519AV200](https://www.hisilicon.com/cn/products/smart-vision/machine-vision/hi3519av200)（[本地原件](../../../../reference_metrial/webpages/HiSilicon_Hi35--387e661a1427ecf6/index.html)）

CloudRobo优势需要工作空间里的数据、模型、镜像、仿真资产与真实机器人配置被成组管理。r2c.json在服务详情、新部署、OBS模型资产和训练终态分别有不同生效规则；如果团队只维护权重版本而忽略映射版本，平台化反而可能掩盖旧配置。云端服务与机器人下层之间还需要动作过期、重连和本地保护，网络可达不等于控制安全。[CloudRobo_R2C_Protocol](https://support.huaweicloud.com/sdkreference-cloudrobo/cloudrobo_03_0005.html)（[本地原件](../../../../reference_metrial/webpages/CloudRobo_R2C_--0d6d7a9901ad30ed/index.html)）

第三方RLinf生态提高算法选择面，910B容器和CPU渲染路径使训练资源和仿真资源分工更清楚。其优势依赖模型、环境、CANN/torch_npu和外部算子版本正确配对；World-model生成与真实物理的误差不能用策略得分自动消除。算法开放并不把海思、310B或CloudRobo全部组合变成已验证支持。[RLinf_Ascend_Container](https://raw.githubusercontent.com/RLinf/RLinf/main/docs/source-en/rst_source/examples/embodied/_ascend_libero.rst)（[本地原件](../../../../reference_metrial/data/RLinf_Ascend_Conta--dc5d74c5151ec519/content.rst)） [RLinf_Wan_Guide](https://raw.githubusercontent.com/RLinf/RLinf/main/docs/source-en/rst_source/examples/embodied/wan.rst)（[本地原件](../../../../reference_metrial/data/RLinf_Wan_Guide--14ee3f4821f26eef/content.rst)）

## 性能与比较的证据尺度

当前公开资料可列硬件峰值、接口约束和开发流程，但缺少统一的机器人任务基准：同一权重、输入相机、精度/batch、功率/温度、样本数量和预处理/RPC口径。模型kernel快不一定让闭环快；模型吞吐也不等于每帧观测年龄低。规划成功、仿真成功、真机自主完成、连续在岗运营和收益需要各自分母与统计。

RLinf Wan结果体现作者任务协议下训练前后的策略差异，不能标成Ascend板卡成绩。CUDA官方内存模型也表明统一地址、managed、mapped和硬件一致性不等价；这些事实只能用于比较问题处理方法，不能把某种互联能力套海思。本文不使用“最低功耗”“最强生态”或“全国产化”作为可验证结论。[RLinf_Wan_Guide](https://raw.githubusercontent.com/RLinf/RLinf/main/docs/source-en/rst_source/examples/embodied/wan.rst)（[本地原件](../../../../reference_metrial/data/RLinf_Wan_Guide--14ee3f4821f26eef/content.rst)） [NVIDIA_CUDA_Memory](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/understanding-memory.html)（[本地原件](../../../../reference_metrial/webpages/CUDA_Memory--453cf4bfa7cf193e/index.html)）

## 迁移资产、许可与维护

可迁移资产优先是源模型/训练数据定义、sensor标定、任务规范、动作/状态契约及测试集；平台专用engine、OM、WK、prefab和BSP二进制需要重新构建/校验。将CUDA代码移到昇腾，或将ACL应用移到海思，不能仅替换API名称；线程/内存/算子/同步和错误恢复模型都可能改变。对有状态策略，还要保存tokenizer、归一化、history与chunk配置。

代码、权重、数据、runtime、firmware、资产和本体SDK许可应分别核验；开源算法不自动授权所有训练数据或商业SDK分发。版本维护还要覆盖PCN/EOL、热设计、产测、OTA/回退和备件。现有文献没有完整交付承诺，不能把技术方案可实现当已获采购和量产放行。

建议科研原型选择最短可复建链，固定模型/本体和环境；媒体节点优先验证长期视频+模型并发；操作机器人先确认动作映射和本地保护，再增加云学习；多机器人云推理须隔离会话状态、观测ID和队列，测每个本体P99及失联表现。所有方案都需要先获得目标SDK/BSP与正式许可，再用实际样机进行放行。

## 本章完成与待核验事项

三个专题独立保留baseline、evidence、quality与dedup，总览引用为专题联合清单，资料目录按08_core导出。每张使用的官方图本轮实际打开，正文说明图能支持的结论。静态依赖部分缺失如实披露；完整产品PDF与源码原件可复查。质量检查证明文件结构与引用归档一致，不自动证明语义或硬件成绩。

下一步09据此评估科研、视觉前端、操作、导航、消费/工业和安全应用，使用事实→影响机制→成立条件→选型动作。尚待取件包括准确SKU/BSP、当前算子/量化支持、模型与本体同条件闭环、价格/供货/生命周期、客户商业运营数据及适用地区监管原文，不能从技术机制直接推出市场份额和ROI。


## 参考资料与原件

下列资料按 2026-11-05 核验时点使用；抓取日期不是发布日期。源码固定到 URL 中的提交 SHA，代表该快照，不保证所有发行包包含相同实现。未运行安装脚本、模型或设备。

| 来源 | 原文 / 本地原件 | 版本与归档边界 |
|---|---|---|
| CloudRobo_ProductPDF | [CloudRobo_ProductPDF](https://support.huaweicloud.com/productdesc-cloudrobo/CloudRobo%20%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D-pdf.pdf) / [原件](../../../../reference_metrial/documents/CloudRobo_Pro--522f065088effec2/document.pdf) | 文档01，2026-11-02；完整20页PDF；采集 UTC 2026-11-04T16:53:04.019493+00:00；complete_static |
| ACL_ModelProcess | [ACL_ModelProcess](https://raw.githubusercontent.com/Ascend/samples/fc2aea93e48be8f8cee51d0c6c1b13a08155f83a/cplusplus/level2_simple_inference/1_classification/resnet50_imagenet_classification/src/model_process.cpp) / [原件](../../../../reference_metrial/data/ACL_ModelProcess--4773c545724ea61b/content.cpp) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:26:46.107974+00:00；complete_static |
| HiSilicon_DV300_Media_PDF | [HiSilicon_DV300_Media_PDF](https://www.hisilicon.com/dam/asset/view/2a1c6e800feb43f4a8a31f8bcdcdc84a.pdf/download) / [原件](../../../../reference_metrial/documents/HiSilicon_DV3--35a27bc010e9b7ba/document.pdf) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:31:04.931888+00:00；complete_static |
| HiSilicon_Hi3519AV200 | [HiSilicon_Hi3519AV200](https://www.hisilicon.com/cn/products/smart-vision/machine-vision/hi3519av200) / [原件](../../../../reference_metrial/webpages/HiSilicon_Hi35--387e661a1427ecf6/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T15:55:51.885466+00:00；complete_static |
| CloudRobo_R2C_Protocol | [CloudRobo_R2C_Protocol](https://support.huaweicloud.com/sdkreference-cloudrobo/cloudrobo_03_0005.html) / [原件](../../../../reference_metrial/webpages/CloudRobo_R2C_--0d6d7a9901ad30ed/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T17:16:19.243550+00:00；partial_static |
| RLinf_Ascend_Container | [RLinf_Ascend_Container](https://raw.githubusercontent.com/RLinf/RLinf/main/docs/source-en/rst_source/examples/embodied/_ascend_libero.rst) / [原件](../../../../reference_metrial/data/RLinf_Ascend_Conta--dc5d74c5151ec519/content.rst) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T17:12:19.065351+00:00；complete_static |
| RLinf_Wan_Guide | [RLinf_Wan_Guide](https://raw.githubusercontent.com/RLinf/RLinf/main/docs/source-en/rst_source/examples/embodied/wan.rst) / [原件](../../../../reference_metrial/data/RLinf_Wan_Guide--14ee3f4821f26eef/content.rst) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T17:09:13.222465+00:00；complete_static |
| NVIDIA_TensorRT_Objects | [NVIDIA_TensorRT_Objects](https://docs.nvidia.com/deeplearning/tensorrt/latest/architecture/how-trt-works.html) / [原件](../../../../reference_metrial/webpages/TensorRT_Objec--9df325c2c44e3de5/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T17:11:40.683207+00:00；complete_static |
| NVIDIA_CUDA_Memory | [NVIDIA_CUDA_Memory](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/understanding-memory.html) / [原件](../../../../reference_metrial/webpages/CUDA_Memory--453cf4bfa7cf193e/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T17:12:04.011696+00:00；complete_static |
| ACL_ResNet_README | [ACL_ResNet_README](https://raw.githubusercontent.com/Ascend/samples/fc2aea93e48be8f8cee51d0c6c1b13a08155f83a/cplusplus/level2_simple_inference/1_classification/resnet50_imagenet_classification/README_CN.md) / [原件](../../../../reference_metrial/data/ACL_ResNet_README--7ee889c63c64edd5/content.md) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:26:44.928697+00:00；complete_static |
| ACL_SampleProcess | [ACL_SampleProcess](https://raw.githubusercontent.com/Ascend/samples/fc2aea93e48be8f8cee51d0c6c1b13a08155f83a/cplusplus/level2_simple_inference/1_classification/resnet50_imagenet_classification/src/sample_process.cpp) / [原件](../../../../reference_metrial/data/ACL_SampleProcess--b1cece1042fbfdaa/content.cpp) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:26:47.147990+00:00；complete_static |
| ACL_Async_ModelProcess | [ACL_Async_ModelProcess](https://raw.githubusercontent.com/Ascend/samples/fc2aea93e48be8f8cee51d0c6c1b13a08155f83a/cplusplus/level2_simple_inference/1_classification/resnet50_async_imagenet_classification/src/model_process.cpp) / [原件](../../../../reference_metrial/data/ACL_Async_ModelPro--9aab3388a79f9a2b/content.cpp) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:26:49.315372+00:00；complete_static |
| ACL_Dynamic_README | [ACL_Dynamic_README](https://raw.githubusercontent.com/Ascend/samples/fc2aea93e48be8f8cee51d0c6c1b13a08155f83a/cplusplus/level2_simple_inference/1_classification/resnet50_imagenet_dynamic_dims/README_CN.md) / [原件](../../../../reference_metrial/data/ACL_Dynamic_README--0e7479d186c8d8e5/content.md) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:26:48.201531+00:00；complete_static |
| ACL_FirstApp_Figure | [ACL_FirstApp_Figure](https://raw.githubusercontent.com/Ascend/samples/fc2aea93e48be8f8cee51d0c6c1b13a08155f83a/cplusplus/level2_simple_inference/1_classification/resnet50_firstapp/README_fig.png) / [原件](../../../../reference_metrial/data/ACL_FirstApp_Figur--f1da2d06245dd3cc/content.png) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:26:50.678467+00:00；complete_static |
| Ascend_Samples_License | [Ascend_Samples_License](https://raw.githubusercontent.com/Ascend/samples/fc2aea93e48be8f8cee51d0c6c1b13a08155f83a/LICENSE) / [原件](../../../../reference_metrial/data/Ascend_Samples_Lic--181037fb87140fdd/content.txt) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:24:54.066194+00:00；complete_static |
| TorchNPU_Compatibility | [TorchNPU_Compatibility](https://raw.githubusercontent.com/Ascend/pytorch/848b8e7271069d5a9947bf75fd02a162092b41a6/COMPATIBILITY.md) / [原件](../../../../reference_metrial/data/TorchNPU_Compatibi--c8e8a0ecbae18c29/content.md) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:26:54.995372+00:00；complete_static |
| MindSpore_Lite_Context | [MindSpore_Lite_Context](https://raw.githubusercontent.com/mindspore-ai/mindspore/16873579685a1662f10ebd1df068bf512f211869/mindspore/lite/python/api/context.py) / [原件](../../../../reference_metrial/data/MindSpore_Lite_Con--05d6c61893baf702/content.py) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:27:03.683423+00:00；complete_static |
| Ultralytics_Ascend_Exporter | [Ultralytics_Ascend_Exporter](https://raw.githubusercontent.com/ultralytics/ultralytics/c4e0ba9310ca5c567adb2b02f351f4d721557c71/ultralytics/utils/export/ascend.py) / [原件](../../../../reference_metrial/data/Ultralytics_Ascend--0826b6cee47ed307/content.py) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:26:59.797042+00:00；complete_static |
| Ultralytics_Ascend_Backend | [Ultralytics_Ascend_Backend](https://raw.githubusercontent.com/ultralytics/ultralytics/c4e0ba9310ca5c567adb2b02f351f4d721557c71/ultralytics/nn/backends/ascend.py) / [原件](../../../../reference_metrial/data/Ultralytics_Ascend--85889b8b8d60cc34/content.py) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:27:00.982899+00:00；complete_static |
| VLLM_Ascend_FAQ | [VLLM_Ascend_FAQ](https://raw.githubusercontent.com/vllm-project/vllm-ascend/4a29682d1d8fa89df63a45dc4df2a2a8068984ff/docs/source/faqs.md) / [原件](../../../../reference_metrial/data/VLLM_Ascend_FAQ--f20d548af3f05045/content.md) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:24:59.633656+00:00；complete_static |
| HiSilicon_DV300_SDK_PDF | [HiSilicon_DV300_SDK_PDF](https://www.hisilicon.com/dam/asset/view/7c925d6a091b49b5b1d1b0dc28d6dc4b.pdf/download) / [原件](../../../../reference_metrial/documents/HiSilicon_DV3--7dcd59b2f2952de6/document.pdf) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:30:58.571674+00:00；complete_static |
| HiSilicon_DV300_SVP_PDF | [HiSilicon_DV300_SVP_PDF](https://www.hisilicon.com/dam/asset/view/4ef2e012655a4aae8c80619b8cfd093f.pdf/download) / [原件](../../../../reference_metrial/documents/HiSilicon_DV3--8b4b0448c818638c/document.pdf) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:31:10.189959+00:00；complete_static |
| HiSilicon_Hi3403V100 | [HiSilicon_Hi3403V100](https://www.hisilicon.com/cn/products/smart-vision/machine-vision/hi3403v100) / [原件](../../../../reference_metrial/webpages/HiSilicon_Hi34--c2d6971a30360f9c/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T15:55:36.357424+00:00；complete_static |
| HiSilicon_Hi3519DV500 | [HiSilicon_Hi3519DV500](https://www.hisilicon.com/cn/products/smart-vision/machine-vision/hi3519dv500) / [原件](../../../../reference_metrial/webpages/HiSilicon_Hi35--fb9339639d9cd3da/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T15:55:55.988547+00:00；complete_static |
| HiSilicon_Hi3516CV610 | [HiSilicon_Hi3516CV610](https://www.hisilicon.com/cn/products/smart-vision/machine-vision/hi3516cv610) / [原件](../../../../reference_metrial/webpages/HiSilicon_Hi35--7e91d964fbc23ad4/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T15:54:58.249797+00:00；complete_static |
| HiView_3403_VPSS | [HiView_3403_VPSS](https://raw.githubusercontent.com/openhisilicon/HIVIEW/395b53d4c28cf5e528c9e1ba3f7ec39ad8e852d4/mod/svp/3403/vpss_capture.cpp) / [原件](../../../../reference_metrial/data/HiView_3403_VPSS--724494f823f91527/content.cpp) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:38:01.012968+00:00；complete_static |
| HiView_3403_YOLO | [HiView_3403_YOLO](https://raw.githubusercontent.com/openhisilicon/HIVIEW/395b53d4c28cf5e528c9e1ba3f7ec39ad8e852d4/mod/svp/3403/yolov8.cpp) / [原件](../../../../reference_metrial/data/HiView_3403_YOLO--b8c035537722bae0/content.cpp) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:38:03.318452+00:00；complete_static |
| OH_Media_EULA | [OH_Media_EULA](https://raw.githubusercontent.com/openharmony/device_soc_hisilicon/7c1e2d5b35c090009bbe195f09337701c60af032/hi3516dv300/sdk_linux/out/lib/LICENSE) / [原件](../../../../reference_metrial/data/OH_Media_EULA--d888125c58c7c3fd/content.txt) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T16:38:04.870536+00:00；complete_static |
| CloudRobo_MetaEngineAdapter | [CloudRobo_MetaEngineAdapter](https://support.huaweicloud.com/sdkreference-cloudrobo/cloudrobo_03_0043.html) / [原件](../../../../reference_metrial/webpages/CloudRobo_Meta--ee80c57df6e65a65/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T17:16:33.063349+00:00；partial_static |
| CloudRobo_SimEvaluation | [CloudRobo_SimEvaluation](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0057.html) / [原件](../../../../reference_metrial/webpages/CloudRobo_SimE--ed5202e058aafdf3/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T17:01:04.460075+00:00；partial_static |
| CloudRobo_Pretrained | [CloudRobo_Pretrained](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0003.html) / [原件](../../../../reference_metrial/webpages/CloudRobo_Pret--b5692b0c250db726/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:52:12.666576+00:00；partial_static |
| CloudRobo_VLN | [CloudRobo_VLN](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0074.html) / [原件](../../../../reference_metrial/webpages/CloudRobo_VLN--8a29cdc042132589/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:52:51.987369+00:00；partial_static |
| CloudRobo_ResidualOverview | [CloudRobo_ResidualOverview](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0019.html) / [原件](../../../../reference_metrial/webpages/CloudRobo_Resi--51dc4befe0b86566/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T16:56:01.075479+00:00；partial_static |
| CloudRobo_ResidualDebug | [CloudRobo_ResidualDebug](https://support.huaweicloud.com/bestpractice-cloudrobo/cloudrobo_05_0027.html) / [原件](../../../../reference_metrial/webpages/CloudRobo_Resi--2af60c241cd552d0/index.html) | 页面未标版号；按采集快照使用；采集 UTC 2026-11-04T17:05:48.028639+00:00；partial_static |
| RLinf_OpenPI_Guide | [RLinf_OpenPI_Guide](https://raw.githubusercontent.com/RLinf/RLinf/main/docs/source-en/rst_source/examples/embodied/pi0.rst) / [原件](../../../../reference_metrial/data/RLinf_OpenPI_Guide--8e9c1b7c17ea131a/content.rst) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T17:09:11.242037+00:00；complete_static |
| RLinf_StarVLA_Guide | [RLinf_StarVLA_Guide](https://raw.githubusercontent.com/RLinf/RLinf/main/docs/source-en/rst_source/examples/embodied/starvla.rst) / [原件](../../../../reference_metrial/data/RLinf_StarVLA_Guid--09b731053f6e4f1a/content.rst) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T17:09:12.182538+00:00；complete_static |
| RLinf_OSMesa_Setup | [RLinf_OSMesa_Setup](https://raw.githubusercontent.com/RLinf/RLinf/main/docs/source-en/rst_source/examples/embodied/_libero_osmesa.rst) / [原件](../../../../reference_metrial/data/RLinf_OSMesa_Setup--c1983dc981b877a3/content.rst) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T17:12:20.011705+00:00；complete_static |
| RLinf_License | [RLinf_License](https://raw.githubusercontent.com/RLinf/RLinf/main/LICENSE) / [原件](../../../../reference_metrial/data/RLinf_License--dca3f21b2135ad15/content.txt) | 固定提交源码/许可快照；确切 SHA 见原文 URL；采集 UTC 2026-11-04T17:08:15.888730+00:00；complete_static |

[主张和图源核验](../../../evidence/08_Core_Technology_Moat.json)。各引用保存原始响应、哈希及 metadata；静态归档不承诺动态交互或像素级复现。
