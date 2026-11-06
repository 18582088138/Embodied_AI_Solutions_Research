import pathlib,json,hashlib
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1];N=P.parent/'01_NVIDIA';R=json.loads((N/'reference_metrial/_registry/materials.json').read_text(encoding='utf-8'))
sid='NVIDIA_Isaac_ROS_Buffer_Migration';r=R[sid];f=pathlib.Path(r['original_file']);assert hashlib.sha256(f.read_bytes()).hexdigest()==r['original_sha256']
m=dict(url=r['url'],status=200,file=str(f),sha256=r['original_sha256'],headers={'Content-Type':r['content_type']},final_url=r['final_url'],retrieved_at_utc=r['retrieved_at_utc'])
(D/'imports/Compare_ROS_Buffer.meta.json').write_text(json.dumps(m,ensure_ascii=False),encoding='utf-8')
