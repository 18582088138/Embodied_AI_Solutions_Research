from rk_work import *
rows={
'07_Ecosystem':[
('RK07_Production','Preparation / Writing Configuration / Notes','writes SN, WIFI MAC, LAN MAC, BT MAC','VendorStorage；2026-07-08；Windows一次一设备','身份写入不等于密钥、标定、集中追溯'),
('RK07_Return','HOW TO INITIATE / WARRANTY','12-month warranty','不含accessories；30 natural days退换；特定商店条款','非ODM/工业现场SLA'),
('Firefly_Home','Customization','Long-term supply, 10-year life cycle and certification support','通用服务；没有逐料号PCN/EOL','不写所有芯片十年供货'),
('RK02_RK182X_Started','Download the SDK Package','Please contact sales@t-firefly.com','x86_64 Ubuntu20.04/22.04 cross-compilation','公开入口非已取得完整BSP'),
('Rockchip_Multicard_2026','03多卡','Firefly AIBOX Pro采用RK3588+RK1828*2','2026-09-22芯片厂商报道','产品组合不是4倍机器人性能')],
'08A_Quantization_Compiler':[
('RK02_00_RKNN3_SDK_Release_Notes_V1.2.0','p17量化定义','4-bit asymmetric quantization','W4A16 G32，input channel每32权重一组','不把KV/全部运算说成4bit'),
('RK02_02_RKNN3_SDK_Development_Guide_V1.2.0','p42—44 GRQ/calibration','minimizes the mean squared error between the outputs of each block','GRQ反向传播GPU/CUDA；multimodal hook args/kwargs','Normal无校准；GRQ不保证机器人任务无损'),
('RK02_02_RKNN3_SDK_Development_Guide_V1.2.0','p47 mixed precision','layer_quant_config and auto_hybrid_rate must not be used together','export_op_quantized_dtype同一ONNX映射JSON','不能复用修改后旧图映射'),
('RK02_02_RKNN3_SDK_Development_Guide_V1.2.0','p147—149 CPU plugin','Pure C only','c908v/RISC-V编译；model_init后加载，输出重新query','补齐图节点不等于NPUkernel或免费fallback'),
('RK02_00_RKNN3_SDK_Release_Notes_V1.2.0','p16 VLM准确率','InternVL3-2B MMbench(cn) 77.23 72.77','浮点与W4A16G32官方表','下降4.46个百分点，非机器人成功率'),
('RK08_TRT_Explicit','Weight-Only Quantization / Q/DQ','WoQ is available only for INT4 block quantization with GEMM layers','TensorRT11.4.1文档快照','机制比较，无同条件速度排名')],
'08B_Memory_Coprocessor_Multicard':[
('RK02_02_RKNN3_SDK_Development_Guide_V1.2.0','p63—64 memory','rknn3_create_mem_from_phys(): ... not implemented','cacheable需TO/FROM_DEVICE阻塞sync；fd需有效size','fd支持不推出跨PCIe透明共享'),
('RK02_02_RKNN3_SDK_Development_Guide_V1.2.0','p100—104 multi-card','The Runtime does not automatically combine multiple contexts into one multi-card model','主机线程/队列；每段session；必须copycallback数据','扩容与单请求延迟分开'),
('RK02_02_RKNN3_SDK_Development_Guide_V1.2.0','p125 Paged Attention','only 1 is supported in the current version','request_num=1；tokens_per_page编译决定','不写任意多请求并行'),
('RK02_00_RKNN3_SDK_Release_Notes_V1.2.0','p12/15性能表','Gemma-4-31B 4x RK1828 5120 128 9153.38','RK3588performance/PCIe/RK182X1GHz；decode13.82TPS','与单卡7B短输入不可算加速比'),
('RK08_TRT_WeightStream','Weight Streaming','offload some weights from device memory to host memory','strong typing、构建flag、budget和scratch','GPU容量机制，非RK支持或性能证据')],
'08C_Perception_RealTime_Trust':[
('RK03_Camera','IQ Files','isp20 xml configuration are not suitable for isp3x even after transfer','kernel5.10示例；ISP3xJSON','sensor/IQ代际必须绑定'),
('RK08_Linux_Locks','rtmutex / semaphore / PREEMPT_RT','counting semaphores have no concept of owners','官方锁语义，raw_spinlock与spinlock不同','优先级继承不消除所有不可抢占区'),
('RK02_AMP_Prereq','4.2 Plan resources','DTS reserved-memory, ITS load/size, and the linker script must agree','private/shared memory、外设/IRQ/IOMUX/clock','分核非完全隔离共享DRAM/电源'),
('RK02_02_RKNN3_SDK_Development_Guide_V1.2.0','p150—151 Encrypted Model','AES-256-CTR ... RSA-OAEP','用户AESkey与RKkey；init后load前解密key','密文传输为官方宣称；不推导完整篡改/安全认证'),
('RK02_SecureBoot','overview Notes','Rollback-index rollback settings are not supported','特定Firefly Linux SDK文档','镜像认证非抗回滚或动作保护'),
('RK08_Jetson_Secure','Secure Boot / Fuses and Security','Once a fuse bit is set to 1, you cannot change its value back to 0','R36.4.4、BootROM/PKC/UEFI','机制比较，非安全性排名')],
'08_Core_Technology_Moat':[
('RK02_02_RKNN3_SDK_Development_Guide_V1.2.0','p101拓扑/p125KV/p150加密','host-side hidden-state forwarding','V1.2.0具体边界已在08A/B/C展开','总览连接机制到放行，不证明已实测收益'),
('Rockchip_Multicard_2026','02/03 VLA与未来产品','计划推出RK1860','2026-09-22计划措辞','非当前可供货SKU'),
('RK02_SecureBoot','overview','Rollback-index rollback settings are not supported','本文08总览安全边界','不将技术组合当整机安全认证')],
'09_SWOT_Analysis':[
('RK09_FinancialAPI','data.content[0:3]','2026年第三季度报告；2026年半年度报告','官网API仅报告标题/date/URL；SSE原件是challenge已拒收','不引用收入/利润或以总收入推机器人收入'),
('RK09_FinancialAPI2','data.content[0]','2025年年度报告','发布日期2026-04-15，正文未取得','访问缺口非公司未披露；无市占率分母'),
('Rockchip_Multicard_2026','01办公智能体','目前已在部分省份部署','瑞芯微与亿次网联、RK1828；厂商宣称','无客户/台数/在岗/ROI；非机器人运营'),
('Firefly_RK182X_Kit','default selected variant','RK3588S (8G+64G) + RK1820 ... $959.00','商店单件页面未结算税/地区/库存','不是双RK1828正式报价'),
('Firefly_RK182X_Kit_PDF','p4 Power consumption','RK3588 + 2 × RK1828 ... Max: 42W','整板12V、测试負载/环境未列','非单芯TDP或全年平均功率'),
('RK07_Shipping','Shipping Time / NOTE','Order preparation time: 3-7 business days','参考运输/备货分开；customs duties客户','不保证逐配置库存/交期'),
('RK09_GenAI','第二、七、十一、十七条','未向境内公众提供生成式人工智能服务的，不适用本办法的规定','2023-07-13公布/08-15施行；有限检索范围','不推导其他法律豁免；不覆盖全部新规/出海辖区')]
}
for stem,items in rows.items():
 f=s/'evidence'/f'{stem}.json';v=json.loads(f.read_text(encoding='utf-8'));result=[]
 for n,loc,quote,conditions,finding in items:
  assert n in v['source_ids'],(stem,n)
  c=claim(n,loc,quote,conditions,finding,'事实/厂商宣称/分析；正文分别标注');c['original_excerpt']=quote;result.append(c)
 v['claim_review']=result;v['manual_review']['coverage']='逐关键主张核对API/手册页码/条款/原文片段；性能与商业宣称、分析、未取得内容明确分开。'
 f.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
print('specific claim audit',list(rows))
