import pathlib,json,re,sys
P=pathlib.Path(__file__).resolve().parent.parent
R=json.loads((P/'reference_metrial/_registry/materials.json').read_text(encoding='utf8'))
s=sys.argv[1];f=pathlib.Path(R[s]['file']);t=f.parent/'text.txt'
if f.suffix=='.pdf':t=P/'reference_metrial/derived/extracted'/(s+'.txt')
t=re.sub(r'\s+',' ',(t if t.exists() else f).read_text(encoding='utf8'))
for pat in sys.argv[2:]:
 print(s,pat)
 ms=list(re.finditer(pat,t,re.I))
 for m in ms[-2:]:print(t[max(0,m.start()-120):m.end()+1100])
