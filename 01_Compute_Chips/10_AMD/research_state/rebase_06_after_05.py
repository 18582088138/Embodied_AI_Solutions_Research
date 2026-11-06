import pathlib,json,hashlib,datetime
P=pathlib.Path(__file__).resolve().parent.parent
b=P/'research_state/baselines/06_Robot_Integration_before.json'
old=json.loads(b.read_text(encoding='utf8'))
new={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in P.glob('*.md')}
assert {k for k in old if old[k]!=new[k]}=={'05_Simulation_Environment.md'}
(P/'research_state/baselines/06_Robot_Integration_initial_before_05_addendum.json').write_text(json.dumps(old,indent=2),encoding='utf8')
(P/'research_state/depth_06/05_addendum_log.json').write_text(json.dumps(dict(reason='06官方检索新发现2026-09特定ROCm Warp真实迁移；完成05纠正及重新QA/去重后重设06起始基线，仅05改变，01—04未变',before=old['05_Simulation_Environment.md'],after=new['05_Simulation_Environment.md']),ensure_ascii=False,indent=2),encoding='utf8')
b.write_text(json.dumps(new,indent=2),encoding='utf8')
