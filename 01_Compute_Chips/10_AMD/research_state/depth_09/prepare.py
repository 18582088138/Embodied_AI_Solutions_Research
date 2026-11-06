import pathlib,json,sys,hashlib,shutil
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from curation import inputs,P,records
stem='09_SWOT_Analysis';D=P/'research_state/depth_09';rows=[]
def a(s,n,c,l='正文',t='事实',k='对象和条件见正文',f='已读原文；不可推广未测SKU/任务或商业收益'):rows.append((s,n,c,l,t,k,f))
a('AMD_Robotics','Robotics','产品路线入口','solutions','事实','2026-11-04网页','目录不等市占率')
for n,c in [('40 Hz','策略调用'),('Ryzen AI 300','部署对象'),('September 29, 2026','演示日期'),('0.25','lift任务'),('ONNX','模型导出')]:a('AMD06_XArm_Sim2Real',n,c,'技术blog','事实','具体XArm6演示','provider/SKU、成功分母与P99未知')
for n,c in [('July 14, 2025','教学日期'),('MI200','训练硬件'),('integrated GPU','端侧对象'),('50 trajectories','示例数据量')]:a('AMD04_LeRobot_Blog',n,c,'技术blog','事实','Koch/π0示例','非泛化/运营成功分母')
for n,c in [('additional hardware accelerators','额外加速器'),('four GMSL2','相机对象'),('less than 10 milliseconds','streaming宣称'),('not been independently verified by AMD','收益责任'),('not initially built-in','雷达等非初始内置'),('©2024','case版权年份')]:a('AMD06_Solectrix_PDF',n,c,'p1—2','厂商宣称','SXVPU具体case','非芯片单独性能/P99/ROI')
for n,c in [('HPX','产品对象'),('©2025','版权日期')]:a('AMD06_STW_PDF',n,c,'case','事实','STW客户案例','精确chip/台数/独立ROI未知')
a('AMD06_Robotec_PDF','demo','HIL成熟度','case','事实','RoSi示例','非在岗运营证明')
for n,c in [('Q4 2027','计划投运'),('5,000-square-metre','设施面积'),('compute on board GENE.01','onboard宣称'),('planned collaboration','合作计划')]:a('AMD06_GB_Factory_PR',n,c,'PR','厂商计划','原始公告','面积不等机器人数量；准确onboard SKU/合同未知')
for n,c in [('288GB','服务器容量'),('1400W','服务器功率')]:a('AMD08_MI350_Architecture',n,c,'MI350','事实','MI355X','非移动端功耗/实测')
a('AMD08_CDNA4_Whitepaper','typically 32','低精度块数值')
for n,c in [('i226','板级组件'),('053700','具体module料号'),('Block Diagram','BOM分层')]:a('AMD07_Congatec_CRX1_PDF',n,c,'p2—3','事实','cRX1具体装配选项','非芯片原生全部接口/模型支持')
a('AMD_RyzenAI_Release','Version 1.9','发行支持边界')
a('AMD_Versal_Gen2_Brief','Shared-exponent','异构格式类别')
a('AMD_VAI_Custom_Ops','tiler','定制交付工作')
a('AMD08_IRON_Repo','complements mainstream','低层工具补充定位')
a('AMD_EDF_SHEL_XSA','SDTGen','软硬件交接')
for n,c in [('obligation for ongoing security maintenance','支持义务'),('Self-maintained','自主维护'),('SPDX','SBOM')]:a('AMD_EDF_Production',n,c,'production','事实','EDF公开指南','扫描不等持续服务/补丁验收')
a('AMD_VitisAI_Gen2_Output','.rai','跨SKU产物边界')
a('AMD_Kria_AI_Dev','Notify Me','未完成订购对象','产品页','事实','2026-11-04网页','准确料号/价格/交期未取得')
a('AMD07_WindRiver_Linux','Linux','OSV支持路径','产品页','事实','具体合同另确认','未买订阅不等有SLA')
a('AMD05_Genesis_Blog','ROCm','仿真后端路线','技术blog','事实','具体教程','非任意backend兼容')
a('AMD05_O3DE_Concepts','ROS','仿真接口路线')
for s,price,pn,lead in [('AMD_K24C','$250.00','SM-K24-XCL2GC','6 weeks'),('AMD_K24I','$350.00','SM-K24-XCL2GI','6 weeks'),('AMD_K26C','$325.00','SM-K26-XCL2GC','26 weeks'),('AMD_K26I','$450.00','SM-K26-XCL2GI','26 weeks')]:
 for n,c in [(price,'公开单项MSRP'),(pn,'准确料号'),(lead,'网页交期')]:a(s,n,c,'产品页','事实','2026-11-04采集英语页；USD MSRP','无数量阶梯/地区税/中国到货报价；网页lead time非合同')
a('AMD_K26I','Expected Product Lifetime','生命周期字段','比较表','事实','K26 variants','不等保修/供应/软件支持期')
a('AMD_Versal_Gen2_Industrial','certification targeted','安全目标','p1','厂商宣称','原始brief','非整机证书')
a('AMD07_ROS2_Control','fallback_controllers','控制器回退条件','controller manager','事实','Jazzy文档','非独立保护端点')
inputs(stem,'09_selection',rows,dict(coverage='市场/采购分母、具体case成熟度、SWOT条件、公开MSRP/交期、系统BOM/TCO敏感性、政策/许可缺口、七场景矩阵与POC至量产放行深入。',versions_and_measurements='K24/K26四料号价格/交期按采集时网页核；case年份、policy频率/预测/计划分开；成本示例是明确假设。',maturity_and_licenses='不补成功率/份额/收入/ROI；法规和财报定位失败未引用；所有正式出口/安全/维护合同待核。',figures_opened='已实际打开Solectrix case PDFp2及congatec cRX1 PDFp2完整渲染；性能责任与optional BOM标记均核查。'))
old=json.loads((P/'research_state/evidence/07_Ecosystem.json').read_text(encoding='utf8'))['figures'];figs=[]
for suffix,slug in [('sxvpu.png','swot_case'),('crxblock.png','swot_bom')]:
 v=next(x.copy() for x in old if x['file'].endswith(suffix));out=P/'reference_metrial/derived/figures/09';out.mkdir(exist_ok=True)
 f=out/(slug+'.png');shutil.copyfile(v['file'],f);v.update(slug=slug,opened=True,file=f.as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),operation=v['operation']+'；本章复制衍生图，原PDF保留并再次实际打开');figs.append(v)
(D/'figures.json').write_text(json.dumps(figs,ensure_ascii=False,indent=2),encoding='utf8')
calc={'classification':'分析敏感性；不是实测或完整TCO/ROI','energy':{'currency':'RMB','N':100,'years':3,'days_per_year':260,'hours_per_day':16,'delta_average_system_power_W':20,'electricity_RMB_per_kWh':1,'formula':'N*(W/1000)*hours_per_day*days_per_year*years*price','total_RMB':100*(20/1000)*16*260*3*1,'per_robot_RMB':(20/1000)*16*260*3*1},'migration':{'currency':'RMB','additional_hours':500,'loaded_rate_RMB_per_hour':300,'additional_NRE_RMB':500*300},'module_grade_delta':{'currency':'USD','N':100,'K26I_MSRP_USD':450,'K26C_MSRP_USD':325,'delta_USD':100*(450-325),'sources':['AMD_K26I','AMD_K26C']},'limitations':['电功率/运行时数/费率/工时均为假设','不同币种不混算，未假设汇率','不同等级模组不保证均符合环境要求','未计系统BOM、维护、税费、停机、故障/备件、业务收益；不是完整总额']}
assert round(calc['energy']['total_RMB'],2)==24960 and round(calc['energy']['per_robot_RMB'],2)==249.6 and calc['module_grade_delta']['delta_USD']==12500
(D/'tco_calculations.json').write_text(json.dumps(calc,ensure_ascii=False,indent=2),encoding='utf8')
R=records();candidates=['AMD09_IR_Annual','AMD09_IR_SEC','AMD09_EAR_742','AMD09_EU_AI_Act']
(D/'external_evidence_gaps.json').write_text(json.dumps({'attempted_sources':{s:R[s] for s in candidates},'consequence':'正文未取得，不引用数值/法规结论，不把采集失败称官方未披露。','discovery_run':json.loads((P/'reference_metrial/_registry/last_run.json').read_text(encoding='utf8'))},ensure_ascii=False,indent=2),encoding='utf8')
(D/'source_meta.json').write_text(json.dumps({'AMD06_Solectrix_PDF':{'title':'Solectrix SXVPU官方案例','version':'PID1671659，版权2024；声明非AMD独立验证'},'AMD06_STW_PDF':{'title':'STW HPX.ai-vision官方案例','version':'版权2025，已归档PDF'},'AMD07_Congatec_CRX1_PDF':{'title':'congatec cRX1 datasheet','version':'公开datasheet；装配料号/选项与正文边界核对'}},ensure_ascii=False,indent=2),encoding='utf8')
