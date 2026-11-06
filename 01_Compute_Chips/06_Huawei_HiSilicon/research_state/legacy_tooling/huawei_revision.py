import pathlib,json,hashlib,sys,shutil,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1]
P=ROOT/'01_Compute_Chips/06_Huawei_HiSilicon'
mode,stem=sys.argv[1:3]
folder=P/'research_state/revisions'/stem
folder.mkdir(parents=True,exist_ok=True)
if mode=='start':
    baseline=folder/'before.json'
    if baseline.exists(): raise RuntimeError('Revision baseline exists; preserve it')
    baseline.write_text(json.dumps({f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in P.glob('*.md')},indent=2),encoding='utf8')
    for f in [P/(stem+'.md'),P/'research_state/evidence'/(stem+'.json'),P/'reference_metrial/derived/qa'/(stem+'_quality.json'),ROOT/'toolkit/manifests'/('Huawei_'+stem+'_config.json')]:
        if f.exists(): shutil.copy2(f,folder/('before_'+f.name))
elif mode=='finish':
    q=json.loads((P/'reference_metrial/derived/qa'/(stem+'_quality.json')).read_text('utf8'))
    assert q['outcome']=='pass'
    shutil.copy2(P/'reference_metrial/_registry/last_run.json',P/'reference_metrial/derived/qa'/(stem+'_dedup.json'))
    (folder/'revision.json').write_text(json.dumps({'reason':sys.argv[3],'after_sha256':hashlib.sha256((P/(stem+'.md')).read_bytes()).hexdigest(),'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline':(folder/'before.json').as_posix(),'outcome':q['outcome']},ensure_ascii=False,indent=2),encoding='utf8')
print(mode,stem)
