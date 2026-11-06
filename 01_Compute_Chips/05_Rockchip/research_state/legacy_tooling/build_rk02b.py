from rk02_report import *
body=(root/'toolkit/drafts/02B.txt').read_text(encoding='utf-8');r=json.loads((a/'_registry/materials.json').read_text(encoding='utf-8'))
ids=list(dict.fromkeys(re.findall(r'\[\[([\w]+)\]\]',body)))
figs=[]
for n in ['RK02_RKNN2_Figure','RK02_YOLO8_OutputFigure','RK02_YOLO8_GraphFigure']:
 ids.append(n);figs.append(figure(n,r[n]['file'],'官方图片原件，实际逐图打开，无裁剪',n))
claims=[claim('RK02_RKNN2_Readme','support/notes','Toolkit2 v2.5.0与旧Toolkit不兼容','master快照；未取得精确commit/发布日期','RV1126/B代际区分'),claim('RK02_YOLO8_Guide','Pretrained Model','YOLOv8优化输出契约','三尺度box/classes/sum','原始后处理不可直接套用'),claim('RK02_YOLO8_Convert','main','均值0/std255与COCO20校准','i8/u8/fp条件','未执行转换；校准不是任务精度证据'),claim('RK02_RKNN2_API','native attr/cache/async','原生内存与上一帧异步语义','size_with_stride/pass_through/frame_id','zero-copy有格式同步条件，FPS不当闭环时延'),claim('RK02_RKNN2_Changes','v2.5.0/v2.3.0','CPU/GPU算子与RK3576W4A16','具体版本/平台','不推导全图NPU或所有SKU低比特'),claim('RK02_Zoo_Readme','Model performance benchmark','76.3/97.7/83.0FPS','yolov8nINT8/640/最大NPU频率；单核按表列','不含预后处理；缺功率与统计'),claim('RK02_RKNN2_License','1.1/2','RKNN SDK专有条款','设计开发测试/Rockchip产品','不称全部Apache开源或已许可量产再分发')]
write('02B_RKNN2_Compiler_Runtime',body,ids,claims,figs,coverage='真实YOLO导出/量化/目标runtime源码链；buffer/布局/cache/async/shape/多核；非NPU后端及基准。完整新版手册和算子矩阵未取得。',licenses='SDK自有协议、Zoo Apache、YOLO源与权重/数据独立。未安装SDK与权重，量产再分发范围需核实。')
