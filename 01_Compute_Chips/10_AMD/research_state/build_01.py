"""Render only AMD chapter 01 and its evidence/catalogue. No network or registry writes."""
import json, pathlib, re

P = pathlib.Path(__file__).resolve().parents[1]
A = P / 'reference_metrial'
R = json.loads((A / '_registry/materials.json').read_text(encoding='utf-8'))
F = {x['slug']: x for x in json.loads((P / 'research_state/figure_manifest.json').read_text(encoding='utf-8'))}
B = (P / 'research_state/01_body.txt').read_text(encoding='utf-8')

labels = {
    'AMD_Robotics': 'AMD机器人方案',
    'AMD_Kria_AI': 'Kria AI方案与脚注',
    'AMD_Versal_AI_Edge_Gen2': 'Versal AI Edge Gen2规格',
    'AMD_Radeon_AI_PRO': 'Radeon AI PRO产品与使用边界',
    'AMD_X100': 'X100系列规格',
    'AMD_X199': 'X199精确SKU规格',
    'AMD_X100_Brief': 'X100产品brief',
    'AMD_P100': 'P100系列规格',
    'AMD_P100_Brief': 'P100产品brief',
    'AMD_P100_Blog': 'P100扩展与供货计划公告',
    'AMD_Kria_AI_Dev': 'Kria AI开发平台规格',
    'AMD_Kria_Selection_PDF': 'Kria选型表XMP499 v1.1',
    'AMD_K26_Brief': 'K26产品brief',
    'AMD_K24_Brief': 'K24产品brief',
    'AMD_K26C': 'K26 Commercial商品/规格',
    'AMD_K26I': 'K26 Industrial商品/规格',
    'AMD_K24C': 'K24 Commercial商品/规格',
    'AMD_K24I': 'K24 Industrial商品/规格',
    'AMD_KV260': 'KV260商品/规格',
    'AMD_KR260': 'KR260商品/规格',
    'AMD_KD240': 'KD240商品/规格',
    'AMD_KV260_Brief': 'KV260产品brief',
    'AMD_KR260_Brief': 'KR260产品brief',
    'AMD_Versal_Gen2_Brief': 'Versal Gen2产品brief',
    'AMD_VEK385': 'VEK385评估套件规格',
    'AMD_VEK280': 'VEK280评估套件规格',
    'AMD_Versal_Gen1_Brief': 'Versal Gen1产品brief',
    'AMD_Embedded_8000_Brief': 'Embedded8000产品brief',
    'AMD_Ryzen_Embedded': 'Ryzen Embedded家族总览',
    'AMD_V3000_Brief': 'V3000产品brief',
    'AMD_V3000': 'V3000当前系列表',
    'AMD_V2000_Brief': 'V2000产品brief',
    'AMD_Ryzen_AI_Max_395': 'Ryzen AI Max+395精确产品页',
    'AMD_R9700_ROCm_Guide': 'R9700官方ROCm指南Rev2.0',
    'Sapphire_R9700': 'Sapphire R9700板卡规格',
    'AMD_MI350X': 'MI350X精确产品页',
    'AMD_MI355X': 'MI355X精确产品页',
    'AMD_MI350P': 'MI350P精确产品页',
    'AMD_Instinct_MI350': 'Instinct MI350系列状态',
    'OpenNav_Robotics_Benchmark': 'OpenNav机器人负载测试',
    'mimik_Agentic_Benchmark': 'mimik容量模型与方法',
}
versions = {
    'AMD_X100_Brief': '©2026；2页；未列正式revision/PID，带Confidential；元数据2026-07-20不作发布日期',
    'AMD_P100_Brief': '©2026；PID4420321；3页；未列revision',
    'AMD_P100_Blog': '2026-03-09公告；供货句为当时计划',
    'AMD_Kria_Selection_PDF': 'XMP499 v1.1；©2023–2025；6页；原件未列明确发布日期',
    'AMD_K26_Brief': '©2023；PID2045205-B；2页',
    'AMD_K24_Brief': '©2023；PID2269838；2页；测试2023-08',
    'AMD_KV260_Brief': '©2025；2页；未列正式revision',
    'AMD_KR260_Brief': '©2023；PID2045205-A；2页',
    'AMD_Versal_Gen2_Brief': '©2024；PID3070664；3页；部分预测2024-03',
    'AMD_Versal_Gen1_Brief': '©2024；PID2790031；2页',
    'AMD_Embedded_8000_Brief': '©2024；PID242578894-A；4页',
    'AMD_V3000_Brief': '©2023；PID221639364-B；3页',
    'AMD_V2000_Brief': '©2023；PID20650345-B；4页',
    'AMD_R9700_ROCm_Guide': 'Rev2.0；©2026；18页；ROCm7.1.1、PyTorch2.11 nightly；历史MSRP截至2025-10-01',
    'AMD_MI350X': '页面Launch2025-06-12；当前规格快照',
    'AMD_MI355X': '页面Launch2025-06-12；当前规格快照',
    'AMD_MI350P': '当前规格/预览；未取得确定交期',
    'OpenNav_Robotics_Benchmark': '2026-07-23，Steven Macenski；AMD合作/资助，第三方独立执行',
    'mimik_Agentic_Benchmark': '合作公告2026-07；当前方法页；设计级模型与trace，非全容量实測',
    'Sapphire_R9700': '当前板卡SKU32358-01；未标更新日',
}
ids = list(dict.fromkeys(re.findall(r'@@(?!FIG:)([A-Za-z0-9_]+)@@', B)))
assert set(ids) <= labels.keys(), set(ids) - labels.keys()
numbers = {sid: f'S{i:02}' for i, sid in enumerate(ids, 1)}
for sid in ids:
    r = R[sid]
    assert r['archive_status'] in ('complete_static','partial_static') and r['status'] == 200, sid
    assert pathlib.Path(r['file']).is_file(), sid
    B = B.replace(f'@@{sid}@@', f"[{numbers[sid]} {labels[sid]}]({r['url']})")
fig_ids = list(dict.fromkeys(re.findall(r'@@FIG:([A-Za-z0-9_]+)@@', B)))
for fid in fig_ids:
    assert F[fid]['source_id'] in ids
    B = B.replace(f'@@FIG:{fid}@@', F[fid]['file'])
assert '@@' not in B

catalogue = []
appendix = ['\n## 参考资料与本地原件\n',
    '全部材料采集于2026-11-04；未标明确发布日期/修订的网页仅代表该日快照。下表给原站URL与本地HTML/PDF，完整响应、HTTP、哈希与缺失依赖见各材料metadata及唯一registry。正文S编号与本表一致。\n',
    '| 编号 / 原文URL | 日期、版本与资料性质 | 本地原件 | 归档状态 |',
    '|---|---|---|---|']
for sid in ids:
    r = R[sid]
    v = versions.get(sid, '网页未标明确发布日期/revision；本次快照')
    title = labels[sid]
    catalogue.append(dict(source_id=sid, number=numbers[sid],title=title,version=v,url=r['url'],
                          file=pathlib.Path(r['file']).as_posix(),sha256=r['sha256'],
                          archive_status=r['archive_status'],collected_at=r.get('retrieved_at_utc',r.get('archived_at_utc'))))
    appendix.append(f"| [{numbers[sid]} {title}]({r['url']}) | {v} | [HTML/PDF原件]({pathlib.Path(r['file']).as_posix()}) | {r['archive_status']} |")
appendix += ['\n归档缺失详情与去重证明见本章QA文件；失败候选留作研究日志，不作为有效参考来源。']
B += '\n'.join(appendix) + '\n'
(P / '01_Hardware_Platform.md').write_text(B, encoding='utf-8')
(P / 'research_state/source_catalog_01.json').write_text(json.dumps(catalogue,ensure_ascii=False,indent=2),encoding='utf-8')
manifest = [dict(name=sid,url=R[sid]['url'],expected=('pdf' if pathlib.Path(R[sid]['file']).suffix=='.pdf' else 'html'),used_by=['01_Hardware_Platform']) for sid in ids]
root = P.parents[1]
(root / 'toolkit/manifests/AMD_01_Hardware_Platform.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

claims = []
def claim(sid, subject, location, kind, conditions, finding, quote, supporting=None):
    claims.append(dict(claim=subject, source_id=sid, location=location, evidence_type=kind,conditions=conditions,
                       finding=finding,exact_quote=quote,source_url=R[sid]['url'],material_version=versions.get(sid,'2026-11-04网页快照，未标revision'),
                       collected_at=R[sid].get('retrieved_at_utc',R[sid].get('archived_at_utc')), supporting_source_ids=supporting or []))

claim('AMD_X100_Brief','X100六款核心/GPU/NPU/外存/功率/工业结温','第2页产品表','事实',
      'X168/X188/X199及i款；最高频率；NPU精度与稀疏条件未完整',
      '逐行检查8/12/16核、32/32/40CU、50TOPS、55W和45–120W，普通0–105/i−40–105；不推全功率同时峰值',
      'Nominal TDP 55 W; TDP Range 45-120 W; LPDDR5x (ECC) 256-Bit 8533 MT/s', ['AMD_X100','AMD_X199'])
claim('AMD_X100_Brief','公开brief修订异常','第1/2页可视标记与PID、PDFmetadata','未知',
      '官网公开URL；元数据创建2026-07-20；未标正式修订',
      '全页图已打开，确有Confidential和空PID，X188i L3=32MB不能自行纠正；不当正式量产保证',
      'AMD Confidential; PID#')
claim('AMD_X199','X199原生网络、Link-ECC与日历LTB','Foundation/System Memory/Interfaces','事实',
      '精确X199 SKU，不推广到其他系列',
      'FP11 BGA，Ethernet=N/A，8channel Link-ECC，LTB2037；Kria载板网络不是原生MAC',
      'Last Time Buy 2037; Memory Controller 8 Channel w/ Link-ECC; Ethernet N/A')
claim('AMD_X199','显示与USB不同资料冲突','Graphics Specifications/Interfaces','未知',
      'X199当前页vs官网X100 brief',
      '当前页单8K60/DP2.0/4K60codec/USB3.2×2；brief更高显示值/不同接口；保留差异待正式手册',
      'Max Resolution (for single display) 7680x4320 @ 60Hz; HW Video Encode / Decode up to 4K @60Hz',['AMD_X100_Brief'])
claim('AMD_X100_Brief','273GB/s与200B容量的推导边界','第1页Highlights','分析',
      '8533MT/s，256bit；200B参数；只算权重，十进制单位',
      '273.1GB/s为理论；FP16/8bit/4bit权重400/200/100GB，尚未含cache/workspace；不证明任意200B可运行',
      'Unified Memory Architecture with up to 273 GB/s; Run models up to 200B+ parameters with up to 128 GB external memory')
claim('AMD_P100_Brief','P100十二款与总TOPS/NPU区分','第1–3页/第3页表（视觉读表）','事实',
      '5普通+5i+2a；4/6/8/10/12核；WGP与CU对应；TOPS条件未齐',
      '30TOPS仅P121/P121i/P122a，其余50；80是总系统；car max频率图表3.65GHz，HTML3.7保留',
      'up to 80 total system TOPS; XDNA 2 NPU delivering up to 50 TOPS',['AMD_P100'])
claim('AMD_P100_Brief','P100工业网络和内存按SKU差异','第3页产品表','事实',
      'P121/P132及i/a有2Ethernet cores；高核数款N/A；LPDDR速率7500/8000/8533不同',
      '不推广双10GbE/TSN全系列；高核数i款8000而普通8533；a款DDR5/USB4 N/A；Link-ECC不替代全系统ECC',
      '10Gb/E Ethernet Cores w/TSN; DDR5 (ECC); LPDDR5X (Link ECC)')
claim('AMD_P100_Blog','P100量产是历史计划，不自动更新为实际','Availability段，2026-03-09','厂商宣称',
      '8–12核预计July2026；4–6核预计Q2；当前采集2026-11-04',
      '既有partner production笼统表述不证明十二款逐SKU交付；未取得当前订单',
      'currently sampling, with production shipments expected to begin in July 2026')
claim('AMD_P100_Brief','24/7寿命、保修、供货期分别处理','第2/3页reliability','厂商宣称',
      'Standard2.5years/Extended最高10years；i/a温度；需BIOS模式',
      'extended运行模式不等于无条件保修或软件支持期；功率/性能约束需正式资料',
      '2.5 Years (Standard) | Up to 10 Years (Extended Mode*)',['AMD_X100_Brief'])
claim('AMD_Kria_AI','新版Kria架构与旧Kria不混用','Kria AI SOMs','事实',
      'X100 COM-HPC SOM，伙伴销售；非K26 Arm+PL',
      '同品牌不证明连接器、镜像、BSP或bitstream兼容；图只支持产品布局',
      'X100 series device on an industry-standard COM-HPC form-factor board')
claim('AMD_Kria_AI_Dev','Kria AI载板接口与状态','General Specifications/Product Features/Notify Me','事实',
      'X199，64/128GB；Spartan UltraScale+载板；FAKRA与RJ45非裸X199接口',
      '逐项核对8FAKRA、4RJ45、QSFP原文10GbE(x4)、CAN/RS485/USB/M.2；未取得价格P/N/确定交期/FPGA SKU/热/尺寸',
      'SOM based on Ryzen AI Embedded X199 processor ... carrier card with Spartan UltraScale+ FPGA; Notify Me')
claim('AMD_Kria_Selection_PDF','K24/K26内存与PL资源','第3页SOM table','事实',
      '生产C/I，不套开发套件；Mb非MB',
      'K26:4GB+16GB eMMC/256K/1248DSP/26.6Mb；K24:2GB+32GB/154K/360DSP/9.4Mb；ECC仅K24I',
      '4 GB 64-bit DDR4 (non-ECC) and 16 GB eMMC; 2 GB 32-bit LPDDR4 ... and 32 GB eMMC',['AMD_K24_Brief'])
claim('AMD_Kria_Selection_PDF','DPU峰值不等于新NPU','第3页DPU行','事实',
      'K26 B4096 300MHz最高1.4TOPS；K24 B2304 INT8 852GOPS；稀疏定义未齐',
      '0.852TOPS单位换算；DPU为PL设计；Mali400为图形；不证明VLA可映射',
      'INT8 (852 GOPs with B2304 DPU); Up to 1.4 TOPs with B4096 at 300 MHz')
claim('AMD_Kria_Selection_PDF','K26 VCU与GTH/PCIe条件','第3页VCU与transceivers及脚注4/5','事实',
      'VCU总4K60；C/I不同GTH；可用收发器限制PCIe IP配置',
      '最多32streams不能乘32个4K60；I10.3125Gb/s；不根据IP块Gen3x16标题称实物x16',
      'total resolution ≤ 4Kp60; For the I-grade SOM, the data rate is 10.3125 Gb/s')
claim('AMD_K26C','K26频率资料冲突','General Specifications vs PSG第3页','未知',
      '网页A53 1.5GHz/R5 600MHz/Mali667 vs PSG1.33/553/600',
      '两版保留，未取得可归档完整DS987，待速度等级与目标配置消歧',
      'Quad-core ... up to 1.5 GHz; ... up to 600 MHz; ... up to 667 MHz',['AMD_Kria_Selection_PDF'])
claim('AMD_K24C','K24功率资料冲突','General Specifications vs PSG第3页','未知',
      '网页典型5W/最大10W估算；PSG2.5/7.5W理论估算',
      '不取较低值作任何bitstream满载保证；1066Mb/s单位未强算带宽',
      'Typical Power 5W; Maximum Power 10W',['AMD_Kria_Selection_PDF'])
claim('AMD_K24_Brief','SOM寿命/温度与开发板差异','第1页C/I表，第2页脚注','事实',
      'C2年保修/5年寿命，I3/10，availability10；仅I ECC；不当空气温度',
      'SOM器件温度范围不推广到0–35°C开发载板；没有统一日历EOL',
      'ECC Memory Support No Yes; Warranty 2 Years 3 Years; Product Availability 10 Years 10 Years',['AMD_K26_Brief','AMD_KD240'])
claim('AMD_Kria_Selection_PDF','开发套件缺eMMC且未生产资格','第4页表与脚注1','事实',
      'KV260/KR260 K26 non-production；KD240 K24 non-production',
      '生产16/32GB eMMC不可套开发板；接口逐表核对；工业寿命不能套套件',
      'Defeatured version of the production SOM, lacks eMMC boot options and is not fully qualified for reliability in harsh environments')
claim('AMD_K24_Brief','K24单轴延迟与idle功率宣称','第2页脚注SOM003/004','厂商宣称',
      '2023-08内部分析；TI TMDS64EVM公开FOC结果 vs KD240 Qdesys实现；2.5W启动bitstream idle',
      '不同实现不是通用伺服2倍；idle比较不是同模型能效；完整回路统计未取得',
      'using the latency results reported by TI ... vs ... algorithm designed by Qdesys; default/idle power ... (2.5W)')
claim('AMD_Versal_AI_Edge_Gen2','Gen2六款资源与精度区分','Product Specifications三种精度及六SKU表','事实',
      '24/96/144tiles；INT8dense31/123/184；sparse61/246/369；MX6dense另列',
      '04=4A78/4R52，无硬ISP/VCU；58=8/10，按SKU1或3ISP；不套最大图全部SKU',
      'INT8 TOPS (Dense); INT8 TOPS (Max Sparsity); MX6 TOPS (Dense)')
claim('AMD_Versal_Gen2_Brief','Gen2数据路径、硬ISP、NoC、安全边界','第1/2页特性','事实',
      'PL预处理/AIE推理/PS后处理；外存与NoC；按SKU硬ISP/VCU',
      '每ISP>1Gpix/s最多5streams不等于15插座；MAC模式不叠加；安全设计≠整机认证',
      'Preprocessing, AI inference, and postprocessing; Assured quality of service (QoS) to prioritize critical traffic')
claim('AMD_Versal_Gen2_Brief','3xTOPS/W与10xscalar为预硅/跨精度估算','第3页VER023/027','厂商宣称',
      'March2024；MX6 vs INT8；1GHz/.7V/100C/typical/60%vector；CPU特定高速度等级',
      '不是同精度同任务实测，不称整机能效/续航或Nav2加速',
      'using the MX6 data type, compared to ... using the INT8 data type; Performance projections as of March 2024')
claim('AMD_VEK385','VEK385准确器件/PCIe/外存/环境与电源','Featured AMD Devices/Board Features/PCIe脚注','事实',
      'XC2VE3858-2MSESSVA2112；20GB160bit；physical x8，Gen5x4/Gen4x8；0–45°Cenvironment',
      'LPDDR5X vs LPDDR5细表命名异常保留；180W电源额定非板耗；评估用途不当量产板',
      'physical x8 edge connector ... Gen5 x4 or Gen4/3 x8; 180W (12V) Power Supply')
claim('AMD_VEK280','Gen1不能套Gen2；SKU/IP模板异常','Featured/Board/What is Inside vs Gen1 brief第2页','未知',
      'A72/R5/AIE-ML，12GB LPDDR4；网页totalINT8 228 vs briefdense202；-2MSE/-2LSE',
      '不同峰值口径不自行统一；工具名称和器件尾缀需实际板号确认',
      'Total AI Compute (INT8) 228 TOPS',['AMD_Versal_Gen1_Brief'])
claim('AMD_Embedded_8000_Brief','8000四款Embedded OPN、GPU、PCIe、制程','第2页框图、第3/4页规格','事实',
      'Zen4/4nm/XDNA1/RDNA3，6/4WGP；NPU16 vs system39；4款OPN',
      'PCIeGen4×20，非家族总览Gen5；DDR5600 128bit理论89.6GB/s不当实测',
      'NPU 16 TOPS; PCIe x20 PCIe Gen4; Process Technology TSMC 4nm',['AMD_Ryzen_Embedded'])
claim('AMD_V3000_Brief','V3000没有集成GPU/NPU','框图/特性/六SKU表','事实',
      'Zen3/6nm，DDR54800 ECC双64bit；Gen4×20，2×10GbEMAC，V3C18I工业',
      '与家族总览图形冲突采用专门brief；MAC需PHY；PDF有V3C18而HTML缺，供货另验',
      '2x 10 Gb Ethernet MAC capable of 1, 2.5 or 10Gbps speeds',['AMD_V3000','AMD_Ryzen_Embedded'])
claim('AMD_V2000_Brief','V2000全部普通与车规差异','第3/4页表及脚注','事实',
      'Zen2/7nm/Vega，普通DDR43200ECC最高64GB，V2A46 LPDDR4X4267最高32GB无ECC；0或−40–105',
      'boost@80°C非全核持续；车规MAC不推广普通款；10year planned不当已EOL',
      '1Gb Integrated Ethernet (Automotive only); 1T Boost Freq. GHz @80C (up to)')
claim('AMD_Ryzen_AI_Max_395','Max+395代理与X199独立规格','Product specs/Memory/AI Engine','事实',
      '16Zen5/40CU；128GB256bit8000；CPU/IOD4nm/3die/Tjmax100；45–120W',
      '不套X1998533与i款工业结温；60FP16/50NPUTOPS条件未完整，不任意排名',
      'Max Memory Speed LPDDR5x-8000; Max. Operating Temperature (Tjmax) 100°C; Package Die Count 3')
claim('Sapphire_R9700','R9700精确板卡而非S款','Specification SKU32358-01','事实',
      'RDNA4/64CU/32GB256bitGDDR6/640GB/s，266.7×111×39mm，300W，blower/12V-2x6',
      '未将同站被动R9700S混用；95.7FP16/1531INT4的sparse条件未齐不比较',
      'SKU#: 32358-01; Cooler Type Active blower fan; Power Consumption 300 W',['AMD_R9700_ROCm_Guide'])
claim('AMD_R9700_ROCm_Guide','多卡显存和P2P依赖，历史价格和5倍测试条件','第12–14/18页及脚注RPW495/499/506','厂商宣称',
      'Rev2.0，ROCm7.1.1/nightly；2025-05测试不同backend/三次平均剔除edge；MSRP2025-10-01',
      '不认为多卡连续显存/线性加速；1299非2026当前成交价；未安装指南；不是机器人收益',
      'Re-Size BAR ... If it is disabled, P2P will be deactivated; As of October 1, 2025 ... MSRP of $1299 USD')
claim('AMD_Radeon_AI_PRO','R9700为工作站卡，数据中心使用边界','当前GD239d脚注','事实',
      'R9000系列除R9600/R9000S例外；具体R9700',
      'partner server目录不推已验证datacenter用途；采用当前脚注而非较旧指南笼统表述',
      'These products are not designed nor validated for datacenter usage. GD-239d')
claim('AMD_MI350X','MI350X/X355X/P独立显存与峰值/板耗','三款精确产品页','事实',
      'CDNA4 3/6nm；FP16matrix dense/sparse，不混FP32；X/355X288GB8TB/s，P144GB4TB/s',
      '1000/1400W OAM vs P600max/450config；P双槽267被动，未取得量产交期',
      'Peak Half Precision Matrix (FP16) Performance 2.3 PFLOPs; with Structured Sparsity 4.6 PFLOPs', ['AMD_MI355X','AMD_MI350P','AMD_Instinct_MI350'])
claim('AMD_X100_Brief','X199 CPU/GPU对Intel为代理与推算','第2页REX007/003','厂商宣称',
      'May2026 Max+39545W/64GB8000 vs X7 358H实测30W推45W；CoreMark1.01/GFXBench5',
      '不是两量产芯片同功率实测或机器人延迟收益；保留投影定义',
      'comparing measured AMD performance at 45W sustained power to 45W Intel performance projected from 30W')
claim('AMD_X100_Brief','1.3倍VLA为五模型几何平均投影','第2页REX001','厂商宣称',
      'Max+395代理X19955W8533 vs Orin64GB60W；FP16；GR00TN1.5/SmolVLA/Pi0DROID/Pi0.5DROID/OpenVLA',
      '未取得shape/batch/warmup/逐模型P99，不当policy频率或物理任务成功率',
      'reflect the geometric mean of performance ... models using FP16 quantization')
claim('AMD_Kria_AI','8000decisions/s是CPU控制回路，VLA另项','Footnotes第二条','厂商宣称',
      'Bosch Rexroth controller on X100，125us；embedL Pi0.5另称<100ms',
      '未取得完整实现与分布，不称VLA8000Hz或端到端伺服/WCET',
      '8,000 Decisions per second (125us) ... Benchmark measures CPU real time control loop latency')
claim('OpenNav_Robotics_Benchmark','OpenNav实验性质、输入与仿真隔离','Benchmark Design/Methodology','事实',
      '2026-07-23，AMD合作/commissioned，独立执行；平台在环；18万sqft/2m/s/15分钟/Gemma4.031BQ4_K_M',
      '第三方受资助测试而非无关系实验；独立机器运行仿真，不当现场运营',
      'work was a collaboration with AMD ... executed independently without influence; A separate machine ... runs the simulation')
claim('OpenNav_Robotics_Benchmark','CPU利用、miss与VLM完成数边界','Platform Results Analysis','事实',
      'StrixHalo120W/Thor130W/Orin65W；18.1/49.8/93.6%；miss.45/1.6/5.8，34/47vs25/35',
      '均有miss，不当硬实时；rounded ratio3.56vs文3.4保留；queries不当任务成功；TDP非能量；rawPDF受限',
      'Control-loop scheduling misses average 5.8x per second ... 1.6x ... 0.45x')
claim('mimik_Agentic_Benchmark','234/104和fleet只是容量模型','Methodology & partnership/Capacity','厂商宣称',
      'AMD合作，设计级publishedspecs，X100用最近公开part补CPU；memory/fleet modeled illustrative',
      'trace证明工作流分工不等于234agents实机或机器人在岗证据',
      'Figures come from design-level modeling using published specifications; Memory and fleet figures are modeled and illustrative')
claim('AMD_K26C','当前商品USD价格/交期','九商品页Price/PartNumber/LeadTime','事实',
      '2026-11-04英文页；K26C/I325/45026周，K24C/I250/3506周，KV249/KR34926周，KD3996周，VEK3851599528周/28069958周',
      '逐页读表；数量/税/地区未明，不当中国含税或千片报价；LTB/寿命不当交期',
      'Price: $325.00 MSRP; Part Number: SM-K26-XCL2GC; Lead Time: 26 Weeks',
      ['AMD_K26I','AMD_K24C','AMD_K24I','AMD_KV260','AMD_KR260','AMD_KD240','AMD_VEK385','AMD_VEK280'])

trace = dict(source_ids=ids, figures=[{k:v for k,v in F[fid].items() if k!='slug'} for fid in fig_ids], claim_review=claims,
             manual_review=dict(
                 coverage='完成01：X100六款/P100十二款/K24K26生产C-I与3套件/新KriaAI/VersalGen2六款与Gen1评估板/8000四款V3000六款V2000五款/开发训练4类；详解内存、接口归属、热、生命周期、采购和benchmark。未开展02–09。完整DS与部分目标硬件交付/实测存在明确缺口。',
                 versions_and_measurements='逐型号对照归档正文、HTML内嵌data-json和PDF可视表格；保留X100公开brief标记异常、K26频率/K24功率/家族总览/VEK命名冲突；代理、投影、设计模型、平台在环、峰值与真实本体结果分开。P100汽车3.65为视觉读图，未依抽取错字。',
                 maturity_and_licenses='商品页、NotifyMe、sampling/历史production计划及MI350P预览分开；生产SOM不套开发套件资格；产品资料不给IP许可，VEK node/device锁及一年updates有限。代码/权重/数据/二进制/本体许可在后续授权章节核验，本章不做整栈许可或整机认证结论。',
                 figures_opened='本次实际打开7幅：X100第2页、P100第3页、PSG第3/4页、8000第2页、KriaAI SOM渲染、VersalGen2框图。全部文字/单位/脚注可读无空白截断；保留Confidential；PSG字体替代告警经视觉核验。宣传robotics图已打开但未用于正文；框图标为最大资源组合，SOM图不推端口/BOM。'))
(P/'research_state/evidence/01_Hardware_Platform.json').write_text(json.dumps(trace,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(report=str(P/'01_Hardware_Platform.md'),sources=len(ids),figures=len(fig_ids),claims=len(claims),body_han=len(re.findall('[\u4e00-\u9fff]',B.split('## 参考资料')[0]))),ensure_ascii=False))
