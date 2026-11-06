import pathlib,json,re,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parent.parent
p=root/'01_Compute_Chips/05_Rockchip';a=p/'reference_metrial'
r=json.loads((a/'_registry/materials.json').read_text(encoding='utf-8'))
used=[]
def cite(m):
 n=m.group(1);v=r[n]
 assert v.get('archive_status') in ['complete_static','partial_static'] and v.get('status')==200,n
 if n not in used:used.append(n)
 return f'[{n} 原文]({v["url"]}) · [本地原件]({pathlib.Path(v["file"]).as_posix()})'
body=r'''# 瑞芯微 Rockchip 具身智能硬件平台：芯片、核心板、加速卡与工程选型

研究启动日期：2026-11-04；完成日期：2026-11-05（Asia/Shanghai）；资料实际采集时刻逐项见文末与 metadata。版本：01 深度样章，等待用户审阅。仅本章完成补深，既有 02—09 尚未按本轮标准重新核验。本报告是公开文献研究，没有安装 BSP、运行模型或测量机器人。

## 1. 结论、范围与证据层次

**Rockchip 的相关硬件应按“通用主控 SoC、专用视觉 SoC、独立 AI 协处理器、低层控制处理器”分别选型，再选择确定型号的核心板和载板。** RK3588/S/S2 系列承载 Linux、视觉预处理、应用调度和接口；RK3576 是另一条八核、6 TOPS 主控路线；RV1126B 更偏相机和 AI-ISP；RK1820/RK1828 通过独立内存和 PCIe/USB 接入主处理器；RK3506 则属于资源较小的控制/交互处理器。不能把每个型号都视为同一种机器人“大脑”。这些定位由官方产品页支持，具体机器人分工是本文分析。{{C:Rockchip_Home}}；{{C:Rockchip_RK3506}}

本章覆盖 RK3588 及实际板卡采用的 RK3588S/S2/J、RK3576/J、RK1820/1828、RV1126B、必要的旧代 RK3568/J 与 RK3506。核心板选择 Radxa CM5，开发板选择 ROCK 5B/5B+、ROCK 4D、ROCK 5T/Industrial、Firefly ROC-RK3588S-PC；AI 加速平台用 Firefly RK182X Development Kit 的两种硬件形态深入。芯片是瑞芯微产品，Radxa/Firefly 的板卡、供电、温度和交期是相应板商责任，不能交叉归属。官方目录仍列 RK3399/Pro、RK1808 等旧产品，目录存在只能说明仍有产品条目，不能证明现货、量产规模或未来供货年限。{{C:Rockchip_Products}}

本轮重要更新来自 **2026-09-22 云栖大会官方报道**：RK3588＋RK1828 的 VLA 演示、双卡/四卡方案及多种边缘终端已被明确展示；同文对 RK1860 仅用“计划推出”，本章将其列为路线图，未列入现行可采购 SKU。报道中的“探索量产路径”也不代表已取得量产客户验收。{{C:Rockchip_Multicard_2026}}

证据分三层使用：芯片官网证明处理器和原生接口；板商规格书、原理图证明具体板级配置；官方/板商 benchmark 证明其所披露条件下的测试主张。**未知项分为官方所取资料未披露、本轮未取得、资料冲突三类。** 不把下载日期当发布日期，不把“支持某模型”当作该机器人实际采用，更不把算力峰值当作动作成功率。

## 2. 芯片计算资源比较

### 2.1 主控、视觉与控制 SoC

下表比较芯片层的计算资源。频率是网页或具体板卡文档给出的最高值，非所有引擎在任意温度和功率下的持续值。未获得可引用制造节点的型号保留缺口；不会从型号新旧或品牌所在地推断制程。

| 芯片/变体 | CPU | GPU/专用图形 | NPU 指标与条件 | 制程/版本边界 | 在本章的角色 | 官方或板商原件 |
|---|---|---|---|---|---|---|
| RK3588 | 4×Cortex-A76＋4×A55 | Mali-G610 MC4，另有2D加速 | 三核6 TOPS；官网列INT4/8/16、FP16/BF16/TF32，未完整限定峰值口径 | 官网8nm；频率以具体板卡配置为准 | 通用主控、多媒体和感知 | {{C:Rockchip_RK3588}} |
| RK3588S/S2 | 同族4×A76＋4×A55；CM5表列A76 2.2—2.4GHz、A55 1.8GHz | 板商列Mali-G610 MP4/MC4 | 板商列最高6 TOPS；精度、稀疏性和功率需绑定文档 | Firefly对S列8nm；CM5实际表及原理图为S2 | 紧凑SOM/单板；高速扩展须另核 | {{C:Radxa_CM5}}；{{C:Firefly_ROC_RK3588S_PDF}} |
| RK3588J | ROCK 5T Industrial列A76最高1.6GHz、A55最高1.29GHz | Mali-G610 MC4 | 板商系列表最高6 TOPS，未给工业版独立持续值 | 此处仅是ROCK 5T Industrial配置；不沿用普通板2.4GHz | 工业板候选 | {{C:Radxa_ROCK5T_Product}} |
| RK3576/J | 4×A72＋4×A53；RK3576官网最高2.2GHz | Mali-G52 MC3 | 官网6 TOPS*未解释星号；ROCK 4D明确6 TOPS@INT8，稀疏性未写 | 制程本轮所取官方页未披露；J配置另核 | 双网口/控制接口较丰富的主控 | {{C:Rockchip_RK3576}}；{{C:Radxa_ROCK4D}} |
| RV1126B | 4×A53＋MCU；频率未列 | 2D图形引擎，不能写成G610 3D GPU | 官网3 TOPS；精度/稀疏性/功率未限定 | FCCSP 14×14mm；制造节点未取得 | 视觉前端和多目采集候选 | {{C:Rockchip_RV1126B}} |
| RK3568 | 4×A55，最高2.0GHz | Mali-G52 2EE，专用2D | 官网1 TOPS；精度/稀疏性未完整披露 | 必要旧代基线；制造节点未取得 | 存量AMR/HMI/网关设计评估 | {{C:Rockchip_RK3568}} |
| RK3568J | 4×A55；所取官网未给频率 | Mali-G52 2EE | 官网写512 MAC，未给同条件TOPS | 不以普通RK3568的1 TOPS自动替换512 MAC | 工业旧代候选 | {{C:Rockchip_RK3568J}} |
| RK3506B/J/G1/G2 | 3×Cortex-A7 | 本次产品页未列GPU/NPU | 未披露学习模型推理算力 | B/J外接16bit DDR2/3/3L；G1/G2分别内置64MB DDR2/128MB DDR3L | 控制、HMI、语音、扫地机等低层计算 | {{C:Rockchip_RK3506}} |

**同为6 TOPS，RK3588和RK3576并不等价。** CPU核心架构、GPU规模、内存总线、PHY复用、软件可用算子与任务调度都有差别。RK3588的较强通用计算与PCIe3扩展有利于多任务主控；RK3576的CAN FD、DSMC及UFS接口有利于某些工业设计，但优势成立的前提是载板真的引出接口、BSP支持目标模式且并发测试通过。没有同一模型、精度、功率和输入下的实测，本章不作推理速度排名。{{C:Rockchip_RK3588}}；{{C:Rockchip_RK3576}}

RK3568/J官网都列内存ECC，但未取得目标核心板上ECC启用、内存容量影响、纠错日志和故障注入验证。ECC支持不等于任意DDR板都已实现可靠性保护，也不等于取得功能安全认证。RK3568J的512 MAC是资源规模描述；从MAC单元数换算TOPS还需要时钟、每周期操作、计数方式和有效利用率，不能直接写成普通RK3568的峰值。{{C:Rockchip_RK3568}}；{{C:Rockchip_RK3568J}}

### 2.2 RK182X：独立内存的AI协处理器

| 型号 | 处理器/精度 | 内置DRAM | AI峰值证据 | 与主机连接 | 模型容量主张及限制 | 来源 |
|---|---|---|---|---|---|---|
| RK1820 | 官方系列页：多核RISC-V；INT4/8/16、FP8/16、BF16 | 板商逐型号列2.5GB | Firefly 2026-08-17手册第23页：20 TOPS INT8；dense/sparse、频率和功率未注明 | 官方系列页列USB3.0、2×PCIe2 x1、RGMII | 板商称3B以内；模型精度、工作区、上下文仍影响容量 | {{C:Rockchip_RK182X}}；{{C:Firefly_RK182X_Kit_PDF}} |
| RK1828 | 同系列描述；不能由系列页推定每精度峰值相同 | 板商逐型号列5GB | 同手册20 TOPS INT8；不视为20 TOPS FP16 | 实际板卡由PCIe互联；主机有相应驱动才可用 | 板商称7B以内；文中真实测试条件另见第7节 | {{C:Firefly_RK182X_Kit_PDF}} |

瑞芯微官网证明“内置高带宽DRAM”及接口，Firefly资料进一步描述3D RAM stacking；这支持“把模型推理工作放在协处理器内存域”的设计理解。**本轮没有取得可直接引用的DRAM GB/s、存储阵列细节、封装剖面或片内计算数据流手册，不能把板商的processing-in-memory宣传语当作已证明的物理存内计算结构。** 同样不从“3D”推导为HBM，不套用GPU HBM/NVLink的一致性模型。{{C:Rockchip_RK182X}}；{{C:Firefly_RK182X_Kit_PDF}}

分析上，主控负责相机采集、预处理、任务和动作接口，协处理器负责已转换模型推理，可以降低大模型与主控其他任务对同一DRAM的竞争；但PCIe搬运、驱动排队、张量重排和返回结果会增加链路成本。5GB加主机16GB不是单一可分配21GB内存池，两张5GB卡也不是未经软件分区就透明的10GB池。多卡报道列流水线并行、混合量化；它能支持可分区模型，不自动保证单卡时延减半或每个VLA都可部署。{{C:Rockchip_Multicard_2026}}

## 3. 芯片接口、内存与传感器能力

### 3.1 原生资源与外部器件

| 芯片 | 内存/存储接口 | 图像输入与ISP | 高速扩展 | 控制/音频 | 不能直接推导的能力 | 来源 |
|---|---|---|---|---|---|---|
| RK3588 | 本轮官网未列完整DDR容量/速率；以板卡和芯片手册补核 | 双16M ISP、HDR/3DNR；多路MIPI/DVP；HDMI2 RX最高4K60 | PCIe3/2、SATA3、RGMII、Type-C/USB3.1/2 | 低速资源按目标模组引出核验 | 32MP宣传不等于单相机32MP任意帧率；HDMI RX不推广到S/S2 | {{C:Rockchip_RK3588}} |
| RK3576 | 32bit LPDDR4/4X/5；UFS2.0两lane、eMMC5.1、SPI NOR/NAND | 16M ISP；HDR最高120dB；CSI C/D-PHY与DVP | USB3 DRD；USB3/PCIe2.1/SATA3 Combo及PCIe/SATA Combo；2×RGMII | CAN FD、DSMC、UART/SPI/PWM/I2C；页面特性提I3C；SAI/PCM/SPDIF/ASRC | Combo不是每项同时占用完整PHY；RGMII需外部PHY成为RJ45 | {{C:Rockchip_RK3576}} |
| RV1126B | 32bit DDR3/3L/4、LP3/4/4X；eMMC4.51 | 12M@30 ISP、8M@30 AI-ISP；2路4lane或4路2lane CSI；DVP/热成像接口 | USB3 DRD、USB2 Host、2×SDIO3、RGMII | 2×CAN、DSMC；集成音频codec | 支持5相机输入不证明每路12MP30同时推理，也不证明硬同步 | {{C:Rockchip_RV1126B}} |
| RK3568/J | 多种DDR/LPDDR、ECC | 8M HDR ISP | PCIe3 1×x2或2×x1；PCIe2.1、SATA3、USB3、QSGMII | 以载板定义为准 | 不能由接口列表相加推出全通道并发或ECC认证 | {{C:Rockchip_RK3568}}；{{C:Rockchip_RK3568J}} |
| RK182X | 内置DRAM；eMMC4.51 | RGA、4K JPEG解码 | USB3、2×PCIe2 x1、RGMII | RISC-V内部任务域，用户控制程序开放性未取得 | JPEG/RGA不代表完整摄像头ISP或可直接控制关节 | {{C:Rockchip_RK182X}} |
| RK3506 | 16bit外接或G1/G2内置DRAM | 本轮页未列相机ISP | 2×USB2 OTG、2×RMII | 2×CAN、6×UART、3×SPI、3×I2C、12×PWM、DSMC/FLEXBUS | CAN控制器需收发器；PWM不等于隔离电机驱动或安全停机 | {{C:Rockchip_RK3506}} |

多路视觉的关键不是只数CSI路数。原始采集、ISP、RGA、CPU缓存、NPU输入输出与显示/编码都会消费内存带宽；载板的电源、排线、摄像头驱动、时间戳和buffer生命周期也参与限制。RV1126B把AI-ISP、动态拼接放在视觉SoC，适合作为传感器端候选，但本轮没有端到端延迟、多路同步误差和观测年龄统计，不能写成已经验证的多相机融合系统。传感器同步机制留待03深入，本章只界定硬件边界。{{C:Rockchip_RV1126B}}

### 3.2 官方图：S2与CM5系统分层

以下第一图由Radxa官方文档提供，图内准确名称为 **RK3588S2**。可看出CPU簇、NPU、多媒体、外部内存和Combo接口的分层；图中的Cortex-M0×3只能证明该图画出的内部模块，不能当作用户已获得三个可编程、安全认证的运动控制核。芯片图不是RK3588完整型号或载板规格表。

![Radxa官方文档提供的RK3588S2芯片框图](@FIG:RK3588S_Chip_Block_Radxa.png@)

第二图为CM5系统图，显示DDR、eMMC、接口连接器和4V供电路径。它把PCIe2单lane和GPIO等送到连接器，因此能辅助理解SOM与载板之间的责任边界；不是说明CM5 IO板上存在所有芯片能力。图框版本写V2.2、日期2024-03-25；当前原理图下载文件封面写V2.21，部分页标题仍V2.2，保留这个内部版本差异，不宣称已取得每次改版PCN。{{C:Radxa_CM5}}；{{C:Radxa_CM5_Schematic_v221}}；{{C:Radxa_CM5IO_Schematic_v220}}

![Radxa官方CM5系统框图](@FIG:CM5_System_Block_Radxa.png@)

## 4. 核心板、开发板与工业款

### 4.1 计算、内存和形态

| 产品/层级 | 精确SoC | RAM选项 | 存储配置 | 尺寸 | 工业/频率边界 | 原文与原件 |
|---|---|---|---|---|---|---|
| Radxa CM5，SOM | 参数表/原理图RK3588S2；页简介泛称RK3588S | 1/2/4/8/16GB LPDDR4X | 可选4/8/16/32GB eMMC，文档写最高512GB；不是全部现货SKU | 55×40mm | 本轮未取得工业温度保证及各内存SKU报价 | {{C:Radxa_CM5}} |
| ROCK 5B，SBC | RK3588 | 4/8/16GB、64bit LPDDR4X | eMMC连接器、microSD，NVMe另配 | 100×75mm | 普通开发板；A76最高2.4GHz，A55最高1.8GHz | {{C:Radxa_ROCK5B_Intro}} |
| ROCK 5B+，SBC | RK3588 | 4/8/12/16/32GB、64bit LPDDR5 | 板载eMMC 32/64/128/256GB选项、microSD；双NVMe另配 | 100×75mm | 与5B共享名称页面，内存/PCIe/相机配置不同 | {{C:Radxa_ROCK5B_Intro}} |
| ROCK 4D，SBC两款 | 商业RK3576；工业RK3576J | 2/4/8/16GB LPDDR5 | 16MB SPI NOR；eMMC/UFS模块接口、microSD | 此次文档未给可核尺寸，不套用别板 | 网页板级温度：商业0—60°C、工业-40—85°C；测量位置/满载条件未写 | {{C:Radxa_ROCK4D}} |
| ROCK 5T/Industrial，SBC | 普通RK3588；工业RK3588J | 普通4/8/12/16/24/32GB；工业4/8/16/24/32GB，64bit LPDDR5 | eMMC 0/32/64/128/256GB、microSD | 110×82mm | 工业CPU频率为1.6/1.29GHz；本轮资料未给可直接引用的温度值 | {{C:Radxa_ROCK5T_Product}}；{{C:Radxa_ROCK5T_Download}} |
| Firefly ROC-RK3588S-PC，SBC | RK3588S | PDF v1.2列4/8/16/32GB，64bit LPDDR4/4X/5；具体颗粒随订单确认 | eMMC 16/32/64/128GB；2242 SATA默认或NVMe兼容；TF卡 | 93×60.15×12.36mm；约50g | 文档工作-20—60°C；存储-20—70°C；非J工业认证 | {{C:Firefly_ROC_RK3588S_PDF}} |

容量选择必须落到BOM和销售料号。比如CM5简介与参数表名称不同，采用表格及实际电路页的S2作为本轮研究对象；ROCK 5B+可选32GB不意味着ROCK 5B也有相同配置；ROC板文档列三种DRAM类型不是保证某一订单同时具备三种内存。**本轮未取得这些SKU的可持续DDR速率和GB/s测量，因此不补写常见网上带宽值。** 即使同为64bit，颗粒速率、训练参数和共享总线竞争仍影响吞吐。

内存估算仅能用于筛选：分析假设7B参数全部以4bit保存，权重裸容量约为7×10^9×4/8＝3.5GB（十进制），还需量化元数据、KV cache、视觉编码器、激活和运行时工作区。这个下限能解释为什么5GB与2.5GB协处理器是不同容量档位，但不能证明任意7B VLM或VLA都能放进5GB。主控增加DRAM也不能自动补齐协处理器内存。{{C:Firefly_RK182X_Kit_PDF}}

### 4.2 已引出接口与供电

| 板/模组 | 摄像头/显示 | 网络 | PCIe/存储 | 控制与扩展 | 供电与条件 | 来源 |
|---|---|---|---|---|---|---|
| CM5＋CM5 IO | 2×CSI、2×DSI、1×HDMI为IO组合描述 | 1GbE；模组图含以太网路径 | IO列M.2 E-Key；模组提供PCIe2单lane | 40pin、风扇、USB3 Host、Type-C、2×USB2 | 模组VCC_SYSIN 3.6—5.2V，推荐4V 3A；不是整机12W实测 | {{C:Radxa_CM5}} |
| ROCK 5B | 单CSI连接口可配1×4lane/2×2lane；双HDMI、DP/DSI，Micro HDMI RX | 2.5GbE；PoE需HAT；无板载Wi-Fi | M-Key Gen3 x4；E-Key；M.2 SATA不支持 | 40pin；2×USB3、2×USB2 | Type-C PD/固定5—20V；文档要求电源功率>30W，推荐PD30W，两种表述保留 | {{C:Radxa_ROCK5B_Intro}}；{{C:Radxa_ROCK5B_Power}} |
| ROCK 5B+ | 两CSI口；标准HDMI RX | 2.5GbE；板载Realtek8852BE；PoE需HAT | 两M-Key各Gen3 x2；B-Key走USB供4G；无E-Key | 40pin、USB等依具体版图 | 比5B需要更多功率；要求>40W，推荐PD65W；非满载耗电 | {{C:Radxa_ROCK5B_Intro}}；{{C:Radxa_ROCK5B_Interface}}；{{C:Radxa_ROCK5B_Power}} |
| ROCK 4D | 1×4lane可拆2×2lane，另1×2lane；HDMI、DSI | 1GbE；Wi-Fi6/BT5.4；PoE需HAT | FPC PCIe2.1 x1；UFS/eMMC接口 | 40pin可复用CAN/UART/SPI/I2C/PWM，风扇口 | Type-C或GPIO；本轮页未给持续功耗曲线 | {{C:Radxa_ROCK4D}} |
| ROCK 5T/Industrial | 两CSI口，HDMI RX，双HDMI/DP/DSI；PDM接口 | 1GbE；普通8852BE，工业Quectel FCE863R | 两M-Key各Gen3 x2；B-Key走USB供4G | 40pin；2×USB3、2×USB2、Type-C OTG/DP | DC9—20V；推荐36W适配器，不当实测耗电 | {{C:Radxa_ROCK5T_Product}}；{{C:Radxa_ROCK5T_Power}} |
| ROC-RK3588S-PC | 单CSI连接口1×4/2×2lane；HDMI、双DSI、DP | 1GbE；双频Wi-Fi/BT4.2 | 2242 SATA默认，PCIe2 NVMe兼容；无本轮证实Gen3 x4 | 20pin、UART/SPI/I2C等含1.8V信号，风扇/Debug | DC12V；支持9—24V；功耗见第6节 | {{C:Firefly_ROC_RK3588S_PDF}} |

以下为ROCK 4D v1.12接口实物图。编号需要与官方网页对应，⑤为FPC、⑧为40pin、⑲/㉗为CSI、㉔/㉖为UFS/eMMC。图本身没有给出所有低速接口的电压、总线速率或收发器，不能仅凭CAN复用功能宣称已具备隔离CAN端口。{{C:Radxa_ROCK4D}}

![Radxa官方ROCK4D v1.12接口图](@FIG:ROCK4D_v112_Interface_Radxa.png@)

机器人集成还需外部器件：RGMII/RMII需要PHY与磁性器件；CAN控制器需要收发器和终端；RS485需要相应收发器，若要求隔离还需隔离电源；MIPI与远距离GMSL/FPD-Link传感器间通常需要桥接器/解串器及驱动。以上为接口机制分析，不表示每块板都已配齐。ROCK 5B/5B+文档还明确40pin没有PMIC PWRON或wake信号，外部上电管理应按电源路径设计，不能假设GPIO可直接唤醒整板。{{C:Radxa_ROCK5B_Interface}}

## 5. Firefly RK182X双芯平台：两种载板不能混用

### 5.1 确定形态和配置

2026-08-17规格PDF共47页，封面明确 **Dual M.2 Module Version** 和 **Dual 260P Module Version**。前者用Core-3588JD4/Core-3576JD4主控与M.2加速卡；后者通过260P主/从核心板组合。当前商店默认选项为RK3588S (8G＋64G)＋RK1820，属于销售选项，不能把它与PDF第4页“双M.2、双RK1828”配置拼成一个订单。{{C:Firefly_RK182X_Kit}}；{{C:Firefly_RK182X_Kit_PDF}}

| 形态 | 主控SOM | 加速器及内存 | 板级I/O | 电源/尺寸 | 原文边界 |
|---|---|---|---|---|---|
| Dual M.2版本，PDF第4页 | Core-3588JD4：4—32GB LPDDR4/4X、32—256GB eMMC；Core-3576JD4：2—16GB、16—256GB eMMC | 2×M-Key 2260/2280加速卡；RK1828每卡5GB、20 TOPS INT8；也列其他品牌卡，本章不展开 | 双1GbE、USB、HDMI；1×RS485、1×CAN FD、2×光隔DI/DO；另有Wi-Fi/4G/5G扩展 | DC12V/7A，9—36V；148×106×36.4mm；净重437g含散热器 | Core-3576JD4主控时NVMe/SATA/Wi-Fi E-Key不可用；不由接口总表推出全部配置都可用 |
| Dual 260P版本，PDF第23页 | 可选Core-3588JD4、Core-3588SJD4 AI、Core-3576JD4；内存/存储逐主板表核对 | RK1820 2.5GB或RK1828 5GB；各20 TOPS INT8；3B/7B属板商模型容量主张 | 总计10个千兆口；8×RJ45 PSE需外部48V ATX、另1×RJ45及1组连接口；串口/RS485/IO等 | DC12V/5A、12—24V或12V ATX；232.97×162.8×34.86mm；净重467g含散热器 | 不是10GbE链路；PSE电源、网口分组和模块适配以第23、27页为准；不推广Dual M.2的CAN FD/功耗表 |

上表全部参数来自同一原件对应页。{{C:Firefly_RK182X_Kit_PDF}}

下图保留Dual M.2版本照片和官方特性说明，能确认卡、载板和主控共同组成平台；不能从照片推定量产料号或所有双卡软件都已验证。随后原始参数表给出不同主控与卡数的功耗，必须按对应行使用。

![Firefly官方Dual M.2版本概览，规格PDF第3页](@FIG:Firefly_RK182X_DualM2_Overview.png@)

![Firefly官方Dual M.2完整参数表，规格PDF第4页](@FIG:Firefly_RK182X_DualM2_Spec.png@)

### 5.2 多卡扩展的工程条件

官方2026年9月报道列Firefly AIBOX Pro RK3588＋RK1828×2、飞凌RK3588＋RK1828×4及万物纵横四路1U服务器，并写双卡约10GB、四卡约20GB内存规模。这是多卡安装容量的量级，不等于单进程透明共享内存；还应核查模型分片、每卡算子支持、传输分区、启动失败恢复和负载不均衡。1U/多卡系统服务固定边缘算力部署，可以通过网络辅助机器人；没有重量、功耗和抗振证据时不推荐直接装入小型移动本体。{{C:Rockchip_Multicard_2026}}

分析示例：PCIe2 x1的5GT/s按8b/10b编码，单方向编码后上限5×10^9×0.8/8＝500MB/s，尚未扣TLP、DMA、驱动和同步开销。若模型权重已常驻RK1828，主机无需每个token搬全部权重；若每步搬大量视觉特征或进行跨卡流水线，互联可能成为限制。这个上限不能作为实测DMA带宽，更不能把双口相加成每个任务天然1GB/s。接口规格根据官方系列页，公式是本文假设分析。{{C:Rockchip_RK182X}}

## 6. 功率、热设计、工业与安全边界

### 6.1 供电额定值与耗电分开

| 硬件/准确组合 | 厂商给出的功耗 | 电源额定/建议 | 温度和测量范围 | 缺失条件 | 原件 |
|---|---|---|---|---|---|
| ROC-RK3588S-PC，v1.2 | Min0.42W；Normal2.28W；Max12W，均按12V电流换算 | DC12V，支持9—24V | 板商工作-20—60°C、存储-20—70°C | 未给Normal/Max负载、采样时长、环境温度、CPU/GPU/NPU并发状态 | {{C:Firefly_ROC_RK3588S_PDF}} |
| Dual M.2：RK3588＋1×RK1828 | Normal9.6W、Max28.8W、Sleep0.72W | 同版12V/7A供电；加速卡另有12V插座 | 同版工作-20—60°C、存储-20—70°C | 整板配置主张；不能拆为单颗RK1828的TDP | {{C:Firefly_RK182X_Kit_PDF}} |
| Dual M.2：RK3588＋2×RK1828 | Normal15.6W、Max42W、Sleep0.72W | 同版供电 | 同版温度条目 | 未说明外设和模型负载；不能用差值13.2W作单卡通用功耗 | {{C:Firefly_RK182X_Kit_PDF}} |
| Dual M.2：RK3576＋1×RK1828 | Normal8.4W、Max28.8W、Sleep1.2W | 同版供电 | 同版温度条目 | 与RK3588组合不同，不能直接得出能效优势 | {{C:Firefly_RK182X_Kit_PDF}} |
| CM5模组 | 文档典型电流2A，未给基准负载；不写成确定TDP | 推荐4V/3A；供电范围3.6—5.2V | 本轮未取得模组工业温度/热阈值 | 4V×3A＝12W是推荐供电能力，不是持续消耗 | {{C:Radxa_CM5}} |
| ROCK 5B/5B+/5T | 本轮未取得各配置持续负载耗电曲线 | 5B推荐30W、5B+推荐65W；5T推荐36W电源 | 5T Industrial温度边界本轮未取得；4D工业页列-40—85°C | 电源容量不等于计算板耗电，不能据此估算续航 | {{C:Radxa_ROCK5B_Power}}；{{C:Radxa_ROCK5T_Power}}；{{C:Radxa_ROCK4D}} |

功耗表有实际电压、电流口径，优于只写“低功耗”，但仍不是完整benchmark。机器人热验证应同时运行目标相机数、ISP/RGA、NPU、CPU规划、日志写入和网络，记录电源输入、各热点、降频、丢帧及端到端P99。环境温度、芯片结温、散热片表面温度必须分别记录；本轮未取得瑞芯微完整结温/降频/关机阈值表，不能借用Jetson阈值。

热设计中，SOM的裸板/芯片、开发板风扇、双芯套件散热器和机器人封闭机箱是不同热路径。电池预算还应包括载板转换损耗、相机/解串器、SSD、无线和风扇，再与电机供电合并。没有全任务能耗曲线，本章不给续航小时数；没有同条件测量，也不把42W对比其他平台某功率模式生成“节能百分比”。

### 6.2 工业款、实时控制与功能安全

ROCK 4D官方文档明确商业/工业版温度，却未说明该温度表对应哪种满载、散热或测试标准；应作为板商产品范围主张，待取得试验报告。ROCK 5T Industrial产品页明确RK3588J及较低CPU频率，下载页存在v2.01工业原理图链接；但此次取得的该PDF内页仍写ROCK 5T、1.2、2025-06-25，不能仅凭下载文件名证明其全部电路对应工业v2.01。工业型号依据产品参数页，具体电路版本须向板商核对。本轮没取得温度、抗振、EMC全项、长期供货和芯片级功能安全证书。**不能用名字中的Industrial补齐-40—85°C，也不能用4D温度推广给5T。**{{C:Radxa_ROCK4D}}；{{C:Radxa_ROCK5T_Product}}；{{C:Radxa_ROCK5T_Industrial_Schematic_v201}}

CPU Linux主控、NPU模型推理、下位控制器、总线和电机伺服是不同频率域。RK3506双CAN/PWM和S2图中的M0核仅提供硬件线索，尚缺控制SDK开放性、中断延迟、WCET、故障域隔离和看门狗反应证据。建议将急停/制动等保护设计为有明确硬件路径的下层功能，但这是分析架构，不代表瑞芯微已经交付某SIL/PL等级的机器人安全系统。{{C:Rockchip_RK3506}}；{{C:Radxa_CM5}}

## 7. 官方性能证据：指标、条件与不能推导的结论

Firefly规格PDF第24页给RK182X LLM/VLM性能表。**条件明确到RKNN3 SDK、w4a16量化、LLM输入128；未明确SDK版本、batch、主机SKU、温度/频率/功率、生成长度、warmup、采样数、统计量、VLM图像尺寸与视觉编码是否计入。** “RK182X”标注的行不能任选归到RK1820或RK1828。表内TTFT/TPS与宣传页“超过100 tokens/s、0.1s”应分开。{{C:Firefly_RK182X_Kit_PDF}}

| 类型/测试平台原标注 | 模型 | TTFT ms | TPS tokens/s | 已披露条件 | 证据边界 |
|---|---|---|---|---|---|
| LLM / RK182X | Qwen2.5-0.5B | 23.50 | 180.77 | RKNN3、w4a16、输入128 | 未写具体1820/1828，不能代表7B |
| LLM / RK182X | Qwen2.5-3B | 84.30 | 87.65 | 同上 | 没有host和P99/WCET |
| LLM / RK1828 | Qwen2.5-7B | 161 | 59.09 | 同上 | 支持此模型测试主张；不代表全部7B模型 |
| LLM / RK1828 | Qwen3-4B | 111.44 | 64.96 | 同上 | 不是VLA策略频率 |
| VLM / RK1820 | Qwen2.5-VL-3B | 114.96 | 46.45 | RKNN3、w4a16、VL的LLM部分输入128 | 图像尺寸/视觉处理计时范围未给 |
| VLM / RK1828 | Qwen2.5-VL-3B | 87.08 | 85.98 | 同上 | 表内平台不同；缺同条件确认，不能计算芯片加速比 |
| VLM / RK1828 | Qwen2.5-VL-7B | 161.12 | 58.94 | 同上 | 不当机器人规划或任务完成率 |
| VLM / RK1828 | InternVL3.5-4B | 109.54 | 64.20 | 同上 | 不推导所有视觉输入都能同速运行 |

表格逐数字对照官方原页，不提高精度、不按柱形图补数。完整原页还含其他模型，以下保留其所有行和脚注。

![Firefly官方RK182X模型测试原表，PDF第24页](@FIG:Firefly_RK182X_Model_Benchmark.png@)

2026-09-22瑞芯微称优化后的π0.5在RK1828上超过5 FPS，演示用RK3588＋RK1828把视觉/语言与机械臂动作衔接；这证明存在厂商公开部署演示，适合列入后续02/04核验入口。尚未公开本轮可引用的模型commit、量化配置、相机和本体状态输入、动作chunk长度、推理计时起止、测试数量和任务成功率。**5 FPS不是5Hz伺服，也不说明每200ms必定输出安全动作。** 本章不将其宣传对比Thor的叙述转换为性能/成本排名。{{C:Rockchip_Multicard_2026}}

## 8. 版本冲突与采用依据

| 对象 | 冲突/缺口 | 本文采用依据 | 必须保留的限制 | 来源 |
|---|---|---|---|---|
| CM5 | 简介RK3588S；表、芯片图、电路页RK3588S2；封面V2.21而内页V2.2/2024-03-25 | 实际表和电路页按S2；尺寸/内存用当前产品文档 | 未取得逐改版PCN，不保证任意历史CM5料号相同 | {{C:Radxa_CM5}}；{{C:Radxa_CM5_Schematic_v221}} |
| ROCK 5B+ | v1.2框图旧标注，下载页明确提示；已取v1.21第3页仍画EKEY/LPDDR4，当前表为无E-Key、LPDDR5 | 当前接口文档、参数表及v1.21第14/22—24页具体电路交叉核验 | 原图保留，不把旧框图当新版全部接口证据；DDR颗粒/速率仍按BOM | {{C:Radxa_ROCK5B_Download}}；{{C:Radxa_ROCK5B_Interface}}；{{C:Radxa_ROCK5BPlus_Schematic_v121}} |
| ROCK 5B |下载文件封面V2.20，而部分页标题仍1.46 | 下载页对应V2.20文件；保留页内标题版本 | 不宣称封面变化代表所有电路变化 | {{C:Radxa_ROCK5B_Download}}；{{C:Radxa_ROCK5B_Schematic_v220}} |
| ROCK 5T Industrial资源 | 下载页/文件名标工业v2.01，所取PDF内页写ROCK 5T、1.2、2025-06-25 | 工业芯片与频率采用产品页；电路版本保持待核 | 不把资源命名视为准确工业原理图或认证证明 | {{C:Radxa_ROCK5T_Download}}；{{C:Radxa_ROCK5T_Industrial_Schematic_v201}} |
| ROC-RK3588S-PC | 当前宣传段含7屏、PCIe3、HDMI RX；PDF v1.2具体板表为4屏、2242 PCIe2/SATA及单CSI；PDF内48MP ISP与RK3588官网双16M亦不一致 | 精确板级参数优先PDF第4—6页；不跨S/普通3588推广ISP数值 | 板表HDMI4K120与第5页图4K60也不一致，需目标固件验证 | {{C:Firefly_ROC_RK3588S}}；{{C:Firefly_ROC_RK3588S_PDF}}；{{C:Rockchip_RK3588}} |
| RK182X开发套件 | 商店默认S＋1820、宣传双M.2、规格PDF双M.2与双260P混在系列内 | 所有接口/功耗严格指定PDF形态与主控组合；价格只指商店默认选项 | 无法用同一网址统一为一款硬件，更不套用双卡参数到默认订单 | {{C:Firefly_RK182X_Kit}}；{{C:Firefly_RK182X_Kit_PDF}} |

下面保留ROCK 5B+ v1.21第3页官方框图，供审查其数据/供电路径和版本冲突：**图中的EKEY、LPDDR4/4X文字是原件内容，不是本文确认的当前板级参数。** 同PDF第14页标题为LPDDR5，第22页为板载PCIe Wi-Fi，第23页为B-Key，第24页为双M-Key，当前文档也明确无E-Key。因此原图只用于整体路径和冲突复核，选型表采用当前接口文档与具体电路页，未修改原图来掩盖冲突。{{C:Radxa_ROCK5BPlus_Schematic_v121}}；{{C:Radxa_ROCK5B_Interface}}

![Radxa官方ROCK5B+ v1.21框图，含需保留解释的旧标注](@FIG:ROCK5BPlus_v121_Block.png@)

## 9. 价格、可采购状态与生命周期

### 9.1 可核验报价及供货层次

以下价格是本轮抓取Firefly国际商店的USD页面快照，单次页面默认选项、数量1的展示口径；未结算，地区/税费/运费/库存未确认，不是中国含税到货价或批量合同价。标题中的“可采购”区分为具有销售入口与已经取得正式报价/交期，后者本轮未开展。

| 对象 | 页面价格/币种 | 配置/数量口径 | 现状证据 | 生命周期/交期缺口 | 来源 |
|---|---|---|---|---|---|
| RK182X Development Kit | USD959 | 默认RK3588S (8GB＋64GB)＋RK1820；页面数量1 | 有Add to cart和配置菜单；未实际下单 | 不代表双M.2双卡SKU；库存、保修、税费及锁定交期未取得 | {{C:Firefly_RK182X_Kit}} |
| ROC-RK3588S-PC | 页面展示USD319；同时可见USD189比较价文字，变体绑定未充分核验 | RAM/eMMC目标变体未确定，故不作为确定SKU价格 | 有销售入口、PDF和下载页 | 不按319给32GB BOM报价，也不计算相对其他平台ROI | {{C:Firefly_ROC_RK3588S}} |
| CM5、ROCK 5B/5B+/4D/5T | 本轮所取文档没有可靠逐SKU报价 | RAM、eMMC、工业/商业版本不同 | 有正式文档、原理图与系统镜像入口 | 本轮未取得实时库存、最低采购数量、生命周期到期年及PCN/EOL承诺 | {{C:Radxa_CM5}}；{{C:Radxa_ROCK5B_Download}}；{{C:Radxa_ROCK5T_Download}} |
| Rockchip裸芯片系列 | 本轮未取得官方单颗/1KU批量价 | 精确SKU、封装、温度级、数量应在报价单确定 | 当前目录和产品页存在 | 产品目录不证明现货/软件维护期限；不能填入虚构“10年供货” | {{C:Rockchip_Products}} |

Firefly首页称支持无最低订单及“long-term supply, 10-year life cycle and certification support”，这是板商通用服务主张，并非本章每款SoC/SOM的逐料号供货到期承诺。ROC销售页所列备货3—7工作日、运输区域天数同样注明按实际订单，不能写成RK1828工业订单的固定交期。采购时需分别取得芯片、SOM、载板、DRAM/eMMC及无线模块的PCN/EOL和替代料规则，确认SDK维护与供货期限是两套契约。{{C:Firefly_Home}}；{{C:Firefly_ROC_RK3588S}}

硬件设计资料可公开访问不等于允许任意商用复制。Radxa页面声明文档CC BY4.0，本轮没有单独核清芯片IP、原理图/PCB设计、BSP源码、GPU/NPU二进制和模型权重的全部许可，因此不会把整个平台称为全部开源或由品牌所在地推出国产化率。02授权后应逐软件交付物核验许可证，01采购先确认设计复用权与板商支持范围。{{C:Radxa_CM5}}

### 9.2 条件选型与本章放行证据

| 任务约束 | 优先评估硬件路线（分析） | 为什么可能成立 | 不成立/仍未知的条件 | 放行前应取得的证据 |
|---|---|---|---|---|
| 多视觉＋Linux规划＋较多高速扩展 | RK3588/ROCK 5B+或精确RK3588 SOM | CPU/GPU、PCIe3、较大主控内存及多媒体资源 | 模型算子/内存瓶颈，PHY复用；板级并发未测 | 目标相机＋模型＋网络＋SSD并发的时延/丢帧/热稳定数据 |
| 控制/网络接口重要、模型可压缩 | RK3576/J与确定载板 | CAN FD/DSMC、UFS、双RGMII原生资源 | 实际板卡可能只引出1GbE或与PCIe/SATA复用 | 连接器/收发器/隔离、驱动版本、总线负载与故障恢复 |
| 2.5GB以内模型工作区或3B级入口 | 主控＋RK1820 | 独立2.5GB DRAM，可把部分AI任务移出主控 | 模型总占用可能超容量；w4a16算子/上下文不同 | 确切模型、产物、内存水位及PCIe全链路计时 |
| 7B量化LLM/VLM或VLA研究 | 主控＋RK1828；必要时多卡 | 5GB独立DRAM和公开模型/VLA部署主张 | 7B裸权重能放不代表完整VLM/VLA可放；演示未给任务成功率 | 编译产物、图像/动作输入、KV/工作区、TTFT与完整观测到动作P99 |
| 视觉前端需AI-ISP/拼接 | RV1126B＋专门相机板 | 12M ISP、AI-ISP、多目硬件线索 | 尚无目标传感器时间同步和完整链路统计 | Sensor+BSP配置、ISP参数、触发/时间戳和持续路数验证 |
| 工业环境长期运行 | RK3576J/ROCK 4D工业或RK3588J/5T工业 | 存在独立工业型号/板级描述 | 未取得5T温度/安全/长期供应承诺；工业频率更低 | 目标SKU宽温满载、EMC/振动、PCN/EOL、BSP维护和正式报价 |
| 低层控制与小内存交互 | RK3506或独立下位控制器与上层SoC组合 | CAN/PWM/UART等适合接口与控制任务 | 没有已证实硬实时/功能安全，不能替代安全控制器认证 | 控制SDK、WCET/看门狗/故障隔离与独立保护链验收 |

上述建议来自本章规格和机制推导，不是量产选型结论。现阶段最有价值的两条PoC是：一条在RK3588/RK3576主控上验证传统感知和接口并发；另一条用明确形态的RK1828组合验证量化大模型的容量、互联和长时间热状态。先锁定料号与任务契约，再比较同条件成本与时延。训练/仿真主机仍需独立选择，本章没有证据把Mali/NPU当作CUDA/RTX软件的可替代运行环境。

## 10. 证据缺口、归档质量与续接

本轮已扩展官网产品/新闻、板商产品参数、47页加速套件手册、17页ROC板手册、核心板和开发板原理图，逐图打开核查。还未取得完整瑞芯微芯片datasheet/TRM、电源热设计手册、各SKU的持续内存带宽、完整生命周期/PCN、全部安全证明以及量产报价；这属于本轮资料取得/披露边界，不能写成相关能力不存在。官网中文下载入口返回空正文，未作为有效来源；8月机器人新闻候选因异常资源URL未归档完成，未用其作事实依据；巡检页本轮抽取正文只有标题，未用来补造方案细节。

所有引用原件通过研究根toolkit统一下载，保留HTML、已取得CSS/图片/字体、PDF、原始响应、SHA256和metadata。部分网页依赖缺失主要是站点脚本/字体或第三方资源访问问题；缺失详情逐项写入登记，本文不承诺像素级、动态交互和视频完整。官方图由本地原件转码/渲染，未改写图中文字；来源、页码、操作和哈希见本章evidence。

检查器验证正文、表格、引用原件、HTML可见文本一致性、图源、链接及其他报告基线；通过只说明这些结构和归档检查通过，不证明语义绝对正确或实机性能。最终重复运行本章引用联合清单用于证明去重。完成状态为01样章已交付、等待审阅；02—09没有被本轮重生成或提前批准。

## 参考资料与本地原文

以下清单仅含实际用于本章的有效来源。网页未给版本/发布日期的标为未注明；URL路径日期仅作定位，不当首次上市日期。PDF封面或页内日期按原件注明，采集时间使用真实UTC记录。
'''
body=re.sub(r'\{\{C:([^}]+)\}\}',cite,body)
body=re.sub(r'@FIG:([^@]+)@',lambda m:(a/'derived/figures'/m[1]).as_posix(),body)
versions={'Firefly_RK182X_Kit_PDF':'封面2026-08-17，47页；两种形态', 'Firefly_ROC_RK3588S_PDF':'v1.2，2025-03-11，17页','Radxa_CM5_Schematic_v221':'封面V2.21，内页V2.2/2024-03-25','Radxa_CM5IO_Schematic_v220':'封面V2.2，内部页各日期保留','Radxa_ROCK5BPlus_Schematic_v121':'V1.21，2026-10-28','Radxa_ROCK5B_Schematic_v220':'封面V2.20，部分页1.46/2026-03-06','Radxa_ROCK5T_Industrial_Schematic_v201':'链接标工业V2.01；所取PDF内页1.2/2025-06-25，版本待核','Rockchip_Multicard_2026':'官方新闻2026-09-22'}
body+='\n| 登记名称 | 版本/发布日期 | 实际采集UTC | 原文/本地原件 | 静态依赖状态 |\n|---|---|---|---|---|\n'
for n in used:
 v=r[n];body+=f'| {n} | {versions.get(n,"网页未注明版本/发布日期；以此快照为限")} | {v["archived_at_utc"]} | [原文]({v["url"]}) · [原件]({pathlib.Path(v["file"]).as_posix()}) | {v["archive_status"]}；缺失{len(v.get("unavailable_assets",{}))}项 |\n'
body+=f'\n[资料总索引]({(a/"index.html").as_posix()}) · [本章证据及图源]({(p/"research_state/evidence/01_Hardware_Platform.json").as_posix()}) · [结构归档检查]({(a/"derived/qa/01_Hardware_Platform_quality.json").as_posix()}) · [去重记录]({(a/"derived/qa/01_Hardware_Platform_dedup_last_run.json").as_posix()}) · [续接状态]({(p/"research_state/progress.json").as_posix()})\n'
(p/'01_Hardware_Platform.md').write_text(body,encoding='utf-8')
fig=json.loads((a/'derived/figures/selected_trace.json').read_text(encoding='utf-8'))
checks=[
 ('RK3588三核6TOPS及8nm','Rockchip_RK3588','Key features / SPECIFICATION','厂商规格','RK3588；峰值精度、稀疏性和功率未完整限定','不推广至S/S2/J所有接口或模型实测'),
 ('RK3576内存32bit及Combo PHY','Rockchip_RK3576','详细参数：内存、Camera、接口','事实','RK3576当前网页；6TOPS星号缺说明','不能同时累加Combo全资源'),
 ('RK1820/1828 2.5/5GB及20TOPS INT8','Firefly_RK182X_Kit_PDF','第23页；第4页RK1828','厂商规格','2026-08-17；dense/sparse和功率未列','系列官网不逐型号映射；由板商逐型号规格补核'),
 ('RK182X高带宽DRAM及互联','Rockchip_RK182X','详细参数CPU/NPU/存储/接口','事实','系列页：USB3、2xPCIe2x1、RGMII','未取得GB/s与存内计算物理机制；不称HBM'),
 ('RV1126B AI-ISP及五相机','Rockchip_RV1126B','主要特性及详细参数','厂商规格','12M30 ISP、8M30 AI-ISP、3TOPS','不证明五路各12M30并发/同步/P99'),
 ('RK3568 ECC与RK3568J 512MAC','Rockchip_RK3568J','Key features / SPECIFICATIONS','事实','工业J产品页写512MAC；普通3568写1TOPS','不将普通峰值套J；ECC板级启用未核'),
 ('RK3506变体及双CAN','Rockchip_RK3506','Detail SPEC','事实','B/J外接DDR；G1 64MB/G2 128MB','无NPU或WCET/安全认证证据'),
 ('CM5准确SoC与版本冲突','Radxa_CM5_Schematic_v221','封面/第2—3页','事实','封面V2.21；内页V2.2、2024-03-25；RK3588S2','沿用S2规格，未虚构PCN'),
 ('CM5供电','Radxa_CM5','Power Supply','厂商规格','3.6—5.2V，推荐4V3A，典型2A未给负载','12W为供电能力，不为TDP'),
 ('ROCK5B与5B+内存和PCIe','Radxa_ROCK5B_Intro','Parameter Configuration','厂商规格','5B LPDDR4X/x4；Plus LPDDR5/双x2','容量不跨板SKU；eMMC配置独立'),
 ('ROCK5B+框图旧标注','Radxa_ROCK5BPlus_Schematic_v121','第3、14、22—24页','事实','V1.21 2026-10-28','原图保留EKEY/LPDDR4，当前接口和具体电路页优先'),
 ('40pin无PWRON/wake','Radxa_ROCK5B_Interface','No power-on / wake-up signal','事实','ROCK5B/5B+','上电管理不能假设GPIO唤醒'),
 ('ROCK4D工业温度','Radxa_ROCK4D','Specifications/Temperature','厂商规格','商业0—60、工业-40—85°C','缺满载/散热/测量位置；不推广5T'),
 ('ROCK5T Industrial频率','Radxa_ROCK5T_Product','Parameter Configuration','厂商规格','RK3588J；A76 1.6GHz/A55 1.29GHz','不套普通2.4/1.8GHz；温度本轮未取得'),
 ('ROCK5T Industrial资源内部版本冲突','Radxa_ROCK5T_Industrial_Schematic_v201','下载页资源名/所取PDF第1—2页','事实','链接工业v2.01；PDF内页ROCK5T 1.2/2025-06-25','资源名不证明实际工业电路；工业芯片/频率依产品页，电路版本待板商确认'),
 ('DualM2与Dual260P不同','Firefly_RK182X_Kit_PDF','第1/4/23/27页','事实','2026-08-17，两种载板','尺寸/网络/CAN/功耗分开；10个千兆口非10GbE'),
 ('双芯整板功耗','Firefly_RK182X_Kit_PDF','第4页Power consumption','厂商宣称','1卡28.8W、2卡42W、RK3576+1卡28.8W Max，12V输入','未给负载/温度/统计；不作为单芯TDP'),
 ('ROC板功耗与规格冲突','Firefly_ROC_RK3588S_PDF','第4—6页及网站宣传段','厂商规格','v1.2 2025-03-11；12W Max、4屏、PCIe2/SATA','网页7屏/Gen3/RX不作为板级能力；48MP不套普通RK3588'),
 ('RK1828 Qwen2.5-7B测试','Firefly_RK182X_Kit_PDF','第24页LLM/VLM性能表','厂商宣称','RKNN3、w4a16、LLM输入128；161ms/59.09TPS','SDK版本、host、batch、时钟/功率、统计及完整链路缺失'),
 ('π0.5超过5FPS','Rockchip_Multicard_2026','02 VLA端侧部署','厂商宣称','2026-09-22 RK3588+RK1828演示','无commit/量化/输入/chunk/任务成功率；非伺服频率'),
 ('RK1860计划','Rockchip_Multicard_2026','03多卡级联：面向后续演进','计划','2026-09-22使用计划推出','不列当前可采购SKU'),
 ('默认套件959USD','Firefly_RK182X_Kit','默认产品选项/价格','事实','RK3588S 8G64G+RK1820；数量1页面；未结算','非双M2双卡价格，税费/库存/地区未确定'),
 ('10年生命周期服务主张','Firefly_Home','Customization服务段','厂商宣称','板商通用服务说明','非Rockchip逐SKU供货承诺，未取得PCN/EOL合同'),
 ('内存容量与PCIe上限计算','Rockchip_RK182X','本文4.1、5.2','分析','7B*4bit/8=3.5GB裸权重；5GT/s*8/10/8=500MB/s','不代表完整模型可部署、实测带宽或透明多卡内存')
]
trace=dict(source_ids=used,figures=fig,claim_review=[dict(claim=x[0],source_id=x[1],location=x[2],evidence_type=x[3],conditions=x[4],finding=x[5]) for x in checks],manual_review=dict(coverage='01覆盖通用/视觉/控制SoC、协处理器、SOM、SBC、工业款、两种双芯载板、内存/接口/功率/热/安全/性能/价格/供应；完整芯片TRM与逐SKU生命周期未取得。',versions_and_measurements='逐数字核对产品页、PDF第4/23/24页和电路目录；保留RK3568J 512MAC、ROCK5B+旧框图、CM5/ROC/SKU冲突；厂商峰值与实机闭环指标分开。',maturity_and_licenses='只记产品文档、销售入口和公开演示；未做硬件/模型运行、下单或安全认证；文档CC BY4.0不推导完整平台许可，软件专题待02授权。',figures_opened='7图已逐张打开：S2芯片图、CM5系统图、4D v1.12接口、Firefly PDF第3/4/24页、5B+ v1.21第3页。文字/标题/单位完整；5B+旧标注明确保留和解释。4D透明背景合成白底后复核。'))
(p/'research_state/evidence/01_Hardware_Platform.json').write_text(json.dumps(trace,ensure_ascii=False,indent=2),encoding='utf-8')
manifest=[dict(name=n,url=r[n]['url'],expected='pdf' if r[n]['file'].endswith('.pdf') else 'html',used_by=['01_Hardware_Platform']) for n in used]
(root/'toolkit/manifests/Rockchip_01_Hardware_Platform.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
notes={n:dict(url=v['url'],archive_status=v.get('archive_status'),error=v.get('error'),unavailable_assets=v.get('unavailable_assets',{})) for n,v in r.items() if n not in used or v.get('archive_status')=='partial_static'}
(a/'derived/qa').mkdir(parents=True,exist_ok=True)
(a/'derived/qa/01_Hardware_Platform_research_log.json').write_text(json.dumps(dict(notes=notes,excluded_sources=['Rockchip_Download:空正文','Rockchip_Robotics_2026:异常资源URL导致失败','Rockchip_Inspection_2026:仅抽取到标题，未引用正文'],tool_tests='15 tests passed',limits='未绕过robots或正文访问限制；未取得完整芯片TRM、热阈值、逐SKU生命周期'),ensure_ascii=False,indent=2),encoding='utf-8')
print('Report written',len(re.findall('[\u4e00-\u9fff]',body)), 'Han characters;',len(used),'sources;',len(fig),'figures')
