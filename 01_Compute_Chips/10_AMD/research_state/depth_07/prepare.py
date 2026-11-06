import sys,pathlib,json,hashlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from curation import inputs,figure_file,records,P
stem='07_Ecosystem';rows=[]
def a(s,n,c,l='正文',t='事实',k='具体版本/日期见正文',f='支持对象、维护责任和商业状态不相互推广'):rows.append((s,n,c,l,t,k,f))
a('AMD07_Robotics_Partners','validated robotics partners','伙伴定位','Why Work','厂商宣称',f='动态目录不完整，标签没有逐BOM/版本测试报告')
for n,c,l in [('053700','X199商业128G模块','p3'),('053710','X199i工业模块','p3'),('Product not yet released for Mass Production','预发布状态','p3脚注'),('Preliminary Revision 0.3','版本','p3脚注'),('120 x 160 mm','模块尺寸','p1'),('Intel® i226','外部网卡控制器','p1'),('PCIe switch','可选交换器','p2'),('Multi Stage Watchdog','板级监测功能','p1'),('Power Loss Control','板掉电功能','p1'),('Flash Update','BIOS升级功能','p1'),('Linux','列出的OS','p1'),('conga-zones','hypervisor','p1'),('Storage -20°C to 80°C','商业storage温度','p1'),('Operating -40°C to +85°C','工业operating','p1'),('053750','散热料号','p3'),('065620','应用载板','p3')]:a('AMD07_Congatec_CRX1_PDF',n,c,l,k='Preliminary0.3 2026-07-08',f='料号不证明现货；功能不当安全认证，TDP不当整机功率')
a('AMD07_Congatec_CRX1','Storage: -40 to +85°C','网页storage冲突','总规格',f='与PDF商业storage冲突保留，正式签版消歧')
a('AMD07_Congatec_CRX1','Ubuntu Pro','OS询价选项','ecosystem',f='选项不证明逐SKU支持订阅')
for n,c in [('hardware vendor','AMD角色'),('for any AMD Adaptive SoC product family','支持声明范围'),('Hardware product lifetime commitments do not imply software support commitments','硬件软件期限分离'),('A maintained update feed or service','EDF缺生产更新feed'),('reference Yocto Project distribution','原型参考镜像'),('source repository, not a supported OS product','linux-xlnx角色'),('Short-term critical bug and security fixes','update分支短期'),('2026.1 6.18','2026.1内核base'),('OSTree, RAUC, Mender, and swupdate','OTA layer路线'),('degree of integration in the EDF reference design may be limited','安全集成边界'),('Certified Ubuntu','Canonical路线'),('Foundries','OTA商业路线'),('create-spdx','SBOM生成')]:a('AMD_EDF_Production',n,c,'生产指南',k='EDF26.06.1-rev3 AdaptiveSoC',f='不推广全部AMD产品；路线不等于已取得合约或完整OTA')
for n,c in [('zero per-device fees','服务计费宣传'),('10+ years','长期服务宣传'),('Yocto Project 5.2','LTS25基础'),('Linux Kernel 6.12','内核基础'),('Pre-validated BSPs for AMD','BSP定位')]:a('AMD07_WindRiver_Linux',n,c,'产品正文','厂商宣称',f='不推目标载板已经验证；没有零订阅成本')
for n,c in [('SCHED_FIFO','实时调度尝试'),('fallback_controllers','降级入口'),('subject to the availability','fallback依赖接口'),('Default: false handle_exceptions','限幅默认false'),('reads states from hardware','read-update-write链')]:a('AMD07_ROS2_Control',n,c,'controller manager','事实','Jazzy当前文档',f='默认值非AMD测量，不构成安全停机认证')
a('AMD04_Ryzers_Repo','composable Dockerfiles','Ryzers定位','README')
a('AMD04_Ryzers_License','SPDX-License-Identifier: MIT','Ryzers MIT','LICENSE',f='只覆盖仓库，权重/数据/runtime另核')
a('AMD_ROSS','assistant designed to help developers','开发助手定位','Overview',f='不是现场机器人控制runtime')
a('AMD07_Distributors','updated on a quarterly basis','渠道时效','Footnotes',f='不是实时库存/价格/交期')
a('AMD07_Warranty','Tray and MPK Processors','保修分类','Warranty',f='不套用第三方模块/整机')
a('AMD06_Solectrix_PDF','not been independently verified by AMD','性能脚注','p2',f='10ms/能效客户宣称，不当闭环统计')
a('AMD06_Robotec_PDF','ultimately built a demo','HIL成熟度','p2')
a('AMD06_STW_PDF','as long as there’s a driver','辅助驾驶阶段','p2')
a('OpenNav_Robotics_Benchmark','180,000','代表仓库规模','benchmark','事实',f='计算基准非客户运营面积')
inputs(stem,'07_ecosystem',rows,dict(coverage='代表模块六料号/外部器件/载板与视觉/HIL分工、开源/开发/控制角色、OS生产维护、产测OTA与渠道保修责任深入覆盖。',versions_and_measurements='congatec PDF预发布未量产脚注和storage冲突已核；ROS参数默认值非实测；无无条件倍数、ROI和机队规模。',maturity_and_licenses='目录/选项与交付分开；MIT分对象；EDF AdaptiveSoC支持声明不推广全公司；未取得正式合同、模块完整BSP/手册、OTA失效测试。',figures_opened='congatec PDF1/2/3完整页实际打开，Solectrix PDF2实际打开；正文采用1/2和Solectrix2三图，脚注与外部器件可读。'))
for slug,s,p in [('crxspec','AMD07_Congatec_CRX1_PDF',1),('crxblock','AMD07_Congatec_CRX1_PDF',2),('sxvpu','AMD06_Solectrix_PDF',2)]:
 o=P/f'reference_metrial/derived/figures/source_{s}_p{p}.png';item=figure_file('07',slug,s,o,records()[s]['url'],f'官方PDF第{p}页，Poppler scale-to1800完整页PNG渲染，未裁剪，已实际打开')
 fp=P/'research_state/depth_07/figures.json';v=json.loads(fp.read_text(encoding='utf8'));orig=pathlib.Path(records()[s]['file'])
 for x in v:
  if x['slug']==slug:x['original_file']=orig.as_posix();x['original_sha256']=hashlib.sha256(orig.read_bytes()).hexdigest()
 fp.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
meta={s:dict(title=s,version='官方快照；准确产品/版本见正文') for s in set(x[0] for x in rows)}
meta['AMD07_Congatec_CRX1_PDF']=dict(title='congatec cRX1 datasheet',version='Preliminary0.3，2026-07-08，末页尚未量产')
meta['AMD_EDF_Production']=dict(title='EDF生产部署指南',version='26.06.1-rev3，AdaptiveSoC')
(P/'research_state/depth_07/source_meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
