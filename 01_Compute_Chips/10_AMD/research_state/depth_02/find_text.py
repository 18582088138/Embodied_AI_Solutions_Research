import pathlib,json,re,sys
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1]
R=json.loads((P/'reference_metrial/_registry/materials.json').read_text(encoding='utf-8'))
s=sys.argv[1];text=re.sub(r'\s+',' ',(pathlib.Path(R[s]['file']).parent/'text.txt').read_text(encoding='utf-8'))
matches=list(re.finditer(sys.argv[2],text,re.I));print(s,'matches',len(matches));end=0
for m in matches:
 if m.start()<end:continue
 begin=max(0,m.start()-120);end=min(len(text),m.end()+800);print(text[begin:end]+'\n')
