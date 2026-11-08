import fs from 'node:fs/promises';

const FONT = 'Microsoft YaHei';
const C = { ink:'#142D4E', body:'#23374F', accent:'#167C92', muted:'#617084', pale:'#EDF3F7', white:'#FFFFFF', border:'#D8E1E8' };

function text(slide, name, value, x, y, w, h, size=25, bold=false, color=C.body, alignment='left') {
  const box = slide.shapes.add({geometry:'textbox', name, position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  box.text=value;
  box.text.style={typeface:FONT,fontSize:size,bold,color,alignment,verticalAlignment:'middle',autoFit:'none',wrap:'square',insets:0};
  return box;
}

function base(presentation, title, subtitle) {
  const slide=presentation.slides.add({width:1280,height:720,background:{fill:C.white}});
  text(slide,'title',title,54,38,1172,64,45,true,C.ink);
  text(slide,'subtitle',subtitle,56,111,1168,48,26,false,C.muted);
  return slide;
}

function table(slide, values, widths, x,y,w,h,heights,size=24) {
  const t=slide.tables.add({rows:values.length,columns:widths.length,left:x,top:y,width:w,height:h,columnWidths:widths,values});
  t.styleOptions={headerRow:false,bandedRows:false};
  t.borders.assign({style:'solid',fill:C.border,width:0.8});
  for(let r=0;r<values.length;r++) {
    t.rows[r].height=heights[r];
    for(let c=0;c<widths.length;c++) {
      const cell=t.getCell(r,c);
      cell.fill=r===0?C.ink:(r%2===1?C.white:C.pale);
      cell.text.style={typeface:FONT,fontSize:size,bold:r===0||c===0,color:r===0?C.white:C.body,alignment:'left',verticalAlignment:'middle'};
    }
  }
  t.cells.block({row:0,column:0,rowCount:values.length,columnCount:widths.length}).assign({margins:{left:12,right:12,top:8,bottom:8}});
  return t;
}

async function photo(slide, relative, x,y,w,h,alt) {
  const bytes=await fs.readFile(new URL(relative,import.meta.url));
  return slide.images.add({dataUrl:'data:image/png;base64,'+bytes.toString('base64'),contentType:'image/png',alt,fit:'contain',position:{left:x,top:y,width:w,height:h}});
}

function notes(slide, explanation, sources) {
  slide.speakerNotes.text=explanation+'\n\n资料截止：2026-11-08（Asia/Shanghai）。\n\n来源：\n'+sources.join('\n');
}

export function addComparisonTable(slide) {
  return table(slide,[
    ['代表方案','软件与开放边界','公开成本口径','适用任务与限制'],
    ['SO-101 + LeRobot','主从示教与训练工具\n顶层仓库 Apache 2.0','US$259 / 299\n未装配 / 装配套件','轻物体桌面拿放\n载荷与寿命待实测'],
    ['OpenArm','七自由度机械臂与 ROS2\n硬件 CERN-OHL-S v2','US$6,500 起*\nV2目录参考价','双臂接触与科研评估\n硬件、驱动版本需锁定'],
    ['ALOHA /\nMobile ALOHA','双臂示教与 ACT\nALOHA采集代码 MIT','约 US$20k / 32k\n2023 / 2024平台预算','双臂及移动学习复现\n体积、同步与数据门槛'],
  ],[220,344,276,328],56,332,1168,290,[50,80,80,80],23);
}

export async function buildSummary(presentation) {
  if(presentation.slides.items.length) throw new Error('The summary builder requires an empty presentation.');
  const s1=base(presentation,'开源具身智能方案全景','研究路线覆盖桌面学习、双臂移动操作与人形运动控制');
  table(s1,[
    ['研究路线','代表候选','主要用途'],
    ['桌面学习与交互','LeRobot / SO-101\nReachy Mini','示教、数据采集与训练\nMini偏桌面交互应用'],
    ['双臂与移动操作','OpenArm、ALOHA / Mobile ALOHA\nReachy 2、XLeRobot','双臂模仿学习与接触操作\n移动平台扩展工作空间'],
    ['人形运动与操作','Berkeley Humanoid Lite、ToddlerBot\nAgiBot X1、OpenLoong','步态与全身控制\n运动和操作协同研究'],
  ],[160,402,316],56,187,878,386,[54,104,114,114],23);
  const bhlPhoto=await photo(s1,'../26_Berkeley_Humanoid_Lite/assets/figures/01_official.png',957,202,271,301,'Berkeley Humanoid Lite 官方本体照片，裁取原图左侧实物');
  bhlPhoto.crop={left:0.02,top:0.04,right:0.6,bottom:0.03};
  text(s1,'photo-label','Berkeley Humanoid Lite\n官方本体照片（裁剪）',957,514,271,59,23,false,C.muted,'center');
  text(s1,'open-scope','开放范围需分别核对硬件、代码、固件、权重、数据和仿真资产',56,597,1170,38,27,true,C.accent);
  text(s1,'footnote','资料截止2026-11-08。已有3项首轮报告，另7项为候选资料，尚未完成同条件性能比较。',56,660,1168,28,20,false,C.muted);
  notes(s1,'本页为研究范围分类，不是产品成熟度或性能排名。LeRobot/SO-101、OpenArm、ALOHA/Mobile ALOHA已有产品级首轮报告，其余7项仅登记候选资料。桌面交互与操作型机器人采用不同任务标准。候选入选不表示全供应链开源。',[
    '仓库研究范围：06_Open_Source/RESEARCH_PLAN.md',
    'LeRobot：https://github.com/huggingface/lerobot',
    'SO-101：https://github.com/TheRobotStudio/SO-ARM100',
    'OpenArm：https://openarm.dev/',
    'ALOHA：https://tonyzhaozh.github.io/aloha/',
    'Mobile ALOHA：https://mobile-aloha.github.io/',
    'Reachy 2：https://www.pollen-robotics.com/reachy/',
    'Reachy Mini：https://github.com/pollen-robotics/reachy_mini',
    'Berkeley Humanoid Lite：https://lite.berkeley-humanoid.org/',
    'ToddlerBot：https://toddlerbot.github.io/',
    'AgiBot X1：https://github.com/AgibotTech/agibot_x1_hardware',
    'OpenLoong：https://github.com/loongOpen/OpenLoong-Hardware',
    'XLeRobot：https://github.com/Vector-Wangel/XLeRobot',
    '图片：https://lite.berkeley-humanoid.org/static/berkeley-humaonid-lite-cover.png（裁取左侧实物，移除右侧CAD示意）',
  ]);

  const s2=base(presentation,'代表方案的能力与成本','低成本桌面学习、双臂接触研究、论文与移动操作复现各有侧重');
  await photo(s2,'../21_LeRobot_SO101/assets/figures/01_official.png',95,168,270,130,'SO-101 follower 官方图片');
  await photo(s2,'../22_OpenArm/assets/figures/01_official.png',478,168,299,130,'OpenArm 与 Cell 官方图片');
  await photo(s2,'../23_ALOHA_Mobile_ALOHA/assets/figures/01_official.png',906,168,230,130,'Mobile ALOHA 原动画的单帧展示');
  text(s2,'image-captions','SO-101',103,296,256,27,21,false,C.muted,'center');
  text(s2,'openarm-caption','OpenArm 与 Cell',490,296,275,27,21,false,C.muted,'center');
  text(s2,'aloha-caption','Mobile ALOHA 演示帧',887,296,267,27,21,false,C.muted,'center');
  addComparisonTable(s2);
  text(s2,'price-boundaries','SO-101套件含示教臂、执行臂和1相机，电脑及训练等另计。*OpenArm具体配置以目录为准，Cell/KER另计。',56,632,1168,25,19,false,C.muted);
  text(s2,'historical-cost','ALOHA金额为历史平台预算，不能视为当前整机报价。资料截止2026-11-08。',56,664,1168,25,19,false,C.muted);
  notes(s2,'SO-101的US$259/299分别对应WowRobo未装配/装配套件，均包含leader、follower和1相机，未包含电脑、训练资源及运输税费，库存未独立确认。LeRobot与SO101硬件仓库的顶层LICENSE为Apache 2.0，不能扩展到全部固件、权重和数据。OpenArm采购目录更新于2026-11-02，WowRobo V2参考列价US$6,500，README称完整双臂系统US$6,500，而目录脚注按一个标准单位说明，实际左右臂、夹爪、相机和计算配置须向供应商确认，Cell/KER另价。OpenArm硬件CERN-OHL-S v2，ROS2代码Apache 2.0。ALOHA US$20k为2023平台预算，Mobile ALOHA US$32k为2024论文预算并包含机载电源和计算，底盘费用不重复相加。Mobile图片为GIF第17帧，不能代表完整运动质量。',[
    'SO101报告：06_Open_Source/21_LeRobot_SO101/01_Product_Research.md',
    'OpenArm报告：06_Open_Source/22_OpenArm/01_Product_Research.md',
    'ALOHA报告：06_Open_Source/23_ALOHA_Mobile_ALOHA/01_Product_Research.md',
    'SO101套件：https://shop.wowrobo.com/products/so-arm101-diy-kit-assembled-version-1',
    'SO101硬件及许可：https://github.com/TheRobotStudio/SO-ARM100',
    'LeRobot许可：https://github.com/huggingface/lerobot/blob/main/LICENSE',
    'OpenArm采购目录：https://docs.openarm.dev/purchase',
    'OpenArm硬件许可：https://github.com/enactic/openarm_hardware/blob/main/LICENSE.txt',
    'ALOHA：https://tonyzhaozh.github.io/aloha/',
    'ALOHA采集代码许可：https://github.com/tonyzhaozh/aloha/blob/main/LICENSE',
    'Mobile ALOHA论文：https://arxiv.org/pdf/2401.02117',
    'SO101图片：https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/main/media/SO101_Follower.webp',
    'OpenArm图片：https://raw.githubusercontent.com/enactic/openarm/main/website/static/img/hardware/openarm_and_cell.png',
    'Mobile ALOHA图片：https://mobile-aloha.github.io/static/images/preview.gif',
  ]);

  const s3=base(presentation,'任务、许可与工程投入决定选型','先建立可复现的任务闭环，再扩展本体、模型或应用场景');
  table(s3,[
    ['任务需求','优先候选','首轮验证重点'],
    ['低预算教学\n桌面操作','SO-101 + LeRobot','标定与采集闭环\n相机布局、独立测试集'],
    ['双臂接触\n标准化评估','OpenArm','硬件与驱动版本\n末端工具、接触反馈'],
    ['论文复现\n移动操作','ALOHA / Mobile ALOHA','多臂与底盘时间同步\n场景耦合、任务数据'],
  ],[179,228,379],56,191,786,354,[54,100,100,100],24);
  text(s3,'total-cost-heading','项目总成本应覆盖',884,191,340,45,28,true,C.ink);
  text(s3,'total-cost-body','本体、相机与主机\n训练算力、装配和标定\n维护、备件及运输税费',884,246,340,115,25,false,C.body);
  text(s3,'license-heading','商用前分层核对许可',884,399,340,45,28,true,C.ink);
  text(s3,'license-body','CAD、代码、固件、权重、\n数据及仿真资产分别确认。',884,456,340,89,25,false,C.body);
  text(s3,'poc-step','建议从一个受控拿放任务起步，记录真实成功次数、人工复位与连续运行表现',56,585,1168,74,28,true,C.accent);
  text(s3,'footnote','以上为研究选型建议。尚未开展实机验收，完整许可、供应商配置与当前报价仍需逐项核验。',56,669,1168,25,20,false,C.muted);
  notes(s3,'本页给出基于首轮报告的分析建议，不是采购承诺、性能排名或实机验收结论。测试应分开示范与独立测试集，并保持相机、本体、对象、初始状态和策略配置可追溯。策略推理、控制与伺服频率分别记录。开源降低早期试错门槛，但装配标定、数据质量、持续运行和维护仍需工程投入。人形候选尚未完成独立产品报告，不在本页给出采购推荐。',[
    '研究问题与边界：06_Open_Source/RESEARCH_PLAN.md',
    'SO101：https://huggingface.co/docs/lerobot/so101',
    'OpenArm：https://docs.openarm.dev/purchase',
    'ALOHA：https://github.com/tonyzhaozh/aloha',
    'Mobile ALOHA：https://arxiv.org/pdf/2401.02117',
  ]);
  return {slideCount:presentation.slides.items.length,font:FONT,slides:presentation.slides.items.map(slide=>slide.id)};
}
