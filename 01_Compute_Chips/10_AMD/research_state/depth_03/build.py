"""Offline builder scoped exclusively to chapter 03; no existing report/registry mutation."""
import json,pathlib,re,hashlib,collections
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1];A=P/'reference_metrial';stem='03_Sensor_Integration'
R=json.loads((A/'_registry/materials.json').read_text(encoding='utf8'))
B=(D/(stem+'.txt')).read_text(encoding='utf8').replace('@@ROOT@@',P.as_posix())
ids=list(dict.fromkeys(re.findall(r'@@(?!FIG:)(\w+)@@',B)));nums={s:f'S{i:02}' for i,s in enumerate(ids,1)}
C={}
for path in [P/'research_state/source_catalog_01.json',P/'research_state/source_catalog_02.json']:
 if path.exists():
  for c in json.loads(path.read_text(encoding='utf8')):C[c['source_id']]=c
titles={
 'AMD_MV_Overview':'KR260机器视觉总览','AMD_MV_Intro':'机器视觉输入、输出与系统依赖','AMD_MV_HW':'SLVS/ISP/10GigE硬件架构','AMD_MV_ISP':'缺陷检测加速与资源表','AMD_MV_SW':'机器视觉驱动与控制面','AMD_MV_Deploy':'机器视觉部署与性能条件','AMD_MV_Issues':'机器视觉已知问题与许可','AMD_MV_Sensor':'IMX547模块、位深和接口',
 'AMD_IMX547_Color':'IMX547 color产品页','AMD_IMX547_Mono':'IMX547 mono产品页',
 'AMD_CSI2_Driver':'linux-xlnx CSI2 Rx driver','AMD_Video_DMA_Driver':'linux-xlnx视频DMA部分源码',
 'AMD_IMX547_Readme':'IMX547 sensor module README','AMD_IMX547_License':'sensor module GPLv2文本','AMD_ISP_Readme':'ISP driver README/SPDX','AMD_ISP_License':'ISP module GPLv2文本',
 'AMD_PTP_HW':'GPS/PPS硬件架构','AMD_PTP_SW':'GPS/PTP软件架构','AMD_PTP_Deploy':'GPS/PTP部署与chrony日志',
 'AMD_TSN_Intro':'TSN v0.3定位与发行','AMD_TSN_HW':'TSN/RS485/CAN硬件架构','AMD_TSN_SW':'TSN ROS/VLAN及设备驱动','AMD_TSN_Deploy':'TSN部署与测量端点',
 'Linux_V4L2_Buffer':'V4L2 buffer与timestamp flags','Linux_V4L2_MMAP':'V4L2 MMAP接口','Linux_V4L2_DMABUF':'V4L2 DMA-BUF importer','Linux_V4L2_Export':'V4L2 EXPBUF export','Linux_DMABUF_Sync':'DMA-BUF同步与缓存访问','Linux_IIO_Buffer':'Linux IIO buffered数据布局','Linux_PTP':'Linux PHC API','Linux_Network_Timestamps':'Linux网络时间戳','Linux_SocketCAN':'Linux SocketCAN API',
 'Compare_03_HSB':'NVIDIA HSB2.7架构','Compare_03_CoE':'Jetson Thor SIPL CoE接收架构'}
def ver(s):
 if s.startswith('AMD_MV_'):return 'KR260文档家族2022.1；页面更新2026-08-13；部署测试组件见正文'
 if s.startswith('AMD_PTP_'):return 'KR260 GPS/PTP旧版Ubuntu参考例；2023日志；页面更新2026-08-13'
 if s.startswith('AMD_TSN_'):return 'TSN教程v0.3；EDF26.06/Jazzy；更新2026-10-23'
 if s.startswith('Linux_'):return 'kernel.org通用API文档2026-11-04快照；非AMD BSP绑定版本'
 if s in ['AMD_CSI2_Driver','AMD_Video_DMA_Driver']:return 'linux-xlnx master 2026-11-04浮动快照；DMA页面仅取得部分源码'
 if s.startswith('AMD_IMX547_') and s not in ['AMD_IMX547_Color','AMD_IMX547_Mono'] or s.startswith('AMD_ISP_'):return 'GitHub main 2026-11-04快照；README/LICENSE，非完整交付包审核'
 if s=='Compare_03_HSB':return 'HSB2.7；2026-11-03原响应导入复用，仅机制对标'
 if s=='Compare_03_CoE':return 'Jetson r39.2.1 CoE；页面更新2026-08-12；2026-11-03原响应导入'
 if s in C:return C[s]['version']
 return '2026-11-04公开快照；未取得明确发布日，适用范围见正文'
catalog=[]
for s in ids:
 r=R[s];assert r.get('status')==200 and r['archive_status'] in ('complete_static','partial_static'),s
 title=titles.get(s,C.get(s,{}).get('title',s));B=B.replace('@@'+s+'@@',f'[{nums[s]} {title}]({r["url"]})')
 catalog.append(dict(source_id=s,number=nums[s],title=title,version=ver(s),url=r['url'],file=pathlib.Path(r['file']).as_posix(),sha256=r['sha256'],original_file=pathlib.Path(r['original_file']).as_posix(),original_sha256=r['original_sha256'],metadata_file=(pathlib.Path(r['file']).parent/'metadata.json').as_posix(),collected_at=r.get('retrieved_at_utc'),archive_status=r['archive_status'],missing_dependencies=r.get('unavailable_assets',{}),unavailable_presentation_assets=r.get('unavailable_presentation_assets',[]),notes=r.get('notes',[])))
F={f['slug']:f for f in json.loads((D/'figures.json').read_text(encoding='utf8'))};figs=[]
for fid in list(dict.fromkeys(re.findall(r'@@FIG:(\w+)@@',B))):
 f={k:v for k,v in F[fid].items() if k!='slug'};assert f['source_id'] in ids
 for key,hkey in [('file','sha256'),('original_file','original_sha256')]:assert hashlib.sha256(pathlib.Path(f[key]).read_bytes()).hexdigest()==f[hkey]
 f['manual_open_review']='2026-11-04逐张调用view_image实际打开：文字、箭头、图例完整，无空白/截断；MV两图IMX574误标与正文IMX547冲突已在图注保留。'
 figs.append(f);B=B.replace('@@FIG:'+fid+'@@',f['file'])
B=re.sub(r'\]\( (C:/[^\n]*?) \)',r'](\1)',B);assert '@@' not in B
reviews=json.loads((D/'reviews.json').read_text(encoding='utf8'));claims=[];errors=[]
for c0 in reviews:
 c=c0.copy();s=c['source_id'];assert s in ids
 t=re.sub(r'\s+',' ',(pathlib.Path(R[s]['file']).parent/'text.txt').read_text(encoding='utf8'));needle=c.pop('needle');m=re.search(re.escape(re.sub(r'\s+',' ',needle)),t,re.I)
 if not m:errors.append([s,needle]);continue
 c.update(exact_quote=t[m.start():m.end()],context_quote=t[max(0,m.start()-100):m.end()+600],source_url=R[s]['url'],material_version=ver(s),collected_at=R[s].get('retrieved_at_utc'),quote_basis='归档text.txt空白规整的精确短引与上下文；人工对照章节/API/原表，匹配不替代语义核验')
 claims.append(c)
if errors:print(json.dumps(dict(missing_quotes=errors),ensure_ascii=False));raise SystemExit(2)
trace=dict(source_ids=ids,figures=figs,claim_review=claims,manual_review=dict(coverage='03全部维度：sensor与PHY/桥接、真实MV/ISP/DDR/10GigE、V4L2与runtime交接、非视觉支持缺口、时间/触发/PTP/TSN、标定/融合、吞吐/age、故障/许可/机制比较及复建验证。',versions_and_measurements='逐项对照归档API/部署/表格；产品120与教程122/8bit/10bpp冲突、sensor图IMX574、color支持、软ISP、I2C及KD240描述冲突保留；分析数字独立复算。media图实际imx547逻辑节点，无CSI接收器，不根据MIPI文件名推PHY。',maturity_and_licenses='GPLv2仅sensor/ISP driver文本；第三方capture网络IP evaluation需正式许可。BSP/container未审完整SBOM，模型/资产/SDK未归因开源。未接板、安装或接受协议。',figures_opened='正文9图逐张实际view_image；全部可读，原图字节复制且哈希一致；另实际打开MV_SW media graph核对imx547/subset/ISP/capture节点；错误label保留，测量事件与接口角色详见图注。'))
sa=next(a for a in R['AMD_MV_SW']['assets'] if a['url'].endswith('/MIPI-CS-2-Media-Graphs.png'))
sap=A/sa.get('local_file',sa['file']);assert hashlib.sha256(sap.read_bytes()).hexdigest()==sa['sha256']
trace['reviewed_supplementary_assets']=[dict(source_id='AMD_MV_SW',source_url=sa['url'],original_file=sap.as_posix(),sha256=sa['sha256'],operation='只读原图；实际view_image打开核验，未嵌正文图',finding='图为imx547→subset→ISP→capture逻辑节点；文件名含MIPI不能证明CSI物理接口')]
E=P/'research_state/evidence'/(stem+'.json');E.write_text(json.dumps(trace,ensure_ascii=False,indent=2),encoding='utf8')
cp=D/(stem+'_sources.json');cp.write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf8')
appendix=['\n## 参考资料与本地原件\n','S编号与正文对应；每项保留原响应、HTML/PDF、metadata与依赖。partial_static有已取得可读正文，部分字体/样式/脚本未归档，不能保证像素/交互完整；不以HTTP200导航/JS壳或下载失败作为有效引用。NVIDIA来源采集2026-11-03，其余引用沿用2026-11-04项目快照，采集日期不等发布日期。\n','| 原始来源 | 日期/版本/条件 | 本地原件与metadata | 归档状态 |','|---|---|---|---|']
for c in catalog:appendix.append(f"| [{c['number']} {c['title']}]({c['url']}) | {c['version']} | [HTML/PDF]({c['file']}) · [metadata]({c['metadata_file']}) | {c['archive_status']} |")
appendix.append(f'\n[主张/图源及人工审阅记录]({E.as_posix()}) · [实际引用完整清单]({cp.as_posix()}) · [03专题资料索引]({(A/"03_sensors/index.html").as_posix()})。未成功候选及归档缺口另见research log；本章没有实机性能、机器人闭环或量产认证结论。')
(P/(stem+'.md')).write_text(B+'\n'.join(appendix)+'\n',encoding='utf8')
mf=P.parents[1]/'toolkit/manifests/AMD_03_Sensor_Integration_final.json';mf.write_text(json.dumps([dict(name=s,url=R[s]['url'],expected='pdf' if pathlib.Path(R[s]['file']).suffix=='.pdf' else 'html',used_by=[stem]) for s in ids],ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(body_han_chars=len(re.findall('[\u4e00-\u9fff]',B)),sources=len(ids),figures=len(figs),claims=len(claims),archive_status=collections.Counter(c['archive_status'] for c in catalog)),ensure_ascii=False))
