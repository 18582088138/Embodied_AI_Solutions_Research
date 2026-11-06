import pathlib,json,hashlib,shutil,subprocess,re,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1];P=ROOT/'01_Compute_Chips/06_Huawei_HiSilicon'
R=json.loads((P/'reference_metrial/_registry/materials.json').read_text('utf8'))
old='源码固定到 URL 中的提交 SHA，代表该快照，不保证所有发行包包含相同实现。'
new='URL带提交SHA或tag的源码限定对应版本；main/master及模型卡仅为采集快照，未锁不可变revision。'
changes=[]
for p in sorted(P.glob('*.md')):
    if p.name in ['01_Hardware_Platform.md','08_Proprietary_Technologies.md','02_Topics_Index.md']: continue
    body=p.read_text('utf8'); amended=body
    # Only reports using non-SHA references need the formerly inaccurate blanket fixed-SHA wording corrected.
    e=P/'research_state/evidence'/(p.stem+'.json')
    if not e.exists(): continue
    trace=json.loads(e.read_text('utf8'))
    moving=[n for n in trace['source_ids'] if re.search(r'/(?:raw/)?(?:main|master)/',R[n]['url'])]
    tags=[n for n in trace['source_ids'] if '/v0.5.1/' in R[n]['url']]
    if moving or tags: amended=amended.replace(old,new)
    for n in moving:
        lines=amended.splitlines()
        for i,line in enumerate(lines):
            if line.startswith('| '+n+' |'): lines[i]=line.replace('固定提交源码/许可快照；确切 SHA 见原文 URL','main/master采集快照，未锁提交SHA')
        amended='\n'.join(lines)+'\n'
    for n in tags:
        lines=amended.splitlines()
        for i,line in enumerate(lines):
            if line.startswith('| '+n+' |'): lines[i]=line.replace('固定提交源码/许可快照；确切 SHA 见原文 URL','固定v0.5.1 tag；未锁提交SHA')
        amended='\n'.join(lines)+'\n'
    if body==amended: continue
    folder=P/'research_state/revisions/reference_versions'/p.stem;folder.mkdir(parents=True,exist_ok=True)
    baseline=folder/'before.json'
    assert not baseline.exists()
    baseline.write_text(json.dumps({f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in P.glob('*.md')},indent=2),encoding='utf8')
    shutil.copy2(p,folder/p.name)
    p.write_text(amended,encoding='utf8')
    subprocess.run(['python',str(ROOT/'toolkit/check_report.py'),'--project',str(P),'--report',p.name,'--baseline',str(baseline)],check=True,stdout=subprocess.DEVNULL)
    subprocess.run(['python',str(ROOT/'toolkit/download_materials.py'),'--project',str(P),'--manifest',str(ROOT/'toolkit/manifests'/('Huawei_'+p.stem+'.json')),'--dimension',p.stem],check=True,stdout=subprocess.DEVNULL)
    run=P/'reference_metrial/_registry/last_run.json'
    stats=json.loads(run.read_text('utf8'));assert stats['network_requests_including_robots']==0
    shutil.copy2(run,P/'reference_metrial/derived/qa'/(p.stem+'_dedup.json'))
    changes.append({'report':p.name,'moving_source_ids':moving,'tag_source_ids':tags,'baseline':baseline.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'quality':'pass','network_requests':0})
    print(p.name,'reference versions corrected; pass; zero requests',flush=True)
(P/'research_state/revisions/reference_versions_audit.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'purpose':'Correct citation wording for moving branches and tags only; no change to01 or archived sources','changes':changes},ensure_ascii=False,indent=2),encoding='utf8')
