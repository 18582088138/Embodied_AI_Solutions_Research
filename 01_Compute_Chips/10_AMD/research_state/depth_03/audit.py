import json,pathlib,re,sys
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1];R=json.loads((P/'reference_metrial/_registry/materials.json').read_text(encoding='utf8'))
if sys.argv[1]=='quality':
 f=P/'reference_metrial/derived/qa/03_Sensor_Integration_quality.json';q=json.loads(f.read_text(encoding='utf8'));print(json.dumps(q,ensure_ascii=False,indent=2))
elif sys.argv[1]=='claims':
 e=json.loads((P/'research_state/evidence/03_Sensor_Integration.json').read_text(encoding='utf8'))
 for c in e['claim_review']:
  if any(re.search(x,c['source_id']) for x in sys.argv[2:]):print(c['source_id'],c['claim'],c['context_quote'])
elif sys.argv[1]=='search':
 for s,r in R.items():
  if not re.search(sys.argv[2],s):continue
  tfile=pathlib.Path(r.get('file','')).parent/'text.txt'
  if not tfile.exists():continue
  t=re.sub(r'\s+',' ',tfile.read_text(encoding='utf8'))
  for m in re.finditer(sys.argv[3],t,re.I):print(s,t[max(0,m.start()-120):m.end()+450])
elif sys.argv[1]=='assets':
 for s in sys.argv[2:]:
  for a in R[s]['assets']:
   if '_images/' in a['url']:print(s,a['url'],(P/'reference_metrial'/a.get('local_file',a['file'])).as_posix())
