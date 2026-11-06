"""Finalize only depth02 index/state after all topics and joint archive passed."""
import pathlib,json,hashlib,shutil,re
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1];A=P/'reference_metrial';Q=A/'derived/qa';T=json.loads((D/'topics.json').read_text(encoding='utf8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mf=P.parents[1]/'toolkit/manifests/AMD_02_software_depth_all.json';M=json.loads(mf.read_text(encoding='utf8'));names={x['name'] for x in M}
run=json.loads((A/'_registry/last_run.json').read_text(encoding='utf8'));C=json.loads((A/'02_software_depth/collection.json').read_text(encoding='utf8'))
assert run['network_requests_including_robots']==0 and run['summary']['failed']==0 and set(run['names'])==names
assert {x['id'] for x in C['materials']}==names
for x in C['materials']:assert pathlib.Path(x['file']).exists() and sha(pathlib.Path(x['file']))==x['sha256']
summaries={};figs=[];claims=[];ids=set()
for stem,title in T:
 q=json.loads((Q/(stem+'_quality.json')).read_text(encoding='utf8'));e=json.loads((P/'research_state/evidence'/(stem+'.json')).read_text(encoding='utf8'))
 assert q['outcome']=='pass' and not q['errors'] and all(q['other_reports_unchanged'].values())
 dr=json.loads((Q/(stem+'_dedup_last_run.json')).read_text(encoding='utf8'));assert dr['network_requests_including_robots']==0 and set(dr['names'])==set(e['source_ids'])
 summaries[stem]=dict(body_han_chars=q['body_han_chars'],sources=q['sources'],figures=q['figures'],tables=q['tables'],claim_reviews=len(e['claim_review']),report_sha256=sha(P/(stem+'.md')))
 ids.update(e['source_ids']);figs+=e['figures'];claims += [dict(topic=stem,**c) for c in e['claim_review']]
assert ids==names
baseline=json.loads((P/'research_state/baselines/02_Topics_Index_before.json').read_text(encoding='utf8'));unchanged={n:sha(P/n)==v for n,v in baseline.items()};assert all(unchanged.values())
shutil.copyfile(A/'_registry/last_run.json',Q/'02_software_depth_all_dedup_last_run.json')
link=lambda label,p:f'[{label}]({p.as_posix()})'
topiclinks={s:link(t,P/(s+'.md')) for s,t in T}
descriptions=[
 'HIP线程/warp与release scope；Graph模板/实例/捕获及graph-safe库；SOMA跨stream；attention与TunableOp；MIGraphX shape/target/.mxr与拷贝；vLLM KV与prefill/decode。',
 'XINT8/A8W8/A16W8/BF16的数值边界；校准reader与SmoothQuant；AutoSearch反馈/停止条件；CPU/NPU分区；context/cache失效；Analyzer时钟和许可。',
 'VAIML passes与CPU-partition产物；AIE chaining/L2/DDR；DP/TP与batch；HCWNC4/8地址/stride；scale贯穿编译和前后处理；异步job、DMA内存与custom op双注册。',
 'XSA→SDT→Lopper→MACHINE/DTS；domain合并规则；carveout/vring/payload；Yocto多配置固件依赖；remoteproc/RPMsg装卸；segmented/DFX；源版本和更新维护责任。',
 'ament/colcon/firmware三pillar；HLS展开与入口带宽；四种感知graph及官方测量；host/kernel源码帧关联与背压；tracing扰动；RT分层；VART→ROS契约和Buffer迁移对标。']
lines=['# AMD 02 软件栈专题索引与审阅入口','',
 '研究截止：2026-11-04。五篇补深专题已完成，等待用户审阅。研究方法参考 NVIDIA 08 的总览/专题组织：从原理和数据流追到 API、配置或源码，说明优化为什么成立，再核对官方测量、对标对象、版本/许可和失效条件。原 01、原 02 与 README 保留。', '',
 '## 1. 按 02A—02E 阅读','',
 '| 独立文件 | 核心机制与实现细节 | 阅读时关注的边界 |','|---|---|---|']
boundaries=[
 '四类“图”消除的开销不同；GPU可见性选择不是隔离；Instinct/Radeon/端侧SKU兼容分别核验。',
 '支持算子不等全部留在NPU；通用Quark文档不替代平台包；1.9/1.8和参数命名冲突保留。',
 '同名VAI EP不等Ryzen ABI；ORT/VART产物不自由交换；HW布局、DMA可达性和job生命周期同时成立才可能少拷贝。',
 '评估镜像不保证custom board；共享内存/RTOS不自动形成缓存一致或WCET；OSPI A/B不等完整产品OTA服务。',
 'stream只绕开特定中间payload；ROS触发和主机拷贝仍在；历史时延表不能当控制频率或完整硬实时证明。']
for (s,t),desc,boundary in zip(T,descriptions,boundaries):lines.append(f'| {topiclinks[s]} | {desc} | {boundary} |')
lines += ['', '## 2. 五篇怎样连接成软件链','',
 '下面是依据专题整理的分析映射，不能把所有软件合成一个跨芯片通用SDK。硬件目标与部署路线先选定，再决定编译器、runtime和系统接口；模型源、编译产物、运行对象、传感器/动作语义是不同交接层。', '',
 '| 链路层次 | 对应专题 | 交接时必须保留的对象 |','|---|---|---|',
 f'| GPU训练/推理部署 | {topiclinks[T[0][0]]} | 框架/ROCm/HIP/库与GPU版本，shape、设备target、Graph依赖、KV/workspace及诊断记录 |',
 f'| Ryzen端侧NPU | {topiclinks[T[1][0]]} | ONNX/校准评估集、量化配置、EP分区、模型context、绑定driver和cache失效规则 |',
 f'| Versal端侧AIE | {topiclinks[T[2][0]]} | 编译JSON/overlay、.rai或目录、CPU/HW tensor metadata、量化参数、buffer/job与custom op |',
 f'| Adaptive SoC系统构建 | {topiclinks[T[3][0]]} | XSA/SDT/domain YAML、DTS/machine、recipe/commit、boot/PL/ELF/rootfs与装载状态 |',
 f'| ROS感知与业务接口 | {topiclinks[T[4][0]]} | frame/epoch、时间基准、标定/布局、producer-consumer同步、期限、过期/排空和降级契约 |', '',
 '软件执行模型与本体控制接口之间仍需具体集成证据。运动、仿真/学习、数据编排和运维的既有平台范围见原 02 总览；本轮没有把第三方理论可运行路线改写为 AMD 自有、量产或本体已验证的交付能力。新 Robotics Software Suite 尚未取得唯一 release，不用旧 KRS 填补该对象。', '',
 link('原 02 软件栈总览',P/'02_Software_Stack.md')+' · '+link('已审阅的 01 硬件平台',P/'01_Hardware_Platform.md'), '',
 '## 3. 本轮值得优先审阅的技术结论','',
 f'1. {topiclinks[T[0][0]]}：Graph减提交开销、编译器优化张量图、attention减少中间物化、在线服务管理KV，各有不同对象和瓶颈。不能把某一优化开关推广成整模型固定收益。',
 f'2. {topiclinks[T[1][0]]}：量化不仅降低位宽，还改变scale、图模式、边界转换及评估成本；编译cache跨EP/driver禁复用，版本升级必须有明确重建路径。',
 f'3. {topiclinks[T[2][0]]}：官方布局图文件名与图内dtype存在差异，已按实际标签解释；wait返回JOB_PENDING时不能回收buffer，异步示例重复旧batch也不等20张新帧。',
 f'4. {topiclinks[T[3][0]]}：固件、device tree与rootfs的一致性由构建依赖和实际装载共同确认。退出host测试不等停RPU；参考发行的长期维护责任仍需产品团队/OSV承担。',
 f'5. {topiclinks[T[4][0]]}：KV260示例纯offload的Mean由91.48降至85.80ms，integrated为66.82ms；26.96%为时延降低。源码进一步显示raw触发、固定尺寸、阻塞读回与early-return风险，收益与正确性须同时验证。', '',
 '上述数字只适用于对应文档的官方测试条件；各专题记录条件和缺项。NVIDIA对标用机制与迁移资产比较，没有相同模型、功耗、BSP与测量口径时不给平台性能排名。', '',
 '## 4. 资料、图源与检查记录','',
 link('02 专题联合资料库（81份，逐份目录）',A/'02_software_depth/index.html')+' · '+link('联合资料清单',mf)+' · '+link('逐份来源/归档状态',A/'02_software_depth/collection.json'), '',
 '| 专题 | 正文汉字 | 来源条目 | 官方图 | 主张核验 | 检查记录 |','|---|---|---|---|---|---|']
for s,t in T:
 u=summaries[s];lines.append(f"| {s[:3]} | {u['body_han_chars']} | {u['sources']} | {u['figures']} | {u['claim_reviews']} | {link('结构/归档',Q/(s+'_quality.json'))} · {link('主张/图源',P/'research_state/evidence'/(s+'.json'))} · {link('来源目录',D/(s+'_sources.json'))} |")
total={k:sum(v[k] for v in summaries.values()) for k in ['body_han_chars','sources','figures','tables','claim_reviews']}
lines += ['', f"五篇合计{total['body_han_chars']}有效正文汉字、{total['tables']}张正文表、{total['figures']}幅官方图和{total['claim_reviews']}项主张记录；跨篇引用计{total['sources']}条，按URL去重为81份。数字只描述材料规模，不替代研究深度或语义正确性。", '',
 '每篇自动检查均通过，图已实际打开查看；主张记录保留原文短引、上下文、版本和成立条件。最后联合导出覆盖五篇全部引用，复用运行的网络请求为0，失败材料未进入有效清单。原 01、原 02、README 与五篇正文的基线哈希一致。', '',
 link('联合复用证明',Q/'02_software_depth_all_dedup_last_run.json')+' · '+link('联合索引/集合核对',Q/'02_software_depth_all_review.json'), '',
 '归档有36份complete_static、45份partial_static；后者已取得有效正文，但仍有图片/样式/外链等依赖缺失。下载器冻结可执行script，未承诺动态交互或像素级完整；原响应、可读HTML/PDF、metadata、图源/衍生哈希均保留在唯一registry下。NVIDIA已有2026-11-03原响应用于对标，导入过程和日期在相应来源记录中区分。', '',
 '## 5. 仍需产品资料或实机补齐的证据','',
 '关键缺口是新AMD Robotics Software Suite/X199的准确软件发行与逐SKU支持；Ryzen文档/包/driver的一致性；Versal容器内完整custom-op约束；KRS历史benchmark的commit、分辨率、样本/warmup、功率及P99；stream的完整连接、帧关联与异常恢复；跨CPU/GPU/NPU/DDR/network的热稳态并发、观测年龄和动作期限；安装二进制/firmware/模型权重/数据与本体SDK的具体许可和维护责任。下载失败与官方未披露分开记录。', '',
 '本轮完成的是文献、API/源码、图和归档核验；未安装SDK、接受EULA、跑模型、刷板或测机器人闭环。五篇各提供可复建验证方案。状态保持02待审阅，03传感器接入尚未开始，继续顺序仍为03→09。', '']
index=P/'02_Topics_Index.md';index.write_text('\n'.join(lines),encoding='utf8')
paths=re.findall(r'\]\(([^)]+)\)',index.read_text(encoding='utf8'));self_log=Q/'02_software_depth_all_review.json'
checks={p:pathlib.Path(p).exists() for p in paths if not p.startswith(('https://','http://','#')) and p!=self_log.as_posix()};assert all(checks.values())
log=dict(outcome='pass',scope='五篇已通过check_report；本日志另核对索引链接、联合清单/collection、既有MD哈希和逐篇复用证明，不自动证明语义或实机性能',
 topics=summaries,totals=total,unique_sources=len(names),archive_status=run['summary'],dedup_network_requests=0,unchanged_reports=unchanged,
 index_file=index.as_posix(),index_sha256=sha(index),index_local_link_checks=len(checks)+1,collection_sha256=sha(A/'02_software_depth/collection.json'),manifest_sha256=sha(mf),
 semantic_review='五篇按原文/API/配置或源码核验机制、版本和测量条件，未把分析风险说成已实测缺陷；目录导航和失败候选不引用；所有图在对应专题完成时逐幅打开。',
 pending_evidence='详见索引第5节及各专题；完整产品交付、时延/功率/闭环与许可证对象仍需额外证据')
self_log.write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf8');assert all(pathlib.Path(p).exists() for p in paths if not p.startswith(('https://','http://','#')))
pf=P/'research_state/progress.json';p=json.loads(pf.read_text(encoding='utf8'));assert p['software_depth_topics']['completed']==[s for s,t in T]
for s,u in summaries.items():assert p['software_depth_topics']['summaries'][s]['report_sha256']==u['report_sha256']
p['scope']='AMD具身智能软硬件平台01—09逐章；01已审阅，02原稿与02A—02E补深完成待审，03未开始'
p['review_status']='02_software_depth_awaiting_review';p['current_dimension']='02_Software_Stack'
p['next_step']='用户审阅02_Topics_Index及02A—02E，依据审阅意见修订；通过后按授权顺序继续03，当前不启动03。'
p['software_depth_topics'].update(review_status='awaiting_user_review',index=index.as_posix(),combined_manifest=mf.as_posix(),collection=(A/'02_software_depth').as_posix(),totals=total,unique_sources=len(names),archive_status=run['summary'],dedup_network_requests=0)
p['qa_files']=list(dict.fromkeys(p['qa_files']+[str(Q/'02_software_depth_all_dedup_last_run.json'),str(Q/'02_software_depth_all_review.json')]))
p['pending_evidence']=list(dict.fromkeys(p['pending_evidence']+['KRS历史感知benchmark完整commit/输入与采样、P99/功率未取得；源码ros2快照不等同测试commit', 'KRS stream固定尺寸、producer/consumer触发/标定/丢帧及异常恢复需完整连接实现和板端验证；仅提出可检验风险', 'ROS2 Lyrical rosidl::Buffer与KRS1.0/Humble发行边界；未取得新AMD平台相应backend统一交付证据']))
pf.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:log[k] for k in ['outcome','totals','unique_sources','dedup_network_requests','index_local_link_checks','unchanged_reports']},ensure_ascii=False,indent=2))
