import pathlib,json,hashlib
root=pathlib.Path(__file__).resolve().parent.parent
p=root/'01_Compute_Chips/05_Rockchip'
s=p/'research_state'
for d in ['baselines','evidence']: (s/d).mkdir(parents=True,exist_ok=True)
b=s/'baselines/01_Hardware_Platform_before.json'
if not b.exists(): b.write_text(json.dumps({f.relative_to(p).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*.md')},indent=2),encoding='utf-8')
sources=[('Rockchip_Home','https://www.rock-chips.com/'),('Rockchip_RK3588','https://www.rock-chips.com/a/en/products/RK35_Series/2022/0926/1660.html'),('Radxa_ROCK5B','https://docs.radxa.com/en/rock5/rock5b'),('Firefly_Home','https://www.t-firefly.com/'),('Rockchip_Products','https://www.rock-chips.com/a/en/products/')]
m=[dict(name=n,url=u,expected='html',used_by=['01_Hardware_Platform']) for n,u in sources]
(root/'toolkit/manifests/Rockchip_01_Discovery.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
(s/'progress.json').write_text(json.dumps(dict(platform='Rockchip 瑞芯微',scope='01 硬件平台；后续02—09待01审阅通过',data_cutoff='2026-11-04 Asia/Shanghai',authorization='用户要求先完成01供审阅，通过后继续',review_status='01 in_progress; not approved',completed_dimensions=[],current_dimension='01',pending_evidence=['当前芯片系列、工业款、SOM/开发板、功耗与生命周期'],next_step='核验官方资料并归档'),ensure_ascii=False,indent=2),encoding='utf-8')
