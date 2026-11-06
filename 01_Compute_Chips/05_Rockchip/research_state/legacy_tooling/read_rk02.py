import pathlib,json,sys,re
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path(__file__).resolve().parent.parent/'01_Compute_Chips/05_Rockchip/reference_metrial'
r=json.loads((p/'_registry/materials.json').read_text(encoding='utf-8'))
for n in sys.argv[1].split(','):
 v=r.get(n,{})
 print('\nSOURCE',n,v.get('archive_status'),v.get('error',''))
 if not v.get('file'):continue
 f=pathlib.Path(v['file']);tf=f.with_name('text.txt')
 if f.suffix=='.pdf':tf=p/'derived/extracted'/f'{n}.txt'
 t=(tf if tf.exists() else f).read_text(encoding='utf-8')
 if len(sys.argv)<3:print(t[:35000])
 else:
  pat=sys.argv[2]
  end=0;count=0
  for m in re.finditer(pat,t,re.I):
   if m.start()<end:continue
   print(t[max(0,m.start()-120):m.end()+900]);end=m.end()+900;count+=1
   if count>=12:break
