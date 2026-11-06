"""Build only chapter 02 and its source/evidence files. Offline; no registry mutation."""
import hashlib, json, pathlib, re
P = pathlib.Path(__file__).resolve().parents[1]
A = P / 'reference_metrial'
R = json.loads((A/'_registry/materials.json').read_text(encoding='utf-8'))
F = {x['slug']:x for x in json.loads((P/'research_state/figure_manifest_02.json').read_text(encoding='utf-8'))}
B = (P/'research_state/02_body.txt').read_text(encoding='utf-8')
LABELS = {
 'AMD_ROCm_Docs':'ROCm Core SDK总览', 'AMD_RyzenAI_Docs':'Ryzen AI软件总览', 'AMD_VitisAI_Current':'Vitis AI当前发行入口',
 'AMD_RyzenAI_Linux':'Ryzen AI Linux安装与P100支持', 'AMD_ROCm_Compatibility':'ROCm设备/OS/组件兼容矩阵',
 'AMD_VitisAI_Gen2_Release':'Vitis AI Gen2 6.3 release notes', 'AMD_Kria_AI_Dev':'Kria AI机器人开发平台',
 'AMD_EDF_Production':'EDF从原型到生产维护指南', 'AMD_XRT_Docs':'XRT Master架构与入口',
 'AMD_Vitis_Product':'Vitis软硬件开发流程', 'AMD_VitisAI_VART_App':'Gen2 VART应用开发与零拷贝',
 'AMD_EDF_Docs':'EDF文档总览', 'KRS_Install':'KRS 1.0安装与多仓库清单', 'AMD_ROSS':'Ross工程助手产品与FAQ',
 'AMD_ROCm_PyTorch':'ROCm PyTorch安装', 'AMD_ROCm_vLLM':'ROCm vLLM安装', 'AMD_ROCm_ORT':'ROCm ORT与MIGraphX插件',
 'AMD_MIGraphX':'MIGraphX安装与支持', 'AMD_RyzenAI_Install':'Ryzen AI Windows安装', 'AMD_RyzenAI_App':'Ryzen AI EP应用与兼容表',
 'AMD_VitisAI_Gen2_Requirements':'Gen2 6.3主机/软件/板级要求', 'AMD_VitisAI_Gen1_Install':'Gen1 6.3安装与NPU IP配置',
 'AMD_EDF_Release':'EDF v26.06.1产物/版本/主机要求', 'AMD_ROCm_Transition':'ROCm TheRock迁移指南',
 'AMD_ROCm_Release':'ROCm Core SDK release/known issues', 'AMD_HIP_Docs':'HIP开发总览', 'AMD_HIPIFY_Docs':'HIPIFY迁移工具',
 'AMD_HIP_Async':'HIP异步执行API', 'AMD_HIP_Memory':'HIP统一内存与设备条件', 'AMD_RyzenAI_Release':'Ryzen AI release/known issues',
 'AMD_RyzenAI_Quantization':'Ryzen AI量化后端配置', 'AMD_VitisAI_Gen2_Quantization':'Gen2 VINT8/BF16量化配置',
 'AMD_Quark_RyzenAI':'Quark支持Ryzen AI的开发路径', 'AMD_RyzenAI_Compile':'Ryzen AI EP编译/运行/缓存',
 'AMD_RyzenAI_Ops':'Ryzen AI算子支持表', 'AMD_RyzenAI_LLM':'Ryzen AI LLM路线', 'AMD_RyzenAI_Server':'Lemonade REST接口',
 'AMD_RyzenAI_Hybrid':'Ryzen AI OGA混合推理', 'AMD_RyzenAI_OGA_Prepare':'OGA模型准备与产物',
 'AMD_Vitis_Libraries':'Vitis Libraries及2025.2维护变更', 'AMD_VitisAI_Gen1_Runtime':'Gen1 CPU与VART runtime API',
 'AMD_VitisAI_Gen1_License':'Gen1 NPU IP/Vivado许可', 'AMD_VitisAI_Gen2_Compile':'Gen2 ONNX离线编译',
 'AMD_VitisAI_Gen2_Install':'Gen2软件/镜像/SDK安装', 'AMD_VitisAI_Gen2_License':'Gen2 compiler/Vivado许可',
 'AMD_VitisAI_Gen2_Output':'Gen2 .rai/cache与编译报告', 'AMD_VitisAI_Gen2_Deploy':'Gen2 ORT/VART ML执行选择',
 'AMD_VitisAI_Gen2_CPU_Partition':'Gen2编译期CPU分区', 'AMD_VitisAI_Gen2_Architecture':'Gen2 VART ML张量/所有权/线程模型',
 'AMD_VitisAI_Gen2_Async':'Gen2异步执行及样例边界', 'AMD_VitisAI_Gen2_Tenancy':'Gen2 DP/TP与资源配置',
 'AMD_XRT_Native':'XRT Native BO/kernel与NPU API', 'AMD_EDF_Product':'EDF产品定位',
 'AMD_EDF_Overview_PDF':'EDF产品概览PDF', 'AMD_EDF_Migration':'PetaLinux到EDF迁移',
 'AMD_EDF_SHEL':'SHEL工具/接口关系', 'AMD_EDF_SHEL_XSA':'XSA到SDT/Yocto machine流程',
 'AMD_EDF_Segmented':'Segmented configuration与DFX区别', 'AMD_EDF_PL_Load':'EDF segmented PL装载与firmware',
 'AMD_EDF_Domains':'EDF多domain/资源/通信YAML', 'AMD_EDF_Zephyr':'Zephyr处理器状态与SMP限制',
 'KRS_Official_Repo':'Xilinx/KRS官方文档仓库', 'KRS_V1_Docs':'KRS 1.0文档入口', 'KRS_Hardware':'KRS官方与非官方硬件范围',
 'KR260_Perception_Deploy':'KR260 ROS 2感知实际部署指南', 'KRS_Realtime':'KRS端到端实时条件', 'KRS_License':'KRS文档仓库Apache-2.0条文',
 'AMD_Ross_Repository':'Ross skills/docs与MCP分工', 'AMD_VitisAI_Gen2_Reference':'VEK385参考系统架构',
 'AMD_RyzenAI_Analyzer':'Ryzen AI NPU Analyzer精度/频率条件', 'AMD_RyzenAI_SMI':'NPU SMI测试/功率范围',
 'AMD_ROCm_Licenses':'ROCm组件混合许可', 'AMD_HIP_License':'HIP许可', 'AMD_RyzenAI_Licenses':'Ryzen AI EULA与第三方条款'
}
ids = list(dict.fromkeys(re.findall(r'@@(?!FIG:)([A-Za-z0-9_]+)@@',B)))
assert set(ids) <= LABELS.keys(), set(ids)-LABELS.keys()
excluded = {
 'KRS_Repository':'错误候选，HTTP404；正确仓库Xilinx/KRS已另归档',
 'KRS_Docs':'JS redirect壳；实际sphinx/build/html页面另归档',
 'Kria_Ubuntu':'redirect壳，无可引用正文', 'Kria_BootFW':'redirect壳，无可引用正文',
 'Kria_OpenAMP':'redirect壳，无可引用正文', 'KR260_Perception_Overview':'目录导航，无实际部署正文',
 'AMD_VitisAI_Gen2_ML_API':'API链接跳转说明，不能代替真实架构/API正文',
 'Kria_Apps_Docs':'根入口redirect/导航，采用实际KR260部署页'
}
assert not set(ids)&excluded.keys()
def version(s):
 if s=='AMD_EDF_Overview_PDF': return 'Sept 2025；28页；方法图，不作为2026支持矩阵'
 if s.startswith('AMD_EDF_') and s not in ('AMD_EDF_Product',): return 'EDF 26.06.1-rev3文档快照；release v26.06.1仅部分重建'
 if s.startswith('AMD_VitisAI_Gen2_') or s=='AMD_VitisAI_VART_App': return 'Gen2 6.3 public guide；Vivado/Vitis 2026.1；Rev-A/B评估硅片'
 if s.startswith('AMD_VitisAI_Gen1_'): return 'Gen1 6.3；VEK280；NPU IP配置需单独匹配'
 if s=='AMD_VitisAI_Current': return '6.3 General Access文档；不代表板/二进制量产认证'
 if s=='AMD_RyzenAI_Docs': return '1.9.0；Last modified 2026-11-02为修改时间'
 if s=='AMD_RyzenAI_App': return '1.9.0 beta描述；兼容表缺1.9，保留1.8驱动行冲突'
 if s=='AMD_RyzenAI_Ops': return 'latest路径但正文表明Ryzen AI1.8.0算子；不能当1.9完整表'
 if s=='AMD_RyzenAI_Install': return '1.9路径；NPU driver32.0.201.448；原页日期10/3/2026'
 if s=='AMD_RyzenAI_Linux': return '1.9；XRT 2.26.89/amdxdna 2.26.260102.59；Linux NPU flow'
 if s.startswith('AMD_RyzenAI_'): return 'Ryzen AI 1.9.0 latest文档快照；各页旧示例/已知问题另标'
 if s=='AMD_Quark_RyzenAI': return '通用Quark latest快照；未标唯一包版本，不替代Vitis所带0.12'
 if s=='AMD_ROCm_Compatibility': return 'Core SDK10.1.0；更新字段2026-08-26，不能当各组件发布日期'
 if s=='AMD_ROCm_vLLM': return '10.1.0选项；0.29.1.dev0+rocm10.1.0（20261002）；矩阵0.29.0另列'
 if s=='AMD_ROCm_PyTorch': return '10.1.0选项；PyTorch2.14.0/Python3.12镜像示例，digest未锁'
 if s=='AMD_ROCm_ORT': return '10.1.0选项；ORT1.29.0，plugin1.0.0+rocm10.1.0，MIGraphX2.18.0'
 if s=='AMD_MIGraphX': return '2.18.0安装选项；Python/架构以对应表为准'
 if s.startswith('AMD_ROCm_'): return 'ROCm Core SDK10.1.0 latest快照；独立组件/旧发行另辨'
 if s.startswith('AMD_HIP'): return 'HIP/HIPIFY latest快照；10.1矩阵HIP7.16.0、HIPIFY10.1.0；硬件特性有条件'
 if s.startswith('AMD_XRT_'): return 'XRT Master快照，含experimental API；不是固定release；旧footer保留'
 if s.startswith('KRS_'): return 'KRS1.0文档/仓库快照；文档Last updated2024-01-02；Vitis2022.1/Humble'
 if s=='KR260_Perception_Deploy': return '文档2022.1；Last updated2026-08-13；xlnx-rel-v2022.1_update4'
 if s=='AMD_Vitis_Libraries': return 'main仓库快照；2025.2起PL库停维护变更；未锁commit'
 if s=='AMD_Kria_AI_Dev': return '2026-11-04产品页快照；Notify Me；未取得唯一suite release'
 if s.startswith('AMD_Ross') or s=='AMD_ROSS': return '产品FAQ/main仓库快照；Vivado全版本/HLS2025.2+；未锁release'
 return '网页快照；未标明确发布日期/修订，不以采集日期代替发布时间'
nums={s:f'S{i:02}' for i,s in enumerate(ids,1)}
catalog=[]
for s in ids:
 r=R[s]; assert r['status']==200 and r['archive_status'] in ('complete_static','partial_static'),s
 assert pathlib.Path(r['file']).is_file(),s
 B=B.replace(f'@@{s}@@',f"[{nums[s]} {LABELS[s]}]({r['url']})")
 catalog.append(dict(source_id=s,number=nums[s],title=LABELS[s],version=version(s),url=r['url'],
  file=pathlib.Path(r['file']).as_posix(),sha256=r['sha256'],original_file=pathlib.Path(r['original_file']).as_posix(),
  original_sha256=r['original_sha256'],metadata_file=(pathlib.Path(r['file']).parent/'metadata.json').as_posix(),
  collected_at=r.get('retrieved_at_utc',r.get('archived_at_utc')),archive_status=r['archive_status'],
  missing_dependencies=r.get('unavailable_assets',{}),notes=r.get('notes',[])))
figids=list(dict.fromkeys(re.findall(r'@@FIG:([A-Za-z0-9_]+)@@',B)))
assert len(figids)==9
for fid in figids:
 assert F[fid]['source_id'] in ids,fid
 B=B.replace(f'@@FIG:{fid}@@',F[fid]['file'])
assert '@@' not in B
body_han=len(re.findall('[\u4e00-\u9fff]',B))
appendix=['\n## 参考资料与本地原件\n',
 '全部引用材料采集于2026-11-04；正文S编号与下表对应。`latest`/`main`/`Master` 是采集时路径，不能作为不可变release。HTML本地快照与原响应分开保存；每份metadata记录HTTP、哈希及缺失依赖。`partial_static`仅代表正文/静态归档的部分完整度，不保证动态交互或像素级保真。\n',
 '| 编号 / 原文URL | 版本、日期与使用条件 | 本地HTML/PDF与元数据 | 归档状态 |', '|---|---|---|---|']
for c in catalog:
 appendix.append(f"| [{c['number']} {c['title']}]({c['url']}) | {c['version']} | [原件]({c['file']}) · [metadata]({c['metadata_file']}) | {c['archive_status']} |")
appendix+=['\n完整引用清单、原响应哈希、缺失依赖与人工核验见 [source catalogue]('+ (P/'research_state/source_catalog_02.json').as_posix()+') 和 [章节证据]('+ (P/'research_state/evidence/02_Software_Stack.json').as_posix()+')。检查与最终复用运行记录见本章QA；没有开展实机测试。']
(P/'02_Software_Stack.md').write_text(B+'\n'.join(appendix)+'\n',encoding='utf-8')
(P/'research_state/source_catalog_02.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
manifest=[dict(name=s,url=R[s]['url'],expected='pdf' if pathlib.Path(R[s]['file']).suffix=='.pdf' else 'html',used_by=['02_Software_Stack']) for s in ids]
(P.parents[1]/'toolkit/manifests/AMD_02_final.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

# Exact quotes are extracted from existing archived text, never generated or fetched.
TEXT={s:re.sub(r'\s+',' ',(pathlib.Path(R[s]['file']).parent/'text.txt').read_text(encoding='utf-8')) for s in ids if pathlib.Path(R[s]['file']).suffix=='.html'}
claims=[];missing=[]
def claim(s,subject,location,needle,conditions,finding,kind='事实',support=None):
 assert s in ids
 content=TEXT[s]; n=re.sub(r'\s+',' ',needle)
 m=re.search(re.escape(n),content,re.I)
 if not m: missing.append((s,needle));return
 l=max(0,m.start()-90);rr=min(len(content),m.end()+460)
 claims.append(dict(claim=subject,source_id=s,source_url=R[s]['url'],location=location,evidence_type=kind,
  conditions=conditions,finding=finding,exact_quote=content[m.start():m.end()],context_quote=content[l:rr],
  quote_character_range=[m.start(),m.end()],quote_basis='归档text.txt，空白规整；是资料定位辅助，不替代人工正文/表核对',
  material_version=version(s),collected_at=R[s].get('retrieved_at_utc'),supporting_source_ids=support or []))

claim('AMD_ROCm_Docs','Core SDK发行版本','ROCm overview','10.1.0','当前ROCm首页','TheRock生产stream；与旧7.1.1路径分开')
claim('AMD_ROCm_Transition','安装前缀与包机制','Installation paths','/opt/rocm/core-10.1','10.1.0；DEB/RPM vs tarball','替代路径和依赖解析有安装方式条件')
claim('AMD_ROCm_Transition','旧发行迁移起点','Transition overview','7.14.0','迁移起点非机器人BSP版本','不把组件版本或Python环境随意混配')
claim('AMD_ROCm_Compatibility','R9700与Max+395架构支持','GPU/APU support table','gfx1151','Max+395/8060S vs Embedded X199','不能由消费APU正式支持推出X199 SKU支持','未知')
claim('AMD_ROCm_Compatibility','MI350P出现在GPU矩阵','Supported GPUs','MI350P','gfx950，OS/driver另表','软件支持条目不证明量产交期')
claim('AMD_ROCm_Compatibility','框架独立版本组合','Framework support','2.14.0','PyTorch/OS/Python明确组合','不把2.14与vLLM的2.13依赖拼为验证环境')
claim('AMD_ROCm_Release','ROCm SMI弃用与迁移','Deprecations','ROCm SMI','10.1标准构建','旧known-issue命令残留不代表已安装工具')
claim('AMD_ROCm_Release','MI350训练回归未全面消失','Known issues','6–22%','特定训练模型/配置','不泛化所有任务或宣称全部修复')
claim('AMD_ROCm_PyTorch','镜像tag只是文档安装示例','Docker install','rocm10.1.0_ubuntu24.04_py3.12_pytorch_release_2.14.0','10.1/2.14/Py3.12','本文未pull，复建还需digest')
claim('AMD_ROCm_vLLM','vLLM开发wheel与依赖','pip wheel install','0.29.1.dev0','ROCm10.1；Py3.14/torch2.13','开发wheel不冒充矩阵稳定0.29.0')
claim('AMD_ROCm_vLLM','tensorizer workaround','Installation workaround','tensorizer==2.12.1','该文档版本组合','与FlashAttention/AITER一同锁版本')
claim('AMD_ROCm_ORT','MIGraphX插件依赖pip库','MIGraphX EP install','migraphx-libs','ORT1.29/MIGraphX2.18/10.1','系统包不能替代pip依赖；EP可见不证明全图优化')
claim('AMD_ROCm_ORT','ORT显式插件注册','Verification code','register_execution_provider_library','独立EP wheel','与旧monolithic路线分开')
claim('AMD_MIGraphX','MIGraphX版本与支持范围','Installation','2.18.0','具体GPU/框架组合','目标VLA动态shape/workspace未取得实测','未知')
claim('AMD_HIP_Async','异步stream/event与竞争','Concurrent kernels','hipStreamWaitEvent','HIP/具体GPU async engine','事件表达依赖，不保证硬实时或等性能')
claim('AMD_HIP_Memory','统一内存特性取决于设备和OS','Unified memory support','HSA_XNACK','HMM/XNACK/设备属性','managed memory、UMA和物理共享DRAM分开')
claim('AMD_RyzenAI_Docs','Ryzen AI文档版本','Overview','1.9.0','修改日期不是release日期','ORT三EP示意不能外推所有Linux后端')
claim('AMD_RyzenAI_Linux','P100系列Linux明确支持','Supported platforms','P100','Ubuntu24.04/kernel≥6.10/Python3.12','仍需目标SKU/载板/BSP')
claim('AMD_RyzenAI_Linux','Linux XRT/xdna版本','Installation DEB names','2.26.260102.59','1.9 Linux NPU flow','runtime DEB preview不混作已量产统一驱动')
claim('AMD_RyzenAI_Install','Windows驱动版本及日期','NPU Driver','32.0.201.448','页面日期10/3/2026、Win11build26100+','应用页1.8最低版本不强套1.9')
claim('AMD_RyzenAI_App','1.9 beta状态冲突','Application Development','beta','同组文档首页1.9、兼容表缺1.9','保留冲突并需实际包release确认','未知',['AMD_RyzenAI_Install','AMD_RyzenAI_Licenses'])
claim('AMD_RyzenAI_App','应用页驱动最低行','EP compatibility','32.0.203.280','1.8行，非1.9已确认最低版本','不取数字较大者自行构成1.9支持规则','未知')
claim('AMD_RyzenAI_Quantization','XINT8后端配置','INT8 CNN quantization','XINT8','对称INT8/power-of-two scale','不套VitisGen2 VINT8')
claim('AMD_VitisAI_Gen2_Quantization','VINT8导出配置','Quantization code','Int32Bias','VitisAI6.3所带Quark；enable_npu_cnn等','后端配置/算子/校准样本必须一起验证')
claim('AMD_VitisAI_Gen2_Quantization','随机校准仅用于测试','Calibration guidance','Use random data (for testing only)','真实校准样本vs随机数据','MinMSE不等于真实机器人成功率','分析')
claim('AMD_Quark_RyzenAI','Quark的RyzenAI导入链','Development Flow Steps','Trained models in popular frameworks','通用latest，PyTorch/TensorFlow导入','格式交换不等于不同后端engine通用')
claim('AMD_RyzenAI_Compile','PHX/HPT的xclbin边界','X1/X2 configuration','4x4.xclbin','PHX/HPT INT8X1；STX/KRK默认X2','路径为phoenix目录下4x4.xclbin；旧Nx4/1x4不继续支持')
claim('AMD_RyzenAI_Compile','ORT context用于部署','EP context model','ep.context_enable','匹配EP/driver/config/model','开发cache不当跨版本可移植产物')
claim('AMD_RyzenAI_Compile','落点报告辅助核验','EP report','XLNX_ONNX_EP_REPORT_FILE','编译与EP配置','CPU fallback必须读取实际分区报告')
claim('AMD_RyzenAI_Ops','算子表仍标旧版且有配置边界','Operator support tables','operators supported in Ryzen AI 1.8.0','1.8表不是完整1.9支持表；算子/shape/backend一起确认','不是任意ONNX全图优化支持；正文与版本记录已保留旧版')
claim('AMD_RyzenAI_Server','REST接口契约','Lemonade server endpoints','/api/v1/chat/completions','当前RyzenAI server文档','文本请求/输出不是关节动作')
claim('AMD_RyzenAI_Hybrid','OGA异构执行','Hybrid deployment','supports deploying LLMs on Ryzen AI PCs','固定模型/tokenizer/context/genai config','不能仅交付一个ONNX')
claim('AMD_RyzenAI_Release','新模型优化状态','Release notes','functional','1.9模型列表','functional支持与optimized性能分开')
claim('AMD_Vitis_Libraries','PL库停止维护','README maintenance notice','will no longer be maintained','2025.2起，七个PL库，AIE库不受影响','旧release可用不代表当前维护')
claim('AMD_VitisAI_Gen1_Install','Gen1 NPU IP精确配置','NPU IP name/default','VE2802_NPU_IP_O00_A304_M3','三DDR/NoCplacement，M1另选','不能跨NPUIP配置重用镜像和模型')
claim('AMD_VitisAI_Gen1_Runtime','CPU仍可能执行未卸载子图','Embedded CPU operations','CPU sub-graphs','未全图accelerated','与CPU不做inferencecompute前句合读')
claim('AMD_VitisAI_Gen1_Runtime','Gen1并发承诺仍为计划','VART features','planned for future releases','Gen1 runtime页','不套Gen2线程安全')
claim('AMD_VitisAI_Gen1_License','Gen1 IP license','Synthesis diagnostics','npu_aieml@2024.06','建NPUreference design','需VivadoEnterprise/Pro；文档公开不免许可')
claim('AMD_VitisAI_Gen2_Requirements','评估硅片成熟度','Board requirements','pre-production','VEK385RevA/B','publicguide不代表量产板认证')
claim('AMD_VitisAI_Gen2_Requirements','绑定软件与opset范围','Software requirements','2.5.1','torch2.5.1/Quark0.12/ORT1.28/opset11–20','不自动替换通用最新版')
claim('AMD_VitisAI_Gen2_Release','摄像头流设计仅RevB','New features','Rev-B','6.3 camera ISP/PL/NPU/CPU/DP','视觉流不等于关节本体闭环')
claim('AMD_VitisAI_Gen2_Compile','大模型external data完整性','ONNX external data','2GB','ONNX主图与外部权重完整路径','单ONNX不包含所有大模型权重')
claim('AMD_VitisAI_Gen2_Install','SDK路径文档残留','SDK environment setup','cortexa72-cortexa53','VEK385目标A78','实际取安装器生成environment，不擅自改原件','未知')
claim('AMD_VitisAI_Gen2_Output','默认单文件.rai','Model Storage Formats','generated by default','6.3 compiled model','mmap加载不证明端到端零拷贝')
claim('AMD_VitisAI_Gen2_Output','开发目录要完整保留','Directory Structure Format','keep_outputs','true保留完整cache','报告样例阈值/clock/编译时间不当通用默认')
claim('AMD_VitisAI_Gen2_Deploy','ORT与VART所需产物','Files Needed','original ONNX model','ORT需原图/config；VART直接compiled model','runtime选择决定分区/依赖')
claim('AMD_VitisAI_Gen2_CPU_Partition','CPU分区在编译期固定','CPU partition workflow','vaiml_cpu_partition','compiler支持CPUoperators','不是ORT任意算子的runtimefallback')
claim('AMD_VitisAI_Gen2_Architecture','HW与CPU view的格式不同','Tensor and Memory Architecture','HCWNC4','示例NCHWFP32→HCWNC4BF16','不同模型取实际metadata，CPUview有copy')
claim('AMD_VitisAI_Gen2_Architecture','HW+NON_CMA禁止组合','Zero-copy behavior','throws std::runtime_error','HW + USER_POINTER_NON_CMA','用户malloc指针不能冒充硬件可见CMA')
claim('AMD_VitisAI_Gen2_Architecture','用户buffer不转移所有权','NpuTensor Ownership','does not take ownership','caller buffer需覆盖tensor/job lifetime','RAII仅runnerallocated；subtensor一层')
claim('AMD_VitisAI_Gen2_Architecture','Gen2 runner线程安全范围','Thread Safety','wait() calls are thread-safe','Gen2执行API，callback内部worker','共享队列仍需应用同步，不外推Gen1')
claim('AMD_VitisAI_Gen2_Async','异步提交资源耗尽','Overview','RESOURCE_UNAVAILABLE','每job独立buffers；slot数量有界','等待完成后重试，不无限积压')
claim('AMD_VitisAI_Gen2_Async','异步样例重复同一batch','Demonstration Example','same in-memory batch','一个输入tensor，默认两个jobs','样例平均时延/FPS不等于真实多相机或P99')
claim('AMD_VitisAI_Gen2_Tenancy','DP复制与TP分片','Data/Tensor Parallelism','replicating','每block16tiles，实际资源看compiler','DP容量和单帧时延分开')
claim('AMD_VitisAI_VART_App','VART-X设备/预处理API','Initialization/PreProcess','IMAGE_PROCESSING_HLS','匹配XCLBIN、VideoInfo、mean/scale','库实现存在不证明所有相机全链零拷贝')
claim('AMD_VitisAI_VART_App','Resize几何须还原','Preprocessing','PANSCAN','DEFAULT/LETTERBOX/PANSCAN','crop/padding还原后才能用于相机坐标观测')
claim('AMD_XRT_Native','BO内存bank与同步','Buffers','kernel.group_id','经典XCLBIN FPGAroute','map/write后设备同步，run/wait后host同步')
claim('AMD_XRT_Native','新NPU API与release边界','Experimental/NPU APIs','experimental','Master ELF/hw_context路线','不可用旧XCLBIN例子替代x86NPU loader')
claim('AMD_XRT_Native','Buffer flags有系统条件','Buffer flags','Not all the flags are honored','host/device/driver-specific','XRT名字不代表所有backendABI相同')
claim('AMD_EDF_Release','26.06.1不是全套重建','Release overview','rebuilds part of v26.06','支持板artifacttable','不推广所有板commonimage为当前验证版')
claim('AMD_EDF_Release','common WIC与板boot固件分开','Common Disk Images','not board-specific','CPUfamilycommonWIC + boardbootfirmware','硬件/DT/PL/driver仍要匹配')
claim('AMD_EDF_SHEL_XSA','Lopper由gen-machine-conf调用','SHEL Flow','invokes it automatically','XSA→SDT→machine/DT→Yocto','不保证任意XSA驱动/隔离完整')
claim('AMD_EDF_SHEL_XSA','实际Yocto接口命令','SHEL Flow in a Few Steps','bitbake edf-linux-disk-image','MACHINE固定为新machine','只是官方命令核验，本章未构建')
claim('AMD_EDF_PL_Load','segmented不需要shell.json','Integration note','do not need a shell.json','segmentedconfiguration，而DFX另有要求','不能混用两类重配置流程')
claim('AMD_EDF_PL_Load','动态装载接口','Deploy and Run','-loadByName','firmwarebundle/DT/PDI一致','接口名不代表自动OTA/停机/回退')
claim('AMD_EDF_Domains','跨domain通信结构','Domain fields','vring','CPU/memory/reservedmemory/remoteproc/rpmsg','YAML描述不等于隔离或安全证书')
claim('AMD_EDF_Zephyr','Zephyr核级状态','Supported Processors','No SMP support','CortexR52PROD、A78EA/noSMP','不泛化所有核/board/peripheral')
claim('AMD_EDF_Production','AMD不是生产OSV','Warning','does not provide production-grade software','AdaptiveSoCfamilies，非所有AMD产品','硬件生命周期不等softwareLTS/SLA')
claim('AMD_EDF_Production','没有生产updatefeed','Introduction','does not operate an update feed','referenceEDFimage','产品需自己/OSV承担安全更新责任')
claim('AMD_EDF_Production','kernel fork不是supported OS','Kernel sources policy','not a supported OS product','linux-xlnx；2026.1base6.18','分支名LTS不代表AMD生产维护SLA')
claim('KRS_Install','旧版KRS验证环境','Prerequisites','only been tested in Ubuntu 22.04','KRS1.0/Humble/Vitis2022.1/GazeboClassic11','不能套新x86Kria/EDF2026')
claim('KRS_Install','DDS设置在target','DDS Recommendation','This step needs to be done on target board','CycloneDDS，hostcrosscompile不同','不把RMWenv无条件套host')
claim('KRS_Hardware','官方与非官方target','Hardware supported','KR260','K26/KV260/KR260 full；其他unofficial','不推广K24/X100')
claim('KR260_Perception_Deploy','部署页版本冲突','Download/install commands','1.3-1','文档2022.1/update4，下载1.3-1 vs安装1.0-1','未宣称复建成功','未知')
claim('KR260_Perception_Deploy','FPGA图像链收益','Performance comparison','24.42%','640×480rectify/resize/AXI4Streamqueue','厂商结果非完整模型/本体成功收益','厂商宣称')
claim('KRS_Realtime','实时必须各层有界','Real-time ROS 2','equally time bounded','ROS/OS/network/applicationalllayers','网页不等目标整机WCET证书')
claim('KRS_License','仓库Apache许可范围','LICENSE.txt','Apache License','Xilinx/KRSdocs仓库','不覆盖全部repos/firmware/IP')
claim('AMD_Kria_AI_Dev','新软件suite尚需唯一发行','Software features','Robotics Software Suite','NotifyMe/Day0declared','未取得publicBSP/model/releasemanifest；不使用KRS/Ross填补','未知')
claim('AMD_ROSS','Ross是工程工具助手','Overview','retrieval-augmented generation','MCP/RAG/skills/designexamples','不等机器人perception/actionruntime')
claim('AMD_ROSS','Ross按工具版本支持','FAQ','Version 2025.2 and later','HLS2025.2+，Vivadoallversions','仍需toollicense，输出非确定')
claim('AMD_Ross_Repository','Ross仓库与MCP分开发行','Prerequisites/Plugin','plugin contains skills only','skills/docsMIT、MCP另安装','不开Ross tools，本章只研究公开资料')
claim('AMD_RyzenAI_Analyzer','Analyzer精度限制','Limitations','INT8','当前BF16only，NPUclock可修改','cycle→time需核实际clock')
claim('AMD_RyzenAI_SMI','latency测试是no-op','NPU sanity check','no-op control code','alltestsperformance，示例84.2us','不是模型时延/机器人闭环实测')
claim('AMD_RyzenAI_SMI','throughput仅shim传输','NPU sanity check','MM2S Shim DMA','DDR→shim→DDR，例59891ops','不当NPU模型吞吐或策略Hz')
claim('AMD_RyzenAI_SMI','Linux功率报告缺失','Platform Information','unavailable for Linux','PHX/HPT不支持功率/GEMM','示例51.3TOPS不是本文实测')
claim('AMD_ROCm_Licenses','整套许可混合','Component license list','GNU General Public License v3.0','具体组件与package分开','文档MIT不覆盖所有库/二进制')
claim('AMD_HIP_License','HIP代码许可','License','MIT','该项目许可范围','不代表权重/数据/runtime全集均MIT')
claim('AMD_RyzenAI_Licenses','EULA只限AMD相关系统','Section2.1.1','include or incorporate AMD products','条款编号2.1不是许可证版本号','分发需具体条款，不是整包MIT')
claim('AMD_RyzenAI_Licenses','beta仅evaluation且无普通分发条款','Section5','Sections 2.1.3 and 2.1.4 do not apply','alpha/beta/EA/preproduction','应用页beta需实际包消歧，未接受EULA')
if missing:
 print(json.dumps({'unmatched_quote_needles':missing},ensure_ascii=False,indent=2)); raise SystemExit(1)
figs=[]
for fid in figids:
 f={k:v for k,v in F[fid].items() if k!='slug'}
 # The page-contained asset is the registry-proven original. Shared pool is identical,
 # but check_report intentionally verifies the self-contained page asset path.
 matches=[a for a in R[f['source_id']].get('assets',[]) if a['url']==f['source_url']]
 if matches:
  a=matches[0]; original=A/a.get('local_file',a['file'])
  assert hashlib.sha256(original.read_bytes()).hexdigest()==f['original_sha256']
  f['original_file']=original.as_posix()
 f['manual_open_review']='已逐张实际打开核查；文字/层次/单位可读，无空白、截断或乱码；渲染/版本限制见正文caption。'
 if fid.startswith('02_edf') or fid=='02_shel_flow': f['material_version']='Sept2025PDF，方法图；页码见operation，非2026支持矩阵'
 elif fid=='02_xrt_layers':f['material_version']='XRTMaster快照，旧footer不能锁定release'
 else:f['material_version']=version(f['source_id'])
 figs.append(f)
trace=dict(source_ids=ids,figures=figs,claim_review=claims,manual_review=dict(
 coverage='02完成：ROCm/HIP/PyTorch/vLLM/MIGraphX、RyzenAI/Quark/OGA、Vitis/Gen1/Gen2/VART/XRT、EDF/SHEL/OpenAMP/Zephyr、KRS/Kriaapps/Ross；完整VEK385视觉→模型链，ROS/动作桥标分析；未开展03。',
 versions_and_measurements='采用具体发行/SDK和设备矩阵，保留Ryzen1.9beta/driver/参数、SDKenv、Masterfooter、旧KRS年代与KR260包名冲突；峰值/sanity/样例/厂商结果不当目标模型、本体或本次实测。',
 maturity_and_licenses='文档公开、账户下载、评估硅片、functional-only、beta和量产支持分开。许可证按文档/代码、IP/compiler、runtime、MCP分层；EULASection5预生产分发限制已读；模型/数据/资产/本体许可还需具体对象。EDFproduction责任明确。',
 figures_opened='9幅逐张实际打开：RyzenAIstack、Vitisflow、XRTlayers、VARTML、async、VEK385system、EDF16/20/24页。无空白/截断/乱码；PDFSept2025仅方法，system图旧ELF/cache由6.3默认.rai正文消歧；HIPforeignObjectSVG未纳入完成图集。'),
 limitations='静态归档与公开材料研究；未安装SDK、接受EULA、下载模型权重、构建/刷板/运行模型或进行实机测试。')
(P/'research_state/evidence/02_Software_Stack.json').write_text(json.dumps(trace,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(report=str(P/'02_Software_Stack.md'),sources=len(ids),figures=len(figs),claims=len(claims),body_han=body_han),ensure_ascii=False))
