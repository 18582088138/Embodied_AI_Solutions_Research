from topic_helpers import *
rows,a=rowset();stem='08A_GPU_Memory_and_Execution'
for n,c in [('eight vertically stacked','8XCD'),('TSMC’s N3P','计算工艺'),('TSMC’s N6','IOD工艺'),('32 are active','有效CU'),('288GB','HBM容量'),('1400W','MI355X功率'),('NPS2','内存分区')]:a('AMD08_MI350_Architecture',n,c,'architecture','事实','MI350X/MI355X',f='服务器机制不当端侧，峰值非持续实测')
for n,c,p in [('typically 32','MX分块','p7'),('E2M1','MXFP4元素','p7'),('160KB','LDS容量','p9'),('256 bytes per clock','LDS读带宽','p9'),('software emulation utilizing the BF16','TF32路线改变','p8'),('10 TFLOP/s','TF/PF冲突','p3'),('MI325X GPUs','表题列名冲突','p8'),('16834','原表数值保留','p8'),('DPX+NPS2','分区/精度跨条件比较','p21'),('PID#2258402-D','PDF版本','p21')]:a('AMD08_CDNA4_Whitepaper',n,c,p,'事实','2026-09-28',f='原件与图核对；不使用冲突表推出旧代精确倍数')
for n,c in [('512K','朴素矩阵loads'),('Ping Pong buffering','double buffer'),('MFMA','矩阵指令'),('M = 4864 and N = 4096','教程维数'),('M / 256 × N / 256','公式维度冲突')]:a('AMD08_CK_GEMM',n,c,'GEMM教程','事实','MI300示例',f='教程简化/冲突不当目标GPU性能配置')
for n,c in [('32 or 64 banks','bank依代际'),('ds_read_b128','读分组'),('additional LDS storage','padding代价'),('XOR preshuffling','不额外存储的重排'),('KPack = 8','例子参数')]:a('AMD08_CK_LDS',n,c,'LDS指南','事实','CK1.3.0',f='32bank/64lane示例不推广RDNA/CDNA4')
a('AMD08_HipBLASLt','General Matrix-Matrix','GEMM库定位')
a('AMD08_HipBLASLt_Tune','offline tuning','离线调优接口')
for n,c in [('HSA_XNACK=1','迁移条件'),('SR-IOV','MI200限制'),('first touch page-fault migration','首触迁移'),('zero copy','访问非本地带宽')]:a('AMD_HIP_Memory',n,c,'unified memory','事实','HIP7.16.0',f='allocator可用不等于高带宽或所有GPU支持')
for n,c in [('hipStreamWaitEvent','设备依赖'),('hipEventReleaseToSystem','system fence')]:a('AMD_HIP_Coherence',n,c,'visibility','事实','HIP7.16.0')
a('AMD_ROCm_Isolation','shouldn’t be used for isolating untrusted','环境变量非安全隔离')
a('AMD_HIP_Allocator','hipFreeAsync','内存生命周期')
a('AMD_HIP_Graphs','not captured by default','host非自动capture')
a('AMD_ROCm_GraphSafe','MIOpen ❌','library支持边界','表','事实','归档文档',f='不是所有图可capture；以具体package/release再验')
a('AMD_vLLM_Optimization','≥32 concurrent requests','attention布局并发条件','指南','事实','Instinct为主',f='不当单机器人batch1吞吐')
a('Compare_TRT_Quant','dequantizes them','INT4 WoQ不同机制')
a('AMD_HIP_Model','architecture dependent','warp依架构')
a('AMD_HIP_License','License','HIP许可入口')
prepare(stem,rows,dict(coverage='CDNA4 MX数值/metadata理想存储、LDS/MFMA与bank、HBM拓扑/分区、HMM/fence/graph/pool、vLLM期限与对标独立深入。',versions_and_measurements='新白皮书TF/PF、表题列名与每CU数冲突保留，MI350-052跨精度/分区不当应用加速；CK教程维度冲突不复用；无目标实测。',maturity_and_licenses='API/机制、理论峰值与机器人任务分开；逐组件许可，未运行GPU或训练模型；数据中心能力不推广端側。',figures_opened='实际打开白皮书p7/p8和MI350芯粒/partition两官方PNG；正文采用四图，表与legend瑕疵均记录。'),{
 'AMD08_CDNA4_Whitepaper':dict(title='CDNA4架构白皮书',version='PID2258402-D，2026-09-28'),
 'AMD08_MI350_Architecture':dict(title='MI350微架构',version='归档页面标ROCm10.1.0；原表口径见正文'),
 'AMD08_CK_GEMM':dict(title='CK Tile MI300 GEMM教程',version='CK1.3.0文档快照，MI300示例'),
 'AMD08_CK_LDS':dict(title='CK Tile LDS bank指南',version='CK1.3.0文档快照')})
pdf_fig('a_mx','AMD08_CDNA4_Whitepaper',7);pdf_fig('a_peak','AMD08_CDNA4_Whitepaper',8)
figure('08','a_chiplet','AMD08_MI350_Architecture','mi350_conceptual_diagram.png',True)
figure('08','a_partition','AMD08_MI350_Architecture','mi350_partition.png',True)
