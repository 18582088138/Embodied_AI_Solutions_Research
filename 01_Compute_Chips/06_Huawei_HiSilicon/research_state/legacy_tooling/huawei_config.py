import pathlib,json,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];P=ROOT/'01_Compute_Chips/06_Huawei_HiSilicon'
stem=sys.argv[1];raw=json.loads((ROOT/'toolkit/drafts'/(stem+'_notes.json')).read_text('utf8'))
for c in raw['claims']:
 c.setdefault('evidence_type','官方事实与条件分析');c.setdefault('conditions','按2026-11-05采集快照及正文限定版本');c.setdefault('finding','支持所述接口/流程，不证明跨SKU性能或商业收益')
raw.setdefault('versions',{});raw['versions']['CloudRobo_ProductPDF']='文档01，2026-11-02；完整20页PDF'
raw.setdefault('figures',[])
registry=json.loads((P/'reference_metrial/_registry/materials.json').read_text('utf8'))
for fig in raw['figures']:
 for asset in registry[fig['source_id']].get('assets',[]):
  if fig.get('source_url')==asset['url']:
   fig['original_file']=(P/'reference_metrial'/asset.get('local_file',asset['file'])).as_posix()
if raw.pop('cloud_figure',False):
 raw['figures'].append({'source_id':'CloudRobo_ProductPDF','file':(P/'reference_metrial/derived/figures/04_cloudrobo_architecture.png').as_posix(),'caption':'CloudRobo官方产品架构（PDF物理第5页）','operation':'2026-11-02 PDF物理第5页110dpi完整渲染；已逐图打开检查，文字完整'})
raw.setdefault('manual_review',{'coverage':raw.pop('coverage','对应章主题、机制及公开证据缺口详见正文'),'versions_and_measurements':'旧200DK/DV300、当前A2/海思产品与CloudRobo云侧严格分开；未运行硬件，未以功能界面代替benchmark','maturity_and_licenses':'代码、权重、数据、资产、本体SDK、商业云合同分别记录，未取得项不授予许可','figures_opened':'复用本轮已实际打开的官方CloudRobo完整架构页，或02/03已核验原图；不足以证明性能'})
(ROOT/'toolkit/manifests'/('Huawei_'+stem+'_config.json')).write_text(json.dumps(raw,ensure_ascii=False,indent=2),encoding='utf8')
