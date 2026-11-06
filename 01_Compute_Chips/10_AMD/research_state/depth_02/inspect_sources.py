import json,pathlib,sys,re
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1]
R=json.loads((P/'reference_metrial/_registry/materials.json').read_text(encoding='utf-8'))
if sys.argv[1]=='list':
 for s,r in R.items():
  if re.search(sys.argv[2],s,re.I):print(s,r.get('archive_status'),r.get('url'))
else:
 for s in sys.argv[1:]:
  r=R[s];p=pathlib.Path(r['file']).parent/'text.txt'
  print('\nSOURCE',s,r.get('archive_status'),'\n',p.read_text(encoding='utf-8') if p.exists() else 'NO text')
