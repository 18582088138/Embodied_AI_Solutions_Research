import json,pathlib,re,sys
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1];A=P/'reference_metrial'
R=json.loads((A/'_registry/materials.json').read_text(encoding='utf8'))
if sys.argv[1]=='assets':
 for s in sys.argv[2:]:
  r=R[s];print(s, list(r.keys()))
  for a in r.get('assets',[]):
   if a.get('kind')=='image' or re.search(r'\.(png|jpg|svg)',a['url'],re.I):print(json.dumps(a))
else:
 s=sys.argv[1];t=re.sub(r'\s+',' ',(pathlib.Path(R[s]['file']).parent/'text.txt').read_text(encoding='utf8'))
 for needle in sys.argv[2:]:
  print('\n',s,needle)
  for m in list(re.finditer(needle,t,re.I))[:2]:print(t[max(0,m.start()-140):m.end()+850])
