import sys,pathlib,json
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from curation import inputs,figure,figure_file,records,P
stem='06_Robot_Integration'
rows=[]
def a(s,n,c,l='正文',t='事实',k='具体版本见正文',f='不推广到未测平台、任务或商业状态'):rows.append((s,n,c,l,t,k,f))
a('AMD_Robotics','Case Studies','官方总页是案例入口')
for n,c,l in [('MI300X','单GPU训练平台','Hardware and Software'),('MI355X','另一单GPU平台','Hardware and Software'),('ROCm implementation','Warp实现为案例补丁','Hardware and Software'),('0.25 m','pick-hold目标','Environment Details'),('orientation-aware caging','奖励随腕方向适配','Environment Details'),('six joint-angle deltas','正文七维动作','action space'),('commanded and actual joints','观测含指令差','observation space'),('gravity compensation','模拟固件重力补偿','Sim2Real Techniques'),('actuation delay','API延迟建模随机化','Sim2Real Techniques'),('two cameras','双相机','Perception and Camera'),('about 4 mm residual','标定拟合残差','Perception and Camera'),('fixed upright orientation','非完整6DoF视觉','Perception and Camera'),('HSV','传统色彩检测','Perception and Camera'),('confidence-weighted average','置信度融合','Perception and Camera'),('PR 15074','librealsense ROCm构建链接','Perception and Camera'),('queried at 40 Hz','策略调用频率','Policy Controller Architecture'),('small multilayer perceptron','MLP非VLA','Policy Controller Architecture'),('AMD Ryzen AI 300','端侧产品家族','Policy Controller Architecture'),('zero-shot sim-to-real','作者迁移宣称','Summary')]:a('AMD06_XArm_Sim2Real',n,c,l,'厂商宣称' if 'zero-shot' in n else '事实','2026-09-29、特定XArm6任务','与图动作7+1冲突保留；没有成功分母、provider或P99，zero-shot并非无需真机标定')
for n,c in [('Koch','leader/follower本体'),('MI200','微调平台'),('Phoenix','端侧iGPU'),('50 trajectories','示范数量'),('fps=15','记录配置15fps'),('koch_follower','执行设备'),('3-billion-parameter','π0约3B')]:a('AMD04_LeRobot_Blog',n,c,'LeRobot workflow','事实','2025-07-14','15fps非servo或P99；不推跨本体泛化')
a('AMD06_XArm_JAX','8-dimensional action space','XArm7仿真八维动作','Training Code','事实','2026-03-31','不能填补XArm6维数冲突')
a('AMD06_XArm_SDK','is_radian=False','SDK角度单位配置','README','事实','当前master快照','冻结SDK/固件；不推参数范围')
a('AMD06_XArm_SDK','arm.emergency_stop()','SDK列急停接口','README','事实','当前master','不当独立安全认证')
a('AMD06_XArm_License','Redistribution and use in source and binary forms','BSD3许可正文','LICENSE','事实','UFActory版权','留版权、免责声明；其他模型/资产条款不同')
a('AMD06_STW_PDF','up to 8 configurable cameras','STW最多八相机','p1','厂商宣称','HPX.ai-vision','设备能力非SoC原生路数')
a('AMD06_STW_PDF','as long as there’s a driver','STW当前辅助驾驶定位','p2','事实','2025版权','未来自主不当已交付无人机队')
a('AMD06_STW_PDF','-40°C','环境需求','p1','厂商宣称','HPX.ai-vision需求','非逐温测量或安全证书')
a('AMD06_Solectrix_PDF','four GMSL2 cameras','SXVPU四相机','p1','事实','2024版权','有外部器件不套Kria原生接口')
a('AMD06_Solectrix_PDF','better than 10 TOPS','设备加速器能效','p2','厂商宣称','SXVPU含额外加速器','缺precision/功率边界，非Kria芯片实测')
a('AMD06_Solectrix_PDF','less than 10 milliseconds','streaming时延','p2','厂商宣称','客户基准','缺P99/完整链，不当制动时延')
a('AMD06_Solectrix_PDF','not initially built-in','雷达等扩展非内建','p2','事实','SXVPU','扩展需单独核')
a('AMD06_Robotec_PDF','ultimately built a demo','Robotec HIL原型成熟度','p2','事实','2025版权','不是量产本体名单')
a('AMD06_Robotec_PDF','not been independently verified by AMD','ROI/性能未独立核验','p2脚注','事实','Robotec宣称','不生成量化收益')
a('AMD06_Robotec_Case','Read Case Study','公开PDF入口','案例页','事实','公开网页','原PDF p2水印如实保留')
a('AMD06_GB_Factory_PR','on board GENE.01','AMD onboard声明','Key Highlights','厂商宣称','2026-10-21','精确芯片未知')
a('AMD06_GB_Factory_PR','operational by Q4 2027','工厂计划时间','Key Highlights','厂商宣称','5000平方米/三设施规划','不是现有在岗机队')
a('AMD06_GB_Factory_PR','€70 million','种子轮总融资','About','事实','AMDVentures参与','不是AMD合同/订单金额')
inputs(stem,'06_robot',rows,dict(coverage='具体XArm6/Koch独立研究感知/训练/执行；XArm7仿真、STW/SXVPU周边、RoSi HIL和GENE.01计划成熟度分别研究。',versions_and_measurements='原图7+1与XArm6正文6+1冲突；40Hz非servo，4mm是外参残差；10ms/TOPS/W为外部加速器整机客户宣称。',maturity_and_licenses='已演示、产品采用、HIL、未来计划分开；SDK BSD3正文核对；未取得补丁ZIP、完整API和GB门户原件；不采用失败页。',figures_opened='实际打开XArm6训练/真机/感知/控制四原图；三客户PDF相关页已渲染放大打开，确认脚注与水印；正文选4张。'))
for slug,m in [('vision','vision_pipeline.png'),('controller','controller_pipeline.png'),('real','real.jpg')]:figure('06',slug,'AMD06_XArm_Sim2Real',m,True)
s='AMD06_STW_PDF';o=P/'reference_metrial/derived/figures/source_AMD06_STW_PDF_p1.png';figure_file('06','stw',s,o,records()[s]['url'],'官方PDF第1页，Poppler PNG完整页渲染scale-to1800，未裁剪，已实际打开')
d=pathlib.Path(__file__).parent
fp=d/'figures.json';fs=json.loads(fp.read_text(encoding='utf8'))
for f in fs:
 if f['slug']=='stw':f['original_file']=records()[s]['file'];f['original_sha256']=records()[s]['sha256']
fp.write_text(json.dumps(fs,ensure_ascii=False,indent=2),encoding='utf8')
meta={s:dict(title=s.replace('AMD06_','').replace('_',' '),version=('2026-09-29' if s=='AMD06_XArm_Sim2Real' else '2026-10-21厂商新闻稿' if s=='AMD06_GB_Factory_PR' else '2024版权' if s=='AMD06_Solectrix_PDF' else '2025版权' if s.endswith('_PDF') else '官方公开快照；日期/版本条件见正文')) for s,*_ in rows}
(d/'source_meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
