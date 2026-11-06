# 02E｜vLLM-MLU、云端编排与监控运维

本篇研究具身系统可能使用的云端语言推理、训练资源分配与运行观测。可核验的交付对象包括vLLM-MLU插件、Kubernetes device plugin和mlu-exporter源码；这些组件分别处理模型服务、设备资源和指标，没有取得厂商机器人云端动作协议、策略SLA或OTA回滚方案。当前证据更适合把寒武纪评估为云端模型服务候选。数据截止2026-11-05，未构建镜像、启动集群或发送推理请求。

## 1. 插件入口与配套版本

vLLM-MLU README声明只支持“MLU370以上”设备；保留原措辞，不将其扩展到MLU220或全部云端SKU。仓库默认分支为v0.11.2-dev，本篇固定树SHA dc984838c63a，属于开发快照，不能认证为稳定发布。2026-04-24新增DeepSeekV4支持是厂商公告，不是该模型在所有SKU上的性能、精度或机器人任务报告。[VLLM](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/README.md)

`setup.py` 注册两个入口：`vllm.platform_plugins` 的 `mlu` 和 `vllm.general_plugins` 的 `mlu_hijack`。进一步读 `vllm_mlu/__init__.py`，前者返回MLUPlatform类路径，后者导入mlu_hijack并注册模型。可见既有平台接口，也有模型和行为适配；仅用“插件”名称不能推导完全无需上游改动。README安装上游vLLM时指定 `VLLM_TARGET_DEVICE=empty`，再装vllm-mlu，还要求Ray2.51.1并复制修改多个Ray文件。[VSET](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/setup.py) [Cambricon_vllm-mlu_vllm_mlu___init___py](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/vllm_mlu/__init__.py) [VLLM](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/README.md)

| 交付对象 | 本轮核验范围 | 明确依赖 | 仍需锁定 |
|---|---|---|---|
| vLLM-MLU | v0.11.2-dev固定SHA | torch2.9.1、torch-mlu≥1.29.1、torch_mlu_ops≥1.8.1 | 商业SDK、driver、上游vLLM精确配套 |
| Python依赖表 | 当前requirements.txt | Ray2.51.1、click8.2.1、triton≥3.2.0等 | 实际解析后lock、平台wheel和ABI |
| K8s device plugin | SHA cccdd66de08a | mtp372 driver≥4.20.9；mtp592≥5.0.0 | CNDEV/cntopo、镜像摘要、容器runtime |
| SMLU先决条件 | device-plugin README | driver≥5.10.27、cndev≥3.9.0 | 具体设备、隔离模式与可用配置 |
| exporter | SHA648a19c7d781 | CNDEV运行最低要求与构建header分列 | 当前CLI冲突、支持指标和采样窗口 |

vLLM requirements的torch2.9.1与 [02C_PyTorch_Backend_and_Distributed_Training.md](02C_PyTorch_Backend_and_Distributed_Training.md) 中torch2.1示例是两条配套路线，不能混装。setup的python_requires≥3.8只是包元数据下界；实际torch及其他依赖会加约束，不能据此认定Python3.8可用。版本字符串读取 `tools/build.property`，本轮所取tree未定位到该路径，构建产物版本仍待完整包核验。自定义kernel还涉及CMake/pybind11与设备依赖；Python源码归档不是成功构建证明。[VREQ](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/requirements.txt) [VSET](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/setup.py) [K8S](https://raw.githubusercontent.com/Cambricon/cambricon-k8s-device-plugin/cccdd66de08ad6b8ade94d140a8cc7d63b87353f/device-plugin/README.md) [EXPORT](https://raw.githubusercontent.com/Cambricon/mlu-exporter/648a19c7d781ada2ea693e46edc562aa57f79be4/README.md)

## 2. 调度、图和量化的有效配置取决于模型

`MLUPlatform` 定义device_type=mlu、dist_backend=cncl、设备可见变量MLU_VISIBLE_DEVICES，Ray资源键却沿用GPU。这是调度标识，不表示芯片执行CUDA。平台列出weightonly、smoothquant、awq_mlu、gptq_mlu、fp8并调用量化注册，表明存在适配入口；每个方法的精度、支持模型、权重布局和硬件范围仍须逐项验证，不能套用MagicMind INT8校准结果。[VPLAT](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/vllm_mlu/platforms/mlu.py)

`check_and_update_config` 选择MLUWorker，强制CompilationMode.NONE、FULL_DECODE_ONLY图模式并启用custom_ops，关闭cascade attention；use_mla时，DeepSeek MCC启用或未使用full mlugraph会关闭chunked prefill，MCC还关闭prefix caching。若max_num_batched_tokens小于max_model_len且未分块，普通模式报错，benchmark模式只警告。因此要保存的是经代码调整后的有效配置，而非启动命令和功能清单。源码中有两个同名 `import_kernels` 方法，Python最终定义会覆盖前者；不能引用前一个导入torch_mlu_ops的片段来认定实际初始化行为。[VPLAT](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/vllm_mlu/platforms/mlu.py)

优势机制是按prefill/decode特点调度，复用缓存和图以降低重复工作；成立条件包括模型路径、shape、缓存布局和调度选项彼此兼容。本轮没有请求trace、设备计时或负载曲线，不能从注册函数返回true推出吞吐优势、TTFT或P99。迁移时应分别测试冷启动、长上下文、多请求和恢复路径，确认功能在实际运行组合中被启用。

## 3. KV cache与attention：按实际布局核对

MLUFlashAttentionBackend的 `get_kv_cache_shape` 返回 `(2,num_blocks,num_kv_heads,block_size,head_size)`，scale形状是 `(2,num_blocks,num_kv_heads,block_size)`；同文件forward docstring残留另一种block_size/num_kv_heads顺序。这里以实际形状函数为依据，保留注释冲突并要求运行时核stride，不把通用vLLM布局直接套到MLU。它列出支持block size1/16/32/64及若干head size，这只是该backend的候选集合，不是任意模型所有算子已通过。[ATTN](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/vllm_mlu/v1/attention/backends/flash_attn.py)

forward的输入query/key/value分别带token、head和head_size维，output必须由外部提供；output_scale/output_block_scale存在时直接抛“fused output quantization未支持”。quantized KV路径调用 `quant_to_paged_cache`，其他路径调用 `reshape_paged_cache`，都截取num_actual_tokens并使用slot_mapping写入页式缓存。分析：cache索引、量化scale、实际token数和并行分片若不同步，既可能读错历史上下文，也会破坏数值；因此量化权重、KV量化和输出量化应分开验收。源码有明确机制，尚无本轮模型精度和内存收益测量。[ATTN](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/vllm_mlu/v1/attention/backends/flash_attn.py)

README在线例程设端口8100、block-size1、maxlen4096、tensor parallel8、memory utilization0.96，并带 `--no-enable-prefix-caching` 和 `--enforce-eager`。不能称这条命令已启用缓存和图优化，或把0.96当安全容量余量；还需计算权重、KV、workspace、并行通信及碎片。OpenAI风格 `/v1/completions` 的输出是模型文本，动作坐标、有效期、权限、超时和断网降级均未由该接口定义。[VLLM](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/README.md)

## 4. Kubernetes：设备分配不等于时延隔离

device plugin以DaemonSet报告节点MLU数量、健康并允许容器消费 `cambricon.com/mlu` 资源。节点需先装驱动/NeuWare，构建要求cndev.h6.5.24、libcndev.so、cntopo及CNCL；运行最低版本与编译header要求分别保留，不能把header版本当所有环境的driver版本。amd64/arm64构建选项表示插件目标架构，不证明220 Arm BSP或机器人Ubuntu镜像。[K8S](https://raw.githubusercontent.com/Cambricon/cambricon-k8s-device-plugin/cccdd66de08ad6b8ade94d140a8cc7d63b87353f/device-plugin/README.md)

README区分default、env-share、mim和topology-aware：env-share将整卡分给多个容器，mim要求主机预设，拓扑模式尝试构成MLULink环。guaranteed/restricted策略只在请求1/2/4/8卡时说明有效，K8s<1.19不能使用该拓扑模式。SMLU最低依赖另列，但示例mode列表未完全解释所有SMLU配置，本轮不补造命令。整卡共享不等于硬件分区，多容器数量不证明内存/带宽隔离或截止时间SLA。[K8S](https://raw.githubusercontent.com/Cambricon/cambricon-k8s-device-plugin/cccdd66de08ad6b8ade94d140a8cc7d63b87353f/device-plugin/README.md)

与多卡CNCL接口对照，plugin决定“进程得到哪些设备”，CNCL负责“张量如何通信”，vLLM负责“请求如何调度”。设备环选择可能降低不合适拓扑的风险，但没有互联实测与模型数据便不能量化收益；Pod重启与任务checkpoint、KV恢复、机器人执行状态恢复还需应用层实现。NVIDIA方向可比较的迁移资产是资源命名、容器依赖、拓扑约束和度量接口，本篇不据通用编排概念给出厂商排名。

## 5. Exporter：指标语义与文档冲突

mlu-exporter提供30108端口/metrics和cndev、mpm、podresources、host collector。MPM速率指标以两次采样差分计算；默认按scrape采样或后台固定间隔的说明影响CPU成本与统计窗口，100ms采样不会自动得到100ms策略响应。K8s低于1.15的podresources需特定feature gate。README又留有未合并冲突标记，virtual-mode有env-share与dynamic-smlu两种表述，mpm-interval-ms项在冲突一侧；不能把整段README当无冲突部署手册。[EXPORT](https://raw.githubusercontent.com/Cambricon/mlu-exporter/648a19c7d781ada2ea693e46edc562aa57f79be4/README.md)

本轮取得实际 `examples/metrics.yaml` 和 `pkg/metrics/conf.go` 交叉核对：YAML有物理memory_used（B）、mpm利用率（%）及uuid/model/driver等标签；Conf对象按collector→metric读取Name、Help、Labels、Push，读取/解析失败返回错误并Fatal。它可以核实指标配置结构，尚不足以解决所有CLI flag和动态SMLU组合，仍需固定发布版本、help输出和目标卡运行检查。指标命名、单位和支持范围应一起归档，不能只保留Dashboard图。[Cambricon_mlu-exporter_examples_metrics_yaml](https://raw.githubusercontent.com/Cambricon/mlu-exporter/648a19c7d781ada2ea693e46edc562aa57f79be4/examples/metrics.yaml) [Cambricon_mlu-exporter_pkg_metrics_conf_go](https://raw.githubusercontent.com/Cambricon/mlu-exporter/648a19c7d781ada2ea693e46edc562aa57f79be4/pkg/metrics/conf.go)

README明确MLU370不支持cluster temperature，该类指标置0。0在此是不可用占位，不是实际0°C或设备健康证据；告警需同时处理指标缺失、占位、支持清单和采样状态。硬件利用率、内存、错误事件与请求延迟应按device UUID、模型/镜像版本及request ID关联；目前只有硬件指标接口，无本轮TTFT、tokens/s、P99、WCET和机器人任务成功率，不能从低利用率或无错误推出闭环正常。[EXPORT](https://raw.githubusercontent.com/Cambricon/mlu-exporter/648a19c7d781ada2ea693e46edc562aa57f79be4/README.md)

## 6. 发布与可复建验证边界

分析建议的部署顺序为：先冻结SDK/driver/固件/torch/插件与镜像摘要，解析依赖并构建单节点最小例程；记录有效量化、cache和图配置，核同一输入的输出与长上下文；再接K8s核设备分配、共享模式及健康变更，最后以请求trace关联exporter指标并测试进程/节点故障。模型更新应版本化权重、tokenizer、template和cache键，重建或清理不兼容缓存；这些是验收动作，不是厂商已提供的OTA框架。

本轮没有该专题专用官方架构图，使用代码、配置和版本条目作为证据；未造图或性能曲线。上游vLLM插件网页未成功取得，未引用其正文。三个仓库源码LICENSE均为Apache2.0，设备SDK/固件、容器基础镜像、模型权重/数据和本体SDK的许可及交付须单独核验。云端文本服务到机器人策略与动作的连线仍是系统集成缺口，需明确网络失效、观测过期和控制器响应后才能判断具身适用性。[VLIC](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/LICENSE) [KLIC](https://raw.githubusercontent.com/Cambricon/cambricon-k8s-device-plugin/cccdd66de08ad6b8ade94d140a8cc7d63b87353f/LICENSE) [EXLIC](https://raw.githubusercontent.com/Cambricon/mlu-exporter/648a19c7d781ada2ea693e46edc562aa57f79be4/LICENSE)

## 参考资料与本地原文

所有正文来源均为2026-11-05采集的归档快照。官网未标发布日期时不使用版权年充当版本；仓库原件URL固定于树SHA，具体提交日期未独立核验。`complete_static`对单独源码/Markdown仅指主文件原件取得，不保证其相对链接、子模块、镜像、模型权重和训练数据均已下载。

| 材料 | 原始URL与版本边界 | 本地原件 | 归档状态 |
|---|---|---|---|
| Cambricon_vllm-mlu_README_md | [原文](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/README.md)；源码固定树SHA dc984838c63a | [原件](REFERENCES.md#ref-c734c5a91d456c8d) | complete_static |
| Cambricon_vllm-mlu_setup_py | [原文](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/setup.py)；源码固定树SHA dc984838c63a | [原件](REFERENCES.md#ref-019b730a22d449c9) | complete_static |
| Cambricon_vllm-mlu_vllm_mlu___init___py | [原文](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/vllm_mlu/__init__.py)；源码固定树SHA dc984838c63a | [原件](REFERENCES.md#ref-b5edd83e14f254c1) | complete_static |
| Cambricon_vllm-mlu_requirements_txt | [原文](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/requirements.txt)；源码固定树SHA dc984838c63a | [原件](REFERENCES.md#ref-edb9923345adc4fe) | complete_static |
| Cambricon_cambricon-k8s-device-plugin_device-plugin_README_md | [原文](https://raw.githubusercontent.com/Cambricon/cambricon-k8s-device-plugin/cccdd66de08ad6b8ade94d140a8cc7d63b87353f/device-plugin/README.md)；源码固定树SHA cccdd66de08a | [原件](REFERENCES.md#ref-7e1078bb8d3d1dc5) | complete_static |
| Cambricon_mlu-exporter_README_md | [原文](https://raw.githubusercontent.com/Cambricon/mlu-exporter/648a19c7d781ada2ea693e46edc562aa57f79be4/README.md)；源码固定树SHA 648a19c7d781 | [原件](REFERENCES.md#ref-c1f83e16add77787) | complete_static |
| Cambricon_vllm-mlu_vllm_mlu_platforms_mlu_py | [原文](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/vllm_mlu/platforms/mlu.py)；源码固定树SHA dc984838c63a | [原件](REFERENCES.md#ref-e9d67bf7129619e6) | complete_static |
| Cambricon_vllm-mlu_vllm_mlu_v1_attention_backends_flash_attn_py | [原文](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/vllm_mlu/v1/attention/backends/flash_attn.py)；源码固定树SHA dc984838c63a | [原件](REFERENCES.md#ref-dd4a9316eaa604ce) | complete_static |
| Cambricon_mlu-exporter_examples_metrics_yaml | [原文](https://raw.githubusercontent.com/Cambricon/mlu-exporter/648a19c7d781ada2ea693e46edc562aa57f79be4/examples/metrics.yaml)；源码固定树SHA 648a19c7d781 | [原件](REFERENCES.md#ref-242b79cf3be7fda5) | complete_static |
| Cambricon_mlu-exporter_pkg_metrics_conf_go | [原文](https://raw.githubusercontent.com/Cambricon/mlu-exporter/648a19c7d781ada2ea693e46edc562aa57f79be4/pkg/metrics/conf.go)；源码固定树SHA 648a19c7d781 | [原件](REFERENCES.md#ref-66baaceccb687f89) | complete_static |
| Cambricon_vllm-mlu_LICENSE | [原文](https://raw.githubusercontent.com/Cambricon/vllm-mlu/dc984838c63aef3de46bbadedd82d9848a19c5d2/LICENSE)；源码固定树SHA dc984838c63a | [原件](REFERENCES.md#ref-067d8c234abda056) | complete_static |
| Cambricon_cambricon-k8s-device-plugin_LICENSE | [原文](https://raw.githubusercontent.com/Cambricon/cambricon-k8s-device-plugin/cccdd66de08ad6b8ade94d140a8cc7d63b87353f/LICENSE)；源码固定树SHA cccdd66de08a | [原件](REFERENCES.md#ref-b9b9f1bf135f0c4e) | complete_static |
| Cambricon_mlu-exporter_LICENSE | [原文](https://raw.githubusercontent.com/Cambricon/mlu-exporter/648a19c7d781ada2ea693e46edc562aa57f79be4/LICENSE)；源码固定树SHA 648a19c7d781 | [原件](REFERENCES.md#ref-523f12100a59e55b) | complete_static |
